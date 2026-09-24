#!/usr/bin/python3
# Masm2c S2S translator (initially based on SCUMMVM tasmrecover)
#
# Masm2c is the legal property of its developers, whose names
# are too numerous to list here. Please refer to the COPYRIGHT
# file distributed with this source distribution.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
try:
    from rich import print  # type: ignore[import-not-found]
    from rich.traceback import install  # type: ignore[import-not-found]
    install(show_locals=True)
except Exception:
    pass

import argparse
import ast
import concurrent.futures
import glob
import logging
import os
import re
import sys
import traceback

from typing import Any

from .cpp import Cpp
from .parser import Parser
from .Token import Token as Token_

__version__ = "0.9.8"

__author__ = "x0r"
__copyright__ = "x0r"
__license__ = "GPL2+"

_logger = logging.getLogger(__name__)

_ASM_IDENTIFIER = r"[A-Za-z_@$?.][A-Za-z0-9_@$?.]*"
_EQUATE_ASSIGNMENT_RE = re.compile(
    rf"^\s*(?P<name>{_ASM_IDENTIFIER})\s*(?:=|\bEQU\b)\s*(?P<expr>[^;\r\n]+)",
    flags=re.IGNORECASE,
)
_INCLUDE_RE = re.compile(r"^\s*INCLUDE\s+(?P<path>[^;\r\n]+)", flags=re.IGNORECASE)
_C_EQUATE_DEFINE_RE = re.compile(
    rf"^\s*#\s*define\s+(?P<name>{_ASM_IDENTIFIER})\s+(?P<expr>[^\r\n]+)"
)
_C_STATIC_CONST_RE = re.compile(
    rf"^\s*static\s+const\s+(?:int|dd|dw|size_t)\s+(?P<name>{_ASM_IDENTIFIER})\s*=\s*(?P<expr>[^;\r\n]+)"
)


def default_jobs() -> int:
    return max(1, int(os.environ.get("JOBS", os.cpu_count() or 1)))


def tracefunc(frame, event, arg, indent=None):
    if indent is None:
        indent = [0]
    if event == "call":
        indent[0] += 2
        print("-" * indent[0] + "> call function", frame.f_code.co_filename, frame.f_code.co_name)
    elif event == "return":
        print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
        indent[0] -= 2
    return tracefunc


def parse_args(args):
    """Parse command line parameters.

    Args:
    ----
      args ([str]): command line parameters as list of strings

    Returns:
    -------
      :obj:`argparse.Namespace`: command line parameters namespace

    """
    aparser = argparse.ArgumentParser(description=f"Masm source to C++ translator V{__version__} {__license__}", prefix_chars="-")
    aparser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__version__}",
    )
    aparser.add_argument(
        "-d",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        default=logging.INFO,
        const=logging.DEBUG,
    )
    aparser.add_argument(
        "-FL",
        "--list",
        dest="list",
        help="Generate all globals to .list file",
        action="store_const",
        const=True,
        default=False,
    )
    aparser.add_argument(
        "-p",
        "--passes",
        dest="passes",
        help="How many parsing passes (default: 2)",
        type=int,
        choices=[1, 2],
        default=2,
    )
    aparser.add_argument(
        "-j",
        "--jobs",
        dest="jobs",
        help="How many source files to translate in parallel (default: CPU count)",
        type=int,
        default=default_jobs(),
    )
    aparser.add_argument(
        "-lo",
        "--loadsegment",
        dest="loadsegment",
        help="Dosbox 0.74.3 loads .exe from 0x1a2 para (w/o debugger), 0x1ed (with debugger), .com from 0x192 (w/o debugger)",
        action="store",
        default="0x1a2",
    )
    aparser.add_argument(
        "-AT",
        dest="loadsegment",
        help="Dosbox 0.74.3 loads .com from 0x192 (w/o debugger)",
        action="store_const",
        const="0x192",
    )
    aparser.add_argument(
        "-m", "--mergeprocs", type=str, default="separate", choices=["separate", "persegment", "single"],
        help="How to merge procs (default: persegment)" )
    aparser.add_argument(
        "--dce",
        action="store_true",
        default=False,
        help="Enable conservative dead-code elimination inside parsed procs",
    )
    aparser.add_argument(
        "--metrics",
        action="store_true",
        default=False,
        help="Print simple per-proc complexity metrics",
    )
    aparser.add_argument("filenames", nargs="+", help="Assembler source .asm Masm 6 or .lst from IDA Pro or .seg Segment dump to merge")
    return aparser.parse_args(args)


def setup_logging(name, loglevel):
    """Setup basic logging.

    Args:
    ----
    loglevel (int): minimum loglevel for emitting messages

    """
    root = logging.getLogger()
    root.setLevel(loglevel)

    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")
    err_handler.setFormatter(formatter)

    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setLevel(loglevel)

    if name:
        if "*" in name:
            name = "masm2c"
        file_handler = logging.FileHandler(f"{name}.log", "w", "utf-8")
        file_handler.setLevel(loglevel)
        formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")
        file_handler.setFormatter(formatter)

        logging.basicConfig(
            handlers=[err_handler, out_handler, file_handler],
            level=loglevel,
            force=True,
        )
    else:
        logging.basicConfig(
            handlers=[err_handler, out_handler],
            level=loglevel,
            force=True,
        )


def process(name, args):
    module_names = args.get("module_names") or {}
    if name in module_names:
        outname = module_names[name]
    elif m := re.match(r"(.+)\.(?:asm|lst)", name.lower()):
        outname = m[1].strip()
    else:
        outname = ""
    p = Parser(args)

    counter = Parser.c_dummy_label[0]

    p.parse_rt_info(outname)
    if args.get("passes") >= 2:
        p.parse_file(name)
        p.next_pass(counter)

    context = p.parse_file(name)

    if args.get("dce") or args.get("metrics"):
        from .proc import Proc
        total_removed = 0
        total_metrics = {
            "procs": 0,
            "statements": 0,
            "labels": 0,
            "flow_changes": 0,
            "terminators": 0,
            "branch_points": 0,
            "cyclomatic": 0,
        }
        for proc_name in context.proc_list:
            proc_obj = context.symbols.get_global(proc_name)
            if not isinstance(proc_obj, Proc):
                continue
            if args.get("dce"):
                total_removed += proc_obj.optimize()
            if args.get("metrics"):
                m = proc_obj.complexity_metrics()
                total_metrics["procs"] += 1
                for key in ("statements", "labels", "flow_changes", "terminators", "branch_points", "cyclomatic"):
                    total_metrics[key] += m[key]
                logging.info(
                    "metrics proc=%s stmts=%d labels=%d flow=%d terms=%d branches=%d cc=%d",
                    proc_name,
                    m["statements"],
                    m["labels"],
                    m["flow_changes"],
                    m["terminators"],
                    m["branch_points"],
                    m["cyclomatic"],
                )
        if args.get("dce"):
            logging.info("DCE summary removed=%d", total_removed)
        if args.get("metrics"):
            logging.info(
                "metrics total procs=%d stmts=%d labels=%d flow=%d terms=%d branches=%d cc=%d",
                total_metrics["procs"],
                total_metrics["statements"],
                total_metrics["labels"],
                total_metrics["flow_changes"],
                total_metrics["terminators"],
                total_metrics["branch_points"],
                total_metrics["cyclomatic"],
            )

    generator = Cpp(context, outfile=outname)
    generator.process()
    generator.save_cpp_files(name)  # start routine
    if args.get("list"):
        generator.dump_globals()
    return generator


def _process_source_worker(name: str, args: dict) -> str:
    setup_logging(name, args["loglevel"])
    try:
        process(name, args)
    except Exception:
        # Some exception types (e.g. lark.VisitError) do not survive pickling
        # back to the parent process.  Re-raise a picklable error that carries
        # the full traceback text so the failure is diagnosable.
        raise RuntimeError(f"Failed translating {name}\n{traceback.format_exc()}") from None
    return name


def should_merge_data_segments(files: list[str]) -> bool:
    """Multi-module builds need linked segment merging even when some inputs are listings."""
    asm_sources = [file for file in files if file.lower().endswith((".asm", ".lst"))]
    return not (len(asm_sources) == 1 and asm_sources[0].lower().endswith(".lst"))


def source_files(files: list[str]) -> list[str]:
    return [file for file in files if file.lower().endswith((".asm", ".lst"))]


def _strip_asm_comment(line: str) -> str:
    """Return source text before an assembler comment."""
    return line.split(";", 1)[0]


def _resolve_include_path(raw_path: str, current_dir: str) -> str | None:
    """Resolve an INCLUDE operand relative to the including source file."""
    include_name = raw_path.strip().strip("\"'<>")
    if not include_name:
        return None
    candidates = [include_name]
    if not os.path.isabs(include_name):
        candidates.insert(0, os.path.join(current_dir, include_name))
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return None


def _iter_source_and_include_lines(sources: list[str]) -> list[str]:
    """Read source files plus directly reachable INCLUDE files."""
    lines: list[str] = []
    pending = list(sources)
    seen: set[str] = set()
    while pending:
        path = pending.pop()
        try:
            real_path = os.path.realpath(path)
        except OSError:
            continue
        if real_path in seen:
            continue
        seen.add(real_path)
        current_dir = os.path.dirname(real_path)
        try:
            with open(real_path, encoding="utf-8", errors="ignore") as handle:
                file_lines = handle.readlines()
        except OSError:
            continue
        for line in file_lines:
            stripped = _strip_asm_comment(line)
            lines.append(stripped)
            if include_match := _INCLUDE_RE.match(stripped):
                include_path = _resolve_include_path(include_match.group("path"), current_dir)
                if include_path is not None:
                    pending.append(include_path)
    return lines


def _iter_existing_equates_header_lines(sources: list[str]) -> list[str]:
    """Read existing aggregate equates headers that can seed a new translation."""
    candidates = {os.path.realpath("_equates.h")}
    for source in sources:
        candidates.add(os.path.realpath(os.path.join(os.path.dirname(source), "_equates.h")))

    lines: list[str] = []
    for path in sorted(candidates):
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                lines.extend(handle.readlines())
        except OSError:
            continue
    return lines


def _collect_numeric_header_equate_candidates(sources: list[str]) -> dict[str, list[str]]:
    """Collect simple numeric equates from existing generated headers."""
    candidates: dict[str, list[str]] = {}
    for line in _iter_existing_equates_header_lines(sources):
        match = _C_EQUATE_DEFINE_RE.match(line) or _C_STATIC_CONST_RE.match(line)
        if not match:
            continue
        name = Parser.mangle_label(match.group("name"))
        expr = match.group("expr").strip()
        candidates.setdefault(name, []).append(expr)
    return candidates


def _replace_masm_number_suffixes(expr: str) -> str:
    """Convert MASM numeric suffix literals to Python integer literals."""
    expr = re.sub(
        r"(?<![A-Za-z0-9_@$?.])([01]+)[Bb](?![A-Za-z0-9_@$?.])",
        lambda match: str(int(match.group(1), 2)),
        expr,
    )
    expr = re.sub(
        r"(?<![A-Za-z0-9_@$?.])([0-9]+)[Dd](?![A-Za-z0-9_@$?.])",
        r"\1",
        expr,
    )
    expr = re.sub(
        r"(?<![A-Za-z0-9_@$?.])([0-7]+)[OoQq](?![A-Za-z0-9_@$?.])",
        lambda match: str(int(match.group(1), 8)),
        expr,
    )
    return re.sub(
        r"(?<![A-Za-z0-9_@$?.])([0-9][0-9A-Fa-f]*)[Hh](?![A-Za-z0-9_@$?.])",
        lambda match: str(int(match.group(1), 16)),
        expr,
    )


def _eval_simple_numeric_equate(expr: str, values: dict[str, int]) -> int | None:
    """Evaluate simple numeric MASM equate expressions using known symbols."""
    if any(quote in expr for quote in ("'", '"', "`", "<", ">")):
        return None
    expr = _replace_masm_number_suffixes(expr)
    expr = re.sub(r"\bMOD\b", "%", expr, flags=re.IGNORECASE)

    def replace_identifier(match: re.Match[str]) -> str:
        name = Parser.mangle_label(match.group(0))
        if name not in values:
            raise KeyError(name)
        return str(values[name])

    try:
        expr = re.sub(_ASM_IDENTIFIER, replace_identifier, expr)
    except KeyError:
        return None
    if re.search(r"[^0-9\s()+\-*/%]", expr):
        return None
    expr = expr.replace("/", "//")
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError:
        return None

    def eval_node(node: ast.AST) -> int:
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return int(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = eval_node(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod)):
            left = eval_node(node.left)
            right = eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if right == 0:
                raise ZeroDivisionError
            if isinstance(node.op, ast.FloorDiv):
                return left // right
            return left % right
        raise ValueError(type(node).__name__)

    try:
        return eval_node(parsed)
    except (ValueError, ZeroDivisionError):
        return None


def _collect_one_source_exports(
    source: str, args_dict: dict, base_counter: int
) -> tuple[set[str], set[str], set[str], set[str]]:
    """Parse one source and report its cross-module code symbol sets.

    Returns (extern procs, offset consumers, unresolved references, public
    code definitions).  Runs in worker processes under ``-j``; per-source
    state is independent, so parallel union is equivalent to the serial loop.
    """
    from . import op
    from .proc import Proc

    parser = Parser(args_dict.copy())
    try:
        if match := re.match(r"(.+)\.(?:asm|lst)", source.lower()):
            parser.parse_rt_info(match[1].strip())
        if (args_dict.get("passes") or 0) >= 2:
            parser.parse_file(source)
            parser.next_pass(base_counter)
        parser.parse_file(source)
    except (Exception, SystemExit):
        logging.exception("Failed collecting exports from %s", source)
        return set(), set(), set(), set()
    external_exports = set(parser.externals_procs)
    offset_consumers = set(parser.externals_vars) | set(parser.externals_abs)
    known_symbols = set(parser.symbols.get_globals())
    unresolved_references: set[str] = set()
    for symbol in parser.symbols.get_globals().values():
        if not hasattr(symbol, "stmts"):
            continue
        labels: list[Any] = list(Token_.find_tokens(getattr(symbol, "stmts", []), "LABEL") or [])
        labels += list(Token_.find_tokens(getattr(symbol, "stmts", []), "COMMON") or [])
        unresolved_references.update(str(label) for label in labels if str(label) not in known_symbols)
    public_definitions = {
        name
        for name in parser.public_symbols
        if isinstance(parser.symbols.get_global(name), (op.label, Proc))
    }
    return external_exports, offset_consumers, unresolved_references, public_definitions


def collect_code_exports(sources: list[str], args: argparse.Namespace) -> tuple[set[str], set[str]]:
    """Collect cross-module code symbols from this translation set."""
    if len(sources) <= 1:
        return set(), set()

    external_exports: set[str] = set()
    external_offset_consumers: set[str] = set()
    public_definitions: set[str] = set()
    unresolved_references: set[str] = set()
    args_dict = vars(args).copy()
    saved_counter = Parser.c_dummy_label[0]
    jobs = max(1, min(getattr(args, "jobs", 1) or 1, len(sources)))
    try:
        if jobs == 1:
            results = [
                _collect_one_source_exports(source, args_dict.copy(), saved_counter)
                for source in sources
            ]
        else:
            with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
                results = list(
                    executor.map(
                        _collect_one_source_exports,
                        sources,
                        [args_dict.copy() for _ in sources],
                        [saved_counter] * len(sources),
                    )
                )
        for exports, consumers, unresolved, publics in results:
            external_exports.update(exports)
            external_offset_consumers.update(consumers)
            unresolved_references.update(unresolved)
            public_definitions.update(publics)
    finally:
        Parser.c_dummy_label[0] = saved_counter
    return external_exports, public_definitions & (unresolved_references | external_offset_consumers | external_exports)


def collect_shared_equates(sources: list[str], args: argparse.Namespace) -> dict[str, str]:
    """Collect simple numeric equates for sibling modules in this translation set."""
    if len(sources) <= 1:
        return {}

    candidates = _collect_numeric_header_equate_candidates(sources)
    for line in _iter_source_and_include_lines(sources):
        if match := _EQUATE_ASSIGNMENT_RE.match(line):
            name = Parser.mangle_label(match.group("name"))
            expr = match.group("expr").strip()
            if "$" in expr and name in candidates:
                continue
            candidates.setdefault(name, []).append(expr)

    final_expressions = {name: expressions[-1] for name, expressions in candidates.items() if expressions}
    values: dict[str, int] = {}
    while True:
        progress = False
        for name, expression in final_expressions.items():
            if name in values:
                continue
            value = _eval_simple_numeric_equate(expression, values)
            if value is None:
                continue
            values[name] = value
            progress = True
        if not progress:
            break

    return {name: str(values[name]) for name in final_expressions if name in values}


def filter_code_symbol_equates(
    shared_equates: dict[str, str],
    external_code_exports: set[str],
    public_code_exports: set[str],
) -> dict[str, str]:
    """Remove numeric seeds for names owned by cross-module code symbols."""
    code_symbols = external_code_exports | public_code_exports
    return {name: value for name, value in shared_equates.items() if name not in code_symbols}


def module_names_for_sources(sources: list[str]) -> dict[str, str]:
    """Return distinct module names for sources sharing the same basename."""
    by_basename: dict[str, list[str]] = {}
    for source in sources:
        base = os.path.splitext(os.path.basename(source))[0].lower()
        by_basename.setdefault(base, []).append(source)
    names: dict[str, str] = {}
    for base, paths in by_basename.items():
        if len(paths) < 2:
            continue
        for path in paths:
            parent = os.path.basename(os.path.dirname(os.path.abspath(path))).lower() or "mod"
            names[path] = re.sub(r"[^A-Za-z0-9_]", "_", f"{parent}_{base}")
    return names


def process_source_files(files: list[str], args: argparse.Namespace) -> None:
    sources = source_files(files)
    if not sources:
        return

    args_dict = vars(args).copy()
    args_dict["module_names"] = module_names_for_sources(sources)
    args.module_names = args_dict["module_names"]
    external_code_exports, public_code_exports = collect_code_exports(sources, args)
    shared_equates = filter_code_symbol_equates(
        collect_shared_equates(sources, args),
        external_code_exports,
        public_code_exports,
    )
    args_dict["external_code_exports"] = sorted(external_code_exports)
    args_dict["public_code_exports"] = sorted(public_code_exports)
    args_dict["shared_equates"] = shared_equates
    args.external_code_exports = args_dict["external_code_exports"]
    args.public_code_exports = args_dict["public_code_exports"]
    args.shared_equates = shared_equates
    jobs = max(1, min(args.jobs, len(sources)))
    failed: list[str] = []
    if jobs == 1:
        for source in sources:
            try:
                _process_source_worker(source, args_dict)
            except SystemExit:
                if len(sources) == 1:
                    raise
                logging.exception("Failed translating %s", source)
                failed.append(source)
            except Exception:
                logging.exception("Failed translating %s", source)
                failed.append(source)
        if failed:
            logging.error("%d source file(s) failed: %s", len(failed), ", ".join(failed))
        return

    logging.info("Translating %d source files with %d workers", len(sources), jobs)
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
        futures = {executor.submit(_process_source_worker, source, args_dict): source for source in sources}
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                future.result()
            except (Exception, SystemExit):
                logging.exception("Failed translating %s", source)
                failed.append(source)
    if failed:
        logging.error("%d source file(s) failed: %s", len(failed), ", ".join(failed))


def main() -> None:
    """Main entry point allowing external calls.

    Args:
    ----
      args ([str]): command line parameter list

    """
    setup_logging("", logging.INFO)
    #if sys.version_info[0] >= 3:
    #    sys.stdout.reconfigure(encoding="utf-8")
    #    sys.stderr.reconfigure(encoding="utf-8")

    args: argparse.Namespace = parse_args(sys.argv[1:])
    logging.info(f"Masm source to C++ translator V{__version__} {__license__}")
    # Process .asm
    files = []
    for pattern in args.filenames:
        files.extend(glob.glob(pattern))

    process_source_files(files, args)

    # Process .seg files
    merge_data_segments = should_merge_data_segments(files)
    generator = Cpp(Parser(vars(args)), merge_data_segments=merge_data_segments)
    generator.convert_segment_files_into_datacpp(files)

    logging.info(" *** Finished")
    raise SystemExit(0)



"""
import auger
import re

if __name__ == "__main__":
  with auger.magic([parser, lex, op, cpp, proc]):   # this is the new line and invokes Auger
    main()
"""

if __name__ == "__main__":
    main()
