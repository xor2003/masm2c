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

# ops that write result + all result flags (first operand is the destination)
FLAGOPS = {'ADD', 'SUB', 'ADC', 'SBB', 'AND', 'OR', 'XOR', 'INC', 'DEC', 'NEG'}
# shifts write ZF/SF/PF from the result only when the count is nonzero
# (the runtime macros early-out on count==0 leaving flags stale) — foldable
# only with a nonzero literal count
SHIFTOPS = {'SHL', 'SHR', 'SAR', 'SAL', 'SHLD', 'SHRD'}
# ops that update ONLY CF/OF or leave flags undefined must NOT pend 'result':
# their dest value is not the flag result, so JZ/JS folds would read the
# operand instead of the real flag — ROL/ROR/RCL/RCR, MUL*, IMUL*, DIV*,
# BT/BTS/BTR/BTC.  They fall through to the generic verbatim+kill path.
# ops emitted verbatim; none write flags
VERBATIM = {'XCHG', 'IN', 'OUT', 'CBW', 'CWD', 'CWDE', 'CLD', 'STD', 'CLI',
            'STI', 'NOP', 'PUSHA', 'POPA', 'PUSHAD', 'POPAD', 'XLAT', 'LEA',
            'BOUND', 'LDS', 'LES', 'MOVBE'}
# verbatim ops that clobber CF/all flags -> pending dies (no foldable producer)
FLAGWRITE = {'POPF', 'SAHF', 'IRET',
             'AAA', 'AAS', 'DAA', 'DAS', 'AAD', 'AAM'}
# verbatim ops that modify ONLY CF -> pending survives, but unsigned folds
# (which reconstruct CF from cmp operands) must defer to the real flag
CFLAG_MOD = {'CLC', 'STC', 'CMC'}
# verbatim ops that READ flags -> need the real flag state, not folds
FLAGREAD_OPS = {'LAHF', 'PUSHF', 'SALC'}
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
    in_s = in_d = False  # inside '...' char / "..." string literal
    prev = ''
    for c in s:
        if in_s:
            cur += c
            if c == "'" and prev != '\\':
                in_s = False
        elif in_d:
            cur += c
            if c == '"' and prev != '\\':
                in_d = False
        elif c == "'":
            in_s = True
            cur += c
        elif c == '"':
            in_d = True
            cur += c
        else:
            if c in '([{':
                depth += 1
            elif c in ')]}':
                depth -= 1
            if c == ',' and depth == 0:
                out.append(cur)
                cur = ''
            else:
                cur += c
        prev = c
    out.append(cur)
    return [a.strip() for a in out if a.strip() != '']


def _signed_cast(expr, bits):
    return {8: f"(signed char)({expr})", 32: f"(int)({expr})"}.get(bits, f"(short)({expr})")


def _nonzero_lit(expr):
    """True when `expr` is a nonzero integer literal (plain or cast)."""
    expr = expr.strip()
    while True:
        m = re.match(r'^\(\s*[a-zA-Z_][\w ]*\s*\)\s*(.*)$', expr)
        if not m or not re.match(r'^[-+(\d]', m.group(1).strip()):
            break
        expr = m.group(1).strip()
    while expr.startswith('(') and expr.endswith(')'):
        expr = expr[1:-1].strip()
    try:
        return int(expr.rstrip('uUlL'), 0) != 0
    except ValueError:
        return False


def _bits(expr):
    """Best-effort operand width in bits (8/16/32)."""
    # the operand's width is decided by the OUTERMOST dereference — the
    # first `*(`-deref's (TYPE*) cast, textually leftmost.  casts inside the
    # address computation itself (e.g. *((dw*)((db*)&v_view+vp_zft)) where
    # (db*) only types the base pointer) must not win: *(dw*) here is a
    # word operand even though a (db*) token also appears in the string
    m = re.search(r'\*\s*\(+\s*(db|dw|dd|byte|word|dword)\s*\*', expr)
    if m:
        t = m.group(1)
        if t in ('db', 'byte'):
            return 8
        if t in ('dd', 'dword'):
            return 32
        return 16
    # a bare *(raddr(...)) / *raddr derefs a db* -> byte
    if re.search(r'\*\s*\(?\s*raddr', expr):
        return 8
    # *((&arr)+i) element deref of a generated byte array -> byte
    if re.search(r'\*\s*\(+\s*&', expr):
        return 8
    if re.search(r'\bbyte_', expr):
        return 8
    if re.search(r'\bdword_', expr):
        return 32
    if re.search(r'\bword_', expr):
        return 16
    if re.search(r'\b(a|b|c|d)(l|h)\b', expr):
        return 8
    if re.search(r'\be(ax|bx|cx|dx|si|di|bp|sp)\b', expr):
        return 32
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
        self.pcf = False     # CF was modified after `pending` was recorded

    def _pend(self, kind, a, b):
        self.pending = (kind, a, b)
        self.pcf = False

    def _kill(self):
        self.pending = None
        self.pcf = False

    # -- condition folding ---------------------------------------------------
    def _cond(self, jcc):
        p = self.pending
        if p is not None:
            kind, a, b = p
            # CF changed since the flag op ran (clc/stc/cmc): unsigned jumps
            # can't be rebuilt from operands, use the materialized flag.
            if self.pcf and jcc in UNSIGNED:
                return FLAGREAD.get(jcc, '0')
            bits = _bits(a)
            if kind == 'cmp':
                t = {8: 'db', 32: 'dd'}.get(bits, 'dw')
                ca, cb = f"({t})({a})", f"({t})({b})"
                if jcc in UNSIGNED:
                    return f"{ca} {UNSIGNED[jcc]} {cb}"
                if jcc in EQUAL:
                    return f"{ca} {EQUAL[jcc]} {cb}"
                if jcc in SIGNED:
                    return f"{_signed_cast(a, bits)} {SIGNED[jcc]} {_signed_cast(b, bits)}"
            elif kind == 'test':
                if jcc in ('JZ', 'JE'):
                    return f"!({a} & {b})"
                if jcc in ('JNZ', 'JNE'):
                    return f"({a} & {b}) != 0"
                if jcc == 'JS':
                    return f"{_signed_cast(f'({a} & {b})', bits)} < 0"
                if jcc == 'JNS':
                    return f"{_signed_cast(f'({a} & {b})', bits)} >= 0"
                # TEST clears CF and OF
                if jcc in ('JC', 'JB', 'JNAE', 'JO'):
                    return '0'
                if jcc in ('JNC', 'JAE', 'JNB', 'JNO'):
                    return '1'
            else:  # 'result': flag macros already ran, folding only for ZF/SF
                if jcc in EQUAL:
                    return f"{a} {EQUAL[jcc]} 0"
                if jcc == 'JS':
                    return f"{_signed_cast(a, bits)} < 0"
                if jcc == 'JNS':
                    return f"{_signed_cast(a, bits)} >= 0"
        return FLAGREAD.get(jcc, '0')

    # -- operand-write invalidation ------------------------------------------
    def _invalidate_writes(self, written, mem_written):
        if self.pending is None:
            return
        if mem_written and _has_memref(self.pending[1] + self.pending[2]):
            self._kill()
            return
        # reg writes clobber the whole family (al kills ax/eax pending ops)
        if {_REGFAM.get(i, i) for i in written} & \
           (_ids(self.pending[1], fam=True) | _ids(self.pending[2], fam=True)):
            self._kill()

    def _dst_names(self, expr):
        """Identifiers a store into `expr` would clobber (incl. index regs)."""
        return _ids(expr)

    # -- R(...) --------------------------------------------------------------
    def op(self, inner):
        inner = inner.strip()
        # a trailing `;` inside R(...) (e.g. `R(CMP(x, y);)`) would otherwise
        # defeat the macro-call parse and lose the operand fold
        if inner.endswith(';'):
            inner = inner[:-1].strip()
        if not inner:
            return []
        # raw emitted statement (e.g. `eax = 3;`, `foo();`, `__disp = x;`)
        if not re.match(r'^[_A-Z][A-Z0-9_]*\s*(\(.*\)?)?\s*$', inner, re.S):
            stmt = inner if inner.endswith(';') else inner + ';'
            lhs = inner.split('=', 1)[0]
            self._invalidate_writes(self._dst_names(lhs), _has_memref(lhs))
            # a call (direct or via dispatch) may clobber any pending operand
            # or the flags themselves -> pending operands are unknowable
            if re.search(r'\b\w+\s*\(', inner) or \
               re.match(r'__disp\b|.*\bCALL_\b', inner):
                self._kill()
            # REP-prefixed / multiword string ops (`REP MOVSW`, `REPE SCASB`)
            # write si/di/cx and es:di memory and can restore/set flags
            if any(w in ('STOSB', 'STOSW', 'STOSD', 'MOVSB', 'MOVSW', 'MOVSD',
                         'LODSB', 'LODSW', 'LODSD', 'SCASB', 'SCASW', 'SCASD',
                         'CMPSB', 'CMPSW', 'CMPSD', 'INSB', 'INSW',
                         'OUTSB', 'OUTSW')
                   for w in inner.split()):
                self._kill()
            return [stmt]
        m = re.match(r'^(_?[A-Z][A-Z_0-9]*)\s*\((.*)\)\s*$', inner, re.S)
        if not m:
            words = inner.rstrip(';').split()
            if any(w in ('STOSB', 'STOSW', 'STOSD', 'MOVSB', 'MOVSW', 'MOVSD',
                         'LODSB', 'LODSW', 'LODSD', 'SCASB', 'SCASW', 'SCASD',
                         'CMPSB', 'CMPSW', 'CMPSD', 'INSB', 'INSW', 'OUTSB', 'OUTSW')
                   for w in words):
                self._kill()  # REP-prefixed / bare string op
                return [f"{{ {inner.rstrip(';')}; }}"]
            m2 = re.match(r'^(_?[A-Z][A-Z_0-9]*)\s*;?\s*$', inner)
            if m2:
                m = _BareMatch(m2.group(1))   # bare op name, no args
            else:
                self._kill()  # unparseable statement; flags unknowable
                return [f"{{ {inner.rstrip(';')}; }}"]
        name, argstr = m.group(1), m.group(2)
        args = split_args(argstr)
        a = args[0] if args else ''
        b = args[1] if len(args) > 1 else ''
        out = []

        if name == '_INT':
            out = [f"_INT({argstr});"]
            self._kill()
        elif name == 'CMP':
            # m2c::CMP_ computes all flags exactly; the fold keeps `if`s readable
            out = [f"CMP({a}, {b});"]
            self._pend('cmp', a, b)
        elif name == 'TEST':
            out = [f"TEST({a}, {b});"]
            self._pend('test', a, b)
        elif name in ASSIGN:
            # MOV is the one op whose stock expansion routes memory accesses
            # through m2c::setdata/getdata (mem_writeb/mem_readb -> VGA plane
            # emulation, latches, shadow memory).  A bare `a = b` on an m2c
            # raddr deref writes shadow memory but never reaches the VGA
            # pipeline, so wrap the access exactly like MOV_ does.
            if _has_memref(a):
                out = [f"m2c::setdata(&({a}), m2c::getdata({b}));"]
            elif _has_memref(b):
                out = [f"{a} = m2c::getdata({b});"]
            else:
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
            self._pend('result', a, '')
        elif name in SHIFTOPS:
            out = [f"{name}({argstr});"]
            # the macro early-outs on count==0 without touching flags, so a
            # result fold is only exact for a known-nonzero literal count
            cnt = args[2] if name in ('SHLD', 'SHRD') else b
            if _nonzero_lit(cnt):
                self._pend('result', a, '')
            else:
                self._kill()
        elif name in SETCC:
            cond = self._cond(SETCC[name])
            out = []
            # re-emitting the producer refreshes all flags — but that would
            # undo a clc/stc/cmc, so only when no CF divergence is pending
            if (self.pending is not None and self.pending[0] in ('cmp', 'test')
                    and not self.pcf
                    and cond == FLAGREAD.get(SETCC[name])):
                p = self.pending
                out.append(f"{p[0].upper()}({p[1]}, {p[2]});")
            out.append(f"{a} = ({cond});")
            self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name in ('PUSH', 'POP'):
            out = [f"{name}({argstr});"]
            if name == 'POP':
                self._invalidate_writes(self._dst_names(a), _has_memref(a))
        elif name in CFLAG_MOD:
            # clc/stc/cmc touch CF only: pending operands stay valid for
            # equality/sign folds, but unsigned folds must read the real CF
            out = [f"{name}({argstr});" if argstr else f"{name};"]
            self.pcf = True
        elif name in FLAGWRITE:
            out = [f"{name}({argstr});" if argstr else f"{name};"]
            self._kill()
        elif name in FLAGREAD_OPS:
            # the op reads real flag bits; if only CF/ZF were materialized,
            # recompute the pending producer so all flags are exact (not
            # when CF was diverted by clc/stc/cmc — a recompute would undo it)
            if (self.pending is not None and self.pending[0] in ('cmp', 'test')
                    and not self.pcf):
                p = self.pending
                out.append(f"{p[0].upper()}({p[1]}, {p[2]});")
            out.append(f"{name}({argstr});" if argstr else f"{name};")
            # LAHF/SALC write the a-reg, PUSHF writes sp
            self._invalidate_writes(
                ({'#a'} if name in ('LAHF', 'SALC') else set())
                | ({'#sp'} if name == 'PUSHF' else set()), False)
        elif name in VERBATIM:
            out = [f"{name}({argstr});" if argstr else f"{name};"]
            # these may still write registers/mem (XCHG, LEA, IN, CBW, XLAT, ...)
            self._invalidate_writes(
                _ids(argstr) | ({'#a'} if name in ('CBW', 'CWDE', 'XLAT') else set())
                | ({'#d'} if name in ('CWD', 'CWDE') else set())
                | ({'es'} if name == 'LES' else set())
                | ({'ds'} if name == 'LDS' else set())
                | ({'#a', '#b', '#c', '#d', '#si', '#di', '#bp', '#sp'}
                   if name in ('POPA', 'POPAD') else set()),
                _has_memref(argstr))
        else:
            out = [f"{name}({argstr});" if argstr else f"{name};"]
            self._kill()
        return out

    # -- J(...) --------------------------------------------------------------
    def jump(self, inner):
        inner = inner.strip()
        if inner.endswith(';'):
            inner = inner[:-1].strip()
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
            # the producer re-emit refreshes all flags — unsafe if a
            # clc/stc/cmc diverted CF in between, so gate on `pcf`
            if (self.pending is not None and self.pending[0] in ('cmp', 'test')
                    and not self.pcf
                    and cond == FLAGREAD.get(name)):
                p = self.pending
                pre.append(f"{p[0].upper()}({p[1]}, {p[2]});")
            pre.append(f"if ({cond}) {{goto {lbl};}}")
            return pre
        if name == 'JMP':
            self._kill()
            return [f"goto {lbl};"]
        if name in ('CALL', 'CALLF'):
            self._kill()
            rest = f", {args[1]}" if len(args) > 1 else ''
            return [f"CALL({lbl}{rest});" if name == 'CALL' else f"CALLF({lbl}{rest});"]
        if name in ('RETN', 'RETF', 'IRET', 'RET'):
            self._kill()
            return [f"{name}({argstr});" if argstr else f"{name};"]
        if name in ('LOOP', 'LOOPE', 'LOOPZ', 'LOOPNE', 'LOOPNZ', 'JCXZ', 'JECXZ'):
            self._kill()
            return [f"{name}({argstr});"]
        self._kill()
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
    in_s = in_d = False
    prev = ''
    while i < len(line) and depth:
        c = line[i]
        if in_s:
            if c == "'" and prev != '\\':
                in_s = False
        elif in_d:
            if c == '"' and prev != '\\':
                in_d = False
        elif c == "'":
            in_s = True
        elif c == '"':
            in_d = True
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        prev = c
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
            lf._kill()
            continue
        comment_m = re.search(r'//\s*(.*)$', ln)
        asm = _asm_text(comment_m.group(1)) if comment_m else ''
        indent = re.match(r'^\s*', ln).group(0)
        first = True
        for _pos, _end, kind, inner in spans:
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
    with open(path, encoding='utf-8', errors='replace') as f:
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
        with open(dst, encoding='utf-8', errors='replace') as f:
            text = include_re.sub(r'\1\2_lifted.cpp"', f.read())
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(text)
        result[p] = n
    return result
