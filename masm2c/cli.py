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
import concurrent.futures
import glob
import logging
import os
import re
import sys

from .cpp import Cpp
from .parser import Parser

__version__ = "0.9.8"

__author__ = "x0r"
__copyright__ = "x0r"
__license__ = "GPL2+"

_logger = logging.getLogger(__name__)


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
    if m := re.match(r"(.+)\.(?:asm|lst)", name.lower()):
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
    process(name, args)
    return name


def should_merge_data_segments(files: list[str]) -> bool:
    """Multi-module builds need linked segment merging even when some inputs are listings."""
    asm_sources = [file for file in files if file.lower().endswith((".asm", ".lst"))]
    return not (len(asm_sources) == 1 and asm_sources[0].lower().endswith(".lst"))


def source_files(files: list[str]) -> list[str]:
    return [file for file in files if file.lower().endswith((".asm", ".lst"))]


def process_source_files(files: list[str], args: argparse.Namespace) -> None:
    sources = source_files(files)
    if not sources:
        return

    args_dict = vars(args)
    jobs = max(1, min(args.jobs, len(sources)))
    if jobs == 1:
        for source in sources:
            _process_source_worker(source, args_dict)
        return

    logging.info("Translating %d source files with %d workers", len(sources), jobs)
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
        futures = {executor.submit(_process_source_worker, source, args_dict): source for source in sources}
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                future.result()
            except Exception:
                logging.exception("Failed translating %s", source)
                raise


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
