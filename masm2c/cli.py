#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from masm2c.parser import Parser
from masm2c.cpp import Cpp

import re

import argparse
import logging
import sys

#from import __version__
__version__='0.9.4'

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
    aparser = argparse.ArgumentParser(description="Masm source to C source translator")
    aparser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{ver}".format(ver=__version__),
    )
    aparser.add_argument('filename', nargs='+', help='Assembler source')
    aparser.add_argument(
        "-d",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        default=logging.INFO,
        const=logging.DEBUG,
    )
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
  #root.addHandler(err_handler)

  out_handler = logging.StreamHandler(sys.stdout)
  #out_handler.setFormatter(logging.Formatter("%(message)s"))
  out_handler.setLevel(loglevel)

  if len(name):
      file_handler = logging.FileHandler(name+'.log', 'w', 'utf-8')
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
         force = True
      )

def process(i):
  name = i
  m = re.match(r'.*?([A-Za-z90-9_.-]+)\.asm', name.lower())
  outname=""
  if m is not None:
     outname = m.group(1).strip()

  p = Parser(skip_binary_data = [
      # These data blobs are not output
      # dreamweb.asm
      #	'characterset1',
   ])
  #p.strip_path = 3
  context = p.parse_file(name)
  #p.link()

  generator = Cpp(context, outfile = outname, blacklist = [], skip_output = [], skip_dispatch_call = True,
                  skip_addr_constants = True,
                  header_omit_blacklisted = True,
                  function_name_remapping = {})
  generator.generate('mainproc') #start routine
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
    logging.info(f"Masm source to C source translator V{__version__} {__license__}")
    for i in args.filename:
       setup_logging(i, args.loglevel)
       generator = process(i)
    generator.produce_data_cpp(args.filename)

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
