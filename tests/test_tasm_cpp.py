from __future__ import absolute_import
from __future__ import print_function

from masm2c import op
from masm2c import cpp
from mock import patch
from masm2c.cpp import Cpp
from masm2c.parser import Parser
import logging
import unittest

from random import randint


# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
#unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)

class CppTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.cpp = Cpp(self.parser)

    def test_cpp_20010(self):
        self.assertEqual(self.parser.parse_arg(u'[a+1]', def_size=1, destination=False), u'*(raddr(ds,a+1))')

    def test_cpp_20020(self):
        self.assertEqual(self.parser.parse_arg(u'ds:40h[eax*2]', def_size=0, destination=False), u'*(raddr(ds,0x40+eax*2))')

    def test_cpp_20030(self):
        self.assertEqual(self.parser.parse_arg(u"'Z' - 'A' +1", def_size=1, destination=False), u"'Z'-'A'+1")

    def test_cpp_20040(self):
        self.assertEqual(self.parser.parse_arg(u"'a'", def_size=1, destination=False), u"'a'")

    def test_cpp_20050(self):
        self.assertEqual(self.parser.parse_arg(u'(1024*10/16)+5', def_size=2, destination=False), u'(1024*10/16)+5')

    def test_cpp_20060(self):
        self.assertEqual(self.parser.parse_arg(u'(1024*10/16)-1', def_size=2, destination=False), u'(1024*10/16)-1')

    #def test_cpp_20070(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'(offset str_buffer+800h)'),def_size=4,destination=False),u'str_buffer+0x800')

    def test_cpp_20080(self):
        self.assertEqual(self.parser.parse_arg(u'-40h', def_size=0, destination=False), u'-0x40')

    def test_cpp_20090(self):
        self.assertEqual(self.parser.parse_arg(u'+40h', def_size=0, destination=False), u'+0x40')

    #def test_cpp_20100(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+0x4000'),def_size=0,destination=False),u'+0x4000')

    #def test_cpp_20110(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx'),def_size=0,destination=False),u'+ecx')

    #def test_cpp_20120(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx*2'),def_size=0,destination=False),u'+ecx*2')

    #def test_cpp_20130(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx*2+0x4000'),def_size=0,destination=False),u'+ecx*2+0x4000')

    #def test_cpp_20140(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx*2-0x0A'),def_size=0,destination=False),u'+ecx*2-0x0A')

    #def test_cpp_20150(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx*4'),def_size=0,destination=False),u'+ecx*4')

    #def test_cpp_20160(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx*4+0x4000'),def_size=0,destination=False),u'+ecx*4+0x4000')

    #def test_cpp_20170(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx*4-0x0A'),def_size=0,destination=False),u'+ecx*4-0x0A')

    #def test_cpp_20180(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+ecx+0x40'),def_size=0,destination=False),u'+ecx+0x40')

    #def test_cpp_20190(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+edx'),def_size=0,destination=False),u'+edx')

    #def test_cpp_20200(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'+edx+0x4000'),def_size=0,destination=False),u'+edx+0x4000')

    #def test_cpp_20210(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-0x108'),def_size=0,destination=False),u'-0x108')

    #def test_cpp_20220(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-0x1C'),def_size=0,destination=False),u'-0x1C')

    #def test_cpp_20230(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-0x20'),def_size=0,destination=False),u'-0x20')

    #def test_cpp_20240(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-0x28'),def_size=0,destination=False),u'-0x28')

    #def test_cpp_20250(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-0x2C'),def_size=0,destination=False),u'-0x2C')

    #def test_cpp_20260(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-1'),def_size=1,destination=False),u'-1')

    #def test_cpp_20270(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-1'),def_size=2,destination=False),u'-1')

    #def test_cpp_20280(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-1'),def_size=4,destination=False),u'-1')

    #def test_cpp_20290(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-1-(-2+3)'),def_size=4,destination=False),u'-1-(-2+3)')

    #def test_cpp_20300(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-12'),def_size=4,destination=False),u'-12')

    #def test_cpp_20310(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-13'),def_size=4,destination=False),u'-13')

    #def test_cpp_20320(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-2'),def_size=1,destination=False),u'-2')

    #def test_cpp_20330(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-2'),def_size=4,destination=False),u'-2')

    #def test_cpp_20340(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-2Dh'),def_size=2,destination=False),u'-0x2D')

    #def test_cpp_20350(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-2Dh'),def_size=4,destination=False),u'-0x2D')

    #def test_cpp_20360(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'-4'),def_size=0,destination=False),u'-4')

    def test_cpp_20370(self):
        self.assertEqual(self.parser.parse_arg(u'0', def_size=0, destination=False), u'0')

    def test_cpp_20380(self):
        self.assertEqual(self.parser.parse_arg(u'0', def_size=1, destination=False), u'0')

    def test_cpp_20390(self):
        self.assertEqual(self.parser.parse_arg(u'0002h', def_size=1, destination=False), u'0x0002')

    def test_cpp_20400(self):
        self.assertEqual(self.parser.parse_arg(u'0007', def_size=1, destination=False), u'0007')

    def test_cpp_20410(self):
        self.assertEqual(self.parser.parse_arg(u'000f3h', def_size=1, destination=False), u'0x000f3')

    def test_cpp_20420(self):
        self.assertEqual(self.parser.parse_arg(u'000ff00ffh', def_size=4, destination=False), u'0x000ff00ff')

    def test_cpp_20430(self):
        self.assertEqual(self.parser.parse_arg(u'001111111B', def_size=1, destination=False), u'0x7f')

    def test_cpp_20440(self):
        self.assertEqual(self.parser.parse_arg(u'00fffh', def_size=2, destination=False), u'0x00fff')

    def test_cpp_20450(self):
        self.assertEqual(self.parser.parse_arg(u'00h', def_size=1, destination=False), u'0x00')

    def test_cpp_20460(self):
        self.assertEqual(self.parser.parse_arg(u'0100b', def_size=4, destination=False), u'0x4')

    def test_cpp_20470(self):
        self.assertEqual(self.parser.parse_arg(u'01010101010101010b', def_size=2, destination=False), u'0xaaaa')

    def test_cpp_20480(self):
        self.assertEqual(self.parser.parse_arg(u'0101010101010101b', def_size=4, destination=False), u'0x5555')

    def test_cpp_20490(self):
        self.assertEqual(self.parser.parse_arg(u'0101b', def_size=4, destination=False), u'0x5')

    def test_cpp_20500(self):
        self.assertEqual(self.parser.parse_arg(u'010B', def_size=1, destination=False), u'0x2')

    def test_cpp_20510(self):
        self.assertEqual(self.parser.parse_arg(u'010B', def_size=4, destination=False), u'0x2')

    def test_cpp_20520(self):
        self.assertEqual(self.parser.parse_arg(u'011111100B', def_size=1, destination=False), u'0xfc')

    def test_cpp_20530(self):
        self.assertEqual(self.parser.parse_arg(u'011111111111111111111111111111111b', def_size=4, destination=False), u'0xffffffff')

    def test_cpp_20540(self):
        self.assertEqual(self.parser.parse_arg(u'01111111111111111b', def_size=2, destination=False), u'0xffff')

    def test_cpp_20550(self):
        self.assertEqual(self.parser.parse_arg(u'011111111B', def_size=1, destination=False), u'0xff')

    def test_cpp_20560(self):
        self.assertEqual(self.parser.parse_arg(u'012345678h', def_size=4, destination=False), u'0x012345678')

    def test_cpp_20570(self):
        self.assertEqual(self.parser.parse_arg(u'01B', def_size=4, destination=False), u'0x1')

    def test_cpp_20580(self):
        self.assertEqual(self.parser.parse_arg(u'01h', def_size=1, destination=False), u'0x01')

    def test_cpp_20590(self):
        self.assertEqual(self.parser.parse_arg(u'02h', def_size=1, destination=False), u'0x02')

    def test_cpp_20600(self):
        self.assertEqual(self.parser.parse_arg(u'03dh', def_size=1, destination=False), u'0x03d')

    def test_cpp_20610(self):
        self.assertEqual(self.parser.parse_arg(u'03eh', def_size=1, destination=False), u'0x03e')

    def test_cpp_20620(self):
        self.assertEqual(self.parser.parse_arg(u'03fh', def_size=1, destination=False), u'0x03f')

    def test_cpp_20630(self):
        self.assertEqual(self.parser.parse_arg(u'042h', def_size=1, destination=False), u'0x042')

    def test_cpp_20640(self):
        self.assertEqual(self.parser.parse_arg(u'077123456h', def_size=4, destination=False), u'0x077123456')

    def test_cpp_20650(self):
        self.assertEqual(self.parser.parse_arg(u'077aaFF00h', def_size=4, destination=False), u'0x077aaFF00')

    def test_cpp_20660(self):
        self.assertEqual(self.parser.parse_arg(u'08h', def_size=1, destination=False), u'0x08')

    def test_cpp_20670(self):
        self.assertEqual(self.parser.parse_arg(u'0B', def_size=1, destination=False), u'0x0')

    def test_cpp_20680(self):
        self.assertEqual(self.parser.parse_arg(u'0BC6058h', def_size=0, destination=False), u'0x0BC6058')

    def test_cpp_20690(self):
        self.assertEqual(self.parser.parse_arg(u'0D5h', def_size=1, destination=False), u'0x0D5')

    def test_cpp_20700(self):
        self.assertEqual(self.parser.parse_arg(u'0Eh', def_size=1, destination=False), u'0x0E')

    def test_cpp_20710(self):
        self.assertEqual(self.parser.parse_arg(u'0F7h', def_size=1, destination=False), u'0x0F7')

    def test_cpp_20720(self):
        self.assertEqual(self.parser.parse_arg(u'0FBCA7654h', def_size=4, destination=False), u'0x0FBCA7654')

    def test_cpp_20730(self):
        self.assertEqual(self.parser.parse_arg(u'0FBCA7h', def_size=4, destination=False), u'0x0FBCA7')

    def test_cpp_20740(self):
        self.assertEqual(self.parser.parse_arg(u'0FEh', def_size=1, destination=False), u'0x0FE')

    def test_cpp_20750(self):
        self.assertEqual(self.parser.parse_arg(u'0FFEh', def_size=2, destination=False), u'0x0FFE')

    def test_cpp_20760(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFC70F9h', def_size=4, destination=False), u'0x0FFFC70F9')

    def test_cpp_20770(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFE0080h', def_size=4, destination=False), u'0x0FFFE0080')

    def test_cpp_20780(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFEDCBFh', def_size=4, destination=False), u'0x0FFFEDCBF')

    def test_cpp_20790(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFEFDFCh', def_size=4, destination=False), u'0x0FFFEFDFC')

    def test_cpp_20800(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFEh', def_size=2, destination=False), u'0x0FFFE')

    def test_cpp_20810(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFF7FFFh', def_size=4, destination=False), u'0x0FFFF7FFF')

    def test_cpp_20820(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFA549h', def_size=4, destination=False), u'0x0FFFFA549')

    def test_cpp_20830(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFEh', def_size=4, destination=False), u'0x0FFFFE')

    def test_cpp_20840(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFED4h', def_size=4, destination=False), u'0x0FFFFFED4')

    def test_cpp_20850(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFEh', def_size=4, destination=False), u'0x0FFFFFE')

    def test_cpp_20860(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFD3h', def_size=4, destination=False), u'0x0FFFFFFD3')

    def test_cpp_20870(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFECh', def_size=4, destination=False), u'0x0FFFFFFEC')

    def test_cpp_20880(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFEh', def_size=4, destination=False), u'0x0FFFFFFE')

    def test_cpp_20890(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFF0h', def_size=4, destination=False), u'0x0FFFFFFF0')

    def test_cpp_20900(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFF7h', def_size=4, destination=False), u'0x0FFFFFFF7')

    def test_cpp_20910(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFAh', def_size=4, destination=False), u'0x0FFFFFFFA')

    def test_cpp_20920(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFBh', def_size=4, destination=False), u'0x0FFFFFFFB')

    def test_cpp_20930(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFCh', def_size=4, destination=False), u'0x0FFFFFFFC')

    def test_cpp_20940(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFDh', def_size=4, destination=False), u'0x0FFFFFFFD')

    def test_cpp_20950(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFEh', def_size=4, destination=False), u'0x0FFFFFFFE')

    def test_cpp_20960(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFFh', def_size=4, destination=False), u'0x0FFFFFFFF')

    def test_cpp_20970(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFFh', def_size=4, destination=False), u'0x0FFFFFFF')

    def test_cpp_20980(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFFh', def_size=4, destination=False), u'0x0FFFFFF')

    def test_cpp_20990(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFFh', def_size=4, destination=False), u'0x0FFFFF')

    def test_cpp_21000(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFFh', def_size=2, destination=False), u'0x0FFFF')

    def test_cpp_21010(self):
        self.assertEqual(self.parser.parse_arg(u'0FFFh', def_size=2, destination=False), u'0x0FFF')

    def test_cpp_21020(self):
        self.assertEqual(self.parser.parse_arg(u'0FFh', def_size=1, destination=False), u'0x0FF')

    def test_cpp_21030(self):
        self.assertEqual(self.parser.parse_arg(u'0Fh', def_size=1, destination=False), u'0x0F')

    def test_cpp_21040(self):
        self.assertEqual(self.parser.parse_arg(u'0a0000h', def_size=4, destination=False), u'0x0a0000')

    def test_cpp_21050(self):
        self.assertEqual(self.parser.parse_arg(u'0a000h', def_size=2, destination=False), u'0x0a000')

    def test_cpp_21060(self):
        self.assertEqual(self.parser.parse_arg(u'0aabbccddh', def_size=4, destination=False), u'0x0aabbccdd')

    def test_cpp_21070(self):
        self.assertEqual(self.parser.parse_arg(u'0abcdef77h', def_size=4, destination=False), u'0x0abcdef77')

    def test_cpp_21080(self):
        self.assertEqual(self.parser.parse_arg(u'0af222h', def_size=4, destination=False), u'0x0af222')

    def test_cpp_21090(self):
        self.assertEqual(self.parser.parse_arg(u'0cch', def_size=1, destination=False), u'0x0cc')

    def test_cpp_21100(self):
        self.assertEqual(self.parser.parse_arg(u'0ddh', def_size=1, destination=False), u'0x0dd')

    def test_cpp_21110(self):
        self.assertEqual(self.parser.parse_arg(u'0df01h', def_size=2, destination=False), u'0x0df01')

    def test_cpp_21120(self):
        self.assertEqual(self.parser.parse_arg(u'0dff1h', def_size=2, destination=False), u'0x0dff1')

    def test_cpp_21130(self):
        self.assertEqual(self.parser.parse_arg(u'0f0ffh', def_size=2, destination=False), u'0x0f0ff')

    def test_cpp_21140(self):
        self.assertEqual(self.parser.parse_arg(u'0f0h', def_size=1, destination=False), u'0x0f0')

    def test_cpp_21150(self):
        self.assertEqual(self.parser.parse_arg(u'0f222h', def_size=2, destination=False), u'0x0f222')

    def test_cpp_21160(self):
        self.assertEqual(self.parser.parse_arg(u'0ffff0003h', def_size=4, destination=False), u'0x0ffff0003')

    def test_cpp_21170(self):
        self.assertEqual(self.parser.parse_arg(u'0ffff00f3h', def_size=4, destination=False), u'0x0ffff00f3')

    def test_cpp_21180(self):
        self.assertEqual(self.parser.parse_arg(u'0ffff01ffh', def_size=4, destination=False), u'0x0ffff01ff')

    def test_cpp_21190(self):
        self.assertEqual(self.parser.parse_arg(u'0ffffff00h', def_size=4, destination=False), u'0x0ffffff00')

    def test_cpp_21200(self):
        self.assertEqual(self.parser.parse_arg(u'0ffffff03h', def_size=4, destination=False), u'0x0ffffff03')

    def test_cpp_21210(self):
        self.assertEqual(self.parser.parse_arg(u'0fffffff3h', def_size=4, destination=False), u'0x0fffffff3')

    def test_cpp_21220(self):
        self.assertEqual(self.parser.parse_arg(u'0ffffffffh', def_size=4, destination=False), u'0x0ffffffff')

    def test_cpp_21230(self):
        self.assertEqual(self.parser.parse_arg(u'0ffffh', def_size=2, destination=False), u'0x0ffff')

    def test_cpp_21240(self):
        self.assertEqual(self.parser.parse_arg(u'0ffh', def_size=1, destination=False), u'0x0ff')

    def test_cpp_21250(self):
        self.assertEqual(self.parser.parse_arg(u'1', def_size=0, destination=False), u'1')

    def test_cpp_21260(self):
        self.assertEqual(self.parser.parse_arg(u'1', def_size=1, destination=False), u'1')

    def test_cpp_21270(self):
        self.assertEqual(self.parser.parse_arg(u'10', def_size=1, destination=False), u'10')

    def test_cpp_21280(self):
        self.assertEqual(self.parser.parse_arg(u'10000h', def_size=4, destination=False), u'0x10000')

    def test_cpp_21290(self):
        self.assertEqual(self.parser.parse_arg(u'1000h', def_size=2, destination=False), u'0x1000')

    def test_cpp_21300(self):
        self.assertEqual(self.parser.parse_arg(u'100h', def_size=2, destination=False), u'0x100')

    def test_cpp_21310(self):
        self.assertEqual(self.parser.parse_arg(u'1024*10/16', def_size=2, destination=False), u'1024*10/16')

    def test_cpp_21320(self):
        self.assertEqual(self.parser.parse_arg(u'1024*1024', def_size=4, destination=False), u'1024*1024')

    def test_cpp_21330(self):
        self.assertEqual(self.parser.parse_arg(u'10B', def_size=4, destination=False), u'0x2')

    def test_cpp_21340(self):
        self.assertEqual(self.parser.parse_arg(u'10h', def_size=0, destination=False), u'0x10')

    def test_cpp_21350(self):
        self.assertEqual(self.parser.parse_arg(u'10h', def_size=1, destination=False), u'0x10')

    def test_cpp_21360(self):
        self.assertEqual(self.parser.parse_arg(u'11', def_size=1, destination=False), u'11')

    def test_cpp_21370(self):
        self.assertEqual(self.parser.parse_arg(u'111', def_size=1, destination=False), u'111')

    def test_cpp_21380(self):
        self.assertEqual(self.parser.parse_arg(u'114h', def_size=2, destination=False), u'0x114')

    def test_cpp_21390(self):
        self.assertEqual(self.parser.parse_arg(u'11h', def_size=1, destination=False), u'0x11')

    def test_cpp_21400(self):
        self.assertEqual(self.parser.parse_arg(u'12', def_size=1, destination=False), u'12')

    def test_cpp_21410(self):
        self.assertEqual(self.parser.parse_arg(u'12340004h', def_size=4, destination=False), u'0x12340004')

    def test_cpp_21420(self):
        self.assertEqual(self.parser.parse_arg(u'1234001Dh', def_size=4, destination=False), u'0x1234001D')

    def test_cpp_21430(self):
        self.assertEqual(self.parser.parse_arg(u'12340128h', def_size=4, destination=False), u'0x12340128')

    def test_cpp_21440(self):
        self.assertEqual(self.parser.parse_arg(u'12340205h', def_size=4, destination=False), u'0x12340205')

    def test_cpp_21450(self):
        self.assertEqual(self.parser.parse_arg(u'12340306h', def_size=4, destination=False), u'0x12340306')

    def test_cpp_21460(self):
        self.assertEqual(self.parser.parse_arg(u'12340407h', def_size=4, destination=False), u'0x12340407')

    def test_cpp_21470(self):
        self.assertEqual(self.parser.parse_arg(u'1234040Ah', def_size=4, destination=False), u'0x1234040A')

    def test_cpp_21480(self):
        self.assertEqual(self.parser.parse_arg(u'12340503h', def_size=4, destination=False), u'0x12340503')

    def test_cpp_21490(self):
        self.assertEqual(self.parser.parse_arg(u'12340506h', def_size=4, destination=False), u'0x12340506')

    def test_cpp_21500(self):
        self.assertEqual(self.parser.parse_arg(u'12340507h', def_size=4, destination=False), u'0x12340507')

    def test_cpp_21510(self):
        self.assertEqual(self.parser.parse_arg(u'12340547h', def_size=4, destination=False), u'0x12340547')

    def test_cpp_21520(self):
        self.assertEqual(self.parser.parse_arg(u'12340559h', def_size=4, destination=False), u'0x12340559')

    def test_cpp_21530(self):
        self.assertEqual(self.parser.parse_arg(u'12340560h', def_size=4, destination=False), u'0x12340560')

    def test_cpp_21540(self):
        self.assertEqual(self.parser.parse_arg(u'1234059Fh', def_size=4, destination=False), u'0x1234059F')

    def test_cpp_21550(self):
        self.assertEqual(self.parser.parse_arg(u'123405A0h', def_size=4, destination=False), u'0x123405A0')

    def test_cpp_21560(self):
        self.assertEqual(self.parser.parse_arg(u'123405FAh', def_size=4, destination=False), u'0x123405FA')

    def test_cpp_21570(self):
        self.assertEqual(self.parser.parse_arg(u'12341678h', def_size=4, destination=False), u'0x12341678')

    def test_cpp_21580(self):
        self.assertEqual(self.parser.parse_arg(u'12341h', def_size=4, destination=False), u'0x12341')

    def test_cpp_21590(self):
        self.assertEqual(self.parser.parse_arg(u'12343h', def_size=4, destination=False), u'0x12343')

    def test_cpp_21600(self):
        self.assertEqual(self.parser.parse_arg(u'12345', def_size=2, destination=False), u'12345')

    def test_cpp_21610(self):
        self.assertEqual(self.parser.parse_arg(u'1234561Dh', def_size=4, destination=False), u'0x1234561D')

    def test_cpp_21620(self):
        self.assertEqual(self.parser.parse_arg(u'12345678h', def_size=4, destination=False), u'0x12345678')

    def test_cpp_21630(self):
        self.assertEqual(self.parser.parse_arg(u'12345h', def_size=4, destination=False), u'0x12345')

    def test_cpp_21640(self):
        self.assertEqual(self.parser.parse_arg(u'12347F7Fh', def_size=4, destination=False), u'0x12347F7F')

    def test_cpp_21650(self):
        self.assertEqual(self.parser.parse_arg(u'12347FFFh', def_size=4, destination=False), u'0x12347FFF')

    def test_cpp_21660(self):
        self.assertEqual(self.parser.parse_arg(u'12348000h', def_size=4, destination=False), u'0x12348000')

    def test_cpp_21670(self):
        self.assertEqual(self.parser.parse_arg(u'12348080h', def_size=4, destination=False), u'0x12348080')

    def test_cpp_21680(self):
        self.assertEqual(self.parser.parse_arg(u'1234h', def_size=2, destination=False), u'0x1234')

    def test_cpp_21690(self):
        self.assertEqual(self.parser.parse_arg(u'127Eh', def_size=2, destination=False), u'0x127E')

    def test_cpp_21700(self):
        self.assertEqual(self.parser.parse_arg(u'12Ch', def_size=2, destination=False), u'0x12C')

    def test_cpp_21710(self):
        self.assertEqual(self.parser.parse_arg(u'13', def_size=1, destination=False), u'13')

    def test_cpp_21720(self):
        self.assertEqual(self.parser.parse_arg(u'132', def_size=1, destination=False), u'132')

    def test_cpp_21730(self):
        self.assertEqual(self.parser.parse_arg(u'133', def_size=1, destination=False), u'133')

    def test_cpp_21740(self):
        self.assertEqual(self.parser.parse_arg(u'13h', def_size=1, destination=False), u'0x13')

    def test_cpp_21750(self):
        self.assertEqual(self.parser.parse_arg(u'14', def_size=1, destination=False), u'14')

    def test_cpp_21760(self):
        self.assertEqual(self.parser.parse_arg(u'14*320', def_size=4, destination=False), u'14*320')

    def test_cpp_21770(self):
        self.assertEqual(self.parser.parse_arg(u'14h', def_size=1, destination=False), u'0x14')

    def test_cpp_21780(self):
        self.assertEqual(self.parser.parse_arg(u'15', def_size=1, destination=False), u'15')

    def test_cpp_21790(self):
        self.assertEqual(self.parser.parse_arg(u'16', def_size=1, destination=False), u'16')

    def test_cpp_21800(self):
        self.assertEqual(self.parser.parse_arg(u'17', def_size=1, destination=False), u'17')

    def test_cpp_21810(self):
        self.assertEqual(self.parser.parse_arg(u'17h', def_size=1, destination=False), u'0x17')

    def test_cpp_21820(self):
        self.assertEqual(self.parser.parse_arg(u'18', def_size=1, destination=False), u'18')

    def test_cpp_21830(self):
        self.assertEqual(self.parser.parse_arg(u'18h', def_size=1, destination=False), u'0x18')

    def test_cpp_21840(self):
        self.assertEqual(self.parser.parse_arg(u'19', def_size=1, destination=False), u'19')

    def test_cpp_21850(self):
        self.assertEqual(self.parser.parse_arg(u'192', def_size=1, destination=False), u'192')

    def test_cpp_21860(self):
        self.assertEqual(self.parser.parse_arg(u'193', def_size=1, destination=False), u'193')

    def test_cpp_21870(self):
        self.assertEqual(self.parser.parse_arg(u'1Ch', def_size=1, destination=False), u'0x1C')

    def test_cpp_21880(self):
        self.assertEqual(self.parser.parse_arg(u'1Eh', def_size=1, destination=False), u'0x1E')

    def test_cpp_21890(self):
        self.assertEqual(self.parser.parse_arg(u'1FEh', def_size=2, destination=False), u'0x1FE')

    def test_cpp_21900(self):
        self.assertEqual(self.parser.parse_arg(u'1FF7Fh', def_size=4, destination=False), u'0x1FF7F')

    def test_cpp_21910(self):
        self.assertEqual(self.parser.parse_arg(u'1FF80h', def_size=4, destination=False), u'0x1FF80')

    def test_cpp_21920(self):
        self.assertEqual(self.parser.parse_arg(u'1FF81h', def_size=4, destination=False), u'0x1FF81')

    def test_cpp_21930(self):
        self.assertEqual(self.parser.parse_arg(u'1FFEh', def_size=2, destination=False), u'0x1FFE')

    def test_cpp_21940(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFEh', def_size=4, destination=False), u'0x1FFFE')

    def test_cpp_21950(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFEh', def_size=4, destination=False), u'0x1FFFFE')

    def test_cpp_21960(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFFEh', def_size=4, destination=False), u'0x1FFFFFE')

    def test_cpp_21970(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFFFEh', def_size=4, destination=False), u'0x1FFFFFFE')

    def test_cpp_21980(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFFFFh', def_size=4, destination=False), u'0x1FFFFFFF')

    def test_cpp_21990(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFFFh', def_size=4, destination=False), u'0x1FFFFFF')

    def test_cpp_22000(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFFh', def_size=4, destination=False), u'0x1FFFFF')

    def test_cpp_22010(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFFh', def_size=4, destination=False), u'0x1FFFF')

    def test_cpp_22020(self):
        self.assertEqual(self.parser.parse_arg(u'1FFFh', def_size=2, destination=False), u'0x1FFF')

    def test_cpp_22030(self):
        self.assertEqual(self.parser.parse_arg(u'1FFh', def_size=2, destination=False), u'0x1FF')

    def test_cpp_22040(self):
        self.assertEqual(self.parser.parse_arg(u'1Fh', def_size=1, destination=False), u'0x1F')

    def test_cpp_22050(self):
        self.assertEqual(self.parser.parse_arg(u'2', def_size=0, destination=False), u'2')

    def test_cpp_22060(self):
        self.assertEqual(self.parser.parse_arg(u'2', def_size=1, destination=False), u'2')

    def test_cpp_22070(self):
        self.assertEqual(self.parser.parse_arg(u'20', def_size=1, destination=False), u'20')

    def test_cpp_22080(self):
        self.assertEqual(self.parser.parse_arg(u'20000h', def_size=4, destination=False), u'0x20000')

    def test_cpp_22090(self):
        self.assertEqual(self.parser.parse_arg(u'20h', def_size=1, destination=False), u'0x20')

    def test_cpp_22100(self):
        self.assertEqual(self.parser.parse_arg(u'21', def_size=1, destination=False), u'21')

    def test_cpp_22110(self):
        self.assertEqual(self.parser.parse_arg(u'21AD3D34h', def_size=4, destination=False), u'0x21AD3D34')

    def test_cpp_22120(self):
        self.assertEqual(self.parser.parse_arg(u'21h', def_size=0, destination=False), u'0x21')

    def test_cpp_22130(self):
        self.assertEqual(self.parser.parse_arg(u'22', def_size=1, destination=False), u'22')

    def test_cpp_22140(self):
        self.assertEqual(self.parser.parse_arg(u'23', def_size=1, destination=False), u'23')

    def test_cpp_22150(self):
        self.assertEqual(self.parser.parse_arg(u'24', def_size=1, destination=False), u'24')

    def test_cpp_22160(self):
        self.assertEqual(self.parser.parse_arg(u'24h', def_size=1, destination=False), u'0x24')

    def test_cpp_22170(self):
        self.assertEqual(self.parser.parse_arg(u'25', def_size=1, destination=False), u'25')

    def test_cpp_22180(self):
        self.assertEqual(self.parser.parse_arg(u'255', def_size=1, destination=False), u'255')

    def test_cpp_22190(self):
        self.assertEqual(self.parser.parse_arg(u'256', def_size=2, destination=False), u'256')

    def test_cpp_22200(self):
        self.assertEqual(self.parser.parse_arg(u'256*3', def_size=2, destination=False), u'256*3')

    def test_cpp_22210(self):
        self.assertEqual(self.parser.parse_arg(u'256+3', def_size=2, destination=False), u'256+3')

    def test_cpp_22220(self):
        self.assertEqual(self.parser.parse_arg(u'256+3+65536', def_size=4, destination=False), u'256+3+65536')

    def test_cpp_22230(self):
        self.assertEqual(self.parser.parse_arg(u'26', def_size=1, destination=False), u'26')

    def test_cpp_22240(self):
        self.assertEqual(self.parser.parse_arg(u'27', def_size=1, destination=False), u'27')

    def test_cpp_22250(self):
        self.assertEqual(self.parser.parse_arg(u'28', def_size=1, destination=False), u'28')

    def test_cpp_22260(self):
        self.assertEqual(self.parser.parse_arg(u'29', def_size=1, destination=False), u'29')

    def test_cpp_22270(self):
        self.assertEqual(self.parser.parse_arg(u'2Ch', def_size=1, destination=False), u'0x2C')

    def test_cpp_22280(self):
        self.assertEqual(self.parser.parse_arg(u'2Dh', def_size=1, destination=False), u'0x2D')

    def test_cpp_22290(self):
        self.assertEqual(self.parser.parse_arg(u'2Dh', def_size=2, destination=False), u'0x2D')

    def test_cpp_22300(self):
        self.assertEqual(self.parser.parse_arg(u'2Dh', def_size=4, destination=False), u'0x2D')

    def test_cpp_22310(self):
        self.assertEqual(self.parser.parse_arg(u'3', def_size=0, destination=False), u'3')

    def test_cpp_22320(self):
        self.assertEqual(self.parser.parse_arg(u'3', def_size=1, destination=False), u'3')

    def test_cpp_22330(self):
        self.assertEqual(self.parser.parse_arg(u'3*4', def_size=4, destination=False), u'3*4')

    def test_cpp_22340(self):
        self.assertEqual(self.parser.parse_arg(u'30', def_size=1, destination=False), u'30')

    def test_cpp_22350(self):
        self.assertEqual(self.parser.parse_arg(u'303Bh', def_size=2, destination=False), u'0x303B')

    def test_cpp_22360(self):
        self.assertEqual(self.parser.parse_arg(u'30h', def_size=1, destination=False), u'0x30')

    def test_cpp_22370(self):
        self.assertEqual(self.parser.parse_arg(u'31', def_size=1, destination=False), u'31')

    def test_cpp_22380(self):
        self.assertEqual(self.parser.parse_arg(u'31h', def_size=0, destination=False), u'0x31')

    def test_cpp_22390(self):
        self.assertEqual(self.parser.parse_arg(u'32', def_size=1, destination=False), u'32')

    def test_cpp_22400(self):
        self.assertEqual(self.parser.parse_arg(u'320*200/4', def_size=4, destination=False), u'320*200/4')

    def test_cpp_22410(self):
        self.assertEqual(self.parser.parse_arg(u'32432434h', def_size=4, destination=False), u'0x32432434')

    def test_cpp_22420(self):
        self.assertEqual(self.parser.parse_arg(u'340128h', def_size=4, destination=False), u'0x340128')

    def test_cpp_22430(self):
        self.assertEqual(self.parser.parse_arg(u'35', def_size=1, destination=False), u'35')

    def test_cpp_22440(self):
        self.assertEqual(self.parser.parse_arg(u'37', def_size=1, destination=False), u'37')

    def test_cpp_22450(self):
        self.assertEqual(self.parser.parse_arg(u'39h', def_size=1, destination=False), u'0x39')

    def test_cpp_22460(self):
        self.assertEqual(self.parser.parse_arg(u'3Ch', def_size=1, destination=False), u'0x3C')

    def test_cpp_22470(self):
        self.assertEqual(self.parser.parse_arg(u'3DAh', def_size=2, destination=False), u'0x3DA')

    def test_cpp_22480(self):
        self.assertEqual(self.parser.parse_arg(u'3Eh', def_size=1, destination=False), u'0x3E')

    def test_cpp_22490(self):
        self.assertEqual(self.parser.parse_arg(u'3FEh', def_size=2, destination=False), u'0x3FE')

    def test_cpp_22500(self):
        self.assertEqual(self.parser.parse_arg(u'3FFEh', def_size=2, destination=False), u'0x3FFE')

    def test_cpp_22510(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFEh', def_size=4, destination=False), u'0x3FFFE')

    def test_cpp_22520(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFEh', def_size=4, destination=False), u'0x3FFFFE')

    def test_cpp_22530(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFFEh', def_size=4, destination=False), u'0x3FFFFFE')

    def test_cpp_22540(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFFFEh', def_size=4, destination=False), u'0x3FFFFFFE')

    def test_cpp_22550(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFFFFh', def_size=4, destination=False), u'0x3FFFFFFF')

    def test_cpp_22560(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFFFh', def_size=4, destination=False), u'0x3FFFFFF')

    def test_cpp_22570(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFFh', def_size=4, destination=False), u'0x3FFFFF')

    def test_cpp_22580(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFFh', def_size=4, destination=False), u'0x3FFFF')

    def test_cpp_22590(self):
        self.assertEqual(self.parser.parse_arg(u'3FFFh', def_size=2, destination=False), u'0x3FFF')

    def test_cpp_22600(self):
        self.assertEqual(self.parser.parse_arg(u'3FFh', def_size=2, destination=False), u'0x3FF')

    def test_cpp_22610(self):
        self.assertEqual(self.parser.parse_arg(u'3Fh', def_size=1, destination=False), u'0x3F')

    def test_cpp_22620(self):
        self.assertEqual(self.parser.parse_arg(u'3c8h', def_size=2, destination=False), u'0x3c8')

    def test_cpp_22630(self):
        self.assertEqual(self.parser.parse_arg(u'3c9h', def_size=2, destination=False), u'0x3c9')

    def test_cpp_22640(self):
        self.assertEqual(self.parser.parse_arg(u'3h', def_size=1, destination=False), u'0x3')

    def test_cpp_22650(self):
        self.assertEqual(self.parser.parse_arg(u'4', def_size=1, destination=False), u'4')

    def test_cpp_22660(self):
        self.assertEqual(self.parser.parse_arg(u'4+5*256', def_size=2, destination=False), u'4+5*256')

    def test_cpp_22670(self):
        self.assertEqual(self.parser.parse_arg(u'4000000', def_size=4, destination=False), u'4000000')

    def test_cpp_22680(self):
        self.assertEqual(self.parser.parse_arg(u'40h', def_size=1, destination=False), u'0x40')

    def test_cpp_22690(self):
        self.assertEqual(self.parser.parse_arg(u'43210123h', def_size=4, destination=False), u'0x43210123')

    def test_cpp_22700(self):
        self.assertEqual(self.parser.parse_arg(u'48h', def_size=1, destination=False), u'0x48')

    def test_cpp_22710(self):
        self.assertEqual(self.parser.parse_arg(u'49h', def_size=1, destination=False), u'0x49')

    def test_cpp_22720(self):
        self.assertEqual(self.parser.parse_arg(u'4Ah', def_size=1, destination=False), u'0x4A')

    def test_cpp_22730(self):
        self.assertEqual(self.parser.parse_arg(u'4Ch', def_size=1, destination=False), u'0x4C')

    def test_cpp_22740(self):
        self.assertEqual(self.parser.parse_arg(u'4ch', def_size=1, destination=False), u'0x4c')

    def test_cpp_22750(self):
        self.assertEqual(self.parser.parse_arg(u'5', def_size=1, destination=False), u'5')

    def test_cpp_22760(self):
        self.assertEqual(self.parser.parse_arg(u'50', def_size=1, destination=False), u'50')

    def test_cpp_22770(self):
        self.assertEqual(self.parser.parse_arg(u'501h', def_size=2, destination=False), u'0x501')

    def test_cpp_22780(self):
        self.assertEqual(self.parser.parse_arg(u'511', def_size=2, destination=False), u'511')

    def test_cpp_22790(self):
        self.assertEqual(self.parser.parse_arg(u'55', def_size=1, destination=False), u'55')

    def test_cpp_22800(self):
        self.assertEqual(self.parser.parse_arg(u'56', def_size=1, destination=False), u'56')

    def test_cpp_22810(self):
        self.assertEqual(self.parser.parse_arg(u'57', def_size=1, destination=False), u'57')

    def test_cpp_22820(self):
        self.assertEqual(self.parser.parse_arg(u'6', def_size=1, destination=False), u'6')

    def test_cpp_22830(self):
        self.assertEqual(self.parser.parse_arg(u'6*256+5', def_size=2, destination=False), u'6*256+5')

    def test_cpp_22840(self):
        self.assertEqual(self.parser.parse_arg(u'60', def_size=1, destination=False), u'60')

    def test_cpp_22850(self):
        self.assertEqual(self.parser.parse_arg(u'65324h', def_size=4, destination=False), u'0x65324')

    def test_cpp_22860(self):
        self.assertEqual(self.parser.parse_arg(u'65423456h', def_size=4, destination=False), u'0x65423456')

    def test_cpp_22870(self):
        self.assertEqual(self.parser.parse_arg(u'6789ABCDh', def_size=4, destination=False), u'0x6789ABCD')

    def test_cpp_22880(self):
        self.assertEqual(self.parser.parse_arg(u'7', def_size=1, destination=False), u'7')

    def test_cpp_22890(self):
        self.assertEqual(self.parser.parse_arg(u'7Eh', def_size=1, destination=False), u'0x7E')

    def test_cpp_22900(self):
        self.assertEqual(self.parser.parse_arg(u'7FEh', def_size=2, destination=False), u'0x7FE')

    def test_cpp_22910(self):
        self.assertEqual(self.parser.parse_arg(u'7FFEh', def_size=2, destination=False), u'0x7FFE')

    def test_cpp_22920(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFEh', def_size=4, destination=False), u'0x7FFFE')

    def test_cpp_22930(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFEh', def_size=4, destination=False), u'0x7FFFFE')

    def test_cpp_22940(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFFEh', def_size=4, destination=False), u'0x7FFFFFE')

    def test_cpp_22950(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFFFEh', def_size=4, destination=False), u'0x7FFFFFFE')

    def test_cpp_22960(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFFFFh', def_size=4, destination=False), u'0x7FFFFFFF')

    def test_cpp_22970(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFFFh', def_size=4, destination=False), u'0x7FFFFFF')

    def test_cpp_22980(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFFh', def_size=4, destination=False), u'0x7FFFFF')

    def test_cpp_22990(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFFh', def_size=4, destination=False), u'0x7FFFF')

    def test_cpp_23000(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFh', def_size=2, destination=False), u'0x7FFF')

    def test_cpp_23010(self):
        self.assertEqual(self.parser.parse_arg(u'7FFFh', def_size=4, destination=False), u'0x7FFF')

    def test_cpp_23020(self):
        self.assertEqual(self.parser.parse_arg(u'7FFh', def_size=2, destination=False), u'0x7FF')

    def test_cpp_23030(self):
        self.assertEqual(self.parser.parse_arg(u'7Fh', def_size=1, destination=False), u'0x7F')

    def test_cpp_23040(self):
        self.assertEqual(self.parser.parse_arg(u'8', def_size=0, destination=False), u'8')

    def test_cpp_23050(self):
        self.assertEqual(self.parser.parse_arg(u'8', def_size=1, destination=False), u'8')

    def test_cpp_23060(self):
        self.assertEqual(self.parser.parse_arg(u'80000000h', def_size=4, destination=False), u'0x80000000')

    def test_cpp_23070(self):
        self.assertEqual(self.parser.parse_arg(u'80000001h', def_size=4, destination=False), u'0x80000001')

    def test_cpp_23080(self):
        self.assertEqual(self.parser.parse_arg(u'80008481h', def_size=4, destination=False), u'0x80008481')

    def test_cpp_23090(self):
        self.assertEqual(self.parser.parse_arg(u'80008688h', def_size=4, destination=False), u'0x80008688')

    def test_cpp_23100(self):
        self.assertEqual(self.parser.parse_arg(u'8000h', def_size=2, destination=False), u'0x8000')

    def test_cpp_23110(self):
        self.assertEqual(self.parser.parse_arg(u'8000h', def_size=4, destination=False), u'0x8000')

    def test_cpp_23120(self):
        self.assertEqual(self.parser.parse_arg(u'801h', def_size=2, destination=False), u'0x801')

    def test_cpp_23130(self):
        self.assertEqual(self.parser.parse_arg(u'80h', def_size=1, destination=False), u'0x80')

    def test_cpp_23140(self):
        self.assertEqual(self.parser.parse_arg(u'81234567h', def_size=4, destination=False), u'0x81234567')

    def test_cpp_23150(self):
        self.assertEqual(self.parser.parse_arg(u'81238567h', def_size=4, destination=False), u'0x81238567')

    def test_cpp_23160(self):
        self.assertEqual(self.parser.parse_arg(u'812FADAh', def_size=4, destination=False), u'0x812FADA')

    def test_cpp_23170(self):
        self.assertEqual(self.parser.parse_arg(u'813F3421h', def_size=4, destination=False), u'0x813F3421')

    def test_cpp_23180(self):
        self.assertEqual(self.parser.parse_arg(u'81h', def_size=1, destination=False), u'0x81')

    def test_cpp_23190(self):
        self.assertEqual(self.parser.parse_arg(u'82345679h', def_size=4, destination=False), u'0x82345679')

    def test_cpp_23200(self):
        self.assertEqual(self.parser.parse_arg(u'8234A6F8h', def_size=4, destination=False), u'0x8234A6F8')

    def test_cpp_23210(self):
        self.assertEqual(self.parser.parse_arg(u'8345A1F2h', def_size=4, destination=False), u'0x8345A1F2')

    def test_cpp_23220(self):
        self.assertEqual(self.parser.parse_arg(u'8C5h', def_size=2, destination=False), u'0x8C5')

    def test_cpp_23230(self):
        self.assertEqual(self.parser.parse_arg(u'8D5h', def_size=2, destination=False), u'0x8D5')

    def test_cpp_23240(self):
        self.assertEqual(self.parser.parse_arg(u'9', def_size=1, destination=False), u'9')

    def test_cpp_23250(self):
        self.assertEqual(self.parser.parse_arg(u'9ABCDEFh', def_size=0, destination=False), u'0x9ABCDEF')

    def test_cpp_23260(self):
        self.assertEqual(self.parser.parse_arg(u'AL', def_size=1, destination=True), u'al')

    def test_cpp_23270(self):
        self.assertEqual(self.parser.parse_arg(u'B', def_size=4, destination=False), u'B')

    def test_cpp_23280(self):
        self.assertEqual(self.parser.parse_arg(u'CC', def_size=4, destination=False), u'CC')

    def test_cpp_23290(self):
        self.assertEqual(self.parser.parse_arg(u'DDD', def_size=0, destination=False), u'DDD')

    def test_cpp_23300(self):
        self.assertEqual(self.parser.parse_arg(u'DX', def_size=2, destination=True), u'dx')

    #def test_cpp_23310(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'OFFSET ASCiI'),def_size=4,destination=False),u'offset(_data,ASCII)')

    #def test_cpp_23320(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'OFFSET AsCii'),def_size=4,destination=False),u'offset(_data,ASCII)')

    def test_cpp_23330(self):
        self.assertEqual(self.parser.parse_arg(u'TWO', def_size=4, destination=False), u'TWO')

    def test_cpp_23340(self):
        self.assertEqual(self.parser.parse_arg(u'ah', def_size=1, destination=False), u'ah')

    def test_cpp_23350(self):
        self.assertEqual(self.parser.parse_arg(u'ah', def_size=1, destination=True), u'ah')

    def test_cpp_23360(self):
        self.assertEqual(self.parser.parse_arg(u'al', def_size=0, destination=False), u'al')

    def test_cpp_23370(self):
        self.assertEqual(self.parser.parse_arg(u'al', def_size=1, destination=False), u'al')

    def test_cpp_23380(self):
        self.assertEqual(self.parser.parse_arg(u'al', def_size=1, destination=True), u'al')

    def test_cpp_23390(self):
        self.assertEqual(self.parser.parse_arg(u'ax', def_size=0, destination=False), u'ax')

    def test_cpp_23400(self):
        self.assertEqual(self.parser.parse_arg(u'ax', def_size=2, destination=False), u'ax')

    def test_cpp_23410(self):
        self.assertEqual(self.parser.parse_arg(u'ax', def_size=2, destination=True), u'ax')

    #def test_cpp_23420(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'b'),def_size=0,destination=False),u'offset(_data,b)')

    #def test_cpp_23430(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'b'),def_size=2,destination=True),u'b')

    #def test_cpp_23440(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'beginningdata'),def_size=0,destination=False),u'offset(_data,beginningdata)')

    def test_cpp_23450(self):
        self.assertEqual(self.parser.parse_arg(u'bh', def_size=0, destination=False), u'bh')

    def test_cpp_23460(self):
        self.assertEqual(self.parser.parse_arg(u'bh', def_size=1, destination=False), u'bh')

    def test_cpp_23470(self):
        self.assertEqual(self.parser.parse_arg(u'bh', def_size=1, destination=True), u'bh')

    def test_cpp_23480(self):
        self.assertEqual(self.parser.parse_arg(u'bl', def_size=0, destination=False), u'bl')

    def test_cpp_23490(self):
        self.assertEqual(self.parser.parse_arg(u'bl', def_size=1, destination=False), u'bl')

    def test_cpp_23500(self):
        self.assertEqual(self.parser.parse_arg(u'bl', def_size=1, destination=True), u'bl')

    def test_cpp_23510(self):
        self.assertEqual(self.parser.parse_arg(u'bp', def_size=2, destination=False), u'bp')

    #def test_cpp_23520(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'buffer'),def_size=0,destination=False),u'offset(_data,buffer)')

    def test_cpp_23530(self):
        self.assertEqual(self.parser.parse_arg(u'bx', def_size=0, destination=False), u'bx')

    def test_cpp_23540(self):
        self.assertEqual(self.parser.parse_arg(u'bx', def_size=2, destination=False), u'bx')

    def test_cpp_23550(self):
        self.assertEqual(self.parser.parse_arg(u'bx', def_size=2, destination=True), u'bx')

    #def test_cpp_23560(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'c'),def_size=4,destination=True),u'c')

    def test_cpp_23570(self):
        self.assertEqual(self.parser.parse_arg(u'ch', def_size=1, destination=True), u'ch')

    def test_cpp_23580(self):
        self.assertEqual(self.parser.parse_arg(u'cl', def_size=0, destination=False), u'cl')

    def test_cpp_23590(self):
        self.assertEqual(self.parser.parse_arg(u'cl', def_size=1, destination=False), u'cl')

    def test_cpp_23600(self):
        self.assertEqual(self.parser.parse_arg(u'cl', def_size=1, destination=True), u'cl')

    def test_cpp_23610(self):
        self.assertEqual(self.parser.parse_arg(u'cx', def_size=0, destination=False), u'cx')

    def test_cpp_23620(self):
        self.assertEqual(self.parser.parse_arg(u'cx', def_size=2, destination=False), u'cx')

    def test_cpp_23630(self):
        self.assertEqual(self.parser.parse_arg(u'cx', def_size=2, destination=True), u'cx')

    def test_cpp_23640(self):
        self.assertEqual(self.parser.parse_arg(u'di', def_size=2, destination=False), u'di')

    def test_cpp_23650(self):
        self.assertEqual(self.parser.parse_arg(u'dl', def_size=0, destination=False), u'dl')

    def test_cpp_23660(self):
        self.assertEqual(self.parser.parse_arg(u'dl', def_size=1, destination=False), u'dl')

    def test_cpp_23670(self):
        self.assertEqual(self.parser.parse_arg(u'dl', def_size=1, destination=True), u'dl')

    def test_cpp_23680(self):
        self.assertEqual(self.parser.parse_arg(u'ds', def_size=0, destination=False), u'ds')

    def test_cpp_23690(self):
        self.assertEqual(self.parser.parse_arg(u'ds', def_size=2, destination=True), u'ds')

    def test_cpp_23700(self):
        self.assertEqual(self.parser.parse_arg(u'dx', def_size=0, destination=False), u'dx')

    def test_cpp_23710(self):
        self.assertEqual(self.parser.parse_arg(u'dx', def_size=2, destination=False), u'dx')

    def test_cpp_23720(self):
        self.assertEqual(self.parser.parse_arg(u'dx', def_size=2, destination=True), u'dx')

    def test_cpp_23730(self):
        self.assertEqual(self.parser.parse_arg(u'eax', def_size=0, destination=False), u'eax')

    def test_cpp_23740(self):
        self.assertEqual(self.parser.parse_arg(u'eax', def_size=4, destination=False), u'eax')

    def test_cpp_23750(self):
        self.assertEqual(self.parser.parse_arg(u'eax', def_size=4, destination=True), u'eax')

    def test_cpp_23760(self):
        self.assertEqual(self.parser.parse_arg(u'eax_0', def_size=0, destination=False), u'eax_0')

    def test_cpp_23770(self):
        self.assertEqual(self.parser.parse_arg(u'ebp', def_size=0, destination=False), u'ebp')

    def test_cpp_23780(self):
        self.assertEqual(self.parser.parse_arg(u'ebp', def_size=4, destination=False), u'ebp')

    def test_cpp_23790(self):
        self.assertEqual(self.parser.parse_arg(u'ebp', def_size=4, destination=True), u'ebp')

    def test_cpp_23800(self):
        self.assertEqual(self.parser.parse_arg(u'ebx', def_size=0, destination=False), u'ebx')

    def test_cpp_23810(self):
        self.assertEqual(self.parser.parse_arg(u'ebx', def_size=4, destination=False), u'ebx')

    def test_cpp_23820(self):
        self.assertEqual(self.parser.parse_arg(u'ebx', def_size=4, destination=True), u'ebx')

    def test_cpp_23830(self):
        self.assertEqual(self.parser.parse_arg(u'ecx', def_size=0, destination=False), u'ecx')

    def test_cpp_23840(self):
        self.assertEqual(self.parser.parse_arg(u'ecx', def_size=4, destination=False), u'ecx')

    def test_cpp_23850(self):
        self.assertEqual(self.parser.parse_arg(u'ecx', def_size=4, destination=True), u'ecx')

    def test_cpp_23860(self):
        self.assertEqual(self.parser.parse_arg(u'ecx_0', def_size=0, destination=False), u'ecx_0')

    def test_cpp_23870(self):
        self.assertEqual(self.parser.parse_arg(u'ecx_0_0', def_size=0, destination=False), u'ecx_0_0')

    def test_cpp_23880(self):
        self.assertEqual(self.parser.parse_arg(u'edi', def_size=0, destination=False), u'edi')

    def test_cpp_23890(self):
        self.assertEqual(self.parser.parse_arg(u'edi', def_size=4, destination=False), u'edi')

    def test_cpp_23900(self):
        self.assertEqual(self.parser.parse_arg(u'edi', def_size=4, destination=True), u'edi')

    def test_cpp_23910(self):
        self.assertEqual(self.parser.parse_arg(u'edi_0', def_size=0, destination=False), u'edi_0')

    def test_cpp_23920(self):
        self.assertEqual(self.parser.parse_arg(u'edi_0', def_size=0, destination=True), u'edi_0')

    def test_cpp_23930(self):
        self.assertEqual(self.parser.parse_arg(u'edx', def_size=0, destination=False), u'edx')

    def test_cpp_23940(self):
        self.assertEqual(self.parser.parse_arg(u'edx', def_size=4, destination=False), u'edx')

    def test_cpp_23950(self):
        self.assertEqual(self.parser.parse_arg(u'edx', def_size=4, destination=True), u'edx')

    def test_cpp_23960(self):
        self.assertEqual(self.parser.parse_arg(u'edx_0_0', def_size=0, destination=False), u'edx_0_0')

    def test_cpp_23970(self):
        self.assertEqual(self.parser.parse_arg(u'edx_0_0', def_size=4, destination=True), u'edx_0_0')

    def test_cpp_23980(self):
        self.assertEqual(self.parser.parse_arg(u'eflags', def_size=1, destination=True), u'eflags')

    def test_cpp_23990(self):
        self.assertEqual(self.parser.parse_arg(u'eflags', def_size=2, destination=True), u'eflags')

    #def test_cpp_24000(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'enddata'),def_size=0,destination=False),u'offset(_data,enddata)')

    def test_cpp_24010(self):
        self.assertEqual(self.parser.parse_arg(u'es', def_size=0, destination=False), u'es')

    def test_cpp_24020(self):
        self.assertEqual(self.parser.parse_arg(u'es', def_size=2, destination=True), u'es')

    def test_cpp_24030(self):
        self.assertEqual(self.parser.parse_arg(u'esi', def_size=0, destination=False), u'esi')

    def test_cpp_24040(self):
        self.assertEqual(self.parser.parse_arg(u'esi', def_size=4, destination=False), u'esi')

    def test_cpp_24050(self):
        self.assertEqual(self.parser.parse_arg(u'esi', def_size=4, destination=True), u'esi')

    def test_cpp_24060(self):
        self.assertEqual(self.parser.parse_arg(u'esi_0', def_size=0, destination=False), u'esi_0')

    def test_cpp_24070(self):
        self.assertEqual(self.parser.parse_arg(u'esi_0', def_size=4, destination=False), u'esi_0')

    def test_cpp_24080(self):
        self.assertEqual(self.parser.parse_arg(u'esi_0', def_size=4, destination=True), u'esi_0')

    def test_cpp_24090(self):
        self.assertEqual(self.parser.parse_arg(u'esp', def_size=4, destination=False), u'esp')

    def test_cpp_24100(self):
        self.assertEqual(self.parser.parse_arg(u'esp', def_size=4, destination=True), u'esp')

    #def test_cpp_24110(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'f'),def_size=0,destination=False),u'offset(_data,f)')

    #def test_cpp_24120(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'fileName'),def_size=0,destination=False),u'offset(_data,fileName)')

    def test_cpp_24130(self):
        self.assertEqual(self.parser.parse_arg(u'flags', def_size=0, destination=False), u'flags')

    def test_cpp_24140(self):
        self.assertEqual(self.parser.parse_arg(u'flags', def_size=1, destination=True), u'flags')

    def test_cpp_24150(self):
        self.assertEqual(self.parser.parse_arg(u'flags', def_size=2, destination=True), u'flags')

    def test_cpp_24160(self):
        self.assertEqual(self.parser.parse_arg(u'flags', def_size=4, destination=False), u'flags')

    def test_cpp_24170(self):
        self.assertEqual(self.parser.parse_arg(u'fs', def_size=0, destination=False), u'fs')

    def test_cpp_24180(self):
        self.assertEqual(self.parser.parse_arg(u'fs', def_size=2, destination=False), u'fs')

    def test_cpp_24190(self):
        self.assertEqual(self.parser.parse_arg(u'fs', def_size=2, destination=True), u'fs')

    #def test_cpp_24200(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'g'),def_size=4,destination=False),u'g')

    def test_cpp_24210(self):
        self.assertEqual(self.parser.parse_arg(u'i', def_size=0, destination=False), u'i')

    def test_cpp_24220(self):
        self.assertEqual(self.parser.parse_arg(u'i', def_size=0, destination=True), u'i')

    def test_cpp_24230(self):
        self.assertEqual(self.parser.parse_arg(u'i', def_size=1, destination=True), u'i')

    def test_cpp_24240(self):
        self.assertEqual(self.parser.parse_arg(u'i', def_size=2, destination=True), u'i')

    def test_cpp_24250(self):
        self.assertEqual(self.parser.parse_arg(u'i', def_size=4, destination=False), u'i')

    def test_cpp_24260(self):
        self.assertEqual(self.parser.parse_arg(u'i', def_size=4, destination=True), u'i')

    def test_cpp_24270(self):
        self.assertEqual(self.parser.parse_arg(u"'tseT'", def_size=4, destination=False), u'0x74736554')

    '''
    #def test_cpp_24280(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[a+1]'),def_size=1,destination=False),u'*(raddr(ds,offset(_data,a)+1))')

    #def test_cpp_24290(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[a]'),def_size=1,destination=False),u'*(raddr(ds,offset(_data,a)))')

    #def test_cpp_24300(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[a]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,a)))')

    #def test_cpp_24310(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[cs:table+ax]'),def_size=0,destination=True),u'*(dw*)(raddr(cs,offset(_text,table)+ax))')

    #def test_cpp_24320(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[doublequote+4]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,doublequote)+4))')

    #def test_cpp_24330(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+4000h]'),def_size=0,destination=False),u'eax+0x4000')

    #def test_cpp_24340(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+40h]'),def_size=0,destination=False),u'eax+0x40')

    #def test_cpp_24350(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+ecx+40h]'),def_size=0,destination=False),u'eax+ecx+0x40')

    def test_cpp_24360(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+ecx]'),def_size=0,destination=False),u'eax+ecx')

    def test_cpp_24370(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax]'),def_size=0,destination=False),u'eax')

    def test_cpp_24380(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+ecx_0]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,ebp+ecx_0))')

    def test_cpp_24390(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+ecx_0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+ecx_0))')

    def test_cpp_24400(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+ecx_vals]'),def_size=0,destination=False),u'ebp+ecx_vals')

    def test_cpp_24410(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+edx_0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+edx_0))')

    def test_cpp_24420(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+edx_0]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+edx_0))')

    def test_cpp_24430(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+i*4+ecx_vals]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+i*4+ecx_vals))')

    def test_cpp_24440(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+i+table]'),def_size=1,destination=True),u'*(raddr(ds,ebp+i+table))')

    def test_cpp_24450(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+iflags]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+iflags))')

    def test_cpp_24460(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+op0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+op0))')

    def test_cpp_24470(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+op0h]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+op0h))')

    def test_cpp_24480(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+s0))')

    def test_cpp_24490(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s0]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+s0))')

    def test_cpp_24500(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s1]'),def_size=1,destination=True),u'*(raddr(ds,ebp+s1))')

    def test_cpp_24510(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s1]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+s1))')

    def test_cpp_24520(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s2]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+s2))')

    def test_cpp_24530(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s2]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+s2))')

    def test_cpp_24540(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+table]'),def_size=0,destination=False),u'ebp+table')

    def test_cpp_24550(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_1C]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_1C))')

    def test_cpp_24560(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_1C]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_1C))')

    def test_cpp_24570(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_20]'),def_size=0,destination=False),u'*(dw*)(raddr(ds,ebp+var_20))')

    def test_cpp_24580(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_20]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_cpp_24590(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_20]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_cpp_24600(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_4]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_4))')

    def test_cpp_24610(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+4000h]'),def_size=0,destination=False),u'ebx+0x4000')

    def test_cpp_24620(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+40h]'),def_size=0,destination=False),u'ebx+0x40')

    def test_cpp_24630(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+edx+4000h]'),def_size=0,destination=False),u'ebx+edx+0x4000')

    def test_cpp_24640(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+edx]'),def_size=0,destination=False),u'ebx+edx')

    def test_cpp_24650(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx]'),def_size=0,destination=False),u'ebx')

    def test_cpp_24660(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+4000h]'),def_size=0,destination=False),u'ecx+0x4000')

    def test_cpp_24670(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+40h]'),def_size=0,destination=False),u'ecx+0x40')

    def test_cpp_24680(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx*2+4000h]'),def_size=0,destination=False),u'ecx+ecx*2+0x4000')

    def test_cpp_24690(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx*2-0Ah]'),def_size=0,destination=False),u'ecx+ecx*2-0x0A')

    def test_cpp_24700(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx*2]'),def_size=0,destination=False),u'ecx+ecx*2')

    def test_cpp_24710(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx]'),def_size=0,destination=False),u'ecx+ecx')

    def test_cpp_24720(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx]'),def_size=0,destination=False),u'ecx')

    def test_cpp_24730(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+1]'),def_size=1,destination=False),u'*(raddr(ds,edi+1))')

    def test_cpp_24740(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+1]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,edi+1))')

    def test_cpp_24750(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+4000h]'),def_size=0,destination=False),u'edi+0x4000')

    def test_cpp_24760(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+40h]'),def_size=0,destination=False),u'edi+0x40')

    def test_cpp_24770(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+ecx]'),def_size=0,destination=False),u'edi+ecx')

    def test_cpp_24780(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi]'),def_size=0,destination=False),u'edi')

    def test_cpp_24790(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi]'),def_size=1,destination=False),u'*(raddr(ds,edi))')

    def test_cpp_24800(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+4000h]'),def_size=0,destination=False),u'edx+0x4000')

    def test_cpp_24810(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+40h]'),def_size=0,destination=False),u'edx+0x40')

    def test_cpp_24820(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx*4+4000h]'),def_size=0,destination=False),u'edx+ecx*4+0x4000')

    def test_cpp_24830(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx*4-0Ah]'),def_size=0,destination=False),u'edx+ecx*4-0x0A')

    def test_cpp_24840(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx*4]'),def_size=0,destination=False),u'edx+ecx*4')

    def test_cpp_24850(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx]'),def_size=0,destination=False),u'edx+ecx')

    def test_cpp_24860(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx]'),def_size=0,destination=False),u'edx')

    def test_cpp_24870(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+4000h]'),def_size=0,destination=False),u'esi+0x4000')

    def test_cpp_24880(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+40h]'),def_size=0,destination=False),u'esi+0x40')

    def test_cpp_24890(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx*8+4000h]'),def_size=0,destination=False),u'esi+ecx*8+0x4000')

    def test_cpp_24900(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx*8-0Ah]'),def_size=0,destination=False),u'esi+ecx*8-0x0A')

    def test_cpp_24910(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx*8]'),def_size=0,destination=False),u'esi+ecx*8')

    def test_cpp_24920(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx]'),def_size=0,destination=False),u'esi+ecx')

    def test_cpp_24930(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi]'),def_size=0,destination=False),u'esi')

    def test_cpp_24940(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+0Ch]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x0C))')

    def test_cpp_24950(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+0Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x0C))')

    def test_cpp_24960(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+10h]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x10))')

    def test_cpp_24970(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+10h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x10))')

    def test_cpp_24980(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+14h]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x14))')

    def test_cpp_24990(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+14h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x14))')

    def test_cpp_25000(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+18h]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x18))')

    def test_cpp_25010(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+18h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x18))')

    def test_cpp_25020(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+1Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x1C))')

    def test_cpp_25030(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+4]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+4))')

    def test_cpp_25040(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+4))')

    def test_cpp_25050(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+8]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+8))')

    def test_cpp_25060(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+8]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+8))')

    def test_cpp_25070(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp]'),def_size=0,destination=False),u'*(dw*)(raddr(ds,esp))')

    def test_cpp_25080(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp))')

    def test_cpp_25090(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[g]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,offset(_data,g)))')

    def test_cpp_25100(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[h2]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,h2)))')

    def test_cpp_25110(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+1]'),def_size=0,destination=False),u'i+1')

    def test_cpp_25120(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+2]'),def_size=0,destination=False),u'i+2')

    def test_cpp_25130(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+3]'),def_size=0,destination=False),u'i+3')

    def test_cpp_25140(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+4]'),def_size=0,destination=False),u'i+4')

    def test_cpp_25150(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+56h]'),def_size=0,destination=False),u'i+0x56')

    def test_cpp_25160(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+5]'),def_size=0,destination=False),u'i+5')

    def test_cpp_25170(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i-10h]'),def_size=0,destination=False),u'i-0x10')

    def test_cpp_25180(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[load_handle]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,offset(_data,load_handle)))')

    def test_cpp_25190(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[load_handle]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,load_handle)))')

    def test_cpp_25200(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var+3]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)+3))')

    def test_cpp_25210(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var+4]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)+4))')

    def test_cpp_25220(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var-1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)-1))')

    def test_cpp_25230(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var0+5]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var0)+5))')

    def test_cpp_25240(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var1+1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+1))')

    def test_cpp_25250(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var1]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,var1)))')

    def test_cpp_25260(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)))')

    def test_cpp_25270(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2+2]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var2)+2))')

    def test_cpp_25280(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2-1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var2)-1))')

    def test_cpp_25290(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2]'),def_size=0,destination=False),u'*(dw*)(raddr(ds,offset(_data,var2)))')

    def test_cpp_25300(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var2)))')

    def test_cpp_25310(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2]'),def_size=2,destination=True),u'*(dw*)(raddr(ds,offset(_data,var2)))')

    def test_cpp_25320(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3+3*4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+3*4))')

    def test_cpp_25330(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3+ebp]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+ebp))')

    def test_cpp_25340(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3]'),def_size=0,destination=False),u'*(dd*)(raddr(ds,offset(_data,var3)))')

    def test_cpp_25350(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)))')

    def test_cpp_25360(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var4+t]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var4)+t))')

    def test_cpp_25370(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var4]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var4)))')

    def test_cpp_25380(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)))')

    def test_cpp_25390(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'_data'),def_size=1,destination=False),u'seg_offset(_data)')

    def test_cpp_25400(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'a'),def_size=1,destination=True),u'a')

    def test_cpp_25410(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [a]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,a)))')

    def test_cpp_25420(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [ebp+var_20]'),def_size=1,destination=False),u'*(raddr(ds,ebp+var_20))')

    def test_cpp_25430(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [ebp+var_20]'),def_size=1,destination=True),u'*(raddr(ds,ebp+var_20))')

    def test_cpp_25440(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+1]'),def_size=0,destination=False),u'*(raddr(ds,edi+1))')

    def test_cpp_25450(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+1]'),def_size=1,destination=True),u'*(raddr(ds,edi+1))')

    def test_cpp_25460(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+7]'),def_size=0,destination=False),u'*(raddr(ds,edi+7))')

    def test_cpp_25470(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+7]'),def_size=1,destination=True),u'*(raddr(ds,edi+7))')

    def test_cpp_25480(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [esi]'),def_size=1,destination=True),u'*(raddr(ds,esi))')

    def test_cpp_25490(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [h2]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,h2)))')

    def test_cpp_25500(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [h]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,h)))')

    def test_cpp_25510(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [testOVerlap+1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,testOVerlap)+1))')

    def test_cpp_25520(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [var1+1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+1))')

    def test_cpp_25530(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [var1+2]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+2))')

    def test_cpp_25540(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr dl'),def_size=1,destination=True),u'dl')

    def test_cpp_25550(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr ds:[0]'),def_size=1,destination=True),u'*(raddr(ds,0))')

    def test_cpp_25560(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr es:[0]'),def_size=0,destination=False),u'*(raddr(es,0))')

    def test_cpp_25570(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr es:[0]'),def_size=1,destination=True),u'*(raddr(es,0))')
    '''
    def test_cpp_25580(self):
        self.assertEqual(self.parser.parse_arg(u'ds:[eax*2]', def_size=0, destination=False), u'*(raddr(ds,eax*2))')

    def test_cpp_25590(self):
        self.assertEqual(self.parser.parse_arg(u'ds:[ebx*4]', def_size=0, destination=False), u'*(raddr(ds,ebx*4))')

    def test_cpp_25600(self):
        self.assertEqual(self.parser.parse_arg(u'ds:[ecx*8]', def_size=0, destination=False), u'*(raddr(ds,ecx*8))')
    '''
    def test_cpp_25610(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:40h[ebx*4]'), def_size=0, destination=False), u'*(raddr(ds,0x40+ebx*4))')

    def test_cpp_25620(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:40h[ecx*8]'), def_size=0, destination=False), u'*(raddr(ds,0x40+ecx*8))')

    def test_cpp_25630(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:[edi]'),def_size=1,destination=True),u'*(raddr(ds,edi))')

    def test_cpp_25640(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:byte_41411F[eax]'),def_size=1,destination=True),u'*(raddr(ds,offset(_bss,byte_41411F)+eax))')

    def test_cpp_25650(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20+4]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_20+4))')

    def test_cpp_25660(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20+4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_20+4))')

    def test_cpp_25670(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_cpp_25680(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_cpp_25690(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebx-4]'),def_size=0,destination=True),u'*(dd*)(raddr(ds,ebx-4))')

    def test_cpp_25700(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+0Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x0C))')

    def test_cpp_25710(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+10h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x10))')

    def test_cpp_25720(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+14h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x14))')

    def test_cpp_25730(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+1Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x1C))')

    def test_cpp_25740(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+4))')

    def test_cpp_25750(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+8]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+8))')

    def test_cpp_25760(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp))')

    def test_cpp_25770(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr buffer'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,buffer)))')

    def test_cpp_25780(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr es:[0]'),def_size=4,destination=True),u'*(dd*)(raddr(es,0))')

    def test_cpp_25790(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr es:[20*320+160]'),def_size=4,destination=True),u'*(dd*)(raddr(es,20*320+160))')

    def test_cpp_25800(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr var4'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var4)))')

    def test_cpp_25810(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'large ds:4000h'),def_size=0,destination=False),u'large ds:0x4000')

    def test_cpp_25820(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset _msg'),def_size=4,destination=False),u'offset(_data,_msg)')

    def test_cpp_25830(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset _test_btc'),def_size=4,destination=False),u'offset(initcall,_test_btc)')

    def test_cpp_25840(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset a0x4000'),def_size=4,destination=False),u'offset(_rdata,a0x4000)')

    def test_cpp_25850(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset aXorl'),def_size=4,destination=False),u'offset(_rdata,aXorl)')

    def test_cpp_25860(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset aXorw'),def_size=4,destination=False),u'offset(_rdata,aXorw)')

    def test_cpp_25870(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset pal_jeu'),def_size=4,destination=False),u'offset(_data,pal_jeu)')

    def test_cpp_25880(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset str1'),def_size=4,destination=False),u'offset(_data,str1)')

    def test_cpp_25890(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset str2'),def_size=4,destination=False),u'offset(_data,str2)')

    def test_cpp_25900(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset str3'),def_size=4,destination=False),u'offset(_data,str3)')

    def test_cpp_25910(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset testOVerlap'),def_size=4,destination=False),u'offset(_data,testOVerlap)')

    def test_cpp_25920(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset unk_40E008'),def_size=4,destination=False),u'offset(_data,unk_40E008)')

    def test_cpp_25930(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset unk_40F064'),def_size=4,destination=False),u'offset(initcall,unk_40F064)')

    def test_cpp_25940(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var1'),def_size=4,destination=False),u'offset(_data,var1)')

    def test_cpp_25950(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var1+1'),def_size=4,destination=False),u'offset(_data,var1)+1')

    def test_cpp_25960(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var2'),def_size=4,destination=False),u'offset(_data,var2)')

    def test_cpp_25970(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var3'),def_size=4,destination=False),u'offset(_data,var3)')

    def test_cpp_25980(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var3+4'),def_size=4,destination=False),u'offset(_data,var3)+4')

    def test_cpp_25990(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var4'),def_size=4,destination=False),u'offset(_data,var4)')

    def test_cpp_26000(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var4+1'),def_size=4,destination=False),u'offset(_data,var4)+1')

    def test_cpp_26010(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var4+4'),def_size=4,destination=False),u'offset(_data,var4)+4')

    def test_cpp_26020(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'op0'),def_size=0,destination=False),u'op0')

    def test_cpp_26030(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'op0'),def_size=4,destination=True),u'op0')

    def test_cpp_26040(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'op1'),def_size=0,destination=False),u'op1')

    def test_cpp_26050(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'printf'),def_size=0,destination=True),u'printf')

    def test_cpp_26060(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ptr'),def_size=0,destination=False),u'ptr')

    def test_cpp_26070(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'r'),def_size=0,destination=False),u'r')

    def test_cpp_26080(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=0,destination=False),u'res')

    def test_cpp_26090(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=0,destination=True),u'res')

    def test_cpp_26100(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=4,destination=False),u'res')

    def test_cpp_26110(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=4,destination=True),u'res')

    def test_cpp_26120(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'resh'),def_size=0,destination=False),u'resh')

    def test_cpp_26130(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'resh'),def_size=4,destination=False),u'resh')

    def test_cpp_26140(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'resz'),def_size=0,destination=False),u'resz')

    def test_cpp_26150(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'rh'),def_size=0,destination=False),u'rh')

    def test_cpp_26160(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's0_0'),def_size=0,destination=False),u's0_0')

    def test_cpp_26170(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's0_0'),def_size=4,destination=False),u's0_0')

    def test_cpp_26180(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's1_0'),def_size=0,destination=False),u's1_0')

    def test_cpp_26190(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's1_0'),def_size=4,destination=False),u's1_0')

    def test_cpp_26200(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'si'),def_size=2,destination=False),u'si')

    def test_cpp_26210(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'small'),def_size=0,destination=False),u'small')

    def test_cpp_26220(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u't'),def_size=4,destination=False),u't')

    def test_cpp_26230(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'taille_moire'),def_size=4,destination=False),u'taille_moire')

    def test_cpp_26240(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'teST2'),def_size=4,destination=False),u'teST2')

    def test_cpp_26250(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'testOVerlap'),def_size=0,destination=False),u'offset(_data,testOVerlap)')

    def test_cpp_26260(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=0,destination=False),u'var1')

    def test_cpp_26270(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=0,destination=False),u'offset(_data,var1)')

    def test_cpp_26280(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=1,destination=False),u'var1')

    def test_cpp_26290(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=1,destination=True),u'*(db*)&m.var1')

    def test_cpp_26300(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=1,destination=True),u'var1')

    def test_cpp_26310(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1[1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+1))')

    def test_cpp_26320(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1[bx+si]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+bx+si))')

    def test_cpp_26330(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1[bx]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+bx))')

    def test_cpp_26340(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var2'),def_size=0,destination=False),u'offset(_data,var2)')

    def test_cpp_26350(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var2'),def_size=2,destination=True),u'var2')

    #def test_cpp_26360(self):
    #    self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3'),def_size=4,destination=True),u'var3')

    def test_cpp_26370(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3+3*4'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+3*4))')

    def test_cpp_26380(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3+ebp'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+ebp))')

    def test_cpp_26390(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var5'),def_size=0,destination=False),u'offset(_data,var5)')

    def test_cpp_26400(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [d]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,offset(_data,d)))')

    def test_cpp_26410(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [e]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,offset(_data,e)))')

    def test_cpp_26420(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [ebp+var_20]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,ebp+var_20))')

    def test_cpp_26430(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [ebp+var_20]'),def_size=2,destination=True),u'*(dw*)(raddr(ds,ebp+var_20))')

    def test_cpp_26440(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [var5+2]'),def_size=2,destination=True),u'*(dw*)(raddr(ds,offset(_data,var5)+2))')

    def test_cpp_26450(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr var5'),def_size=2,destination=True),u'*(dw*)(raddr(ds,offset(_data,var5)))')

    def test_cpp_26460(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word'),def_size=0,destination=False),u'word')

    def test_cpp_26470(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3'),def_size=0,destination=False),u'var3')
    '''

    def test_cpp_26480(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u"'Z' - 'A' +1")), 1)

    def test_cpp_26490(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u"'a'")), 1)

    def test_cpp_26500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u"'c'")), 1)

    def test_cpp_26510(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u"'d'")), 1)

    def test_cpp_26520(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u"'dcba'")), 4)

    def test_cpp_26530(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u"'tseT'")), 4)

    def test_cpp_26540(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'(1024*10/16)+5')), 2)

    def test_cpp_26550(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'(1024*10/16)-1')), 2)

    def test_cpp_26560(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'(offset str_buffer+800h)')), 2)

    def test_cpp_26570(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'(offset str_buffer+810h)')), 2)

    def test_cpp_26580(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'+40h')), 1)

    def test_cpp_26590(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'+4000H')), 2)

    def test_cpp_26600(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-108h')), 2)

    def test_cpp_26610(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-1Ch')), 1)

    def test_cpp_26620(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-20h')), 1)

    def test_cpp_26630(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-28h')), 1)

    def test_cpp_26640(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-2Ch')), 1)

    def test_cpp_26650(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-1')), 1)

    def test_cpp_26660(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-1-(-2+3)')), 1)

    def test_cpp_26670(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'-12')), 1)

    def test_cpp_26680(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0')), 1)

    def test_cpp_26690(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0002h')), 1)

    def test_cpp_26700(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0007')), 1)

    def test_cpp_26710(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'000f3h')), 1)

    def test_cpp_26720(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'000ff00ffh')), 4)

    def test_cpp_26730(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'001111111B')), 1)

    def test_cpp_26740(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'00fffh')), 2)

    def test_cpp_26750(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'00h')), 1)

    def test_cpp_26760(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0100b')), 1)

    def test_cpp_26770(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'01010101010101010b')), 2)

    def test_cpp_26780(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0101010101010101b')), 2)

    def test_cpp_26790(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0101b')), 1)

    def test_cpp_26800(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'010B')), 1)

    def test_cpp_26810(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'011111100B')), 1)

    def test_cpp_26820(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'011111111111111111111111111111111b')), 4)

    def test_cpp_26830(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'01111111111111111b')), 2)

    def test_cpp_26840(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'011111111B')), 1)

    def test_cpp_26850(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'012345678h')), 4)

    def test_cpp_26860(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'01B')), 1)

    def test_cpp_26870(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'01h')), 1)

    def test_cpp_26880(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'02h')), 1)

    def test_cpp_26890(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'03dh')), 1)

    def test_cpp_26900(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'03eh')), 1)

    def test_cpp_26910(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'03fh')), 1)

    def test_cpp_26920(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'042h')), 1)

    def test_cpp_26930(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'077123456h')), 4)

    def test_cpp_26940(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'077aaFF00h')), 4)

    def test_cpp_26950(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'08h')), 1)

    def test_cpp_26960(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0B')), 1)

    def test_cpp_26970(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0BC6058h')), 4)

    def test_cpp_26980(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0D5h')), 1)

    def test_cpp_26990(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0Eh')), 1)

    def test_cpp_27000(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0F7h')), 1)

    def test_cpp_27010(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FBCA7654h')), 4)

    def test_cpp_27020(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FBCA7h')), 4)

    def test_cpp_27030(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FEh')), 1)

    def test_cpp_27040(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFEh')), 2)

    def test_cpp_27050(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFC70F9h')), 4)

    def test_cpp_27060(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFE0080h')), 4)

    def test_cpp_27070(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFEDCBFh')), 4)

    def test_cpp_27080(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFEFDFCh')), 4)

    def test_cpp_27090(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFEh')), 2)

    def test_cpp_27100(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFF7FFFh')), 4)

    def test_cpp_27110(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFA549h')), 4)

    def test_cpp_27120(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFEh')), 4)

    def test_cpp_27130(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFED4h')), 4)

    def test_cpp_27140(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFEh')), 4)

    def test_cpp_27150(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFD3h')), 4)

    def test_cpp_27160(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFECh')), 4)

    def test_cpp_27170(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFEh')), 4)

    def test_cpp_27180(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFF0h')), 4)

    def test_cpp_27190(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFF7h')), 4)

    def test_cpp_27200(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFAh')), 4)

    def test_cpp_27210(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFBh')), 4)

    def test_cpp_27220(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFCh')), 4)

    def test_cpp_27230(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFDh')), 4)

    def test_cpp_27240(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFEh')), 4)

    def test_cpp_27250(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFFh')), 4)

    def test_cpp_27260(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFFh')), 4)

    def test_cpp_27270(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFFh')), 4)

    def test_cpp_27280(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFFh')), 4)

    def test_cpp_27290(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFFh')), 2)

    def test_cpp_27300(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFFh')), 2)

    def test_cpp_27310(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0FFh')), 1)

    def test_cpp_27320(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0Fh')), 1)

    def test_cpp_27330(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0a0000h')), 4)

    def test_cpp_27340(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0a000h')), 2)

    def test_cpp_27350(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0aabbccddh')), 4)

    def test_cpp_27360(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0abcdef77h')), 4)

    def test_cpp_27370(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0af222h')), 4)

    def test_cpp_27380(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0cch')), 1)

    def test_cpp_27390(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ddh')), 1)

    def test_cpp_27400(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0df01h')), 2)

    def test_cpp_27410(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0dff1h')), 2)

    def test_cpp_27420(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0f0ffh')), 2)

    def test_cpp_27430(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0f0h')), 1)

    def test_cpp_27440(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0f222h')), 2)

    def test_cpp_27450(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffff0003h')), 4)

    def test_cpp_27460(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffff00f3h')), 4)

    def test_cpp_27470(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffff01ffh')), 4)

    def test_cpp_27480(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffffff00h')), 4)

    def test_cpp_27490(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffffff03h')), 4)

    def test_cpp_27500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0fffffff3h')), 4)

    def test_cpp_27510(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffffffffh')), 4)

    def test_cpp_27520(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffffh')), 2)

    def test_cpp_27530(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0ffh')), 1)

    def test_cpp_27540(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'0Ch')), 1)

    def test_cpp_27550(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1')), 1)

    def test_cpp_27560(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'10')), 1)

    def test_cpp_27570(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'10000h')), 4)

    def test_cpp_27580(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1000h')), 2)

    def test_cpp_27590(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'100h')), 2)

    def test_cpp_27600(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1024*10/16')), 2)

    def test_cpp_27610(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1024*1024')), 4)

    def test_cpp_27620(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'10B')), 1)

    def test_cpp_27630(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'10h')), 1)

    def test_cpp_27640(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'11')), 1)

    def test_cpp_27650(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'111')), 1)

    def test_cpp_27660(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'114h')), 2)

    def test_cpp_27670(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'11h')), 1)

    def test_cpp_27680(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12')), 1)

    def test_cpp_27690(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340004h')), 4)

    def test_cpp_27700(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1234001Dh')), 4)

    def test_cpp_27710(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340128h')), 4)

    def test_cpp_27720(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340205h')), 4)

    def test_cpp_27730(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340306h')), 4)

    def test_cpp_27740(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340407h')), 4)

    def test_cpp_27750(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1234040Ah')), 4)

    def test_cpp_27760(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340503h')), 4)

    def test_cpp_27770(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340506h')), 4)

    def test_cpp_27780(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340507h')), 4)

    def test_cpp_27790(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340547h')), 4)

    def test_cpp_27800(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340559h')), 4)

    def test_cpp_27810(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12340560h')), 4)

    def test_cpp_27820(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1234059Fh')), 4)

    def test_cpp_27830(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'123405A0h')), 4)

    def test_cpp_27840(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'123405FAh')), 4)

    def test_cpp_27850(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12341678h')), 4)

    def test_cpp_27860(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12341h')), 4)

    def test_cpp_27870(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12343h')), 4)

    def test_cpp_27880(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12345')), 2)

    def test_cpp_27890(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1234561Dh')), 4)

    def test_cpp_27900(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12345678h')), 4)

    def test_cpp_27910(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12345h')), 4)

    def test_cpp_27920(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12347F7Fh')), 4)

    def test_cpp_27930(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12347FFFh')), 4)

    def test_cpp_27940(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12348000h')), 4)

    def test_cpp_27950(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12348080h')), 4)

    def test_cpp_27960(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1234h')), 2)

    def test_cpp_27970(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'127Eh')), 2)

    def test_cpp_27980(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'12Ch')), 2)

    def test_cpp_27990(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'13')), 1)

    def test_cpp_28000(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'132')), 1)

    def test_cpp_28010(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'133')), 1)

    def test_cpp_28020(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'13h')), 1)

    def test_cpp_28030(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'14')), 1)

    def test_cpp_28040(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'14*320')), 2)

    def test_cpp_28050(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'14h')), 1)

    def test_cpp_28060(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'15')), 1)

    def test_cpp_28070(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'16')), 1)

    def test_cpp_28080(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'17')), 1)

    def test_cpp_28090(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'17h')), 1)

    def test_cpp_28100(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'18')), 1)

    def test_cpp_28110(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'18h')), 1)

    def test_cpp_28120(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'19')), 1)

    def test_cpp_28130(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'192')), 1)

    def test_cpp_28140(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'193')), 1)

    def test_cpp_28150(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1Ch')), 1)

    def test_cpp_28160(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1Eh')), 1)

    def test_cpp_28170(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FEh')), 2)

    def test_cpp_28180(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FF7Fh')), 4)

    def test_cpp_28190(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FF80h')), 4)

    def test_cpp_28200(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FF81h')), 4)

    def test_cpp_28210(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFEh')), 2)

    def test_cpp_28220(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFEh')), 4)

    def test_cpp_28230(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFEh')), 4)

    def test_cpp_28240(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFFEh')), 4)

    def test_cpp_28250(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFFFEh')), 4)

    def test_cpp_28260(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFFFFh')), 4)

    def test_cpp_28270(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFFFh')), 4)

    def test_cpp_28280(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFFh')), 4)

    def test_cpp_28290(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFFh')), 4)

    def test_cpp_28300(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFFh')), 2)

    def test_cpp_28310(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1FFh')), 2)

    def test_cpp_28320(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'1Fh')), 1)

    def test_cpp_28330(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'2')), 1)

    def test_cpp_28340(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'20')), 1)

    def test_cpp_28350(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'20000h')), 4)

    def test_cpp_28360(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'20h')), 1)

    def test_cpp_28370(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'21')), 1)

    def test_cpp_28380(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'21AD3D34h')), 4)

    def test_cpp_28390(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'21h')), 1)

    def test_cpp_28400(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'22')), 1)

    def test_cpp_28410(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'23')), 1)

    def test_cpp_28420(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'24')), 1)

    def test_cpp_28430(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'24h')), 1)

    def test_cpp_28440(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'25')), 1)

    def test_cpp_28450(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'255')), 1)

    def test_cpp_28460(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'256')), 2)

    def test_cpp_28470(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'256*3')), 2)

    def test_cpp_28480(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'256+3')), 2)

    def test_cpp_28490(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'256+3+65536')), 4)

    def test_cpp_28500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'26')), 1)

    def test_cpp_28510(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'2Dh')), 1)

    def test_cpp_28520(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3')), 1)

    def test_cpp_28530(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3*4')), 1)

    def test_cpp_28540(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'30')), 1)

    def test_cpp_28550(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'303Bh')), 2)

    def test_cpp_28560(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'30h')), 1)

    def test_cpp_28570(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'31')), 1)

    def test_cpp_28580(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'31h')), 1)

    def test_cpp_28590(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'32')), 1)

    def test_cpp_28600(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'320*200/4')), 2)

    def test_cpp_28610(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'32432434h')), 4)

    def test_cpp_28620(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'340128h')), 4)

    def test_cpp_28630(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'35')), 1)

    def test_cpp_28640(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'37')), 1)

    def test_cpp_28650(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'39h')), 1)

    def test_cpp_28660(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3Ch')), 1)

    def test_cpp_28670(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3DAh')), 2)

    def test_cpp_28680(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3Eh')), 1)

    def test_cpp_28690(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FEh')), 2)

    def test_cpp_28700(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFEh')), 2)

    def test_cpp_28710(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFEh')), 4)

    def test_cpp_28720(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFEh')), 4)

    def test_cpp_28730(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFFEh')), 4)

    def test_cpp_28740(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFFFEh')), 4)

    def test_cpp_28750(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFFFFh')), 4)

    def test_cpp_28760(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFFFh')), 4)

    def test_cpp_28770(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFFh')), 4)

    def test_cpp_28780(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFFh')), 4)

    def test_cpp_28790(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFFh')), 2)

    def test_cpp_28800(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3FFh')), 2)

    def test_cpp_28810(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3Fh')), 1)

    def test_cpp_28820(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3c8h')), 2)

    def test_cpp_28830(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3c9h')), 2)

    def test_cpp_28840(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'3h')), 1)

    def test_cpp_28850(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'4')), 1)

    def test_cpp_28860(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'4+5*256')), 2)

    def test_cpp_28870(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'4000000')), 4)

    def test_cpp_28880(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'40h')), 1)

    def test_cpp_28890(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'43210123h')), 4)

    def test_cpp_28900(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'48h')), 1)

    def test_cpp_28910(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'49h')), 1)

    def test_cpp_28920(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'4Ah')), 1)

    def test_cpp_28930(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'4Ch')), 1)

    def test_cpp_28940(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'4ch')), 1)

    def test_cpp_28950(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'5')), 1)

    def test_cpp_28960(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'50')), 1)

    def test_cpp_28970(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'501h')), 2)

    def test_cpp_28980(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'511')), 2)

    def test_cpp_28990(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'55')), 1)

    def test_cpp_29000(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'56')), 1)

    def test_cpp_29010(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'57')), 1)

    def test_cpp_29020(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'6')), 1)

    def test_cpp_29030(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'6*256+5')), 2)

    def test_cpp_29040(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'60')), 1)

    def test_cpp_29050(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'65324h')), 4)

    def test_cpp_29060(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'65423456h')), 4)

    def test_cpp_29070(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'6789ABCDh')), 4)

    def test_cpp_29080(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7')), 1)

    def test_cpp_29090(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7Eh')), 1)

    def test_cpp_29100(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FEh')), 2)

    def test_cpp_29110(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFEh')), 2)

    def test_cpp_29120(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFEh')), 4)

    def test_cpp_29130(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFEh')), 4)

    def test_cpp_29140(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFFEh')), 4)

    def test_cpp_29150(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFFFEh')), 4)

    def test_cpp_29160(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFFFFh')), 4)

    def test_cpp_29170(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFFFh')), 4)

    def test_cpp_29180(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFFh')), 4)

    def test_cpp_29190(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFFh')), 4)

    def test_cpp_29200(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFFh')), 2)

    def test_cpp_29210(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7FFh')), 2)

    def test_cpp_29220(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'7Fh')), 1)

    def test_cpp_29230(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'8')), 1)

    def test_cpp_29240(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'80000000h')), 4)

    def test_cpp_29250(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'80000001h')), 4)

    def test_cpp_29260(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'80008481h')), 4)

    def test_cpp_29270(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'80008688h')), 4)

    def test_cpp_29280(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'8000h')), 2)

    def test_cpp_29290(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'801h')), 2)

    def test_cpp_29300(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'80h')), 1)

    def test_cpp_29310(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'81234567h')), 4)

    def test_cpp_29320(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'81238567h')), 4)

    def test_cpp_29330(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'812FADAh')), 4)

    def test_cpp_29340(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'813F3421h')), 4)

    def test_cpp_29350(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'81h')), 1)

    def test_cpp_29360(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'82345679h')), 4)

    def test_cpp_29370(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'8234A6F8h')), 4)

    def test_cpp_29380(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'8345A1F2h')), 4)

    def test_cpp_29390(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'8C5h')), 2)

    def test_cpp_29400(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'8D5h')), 2)

    def test_cpp_29410(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'9')), 1)

    def test_cpp_29420(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'9ABCDEFh')), 4)

    def test_cpp_29430(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'AL')), 1)

    def test_cpp_29440(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'B')), 0)

    def test_cpp_29450(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'CC')), 0)

    def test_cpp_29460(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'DDD')), 0)

    def test_cpp_29470(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'DX')), 2)

    def test_cpp_29480(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'OFFSET ASCiI')), 2)

    def test_cpp_29490(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'OFFSET AsCii')), 2)

    def test_cpp_29500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'TWO')), 0)

    def test_cpp_29510(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[a+1]')), 0)

    #def test_cpp_29520(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[a]')),0)

    def test_cpp_29530(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[cs:table+ax]')), 0)

    def test_cpp_29540(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[doublequote+4]')), 0)

    def test_cpp_29550(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[eax+4000h]')), 0)

    def test_cpp_29560(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[eax+40h]')), 0)

    def test_cpp_29570(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[eax+ecx+40h]')), 0)

    def test_cpp_29580(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[eax+ecx]')), 0)

    def test_cpp_29590(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[eax]')), 0)

    def test_cpp_29600(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+ecx_0]')), 0)

    def test_cpp_29610(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+ecx_vals]')), 0)

    def test_cpp_29620(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+edx_0]')), 0)

    def test_cpp_29630(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+i*4+ecx_vals]')), 0)

    def test_cpp_29640(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+i+table]')), 0)

    def test_cpp_29650(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+iflags]')), 0)

    def test_cpp_29660(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+op0]')), 0)

    def test_cpp_29670(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+op0h]')), 0)

    def test_cpp_29680(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+s0]')), 0)

    def test_cpp_29690(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+s1]')), 0)

    def test_cpp_29700(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+s2]')), 0)

    def test_cpp_29710(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+table]')), 0)

    def test_cpp_29720(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+var_1C]')), 0)

    def test_cpp_29730(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+var_20]')), 0)

    def test_cpp_29740(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebp+var_4]')), 0)

    def test_cpp_29750(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebx+4000h]')), 0)

    def test_cpp_29760(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebx+40h]')), 0)

    def test_cpp_29770(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebx+edx+4000h]')), 0)

    def test_cpp_29780(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebx+edx]')), 0)

    def test_cpp_29790(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ebx]')), 0)

    def test_cpp_29800(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx+4000h]')), 0)

    def test_cpp_29810(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx+40h]')), 0)

    def test_cpp_29820(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx+ecx*2+4000h]')), 0)

    def test_cpp_29830(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx+ecx*2-0Ah]')), 0)

    def test_cpp_29840(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx+ecx*2]')), 0)

    def test_cpp_29850(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx+ecx]')), 0)

    def test_cpp_29860(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[ecx]')), 0)

    def test_cpp_29870(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edi+1]')), 0)

    def test_cpp_29880(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edi+4000h]')), 0)

    def test_cpp_29890(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edi+40h]')), 0)

    def test_cpp_29900(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edi+ecx]')), 0)

    def test_cpp_29910(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edi]')), 0)

    def test_cpp_29920(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx+4000h]')), 0)

    def test_cpp_29930(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx+40h]')), 0)

    def test_cpp_29940(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx+ecx*4+4000h]')), 0)

    def test_cpp_29950(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx+ecx*4-0Ah]')), 0)

    def test_cpp_29960(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx+ecx*4]')), 0)

    def test_cpp_29970(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx+ecx]')), 0)

    def test_cpp_29980(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[edx]')), 0)

    def test_cpp_29990(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi+4000h]')), 0)

    def test_cpp_30000(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi+40h]')), 0)

    def test_cpp_30010(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi+ecx*8+4000h]')), 0)

    def test_cpp_30020(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi+ecx*8-0Ah]')), 0)

    def test_cpp_30030(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi+ecx*8]')), 0)

    def test_cpp_30040(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi+ecx]')), 0)

    def test_cpp_30050(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esi]')), 0)

    def test_cpp_30060(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+0Ch]')), 0)

    def test_cpp_30070(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+10h]')), 0)

    def test_cpp_30080(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+14h]')), 0)

    def test_cpp_30090(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+18h]')), 0)

    def test_cpp_30100(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+1Ch]')), 0)

    def test_cpp_30110(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+4]')), 0)

    def test_cpp_30120(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp+8]')), 0)

    def test_cpp_30130(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[esp]')), 0)

    #def test_cpp_30140(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[g]')),0)

    #def test_cpp_30150(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[h2]')),0)

    def test_cpp_30160(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i+1]')), 0)

    def test_cpp_30170(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i+2]')), 0)

    def test_cpp_30180(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i+3]')), 0)

    def test_cpp_30190(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i+4]')), 0)

    def test_cpp_30200(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i+56h]')), 0)

    def test_cpp_30210(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i+5]')), 0)

    def test_cpp_30220(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[i-10h]')), 0)

    #def test_cpp_30230(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[load_handle]')),0)

    def test_cpp_30240(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var+3]')), 0)

    def test_cpp_30250(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var+4]')), 0)

    def test_cpp_30260(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var-1]')), 0)

    def test_cpp_30270(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var0+5]')), 0)

    def test_cpp_30280(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var1+1]')), 0)

    #def test_cpp_30290(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var1]')),0)

    def test_cpp_30300(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var2+2]')), 0)

    def test_cpp_30310(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var2-1]')), 0)

    #def test_cpp_30320(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var2]')),0)

    #def test_cpp_30330(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var2]')),0)

    def test_cpp_30340(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var3+3*4]')), 0)

    def test_cpp_30350(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'[var3+ebp]')), 0)

    #def test_cpp_30360(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var3]')),0)

    #def test_cpp_30370(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var4+t]')),0)

    #def test_cpp_30380(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var4]')),0)

    #def test_cpp_30390(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var]')),0)

    #def test_cpp_30400(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'_data')),1)

    #def test_cpp_30410(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'a')),1)

    def test_cpp_30420(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ah')), 1)

    def test_cpp_30430(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'al')), 1)

    def test_cpp_30440(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ax')), 2)

    #def test_cpp_30450(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'b')),1)

    #def test_cpp_30460(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'b')),2)

    #def test_cpp_30470(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'beginningdata')),1)

    def test_cpp_30480(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'bh')), 1)

    def test_cpp_30490(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'bl')), 1)

    def test_cpp_30500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'bp')), 2)

    #def test_cpp_30510(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'buffer')),1)

    def test_cpp_30520(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'bx')), 2)

    def test_cpp_30530(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [a]')), 1)

    def test_cpp_30540(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [ebp+var_20]')), 1)

    def test_cpp_30550(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [edi+1]')), 1)

    def test_cpp_30560(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [edi+7]')), 1)

    def test_cpp_30570(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [esi]')), 1)

    def test_cpp_30580(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [h2]')), 1)

    def test_cpp_30590(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [h]')), 1)

    def test_cpp_30600(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [testOVerlap+1]')), 1)

    def test_cpp_30610(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [var1+1]')), 1)

    def test_cpp_30620(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr [var1+2]')), 1)

    def test_cpp_30630(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr dl')), 1)

    def test_cpp_30640(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr ds:[0]')), 1)

    def test_cpp_30650(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'byte ptr es:[0]')), 1)

    #def test_cpp_30660(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'c')),4)

    def test_cpp_30670(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ch')), 1)

    def test_cpp_30680(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'cl')), 1)

    def test_cpp_30690(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'cx')), 2)

    def test_cpp_30700(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'di')), 2)

    def test_cpp_30710(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dl')), 1)

    def test_cpp_30720(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds')), 2)

    def test_cpp_30730(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:0[eax*2]')), 0)

    def test_cpp_30740(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:0[ebx*4]')), 0)

    def test_cpp_30750(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:0[ecx*8]')), 0)

    def test_cpp_30760(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:40h[eax*2]')), 0)

    def test_cpp_30770(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:40h[ebx*4]')), 0)

    def test_cpp_30780(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:40h[ecx*8]')), 0)

    def test_cpp_30790(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ds:[edi]')), 0)

    #def test_cpp_30800(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'ds:byte_41411F[eax]')),1)

    def test_cpp_30810(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [ebp+var_20+4]')), 4)

    def test_cpp_30820(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [ebp+var_20]')), 4)

    def test_cpp_30830(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [ebx-4]')), 4)

    def test_cpp_30840(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp+0Ch]')), 4)

    def test_cpp_30850(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp+10h]')), 4)

    def test_cpp_30860(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp+14h]')), 4)

    def test_cpp_30870(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp+1Ch]')), 4)

    def test_cpp_30880(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp+4]')), 4)

    def test_cpp_30890(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp+8]')), 4)

    def test_cpp_30900(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr [esp]')), 4)

    def test_cpp_30910(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr buffer')), 4)

    def test_cpp_30920(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr es:[0]')), 4)

    def test_cpp_30930(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr es:[20*320+160]')), 4)

    def test_cpp_30940(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dword ptr var4')), 4)

    def test_cpp_30950(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'dx')), 2)

    def test_cpp_30960(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'eax')), 4)

    def test_cpp_30970(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'eax_0')), 0)

    def test_cpp_30980(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ebp')), 4)

    def test_cpp_30990(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ebx')), 4)

    def test_cpp_31000(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ecx')), 4)

    def test_cpp_31010(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ecx_0')), 0)

    def test_cpp_31020(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'ecx_0_0')), 0)

    def test_cpp_31030(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'edi')), 4)

    def test_cpp_31040(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'edi_0')), 0)

    def test_cpp_31050(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'edx')), 4)

    def test_cpp_31060(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'edx_0_0')), 0)

    def test_cpp_31070(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'eflags')), 0)

    #def test_cpp_31080(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'enddata')),1)

    def test_cpp_31090(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'es')), 2)

    def test_cpp_31100(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'esi')), 4)

    def test_cpp_31110(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'esi_0')), 0)

    def test_cpp_31120(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'esp')), 4)

    #def test_cpp_31130(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'fileName')),1)

    def test_cpp_31140(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'flags')), 0)

    def test_cpp_31150(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'fs')), 2)

    #def test_cpp_31160(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'g')),4)

    def test_cpp_31170(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'i')), 0)

    def test_cpp_31180(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'large ds:4000h')), 4)

    def test_cpp_31190(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset _msg')), 2)

    def test_cpp_31200(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset _test_btc')), 2)

    def test_cpp_31210(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset pal_jeu')), 2)

    def test_cpp_31220(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset str1')), 2)

    def test_cpp_31230(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset str2')), 2)

    def test_cpp_31240(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset str3')), 2)

    def test_cpp_31250(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset str_buffer+810h')), 2)

    def test_cpp_31260(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset testOVerlap')), 2)

    def test_cpp_31270(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset unk_40E008')), 2)

    def test_cpp_31280(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset unk_40F064')), 2)

    def test_cpp_31290(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var1')), 2)

    def test_cpp_31300(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var1+1')), 2)

    def test_cpp_31310(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var2')), 2)

    def test_cpp_31320(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var3')), 2)

    def test_cpp_31330(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var3+4')), 2)

    def test_cpp_31340(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var4')), 2)

    def test_cpp_31350(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var4+1')), 2)

    def test_cpp_31360(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'offset var4+4')), 2)

    def test_cpp_31370(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'op0')), 0)

    def test_cpp_31380(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'op1')), 0)

    def test_cpp_31390(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'printf')), 0)

    def test_cpp_31400(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'r')), 0)

    def test_cpp_31410(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'res')), 0)

    def test_cpp_31420(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'resh')), 0)

    def test_cpp_31430(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'resz')), 0)

    def test_cpp_31440(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'rh')), 0)

    def test_cpp_31450(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u's0_0')), 0)

    def test_cpp_31460(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u's1_0')), 0)

    def test_cpp_31470(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'si')), 2)

    def test_cpp_31480(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u't')), 0)

    def test_cpp_31490(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'taille_moire')), 0)

    def test_cpp_31500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'teST2')), 0)

    def test_cpp_31500(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'teST2')), 0)

    def test_cpp_31510(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'fs: 8')), 0)

    #def test_cpp_31520(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var1')),1)

    #def test_cpp_31530(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var1[1]')),1)

    #def test_cpp_31540(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var1[bx+si]')),1)

    #def test_cpp_31550(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var1[bx]')),1)

    #def test_cpp_31560(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var2')),2)

    #def test_cpp_31570(self):
    #    self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var3')),4)

    #def test_cpp_31580(self):
    #    self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var3+3*4')),4)

    def test_cpp_31590(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'var3+ebp')), 4)

    #def test_cpp_31600(self):
    #   self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var5')),1)

    def test_cpp_31610(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'word ptr [d]')), 2)

    def test_cpp_31620(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'word ptr [e]')), 2)

    def test_cpp_31630(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'word ptr [ebp+var_20]')), 2)

    def test_cpp_31640(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'word ptr [var5+2]')), 2)

    def test_cpp_31650(self):
        self.assertEqual(self.cpp.calculate_size(self.parser.test_size(u'word ptr var5')), 2)

    def test_cpp_31660(self):
        self.assertEqual(self.parser.is_register(expr=u'_data'), 0)

    def test_cpp_31670(self):
        self.assertEqual(self.parser.is_register(expr=u'offset var1'), 0)

    def test_cpp_31680(self):
        self.assertEqual(self.parser.is_register(expr=u'var1'), 0)

    def test_cpp_31690(self):
        self.assertEqual(self.parser.is_register(expr=u'cl'), 1)

    def test_cpp_31700(self):
        self.assertEqual(self.parser.is_register(expr=u'[edi+1]'), 0)

    def test_cpp_31710(self):
        self.assertEqual(self.parser.is_register(expr=u'[doublequote+4]'), 0)

    def test_cpp_31720(self):
        self.assertEqual(self.parser.is_register(expr=u'dl'), 1)

    def test_cpp_31730(self):
        self.assertEqual(self.parser.is_register(expr=u'-12'), 0)

    def test_cpp_31740(self):
        self.assertEqual(self.parser.is_register(expr=u'teST2'), 0)

    def test_cpp_31750(self):
        self.assertEqual(self.parser.is_register(expr=u"'d'"), 0)

    def test_cpp_31760(self):
        self.assertEqual(self.parser.is_register(expr=u'dx'), 2)

    def test_cpp_31770(self):
        self.assertEqual(self.parser.is_register(expr=u'esi'), 4)

    def test_cpp_31780(self):
        self.assertEqual(self.parser.is_register(expr=u'enddata'), 0)

    def test_cpp_31790(self):
        self.assertEqual(self.parser.is_register(expr=u"'Z' - 'A' +1"), 0)

    def test_cpp_31800(self):
        self.assertEqual(self.parser.is_register(expr=u'beginningdata'), 0)

    def test_cpp_31810(self):
        self.assertEqual(self.parser.is_register(expr=u'al'), 1)

    def test_cpp_31820(self):
        self.assertEqual(self.parser.is_register(expr=u'ebx'), 4)

    def test_cpp_31830(self):
        self.assertEqual(self.parser.is_register(expr=u'edi'), 4)

    def test_cpp_31840(self):
        self.assertEqual(self.parser.is_register(expr=u'ds'), 2)

    def test_cpp_31850(self):
        self.assertEqual(self.parser.is_register(expr=u'eax'), 4)

    def test_cpp_31860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u"'Z' - 'A' +1"), u"'Z' - 'A' +1")

    def test_cpp_31870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'((((2030080+64000*26)/4096)+1)*4096)-1'), u'((((2030080+64000*26)/4096)+1)*4096)-1')

    def test_cpp_31880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'(00+38*3)*320+1/2+33*(3-1)'), u'(00+38*3)*320+1/2+33*(3-1)')

    def test_cpp_31890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'(1024*10/16)+5'), u'(1024*10/16)+5')

    def test_cpp_31900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'(1024*10/16)-1'), u'(1024*10/16)-1')

    def test_cpp_31910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+0x40'), u'+0x40')

    def test_cpp_31920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+0x4000'), u'+0x4000')

    def test_cpp_31930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx'), u'+ecx')

    def test_cpp_31940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx*2'), u'+ecx*2')

    def test_cpp_31950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx*2+0x4000'), u'+ecx*2+0x4000')

    def test_cpp_31960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx*2-0x0A'), u'+ecx*2-0x0A')

    def test_cpp_31970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx*4'), u'+ecx*4')

    def test_cpp_31980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx*4+0x4000'), u'+ecx*4+0x4000')

    def test_cpp_31990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx*4-0x0A'), u'+ecx*4-0x0A')

    def test_cpp_32000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+ecx+0x40'), u'+ecx+0x40')

    def test_cpp_32010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+edx'), u'+edx')

    def test_cpp_32020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'+edx+0x4000'), u'+edx+0x4000')

    def test_cpp_32030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-0x108'), u'-0x108')

    def test_cpp_32040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-0x1C'), u'-0x1C')

    def test_cpp_32050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-0x20'), u'-0x20')

    def test_cpp_32060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-0x28'), u'-0x28')

    def test_cpp_32070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-0x2C'), u'-0x2C')

    def test_cpp_32080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-1'), u'-1')

    def test_cpp_32090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-1-(-2+3)'), u'-1-(-2+3)')

    def test_cpp_32100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-108h'), u'-0x108')

    def test_cpp_32110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-12'), u'-12')

    def test_cpp_32130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-1Ch'), u'-0x1C')

    def test_cpp_32140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-2'), u'-2')

    def test_cpp_32170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-2Ch'), u'-0x2C')

    def test_cpp_32180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-2Dh'), u'-0x2D')

    def test_cpp_32190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'-4'), u'-4')

    def test_cpp_32220(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0'), u'0')

    def test_cpp_32230(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0002h'), u'0x0002')

    def test_cpp_32240(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0007'), u'0007')

    def test_cpp_32250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'000f3h'), u'0x000f3')

    def test_cpp_32260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'000ff00ffh'), u'0x000ff00ff')

    def test_cpp_32270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'001111111B'), u'0x7f')

    def test_cpp_32280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'00fffh'), u'0x00fff')

    def test_cpp_32290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'00h'), u'0x00')

    def test_cpp_32300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0100b'), u'0x4')

    def test_cpp_32310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'01010101010101010b'), u'0xaaaa')

    def test_cpp_32320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0101010101010101b'), u'0x5555')

    def test_cpp_32330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0101b'), u'0x5')

    def test_cpp_32340(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'010B'), u'0x2')

    def test_cpp_32350(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'011111100B'), u'0xfc')

    def test_cpp_32360(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'011111111111111111111111111111111b'), u'0xffffffff')

    def test_cpp_32370(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'01111111111111111b'), u'0xffff')

    def test_cpp_32380(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'011111111B'), u'0xff')

    def test_cpp_32390(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'012345678h'), u'0x012345678')

    def test_cpp_32400(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'01B'), u'0x1')

    def test_cpp_32410(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'01h'), u'0x01')

    def test_cpp_32420(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'02h'), u'0x02')

    def test_cpp_32430(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'03dh'), u'0x03d')

    def test_cpp_32440(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'03eh'), u'0x03e')

    def test_cpp_32450(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'03fh'), u'0x03f')

    def test_cpp_32470(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'077123456h'), u'0x077123456')

    def test_cpp_32480(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'077aaFF00h'), u'0x077aaFF00')

    def test_cpp_32490(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'08h'), u'0x08')

    def test_cpp_32500(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0B'), u'0x0')

    def test_cpp_32510(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0BC6058h'), u'0x0BC6058')

    def test_cpp_32520(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0Ch'), u'0x0C')

    def test_cpp_32530(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0D5h'), u'0x0D5')

    def test_cpp_32540(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0Eh'), u'0x0E')

    def test_cpp_32550(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0F7h'), u'0x0F7')

    def test_cpp_32560(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FBCA7654h'), u'0x0FBCA7654')

    def test_cpp_32570(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FBCA7h'), u'0x0FBCA7')

    def test_cpp_32580(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FEh'), u'0x0FE')

    def test_cpp_32590(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFEh'), u'0x0FFE')

    def test_cpp_32600(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFC70F9h'), u'0x0FFFC70F9')

    def test_cpp_32610(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFE0080h'), u'0x0FFFE0080')

    def test_cpp_32620(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFEDCBFh'), u'0x0FFFEDCBF')

    def test_cpp_32630(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFEFDFCh'), u'0x0FFFEFDFC')

    def test_cpp_32640(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFEh'), u'0x0FFFE')

    def test_cpp_32650(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFF7FFFh'), u'0x0FFFF7FFF')

    def test_cpp_32660(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFA549h'), u'0x0FFFFA549')

    def test_cpp_32670(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFEh'), u'0x0FFFFE')

    def test_cpp_32680(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFED4h'), u'0x0FFFFFED4')

    def test_cpp_32690(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFEh'), u'0x0FFFFFE')

    def test_cpp_32700(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFD3h'), u'0x0FFFFFFD3')

    def test_cpp_32710(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFECh'), u'0x0FFFFFFEC')

    def test_cpp_32720(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFEh'), u'0x0FFFFFFE')

    def test_cpp_32730(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFF0h'), u'0x0FFFFFFF0')

    def test_cpp_32740(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFF7h'), u'0x0FFFFFFF7')

    def test_cpp_32750(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFFAh'), u'0x0FFFFFFFA')

    def test_cpp_32760(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFFh'), u'0x0FFFFFFF')

    def test_cpp_32770(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFFh'), u'0x0FFFFFF')

    def test_cpp_32780(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFFh'), u'0x0FFFFF')

    def test_cpp_32790(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFFh'), u'0x0FFFF')

    def test_cpp_32800(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFFh'), u'0x0FFF')

    def test_cpp_32810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0FFh'), u'0x0FF')

    def test_cpp_32820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0Fh'), u'0x0F')

    def test_cpp_32830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0a0000h'), u'0x0a0000')

    def test_cpp_32840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0a000h'), u'0x0a000')

    def test_cpp_32850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0aabbccddh'), u'0x0aabbccdd')

    def test_cpp_32860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0abcdef77h'), u'0x0abcdef77')

    def test_cpp_32870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0af222h'), u'0x0af222')

    def test_cpp_32880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0cch'), u'0x0cc')

    def test_cpp_32890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ddh'), u'0x0dd')

    def test_cpp_32900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0df01h'), u'0x0df01')

    def test_cpp_32910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0dff1h'), u'0x0dff1')

    def test_cpp_32920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0f0ffh'), u'0x0f0ff')

    def test_cpp_32930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0f0h'), u'0x0f0')

    def test_cpp_32940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0f222h'), u'0x0f222')

    def test_cpp_32950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffff0003h'), u'0x0ffff0003')

    def test_cpp_32960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffff00f3h'), u'0x0ffff00f3')

    def test_cpp_32970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffff01ffh'), u'0x0ffff01ff')

    def test_cpp_32980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffffff00h'), u'0x0ffffff00')

    def test_cpp_32990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffffff03h'), u'0x0ffffff03')

    def test_cpp_33000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0fffffff3h'), u'0x0fffffff3')

    def test_cpp_33010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffffffffh'), u'0x0ffffffff')

    def test_cpp_33020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffffh'), u'0x0ffff')

    def test_cpp_33030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0ffh'), u'0x0ff')

    def test_cpp_33040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0x0C'), u'0x0C')

    def test_cpp_33050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0x10'), u'0x10')

    def test_cpp_33060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'0x14'), u'0x14')

    def test_cpp_33070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1'), u'1')

    def test_cpp_33080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'10'), u'10')

    def test_cpp_33090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'10000h'), u'0x10000')

    def test_cpp_33100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1000h'), u'0x1000')

    def test_cpp_33110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'100h'), u'0x100')

    def test_cpp_33120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1024*10/16'), u'1024*10/16')

    def test_cpp_33130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1024*1024'), u'1024*1024')

    def test_cpp_33140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'10B'), u'0x2')

    def test_cpp_33150(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'10h'), u'0x10')

    def test_cpp_33160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'11'), u'11')

    def test_cpp_33170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'111'), u'111')

    def test_cpp_33180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'114h'), u'0x114')

    def test_cpp_33190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'11h'), u'0x11')

    def test_cpp_33200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12'), u'12')

    def test_cpp_33210(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12340004h'), u'0x12340004')

    def test_cpp_33220(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1234001Dh'), u'0x1234001D')

    def test_cpp_33230(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12341h'), u'0x12341')

    def test_cpp_33240(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12343h'), u'0x12343')

    def test_cpp_33250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12345'), u'12345')

    def test_cpp_33260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1234561Dh'), u'0x1234561D')

    def test_cpp_33270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12345678h'), u'0x12345678')

    def test_cpp_33280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12345h'), u'0x12345')

    def test_cpp_33290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12347F7Fh'), u'0x12347F7F')

    def test_cpp_33300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12347FFFh'), u'0x12347FFF')

    def test_cpp_33310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12348000h'), u'0x12348000')

    def test_cpp_33320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12348080h'), u'0x12348080')

    def test_cpp_33330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1234h'), u'0x1234')

    def test_cpp_33340(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'127Eh'), u'0x127E')

    def test_cpp_33350(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'12Ch'), u'0x12C')

    def test_cpp_33360(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'13'), u'13')

    def test_cpp_33370(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'132'), u'132')

    def test_cpp_33380(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'133'), u'133')

    def test_cpp_33390(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'13h'), u'0x13')

    def test_cpp_33400(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'14'), u'14')

    def test_cpp_33410(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'14*320'), u'14*320')

    def test_cpp_33420(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'14h'), u'0x14')

    def test_cpp_33430(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'15'), u'15')

    def test_cpp_33440(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1500'), u'1500')

    def test_cpp_33450(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'16'), u'16')

    def test_cpp_33460(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'17'), u'17')

    def test_cpp_33470(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'17h'), u'0x17')

    def test_cpp_33480(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'18'), u'18')

    def test_cpp_33490(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'18h'), u'0x18')

    def test_cpp_33500(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'19'), u'19')

    def test_cpp_33510(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'192'), u'192')

    def test_cpp_33520(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'193'), u'193')

    def test_cpp_33530(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1Ch'), u'0x1C')

    def test_cpp_33540(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1Eh'), u'0x1E')

    def test_cpp_33550(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FEh'), u'0x1FE')

    def test_cpp_33560(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FF7Fh'), u'0x1FF7F')

    def test_cpp_33570(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FF80h'), u'0x1FF80')

    def test_cpp_33580(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FF81h'), u'0x1FF81')

    def test_cpp_33590(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFEh'), u'0x1FFE')

    def test_cpp_33600(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFEh'), u'0x1FFFE')

    def test_cpp_33610(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFEh'), u'0x1FFFFE')

    def test_cpp_33620(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFFEh'), u'0x1FFFFFE')

    def test_cpp_33630(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFFFEh'), u'0x1FFFFFFE')

    def test_cpp_33640(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFFFFh'), u'0x1FFFFFFF')

    def test_cpp_33650(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFFFh'), u'0x1FFFFFF')

    def test_cpp_33660(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFFh'), u'0x1FFFFF')

    def test_cpp_33670(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFFh'), u'0x1FFFF')

    def test_cpp_33680(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFFh'), u'0x1FFF')

    def test_cpp_33690(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1FFh'), u'0x1FF')

    def test_cpp_33700(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'1Fh'), u'0x1F')

    def test_cpp_33710(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'2'), u'2')

    def test_cpp_33720(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'20'), u'20')

    def test_cpp_33730(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'20000h'), u'0x20000')

    def test_cpp_33740(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'20h'), u'0x20')

    def test_cpp_33750(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'21'), u'21')

    def test_cpp_33760(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'21AD3D34h'), u'0x21AD3D34')

    def test_cpp_33770(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'21h'), u'0x21')

    def test_cpp_33780(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'22'), u'22')

    def test_cpp_33790(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'23'), u'23')

    def test_cpp_33800(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'24'), u'24')

    def test_cpp_33810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'24h'), u'0x24')

    def test_cpp_33820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'25'), u'25')

    def test_cpp_33830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'255'), u'255')

    def test_cpp_33840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'256'), u'256')

    def test_cpp_33850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'256*3'), u'256*3')

    def test_cpp_33860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'256+3'), u'256+3')

    def test_cpp_33870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'256+3+65536'), u'256+3+65536')

    def test_cpp_33880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'26'), u'26')

    def test_cpp_33890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'27'), u'27')

    def test_cpp_33900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'28'), u'28')

    def test_cpp_33910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'29'), u'29')

    def test_cpp_33920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'2Ch'), u'0x2C')

    def test_cpp_33930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'2Dh'), u'0x2D')

    def test_cpp_33940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3'), u'3')

    def test_cpp_33950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3*4'), u'3*4')

    def test_cpp_33960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'30'), u'30')

    def test_cpp_33970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'303Bh'), u'0x303B')

    def test_cpp_33980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'30h'), u'0x30')

    def test_cpp_33990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'31'), u'31')

    def test_cpp_34000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'31h'), u'0x31')

    def test_cpp_34010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'32'), u'32')

    def test_cpp_34020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'320*200/4'), u'320*200/4')

    def test_cpp_34030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'32432434h'), u'0x32432434')

    def test_cpp_34040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'340128h'), u'0x340128')

    def test_cpp_34050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'35'), u'35')

    def test_cpp_34060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'37'), u'37')

    def test_cpp_34070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'39h'), u'0x39')

    def test_cpp_34080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3Ch'), u'0x3C')

    def test_cpp_34090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3DAh'), u'0x3DA')

    def test_cpp_34100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3Eh'), u'0x3E')

    def test_cpp_34110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FEh'), u'0x3FE')

    def test_cpp_34120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFEh'), u'0x3FFE')

    def test_cpp_34130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFEh'), u'0x3FFFE')

    def test_cpp_34140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFEh'), u'0x3FFFFE')

    def test_cpp_34150(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFFEh'), u'0x3FFFFFE')

    def test_cpp_34160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFFFEh'), u'0x3FFFFFFE')

    def test_cpp_34170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFFFFh'), u'0x3FFFFFFF')

    def test_cpp_34180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFFFh'), u'0x3FFFFFF')

    def test_cpp_34190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFFh'), u'0x3FFFFF')

    def test_cpp_34200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFFh'), u'0x3FFFF')

    def test_cpp_34210(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFFh'), u'0x3FFF')

    def test_cpp_34220(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3FFh'), u'0x3FF')

    def test_cpp_34230(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3Fh'), u'0x3F')

    def test_cpp_34240(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3c8h'), u'0x3c8')

    def test_cpp_34250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3c9h'), u'0x3c9')

    def test_cpp_34260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'3h'), u'0x3')

    def test_cpp_34270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'4'), u'4')

    def test_cpp_34280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'4+5*256'), u'4+5*256')

    def test_cpp_34290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'4000000'), u'4000000')

    def test_cpp_34300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'40h'), u'0x40')

    def test_cpp_34310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'43210123h'), u'0x43210123')

    def test_cpp_34320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'48h'), u'0x48')

    def test_cpp_34330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'49h'), u'0x49')

    def test_cpp_34340(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'4Ah'), u'0x4A')

    def test_cpp_34350(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'4Ch'), u'0x4C')

    def test_cpp_34360(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'4ch'), u'0x4c')

    def test_cpp_34370(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'5'), u'5')

    def test_cpp_34380(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'50'), u'50')

    def test_cpp_34390(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'501h'), u'0x501')

    def test_cpp_34400(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'511'), u'511')

    def test_cpp_34410(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'55'), u'55')

    def test_cpp_34420(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'56'), u'56')

    def test_cpp_34430(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'57'), u'57')

    def test_cpp_34440(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'6'), u'6')

    def test_cpp_34450(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'6*256+5'), u'6*256+5')

    def test_cpp_34460(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'60'), u'60')

    def test_cpp_34470(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'65324h'), u'0x65324')

    def test_cpp_34480(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'65423456h'), u'0x65423456')

    def test_cpp_34490(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'6789ABCDh'), u'0x6789ABCD')

    def test_cpp_34500(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7'), u'7')

    def test_cpp_34510(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7Eh'), u'0x7E')

    def test_cpp_34520(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FEh'), u'0x7FE')

    def test_cpp_34530(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFEh'), u'0x7FFE')

    def test_cpp_34540(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFEh'), u'0x7FFFE')

    def test_cpp_34550(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFEh'), u'0x7FFFFE')

    def test_cpp_34560(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFFEh'), u'0x7FFFFFE')

    def test_cpp_34570(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFFFEh'), u'0x7FFFFFFE')

    def test_cpp_34580(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFFFFh'), u'0x7FFFFFFF')

    def test_cpp_34590(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFFFh'), u'0x7FFFFFF')

    def test_cpp_34600(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFFh'), u'0x7FFFFF')

    def test_cpp_34610(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFFh'), u'0x7FFFF')

    def test_cpp_34620(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFFh'), u'0x7FFF')

    def test_cpp_34630(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7FFh'), u'0x7FF')

    def test_cpp_34640(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7Fh'), u'0x7F')

    def test_cpp_34650(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'8'), u'8')

    def test_cpp_34660(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'80000000h'), u'0x80000000')

    def test_cpp_34670(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'80000001h'), u'0x80000001')

    def test_cpp_34680(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'80008481h'), u'0x80008481')

    def test_cpp_34690(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'80008688h'), u'0x80008688')

    def test_cpp_34700(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'8000h'), u'0x8000')

    def test_cpp_34710(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'801h'), u'0x801')

    def test_cpp_34720(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'80h'), u'0x80')

    def test_cpp_34730(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'81234567h'), u'0x81234567')

    def test_cpp_34740(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'81238567h'), u'0x81238567')

    def test_cpp_34750(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'812FADAh'), u'0x812FADA')

    def test_cpp_34760(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'813F3421h'), u'0x813F3421')

    def test_cpp_34770(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'81h'), u'0x81')

    def test_cpp_34780(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'82345679h'), u'0x82345679')

    def test_cpp_34790(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'8234A6F8h'), u'0x8234A6F8')

    def test_cpp_34800(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'8345A1F2h'), u'0x8345A1F2')

    def test_cpp_34810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'8C5h'), u'0x8C5')

    def test_cpp_34820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'8D5h'), u'0x8D5')

    def test_cpp_34830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'9'), u'9')

    def test_cpp_34840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'9ABCDEFh'), u'0x9ABCDEF')

    def test_cpp_34850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'AL'), u'AL')

    def test_cpp_34860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'B'), u'B')

    def test_cpp_34870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'CC'), u'CC')

    def test_cpp_34880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'DDD'), u'DDD')

    def test_cpp_34890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'DX'), u'DX')

    def test_cpp_34900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'OFFSET ASCiI'), u'OFFSET ASCiI')

    def test_cpp_34910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'OFFSET AsCii'), u'OFFSET AsCii')

    def test_cpp_34920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'TWO'), u'TWO')

    def test_cpp_34930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[a+1]'), u'[a+1]')

    def test_cpp_34940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[a]'), u'[a]')

    def test_cpp_34950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[cs:table+ax]'), u'[cs:table+ax]')

    def test_cpp_34960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[doublequote+4]'), u'[doublequote+4]')

    '''
    def test_cpp_34970(self):
        self.assertEqual(convert_number_to_c(expr=u'[eax+4000h]'), u'[eax+0x4000]')

    def test_cpp_34980(self):
        self.assertEqual(convert_number_to_c(expr=u'[eax+40h]'), u'[eax+0x40]')

    def test_cpp_34990(self):
        self.assertEqual(convert_number_to_c(expr=u'[eax+ecx+40h]'), u'[eax+ecx+0x40]')
    '''

    def test_cpp_35000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[eax+ecx]'), u'[eax+ecx]')

    def test_cpp_35010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[eax]'), u'[eax]')

    def test_cpp_35020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+ecx_0]'), u'[ebp+ecx_0]')

    def test_cpp_35030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+ecx_vals]'), u'[ebp+ecx_vals]')

    def test_cpp_35040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+edx_0]'), u'[ebp+edx_0]')

    def test_cpp_35050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+i*4+ecx_vals]'), u'[ebp+i*4+ecx_vals]')

    def test_cpp_35060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+i+table]'), u'[ebp+i+table]')

    def test_cpp_35070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+iflags]'), u'[ebp+iflags]')

    def test_cpp_35080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+op0]'), u'[ebp+op0]')

    def test_cpp_35090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+op0h]'), u'[ebp+op0h]')

    def test_cpp_35100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+s0]'), u'[ebp+s0]')

    def test_cpp_35110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+s1]'), u'[ebp+s1]')

    def test_cpp_35120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+s2]'), u'[ebp+s2]')

    def test_cpp_35130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+table]'), u'[ebp+table]')

    def test_cpp_35140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+var_1C]'), u'[ebp+var_1C]')

    def test_cpp_35150(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+var_20]'), u'[ebp+var_20]')

    def test_cpp_35160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebp+var_4]'), u'[ebp+var_4]')

    '''
    def test_cpp_35170(self):
        self.assertEqual(convert_number_to_c(expr=u'[ebx+4000h]'), u'[ebx+0x4000]')

    def test_cpp_35180(self):
        self.assertEqual(convert_number_to_c(expr=u'[ebx+40h]'), u'[ebx+0x40]')

    def test_cpp_35190(self):
        self.assertEqual(convert_number_to_c(expr=u'[ebx+edx+4000h]'), u'[ebx+edx+0x4000]')
    '''

    def test_cpp_35200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebx+edx]'), u'[ebx+edx]')

    def test_cpp_35210(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'[ebx]'), u'[ebx]')

    '''
    def test_cpp_35220(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx+4000h]'), u'[ecx+0x4000]')

    def test_cpp_35230(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx+40h]'), u'[ecx+0x40]')

    def test_cpp_35240(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx+ecx*2+4000h]'), u'[ecx+ecx*2+0x4000]')

    def test_cpp_35250(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx+ecx*2-0Ah]'), u'[ecx+ecx*2-0x0A]')

    def test_cpp_35260(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx+ecx*2]'), u'[ecx+ecx*2]')

    def test_cpp_35270(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx+ecx]'), u'[ecx+ecx]')

    def test_cpp_35280(self):
        self.assertEqual(convert_number_to_c(expr=u'[ecx]'), u'[ecx]')

    def test_cpp_35290(self):
        self.assertEqual(convert_number_to_c(expr=u'[edi+1]'), u'[edi+1]')

    def test_cpp_35300(self):
        self.assertEqual(convert_number_to_c(expr=u'[edi+4000h]'), u'[edi+0x4000]')

    def test_cpp_35310(self):
        self.assertEqual(convert_number_to_c(expr=u'[edi+40h]'), u'[edi+0x40]')

    def test_cpp_35320(self):
        self.assertEqual(convert_number_to_c(expr=u'[edi+ecx]'), u'[edi+ecx]')

    def test_cpp_35330(self):
        self.assertEqual(convert_number_to_c(expr=u'[edi]'), u'[edi]')

    def test_cpp_35340(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx+4000h]'), u'[edx+0x4000]')

    def test_cpp_35350(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx+40h]'), u'[edx+0x40]')

    def test_cpp_35360(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx+ecx*4+4000h]'), u'[edx+ecx*4+0x4000]')

    def test_cpp_35370(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx+ecx*4-0Ah]'), u'[edx+ecx*4-0x0A]')

    def test_cpp_35380(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx+ecx*4]'), u'[edx+ecx*4]')

    def test_cpp_35390(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx+ecx]'), u'[edx+ecx]')

    def test_cpp_35400(self):
        self.assertEqual(convert_number_to_c(expr=u'[edx]'), u'[edx]')

    def test_cpp_35410(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi+4000h]'), u'[esi+0x4000]')

    def test_cpp_35420(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi+40h]'), u'[esi+0x40]')

    def test_cpp_35430(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi+ecx*8+4000h]'), u'[esi+ecx*8+0x4000]')

    def test_cpp_35440(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi+ecx*8-0Ah]'), u'[esi+ecx*8-0x0A]')

    def test_cpp_35450(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi+ecx*8]'), u'[esi+ecx*8]')

    def test_cpp_35460(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi+ecx]'), u'[esi+ecx]')

    def test_cpp_35470(self):
        self.assertEqual(convert_number_to_c(expr=u'[esi]'), u'[esi]')

    def test_cpp_35480(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+0Ch]'), u'[esp+0x0C]')

    def test_cpp_35490(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+10h]'), u'[esp+0x10]')

    def test_cpp_35500(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+14h]'), u'[esp+0x14]')

    def test_cpp_35510(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+18h]'), u'[esp+0x18]')

    def test_cpp_35520(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+1Ch]'), u'[esp+0x1C]')

    def test_cpp_35530(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+4]'), u'[esp+4]')

    def test_cpp_35540(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp+8]'), u'[esp+8]')

    def test_cpp_35550(self):
        self.assertEqual(convert_number_to_c(expr=u'[esp]'), u'[esp]')

    def test_cpp_35560(self):
        self.assertEqual(convert_number_to_c(expr=u'[g]'), u'[g]')

    def test_cpp_35570(self):
        self.assertEqual(convert_number_to_c(expr=u'[h2]'), u'[h2]')

    def test_cpp_35580(self):
        self.assertEqual(convert_number_to_c(expr=u'[i+1]'), u'[i+1]')

    def test_cpp_35590(self):
        self.assertEqual(convert_number_to_c(expr=u'[i+2]'), u'[i+2]')

    def test_cpp_35600(self):
        self.assertEqual(convert_number_to_c(expr=u'[i+3]'), u'[i+3]')

    def test_cpp_35610(self):
        self.assertEqual(convert_number_to_c(expr=u'[i+4]'), u'[i+4]')

    def test_cpp_35620(self):
        self.assertEqual(convert_number_to_c(expr=u'[i+56h]'), u'[i+0x56]')

    def test_cpp_35630(self):
        self.assertEqual(convert_number_to_c(expr=u'[i+5]'), u'[i+5]')

    def test_cpp_35640(self):
        self.assertEqual(convert_number_to_c(expr=u'[i-10h]'), u'[i-0x10]')

    def test_cpp_35650(self):
        self.assertEqual(convert_number_to_c(expr=u'[load_handle]'), u'[load_handle]')

    def test_cpp_35660(self):
        self.assertEqual(convert_number_to_c(expr=u'[var+3]'), u'[var+3]')

    def test_cpp_35670(self):
        self.assertEqual(convert_number_to_c(expr=u'[var+4]'), u'[var+4]')

    def test_cpp_35680(self):
        self.assertEqual(convert_number_to_c(expr=u'[var-1]'), u'[var-1]')

    def test_cpp_35690(self):
        self.assertEqual(convert_number_to_c(expr=u'[var0+5]'), u'[var0+5]')

    def test_cpp_35700(self):
        self.assertEqual(convert_number_to_c(expr=u'[var1+1]'), u'[var1+1]')

    def test_cpp_35710(self):
        self.assertEqual(convert_number_to_c(expr=u'[var1]'), u'[var1]')

    def test_cpp_35720(self):
        self.assertEqual(convert_number_to_c(expr=u'[var2+2]'), u'[var2+2]')

    def test_cpp_35730(self):
        self.assertEqual(convert_number_to_c(expr=u'[var2-1]'), u'[var2-1]')

    def test_cpp_35740(self):
        self.assertEqual(convert_number_to_c(expr=u'[var2]'), u'[var2]')

    def test_cpp_35750(self):
        self.assertEqual(convert_number_to_c(expr=u'[var3+3*4]'), u'[var3+3*4]')

    def test_cpp_35760(self):
        self.assertEqual(convert_number_to_c(expr=u'[var3+ebp]'), u'[var3+ebp]')

    def test_cpp_35770(self):
        self.assertEqual(convert_number_to_c(expr=u'[var3]'), u'[var3]')

    def test_cpp_35780(self):
        self.assertEqual(convert_number_to_c(expr=u'[var4+t]'), u'[var4+t]')

    def test_cpp_35790(self):
        self.assertEqual(convert_number_to_c(expr=u'[var4]'), u'[var4]')

    def test_cpp_35800(self):
        self.assertEqual(convert_number_to_c(expr=u'[var]'), u'[var]')
    '''

    def test_cpp_35810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ah'), u'ah')

    def test_cpp_35820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'al'), u'al')

    def test_cpp_35830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ax'), u'ax')

    def test_cpp_35840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'b'), u'b')

    def test_cpp_35850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'beginningdata'), u'beginningdata')

    def test_cpp_35860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'bh'), u'bh')

    def test_cpp_35870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'bl'), u'bl')

    def test_cpp_35880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'bp'), u'bp')

    def test_cpp_35890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'buffer'), u'buffer')

    def test_cpp_35900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'bx'), u'bx')

    def test_cpp_35910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [a]'), u'byte ptr [a]')

    def test_cpp_35920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [ebp+var_20]'), u'byte ptr [ebp+var_20]')

    def test_cpp_35930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [edi+1]'), u'byte ptr [edi+1]')

    def test_cpp_35940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [edi+7]'), u'byte ptr [edi+7]')

    def test_cpp_35950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [esi]'), u'byte ptr [esi]')

    def test_cpp_35960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [h2]'), u'byte ptr [h2]')

    def test_cpp_35970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [h]'), u'byte ptr [h]')

    def test_cpp_35980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [testOVerlap+1]'), u'byte ptr [testOVerlap+1]')

    def test_cpp_35990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [var1+1]'), u'byte ptr [var1+1]')

    def test_cpp_36000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr [var1+2]'), u'byte ptr [var1+2]')

    def test_cpp_36010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr dl'), u'byte ptr dl')

    def test_cpp_36020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr ds:[0]'), u'byte ptr ds:[0]')

    def test_cpp_36030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'byte ptr es:[0]'), u'byte ptr es:[0]')

    def test_cpp_36040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ch'), u'ch')

    def test_cpp_36050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'cl'), u'cl')

    def test_cpp_36060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'cx'), u'cx')

    def test_cpp_36070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'di'), u'di')

    def test_cpp_36080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dl'), u'dl')

    def test_cpp_36090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ds'), u'ds')

    def test_cpp_36100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ds:0[eax*2]'), u'ds:0[eax*2]')

    def test_cpp_36110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ds:0[ebx*4]'), u'ds:0[ebx*4]')

    def test_cpp_36120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ds:0[ecx*8]'), u'ds:0[ecx*8]')

    #def test_cpp_36130(self):
    #    self.assertEqual(convert_number_to_c(expr=u'ds:40h[eax*2]'), u'ds:0x40[eax*2]')

    #def test_cpp_36140(self):
    #    self.assertEqual(convert_number_to_c(expr=u'ds:40h[ebx*4]'), u'ds:0x40[ebx*4]')

    #def test_cpp_36150(self):
    #    self.assertEqual(convert_number_to_c(expr=u'ds:40h[ecx*8]'), u'ds:0x40[ecx*8]')

    def test_cpp_36160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ds:[edi]'), u'ds:[edi]')

    def test_cpp_36170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ds:byte_41411F[eax]'), u'ds:byte_41411F[eax]')

    def test_cpp_36180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr [ebp+var_20+4]'), u'dword ptr [ebp+var_20+4]')

    def test_cpp_36190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr [ebp+var_20]'), u'dword ptr [ebp+var_20]')

    def test_cpp_36200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr [ebx-4]'), u'dword ptr [ebx-4]')

    '''
    def test_cpp_36210(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+0Ch]'), u'dword ptr [esp+0x0C]')

    def test_cpp_36220(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+10h]'), u'dword ptr [esp+0x10]')

    def test_cpp_36230(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+14h]'), u'dword ptr [esp+0x14]')

    def test_cpp_36240(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+1Ch]'), u'dword ptr [esp+0x1C]')
    '''

    def test_cpp_36250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr [esp+4]'), u'dword ptr [esp+4]')

    def test_cpp_36260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr [esp+8]'), u'dword ptr [esp+8]')

    def test_cpp_36270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr [esp]'), u'dword ptr [esp]')

    def test_cpp_36280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr buffer'), u'dword ptr buffer')

    def test_cpp_36290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr es:[0]'), u'dword ptr es:[0]')

    def test_cpp_36300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr es:[20*320+160]'), u'dword ptr es:[20*320+160]')

    def test_cpp_36310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword ptr var4'), u'dword ptr var4')

    def test_cpp_36320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dword'), u'dword')

    def test_cpp_36330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'dx'), u'dx')

    def test_cpp_36340(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'eax'), u'eax')

    def test_cpp_36350(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'eax_0'), u'eax_0')

    def test_cpp_36360(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ebp'), u'ebp')

    def test_cpp_36370(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ebx'), u'ebx')

    def test_cpp_36380(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ecx'), u'ecx')

    def test_cpp_36390(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ecx_0'), u'ecx_0')

    def test_cpp_36400(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ecx_0_0'), u'ecx_0_0')

    def test_cpp_36410(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'edi'), u'edi')

    def test_cpp_36420(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'edi_0'), u'edi_0')

    def test_cpp_36430(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'edx'), u'edx')

    def test_cpp_36440(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'edx_0_0'), u'edx_0_0')

    def test_cpp_36450(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'eflags'), u'eflags')

    def test_cpp_36460(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'enddata'), u'enddata')

    def test_cpp_36470(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'es'), u'es')

    def test_cpp_36480(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'esi'), u'esi')

    def test_cpp_36490(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'esi_0'), u'esi_0')

    def test_cpp_36500(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'esp'), u'esp')

    def test_cpp_36510(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'f'), u'f')

    def test_cpp_36520(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'fileName'), u'fileName')

    def test_cpp_36530(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'flags'), u'flags')

    def test_cpp_36540(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'fs'), u'fs')

    def test_cpp_36550(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'i'), u'i')

    #def test_cpp_36560(self):
        # self.assertEqual(convert_number_to_c(expr=u'large ds:4000h'), u'large ds:0x4000')

    def test_cpp_36570(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset _msg'), u'offset _msg')

    def test_cpp_36580(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset _test_btc'), u'offset _test_btc')

    def test_cpp_36590(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000'), u'offset a0x4000')

    def test_cpp_36600(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000Eax'), u'offset a0x4000Eax')

    def test_cpp_36610(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000Ebx'), u'offset a0x4000Ebx')

    def test_cpp_36620(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000EbxEdx'), u'offset a0x4000EbxEdx')

    def test_cpp_36630(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000Ecx'), u'offset a0x4000Ecx')

    def test_cpp_36640(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000EcxEcx2'), u'offset a0x4000EcxEcx2')

    def test_cpp_36650(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000Edi'), u'offset a0x4000Edi')

    def test_cpp_36660(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000Edx'), u'offset a0x4000Edx')

    def test_cpp_36670(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000EdxEcx4'), u'offset a0x4000EdxEcx4')

    def test_cpp_36680(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000Esi'), u'offset a0x4000Esi')

    def test_cpp_36690(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x4000EsiEcx8'), u'offset a0x4000EsiEcx8')

    def test_cpp_36700(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Eax'), u'offset a0x40Eax')

    def test_cpp_36710(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Eax2'), u'offset a0x40Eax2')

    def test_cpp_36720(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40EaxEcx'), u'offset a0x40EaxEcx')

    def test_cpp_36730(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Ebx'), u'offset a0x40Ebx')

    def test_cpp_36740(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Ebx4'), u'offset a0x40Ebx4')

    def test_cpp_36750(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Ecx'), u'offset a0x40Ecx')

    def test_cpp_36760(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Ecx8'), u'offset a0x40Ecx8')

    def test_cpp_36770(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Edi'), u'offset a0x40Edi')

    def test_cpp_36780(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Edx'), u'offset a0x40Edx')

    def test_cpp_36790(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a0x40Esi'), u'offset a0x40Esi')

    def test_cpp_36800(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10EcxEcx2'), u'offset a10EcxEcx2')

    def test_cpp_36810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10EdxEcx4'), u'offset a10EdxEcx4')

    def test_cpp_36820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10EsiEcx8'), u'offset a10EsiEcx8')

    def test_cpp_36830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxB08lx'), u'offset a10sA08lxB08lx')

    def test_cpp_36840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxB08lxC'), u'offset a10sA08lxB08lxC')

    def test_cpp_36850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxB08lxR'), u'offset a10sA08lxB08lxR')

    def test_cpp_36860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxB08lxR_0'), u'offset a10sA08lxB08lxR_0')

    def test_cpp_36870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxR08lx'), u'offset a10sA08lxR08lx')

    def test_cpp_36880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxR08lx0'), u'offset a10sA08lxR08lx0')

    def test_cpp_36890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxR08lxC'), u'offset a10sA08lxR08lxC')

    def test_cpp_36900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxR08lxL'), u'offset a10sA08lxR08lxL')

    def test_cpp_36910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08lxR08lx_0'), u'offset a10sA08lxR08lx_0')

    def test_cpp_36920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sA08xR08xCci'), u'offset a10sA08xR08xCci')

    def test_cpp_36930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sAh08lxAl08l'), u'offset a10sAh08lxAl08l')

    def test_cpp_36940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sD'), u'offset a10sD')

    def test_cpp_36950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sEax08lxA08l'), u'offset a10sEax08lxA08l')

    def test_cpp_36960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sEcx08lxZfLd'), u'offset a10sEcx08lxZfLd')

    def test_cpp_36970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset a10sEsi08lxEdi0'), u'offset a10sEsi08lxEdi0')

    def test_cpp_36980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAaa'), u'offset aAaa')

    def test_cpp_36990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAad'), u'offset aAad')

    def test_cpp_37000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAam'), u'offset aAam')

    def test_cpp_37010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAas'), u'offset aAas')

    def test_cpp_37020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAdcb'), u'offset aAdcb')

    def test_cpp_37030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAdcl'), u'offset aAdcl')

    def test_cpp_37040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAdcw'), u'offset aAdcw')

    def test_cpp_37050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAddb'), u'offset aAddb')

    def test_cpp_37060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAddl'), u'offset aAddl')

    def test_cpp_37070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAddw'), u'offset aAddw')

    def test_cpp_37080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAndb'), u'offset aAndb')

    def test_cpp_37090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAndl'), u'offset aAndl')

    def test_cpp_37100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aAndw'), u'offset aAndw')

    def test_cpp_37110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBsfl'), u'offset aBsfl')

    def test_cpp_37120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBsfw'), u'offset aBsfw')

    def test_cpp_37130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBsrl'), u'offset aBsrl')

    def test_cpp_37140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBsrw'), u'offset aBsrw')

    def test_cpp_37150(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBswapl'), u'offset aBswapl')

    def test_cpp_37160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtcl'), u'offset aBtcl')

    def test_cpp_37170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtcw'), u'offset aBtcw')

    def test_cpp_37180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtl'), u'offset aBtl')

    def test_cpp_37190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtrl'), u'offset aBtrl')

    def test_cpp_37200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtrw'), u'offset aBtrw')

    def test_cpp_37210(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtsl'), u'offset aBtsl')

    def test_cpp_37220(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtsw'), u'offset aBtsw')

    def test_cpp_37230(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aBtw'), u'offset aBtw')

    def test_cpp_37240(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCbw'), u'offset aCbw')

    def test_cpp_37250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCdq'), u'offset aCdq')

    def test_cpp_37260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpb'), u'offset aCmpb')

    def test_cpp_37270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpl'), u'offset aCmpl')

    def test_cpp_37280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpsb'), u'offset aCmpsb')

    def test_cpp_37290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpsl'), u'offset aCmpsl')

    def test_cpp_37300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpsw'), u'offset aCmpsw')

    def test_cpp_37310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpw'), u'offset aCmpw')

    def test_cpp_37320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpxchg8bEax08'), u'offset aCmpxchg8bEax08')

    def test_cpp_37330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpxchgb'), u'offset aCmpxchgb')

    def test_cpp_37340(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpxchgl'), u'offset aCmpxchgl')

    def test_cpp_37350(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCmpxchgw'), u'offset aCmpxchgw')

    def test_cpp_37360(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCwd'), u'offset aCwd')

    def test_cpp_37370(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aCwde'), u'offset aCwde')

    def test_cpp_37380(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDaa'), u'offset aDaa')

    def test_cpp_37390(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDas'), u'offset aDas')

    def test_cpp_37400(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDecb'), u'offset aDecb')

    def test_cpp_37410(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDecl'), u'offset aDecl')

    def test_cpp_37420(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDecw'), u'offset aDecw')

    def test_cpp_37430(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDivb'), u'offset aDivb')

    def test_cpp_37440(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDivl'), u'offset aDivl')

    def test_cpp_37450(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aDivw'), u'offset aDivw')

    def test_cpp_37460(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEax'), u'offset aEax')

    def test_cpp_37470(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEax2'), u'offset aEax2')

    def test_cpp_37480(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEaxEcx'), u'offset aEaxEcx')

    def test_cpp_37490(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEbx'), u'offset aEbx')

    def test_cpp_37500(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEbx4'), u'offset aEbx4')

    def test_cpp_37510(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEbxEdx'), u'offset aEbxEdx')

    def test_cpp_37520(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEcx'), u'offset aEcx')

    def test_cpp_37530(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEcx8'), u'offset aEcx8')

    def test_cpp_37540(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEcxEcx'), u'offset aEcxEcx')

    def test_cpp_37550(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEcxEcx2'), u'offset aEcxEcx2')

    def test_cpp_37560(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEdi'), u'offset aEdi')

    def test_cpp_37570(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEdiEcx'), u'offset aEdiEcx')

    def test_cpp_37580(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEdx'), u'offset aEdx')

    def test_cpp_37590(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEdxEcx'), u'offset aEdxEcx')

    def test_cpp_37600(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEdxEcx4'), u'offset aEdxEcx4')

    def test_cpp_37610(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEsi'), u'offset aEsi')

    def test_cpp_37620(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEsiEcx'), u'offset aEsiEcx')

    def test_cpp_37630(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aEsiEcx8'), u'offset aEsiEcx8')

    def test_cpp_37640(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aIdivb'), u'offset aIdivb')

    def test_cpp_37650(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aIdivl'), u'offset aIdivl')

    def test_cpp_37660(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aIdivw'), u'offset aIdivw')

    def test_cpp_37670(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aImulb'), u'offset aImulb')

    def test_cpp_37680(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aImull'), u'offset aImull')

    def test_cpp_37690(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aImullIm'), u'offset aImullIm')

    def test_cpp_37700(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aImulw'), u'offset aImulw')

    def test_cpp_37710(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aImulwIm'), u'offset aImulwIm')

    def test_cpp_37720(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aIncb'), u'offset aIncb')

    def test_cpp_37730(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aIncl'), u'offset aIncl')

    def test_cpp_37740(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aIncw'), u'offset aIncw')

    def test_cpp_37750(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJa'), u'offset aJa')

    def test_cpp_37760(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJae'), u'offset aJae')

    def test_cpp_37770(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJb'), u'offset aJb')

    def test_cpp_37780(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJbe'), u'offset aJbe')

    def test_cpp_37790(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJcxz'), u'offset aJcxz')

    def test_cpp_37800(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJe'), u'offset aJe')

    def test_cpp_37810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJecxz'), u'offset aJecxz')

    def test_cpp_37820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJg'), u'offset aJg')

    def test_cpp_37830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJge'), u'offset aJge')

    def test_cpp_37840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJl'), u'offset aJl')

    def test_cpp_37850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJle'), u'offset aJle')

    def test_cpp_37860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJne'), u'offset aJne')

    def test_cpp_37870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJns'), u'offset aJns')

    def test_cpp_37880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aJs'), u'offset aJs')

    def test_cpp_37890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLeaS08lx'), u'offset aLeaS08lx')

    def test_cpp_37900(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLodsb'), u'offset aLodsb')

    def test_cpp_37910(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLodsl'), u'offset aLodsl')

    def test_cpp_37920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLodsw'), u'offset aLodsw')

    def test_cpp_37930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLoopl'), u'offset aLoopl')

    def test_cpp_37940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLoopnzl'), u'offset aLoopnzl')

    def test_cpp_37950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aLoopzl'), u'offset aLoopzl')

    def test_cpp_37960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aMovsb'), u'offset aMovsb')

    def test_cpp_37970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aMovsl'), u'offset aMovsl')

    def test_cpp_37980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aMovsw'), u'offset aMovsw')

    def test_cpp_37990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aMulb'), u'offset aMulb')

    def test_cpp_38000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aMull'), u'offset aMull')

    def test_cpp_38010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aMulw'), u'offset aMulw')

    def test_cpp_38020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aNegb'), u'offset aNegb')

    def test_cpp_38030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aNegl'), u'offset aNegl')

    def test_cpp_38040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aNegw'), u'offset aNegw')

    def test_cpp_38050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aNotb'), u'offset aNotb')

    def test_cpp_38060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aNotl'), u'offset aNotl')

    def test_cpp_38070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aNotw'), u'offset aNotw')

    def test_cpp_38080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aOrb'), u'offset aOrb')

    def test_cpp_38090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aOrl'), u'offset aOrl')

    def test_cpp_38100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aOrw'), u'offset aOrw')

    def test_cpp_38110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aPopcntA08lxR08'), u'offset aPopcntA08lxR08')

    def test_cpp_38120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aPoplEsp08lx'), u'offset aPoplEsp08lx')

    def test_cpp_38130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aPopwEsp08lx'), u'offset aPopwEsp08lx')

    def test_cpp_38140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRclb'), u'offset aRclb')

    def test_cpp_38150(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRcll'), u'offset aRcll')

    def test_cpp_38160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRclw'), u'offset aRclw')

    def test_cpp_38170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRcrb'), u'offset aRcrb')

    def test_cpp_38180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRcrl'), u'offset aRcrl')

    def test_cpp_38190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRcrw'), u'offset aRcrw')

    def test_cpp_38200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepLodsb'), u'offset aRepLodsb')

    def test_cpp_38210(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepLodsl'), u'offset aRepLodsl')

    def test_cpp_38220(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepLodsw'), u'offset aRepLodsw')

    def test_cpp_38230(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepMovsb'), u'offset aRepMovsb')

    def test_cpp_38240(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepMovsl'), u'offset aRepMovsl')

    def test_cpp_38250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepMovsw'), u'offset aRepMovsw')

    def test_cpp_38260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepStosb'), u'offset aRepStosb')

    def test_cpp_38270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepStosl'), u'offset aRepStosl')

    def test_cpp_38280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepStosw'), u'offset aRepStosw')

    def test_cpp_38290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepnzCmpsb'), u'offset aRepnzCmpsb')

    def test_cpp_38300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepnzCmpsl'), u'offset aRepnzCmpsl')

    def test_cpp_38310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepnzCmpsw'), u'offset aRepnzCmpsw')

    def test_cpp_38320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepnzScasb'), u'offset aRepnzScasb')

    def test_cpp_38330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepnzScasl'), u'offset aRepnzScasl')

    def test_cpp_38340(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepnzScasw'), u'offset aRepnzScasw')

    def test_cpp_38350(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepzCmpsb'), u'offset aRepzCmpsb')

    def test_cpp_38360(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepzCmpsl'), u'offset aRepzCmpsl')

    def test_cpp_38370(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepzCmpsw'), u'offset aRepzCmpsw')

    def test_cpp_38380(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepzScasb'), u'offset aRepzScasb')

    def test_cpp_38390(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepzScasl'), u'offset aRepzScasl')

    def test_cpp_38400(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRepzScasw'), u'offset aRepzScasw')

    def test_cpp_38410(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRolb'), u'offset aRolb')

    def test_cpp_38420(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRoll'), u'offset aRoll')

    def test_cpp_38430(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRolw'), u'offset aRolw')

    def test_cpp_38440(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRorb'), u'offset aRorb')

    def test_cpp_38450(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRorl'), u'offset aRorl')

    def test_cpp_38460(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aRorw'), u'offset aRorw')

    def test_cpp_38470(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSarb'), u'offset aSarb')

    def test_cpp_38480(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSarl'), u'offset aSarl')

    def test_cpp_38490(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSarw'), u'offset aSarw')

    def test_cpp_38500(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSbbb'), u'offset aSbbb')

    def test_cpp_38510(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSbbl'), u'offset aSbbl')

    def test_cpp_38520(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSbbw'), u'offset aSbbw')

    def test_cpp_38530(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aScasb'), u'offset aScasb')

    def test_cpp_38540(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aScasl'), u'offset aScasl')

    def test_cpp_38550(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aScasw'), u'offset aScasw')

    def test_cpp_38560(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSetb'), u'offset aSetb')

    def test_cpp_38570(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSete'), u'offset aSete')

    def test_cpp_38580(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSetne'), u'offset aSetne')

    def test_cpp_38590(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShlb'), u'offset aShlb')

    def test_cpp_38600(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShldl'), u'offset aShldl')

    def test_cpp_38610(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShldw'), u'offset aShldw')

    def test_cpp_38620(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShll'), u'offset aShll')

    def test_cpp_38630(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShlw'), u'offset aShlw')

    def test_cpp_38640(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShrb'), u'offset aShrb')

    def test_cpp_38650(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShrdl'), u'offset aShrdl')

    def test_cpp_38660(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShrdw'), u'offset aShrdw')

    def test_cpp_38670(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShrl'), u'offset aShrl')

    def test_cpp_38680(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aShrw'), u'offset aShrw')

    def test_cpp_38690(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aStosb'), u'offset aStosb')

    def test_cpp_38700(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aStosl'), u'offset aStosl')

    def test_cpp_38710(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aStosw'), u'offset aStosw')

    def test_cpp_38720(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSubb'), u'offset aSubb')

    def test_cpp_38730(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSubl'), u'offset aSubl')

    def test_cpp_38740(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aSubw'), u'offset aSubw')

    def test_cpp_38750(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXaddb'), u'offset aXaddb')

    def test_cpp_38760(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXaddl'), u'offset aXaddl')

    def test_cpp_38770(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXaddlSameRes08'), u'offset aXaddlSameRes08')

    def test_cpp_38780(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXaddw'), u'offset aXaddw')

    def test_cpp_38790(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXchgb'), u'offset aXchgb')

    def test_cpp_38800(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXchgl'), u'offset aXchgl')

    def test_cpp_38810(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXchgw'), u'offset aXchgw')

    def test_cpp_38820(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXlatEax08lx'), u'offset aXlatEax08lx')

    def test_cpp_38830(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXorb'), u'offset aXorb')

    def test_cpp_38840(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXorl'), u'offset aXorl')

    def test_cpp_38850(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset aXorw'), u'offset aXorw')

    def test_cpp_38860(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset pal_jeu'), u'offset pal_jeu')

    def test_cpp_38870(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset str1'), u'offset str1')

    def test_cpp_38880(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset str2'), u'offset str2')

    def test_cpp_38890(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset str3'), u'offset str3')

    #def test_cpp_38900(self):
        # self.assertEqual(convert_number_to_c(expr=u'offset str_buffer+800h'), u'offset str_buffer+0x800')

    #def test_cpp_38910(self):
        # self.assertEqual(convert_number_to_c(expr=u'offset str_buffer+810h'), u'offset str_buffer+0x810')

    def test_cpp_38920(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset testOVerlap'), u'offset testOVerlap')

    def test_cpp_38930(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset unk_40E008'), u'offset unk_40E008')

    def test_cpp_38940(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset unk_40F064'), u'offset unk_40F064')

    def test_cpp_38950(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var1'), u'offset var1')

    def test_cpp_38960(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var1+1'), u'offset var1+1')

    def test_cpp_38970(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var2'), u'offset var2')

    def test_cpp_38980(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var3'), u'offset var3')

    def test_cpp_38990(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var3+4'), u'offset var3+4')

    def test_cpp_39000(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var4'), u'offset var4')

    def test_cpp_39010(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var4+1'), u'offset var4+1')

    def test_cpp_39020(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'offset var4+4'), u'offset var4+4')

    def test_cpp_39030(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'op0'), u'op0')

    def test_cpp_39040(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'op1'), u'op1')

    def test_cpp_39050(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'printf'), u'printf')

    def test_cpp_39060(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'ptr'), u'ptr')

    def test_cpp_39070(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'r'), u'r')

    def test_cpp_39080(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'res'), u'res')

    def test_cpp_39090(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'resh'), u'resh')

    def test_cpp_39100(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'resz'), u'resz')

    def test_cpp_39110(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'rh'), u'rh')

    def test_cpp_39120(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u's0_0'), u's0_0')

    def test_cpp_39130(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u's1_0'), u's1_0')

    def test_cpp_39140(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'si'), u'si')

    def test_cpp_39150(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'small'), u'small')

    def test_cpp_39160(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u't'), u't')

    def test_cpp_39170(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'taille_moire'), u'taille_moire')

    def test_cpp_39180(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'teST2'), u'teST2')

    def test_cpp_39190(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'testOVerlap'), u'testOVerlap')

    def test_cpp_39200(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var1'), u'var1')

    def test_cpp_39210(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var1[1]'), u'var1[1]')

    def test_cpp_39220(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var1[bx+si]'), u'var1[bx+si]')

    def test_cpp_39230(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var1[bx]'), u'var1[bx]')

    def test_cpp_39240(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var2'), u'var2')

    def test_cpp_39250(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var3+3*4'), u'var3+3*4')

    def test_cpp_39260(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var3+ebp'), u'var3+ebp')

    def test_cpp_39270(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'var5'), u'var5')

    def test_cpp_39280(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'word ptr [d]'), u'word ptr [d]')

    def test_cpp_39290(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'word ptr [e]'), u'word ptr [e]')

    def test_cpp_39300(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'word ptr [ebp+var_20]'), u'word ptr [ebp+var_20]')

    def test_cpp_39310(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'word ptr [var5+2]'), u'word ptr [var5+2]')

    def test_cpp_39320(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'word ptr var5'), u'word ptr var5')

    def test_cpp_39330(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'word'), u'word')

    def test_cpp_36335(self):
        self.assertEqual(self.cpp.convert_asm_number_into_c(expr=u'7o'), u'07')

    def test_cpp_39340(self):
        self.assertEqual(self.cpp.cpp_mangle_label(name='loc_40458F'), 'loc_40458f')

    def test_cpp_39350(self):
        self.assertEqual(self.cpp.cpp_mangle_label(name=u'_start'), u'_start')

    def test_cpp_39360(self):
        self.assertEqual(self.cpp.cpp_mangle_label(name=u'_st$art$'), u'_st_tmpart_tmp')


if __name__ == "__main__":
    unittest.main()
