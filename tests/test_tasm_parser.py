from __future__ import absolute_import
from __future__ import print_function

from tasm import parser
from tasm import cpp
from tasm import op
from tasm import proc
from tasm import lex

from builtins import chr
from builtins import hex
from builtins import object
from builtins import range
from builtins import str
import future.types
from future.types import Integral
import future.types.newobject
from future.types.newobject import newobject
import future.types.newrange
from future.types.newrange import newrange
import future.types.newstr
from future.types.newstr import BaseNewStr
from future.types.newstr import newstr
import logging
from logging import BufferingFormatter
from mock import patch
import ntpath
import re
from re import Scanner
import re, string, os
import sys
import tasm.lex
import tasm.op
from tasm.op import label
from tasm.op import var
import tasm.parser
from tasm.parser import Parser
import tasm.proc
from tasm.proc import Proc
import traceback
import unittest

class ParserTest(unittest.TestCase):

    @patch.object(logging, 'debug')
    @patch.object(logging, 'info')
    #@patch.object(parser, 'get_global')
    def test_convert_data(self, mock_info, mock_debug):
        #mock_get_global.return_value = var()
        mock_info.return_value = None
        mock_debug.return_value = None
        parser_instance = Parser([])

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=256,v=u'2*2')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=256,v=u'3)')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=256,v=u'5*5 dup (0')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=256,v=u'testEqu*2')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=4294967296,v=u'test2')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=65536,v=u'2*2')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=65536,v=u'3)')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=65536,v=u'5*5 dup (0')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=65536,v=u'test2')

        with self.assertRaises(KeyError):
            parser_instance.convert_data(base=65536,v=u'testEqu*2')

        #self.assertEqual(parser_instance.convert_data(base=4294967296,v=u'var5'),u'offset(_data,var5)')

    def test_convert_data_to_blob(self):
        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u"'00000000'", u'0Dh', u'0Ah', u"'$'"]),[48, 48, 48, 48, 48, 48, 48, 48, 13, 10, 36])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u"'Hello World From Protected Mode!'", u'10', u'13', u"'$'"]),[72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 32, 70, 114, 111, 109, 32, 80, 114, 111, 116, 101, 99, 116, 101, 100, 32, 77, 111, 100, 101, 33, 10, 13, 36])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u"'OKOKOKOK'", u'10', u'13']),[79, 75, 79, 75, 79, 75, 79, 75, 10, 13])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u"'OKOKOKOK'"]),[79, 75, 79, 75, 79, 75, 79, 75])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u"'ab''cd'"]),[97, 98, 39, 39, 99, 100])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u"'file.txt'", u'0']),[102, 105, 108, 101, 46, 116, 120, 116, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'1']),[1])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'10 dup (?)']),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'100 dup (1)']),[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'12']),[12])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'131']),[131])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'141']),[141])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'2', u'5', u'6']),[2, 5, 6])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'2']),[2])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'4 dup (5)']),[5, 5, 5, 5])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'4']),[4])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'5 dup (0)']),[0, 0, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'5*5 dup (0', u'testEqu*2', u'2*2', u'3)']),[0, 0, 4, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'6']),[6])

        self.assertEqual(parser_instance.convert_data_to_blob(width=2,data=[u'11']),[11, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=2,data=[u'2', u'5', u'0']),[2, 0, 5, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=2,data=[u'2']),[2, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=2,data=[u'223', u'22']),[223, 0, 22, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=2,data=[u'4', u'6', u'9']),[4, 0, 6, 0, 9, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'0']),[0, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'10 dup (?)']),[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'11', u'-11', u'2', u'4']),[11, 0, 0, 0, 245, 255, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'11', u'-11', u'2', u'4000000']),[11, 0, 0, 0, 245, 255, 0, 0, 2, 0, 0, 0, 0, 9, 61, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'111', u'1']),[111, 0, 0, 0, 1, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'3']),[3, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'34']),[34, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'9', u'8', u'7', u'1']),[9, 0, 0, 0, 8, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'offset var5']),[0, 0, 0, 0])
        self.assertEqual(parser_instance.convert_data_to_blob(width=4,data=[u'test2']),[0, 0, 0, 0])
        #self.assertEqual(parser_instance.convert_data_to_blob(width=1,data=[u'2*2 dup (0,testEqu*2,2*2,3)']),[0, 0, 0, 0])

    @patch.object(logging, 'debug')
    @patch.object(logging, 'warning')
    def test_convert_data_to_c(self, mock_warning, mock_debug):
        mock_warning.return_value = None
        mock_debug.return_value = None
        parser_instance = Parser([])

        #self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'offset var5'],label=''),(['', 'offset(_data,var5)', ', // dummy1\n'], ['dw dummy1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u"'00000000'", u'0Dh', u'0Ah', u"'$'"],label=u'ASCII'),(['{', u"'0','0','0','0','0','0','0','0','\\r','\\n','$'", '}', u', // ASCII\n'], ['char ASCII[11]', ';\n'], 2))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u"'Hello World From Protected Mode!'", u'10', u'13', u"'$'"],label=u'_msg'),(['{', u"'H','e','l','l','o',' ','W','o','r','l','d',' ','F','r','o','m',' ','P','r','o','t','e','c','t','e','d',' ','M','o','d','e','!','\\n','\\r','$'", '}', u', // _msg\n'], ['char _msg[35]', ';\n'], 2))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u"'OKOKOKOK'", u'10', u'13'],label=''),(['{', u"'O','K','O','K','O','K','O','K','\\n','\\r'", '}', ', // dummy1\n'], ['char dummy1[10]', ';\n'], 2))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u"'OKOKOKOK'"],label=''),(['{', u"'O','K','O','K','O','K','O','K'", '}', ', // dummy1\n'], ['char dummy1[8]', ';\n'], 0))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u"'ab''cd'"],label=u'doublequote'),(['{', u"'a','b','\\'','\\'','c','d'", '}', u', // doublequote\n'], ['char doublequote[6]', ';\n'], 0))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u"'file.txt'", u'0'],label=u'fileName'),(['', u'"file.txt"', u', // fileName\n'], ['char fileName[9]', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'1'],label=u'var1'),(['', '1', u', // var1\n'], [u'db var1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'10 dup (?)'],label=u'var0'),(['{', '0,', '0,', '0,', '0,', '0,', '0,', '0,', '0,', '0,', '0', '}', u', // var0\n'], ['db var0[10]', ';\n'], 10))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'100 dup (1)'],label=u'var4'),(['{', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1,', '1', '}', u', // var4\n'], ['db var4[100]', ';\n'], 100))


        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'12'],label=''),(['', '12', ', // dummy1\n'], ['db dummy1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'131'],label=u'var4'),(['', '131', u', // var4\n'], [u'db var4', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'141'],label=''),(['', '141', ', // dummy1\n'], ['db dummy1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'2', u'5', u'6'],label=u'var1'),(['{', '2,', '5,', '6', '}', u', // var1\n'], ['db var1[3]', ';\n'], 3))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'2'],label=u'var1'),(['', '2', u', // var1\n'], [u'db var1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'4 dup (5)'],label=''),(['{', '5,', '5,', '5,', '5', '}', ', // dummy1\n'], ['db dummy1[4]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'4 dup (5)'],label=u'var'),(['{', '5,', '5,', '5,', '5', '}', u', // var\n'], ['db var[4]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'4'],label=u'beginningdata'),(['', '4', u', // beginningdata\n'], [u'db beginningdata', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'4'],label=u'enddata'),(['', '4', u', // enddata\n'], [u'db enddata', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'5 dup (0)'],label=u'var2'),(['{', '0,', '0,', '0,', '0,', '0', '}', u', // var2\n'], ['db var2[5]', ';\n'], 5))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'5*5 dup (0', u'testEqu*2', u'2*2', u'3)'],label=u'var3'),(['{', '0,', '0,', '4,', '0', '}', ', // var3\n'], ['db var3[4]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'6'],label=u'var1'),(['', '6', u', // var1\n'], [u'db var1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=2,data=[u'11'],label=u'var2'),(['', '11', u', // var2\n'], [u'dw var2', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=2,data=[u'2', u'5', u'0'],label=u'var5'),(['{', '2,', '5,', '0', '}', u', // var5\n'], ['dw var5[3]', ';\n'], 3))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=2,data=[u'2'],label=u'var2'),(['', '2', u', // var2\n'], [u'dw var2', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=2,data=[u'223', u'22'],label=''),(['{', '223,', '22', '}', ', // dummy1\n'], ['dw dummy1[2]', ';\n'], 2))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=2,data=[u'4', u'6', u'9'],label=u'var2'),(['{', '4,', '6,', '9', '}', u', // var2\n'], ['dw var2[3]', ';\n'], 3))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'0'],label=u'load_handle'),(['', '0', u', // load_handle\n'], [u'dd load_handle', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'10 dup (?)'],label=u'var5'),(['{', '0,', '0,', '0,', '0,', '0,', '0,', '0,', '0,', '0,', '0', '}', u', // var5\n'], ['dd var5[10]', ';\n'], 10))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'11', u'-11', u'2', u'4'],label=u'var3'),(['{', '11,', '4294967285,', '2,', '4', '}', u', // var3\n'], ['dd var3[4]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'11', u'-11', u'2', u'4000000'],label=u'var3'),(['{', '11,', '4294967285,', '2,', '4000000', '}', u', // var3\n'], ['dd var3[4]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'111', u'1'],label=''),(['{', '111,', '1', '}', ', // dummy1\n'], ['dd dummy1[2]', ';\n'], 2))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'3'],label=u'var3'),(['', '3', u', // var3\n'], [u'dd var3', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'34'],label=u'var3'),(['', '34', u', // var3\n'], [u'dd var3', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'9', u'8', u'7', u'1'],label=u'var6'),(['{', '9,', '8,', '7,', '1', '}', u', // var6\n'], ['dd var6[4]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'offset var5'],label=''),(['', '0', ', // dummy1\n'], ['dw dummy1', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=4,data=[u'test2'],label=u'var3'),(['', '0', u', // var3\n'], [u'dd var3', ';\n'], 1))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,data=["'abcde\0\0'"],label=u'var5'),(['{', "'a','b','c','d','e','\\0','\\0'", '}', ', // var5\n'], ['char var5[7]', ';\n'], 0))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,label='_a_mod_nst_669_s',data=["'.MOD.'", '0', '0', '0', '0']),(['', '".MOD.\\0\\0\\0"', ', // _a_mod_nst_669_s\n'], ['char _a_mod_nst_669_s[9]', ';\n'], 4))

        parser_instance = Parser([])
        self.assertEqual(parser_instance.convert_data_to_c(width=1,label=u'var3',data=["'*'", '10', '11', '3 * 15 DUP(0)']),(['', '"*\\n\\x0b"', ', // var3\n'], ['char var3[4]', ';\n'], 3))

        #parser_instance = Parser([])
        #self.assertEqual(parser_instance.convert_data_to_c(width=1,data=[u'2*2 dup (0,testEqu*2,2*2,3)']),[0, 0, 0, 0])


    @patch.object(logging, 'debug')
    def test_fix_dollar(self, mock_debug):
        mock_debug.return_value = None
        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='3'),'3')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='1'),'1')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='-13'),'-13')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='13'),'13')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='4'),'4')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='var1'),'var1')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='1'),'1')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='2'),'2')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='(00+38*3)*320+1/2+33*(3-1)'),'(00+38*3)*320+1/2+33*(3-1)')

        parser_instance = Parser([])
        self.assertEqual(parser_instance.fix_dollar(v='1500 ; 8*2*3 ;+1 +19*13*2*4'),'1500 ; 8*2*3 ;+1 +19*13*2*4')

    def test_parse_int(self):
        parser_instance = Parser([])

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u"'Z' - 'A' +1")
        
        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u"'a'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u"'c'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u"'d'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u"'tseT'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'3)')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'5*5 dup (0')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'B')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'CC')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'DDD')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'OFFSET ASCiI')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'OFFSET AsCii')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[doublequote+4]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[edi+1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[edi]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[load_handle]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var+3]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var+4]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var-1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var0+5]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var1+1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var2+2]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var2-1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var2]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var3+3*4]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var3+ebp]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var3]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'[var]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'_data')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'al')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'beginningdata')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'bl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'buffer')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'bx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'byte ptr [edi+1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'byte ptr [edi+7]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'byte ptr dl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'cl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'cx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'dl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'ds')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'ds:[edi]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'dword ptr buffer')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'dx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'eax')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'ebp')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'ebx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'ecx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'edi')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'edx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'enddata')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'es')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'esi')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'fileName')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'offset _msg')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'offset var1')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'offset var2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'offset var5')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'teST2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'test2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'testEqu*2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var1')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var1[1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var1[bx+si]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var1[bx]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var3')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var3+3*4')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'var3+ebp')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'word ptr [var5+2]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'word ptr var5')


        with self.assertRaises(ValueError):
            parser_instance.parse_int(v=u'ah')

        self.assertEqual(parser_instance.parse_int(v=u'14*320'),4480)
        self.assertEqual(parser_instance.parse_int(v=u'2*2'),4)
        self.assertEqual(parser_instance.parse_int(v=u'3*4'),12)
        self.assertEqual(parser_instance.parse_int(v=u'-1-(-2+3)'),-2)
        self.assertEqual(parser_instance.parse_int(v=u'-1'),-1)
        self.assertEqual(parser_instance.parse_int(v=u'-11'),-11)
        self.assertEqual(parser_instance.parse_int(v=u'-2'),-2)
        self.assertEqual(parser_instance.parse_int(v=u'0'),0)
        self.assertEqual(parser_instance.parse_int(v=u'00h'),0)
        self.assertEqual(parser_instance.parse_int(v=u'03dh'),61)
        self.assertEqual(parser_instance.parse_int(v=u'03eh'),62)
        self.assertEqual(parser_instance.parse_int(v=u'03fh'),63)
        self.assertEqual(parser_instance.parse_int(v=u'042h'),66)
        self.assertEqual(parser_instance.parse_int(v=u'0Ah'),10)
        self.assertEqual(parser_instance.parse_int(v=u'0Dh'),13)
        self.assertEqual(parser_instance.parse_int(v=u'0Fh'),15)
        self.assertEqual(parser_instance.parse_int(v=u'0ffffff00h'),4294967040)
        self.assertEqual(parser_instance.parse_int(v=u'1'),1)
        self.assertEqual(parser_instance.parse_int(v=u'10'),10)
        self.assertEqual(parser_instance.parse_int(v=u'100'),100)
        self.assertEqual(parser_instance.parse_int(v=u'1000h'),4096)
        self.assertEqual(parser_instance.parse_int(v=u'11'),11)
        self.assertEqual(parser_instance.parse_int(v=u'111'),111)
        self.assertEqual(parser_instance.parse_int(v=u'12'),12)
        self.assertEqual(parser_instance.parse_int(v=u'13'),13)
        self.assertEqual(parser_instance.parse_int(v=u'131'),131)
        self.assertEqual(parser_instance.parse_int(v=u'16'),16)
        self.assertEqual(parser_instance.parse_int(v=u'2'),2)
        self.assertEqual(parser_instance.parse_int(v=u'21h'),33)
        self.assertEqual(parser_instance.parse_int(v=u'22'),22)
        self.assertEqual(parser_instance.parse_int(v=u'223'),223)
        self.assertEqual(parser_instance.parse_int(v=u'25'),25)
        self.assertEqual(parser_instance.parse_int(v=u'3'),3)
        self.assertEqual(parser_instance.parse_int(v=u'30h'),48)
        self.assertEqual(parser_instance.parse_int(v=u'34'),34)
        self.assertEqual(parser_instance.parse_int(v=u'35'),35)
        self.assertEqual(parser_instance.parse_int(v=u'37'),37)
        self.assertEqual(parser_instance.parse_int(v=u'39h'),57)
        self.assertEqual(parser_instance.parse_int(v=u'4'),4)
        self.assertEqual(parser_instance.parse_int(v=u'4000000'),4000000)
        self.assertEqual(parser_instance.parse_int(v=u'4ch'),76)
        self.assertEqual(parser_instance.parse_int(v=u'5'),5)
        self.assertEqual(parser_instance.parse_int(v=u'50'),50)
        self.assertEqual(parser_instance.parse_int(v=u'6'),6)
        self.assertEqual(parser_instance.parse_int(v=u'64000'),64000)
        self.assertEqual(parser_instance.parse_int(v=u'7'),7)
        self.assertEqual(parser_instance.parse_int(v=u'0h'),0)
        self.assertEqual(parser_instance.parse_int(v=u'0b'),0)


    def test_calculate_data_size(self):
        parser_instance = Parser([])
        self.assertEqual(parser_instance.calculate_data_size(cmd0='b'),1)
        self.assertEqual(parser_instance.calculate_data_size(cmd0='d'),4)
        self.assertEqual(parser_instance.calculate_data_size(cmd0='q'),8)
        self.assertEqual(parser_instance.calculate_data_size(cmd0='w'),2)
        self.assertEqual(parser_instance.calculate_data_size(cmd0='t'),10)
        
if __name__ == "__main__":
    unittest.main()
