#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from masm2c.parser import Parser
from masm2c.cpp import Cpp

import re

import argparse
import logging
import sys

#from masm2c.__init__ import __version__
__version__ = '0.9.5'

__author__ = "x0r"
__copyright__ = "x0r"
__license__ = "GPL2+"

_logger = logging.getLogger(__name__)


def tracefunc(frame, event, arg, indent=[0]):
    if event == "call":
        indent[0] += 2
        print("-" * indent[0] + "> call function", frame.f_code.co_filename, frame.f_code.co_name)
    elif event == "return":
        print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
        indent[0] -= 2
    return tracefunc


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    aparser = argparse.ArgumentParser(description=f"Masm source to C++ translator V{__version__} {__license__}", prefix_chars='-/')
    aparser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{ver}".format(ver=__version__),
    )
    aparser.add_argument('filenames', nargs='+', help='Assembler source .asm Masm 6 or .lst from IDA Pro or .seg Segment dump to merge')
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
        "/Fl",
        "--list",
        dest="list",
        #nargs="?",
        help="Generate all globals to .list file",
        action="store_const",
        const=True,
        default=False,
    )
    '''
    aparser.add_argument(
        "-s",
        "--singleproc",
        dest="singleproc",
        help="Merge all procs together",
        action="store_const",
        default=False,
        const=True,
    )
    aparser.add_argument(
        "-p",
        "--procpersegment",
        dest="procperseg",
        help="Each code segment is merged to a single procedure",
        action="store_const",
        default=False,
        const=True,
    )
    '''
    aparser.add_argument(
        "-p",
        "--passes",
        dest="passes",
        help="How many parsing passes (default: 2)",
        nargs=1,
        type=int,
        choices=[1, 2],
        default=2,
    )
    aparser.add_argument(
        "-lo",
        "--loadsegment",
        dest="loadsegment",
        help="Dosbox 0.74.3 loads .exe from 0x1a2 para (w/o debugger), 0x1ed (with debugger), .com from 0x192 (w/o debugger)",
        action="store",
        default='0x1a2',
    )
    aparser.add_argument(
        "/AT",
        dest="loadsegment",
        help="Dosbox 0.74.3 loads .com from 0x192 (w/o debugger)",
        action="store_const",
        const='0x192',
    )
    aparser.add_argument(
        '-m', '--mergeprocs', type=str, default='separate', choices=["separate", "persegment", "single"],
        help='How to merge procs (default: persegment)', )
    return aparser.parse_args(args)


def setup_logging(name, loglevel):
    """Setup basic logging

      Args:
        loglevel (int): minimum loglevel for emitting messages
    """
    root = logging.getLogger()
    root.setLevel(loglevel)

    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")
    err_handler.setFormatter(formatter)
    # root.addHandler(err_handler)

    out_handler = logging.StreamHandler(sys.stdout)
    # out_handler.setFormatter(logging.Formatter("%(message)s"))
    out_handler.setLevel(loglevel)

    if len(name):
        file_handler = logging.FileHandler(name + '.log', 'w', 'utf-8')
        file_handler.setLevel(loglevel)
        formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")
        file_handler.setFormatter(formatter)

        logging.basicConfig(
            handlers=[err_handler, out_handler, file_handler],
            level=loglevel,
            force=True
        )
    else:
        logging.basicConfig(
            handlers=[err_handler, out_handler],
            level=loglevel,
            force=True
        )


def process(i, args):
    name = i
    m = re.match(r'(.+)\.(?:asm|lst)', name.lower())
    outname = ""
    if m:
        outname = m.group(1).strip()

    p = Parser(args)

    counter = Parser.c_dummy_label

    p.parse_rt_info(outname)
    if args.passes >= 2:
        p.parse_file(name)
        p.next_pass(counter)

    context = p.parse_file(name)

    generator = Cpp(context, outfile=outname, skip_output=[])
    generator.generate('mainproc')  # start routine
    if args.list:
        generator.dump_globals()
    return generator


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    setup_logging('', logging.INFO)
    if sys.version_info[0] >= 3:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    args = parse_args(args)
    logging.info(f"Masm source to C++ translator V{__version__} {__license__}")
    # Process .asm
    merge_data_segments = True
    for i in args.filenames:
        if i.lower().endswith('.lst'):
            merge_data_segments = False
        if i.lower().endswith('.asm') or i.lower().endswith('.lst'):
            setup_logging(i, args.loglevel)
            process(i, args)

    # Process .seg files
    generator = Cpp(Parser(args), merge_data_segments=merge_data_segments)
    generator.produce_data_cpp(args.filenames)

    logging.info(f" *** Finished")


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


'''
import auger
import re

if __name__ == "__main__":
  with auger.magic([parser, lex, op, cpp, proc]):   # this is the new line and invokes Auger
    main()
'''

if __name__ == "__main__":
    run()
