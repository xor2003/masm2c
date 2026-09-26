"""Readable-C post-transform for generated fake-C (--lift).

Rewrites each ``R(<stmt>);`` / ``J(<jump>);`` line emitted by the Cpp backend
into readable C — direct assignments, folded flag conditions, ``goto``,
``CALL``/``RETN`` — while preserving the surrounding m2c proc skeleton
(signatures, ``X86_REGREF`` register refs, the ``__disp`` dispatch switch and
all data declarations) verbatim, so the result still runs on the asm.h
runtime and passes asmTests.

With ``--lift`` the readable variant is written to separate
``<name>_lifted.cpp`` siblings; the standard ``<name>.cpp`` output is left
untouched. Segment ``#include``s inside lifted files are repointed to the
``_lifted`` siblings, so a lifted set compiles independently of the stock
files. Only statement text is transformed; control flow structure is
unchanged.
"""

from __future__ import annotations

import logging
import os
import re

# ---------------------------------------------------------------------------
# jcc condition tables (same folding as tools/lift.py)
# ---------------------------------------------------------------------------

UNSIGNED = {'JC': '<', 'JB': '<', 'JNAE': '<', 'JNC': '>=', 'JAE': '>=', 'JNB': '>=',
            'JA': '>', 'JNBE': '>', 'JBE': '<=', 'JNA': '<='}
SIGNED = {'JL': '<', 'JNGE': '<', 'JGE': '>=', 'JNL': '>=',
          'JG': '>', 'JNLE': '>', 'JLE': '<=', 'JNG': '<='}
EQUAL = {'JZ': '==', 'JE': '==', 'JNZ': '!=', 'JNE': '!='}
# Fallback when folding is not possible: read the real flag (m2c X86_REGREF
# exposes CF/ZF/SF/OF as _state bools inside every proc).
FLAGREAD = {'JC': 'CF', 'JB': 'CF', 'JNAE': 'CF', 'JNC': '!CF', 'JAE': '!CF', 'JNB': '!CF',
            'JZ': 'ZF', 'JE': 'ZF', 'JNZ': '!ZF', 'JNE': '!ZF',
            'JS': 'SF', 'JNS': '!SF', 'JO': 'OF', 'JNO': '!OF',
            'JP': 'PF', 'JPE': 'PF', 'JNP': '!PF', 'JPO': '!PF',
            'JA': '(!CF && !ZF)', 'JNBE': '(!CF && !ZF)',
            'JBE': '(CF || ZF)', 'JNA': '(CF || ZF)',
            'JL': '(SF != OF)', 'JNGE': '(SF != OF)', 'JGE': '(SF == OF)', 'JNL': '(SF == OF)',
            'JG': '(!ZF && SF == OF)', 'JNLE': '(!ZF && SF == OF)',
            'JLE': '(ZF || SF != OF)', 'JNG': '(ZF || SF != OF)'}

# ops that write result + flags (first operand is the destination)
FLAGOPS = {'ADD', 'SUB', 'ADC', 'SBB', 'AND', 'OR', 'XOR', 'INC', 'DEC', 'NEG',
           'SHL', 'SHR', 'SAR', 'ROL', 'ROR', 'SHLD', 'SHRD', 'IMUL',
           'MUL1_1', 'MUL1_2', 'DIV2', 'BT', 'BTS', 'BTR', 'BTC'}
# ops emitted verbatim; none write flags
VERBATIM = {'XCHG', 'IN', 'OUT', 'CBW', 'CWD', 'CWDE', 'CLD', 'STD', 'CLI',
            'STI', 'NOP', 'PUSHA', 'POPA', 'PUSHAD', 'POPAD', 'XLAT', 'LEA',
            'BOUND', 'LDS', 'LES', 'MOVBE'}
# verbatim ops that clobber CF/all flags -> pending dies (no foldable producer)
FLAGWRITE = {'CLC', 'STC', 'CMC', 'POPF', 'SAHF', 'IRET',
             'AAA', 'AAS', 'DAA', 'DAS', 'AAD', 'AAM'}
# verbatim ops that READ flags -> need the real flag state, not folds
FLAGREAD_OPS = {'LAHF', 'PUSHF'}
ASSIGN = {'MOV'}
# zero/sign-extension loads have real semantics; keep the runtime macro
EXT_OPS = {'MOVZX', 'MOVSX'}
SETCC = {'SETZ': 'JZ', 'SETNZ': 'JNZ', 'SETE': 'JZ', 'SETNE': 'JNZ',
         'SETB': 'JC', 'SETC': 'JC', 'SETAE': 'JNC', 'SETNC': 'JNC',
         'SETBE': 'JBE', 'SETA': 'JA', 'SETS': 'JS', 'SETNS': 'JNS',
         'SETO': 'JO', 'SETNO': 'JNO', 'SETP': 'JP', 'SETNP': 'JNP',
         'SETL': 'JL', 'SETGE': 'JGE', 'SETLE': 'JLE', 'SETG': 'JG',
         'SETNLE': 'JG', 'SETNGE': 'JL', 'SETNAE': 'JC', 'SETNB': 'JNC'}

_TYPEWORDS = {'db', 'dw', 'dd', 'raddr', 'raddr_', 'offset', 'seg_offset',
              'm2c', 'short', 'int', 'char', 'unsigned', 'long', 'signed',
              'dwb', 'mem', 'realAddress', 'if', 'sizeof', 'volatile'}
_ID_RE = re.compile(r'\b[a-zA-Z_][\w]*\b')

RE_ASM_COMMENT = re.compile(r'^\s*\d+\s+(.*?)\s*$')


_REGFAM = {}
for _fam, _names in {
    'a': ('eax', 'ax', 'al', 'ah'), 'b': ('ebx', 'bx', 'bl', 'bh'),
    'c': ('ecx', 'cx', 'cl', 'ch'), 'd': ('edx', 'dx', 'dl', 'dh'),
    'si': ('esi', 'si'), 'di': ('edi', 'di'),
    'bp': ('ebp', 'bp'), 'sp': ('esp', 'sp'),
}.items():
    for _n in _names:
        _REGFAM[_n] = f"#{_fam}"


def _ids(expr, fam=False):
    ids = {i for i in _ID_RE.findall(expr) if i not in _TYPEWORDS}
    if fam:
        return {_REGFAM.get(i, i) for i in ids}
    return ids


def _has_memref(expr):
    return ('*' in expr) or ('raddr' in expr) or re.search(r'\b(word_|byte_|dword_|seg_|mem\b)', expr) is not None


def split_args(s):
    out, depth, cur = [], 0, ''
    for c in s:
        if c in '([{': depth += 1
        if c in ')]}': depth -= 1
        if c == ',' and depth == 0:
            out.append(cur); cur = ''
        else: cur += c
    out.append(cur)
    return [a.strip() for a in out if a.strip() != '']


def _signed_cast(expr, bits):
    return {8: f"(char)({expr})", 32: f"(int)({expr})"}.get(bits, f"(short)({expr})")


def _bits(expr):
    """Best-effort operand width in bits (8/16/32)."""
    if re.search(r'\*\s*\(\s*db\s*\*|\*\s*\(\s*byte\s*\*|\bbyte_', expr): return 8
    if re.search(r'\*\s*\(\s*dd\s*\*|\*\s*\(\s*dword\s*\*|\bdword_', expr): return 32
    if re.search(r'\b(a|b|c|d)(l|h)\b', expr): return 8
    if re.search(r'\be(ax|bx|cx|dx|si|di|bp|sp)\b', expr): return 32
    return 16





class _BareMatch:
    def __init__(self, name):
        self._name = name
    def group(self, n):
        return self._name if n == 1 else ''


class _Lifter:
    """Sequential pending-flag state for one straight-line text run."""

    def __init__(self):
        self.pending = None  # ('cmp'|'test'|'result', a, b)

    # -- condition folding ---------------------------------------------------
    def _cond(self, jcc):
        p = self.pending
        if p is not None:
            kind, a, b = p
            bits = _bits(a)
            if kind == 'cmp':
                t = {8: 'db', 32: 'dd'}.get(bits, 'dw')
                ca, cb = f"({t})({a})", f"({t})({b})"
                if jcc in UNSIGNED: return f"{ca} {UNSIGNED[jcc]} {cb}"
                if jcc in EQUAL:    return f"{ca} {EQUAL[jcc]} {cb}"
                if jcc in SIGNED:
                    return f"{_signed_cast(a, bits)} {SIGNED[jcc]} {_signed_cast(b, bits)}"
            elif kind == 'test':
                if jcc in ('JZ', 'JE'):   return f"!({a} & {b})"
                if jcc in ('JNZ', 'JNE'): return f"({a} & {b}) != 0"
                if jcc == 'JS':  return f"{_signed_cast(f'({a} & {b})', bits)} < 0"
                if jcc == 'JNS': return f"{_signed_cast(f'({a} & {b})', bits)} >= 0"
                # TEST clears CF and OF
                if jcc in ('JC', 'JB', 'JNAE', 'JO'):  return '0'
                if jcc in ('JNC', 'JAE', 'JNB', 'JNO'): return '1'
            else:  # 'result': flag macros already ran, folding only for ZF/SF
                if jcc in EQUAL: return f"{a} {EQUAL[jcc]} 0"
                if jcc == 'JS':  return f"{_signed_cast(a, bits)} < 0"
                if jcc == 'JNS': return f"{_signed_cast(a, bits)} >= 0"
        return FLAGREAD.get(jcc, '0')

    # -- operand-write invalidation ------------------------------------------
    def _invalidate_writes(self, written, mem_written):
        if self.pending is None:
            return
        if mem_written and _has_memref(self.pending[1] + self.pending[2]):
            self.pending = None
            return
        # reg writes clobber the whole family (al kills ax/eax pending ops)
        if {_REGFAM.get(i, i) for i in written} & \
           (_ids(self.pending[1], fam=True) | _ids(self.pending[2], fam=True)):
            self.pending = None

    def _dst_names(self, expr):
        """Identifiers a store into `expr` would clobber (incl. index regs)."""
        return _ids(expr)

    # -- R(...) --------------------------------------------------------------
    def op(self, inner):
        inner = inner.strip()
        if not inner:
            return []
        # raw emitted statement (e.g. `eax = 3;`, `foo();`, `__disp = x;`)
        if not re.match(r'^[_A-Z][A-Z0-9_]*\s*(\(.*\)?)?\s*$', inner, re.S):
            stmt = inner if inner.endswith(';') else inner + ';'
            lhs = inner.split('=', 1)[0]
            self._invalidate_writes(self._dst_names(lhs), _has_memref(lhs))
            if re.match(r'__disp\b|.*\bCALL_\b', inner):
                self.pending = None
            return [stmt]
        m = re.match(r'^(_?[A-Z][A-Z_0-9]*)\s*\((.*)\)\s*$', inner, re.S)
        if not m:
            words = inner.rstrip(';').split()
            if any(w in ('STOSB', 'STOSW', 'STOSD', 'MOVSB', 'MOVSW', 'MOVSD',
                         'LODSB', 'LODSW', 'LODSD', 'SCASB', 'SCASW', 'SCASD',
                         'CMPSB', 'CMPSW', 'CMPSD', 'INSB', 'INSW', 'OUTSB', 'OUTSW')
                   for w in words):
                self.pending = None  # REP-prefixed / bare string op
                return [f"{{ {inner.rstrip(';')}; }}"]
            m2 = re.match(r'^(_?[A-Z][A-Z_0-9]*)\s*;?\s*$', inner)
            if m2:
                m = _BareMatch(m2.group(1))   # bare op name, no args
            else:
                return [f"{{ {inner.rstrip(';')}; }}"]
        name, argstr = m.group(1), m.group(2)
        args = split_args(argstr)
        a = args[0] if args else ''
        b = args[1] if len(args) > 1 else ''
        out = []

        if name == '_INT':
            out = [f"_INT({argstr});"]
            self.pending = None
        elif name == 'CMP':
            # m2c::CMP_ computes all flags exactly; the fold keeps `if`s readable
            out = [f"CMP({a}, {b});"]
            self.pending = ('cmp', a, b)
        elif name == 'TEST':
            out = [f"TEST({a}, {b});"]
            self.pending = ('test', a, b)
        elif name in ASSIGN:
            out = [f"{a} = {b};"]
            self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name in EXT_OPS:
            out = [f"{name}({a}, {b});"]
            self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name == 'NOT':
            out = [f"{a} = ~{a};"]
            self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name in FLAGOPS:
            out = [f"{name}({argstr});"]
            self.pending = ('result', a, '')
        elif name in SETCC:
            cond = self._cond(SETCC[name])
            out = []
            if (self.pending is not None and self.pending[0] in ('cmp', 'test')
                    and cond == FLAGREAD.get(SETCC[name])):
                p = self.pending
                out.append(f"{p[0].upper()}({p[1]}, {p[2]});")
            out.append(f"{a} = ({cond});")
            self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name in ('PUSH', 'POP'):
            out = [f"{name}({argstr});"]
            if name == 'POP':
                self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name in FLAGWRITE:
            out = [f"{name}({argstr});" if argstr else f"{name};"]
            self.pending = None
        elif name in FLAGREAD_OPS:
            # the op reads real flag bits; if only CF/ZF were materialized,
            # recompute the pending producer so all flags are exact
            if self.pending is not None and self.pending[0] in ('cmp', 'test'):
                p = self.pending
                out.append(f"{p[0].upper()}({p[1]}, {p[2]});")
            out.append(f"{name}({argstr});" if argstr else f"{name};")
        elif name in VERBATIM:
            out = [f"{name}({argstr});" if argstr else f"{name};"]
            # these may still write registers/mem (XCHG, LEA, IN, CBW, XLAT, ...)
            self._invalidate_writes(
                _ids(argstr) | ({'#a'} if name in ('CBW', 'CWDE', 'XLAT') else set())
                | ({'#d'} if name in ('CWD', 'CWDE') else set())
                | ({'#a', '#b', '#c', '#d', '#si', '#di', '#bp', '#sp'}
                   if name in ('POPA', 'POPAD') else set()),
                _has_memref(a))
        else:
            out = [f"{name}({argstr});"]
            self.pending = None
        return out

    # -- J(...) --------------------------------------------------------------
    def jump(self, inner):
        inner = inner.strip()
        m = re.match(r'^([A-Z][A-Z_0-9]*)\s*\((.*)\)\s*$', inner, re.S)
        if not m:
            return [f"J({inner});"]
        name, argstr = m.group(1), m.group(2)
        args = split_args(argstr)
        lbl = args[0] if args else ''

        if name in UNSIGNED or name in SIGNED or name in EQUAL or \
           name in ('JS', 'JNS', 'JO', 'JNO', 'JP', 'JPE', 'JNP', 'JPO'):
            cond = self._cond(name)
            pre = []
            if (self.pending is not None and self.pending[0] in ('cmp', 'test')
                    and cond == FLAGREAD.get(name)):
                p = self.pending
                pre.append(f"{p[0].upper()}({p[1]}, {p[2]});")
            pre.append(f"if ({cond}) {{goto {lbl};}}")
            return pre
        if name == 'JMP':
            self.pending = None
            return [f"goto {lbl};"]
        if name in ('CALL', 'CALLF'):
            self.pending = None
            rest = f", {args[1]}" if len(args) > 1 else ''
            return [f"CALL({lbl}{rest});" if name == 'CALL' else f"CALLF({lbl}{rest});"]
        if name in ('RETN', 'RETF', 'IRET', 'RET'):
            self.pending = None
            return [f"{name}({argstr});" if argstr else f"{name};"]
        if name in ('LOOP', 'LOOPE', 'LOOPZ', 'LOOPNE', 'LOOPNZ', 'JCXZ', 'JECXZ'):
            self.pending = None
            return [f"{name}({argstr});"]
        self.pending = None
        return [f"J({inner});"]


def _asm_text(comment):
    """Turn the trailing generated comment into the /* asm */ body."""
    if not comment:
        return ''
    c = comment.strip()
    m = RE_ASM_COMMENT.match(c)
    body = m.group(1) if m else c
    return body.replace('*/', '* /').strip()


_STMT_RE = re.compile(r'\b([RJ])\(')


def _extract_stmt(line, pos):
    """`line[pos:]` starts `R(`/`J(` -> (kind, inner, end_pos) or None."""
    i = pos + 2  # past 'X('
    depth = 1
    while i < len(line) and depth:
        c = line[i]
        if c == '(': depth += 1
        elif c == ')': depth -= 1
        i += 1
    if depth:
        return None
    return line[pos], line[pos + 2:i - 1], i


def lift_cpp_text(text):
    """Return (lifted_text, changed_count) for generated C++ source text."""
    out = []
    lf = _Lifter()
    changed = 0
    for ln in text.splitlines():
        # find R(/J( statement spans (may be several per line)
        spans = []
        for sm in _STMT_RE.finditer(ln):
            pos = sm.start()
            if spans and pos < spans[-1][1]:
                continue  # inside a previous span
            pre = ln[:pos]
            if '//' in pre or '/*' in pre:
                continue  # inside a comment
            pre_s = pre.strip()
            if pre_s and not pre_s.endswith((';', '{', '}')):
                continue  # not at a statement boundary (e.g. `= R(x)`)
            ext = _extract_stmt(ln, pos)
            if ext:
                spans.append((pos, ext[2], ext[0], ext[1]))
        if not spans:
            out.append(ln)
            s = ln.strip()
            if not s or s.startswith('//') or s.startswith('/*'):
                continue  # comments/blanks don't disturb pending flags
            lf.pending = None
            continue
        comment_m = re.search(r'//\s*(.*)$', ln)
        asm = _asm_text(comment_m.group(1)) if comment_m else ''
        indent = re.match(r'^\s*', ln).group(0)
        first = True
        for pos, end, kind, inner in spans:
            stmts = lf.op(inner) if kind == 'R' else lf.jump(inner)
            if first and asm:
                out.append(f"{indent}/* {asm} */")
            for st in stmts:
                out.append(f"{indent}{st}")
            first = False
            changed += 1
    return '\n'.join(out) + '\n', changed


def lift_cpp_file(path, dst=None):
    """Lift `path`; writes to `dst` (separate file) or in-place. Returns count."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        lifted, changed = lift_cpp_text(f.read())
    if changed or dst:
        with open(dst or path, 'w', encoding='utf-8') as f:
            f.write(lifted)
    logging.info("lift: %s -> %s (%d statements rewritten)",
                 path, dst or path, changed)
    return changed


def lifted_name(path):
    stem, _ = os.path.splitext(path)
    return f"{stem}_lifted.cpp"


def lift_cpp_files(paths):
    """Write ``*_lifted.cpp`` siblings for each generated .cpp in `paths`.

    Segment ``#include "x.cpp"`` lines in lifted output are repointed to the
    lifted siblings so the lifted set is self-consistent.
    """
    stems = {os.path.splitext(os.path.basename(p))[0] for p in paths}
    include_re = re.compile(
        r'(#include\s+")(' + '|'.join(re.escape(s) for s in sorted(stems)) + r')\.cpp"')
    result = {}
    for p in paths:
        dst = lifted_name(p)
        n = lift_cpp_file(p, dst=dst)
        with open(dst, 'r', encoding='utf-8', errors='replace') as f:
            text = include_re.sub(r'\1\2_lifted.cpp"', f.read())
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(text)
        result[p] = n
    return result
