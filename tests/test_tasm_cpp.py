import unittest

from masm2c.cpp import Cpp
from masm2c.parser import Parser

# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).

class CppTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.cpp = Cpp(self.parser)

    def test_args_20010(self):
        assert self.parser.parse_arg('[a+1]', def_size=1, destination=False) == '*(raddr(ds,a+1))'

    def test_args_20020(self):
        assert self.parser.parse_arg('ds:40h[eax*2]', def_size=0, destination=False) == '*(raddr(ds,0x40+eax*2))'

    def test_args_20030(self):
        assert self.parser.parse_arg("'Z' - 'A' +1", def_size=1, destination=False) == "'Z'-'A'+1"

    def test_args_20040(self):
        assert self.parser.parse_arg("'a'", def_size=1, destination=False) == "'a'"

    def test_args_20050(self):
        assert self.parser.parse_arg('(1024*10/16)+5', def_size=2, destination=False) == '(1024*10/16)+5'

    def test_args_20060(self):
        assert self.parser.parse_arg('(1024*10/16)-1', def_size=2, destination=False) == '(1024*10/16)-1'

    #def test_args_20070(self):

    def test_args_20080(self):
        assert self.parser.parse_arg('-40h', def_size=0, destination=False) == '-0x40'

    def test_args_20090(self):
        assert self.parser.parse_arg('+40h', def_size=0, destination=False) == '+0x40'

    #def test_args_20100(self):

    #def test_args_20110(self):

    #def test_args_20120(self):

    #def test_args_20130(self):

    #def test_args_20140(self):

    #def test_args_20150(self):

    #def test_args_20160(self):

    #def test_args_20170(self):

    #def test_args_20180(self):

    #def test_args_20190(self):

    #def test_args_20200(self):

    #def test_args_20210(self):

    #def test_args_20220(self):

    #def test_args_20230(self):

    #def test_args_20240(self):

    #def test_args_20250(self):

    #def test_args_20260(self):

    #def test_args_20270(self):

    #def test_args_20280(self):

    #def test_args_20290(self):

    #def test_args_20300(self):

    #def test_args_20310(self):

    #def test_args_20320(self):

    #def test_args_20330(self):

    #def test_args_20340(self):

    #def test_args_20350(self):

    #def test_args_20360(self):

    def test_args_20370(self):
        assert self.parser.parse_arg('0', def_size=0, destination=False) == '0'

    def test_args_20380(self):
        assert self.parser.parse_arg('0', def_size=1, destination=False) == '0'

    def test_args_20390(self):
        assert self.parser.parse_arg('0002h', def_size=1, destination=False) == '0x0002'

    def test_args_20400(self):
        assert self.parser.parse_arg('0007', def_size=1, destination=False) == '0007'

    def test_args_20410(self):
        assert self.parser.parse_arg('000f3h', def_size=1, destination=False) == '0x000f3'

    def test_args_20420(self):
        assert self.parser.parse_arg('000ff00ffh', def_size=4, destination=False) == '0x000ff00ff'

    def test_args_20430(self):
        assert self.parser.parse_arg('001111111B', def_size=1, destination=False) == '0x7f'

    def test_args_20440(self):
        assert self.parser.parse_arg('00fffh', def_size=2, destination=False) == '0x00fff'

    def test_args_20450(self):
        assert self.parser.parse_arg('00h', def_size=1, destination=False) == '0x00'

    def test_args_20460(self):
        assert self.parser.parse_arg('0100b', def_size=4, destination=False) == '0x4'

    def test_args_20470(self):
        assert self.parser.parse_arg('01010101010101010b', def_size=2, destination=False) == '0xaaaa'

    def test_args_20480(self):
        assert self.parser.parse_arg('0101010101010101b', def_size=4, destination=False) == '0x5555'

    def test_args_20490(self):
        assert self.parser.parse_arg('0101b', def_size=4, destination=False) == '0x5'

    def test_args_20500(self):
        assert self.parser.parse_arg('010B', def_size=1, destination=False) == '0x2'

    def test_args_20510(self):
        assert self.parser.parse_arg('010B', def_size=4, destination=False) == '0x2'

    def test_args_20520(self):
        assert self.parser.parse_arg('011111100B', def_size=1, destination=False) == '0xfc'

    def test_args_20530(self):
        assert self.parser.parse_arg('011111111111111111111111111111111b', def_size=4, destination=False) == '0xffffffff'

    def test_args_20540(self):
        assert self.parser.parse_arg('01111111111111111b', def_size=2, destination=False) == '0xffff'

    def test_args_20550(self):
        assert self.parser.parse_arg('011111111B', def_size=1, destination=False) == '0xff'

    def test_args_20560(self):
        assert self.parser.parse_arg('012345678h', def_size=4, destination=False) == '0x012345678'

    def test_args_20570(self):
        assert self.parser.parse_arg('01B', def_size=4, destination=False) == '0x1'

    def test_args_20580(self):
        assert self.parser.parse_arg('01h', def_size=1, destination=False) == '0x01'

    def test_args_20590(self):
        assert self.parser.parse_arg('02h', def_size=1, destination=False) == '0x02'

    def test_args_20600(self):
        assert self.parser.parse_arg('03dh', def_size=1, destination=False) == '0x03d'

    def test_args_20610(self):
        assert self.parser.parse_arg('03eh', def_size=1, destination=False) == '0x03e'

    def test_args_20620(self):
        assert self.parser.parse_arg('03fh', def_size=1, destination=False) == '0x03f'

    def test_args_20630(self):
        assert self.parser.parse_arg('042h', def_size=1, destination=False) == '0x042'

    def test_args_20640(self):
        assert self.parser.parse_arg('077123456h', def_size=4, destination=False) == '0x077123456'

    def test_args_20650(self):
        assert self.parser.parse_arg('077aaFF00h', def_size=4, destination=False) == '0x077aaFF00'

    def test_args_20660(self):
        assert self.parser.parse_arg('08h', def_size=1, destination=False) == '0x08'

    def test_args_20670(self):
        assert self.parser.parse_arg('0B', def_size=1, destination=False) == '0x0'

    def test_args_20680(self):
        assert self.parser.parse_arg('0BC6058h', def_size=0, destination=False) == '0x0BC6058'

    def test_args_20690(self):
        assert self.parser.parse_arg('0D5h', def_size=1, destination=False) == '0x0D5'

    def test_args_20700(self):
        assert self.parser.parse_arg('0Eh', def_size=1, destination=False) == '0x0E'

    def test_args_20710(self):
        assert self.parser.parse_arg('0F7h', def_size=1, destination=False) == '0x0F7'

    def test_args_20720(self):
        assert self.parser.parse_arg('0FBCA7654h', def_size=4, destination=False) == '0x0FBCA7654'

    def test_args_20730(self):
        assert self.parser.parse_arg('0FBCA7h', def_size=4, destination=False) == '0x0FBCA7'

    def test_args_20740(self):
        assert self.parser.parse_arg('0FEh', def_size=1, destination=False) == '0x0FE'

    def test_args_20750(self):
        assert self.parser.parse_arg('0FFEh', def_size=2, destination=False) == '0x0FFE'

    def test_args_20760(self):
        assert self.parser.parse_arg('0FFFC70F9h', def_size=4, destination=False) == '0x0FFFC70F9'

    def test_args_20770(self):
        assert self.parser.parse_arg('0FFFE0080h', def_size=4, destination=False) == '0x0FFFE0080'

    def test_args_20780(self):
        assert self.parser.parse_arg('0FFFEDCBFh', def_size=4, destination=False) == '0x0FFFEDCBF'

    def test_args_20790(self):
        assert self.parser.parse_arg('0FFFEFDFCh', def_size=4, destination=False) == '0x0FFFEFDFC'

    def test_args_20800(self):
        assert self.parser.parse_arg('0FFFEh', def_size=2, destination=False) == '0x0FFFE'

    def test_args_20810(self):
        assert self.parser.parse_arg('0FFFF7FFFh', def_size=4, destination=False) == '0x0FFFF7FFF'

    def test_args_20820(self):
        assert self.parser.parse_arg('0FFFFA549h', def_size=4, destination=False) == '0x0FFFFA549'

    def test_args_20830(self):
        assert self.parser.parse_arg('0FFFFEh', def_size=4, destination=False) == '0x0FFFFE'

    def test_args_20840(self):
        assert self.parser.parse_arg('0FFFFFED4h', def_size=4, destination=False) == '0x0FFFFFED4'

    def test_args_20850(self):
        assert self.parser.parse_arg('0FFFFFEh', def_size=4, destination=False) == '0x0FFFFFE'

    def test_args_20860(self):
        assert self.parser.parse_arg('0FFFFFFD3h', def_size=4, destination=False) == '0x0FFFFFFD3'

    def test_args_20870(self):
        assert self.parser.parse_arg('0FFFFFFECh', def_size=4, destination=False) == '0x0FFFFFFEC'

    def test_args_20880(self):
        assert self.parser.parse_arg('0FFFFFFEh', def_size=4, destination=False) == '0x0FFFFFFE'

    def test_args_20890(self):
        assert self.parser.parse_arg('0FFFFFFF0h', def_size=4, destination=False) == '0x0FFFFFFF0'

    def test_args_20900(self):
        assert self.parser.parse_arg('0FFFFFFF7h', def_size=4, destination=False) == '0x0FFFFFFF7'

    def test_args_20910(self):
        assert self.parser.parse_arg('0FFFFFFFAh', def_size=4, destination=False) == '0x0FFFFFFFA'

    def test_args_20920(self):
        assert self.parser.parse_arg('0FFFFFFFBh', def_size=4, destination=False) == '0x0FFFFFFFB'

    def test_args_20930(self):
        assert self.parser.parse_arg('0FFFFFFFCh', def_size=4, destination=False) == '0x0FFFFFFFC'

    def test_args_20940(self):
        assert self.parser.parse_arg('0FFFFFFFDh', def_size=4, destination=False) == '0x0FFFFFFFD'

    def test_args_20950(self):
        assert self.parser.parse_arg('0FFFFFFFEh', def_size=4, destination=False) == '0x0FFFFFFFE'

    def test_args_20960(self):
        assert self.parser.parse_arg('0FFFFFFFFh', def_size=4, destination=False) == '0x0FFFFFFFF'

    def test_args_20970(self):
        assert self.parser.parse_arg('0FFFFFFFh', def_size=4, destination=False) == '0x0FFFFFFF'

    def test_args_20980(self):
        assert self.parser.parse_arg('0FFFFFFh', def_size=4, destination=False) == '0x0FFFFFF'

    def test_args_20990(self):
        assert self.parser.parse_arg('0FFFFFh', def_size=4, destination=False) == '0x0FFFFF'

    def test_args_21000(self):
        assert self.parser.parse_arg('0FFFFh', def_size=2, destination=False) == '0x0FFFF'

    def test_args_21010(self):
        assert self.parser.parse_arg('0FFFh', def_size=2, destination=False) == '0x0FFF'

    def test_args_21020(self):
        assert self.parser.parse_arg('0FFh', def_size=1, destination=False) == '0x0FF'

    def test_args_21030(self):
        assert self.parser.parse_arg('0Fh', def_size=1, destination=False) == '0x0F'

    def test_args_21040(self):
        assert self.parser.parse_arg('0a0000h', def_size=4, destination=False) == '0x0a0000'

    def test_args_21050(self):
        assert self.parser.parse_arg('0a000h', def_size=2, destination=False) == '0x0a000'

    def test_args_21060(self):
        assert self.parser.parse_arg('0aabbccddh', def_size=4, destination=False) == '0x0aabbccdd'

    def test_args_21070(self):
        assert self.parser.parse_arg('0abcdef77h', def_size=4, destination=False) == '0x0abcdef77'

    def test_args_21080(self):
        assert self.parser.parse_arg('0af222h', def_size=4, destination=False) == '0x0af222'

    def test_args_21090(self):
        assert self.parser.parse_arg('0cch', def_size=1, destination=False) == '0x0cc'

    def test_args_21100(self):
        assert self.parser.parse_arg('0ddh', def_size=1, destination=False) == '0x0dd'

    def test_args_21110(self):
        assert self.parser.parse_arg('0df01h', def_size=2, destination=False) == '0x0df01'

    def test_args_21120(self):
        assert self.parser.parse_arg('0dff1h', def_size=2, destination=False) == '0x0dff1'

    def test_args_21130(self):
        assert self.parser.parse_arg('0f0ffh', def_size=2, destination=False) == '0x0f0ff'

    def test_args_21140(self):
        assert self.parser.parse_arg('0f0h', def_size=1, destination=False) == '0x0f0'

    def test_args_21150(self):
        assert self.parser.parse_arg('0f222h', def_size=2, destination=False) == '0x0f222'

    def test_args_21160(self):
        assert self.parser.parse_arg('0ffff0003h', def_size=4, destination=False) == '0x0ffff0003'

    def test_args_21170(self):
        assert self.parser.parse_arg('0ffff00f3h', def_size=4, destination=False) == '0x0ffff00f3'

    def test_args_21180(self):
        assert self.parser.parse_arg('0ffff01ffh', def_size=4, destination=False) == '0x0ffff01ff'

    def test_args_21190(self):
        assert self.parser.parse_arg('0ffffff00h', def_size=4, destination=False) == '0x0ffffff00'

    def test_args_21200(self):
        assert self.parser.parse_arg('0ffffff03h', def_size=4, destination=False) == '0x0ffffff03'

    def test_args_21210(self):
        assert self.parser.parse_arg('0fffffff3h', def_size=4, destination=False) == '0x0fffffff3'

    def test_args_21220(self):
        assert self.parser.parse_arg('0ffffffffh', def_size=4, destination=False) == '0x0ffffffff'

    def test_args_21230(self):
        assert self.parser.parse_arg('0ffffh', def_size=2, destination=False) == '0x0ffff'

    def test_args_21240(self):
        assert self.parser.parse_arg('0ffh', def_size=1, destination=False) == '0x0ff'

    def test_args_21250(self):
        assert self.parser.parse_arg('1', def_size=0, destination=False) == '1'

    def test_args_21260(self):
        assert self.parser.parse_arg('1', def_size=1, destination=False) == '1'

    def test_args_21270(self):
        assert self.parser.parse_arg('10', def_size=1, destination=False) == '10'

    def test_args_21280(self):
        assert self.parser.parse_arg('10000h', def_size=4, destination=False) == '0x10000'

    def test_args_21290(self):
        assert self.parser.parse_arg('1000h', def_size=2, destination=False) == '0x1000'

    def test_args_21300(self):
        assert self.parser.parse_arg('100h', def_size=2, destination=False) == '0x100'

    def test_args_21310(self):
        assert self.parser.parse_arg('1024*10/16', def_size=2, destination=False) == '1024*10/16'

    def test_args_21320(self):
        assert self.parser.parse_arg('1024*1024', def_size=4, destination=False) == '1024*1024'

    def test_args_21330(self):
        assert self.parser.parse_arg('10B', def_size=4, destination=False) == '0x2'

    def test_args_21340(self):
        assert self.parser.parse_arg('10h', def_size=0, destination=False) == '0x10'

    def test_args_21350(self):
        assert self.parser.parse_arg('10h', def_size=1, destination=False) == '0x10'

    def test_args_21360(self):
        assert self.parser.parse_arg('11', def_size=1, destination=False) == '11'

    def test_args_21370(self):
        assert self.parser.parse_arg('111', def_size=1, destination=False) == '111'

    def test_args_21380(self):
        assert self.parser.parse_arg('114h', def_size=2, destination=False) == '0x114'

    def test_args_21390(self):
        assert self.parser.parse_arg('11h', def_size=1, destination=False) == '0x11'

    def test_args_21400(self):
        assert self.parser.parse_arg('12', def_size=1, destination=False) == '12'

    def test_args_21410(self):
        assert self.parser.parse_arg('12340004h', def_size=4, destination=False) == '0x12340004'

    def test_args_21420(self):
        assert self.parser.parse_arg('1234001Dh', def_size=4, destination=False) == '0x1234001D'

    def test_args_21430(self):
        assert self.parser.parse_arg('12340128h', def_size=4, destination=False) == '0x12340128'

    def test_args_21440(self):
        assert self.parser.parse_arg('12340205h', def_size=4, destination=False) == '0x12340205'

    def test_args_21450(self):
        assert self.parser.parse_arg('12340306h', def_size=4, destination=False) == '0x12340306'

    def test_args_21460(self):
        assert self.parser.parse_arg('12340407h', def_size=4, destination=False) == '0x12340407'

    def test_args_21470(self):
        assert self.parser.parse_arg('1234040Ah', def_size=4, destination=False) == '0x1234040A'

    def test_args_21480(self):
        assert self.parser.parse_arg('12340503h', def_size=4, destination=False) == '0x12340503'

    def test_args_21490(self):
        assert self.parser.parse_arg('12340506h', def_size=4, destination=False) == '0x12340506'

    def test_args_21500(self):
        assert self.parser.parse_arg('12340507h', def_size=4, destination=False) == '0x12340507'

    def test_args_21510(self):
        assert self.parser.parse_arg('12340547h', def_size=4, destination=False) == '0x12340547'

    def test_args_21520(self):
        assert self.parser.parse_arg('12340559h', def_size=4, destination=False) == '0x12340559'

    def test_args_21530(self):
        assert self.parser.parse_arg('12340560h', def_size=4, destination=False) == '0x12340560'

    def test_args_21540(self):
        assert self.parser.parse_arg('1234059Fh', def_size=4, destination=False) == '0x1234059F'

    def test_args_21550(self):
        assert self.parser.parse_arg('123405A0h', def_size=4, destination=False) == '0x123405A0'

    def test_args_21560(self):
        assert self.parser.parse_arg('123405FAh', def_size=4, destination=False) == '0x123405FA'

    def test_args_21570(self):
        assert self.parser.parse_arg('12341678h', def_size=4, destination=False) == '0x12341678'

    def test_args_21580(self):
        assert self.parser.parse_arg('12341h', def_size=4, destination=False) == '0x12341'

    def test_args_21590(self):
        assert self.parser.parse_arg('12343h', def_size=4, destination=False) == '0x12343'

    def test_args_21600(self):
        assert self.parser.parse_arg('12345', def_size=2, destination=False) == '12345'

    def test_args_21610(self):
        assert self.parser.parse_arg('1234561Dh', def_size=4, destination=False) == '0x1234561D'

    def test_args_21620(self):
        assert self.parser.parse_arg('12345678h', def_size=4, destination=False) == '0x12345678'

    def test_args_21630(self):
        assert self.parser.parse_arg('12345h', def_size=4, destination=False) == '0x12345'

    def test_args_21640(self):
        assert self.parser.parse_arg('12347F7Fh', def_size=4, destination=False) == '0x12347F7F'

    def test_args_21650(self):
        assert self.parser.parse_arg('12347FFFh', def_size=4, destination=False) == '0x12347FFF'

    def test_args_21660(self):
        assert self.parser.parse_arg('12348000h', def_size=4, destination=False) == '0x12348000'

    def test_args_21670(self):
        assert self.parser.parse_arg('12348080h', def_size=4, destination=False) == '0x12348080'

    def test_args_21680(self):
        assert self.parser.parse_arg('1234h', def_size=2, destination=False) == '0x1234'

    def test_args_21690(self):
        assert self.parser.parse_arg('127Eh', def_size=2, destination=False) == '0x127E'

    def test_args_21700(self):
        assert self.parser.parse_arg('12Ch', def_size=2, destination=False) == '0x12C'

    def test_args_21710(self):
        assert self.parser.parse_arg('13', def_size=1, destination=False) == '13'

    def test_args_21720(self):
        assert self.parser.parse_arg('132', def_size=1, destination=False) == '132'

    def test_args_21730(self):
        assert self.parser.parse_arg('133', def_size=1, destination=False) == '133'

    def test_args_21740(self):
        assert self.parser.parse_arg('13h', def_size=1, destination=False) == '0x13'

    def test_args_21750(self):
        assert self.parser.parse_arg('14', def_size=1, destination=False) == '14'

    def test_args_21760(self):
        assert self.parser.parse_arg('14*320', def_size=4, destination=False) == '14*320'

    def test_args_21770(self):
        assert self.parser.parse_arg('14h', def_size=1, destination=False) == '0x14'

    def test_args_21780(self):
        assert self.parser.parse_arg('15', def_size=1, destination=False) == '15'

    def test_args_21790(self):
        assert self.parser.parse_arg('16', def_size=1, destination=False) == '16'

    def test_args_21800(self):
        assert self.parser.parse_arg('17', def_size=1, destination=False) == '17'

    def test_args_21810(self):
        assert self.parser.parse_arg('17h', def_size=1, destination=False) == '0x17'

    def test_args_21820(self):
        assert self.parser.parse_arg('18', def_size=1, destination=False) == '18'

    def test_args_21830(self):
        assert self.parser.parse_arg('18h', def_size=1, destination=False) == '0x18'

    def test_args_21840(self):
        assert self.parser.parse_arg('19', def_size=1, destination=False) == '19'

    def test_args_21850(self):
        assert self.parser.parse_arg('192', def_size=1, destination=False) == '192'

    def test_args_21860(self):
        assert self.parser.parse_arg('193', def_size=1, destination=False) == '193'

    def test_args_21870(self):
        assert self.parser.parse_arg('1Ch', def_size=1, destination=False) == '0x1C'

    def test_args_21880(self):
        assert self.parser.parse_arg('1Eh', def_size=1, destination=False) == '0x1E'

    def test_args_21890(self):
        assert self.parser.parse_arg('1FEh', def_size=2, destination=False) == '0x1FE'

    def test_args_21900(self):
        assert self.parser.parse_arg('1FF7Fh', def_size=4, destination=False) == '0x1FF7F'

    def test_args_21910(self):
        assert self.parser.parse_arg('1FF80h', def_size=4, destination=False) == '0x1FF80'

    def test_args_21920(self):
        assert self.parser.parse_arg('1FF81h', def_size=4, destination=False) == '0x1FF81'

    def test_args_21930(self):
        assert self.parser.parse_arg('1FFEh', def_size=2, destination=False) == '0x1FFE'

    def test_args_21940(self):
        assert self.parser.parse_arg('1FFFEh', def_size=4, destination=False) == '0x1FFFE'

    def test_args_21950(self):
        assert self.parser.parse_arg('1FFFFEh', def_size=4, destination=False) == '0x1FFFFE'

    def test_args_21960(self):
        assert self.parser.parse_arg('1FFFFFEh', def_size=4, destination=False) == '0x1FFFFFE'

    def test_args_21970(self):
        assert self.parser.parse_arg('1FFFFFFEh', def_size=4, destination=False) == '0x1FFFFFFE'

    def test_args_21980(self):
        assert self.parser.parse_arg('1FFFFFFFh', def_size=4, destination=False) == '0x1FFFFFFF'

    def test_args_21990(self):
        assert self.parser.parse_arg('1FFFFFFh', def_size=4, destination=False) == '0x1FFFFFF'

    def test_args_22000(self):
        assert self.parser.parse_arg('1FFFFFh', def_size=4, destination=False) == '0x1FFFFF'

    def test_args_22010(self):
        assert self.parser.parse_arg('1FFFFh', def_size=4, destination=False) == '0x1FFFF'

    def test_args_22020(self):
        assert self.parser.parse_arg('1FFFh', def_size=2, destination=False) == '0x1FFF'

    def test_args_22030(self):
        assert self.parser.parse_arg('1FFh', def_size=2, destination=False) == '0x1FF'

    def test_args_22040(self):
        assert self.parser.parse_arg('1Fh', def_size=1, destination=False) == '0x1F'

    def test_args_22050(self):
        assert self.parser.parse_arg('2', def_size=0, destination=False) == '2'

    def test_args_22060(self):
        assert self.parser.parse_arg('2', def_size=1, destination=False) == '2'

    def test_args_22070(self):
        assert self.parser.parse_arg('20', def_size=1, destination=False) == '20'

    def test_args_22080(self):
        assert self.parser.parse_arg('20000h', def_size=4, destination=False) == '0x20000'

    def test_args_22090(self):
        assert self.parser.parse_arg('20h', def_size=1, destination=False) == '0x20'

    def test_args_22100(self):
        assert self.parser.parse_arg('21', def_size=1, destination=False) == '21'

    def test_args_22110(self):
        assert self.parser.parse_arg('21AD3D34h', def_size=4, destination=False) == '0x21AD3D34'

    def test_args_22120(self):
        assert self.parser.parse_arg('21h', def_size=0, destination=False) == '0x21'

    def test_args_22130(self):
        assert self.parser.parse_arg('22', def_size=1, destination=False) == '22'

    def test_args_22140(self):
        assert self.parser.parse_arg('23', def_size=1, destination=False) == '23'

    def test_args_22150(self):
        assert self.parser.parse_arg('24', def_size=1, destination=False) == '24'

    def test_args_22160(self):
        assert self.parser.parse_arg('24h', def_size=1, destination=False) == '0x24'

    def test_args_22170(self):
        assert self.parser.parse_arg('25', def_size=1, destination=False) == '25'

    def test_args_22180(self):
        assert self.parser.parse_arg('255', def_size=1, destination=False) == '255'

    def test_args_22190(self):
        assert self.parser.parse_arg('256', def_size=2, destination=False) == '256'

    def test_args_22200(self):
        assert self.parser.parse_arg('256*3', def_size=2, destination=False) == '256*3'

    def test_args_22210(self):
        assert self.parser.parse_arg('256+3', def_size=2, destination=False) == '256+3'

    def test_args_22220(self):
        assert self.parser.parse_arg('256+3+65536', def_size=4, destination=False) == '256+3+65536'

    def test_args_22230(self):
        assert self.parser.parse_arg('26', def_size=1, destination=False) == '26'

    def test_args_22240(self):
        assert self.parser.parse_arg('27', def_size=1, destination=False) == '27'

    def test_args_22250(self):
        assert self.parser.parse_arg('28', def_size=1, destination=False) == '28'

    def test_args_22260(self):
        assert self.parser.parse_arg('29', def_size=1, destination=False) == '29'

    def test_args_22270(self):
        assert self.parser.parse_arg('2Ch', def_size=1, destination=False) == '0x2C'

    def test_args_22280(self):
        assert self.parser.parse_arg('2Dh', def_size=1, destination=False) == '0x2D'

    def test_args_22290(self):
        assert self.parser.parse_arg('2Dh', def_size=2, destination=False) == '0x2D'

    def test_args_22300(self):
        assert self.parser.parse_arg('2Dh', def_size=4, destination=False) == '0x2D'

    def test_args_22310(self):
        assert self.parser.parse_arg('3', def_size=0, destination=False) == '3'

    def test_args_22320(self):
        assert self.parser.parse_arg('3', def_size=1, destination=False) == '3'

    def test_args_22330(self):
        assert self.parser.parse_arg('3*4', def_size=4, destination=False) == '3*4'

    def test_args_22340(self):
        assert self.parser.parse_arg('30', def_size=1, destination=False) == '30'

    def test_args_22350(self):
        assert self.parser.parse_arg('303Bh', def_size=2, destination=False) == '0x303B'

    def test_args_22360(self):
        assert self.parser.parse_arg('30h', def_size=1, destination=False) == '0x30'

    def test_args_22370(self):
        assert self.parser.parse_arg('31', def_size=1, destination=False) == '31'

    def test_args_22380(self):
        assert self.parser.parse_arg('31h', def_size=0, destination=False) == '0x31'

    def test_args_22390(self):
        assert self.parser.parse_arg('32', def_size=1, destination=False) == '32'

    def test_args_22400(self):
        assert self.parser.parse_arg('320*200/4', def_size=4, destination=False) == '320*200/4'

    def test_args_22410(self):
        assert self.parser.parse_arg('32432434h', def_size=4, destination=False) == '0x32432434'

    def test_args_22420(self):
        assert self.parser.parse_arg('340128h', def_size=4, destination=False) == '0x340128'

    def test_args_22430(self):
        assert self.parser.parse_arg('35', def_size=1, destination=False) == '35'

    def test_args_22440(self):
        assert self.parser.parse_arg('37', def_size=1, destination=False) == '37'

    def test_args_22450(self):
        assert self.parser.parse_arg('39h', def_size=1, destination=False) == '0x39'

    def test_args_22460(self):
        assert self.parser.parse_arg('3Ch', def_size=1, destination=False) == '0x3C'

    def test_args_22470(self):
        assert self.parser.parse_arg('3DAh', def_size=2, destination=False) == '0x3DA'

    def test_args_22480(self):
        assert self.parser.parse_arg('3Eh', def_size=1, destination=False) == '0x3E'

    def test_args_22490(self):
        assert self.parser.parse_arg('3FEh', def_size=2, destination=False) == '0x3FE'

    def test_args_22500(self):
        assert self.parser.parse_arg('3FFEh', def_size=2, destination=False) == '0x3FFE'

    def test_args_22510(self):
        assert self.parser.parse_arg('3FFFEh', def_size=4, destination=False) == '0x3FFFE'

    def test_args_22520(self):
        assert self.parser.parse_arg('3FFFFEh', def_size=4, destination=False) == '0x3FFFFE'

    def test_args_22530(self):
        assert self.parser.parse_arg('3FFFFFEh', def_size=4, destination=False) == '0x3FFFFFE'

    def test_args_22540(self):
        assert self.parser.parse_arg('3FFFFFFEh', def_size=4, destination=False) == '0x3FFFFFFE'

    def test_args_22550(self):
        assert self.parser.parse_arg('3FFFFFFFh', def_size=4, destination=False) == '0x3FFFFFFF'

    def test_args_22560(self):
        assert self.parser.parse_arg('3FFFFFFh', def_size=4, destination=False) == '0x3FFFFFF'

    def test_args_22570(self):
        assert self.parser.parse_arg('3FFFFFh', def_size=4, destination=False) == '0x3FFFFF'

    def test_args_22580(self):
        assert self.parser.parse_arg('3FFFFh', def_size=4, destination=False) == '0x3FFFF'

    def test_args_22590(self):
        assert self.parser.parse_arg('3FFFh', def_size=2, destination=False) == '0x3FFF'

    def test_args_22600(self):
        assert self.parser.parse_arg('3FFh', def_size=2, destination=False) == '0x3FF'

    def test_args_22610(self):
        assert self.parser.parse_arg('3Fh', def_size=1, destination=False) == '0x3F'

    def test_args_22620(self):
        assert self.parser.parse_arg('3c8h', def_size=2, destination=False) == '0x3c8'

    def test_args_22630(self):
        assert self.parser.parse_arg('3c9h', def_size=2, destination=False) == '0x3c9'

    def test_args_22640(self):
        assert self.parser.parse_arg('3h', def_size=1, destination=False) == '0x3'

    def test_args_22650(self):
        assert self.parser.parse_arg('4', def_size=1, destination=False) == '4'

    def test_args_22660(self):
        assert self.parser.parse_arg('4+5*256', def_size=2, destination=False) == '4+5*256'

    def test_args_22670(self):
        assert self.parser.parse_arg('4000000', def_size=4, destination=False) == '4000000'

    def test_args_22680(self):
        assert self.parser.parse_arg('40h', def_size=1, destination=False) == '0x40'

    def test_args_22690(self):
        assert self.parser.parse_arg('43210123h', def_size=4, destination=False) == '0x43210123'

    def test_args_22700(self):
        assert self.parser.parse_arg('48h', def_size=1, destination=False) == '0x48'

    def test_args_22710(self):
        assert self.parser.parse_arg('49h', def_size=1, destination=False) == '0x49'

    def test_args_22720(self):
        assert self.parser.parse_arg('4Ah', def_size=1, destination=False) == '0x4A'

    def test_args_22730(self):
        assert self.parser.parse_arg('4Ch', def_size=1, destination=False) == '0x4C'

    def test_args_22740(self):
        assert self.parser.parse_arg('4ch', def_size=1, destination=False) == '0x4c'

    def test_args_22750(self):
        assert self.parser.parse_arg('5', def_size=1, destination=False) == '5'

    def test_args_22760(self):
        assert self.parser.parse_arg('50', def_size=1, destination=False) == '50'

    def test_args_22770(self):
        assert self.parser.parse_arg('501h', def_size=2, destination=False) == '0x501'

    def test_args_22780(self):
        assert self.parser.parse_arg('511', def_size=2, destination=False) == '511'

    def test_args_22790(self):
        assert self.parser.parse_arg('55', def_size=1, destination=False) == '55'

    def test_args_22800(self):
        assert self.parser.parse_arg('56', def_size=1, destination=False) == '56'

    def test_args_22810(self):
        assert self.parser.parse_arg('57', def_size=1, destination=False) == '57'

    def test_args_22820(self):
        assert self.parser.parse_arg('6', def_size=1, destination=False) == '6'

    def test_args_22830(self):
        assert self.parser.parse_arg('6*256+5', def_size=2, destination=False) == '6*256+5'

    def test_args_22840(self):
        assert self.parser.parse_arg('60', def_size=1, destination=False) == '60'

    def test_args_22850(self):
        assert self.parser.parse_arg('65324h', def_size=4, destination=False) == '0x65324'

    def test_args_22860(self):
        assert self.parser.parse_arg('65423456h', def_size=4, destination=False) == '0x65423456'

    def test_args_22870(self):
        assert self.parser.parse_arg('6789ABCDh', def_size=4, destination=False) == '0x6789ABCD'

    def test_args_22880(self):
        assert self.parser.parse_arg('7', def_size=1, destination=False) == '7'

    def test_args_22890(self):
        assert self.parser.parse_arg('7Eh', def_size=1, destination=False) == '0x7E'

    def test_args_22900(self):
        assert self.parser.parse_arg('7FEh', def_size=2, destination=False) == '0x7FE'

    def test_args_22910(self):
        assert self.parser.parse_arg('7FFEh', def_size=2, destination=False) == '0x7FFE'

    def test_args_22920(self):
        assert self.parser.parse_arg('7FFFEh', def_size=4, destination=False) == '0x7FFFE'

    def test_args_22930(self):
        assert self.parser.parse_arg('7FFFFEh', def_size=4, destination=False) == '0x7FFFFE'

    def test_args_22940(self):
        assert self.parser.parse_arg('7FFFFFEh', def_size=4, destination=False) == '0x7FFFFFE'

    def test_args_22950(self):
        assert self.parser.parse_arg('7FFFFFFEh', def_size=4, destination=False) == '0x7FFFFFFE'

    def test_args_22960(self):
        assert self.parser.parse_arg('7FFFFFFFh', def_size=4, destination=False) == '0x7FFFFFFF'

    def test_args_22970(self):
        assert self.parser.parse_arg('7FFFFFFh', def_size=4, destination=False) == '0x7FFFFFF'

    def test_args_22980(self):
        assert self.parser.parse_arg('7FFFFFh', def_size=4, destination=False) == '0x7FFFFF'

    def test_args_22990(self):
        assert self.parser.parse_arg('7FFFFh', def_size=4, destination=False) == '0x7FFFF'

    def test_args_23000(self):
        assert self.parser.parse_arg('7FFFh', def_size=2, destination=False) == '0x7FFF'

    def test_args_23010(self):
        assert self.parser.parse_arg('7FFFh', def_size=4, destination=False) == '0x7FFF'

    def test_args_23020(self):
        assert self.parser.parse_arg('7FFh', def_size=2, destination=False) == '0x7FF'

    def test_args_23030(self):
        assert self.parser.parse_arg('7Fh', def_size=1, destination=False) == '0x7F'

    def test_args_23040(self):
        assert self.parser.parse_arg('8', def_size=0, destination=False) == '8'

    def test_args_23050(self):
        assert self.parser.parse_arg('8', def_size=1, destination=False) == '8'

    def test_args_23060(self):
        assert self.parser.parse_arg('80000000h', def_size=4, destination=False) == '0x80000000'

    def test_args_23070(self):
        assert self.parser.parse_arg('80000001h', def_size=4, destination=False) == '0x80000001'

    def test_args_23080(self):
        assert self.parser.parse_arg('80008481h', def_size=4, destination=False) == '0x80008481'

    def test_args_23090(self):
        assert self.parser.parse_arg('80008688h', def_size=4, destination=False) == '0x80008688'

    def test_args_23100(self):
        assert self.parser.parse_arg('8000h', def_size=2, destination=False) == '0x8000'

    def test_args_23110(self):
        assert self.parser.parse_arg('8000h', def_size=4, destination=False) == '0x8000'

    def test_args_23120(self):
        assert self.parser.parse_arg('801h', def_size=2, destination=False) == '0x801'

    def test_args_23130(self):
        assert self.parser.parse_arg('80h', def_size=1, destination=False) == '0x80'

    def test_args_23140(self):
        assert self.parser.parse_arg('81234567h', def_size=4, destination=False) == '0x81234567'

    def test_args_23150(self):
        assert self.parser.parse_arg('81238567h', def_size=4, destination=False) == '0x81238567'

    def test_args_23160(self):
        assert self.parser.parse_arg('812FADAh', def_size=4, destination=False) == '0x812FADA'

    def test_args_23170(self):
        assert self.parser.parse_arg('813F3421h', def_size=4, destination=False) == '0x813F3421'

    def test_args_23180(self):
        assert self.parser.parse_arg('81h', def_size=1, destination=False) == '0x81'

    def test_args_23190(self):
        assert self.parser.parse_arg('82345679h', def_size=4, destination=False) == '0x82345679'

    def test_args_23200(self):
        assert self.parser.parse_arg('8234A6F8h', def_size=4, destination=False) == '0x8234A6F8'

    def test_args_23210(self):
        assert self.parser.parse_arg('8345A1F2h', def_size=4, destination=False) == '0x8345A1F2'

    def test_args_23220(self):
        assert self.parser.parse_arg('8C5h', def_size=2, destination=False) == '0x8C5'

    def test_args_23230(self):
        assert self.parser.parse_arg('8D5h', def_size=2, destination=False) == '0x8D5'

    def test_args_23240(self):
        assert self.parser.parse_arg('9', def_size=1, destination=False) == '9'

    def test_args_23250(self):
        assert self.parser.parse_arg('9ABCDEFh', def_size=0, destination=False) == '0x9ABCDEF'

    def test_args_23260(self):
        assert self.parser.parse_arg('AL', def_size=1, destination=True) == 'al'

    def test_args_23270(self):
        assert self.parser.parse_arg('B', def_size=4, destination=False) == 'b'

    def test_args_23280(self):
        assert self.parser.parse_arg('CC', def_size=4, destination=False) == 'cc'

    def test_args_23290(self):
        assert self.parser.parse_arg('DDD', def_size=0, destination=False) == 'ddd'

    def test_args_23300(self):
        assert self.parser.parse_arg('DX', def_size=2, destination=True) == 'dx'

    #def test_args_23310(self):

    #def test_args_23320(self):

    def test_args_23330(self):
        assert self.parser.parse_arg('TWO', def_size=4, destination=False) == 'two'

    def test_args_23340(self):
        assert self.parser.parse_arg('ah', def_size=1, destination=False) == 'ah'

    def test_args_23350(self):
        assert self.parser.parse_arg('ah', def_size=1, destination=True) == 'ah'

    def test_args_23360(self):
        assert self.parser.parse_arg('al', def_size=0, destination=False) == 'al'

    def test_args_23370(self):
        assert self.parser.parse_arg('al', def_size=1, destination=False) == 'al'

    def test_args_23380(self):
        assert self.parser.parse_arg('al', def_size=1, destination=True) == 'al'

    def test_args_23390(self):
        assert self.parser.parse_arg('ax', def_size=0, destination=False) == 'ax'

    def test_args_23400(self):
        assert self.parser.parse_arg('ax', def_size=2, destination=False) == 'ax'

    def test_args_23410(self):
        assert self.parser.parse_arg('ax', def_size=2, destination=True) == 'ax'

    #def test_args_23420(self):

    #def test_args_23430(self):

    #def test_args_23440(self):

    def test_args_23450(self):
        assert self.parser.parse_arg('bh', def_size=0, destination=False) == 'bh'

    def test_args_23460(self):
        assert self.parser.parse_arg('bh', def_size=1, destination=False) == 'bh'

    def test_args_23470(self):
        assert self.parser.parse_arg('bh', def_size=1, destination=True) == 'bh'

    def test_args_23480(self):
        assert self.parser.parse_arg('bl', def_size=0, destination=False) == 'bl'

    def test_args_23490(self):
        assert self.parser.parse_arg('bl', def_size=1, destination=False) == 'bl'

    def test_args_23500(self):
        assert self.parser.parse_arg('bl', def_size=1, destination=True) == 'bl'

    def test_args_23510(self):
        assert self.parser.parse_arg('bp', def_size=2, destination=False) == 'bp'

    #def test_args_23520(self):

    def test_args_23530(self):
        assert self.parser.parse_arg('bx', def_size=0, destination=False) == 'bx'

    def test_args_23540(self):
        assert self.parser.parse_arg('bx', def_size=2, destination=False) == 'bx'

    def test_args_23550(self):
        assert self.parser.parse_arg('bx', def_size=2, destination=True) == 'bx'

    #def test_args_23560(self):

    def test_args_23570(self):
        assert self.parser.parse_arg('ch', def_size=1, destination=True) == 'ch'

    def test_args_23580(self):
        assert self.parser.parse_arg('cl', def_size=0, destination=False) == 'cl'

    def test_args_23590(self):
        assert self.parser.parse_arg('cl', def_size=1, destination=False) == 'cl'

    def test_args_23600(self):
        assert self.parser.parse_arg('cl', def_size=1, destination=True) == 'cl'

    def test_args_23610(self):
        assert self.parser.parse_arg('cx', def_size=0, destination=False) == 'cx'

    def test_args_23620(self):
        assert self.parser.parse_arg('cx', def_size=2, destination=False) == 'cx'

    def test_args_23630(self):
        assert self.parser.parse_arg('cx', def_size=2, destination=True) == 'cx'

    def test_args_23640(self):
        assert self.parser.parse_arg('di', def_size=2, destination=False) == 'di'

    def test_args_23650(self):
        assert self.parser.parse_arg('dl', def_size=0, destination=False) == 'dl'

    def test_args_23660(self):
        assert self.parser.parse_arg('dl', def_size=1, destination=False) == 'dl'

    def test_args_23670(self):
        assert self.parser.parse_arg('dl', def_size=1, destination=True) == 'dl'

    def test_args_23680(self):
        assert self.parser.parse_arg('ds', def_size=0, destination=False) == 'ds'

    def test_args_23690(self):
        assert self.parser.parse_arg('ds', def_size=2, destination=True) == 'ds'

    def test_args_23700(self):
        assert self.parser.parse_arg('dx', def_size=0, destination=False) == 'dx'

    def test_args_23710(self):
        assert self.parser.parse_arg('dx', def_size=2, destination=False) == 'dx'

    def test_args_23720(self):
        assert self.parser.parse_arg('dx', def_size=2, destination=True) == 'dx'

    def test_args_23730(self):
        assert self.parser.parse_arg('eax', def_size=0, destination=False) == 'eax'

    def test_args_23740(self):
        assert self.parser.parse_arg('eax', def_size=4, destination=False) == 'eax'

    def test_args_23750(self):
        assert self.parser.parse_arg('eax', def_size=4, destination=True) == 'eax'

    def test_args_23760(self):
        assert self.parser.parse_arg('eax_0', def_size=0, destination=False) == 'eax_0'

    def test_args_23770(self):
        assert self.parser.parse_arg('ebp', def_size=0, destination=False) == 'ebp'

    def test_args_23780(self):
        assert self.parser.parse_arg('ebp', def_size=4, destination=False) == 'ebp'

    def test_args_23790(self):
        assert self.parser.parse_arg('ebp', def_size=4, destination=True) == 'ebp'

    def test_args_23800(self):
        assert self.parser.parse_arg('ebx', def_size=0, destination=False) == 'ebx'

    def test_args_23810(self):
        assert self.parser.parse_arg('ebx', def_size=4, destination=False) == 'ebx'

    def test_args_23820(self):
        assert self.parser.parse_arg('ebx', def_size=4, destination=True) == 'ebx'

    def test_args_23830(self):
        assert self.parser.parse_arg('ecx', def_size=0, destination=False) == 'ecx'

    def test_args_23840(self):
        assert self.parser.parse_arg('ecx', def_size=4, destination=False) == 'ecx'

    def test_args_23850(self):
        assert self.parser.parse_arg('ecx', def_size=4, destination=True) == 'ecx'

    def test_args_23860(self):
        assert self.parser.parse_arg('ecx_0', def_size=0, destination=False) == 'ecx_0'

    def test_args_23870(self):
        assert self.parser.parse_arg('ecx_0_0', def_size=0, destination=False) == 'ecx_0_0'

    def test_args_23880(self):
        assert self.parser.parse_arg('edi', def_size=0, destination=False) == 'edi'

    def test_args_23890(self):
        assert self.parser.parse_arg('edi', def_size=4, destination=False) == 'edi'

    def test_args_23900(self):
        assert self.parser.parse_arg('edi', def_size=4, destination=True) == 'edi'

    def test_args_23910(self):
        assert self.parser.parse_arg('edi_0', def_size=0, destination=False) == 'edi_0'

    def test_args_23920(self):
        assert self.parser.parse_arg('edi_0', def_size=0, destination=True) == 'edi_0'

    def test_args_23930(self):
        assert self.parser.parse_arg('edx', def_size=0, destination=False) == 'edx'

    def test_args_23940(self):
        assert self.parser.parse_arg('edx', def_size=4, destination=False) == 'edx'

    def test_args_23950(self):
        assert self.parser.parse_arg('edx', def_size=4, destination=True) == 'edx'

    def test_args_23960(self):
        assert self.parser.parse_arg('edx_0_0', def_size=0, destination=False) == 'edx_0_0'

    def test_args_23970(self):
        assert self.parser.parse_arg('edx_0_0', def_size=4, destination=True) == 'edx_0_0'

    def test_args_23980(self):
        assert self.parser.parse_arg('eflags', def_size=1, destination=True) == 'eflags'

    def test_args_23990(self):
        assert self.parser.parse_arg('eflags', def_size=2, destination=True) == 'eflags'

    #def test_args_24000(self):

    def test_args_24010(self):
        assert self.parser.parse_arg('es', def_size=0, destination=False) == 'es'

    def test_args_24020(self):
        assert self.parser.parse_arg('es', def_size=2, destination=True) == 'es'

    def test_args_24030(self):
        assert self.parser.parse_arg('esi', def_size=0, destination=False) == 'esi'

    def test_args_24040(self):
        assert self.parser.parse_arg('esi', def_size=4, destination=False) == 'esi'

    def test_args_24050(self):
        assert self.parser.parse_arg('esi', def_size=4, destination=True) == 'esi'

    def test_args_24060(self):
        assert self.parser.parse_arg('esi_0', def_size=0, destination=False) == 'esi_0'

    def test_args_24070(self):
        assert self.parser.parse_arg('esi_0', def_size=4, destination=False) == 'esi_0'

    def test_args_24080(self):
        assert self.parser.parse_arg('esi_0', def_size=4, destination=True) == 'esi_0'

    def test_args_24090(self):
        assert self.parser.parse_arg('esp', def_size=4, destination=False) == 'esp'

    def test_args_24100(self):
        assert self.parser.parse_arg('esp', def_size=4, destination=True) == 'esp'

    #def test_args_24110(self):

    #def test_args_24120(self):

    def test_args_24130(self):
        assert self.parser.parse_arg('flags', def_size=0, destination=False) == 'flags'

    def test_args_24140(self):
        assert self.parser.parse_arg('flags', def_size=1, destination=True) == 'flags'

    def test_args_24150(self):
        assert self.parser.parse_arg('flags', def_size=2, destination=True) == 'flags'

    def test_args_24160(self):
        assert self.parser.parse_arg('flags', def_size=4, destination=False) == 'flags'

    def test_args_24170(self):
        assert self.parser.parse_arg('fs', def_size=0, destination=False) == 'fs'

    def test_args_24180(self):
        assert self.parser.parse_arg('fs', def_size=2, destination=False) == 'fs'

    def test_args_24190(self):
        assert self.parser.parse_arg('fs', def_size=2, destination=True) == 'fs'

    #def test_args_24200(self):

    def test_args_24210(self):
        assert self.parser.parse_arg('i', def_size=0, destination=False) == 'i'

    def test_args_24220(self):
        assert self.parser.parse_arg('i', def_size=0, destination=True) == 'i'

    def test_args_24230(self):
        assert self.parser.parse_arg('i', def_size=1, destination=True) == 'i'

    def test_args_24240(self):
        assert self.parser.parse_arg('i', def_size=2, destination=True) == 'i'

    def test_args_24250(self):
        assert self.parser.parse_arg('i', def_size=4, destination=False) == 'i'

    def test_args_24260(self):
        assert self.parser.parse_arg('i', def_size=4, destination=True) == 'i'

    def test_args_24270(self):
        assert self.parser.parse_arg("'tseT'", def_size=4, destination=False) == '0x74736554'

    """
    #def test_args_24280(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[a+1]'),def_size=1,destination=False),u'*(raddr(ds,offset(_data,a)+1))')

    #def test_args_24290(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[a]'),def_size=1,destination=False),u'*(raddr(ds,offset(_data,a)))')

    #def test_args_24300(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[a]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,a)))')

    #def test_args_24310(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[cs:table+ax]'),def_size=0,destination=True),u'*(dw*)(raddr(cs,offset(_text,table)+ax))')

    #def test_args_24320(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[doublequote+4]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,doublequote)+4))')

    #def test_args_24330(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+4000h]'),def_size=0,destination=False),u'eax+0x4000')

    #def test_args_24340(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+40h]'),def_size=0,destination=False),u'eax+0x40')

    #def test_args_24350(self):
        # self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+ecx+40h]'),def_size=0,destination=False),u'eax+ecx+0x40')

    def test_args_24360(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax+ecx]'),def_size=0,destination=False),u'eax+ecx')

    def test_args_24370(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[eax]'),def_size=0,destination=False),u'eax')

    def test_args_24380(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+ecx_0]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,ebp+ecx_0))')

    def test_args_24390(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+ecx_0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+ecx_0))')

    def test_args_24400(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+ecx_vals]'),def_size=0,destination=False),u'ebp+ecx_vals')

    def test_args_24410(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+edx_0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+edx_0))')

    def test_args_24420(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+edx_0]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+edx_0))')

    def test_args_24430(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+i*4+ecx_vals]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+i*4+ecx_vals))')

    def test_args_24440(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+i+table]'),def_size=1,destination=True),u'*(raddr(ds,ebp+i+table))')

    def test_args_24450(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+iflags]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+iflags))')

    def test_args_24460(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+op0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+op0))')

    def test_args_24470(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+op0h]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+op0h))')

    def test_args_24480(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s0]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+s0))')

    def test_args_24490(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s0]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+s0))')

    def test_args_24500(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s1]'),def_size=1,destination=True),u'*(raddr(ds,ebp+s1))')

    def test_args_24510(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s1]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+s1))')

    def test_args_24520(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s2]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+s2))')

    def test_args_24530(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+s2]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+s2))')

    def test_args_24540(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+table]'),def_size=0,destination=False),u'ebp+table')

    def test_args_24550(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_1C]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_1C))')

    def test_args_24560(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_1C]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_1C))')

    def test_args_24570(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_20]'),def_size=0,destination=False),u'*(dw*)(raddr(ds,ebp+var_20))')

    def test_args_24580(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_20]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_args_24590(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_20]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_args_24600(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebp+var_4]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_4))')

    def test_args_24610(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+4000h]'),def_size=0,destination=False),u'ebx+0x4000')

    def test_args_24620(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+40h]'),def_size=0,destination=False),u'ebx+0x40')

    def test_args_24630(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+edx+4000h]'),def_size=0,destination=False),u'ebx+edx+0x4000')

    def test_args_24640(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx+edx]'),def_size=0,destination=False),u'ebx+edx')

    def test_args_24650(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ebx]'),def_size=0,destination=False),u'ebx')

    def test_args_24660(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+4000h]'),def_size=0,destination=False),u'ecx+0x4000')

    def test_args_24670(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+40h]'),def_size=0,destination=False),u'ecx+0x40')

    def test_args_24680(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx*2+4000h]'),def_size=0,destination=False),u'ecx+ecx*2+0x4000')

    def test_args_24690(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx*2-0Ah]'),def_size=0,destination=False),u'ecx+ecx*2-0x0A')

    def test_args_24700(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx*2]'),def_size=0,destination=False),u'ecx+ecx*2')

    def test_args_24710(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx+ecx]'),def_size=0,destination=False),u'ecx+ecx')

    def test_args_24720(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[ecx]'),def_size=0,destination=False),u'ecx')

    def test_args_24730(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+1]'),def_size=1,destination=False),u'*(raddr(ds,edi+1))')

    def test_args_24740(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+1]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,edi+1))')

    def test_args_24750(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+4000h]'),def_size=0,destination=False),u'edi+0x4000')

    def test_args_24760(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+40h]'),def_size=0,destination=False),u'edi+0x40')

    def test_args_24770(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi+ecx]'),def_size=0,destination=False),u'edi+ecx')

    def test_args_24780(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi]'),def_size=0,destination=False),u'edi')

    def test_args_24790(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edi]'),def_size=1,destination=False),u'*(raddr(ds,edi))')

    def test_args_24800(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+4000h]'),def_size=0,destination=False),u'edx+0x4000')

    def test_args_24810(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+40h]'),def_size=0,destination=False),u'edx+0x40')

    def test_args_24820(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx*4+4000h]'),def_size=0,destination=False),u'edx+ecx*4+0x4000')

    def test_args_24830(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx*4-0Ah]'),def_size=0,destination=False),u'edx+ecx*4-0x0A')

    def test_args_24840(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx*4]'),def_size=0,destination=False),u'edx+ecx*4')

    def test_args_24850(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx+ecx]'),def_size=0,destination=False),u'edx+ecx')

    def test_args_24860(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[edx]'),def_size=0,destination=False),u'edx')

    def test_args_24870(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+4000h]'),def_size=0,destination=False),u'esi+0x4000')

    def test_args_24880(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+40h]'),def_size=0,destination=False),u'esi+0x40')

    def test_args_24890(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx*8+4000h]'),def_size=0,destination=False),u'esi+ecx*8+0x4000')

    def test_args_24900(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx*8-0Ah]'),def_size=0,destination=False),u'esi+ecx*8-0x0A')

    def test_args_24910(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx*8]'),def_size=0,destination=False),u'esi+ecx*8')

    def test_args_24920(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi+ecx]'),def_size=0,destination=False),u'esi+ecx')

    def test_args_24930(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esi]'),def_size=0,destination=False),u'esi')

    def test_args_24940(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+0Ch]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x0C))')

    def test_args_24950(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+0Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x0C))')

    def test_args_24960(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+10h]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x10))')

    def test_args_24970(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+10h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x10))')

    def test_args_24980(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+14h]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x14))')

    def test_args_24990(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+14h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x14))')

    def test_args_25000(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+18h]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+0x18))')

    def test_args_25010(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+18h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x18))')

    def test_args_25020(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+1Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x1C))')

    def test_args_25030(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+4]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+4))')

    def test_args_25040(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+4))')

    def test_args_25050(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+8]'),def_size=0,destination=True),u'*(dw*)(raddr(ds,esp+8))')

    def test_args_25060(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp+8]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+8))')

    def test_args_25070(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp]'),def_size=0,destination=False),u'*(dw*)(raddr(ds,esp))')

    def test_args_25080(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[esp]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp))')

    def test_args_25090(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[g]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,offset(_data,g)))')

    def test_args_25100(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[h2]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,h2)))')

    def test_args_25110(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+1]'),def_size=0,destination=False),u'i+1')

    def test_args_25120(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+2]'),def_size=0,destination=False),u'i+2')

    def test_args_25130(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+3]'),def_size=0,destination=False),u'i+3')

    def test_args_25140(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+4]'),def_size=0,destination=False),u'i+4')

    def test_args_25150(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+56h]'),def_size=0,destination=False),u'i+0x56')

    def test_args_25160(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i+5]'),def_size=0,destination=False),u'i+5')

    def test_args_25170(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[i-10h]'),def_size=0,destination=False),u'i-0x10')

    def test_args_25180(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[load_handle]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,offset(_data,load_handle)))')

    def test_args_25190(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[load_handle]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,load_handle)))')

    def test_args_25200(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var+3]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)+3))')

    def test_args_25210(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var+4]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)+4))')

    def test_args_25220(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var-1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)-1))')

    def test_args_25230(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var0+5]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var0)+5))')

    def test_args_25240(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var1+1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+1))')

    def test_args_25250(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var1]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,var1)))')

    def test_args_25260(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)))')

    def test_args_25270(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2+2]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var2)+2))')

    def test_args_25280(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2-1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var2)-1))')

    def test_args_25290(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2]'),def_size=0,destination=False),u'*(dw*)(raddr(ds,offset(_data,var2)))')

    def test_args_25300(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var2)))')

    def test_args_25310(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var2]'),def_size=2,destination=True),u'*(dw*)(raddr(ds,offset(_data,var2)))')

    def test_args_25320(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3+3*4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+3*4))')

    def test_args_25330(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3+ebp]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+ebp))')

    def test_args_25340(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3]'),def_size=0,destination=False),u'*(dd*)(raddr(ds,offset(_data,var3)))')

    def test_args_25350(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var3]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)))')

    def test_args_25360(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var4+t]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var4)+t))')

    def test_args_25370(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var4]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var4)))')

    def test_args_25380(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'[var]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var)))')

    def test_args_25390(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'_data'),def_size=1,destination=False),u'seg_offset(_data)')

    def test_args_25400(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'a'),def_size=1,destination=True),u'a')

    def test_args_25410(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [a]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,a)))')

    def test_args_25420(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [ebp+var_20]'),def_size=1,destination=False),u'*(raddr(ds,ebp+var_20))')

    def test_args_25430(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [ebp+var_20]'),def_size=1,destination=True),u'*(raddr(ds,ebp+var_20))')

    def test_args_25440(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+1]'),def_size=0,destination=False),u'*(raddr(ds,edi+1))')

    def test_args_25450(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+1]'),def_size=1,destination=True),u'*(raddr(ds,edi+1))')

    def test_args_25460(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+7]'),def_size=0,destination=False),u'*(raddr(ds,edi+7))')

    def test_args_25470(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [edi+7]'),def_size=1,destination=True),u'*(raddr(ds,edi+7))')

    def test_args_25480(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [esi]'),def_size=1,destination=True),u'*(raddr(ds,esi))')

    def test_args_25490(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [h2]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,h2)))')

    def test_args_25500(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [h]'),def_size=0,destination=False),u'*(raddr(ds,offset(_data,h)))')

    def test_args_25510(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [testOVerlap+1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,testOVerlap)+1))')

    def test_args_25520(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [var1+1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+1))')

    def test_args_25530(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr [var1+2]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+2))')

    def test_args_25540(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr dl'),def_size=1,destination=True),u'dl')

    def test_args_25550(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr ds:[0]'),def_size=1,destination=True),u'*(raddr(ds,0))')

    def test_args_25560(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr es:[0]'),def_size=0,destination=False),u'*(raddr(es,0))')

    def test_args_25570(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'byte ptr es:[0]'),def_size=1,destination=True),u'*(raddr(es,0))')
    """
    def test_args_25580(self):
        assert self.parser.parse_arg('ds:[eax*2]', def_size=0, destination=False) == '*(raddr(ds,eax*2))'

    def test_args_25590(self):
        assert self.parser.parse_arg('ds:[ebx*4]', def_size=0, destination=False) == '*(raddr(ds,ebx*4))'

    def test_args_25600(self):
        assert self.parser.parse_arg('ds:[ecx*8]', def_size=0, destination=False) == '*(raddr(ds,ecx*8))'
    """
    def test_args_25610(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:40h[ebx*4]'), def_size=0, destination=False), u'*(raddr(ds,0x40+ebx*4))')

    def test_args_25620(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:40h[ecx*8]'), def_size=0, destination=False), u'*(raddr(ds,0x40+ecx*8))')

    def test_args_25630(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:[edi]'),def_size=1,destination=True),u'*(raddr(ds,edi))')

    def test_args_25640(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ds:byte_41411F[eax]'),def_size=1,destination=True),u'*(raddr(ds,offset(_bss,byte_41411F)+eax))')

    def test_args_25650(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20+4]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_20+4))')

    def test_args_25660(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20+4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_20+4))')

    def test_args_25670(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20]'),def_size=4,destination=False),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_args_25680(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebp+var_20]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,ebp+var_20))')

    def test_args_25690(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [ebx-4]'),def_size=0,destination=True),u'*(dd*)(raddr(ds,ebx-4))')

    def test_args_25700(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+0Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x0C))')

    def test_args_25710(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+10h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x10))')

    def test_args_25720(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+14h]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x14))')

    def test_args_25730(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+1Ch]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+0x1C))')

    def test_args_25740(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+4]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+4))')

    def test_args_25750(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp+8]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp+8))')

    def test_args_25760(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr [esp]'),def_size=4,destination=True),u'*(dd*)(raddr(ds,esp))')

    def test_args_25770(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr buffer'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,buffer)))')

    def test_args_25780(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr es:[0]'),def_size=4,destination=True),u'*(dd*)(raddr(es,0))')

    def test_args_25790(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr es:[20*320+160]'),def_size=4,destination=True),u'*(dd*)(raddr(es,20*320+160))')

    def test_args_25800(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'dword ptr var4'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var4)))')

    def test_args_25810(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'large ds:4000h'),def_size=0,destination=False),u'large ds:0x4000')

    def test_args_25820(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset _msg'),def_size=4,destination=False),u'offset(_data,_msg)')

    def test_args_25830(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset _test_btc'),def_size=4,destination=False),u'offset(initcall,_test_btc)')

    def test_args_25840(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset a0x4000'),def_size=4,destination=False),u'offset(_rdata,a0x4000)')

    def test_args_25850(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset aXorl'),def_size=4,destination=False),u'offset(_rdata,aXorl)')

    def test_args_25860(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset aXorw'),def_size=4,destination=False),u'offset(_rdata,aXorw)')

    def test_args_25870(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset pal_jeu'),def_size=4,destination=False),u'offset(_data,pal_jeu)')

    def test_args_25880(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset str1'),def_size=4,destination=False),u'offset(_data,str1)')

    def test_args_25890(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset str2'),def_size=4,destination=False),u'offset(_data,str2)')

    def test_args_25900(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset str3'),def_size=4,destination=False),u'offset(_data,str3)')

    def test_args_25910(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset testOVerlap'),def_size=4,destination=False),u'offset(_data,testOVerlap)')

    def test_args_25920(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset unk_40E008'),def_size=4,destination=False),u'offset(_data,unk_40E008)')

    def test_args_25930(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset unk_40F064'),def_size=4,destination=False),u'offset(initcall,unk_40F064)')

    def test_args_25940(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var1'),def_size=4,destination=False),u'offset(_data,var1)')

    def test_args_25950(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var1+1'),def_size=4,destination=False),u'offset(_data,var1)+1')

    def test_args_25960(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var2'),def_size=4,destination=False),u'offset(_data,var2)')

    def test_args_25970(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var3'),def_size=4,destination=False),u'offset(_data,var3)')

    def test_args_25980(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var3+4'),def_size=4,destination=False),u'offset(_data,var3)+4')

    def test_args_25990(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var4'),def_size=4,destination=False),u'offset(_data,var4)')

    def test_args_26000(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var4+1'),def_size=4,destination=False),u'offset(_data,var4)+1')

    def test_args_26010(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'offset var4+4'),def_size=4,destination=False),u'offset(_data,var4)+4')

    def test_args_26020(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'op0'),def_size=0,destination=False),u'op0')

    def test_args_26030(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'op0'),def_size=4,destination=True),u'op0')

    def test_args_26040(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'op1'),def_size=0,destination=False),u'op1')

    def test_args_26050(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'printf'),def_size=0,destination=True),u'printf')

    def test_args_26060(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'ptr'),def_size=0,destination=False),u'ptr')

    def test_args_26070(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'r'),def_size=0,destination=False),u'r')

    def test_args_26080(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=0,destination=False),u'res')

    def test_args_26090(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=0,destination=True),u'res')

    def test_args_26100(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=4,destination=False),u'res')

    def test_args_26110(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'res'),def_size=4,destination=True),u'res')

    def test_args_26120(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'resh'),def_size=0,destination=False),u'resh')

    def test_args_26130(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'resh'),def_size=4,destination=False),u'resh')

    def test_args_26140(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'resz'),def_size=0,destination=False),u'resz')

    def test_args_26150(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'rh'),def_size=0,destination=False),u'rh')

    def test_args_26160(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's0_0'),def_size=0,destination=False),u's0_0')

    def test_args_26170(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's0_0'),def_size=4,destination=False),u's0_0')

    def test_args_26180(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's1_0'),def_size=0,destination=False),u's1_0')

    def test_args_26190(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u's1_0'),def_size=4,destination=False),u's1_0')

    def test_args_26200(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'si'),def_size=2,destination=False),u'si')

    def test_args_26210(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'small'),def_size=0,destination=False),u'small')

    def test_args_26220(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u't'),def_size=4,destination=False),u't')

    def test_args_26230(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'taille_moire'),def_size=4,destination=False),u'taille_moire')

    def test_args_26240(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'teST2'),def_size=4,destination=False),u'teST2')

    def test_args_26250(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'testOVerlap'),def_size=0,destination=False),u'offset(_data,testOVerlap)')

    def test_args_26260(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=0,destination=False),u'var1')

    def test_args_26270(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=0,destination=False),u'offset(_data,var1)')

    def test_args_26280(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=1,destination=False),u'var1')

    def test_args_26290(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=1,destination=True),u'*(db*)&m.var1')

    def test_args_26300(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1'),def_size=1,destination=True),u'var1')

    def test_args_26310(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1[1]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+1))')

    def test_args_26320(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1[bx+si]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+bx+si))')

    def test_args_26330(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var1[bx]'),def_size=1,destination=True),u'*(raddr(ds,offset(_data,var1)+bx))')

    def test_args_26340(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var2'),def_size=0,destination=False),u'offset(_data,var2)')

    def test_args_26350(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var2'),def_size=2,destination=True),u'var2')

    #def test_args_26360(self):
    #    self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3'),def_size=4,destination=True),u'var3')

    def test_args_26370(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3+3*4'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+3*4))')

    def test_args_26380(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3+ebp'),def_size=4,destination=True),u'*(dd*)(raddr(ds,offset(_data,var3)+ebp))')

    def test_args_26390(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var5'),def_size=0,destination=False),u'offset(_data,var5)')

    def test_args_26400(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [d]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,offset(_data,d)))')

    def test_args_26410(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [e]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,offset(_data,e)))')

    def test_args_26420(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [ebp+var_20]'),def_size=2,destination=False),u'*(dw*)(raddr(ds,ebp+var_20))')

    def test_args_26430(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [ebp+var_20]'),def_size=2,destination=True),u'*(dw*)(raddr(ds,ebp+var_20))')

    def test_args_26440(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr [var5+2]'),def_size=2,destination=True),u'*(dw*)(raddr(ds,offset(_data,var5)+2))')

    def test_args_26450(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word ptr var5'),def_size=2,destination=True),u'*(dw*)(raddr(ds,offset(_data,var5)))')

    def test_args_26460(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'word'),def_size=0,destination=False),u'word')

    def test_args_26470(self):
        self.assertEqual(self.cpp.expand(expr=self.parser.parse_arg(u'var3'),def_size=0,destination=False),u'var3')
    """

    """
    def test_cpp_26480(self):
        self.assertEqual(self.parser.test_size(u"'Z' - 'A' +1"), 1)

    def test_cpp_26490(self):
        self.assertEqual(self.parser.test_size(u"'a'"), 1)

    def test_cpp_26500(self):
        self.assertEqual(self.parser.test_size(u"'c'"), 1)

    def test_cpp_26510(self):
        self.assertEqual(self.parser.test_size(u"'d'"), 1)

    def test_cpp_26520(self):
        self.assertEqual(self.parser.test_size(u"'dcba'"), 4)

    def test_cpp_26530(self):
        self.assertEqual(self.parser.test_size(u"'tseT'"), 4)

    def test_cpp_26540(self):
        self.assertEqual(self.parser.test_size(u'(1024*10/16)+5'), 2)

    def test_cpp_26550(self):
        self.assertEqual(self.parser.test_size(u'(1024*10/16)-1'), 2)

    def test_cpp_26560(self):
        self.assertEqual(self.parser.test_size(u'(offset str_buffer+800h)'), 2)

    def test_cpp_26570(self):
        self.assertEqual(self.parser.test_size(u'(offset str_buffer+810h)'), 2)

    def test_cpp_26580(self):
        self.assertEqual(self.parser.test_size(u'+40h'), 1)

    def test_cpp_26590(self):
        self.assertEqual(self.parser.test_size(u'+4000H'), 2)

    def test_cpp_26600(self):
        self.assertEqual(self.parser.test_size(u'-108h'), 2)

    def test_cpp_26610(self):
        self.assertEqual(self.parser.test_size(u'-1Ch'), 1)

    def test_cpp_26620(self):
        self.assertEqual(self.parser.test_size(u'-20h'), 1)

    def test_cpp_26630(self):
        self.assertEqual(self.parser.test_size(u'-28h'), 1)

    def test_cpp_26640(self):
        self.assertEqual(self.parser.test_size(u'-2Ch'), 1)

    def test_cpp_26650(self):
        self.assertEqual(self.parser.test_size(u'-1'), 1)

    def test_cpp_26660(self):
        self.assertEqual(self.parser.test_size(u'-1-(-2+3)'), 1)

    def test_cpp_26670(self):
        self.assertEqual(self.parser.test_size(u'-12'), 1)

    def test_cpp_26680(self):
        self.assertEqual(self.parser.test_size(u'0'), 1)

    def test_cpp_26690(self):
        self.assertEqual(self.parser.test_size(u'0002h'), 1)

    def test_cpp_26700(self):
        self.assertEqual(self.parser.test_size(u'0007'), 1)  # it is hard to guess size of octal number

    def test_cpp_26710(self):
        self.assertEqual(self.parser.test_size(u'000f3h'), 1)

    def test_cpp_26720(self):
        self.assertEqual(self.parser.test_size(u'000ff00ffh'), 4)

    def test_cpp_26730(self):
        self.assertEqual(self.parser.test_size(u'001111111B'), 1)

    def test_cpp_26740(self):
        self.assertEqual(self.parser.test_size(u'00fffh'), 2)

    def test_cpp_26750(self):
        self.assertEqual(self.parser.test_size(u'00h'), 1)

    def test_cpp_26760(self):
        self.assertEqual(self.parser.test_size(u'0100b'), 1)

    def test_cpp_26770(self):
        self.assertEqual(self.parser.test_size(u'01010101010101010b'), 2)

    def test_cpp_26780(self):
        self.assertEqual(self.parser.test_size(u'0101010101010101b'), 2)

    def test_cpp_26790(self):
        self.assertEqual(self.parser.test_size(u'0101b'), 1)

    def test_cpp_26800(self):
        self.assertEqual(self.parser.test_size(u'010B'), 1)

    def test_cpp_26810(self):
        self.assertEqual(self.parser.test_size(u'011111100B'), 1)

    def test_cpp_26820(self):
        self.assertEqual(self.parser.test_size(u'011111111111111111111111111111111b'), 4)

    def test_cpp_26830(self):
        self.assertEqual(self.parser.test_size(u'01111111111111111b'), 2)

    def test_cpp_26840(self):
        self.assertEqual(self.parser.test_size(u'011111111B'), 1)

    def test_cpp_26850(self):
        self.assertEqual(self.parser.test_size(u'012345678h'), 4)

    def test_cpp_26860(self):
        self.assertEqual(self.parser.test_size(u'01B'), 1)

    def test_cpp_26870(self):
        self.assertEqual(self.parser.test_size(u'01h'), 1)

    def test_cpp_26880(self):
        self.assertEqual(self.parser.test_size(u'02h'), 1)

    def test_cpp_26890(self):
        self.assertEqual(self.parser.test_size(u'03dh'), 1)

    def test_cpp_26900(self):
        self.assertEqual(self.parser.test_size(u'03eh'), 1)

    def test_cpp_26910(self):
        self.assertEqual(self.parser.test_size(u'03fh'), 1)

    def test_cpp_26920(self):
        self.assertEqual(self.parser.test_size(u'042h'), 1)

    def test_cpp_26930(self):
        self.assertEqual(self.parser.test_size(u'077123456h'), 4)

    def test_cpp_26940(self):
        self.assertEqual(self.parser.test_size(u'077aaFF00h'), 4)

    def test_cpp_26950(self):
        self.assertEqual(self.parser.test_size(u'08h'), 1)

    def test_cpp_26960(self):
        self.assertEqual(self.parser.test_size(u'0B'), 1)

    def test_cpp_26970(self):
        self.assertEqual(self.parser.test_size(u'0BC6058h'), 4)

    def test_cpp_26980(self):
        self.assertEqual(self.parser.test_size(u'0D5h'), 1)

    def test_cpp_26990(self):
        self.assertEqual(self.parser.test_size(u'0Eh'), 1)

    def test_cpp_27000(self):
        self.assertEqual(self.parser.test_size(u'0F7h'), 1)

    def test_cpp_27010(self):
        self.assertEqual(self.parser.test_size(u'0FBCA7654h'), 4)

    def test_cpp_27020(self):
        self.assertEqual(self.parser.test_size(u'0FBCA7h'), 4)

    def test_cpp_27030(self):
        self.assertEqual(self.parser.test_size(u'0FEh'), 1)

    def test_cpp_27040(self):
        self.assertEqual(self.parser.test_size(u'0FFEh'), 2)

    def test_cpp_27050(self):
        self.assertEqual(self.parser.test_size(u'0FFFC70F9h'), 4)

    def test_cpp_27060(self):
        self.assertEqual(self.parser.test_size(u'0FFFE0080h'), 4)

    def test_cpp_27070(self):
        self.assertEqual(self.parser.test_size(u'0FFFEDCBFh'), 4)

    def test_cpp_27080(self):
        self.assertEqual(self.parser.test_size(u'0FFFEFDFCh'), 4)

    def test_cpp_27090(self):
        self.assertEqual(self.parser.test_size(u'0FFFEh'), 2)

    def test_cpp_27100(self):
        self.assertEqual(self.parser.test_size(u'0FFFF7FFFh'), 4)

    def test_cpp_27110(self):
        self.assertEqual(self.parser.test_size(u'0FFFFA549h'), 4)

    def test_cpp_27120(self):
        self.assertEqual(self.parser.test_size(u'0FFFFEh'), 4)

    def test_cpp_27130(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFED4h'), 4)

    def test_cpp_27140(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFEh'), 4)

    def test_cpp_27150(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFD3h'), 4)

    def test_cpp_27160(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFECh'), 4)

    def test_cpp_27170(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFEh'), 4)

    def test_cpp_27180(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFF0h'), 4)

    def test_cpp_27190(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFF7h'), 4)

    def test_cpp_27200(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFAh'), 4)

    def test_cpp_27210(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFBh'), 4)

    def test_cpp_27220(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFCh'), 4)

    def test_cpp_27230(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFDh'), 4)

    def test_cpp_27240(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFEh'), 4)

    def test_cpp_27250(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFFh'), 4)

    def test_cpp_27260(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFFh'), 4)

    def test_cpp_27270(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFFh'), 4)

    def test_cpp_27280(self):
        self.assertEqual(self.parser.test_size(u'0FFFFFh'), 4)

    def test_cpp_27290(self):
        self.assertEqual(self.parser.test_size(u'0FFFFh'), 2)

    def test_cpp_27300(self):
        self.assertEqual(self.parser.test_size(u'0FFFh'), 2)

    def test_cpp_27310(self):
        self.assertEqual(self.parser.test_size(u'0FFh'), 1)

    def test_cpp_27320(self):
        self.assertEqual(self.parser.test_size(u'0Fh'), 1)

    def test_cpp_27330(self):
        self.assertEqual(self.parser.test_size(u'0a0000h'), 4)

    def test_cpp_27340(self):
        self.assertEqual(self.parser.test_size(u'0a000h'), 2)

    def test_cpp_27350(self):
        self.assertEqual(self.parser.test_size(u'0aabbccddh'), 4)

    def test_cpp_27360(self):
        self.assertEqual(self.parser.test_size(u'0abcdef77h'), 4)

    def test_cpp_27370(self):
        self.assertEqual(self.parser.test_size(u'0af222h'), 4)

    def test_cpp_27380(self):
        self.assertEqual(self.parser.test_size(u'0cch'), 1)

    def test_cpp_27390(self):
        self.assertEqual(self.parser.test_size(u'0ddh'), 1)

    def test_cpp_27400(self):
        self.assertEqual(self.parser.test_size(u'0df01h'), 2)

    def test_cpp_27410(self):
        self.assertEqual(self.parser.test_size(u'0dff1h'), 2)

    def test_cpp_27420(self):
        self.assertEqual(self.parser.test_size(u'0f0ffh'), 2)

    def test_cpp_27430(self):
        self.assertEqual(self.parser.test_size(u'0f0h'), 1)

    def test_cpp_27440(self):
        self.assertEqual(self.parser.test_size(u'0f222h'), 2)

    def test_cpp_27450(self):
        self.assertEqual(self.parser.test_size(u'0ffff0003h'), 4)

    def test_cpp_27460(self):
        self.assertEqual(self.parser.test_size(u'0ffff00f3h'), 4)

    def test_cpp_27470(self):
        self.assertEqual(self.parser.test_size(u'0ffff01ffh'), 4)

    def test_cpp_27480(self):
        self.assertEqual(self.parser.test_size(u'0ffffff00h'), 4)

    def test_cpp_27490(self):
        self.assertEqual(self.parser.test_size(u'0ffffff03h'), 4)

    def test_cpp_27500(self):
        self.assertEqual(self.parser.test_size(u'0fffffff3h'), 4)

    def test_cpp_27510(self):
        self.assertEqual(self.parser.test_size(u'0ffffffffh'), 4)

    def test_cpp_27520(self):
        self.assertEqual(self.parser.test_size(u'0ffffh'), 2)

    def test_cpp_27530(self):
        self.assertEqual(self.parser.test_size(u'0ffh'), 1)

    def test_cpp_27540(self):
        self.assertEqual(self.parser.test_size(u'0Ch'), 1)

    def test_cpp_27550(self):
        self.assertEqual(self.parser.test_size(u'1'), 1)

    def test_cpp_27560(self):
        self.assertEqual(self.parser.test_size(u'10'), 1)

    def test_cpp_27570(self):
        self.assertEqual(self.parser.test_size(u'10000h'), 4)

    def test_cpp_27580(self):
        self.assertEqual(self.parser.test_size(u'1000h'), 2)

    def test_cpp_27590(self):
        self.assertEqual(self.parser.test_size(u'100h'), 2)

    def test_cpp_27600(self):
        self.assertEqual(self.parser.test_size(u'1024*10/16'), 2)

    def test_cpp_27610(self):
        self.assertEqual(self.parser.test_size(u'1024*1024'), 4)

    def test_cpp_27620(self):
        self.assertEqual(self.parser.test_size(u'10B'), 1)

    def test_cpp_27630(self):
        self.assertEqual(self.parser.test_size(u'10h'), 1)

    def test_cpp_27640(self):
        self.assertEqual(self.parser.test_size(u'11'), 1)

    def test_cpp_27650(self):
        self.assertEqual(self.parser.test_size(u'111'), 1)

    def test_cpp_27660(self):
        self.assertEqual(self.parser.test_size(u'114h'), 2)

    def test_cpp_27670(self):
        self.assertEqual(self.parser.test_size(u'11h'), 1)

    def test_cpp_27680(self):
        self.assertEqual(self.parser.test_size(u'12'), 1)

    def test_cpp_27690(self):
        self.assertEqual(self.parser.test_size(u'12340004h'), 4)

    def test_cpp_27700(self):
        self.assertEqual(self.parser.test_size(u'1234001Dh'), 4)

    def test_cpp_27710(self):
        self.assertEqual(self.parser.test_size(u'12340128h'), 4)

    def test_cpp_27720(self):
        self.assertEqual(self.parser.test_size(u'12340205h'), 4)

    def test_cpp_27730(self):
        self.assertEqual(self.parser.test_size(u'12340306h'), 4)

    def test_cpp_27740(self):
        self.assertEqual(self.parser.test_size(u'12340407h'), 4)

    def test_cpp_27750(self):
        self.assertEqual(self.parser.test_size(u'1234040Ah'), 4)

    def test_cpp_27760(self):
        self.assertEqual(self.parser.test_size(u'12340503h'), 4)

    def test_cpp_27770(self):
        self.assertEqual(self.parser.test_size(u'12340506h'), 4)

    def test_cpp_27780(self):
        self.assertEqual(self.parser.test_size(u'12340507h'), 4)

    def test_cpp_27790(self):
        self.assertEqual(self.parser.test_size(u'12340547h'), 4)

    def test_cpp_27800(self):
        self.assertEqual(self.parser.test_size(u'12340559h'), 4)

    def test_cpp_27810(self):
        self.assertEqual(self.parser.test_size(u'12340560h'), 4)

    def test_cpp_27820(self):
        self.assertEqual(self.parser.test_size(u'1234059Fh'), 4)

    def test_cpp_27830(self):
        self.assertEqual(self.parser.test_size(u'123405A0h'), 4)

    def test_cpp_27840(self):
        self.assertEqual(self.parser.test_size(u'123405FAh'), 4)

    def test_cpp_27850(self):
        self.assertEqual(self.parser.test_size(u'12341678h'), 4)

    def test_cpp_27860(self):
        self.assertEqual(self.parser.test_size(u'12341h'), 4)

    def test_cpp_27870(self):
        self.assertEqual(self.parser.test_size(u'12343h'), 4)

    def test_cpp_27880(self):
        self.assertEqual(self.parser.test_size(u'12345'), 2)

    def test_cpp_27890(self):
        self.assertEqual(self.parser.test_size(u'1234561Dh'), 4)

    def test_cpp_27900(self):
        self.assertEqual(self.parser.test_size(u'12345678h'), 4)

    def test_cpp_27910(self):
        self.assertEqual(self.parser.test_size(u'12345h'), 4)

    def test_cpp_27920(self):
        self.assertEqual(self.parser.test_size(u'12347F7Fh'), 4)

    def test_cpp_27930(self):
        self.assertEqual(self.parser.test_size(u'12347FFFh'), 4)

    def test_cpp_27940(self):
        self.assertEqual(self.parser.test_size(u'12348000h'), 4)

    def test_cpp_27950(self):
        self.assertEqual(self.parser.test_size(u'12348080h'), 4)

    def test_cpp_27960(self):
        self.assertEqual(self.parser.test_size(u'1234h'), 2)

    def test_cpp_27970(self):
        self.assertEqual(self.parser.test_size(u'127Eh'), 2)

    def test_cpp_27980(self):
        self.assertEqual(self.parser.test_size(u'12Ch'), 2)

    def test_cpp_27990(self):
        self.assertEqual(self.parser.test_size(u'13'), 1)

    def test_cpp_28000(self):
        self.assertEqual(self.parser.test_size(u'132'), 1)

    def test_cpp_28010(self):
        self.assertEqual(self.parser.test_size(u'133'), 1)

    def test_cpp_28020(self):
        self.assertEqual(self.parser.test_size(u'13h'), 1)

    def test_cpp_28030(self):
        self.assertEqual(self.parser.test_size(u'14'), 1)

    def test_cpp_28040(self):
        self.assertEqual(self.parser.test_size(u'14*320'), 2)

    def test_cpp_28050(self):
        self.assertEqual(self.parser.test_size(u'14h'), 1)

    def test_cpp_28060(self):
        self.assertEqual(self.parser.test_size(u'15'), 1)

    def test_cpp_28070(self):
        self.assertEqual(self.parser.test_size(u'16'), 1)

    def test_cpp_28080(self):
        self.assertEqual(self.parser.test_size(u'17'), 1)

    def test_cpp_28090(self):
        self.assertEqual(self.parser.test_size(u'17h'), 1)

    def test_cpp_28100(self):
        self.assertEqual(self.parser.test_size(u'18'), 1)

    def test_cpp_28110(self):
        self.assertEqual(self.parser.test_size(u'18h'), 1)

    def test_cpp_28120(self):
        self.assertEqual(self.parser.test_size(u'19'), 1)

    def test_cpp_28130(self):
        self.assertEqual(self.parser.test_size(u'192'), 1)

    def test_cpp_28140(self):
        self.assertEqual(self.parser.test_size(u'193'), 1)

    def test_cpp_28150(self):
        self.assertEqual(self.parser.test_size(u'1Ch'), 1)

    def test_cpp_28160(self):
        self.assertEqual(self.parser.test_size(u'1Eh'), 1)

    def test_cpp_28170(self):
        self.assertEqual(self.parser.test_size(u'1FEh'), 2)

    def test_cpp_28180(self):
        self.assertEqual(self.parser.test_size(u'1FF7Fh'), 4)

    def test_cpp_28190(self):
        self.assertEqual(self.parser.test_size(u'1FF80h'), 4)

    def test_cpp_28200(self):
        self.assertEqual(self.parser.test_size(u'1FF81h'), 4)

    def test_cpp_28210(self):
        self.assertEqual(self.parser.test_size(u'1FFEh'), 2)

    def test_cpp_28220(self):
        self.assertEqual(self.parser.test_size(u'1FFFEh'), 4)

    def test_cpp_28230(self):
        self.assertEqual(self.parser.test_size(u'1FFFFEh'), 4)

    def test_cpp_28240(self):
        self.assertEqual(self.parser.test_size(u'1FFFFFEh'), 4)

    def test_cpp_28250(self):
        self.assertEqual(self.parser.test_size(u'1FFFFFFEh'), 4)

    def test_cpp_28260(self):
        self.assertEqual(self.parser.test_size(u'1FFFFFFFh'), 4)

    def test_cpp_28270(self):
        self.assertEqual(self.parser.test_size(u'1FFFFFFh'), 4)

    def test_cpp_28280(self):
        self.assertEqual(self.parser.test_size(u'1FFFFFh'), 4)

    def test_cpp_28290(self):
        self.assertEqual(self.parser.test_size(u'1FFFFh'), 4)

    def test_cpp_28300(self):
        self.assertEqual(self.parser.test_size(u'1FFFh'), 2)

    def test_cpp_28310(self):
        self.assertEqual(self.parser.test_size(u'1FFh'), 2)

    def test_cpp_28320(self):
        self.assertEqual(self.parser.test_size(u'1Fh'), 1)

    def test_cpp_28330(self):
        self.assertEqual(self.parser.test_size(u'2'), 1)

    def test_cpp_28340(self):
        self.assertEqual(self.parser.test_size(u'20'), 1)

    def test_cpp_28350(self):
        self.assertEqual(self.parser.test_size(u'20000h'), 4)

    def test_cpp_28360(self):
        self.assertEqual(self.parser.test_size(u'20h'), 1)

    def test_cpp_28370(self):
        self.assertEqual(self.parser.test_size(u'21'), 1)

    def test_cpp_28380(self):
        self.assertEqual(self.parser.test_size(u'21AD3D34h'), 4)

    def test_cpp_28390(self):
        self.assertEqual(self.parser.test_size(u'21h'), 1)

    def test_cpp_28400(self):
        self.assertEqual(self.parser.test_size(u'22'), 1)

    def test_cpp_28410(self):
        self.assertEqual(self.parser.test_size(u'23'), 1)

    def test_cpp_28420(self):
        self.assertEqual(self.parser.test_size(u'24'), 1)

    def test_cpp_28430(self):
        self.assertEqual(self.parser.test_size(u'24h'), 1)

    def test_cpp_28440(self):
        self.assertEqual(self.parser.test_size(u'25'), 1)

    def test_cpp_28450(self):
        self.assertEqual(self.parser.test_size(u'255'), 1)

    def test_cpp_28460(self):
        self.assertEqual(self.parser.test_size(u'256'), 2)

    def test_cpp_28470(self):
        self.assertEqual(self.parser.test_size(u'256*3'), 2)

    def test_cpp_28480(self):
        self.assertEqual(self.parser.test_size(u'256+3'), 2)

    def test_cpp_28490(self):
        self.assertEqual(self.parser.test_size(u'256+3+65536'), 4)

    def test_cpp_28500(self):
        self.assertEqual(self.parser.test_size(u'26'), 1)

    def test_cpp_28510(self):
        self.assertEqual(self.parser.test_size(u'2Dh'), 1)

    def test_cpp_28520(self):
        self.assertEqual(self.parser.test_size(u'3'), 1)

    def test_cpp_28530(self):
        self.assertEqual(self.parser.test_size(u'3*4'), 1)

    def test_cpp_28540(self):
        self.assertEqual(self.parser.test_size(u'30'), 1)

    def test_cpp_28550(self):
        self.assertEqual(self.parser.test_size(u'303Bh'), 2)

    def test_cpp_28560(self):
        self.assertEqual(self.parser.test_size(u'30h'), 1)

    def test_cpp_28570(self):
        self.assertEqual(self.parser.test_size(u'31'), 1)

    def test_cpp_28580(self):
        self.assertEqual(self.parser.test_size(u'31h'), 1)

    def test_cpp_28590(self):
        self.assertEqual(self.parser.test_size(u'32'), 1)

    def test_cpp_28600(self):
        self.assertEqual(self.parser.test_size(u'320*200/4'), 2)

    def test_cpp_28610(self):
        self.assertEqual(self.parser.test_size(u'32432434h'), 4)

    def test_cpp_28620(self):
        self.assertEqual(self.parser.test_size(u'340128h'), 4)

    def test_cpp_28630(self):
        self.assertEqual(self.parser.test_size(u'35'), 1)

    def test_cpp_28640(self):
        self.assertEqual(self.parser.test_size(u'37'), 1)

    def test_cpp_28650(self):
        self.assertEqual(self.parser.test_size(u'39h'), 1)

    def test_cpp_28660(self):
        self.assertEqual(self.parser.test_size(u'3Ch'), 1)

    def test_cpp_28670(self):
        self.assertEqual(self.parser.test_size(u'3DAh'), 2)

    def test_cpp_28680(self):
        self.assertEqual(self.parser.test_size(u'3Eh'), 1)

    def test_cpp_28690(self):
        self.assertEqual(self.parser.test_size(u'3FEh'), 2)

    def test_cpp_28700(self):
        self.assertEqual(self.parser.test_size(u'3FFEh'), 2)

    def test_cpp_28710(self):
        self.assertEqual(self.parser.test_size(u'3FFFEh'), 4)

    def test_cpp_28720(self):
        self.assertEqual(self.parser.test_size(u'3FFFFEh'), 4)

    def test_cpp_28730(self):
        self.assertEqual(self.parser.test_size(u'3FFFFFEh'), 4)

    def test_cpp_28740(self):
        self.assertEqual(self.parser.test_size(u'3FFFFFFEh'), 4)

    def test_cpp_28750(self):
        self.assertEqual(self.parser.test_size(u'3FFFFFFFh'), 4)

    def test_cpp_28760(self):
        self.assertEqual(self.parser.test_size(u'3FFFFFFh'), 4)

    def test_cpp_28770(self):
        self.assertEqual(self.parser.test_size(u'3FFFFFh'), 4)

    def test_cpp_28780(self):
        self.assertEqual(self.parser.test_size(u'3FFFFh'), 4)

    def test_cpp_28790(self):
        self.assertEqual(self.parser.test_size(u'3FFFh'), 2)

    def test_cpp_28800(self):
        self.assertEqual(self.parser.test_size(u'3FFh'), 2)

    def test_cpp_28810(self):
        self.assertEqual(self.parser.test_size(u'3Fh'), 1)

    def test_cpp_28820(self):
        self.assertEqual(self.parser.test_size(u'3c8h'), 2)

    def test_cpp_28830(self):
        self.assertEqual(self.parser.test_size(u'3c9h'), 2)

    def test_cpp_28840(self):
        self.assertEqual(self.parser.test_size(u'3h'), 1)

    def test_cpp_28850(self):
        self.assertEqual(self.parser.test_size(u'4'), 1)

    def test_cpp_28860(self):
        self.assertEqual(self.parser.test_size(u'4+5*256'), 2)

    def test_cpp_28870(self):
        self.assertEqual(self.parser.test_size(u'4000000'), 4)

    def test_cpp_28880(self):
        self.assertEqual(self.parser.test_size(u'40h'), 1)

    def test_cpp_28890(self):
        self.assertEqual(self.parser.test_size(u'43210123h'), 4)

    def test_cpp_28900(self):
        self.assertEqual(self.parser.test_size(u'48h'), 1)

    def test_cpp_28910(self):
        self.assertEqual(self.parser.test_size(u'49h'), 1)

    def test_cpp_28920(self):
        self.assertEqual(self.parser.test_size(u'4Ah'), 1)

    def test_cpp_28930(self):
        self.assertEqual(self.parser.test_size(u'4Ch'), 1)

    def test_cpp_28940(self):
        self.assertEqual(self.parser.test_size(u'4ch'), 1)

    def test_cpp_28950(self):
        self.assertEqual(self.parser.test_size(u'5'), 1)

    def test_cpp_28960(self):
        self.assertEqual(self.parser.test_size(u'50'), 1)

    def test_cpp_28970(self):
        self.assertEqual(self.parser.test_size(u'501h'), 2)

    def test_cpp_28980(self):
        self.assertEqual(self.parser.test_size(u'511'), 2)

    def test_cpp_28990(self):
        self.assertEqual(self.parser.test_size(u'55'), 1)

    def test_cpp_29000(self):
        self.assertEqual(self.parser.test_size(u'56'), 1)

    def test_cpp_29010(self):
        self.assertEqual(self.parser.test_size(u'57'), 1)

    def test_cpp_29020(self):
        self.assertEqual(self.parser.test_size(u'6'), 1)

    def test_cpp_29030(self):
        self.assertEqual(self.parser.test_size(u'6*256+5'), 2)

    def test_cpp_29040(self):
        self.assertEqual(self.parser.test_size(u'60'), 1)

    def test_cpp_29050(self):
        self.assertEqual(self.parser.test_size(u'65324h'), 4)

    def test_cpp_29060(self):
        self.assertEqual(self.parser.test_size(u'65423456h'), 4)

    def test_cpp_29070(self):
        self.assertEqual(self.parser.test_size(u'6789ABCDh'), 4)

    def test_cpp_29080(self):
        self.assertEqual(self.parser.test_size(u'7'), 1)

    def test_cpp_29090(self):
        self.assertEqual(self.parser.test_size(u'7Eh'), 1)

    def test_cpp_29100(self):
        self.assertEqual(self.parser.test_size(u'7FEh'), 2)

    def test_cpp_29110(self):
        self.assertEqual(self.parser.test_size(u'7FFEh'), 2)

    def test_cpp_29120(self):
        self.assertEqual(self.parser.test_size(u'7FFFEh'), 4)

    def test_cpp_29130(self):
        self.assertEqual(self.parser.test_size(u'7FFFFEh'), 4)

    def test_cpp_29140(self):
        self.assertEqual(self.parser.test_size(u'7FFFFFEh'), 4)

    def test_cpp_29150(self):
        self.assertEqual(self.parser.test_size(u'7FFFFFFEh'), 4)

    def test_cpp_29160(self):
        self.assertEqual(self.parser.test_size(u'7FFFFFFFh'), 4)

    def test_cpp_29170(self):
        self.assertEqual(self.parser.test_size(u'7FFFFFFh'), 4)

    def test_cpp_29180(self):
        self.assertEqual(self.parser.test_size(u'7FFFFFh'), 4)

    def test_cpp_29190(self):
        self.assertEqual(self.parser.test_size(u'7FFFFh'), 4)

    def test_cpp_29200(self):
        self.assertEqual(self.parser.test_size(u'7FFFh'), 2)

    def test_cpp_29210(self):
        self.assertEqual(self.parser.test_size(u'7FFh'), 2)

    def test_cpp_29220(self):
        self.assertEqual(self.parser.test_size(u'7Fh'), 1)

    def test_cpp_29230(self):
        self.assertEqual(self.parser.test_size(u'8'), 1)

    def test_cpp_29240(self):
        self.assertEqual(self.parser.test_size(u'80000000h'), 4)

    def test_cpp_29250(self):
        self.assertEqual(self.parser.test_size(u'80000001h'), 4)

    def test_cpp_29260(self):
        self.assertEqual(self.parser.test_size(u'80008481h'), 4)

    def test_cpp_29270(self):
        self.assertEqual(self.parser.test_size(u'80008688h'), 4)

    def test_cpp_29280(self):
        self.assertEqual(self.parser.test_size(u'8000h'), 2)

    def test_cpp_29290(self):
        self.assertEqual(self.parser.test_size(u'801h'), 2)

    def test_cpp_29300(self):
        self.assertEqual(self.parser.test_size(u'80h'), 1)

    def test_cpp_29310(self):
        self.assertEqual(self.parser.test_size(u'81234567h'), 4)

    def test_cpp_29320(self):
        self.assertEqual(self.parser.test_size(u'81238567h'), 4)

    def test_cpp_29330(self):
        self.assertEqual(self.parser.test_size(u'812FADAh'), 4)

    def test_cpp_29340(self):
        self.assertEqual(self.parser.test_size(u'813F3421h'), 4)

    def test_cpp_29350(self):
        self.assertEqual(self.parser.test_size(u'81h'), 1)

    def test_cpp_29360(self):
        self.assertEqual(self.parser.test_size(u'82345679h'), 4)

    def test_cpp_29370(self):
        self.assertEqual(self.parser.test_size(u'8234A6F8h'), 4)

    def test_cpp_29380(self):
        self.assertEqual(self.parser.test_size(u'8345A1F2h'), 4)

    def test_cpp_29390(self):
        self.assertEqual(self.parser.test_size(u'8C5h'), 2)

    def test_cpp_29400(self):
        self.assertEqual(self.parser.test_size(u'8D5h'), 2)

    def test_cpp_29410(self):
        self.assertEqual(self.parser.test_size(u'9'), 1)

    def test_cpp_29420(self):
        self.assertEqual(self.parser.test_size(u'9ABCDEFh'), 4)

    def test_cpp_29430(self):
        self.assertEqual(self.parser.test_size(u'AL'), 1)

    def test_cpp_29440(self):
        self.assertEqual(self.parser.test_size(u'B'), 0)

    def test_cpp_29450(self):
        self.assertEqual(self.parser.test_size(u'CC'), 0)

    def test_cpp_29460(self):
        self.assertEqual(self.parser.test_size(u'DDD'), 0)

    def test_cpp_29470(self):
        self.assertEqual(self.parser.test_size(u'DX'), 2)

    def test_cpp_29480(self):
        self.assertEqual(self.parser.test_size(u'OFFSET ASCiI'), 2)

    def test_cpp_29490(self):
        self.assertEqual(self.parser.test_size(u'OFFSET AsCii'), 2)

    def test_cpp_29500(self):
        self.assertEqual(self.parser.test_size(u'TWO'), 0)

    def test_cpp_29510(self):
        self.assertEqual(self.parser.test_size(u'[a+1]'), 0)

    #def test_cpp_29520(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[a]')),0)

    def test_cpp_29530(self):
        self.assertEqual(self.parser.test_size(u'[cs:table+ax]'), 0)

    def test_cpp_29540(self):
        self.assertEqual(self.parser.test_size(u'[doublequote+4]'), 0)

    def test_cpp_29550(self):
        self.assertEqual(self.parser.test_size(u'[eax+4000h]'), 0)

    def test_cpp_29560(self):
        self.assertEqual(self.parser.test_size(u'[eax+40h]'), 0)

    def test_cpp_29570(self):
        self.assertEqual(self.parser.test_size(u'[eax+ecx+40h]'), 0)

    def test_cpp_29580(self):
        self.assertEqual(self.parser.test_size(u'[eax+ecx]'), 0)

    def test_cpp_29590(self):
        self.assertEqual(self.parser.test_size(u'[eax]'), 0)

    def test_cpp_29600(self):
        self.assertEqual(self.parser.test_size(u'[ebp+ecx_0]'), 0)

    def test_cpp_29610(self):
        self.assertEqual(self.parser.test_size(u'[ebp+ecx_vals]'), 0)

    def test_cpp_29620(self):
        self.assertEqual(self.parser.test_size(u'[ebp+edx_0]'), 0)

    def test_cpp_29630(self):
        self.assertEqual(self.parser.test_size(u'[ebp+i*4+ecx_vals]'), 0)

    def test_cpp_29640(self):
        self.assertEqual(self.parser.test_size(u'[ebp+i+table]'), 0)

    def test_cpp_29650(self):
        self.assertEqual(self.parser.test_size(u'[ebp+iflags]'), 0)

    def test_cpp_29660(self):
        self.assertEqual(self.parser.test_size(u'[ebp+op0]'), 0)

    def test_cpp_29670(self):
        self.assertEqual(self.parser.test_size(u'[ebp+op0h]'), 0)

    def test_cpp_29680(self):
        self.assertEqual(self.parser.test_size(u'[ebp+s0]'), 0)

    def test_cpp_29690(self):
        self.assertEqual(self.parser.test_size(u'[ebp+s1]'), 0)

    def test_cpp_29700(self):
        self.assertEqual(self.parser.test_size(u'[ebp+s2]'), 0)

    def test_cpp_29710(self):
        self.assertEqual(self.parser.test_size(u'[ebp+table]'), 0)

    def test_cpp_29720(self):
        self.assertEqual(self.parser.test_size(u'[ebp+var_1C]'), 0)

    def test_cpp_29730(self):
        self.assertEqual(self.parser.test_size(u'[ebp+var_20]'), 0)

    def test_cpp_29740(self):
        self.assertEqual(self.parser.test_size(u'[ebp+var_4]'), 0)

    def test_cpp_29750(self):
        self.assertEqual(self.parser.test_size(u'[ebx+4000h]'), 0)

    def test_cpp_29760(self):
        self.assertEqual(self.parser.test_size(u'[ebx+40h]'), 0)

    def test_cpp_29770(self):
        self.assertEqual(self.parser.test_size(u'[ebx+edx+4000h]'), 0)

    def test_cpp_29780(self):
        self.assertEqual(self.parser.test_size(u'[ebx+edx]'), 0)

    def test_cpp_29790(self):
        self.assertEqual(self.parser.test_size(u'[ebx]'), 0)

    def test_cpp_29800(self):
        self.assertEqual(self.parser.test_size(u'[ecx+4000h]'), 0)

    def test_cpp_29810(self):
        self.assertEqual(self.parser.test_size(u'[ecx+40h]'), 0)

    def test_cpp_29820(self):
        self.assertEqual(self.parser.test_size(u'[ecx+ecx*2+4000h]'), 0)

    def test_cpp_29830(self):
        self.assertEqual(self.parser.test_size(u'[ecx+ecx*2-0Ah]'), 0)

    def test_cpp_29840(self):
        self.assertEqual(self.parser.test_size(u'[ecx+ecx*2]'), 0)

    def test_cpp_29850(self):
        self.assertEqual(self.parser.test_size(u'[ecx+ecx]'), 0)

    def test_cpp_29860(self):
        self.assertEqual(self.parser.test_size(u'[ecx]'), 0)

    def test_cpp_29870(self):
        self.assertEqual(self.parser.test_size(u'[edi+1]'), 0)

    def test_cpp_29880(self):
        self.assertEqual(self.parser.test_size(u'[edi+4000h]'), 0)

    def test_cpp_29890(self):
        self.assertEqual(self.parser.test_size(u'[edi+40h]'), 0)

    def test_cpp_29900(self):
        self.assertEqual(self.parser.test_size(u'[edi+ecx]'), 0)

    def test_cpp_29910(self):
        self.assertEqual(self.parser.test_size(u'[edi]'), 0)

    def test_cpp_29920(self):
        self.assertEqual(self.parser.test_size(u'[edx+4000h]'), 0)

    def test_cpp_29930(self):
        self.assertEqual(self.parser.test_size(u'[edx+40h]'), 0)

    def test_cpp_29940(self):
        self.assertEqual(self.parser.test_size(u'[edx+ecx*4+4000h]'), 0)

    def test_cpp_29950(self):
        self.assertEqual(self.parser.test_size(u'[edx+ecx*4-0Ah]'), 0)

    def test_cpp_29960(self):
        self.assertEqual(self.parser.test_size(u'[edx+ecx*4]'), 0)

    def test_cpp_29970(self):
        self.assertEqual(self.parser.test_size(u'[edx+ecx]'), 0)

    def test_cpp_29980(self):
        self.assertEqual(self.parser.test_size(u'[edx]'), 0)

    def test_cpp_29990(self):
        self.assertEqual(self.parser.test_size(u'[esi+4000h]'), 0)

    def test_cpp_30000(self):
        self.assertEqual(self.parser.test_size(u'[esi+40h]'), 0)

    def test_cpp_30010(self):
        self.assertEqual(self.parser.test_size(u'[esi+ecx*8+4000h]'), 0)

    def test_cpp_30020(self):
        self.assertEqual(self.parser.test_size(u'[esi+ecx*8-0Ah]'), 0)

    def test_cpp_30030(self):
        self.assertEqual(self.parser.test_size(u'[esi+ecx*8]'), 0)

    def test_cpp_30040(self):
        self.assertEqual(self.parser.test_size(u'[esi+ecx]'), 0)

    def test_cpp_30050(self):
        self.assertEqual(self.parser.test_size(u'[esi]'), 0)

    def test_cpp_30060(self):
        self.assertEqual(self.parser.test_size(u'[esp+0Ch]'), 0)

    def test_cpp_30070(self):
        self.assertEqual(self.parser.test_size(u'[esp+10h]'), 0)

    def test_cpp_30080(self):
        self.assertEqual(self.parser.test_size(u'[esp+14h]'), 0)

    def test_cpp_30090(self):
        self.assertEqual(self.parser.test_size(u'[esp+18h]'), 0)

    def test_cpp_30100(self):
        self.assertEqual(self.parser.test_size(u'[esp+1Ch]'), 0)

    def test_cpp_30110(self):
        self.assertEqual(self.parser.test_size(u'[esp+4]'), 0)

    def test_cpp_30120(self):
        self.assertEqual(self.parser.test_size(u'[esp+8]'), 0)

    def test_cpp_30130(self):
        self.assertEqual(self.parser.test_size(u'[esp]'), 0)

    #def test_cpp_30140(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[g]')),0)

    #def test_cpp_30150(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[h2]')),0)

    def test_cpp_30160(self):
        self.assertEqual(self.parser.test_size(u'[i+1]'), 0)

    def test_cpp_30170(self):
        self.assertEqual(self.parser.test_size(u'[i+2]'), 0)

    def test_cpp_30180(self):
        self.assertEqual(self.parser.test_size(u'[i+3]'), 0)

    def test_cpp_30190(self):
        self.assertEqual(self.parser.test_size(u'[i+4]'), 0)

    def test_cpp_30200(self):
        self.assertEqual(self.parser.test_size(u'[i+56h]'), 0)

    def test_cpp_30210(self):
        self.assertEqual(self.parser.test_size(u'[i+5]'), 0)

    def test_cpp_30220(self):
        self.assertEqual(self.parser.test_size(u'[i-10h]'), 0)

    #def test_cpp_30230(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[load_handle]')),0)

    def test_cpp_30240(self):
        self.assertEqual(self.parser.test_size(u'[var+3]'), 0)

    def test_cpp_30250(self):
        self.assertEqual(self.parser.test_size(u'[var+4]'), 0)

    def test_cpp_30260(self):
        self.assertEqual(self.parser.test_size(u'[var-1]'), 0)

    def test_cpp_30270(self):
        self.assertEqual(self.parser.test_size(u'[var0+5]'), 0)

    def test_cpp_30280(self):
        self.assertEqual(self.parser.test_size(u'[var1+1]'), 0)

    #def test_cpp_30290(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var1]')),0)

    def test_cpp_30300(self):
        self.assertEqual(self.parser.test_size(u'[var2+2]'), 0)

    def test_cpp_30310(self):
        self.assertEqual(self.parser.test_size(u'[var2-1]'), 0)

    #def test_cpp_30320(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var2]')),0)

    #def test_cpp_30330(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'[var2]')),0)

    def test_cpp_30340(self):
        self.assertEqual(self.parser.test_size(u'[var3+3*4]'), 0)

    def test_cpp_30350(self):
        self.assertEqual(self.parser.test_size(u'[var3+ebp]'), 0)

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
        self.assertEqual(self.parser.test_size(u'ah'), 1)

    def test_cpp_30430(self):
        self.assertEqual(self.parser.test_size(u'al'), 1)

    def test_cpp_30440(self):
        self.assertEqual(self.parser.test_size(u'ax'), 2)

    #def test_cpp_30450(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'b')),1)

    #def test_cpp_30460(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'b')),2)

    #def test_cpp_30470(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'beginningdata')),1)

    def test_cpp_30480(self):
        self.assertEqual(self.parser.test_size(u'bh'), 1)

    def test_cpp_30490(self):
        self.assertEqual(self.parser.test_size(u'bl'), 1)

    def test_cpp_30500(self):
        self.assertEqual(self.parser.test_size(u'bp'), 2)

    #def test_cpp_30510(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'buffer')),1)

    def test_cpp_30520(self):
        self.assertEqual(self.parser.test_size(u'bx'), 2)

    def test_cpp_30530(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [a]'), 1)

    def test_cpp_30540(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [ebp+var_20]'), 1)

    def test_cpp_30550(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [edi+1]'), 1)

    def test_cpp_30560(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [edi+7]'), 1)

    def test_cpp_30570(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [esi]'), 1)

    def test_cpp_30580(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [h2]'), 1)

    def test_cpp_30590(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [h]'), 1)

    def test_cpp_30600(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [testOVerlap+1]'), 1)

    def test_cpp_30610(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [var1+1]'), 1)

    def test_cpp_30620(self):
        self.assertEqual(self.parser.test_size(u'byte ptr [var1+2]'), 1)

    def test_cpp_30630(self):
        self.assertEqual(self.parser.test_size(u'byte ptr dl'), 1)

    def test_cpp_30640(self):
        self.assertEqual(self.parser.test_size(u'byte ptr ds:[0]'), 1)

    def test_cpp_30650(self):
        self.assertEqual(self.parser.test_size(u'byte ptr es:[0]'), 1)

    #def test_cpp_30660(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'c')),4)

    def test_cpp_30670(self):
        self.assertEqual(self.parser.test_size(u'ch'), 1)

    def test_cpp_30680(self):
        self.assertEqual(self.parser.test_size(u'cl'), 1)

    def test_cpp_30690(self):
        self.assertEqual(self.parser.test_size(u'cx'), 2)

    def test_cpp_30700(self):
        self.assertEqual(self.parser.test_size(u'di'), 2)

    def test_cpp_30710(self):
        self.assertEqual(self.parser.test_size(u'dl'), 1)

    def test_cpp_30720(self):
        self.assertEqual(self.parser.test_size(u'ds'), 2)

    def test_cpp_30730(self):
        self.assertEqual(self.parser.test_size(u'ds:0[eax*2]'), 0)

    def test_cpp_30740(self):
        self.assertEqual(self.parser.test_size(u'ds:0[ebx*4]'), 0)

    def test_cpp_30750(self):
        self.assertEqual(self.parser.test_size(u'ds:0[ecx*8]'), 0)

    def test_cpp_30760(self):
        self.assertEqual(self.parser.test_size(u'ds:40h[eax*2]'), 0)

    def test_cpp_30770(self):
        self.assertEqual(self.parser.test_size(u'ds:40h[ebx*4]'), 0)

    def test_cpp_30780(self):
        self.assertEqual(self.parser.test_size(u'ds:40h[ecx*8]'), 0)

    def test_cpp_30790(self):
        self.assertEqual(self.parser.test_size(u'ds:[edi]'), 0)

    #def test_cpp_30800(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'ds:byte_41411F[eax]')),1)

    def test_cpp_30810(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [ebp+var_20+4]'), 4)

    def test_cpp_30820(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [ebp+var_20]'), 4)

    def test_cpp_30830(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [ebx-4]'), 4)

    def test_cpp_30840(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp+0Ch]'), 4)

    def test_cpp_30850(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp+10h]'), 4)

    def test_cpp_30860(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp+14h]'), 4)

    def test_cpp_30870(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp+1Ch]'), 4)

    def test_cpp_30880(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp+4]'), 4)

    def test_cpp_30890(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp+8]'), 4)

    def test_cpp_30900(self):
        self.assertEqual(self.parser.test_size(u'dword ptr [esp]'), 4)

    def test_cpp_30910(self):
        self.assertEqual(self.parser.test_size(u'dword ptr buffer'), 4)

    def test_cpp_30920(self):
        self.assertEqual(self.parser.test_size(u'dword ptr es:[0]'), 4)

    def test_cpp_30930(self):
        self.assertEqual(self.parser.test_size(u'dword ptr es:[20*320+160]'), 4)

    def test_cpp_30940(self):
        self.assertEqual(self.parser.test_size(u'dword ptr var4'), 4)

    def test_cpp_30950(self):
        self.assertEqual(self.parser.test_size(u'dx'), 2)

    def test_cpp_30960(self):
        self.assertEqual(self.parser.test_size(u'eax'), 4)

    def test_cpp_30970(self):
        self.assertEqual(self.parser.test_size(u'eax_0'), 0)

    def test_cpp_30980(self):
        self.assertEqual(self.parser.test_size(u'ebp'), 4)

    def test_cpp_30990(self):
        self.assertEqual(self.parser.test_size(u'ebx'), 4)

    def test_cpp_31000(self):
        self.assertEqual(self.parser.test_size(u'ecx'), 4)

    def test_cpp_31010(self):
        self.assertEqual(self.parser.test_size(u'ecx_0'), 0)

    def test_cpp_31020(self):
        self.assertEqual(self.parser.test_size(u'ecx_0_0'), 0)

    def test_cpp_31030(self):
        self.assertEqual(self.parser.test_size(u'edi'), 4)

    def test_cpp_31040(self):
        self.assertEqual(self.parser.test_size(u'edi_0'), 0)

    def test_cpp_31050(self):
        self.assertEqual(self.parser.test_size(u'edx'), 4)

    def test_cpp_31060(self):
        self.assertEqual(self.parser.test_size(u'edx_0_0'), 0)

    def test_cpp_31070(self):
        self.assertEqual(self.parser.test_size(u'eflags'), 0)

    #def test_cpp_31080(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'enddata')),1)

    def test_cpp_31090(self):
        self.assertEqual(self.parser.test_size(u'es'), 2)

    def test_cpp_31100(self):
        self.assertEqual(self.parser.test_size(u'esi'), 4)

    def test_cpp_31110(self):
        self.assertEqual(self.parser.test_size(u'esi_0'), 0)

    def test_cpp_31120(self):
        self.assertEqual(self.parser.test_size(u'esp'), 4)

    #def test_cpp_31130(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'fileName')),1)

    def test_cpp_31140(self):
        self.assertEqual(self.parser.test_size(u'flags'), 0)

    def test_cpp_31150(self):
        self.assertEqual(self.parser.test_size(u'fs'), 2)

    #def test_cpp_31160(self):
        # self.assertEqual(self.cpp.get_size(self.parser.test_size(u'g')),4)

    def test_cpp_31170(self):
        self.assertEqual(self.parser.test_size(u'i'), 0)

    def test_cpp_31180(self):
        self.assertEqual(self.parser.test_size(u'large ds:4000h'), 4)

    def test_cpp_31190(self):
        self.assertEqual(self.parser.test_size(u'offset _msg'), 2)

    def test_cpp_31200(self):
        self.assertEqual(self.parser.test_size(u'offset _test_btc'), 2)

    def test_cpp_31210(self):
        self.assertEqual(self.parser.test_size(u'offset pal_jeu'), 2)

    def test_cpp_31220(self):
        self.assertEqual(self.parser.test_size(u'offset str1'), 2)

    def test_cpp_31230(self):
        self.assertEqual(self.parser.test_size(u'offset str2'), 2)

    def test_cpp_31240(self):
        self.assertEqual(self.parser.test_size(u'offset str3'), 2)

    def test_cpp_31250(self):
        self.assertEqual(self.parser.test_size(u'offset str_buffer+810h'), 2)

    def test_cpp_31260(self):
        self.assertEqual(self.parser.test_size(u'offset testOVerlap'), 2)

    def test_cpp_31270(self):
        self.assertEqual(self.parser.test_size(u'offset unk_40E008'), 2)

    def test_cpp_31280(self):
        self.assertEqual(self.parser.test_size(u'offset unk_40F064'), 2)

    def test_cpp_31290(self):
        self.assertEqual(self.parser.test_size(u'offset var1'), 2)

    def test_cpp_31300(self):
        self.assertEqual(self.parser.test_size(u'offset var1+1'), 2)

    def test_cpp_31310(self):
        self.assertEqual(self.parser.test_size(u'offset var2'), 2)

    def test_cpp_31320(self):
        self.assertEqual(self.parser.test_size(u'offset var3'), 2)

    def test_cpp_31330(self):
        self.assertEqual(self.parser.test_size(u'offset var3+4'), 2)

    def test_cpp_31340(self):
        self.assertEqual(self.parser.test_size(u'offset var4'), 2)

    def test_cpp_31350(self):
        self.assertEqual(self.parser.test_size(u'offset var4+1'), 2)

    def test_cpp_31360(self):
        self.assertEqual(self.parser.test_size(u'offset var4+4'), 2)

    def test_cpp_31370(self):
        self.assertEqual(self.parser.test_size(u'op0'), 0)

    def test_cpp_31380(self):
        self.assertEqual(self.parser.test_size(u'op1'), 0)

    def test_cpp_31390(self):
        self.assertEqual(self.parser.test_size(u'printf'), 0)

    def test_cpp_31400(self):
        self.assertEqual(self.parser.test_size(u'r'), 0)

    def test_cpp_31410(self):
        self.assertEqual(self.parser.test_size(u'res'), 0)

    def test_cpp_31420(self):
        self.assertEqual(self.parser.test_size(u'resh'), 0)

    def test_cpp_31430(self):
        self.assertEqual(self.parser.test_size(u'resz'), 0)

    def test_cpp_31440(self):
        self.assertEqual(self.parser.test_size(u'rh'), 0)

    def test_cpp_31450(self):
        self.assertEqual(self.parser.test_size(u's0_0'), 0)

    def test_cpp_31460(self):
        self.assertEqual(self.parser.test_size(u's1_0'), 0)

    def test_cpp_31470(self):
        self.assertEqual(self.parser.test_size(u'si'), 2)

    def test_cpp_31480(self):
        self.assertEqual(self.parser.test_size(u't'), 0)

    def test_cpp_31490(self):
        self.assertEqual(self.parser.test_size(u'taille_moire'), 0)

    def test_cpp_31500(self):
        self.assertEqual(self.parser.test_size(u'teST2'), 0)

    def test_cpp_31500(self):
        self.assertEqual(self.parser.test_size(u'teST2'), 0)

    def test_cpp_31510(self):
        self.assertEqual(self.parser.test_size(u'fs: 8'), 0)

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
        self.assertEqual(self.parser.test_size(u'var3+ebp'), 4)

    #def test_cpp_31600(self):
    #   self.assertEqual(self.cpp.get_size(self.parser.test_size(u'var5')),1)

    def test_cpp_31610(self):
        self.assertEqual(self.parser.test_size(u'word ptr [d]'), 2)

    def test_cpp_31620(self):
        self.assertEqual(self.parser.test_size(u'word ptr [e]'), 2)

    def test_cpp_31630(self):
        self.assertEqual(self.parser.test_size(u'word ptr [ebp+var_20]'), 2)

    def test_cpp_31640(self):
        self.assertEqual(self.parser.test_size(u'word ptr [var5+2]'), 2)

    def test_cpp_31650(self):
        self.assertEqual(self.parser.test_size(u'word ptr var5'), 2)
    """

    def test_cpp_31660(self):
        assert self.parser.is_register(expr='_data') == 0

    def test_cpp_31670(self):
        assert self.parser.is_register(expr='offset var1') == 0

    def test_cpp_31680(self):
        assert self.parser.is_register(expr='var1') == 0

    def test_cpp_31690(self):
        assert self.parser.is_register(expr='cl') == 1

    def test_cpp_31700(self):
        assert self.parser.is_register(expr='[edi+1]') == 0

    def test_cpp_31710(self):
        assert self.parser.is_register(expr='[doublequote+4]') == 0

    def test_cpp_31720(self):
        assert self.parser.is_register(expr='dl') == 1

    def test_cpp_31730(self):
        assert self.parser.is_register(expr='-12') == 0

    def test_cpp_31740(self):
        assert self.parser.is_register(expr='teST2') == 0

    def test_cpp_31750(self):
        assert self.parser.is_register(expr="'d'") == 0

    def test_cpp_31760(self):
        assert self.parser.is_register(expr='dx') == 2

    def test_cpp_31770(self):
        assert self.parser.is_register(expr='esi') == 4

    def test_cpp_31780(self):
        assert self.parser.is_register(expr='enddata') == 0

    def test_cpp_31790(self):
        assert self.parser.is_register(expr="'Z' - 'A' +1") == 0

    def test_cpp_31800(self):
        assert self.parser.is_register(expr='beginningdata') == 0

    def test_cpp_31810(self):
        assert self.parser.is_register(expr='al') == 1

    def test_cpp_31820(self):
        assert self.parser.is_register(expr='ebx') == 4

    def test_cpp_31830(self):
        assert self.parser.is_register(expr='edi') == 4

    def test_cpp_31840(self):
        assert self.parser.is_register(expr='ds') == 2

    def test_cpp_31850(self):
        assert self.parser.is_register(expr='eax') == 4

    def test_cpp_31860(self):
        assert self.cpp.convert_asm_number_into_c(expr="'Z' - 'A' +1") == "'Z' - 'A' +1"

    def test_cpp_31870(self):
        assert self.cpp.convert_asm_number_into_c(expr='((((2030080+64000*26)/4096)+1)*4096)-1') == '((((2030080+64000*26)/4096)+1)*4096)-1'

    def test_cpp_31880(self):
        assert self.cpp.convert_asm_number_into_c(expr='(00+38*3)*320+1/2+33*(3-1)') == '(00+38*3)*320+1/2+33*(3-1)'

    def test_cpp_31890(self):
        assert self.cpp.convert_asm_number_into_c(expr='(1024*10/16)+5') == '(1024*10/16)+5'

    def test_cpp_31900(self):
        assert self.cpp.convert_asm_number_into_c(expr='(1024*10/16)-1') == '(1024*10/16)-1'

    def test_cpp_31910(self):
        assert self.cpp.convert_asm_number_into_c(expr='+0x40') == '+0x40'

    def test_cpp_31920(self):
        assert self.cpp.convert_asm_number_into_c(expr='+0x4000') == '+0x4000'

    def test_cpp_31930(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx') == '+ecx'

    def test_cpp_31940(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx*2') == '+ecx*2'

    def test_cpp_31950(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx*2+0x4000') == '+ecx*2+0x4000'

    def test_cpp_31960(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx*2-0x0A') == '+ecx*2-0x0A'

    def test_cpp_31970(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx*4') == '+ecx*4'

    def test_cpp_31980(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx*4+0x4000') == '+ecx*4+0x4000'

    def test_cpp_31990(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx*4-0x0A') == '+ecx*4-0x0A'

    def test_cpp_32000(self):
        assert self.cpp.convert_asm_number_into_c(expr='+ecx+0x40') == '+ecx+0x40'

    def test_cpp_32010(self):
        assert self.cpp.convert_asm_number_into_c(expr='+edx') == '+edx'

    def test_cpp_32020(self):
        assert self.cpp.convert_asm_number_into_c(expr='+edx+0x4000') == '+edx+0x4000'

    def test_cpp_32030(self):
        assert self.cpp.convert_asm_number_into_c(expr='-0x108') == '-0x108'

    def test_cpp_32040(self):
        assert self.cpp.convert_asm_number_into_c(expr='-0x1C') == '-0x1C'

    def test_cpp_32050(self):
        assert self.cpp.convert_asm_number_into_c(expr='-0x20') == '-0x20'

    def test_cpp_32060(self):
        assert self.cpp.convert_asm_number_into_c(expr='-0x28') == '-0x28'

    def test_cpp_32070(self):
        assert self.cpp.convert_asm_number_into_c(expr='-0x2C') == '-0x2C'

    def test_cpp_32080(self):
        assert self.cpp.convert_asm_number_into_c(expr='-1') == '-1'

    def test_cpp_32090(self):
        assert self.cpp.convert_asm_number_into_c(expr='-1-(-2+3)') == '-1-(-2+3)'

    def test_cpp_32100(self):
        assert self.cpp.convert_asm_number_into_c(expr='-108h') == '-0x108'

    def test_cpp_32110(self):
        assert self.cpp.convert_asm_number_into_c(expr='-12') == '-12'

    def test_cpp_32130(self):
        assert self.cpp.convert_asm_number_into_c(expr='-1Ch') == '-0x1C'

    def test_cpp_32140(self):
        assert self.cpp.convert_asm_number_into_c(expr='-2') == '-2'

    def test_cpp_32170(self):
        assert self.cpp.convert_asm_number_into_c(expr='-2Ch') == '-0x2C'

    def test_cpp_32180(self):
        assert self.cpp.convert_asm_number_into_c(expr='-2Dh') == '-0x2D'

    def test_cpp_32190(self):
        assert self.cpp.convert_asm_number_into_c(expr='-4') == '-4'

    def test_cpp_32220(self):
        assert self.cpp.convert_asm_number_into_c(expr='0') == '0'

    def test_cpp_32230(self):
        assert self.cpp.convert_asm_number_into_c(expr='0002h') == '0x0002'

    def test_cpp_32240(self):
        assert self.cpp.convert_asm_number_into_c(expr='0007') == '0007'

    def test_cpp_32250(self):
        assert self.cpp.convert_asm_number_into_c(expr='000f3h') == '0x000f3'

    def test_cpp_32260(self):
        assert self.cpp.convert_asm_number_into_c(expr='000ff00ffh') == '0x000ff00ff'

    def test_cpp_32270(self):
        assert self.cpp.convert_asm_number_into_c(expr='001111111B') == '0x7f'

    def test_cpp_32280(self):
        assert self.cpp.convert_asm_number_into_c(expr='00fffh') == '0x00fff'

    def test_cpp_32290(self):
        assert self.cpp.convert_asm_number_into_c(expr='00h') == '0x00'

    def test_cpp_32300(self):
        assert self.cpp.convert_asm_number_into_c(expr='0100b') == '0x4'

    def test_cpp_32310(self):
        assert self.cpp.convert_asm_number_into_c(expr='01010101010101010b') == '0xaaaa'

    def test_cpp_32320(self):
        assert self.cpp.convert_asm_number_into_c(expr='0101010101010101b') == '0x5555'

    def test_cpp_32330(self):
        assert self.cpp.convert_asm_number_into_c(expr='0101b') == '0x5'

    def test_cpp_32340(self):
        assert self.cpp.convert_asm_number_into_c(expr='010B') == '0x2'

    def test_cpp_32350(self):
        assert self.cpp.convert_asm_number_into_c(expr='011111100B') == '0xfc'

    def test_cpp_32360(self):
        assert self.cpp.convert_asm_number_into_c(expr='011111111111111111111111111111111b') == '0xffffffff'

    def test_cpp_32370(self):
        assert self.cpp.convert_asm_number_into_c(expr='01111111111111111b') == '0xffff'

    def test_cpp_32380(self):
        assert self.cpp.convert_asm_number_into_c(expr='011111111B') == '0xff'

    def test_cpp_32390(self):
        assert self.cpp.convert_asm_number_into_c(expr='012345678h') == '0x012345678'

    def test_cpp_32400(self):
        assert self.cpp.convert_asm_number_into_c(expr='01B') == '0x1'

    def test_cpp_32410(self):
        assert self.cpp.convert_asm_number_into_c(expr='01h') == '0x01'

    def test_cpp_32420(self):
        assert self.cpp.convert_asm_number_into_c(expr='02h') == '0x02'

    def test_cpp_32430(self):
        assert self.cpp.convert_asm_number_into_c(expr='03dh') == '0x03d'

    def test_cpp_32440(self):
        assert self.cpp.convert_asm_number_into_c(expr='03eh') == '0x03e'

    def test_cpp_32450(self):
        assert self.cpp.convert_asm_number_into_c(expr='03fh') == '0x03f'

    def test_cpp_32470(self):
        assert self.cpp.convert_asm_number_into_c(expr='077123456h') == '0x077123456'

    def test_cpp_32480(self):
        assert self.cpp.convert_asm_number_into_c(expr='077aaFF00h') == '0x077aaFF00'

    def test_cpp_32490(self):
        assert self.cpp.convert_asm_number_into_c(expr='08h') == '0x08'

    def test_cpp_32500(self):
        assert self.cpp.convert_asm_number_into_c(expr='0B') == '0x0'

    def test_cpp_32510(self):
        assert self.cpp.convert_asm_number_into_c(expr='0BC6058h') == '0x0BC6058'

    def test_cpp_32520(self):
        assert self.cpp.convert_asm_number_into_c(expr='0Ch') == '0x0C'

    def test_cpp_32530(self):
        assert self.cpp.convert_asm_number_into_c(expr='0D5h') == '0x0D5'

    def test_cpp_32540(self):
        assert self.cpp.convert_asm_number_into_c(expr='0Eh') == '0x0E'

    def test_cpp_32550(self):
        assert self.cpp.convert_asm_number_into_c(expr='0F7h') == '0x0F7'

    def test_cpp_32560(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FBCA7654h') == '0x0FBCA7654'

    def test_cpp_32570(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FBCA7h') == '0x0FBCA7'

    def test_cpp_32580(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FEh') == '0x0FE'

    def test_cpp_32590(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFEh') == '0x0FFE'

    def test_cpp_32600(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFC70F9h') == '0x0FFFC70F9'

    def test_cpp_32610(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFE0080h') == '0x0FFFE0080'

    def test_cpp_32620(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFEDCBFh') == '0x0FFFEDCBF'

    def test_cpp_32630(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFEFDFCh') == '0x0FFFEFDFC'

    def test_cpp_32640(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFEh') == '0x0FFFE'

    def test_cpp_32650(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFF7FFFh') == '0x0FFFF7FFF'

    def test_cpp_32660(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFA549h') == '0x0FFFFA549'

    def test_cpp_32670(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFEh') == '0x0FFFFE'

    def test_cpp_32680(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFED4h') == '0x0FFFFFED4'

    def test_cpp_32690(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFEh') == '0x0FFFFFE'

    def test_cpp_32700(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFD3h') == '0x0FFFFFFD3'

    def test_cpp_32710(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFECh') == '0x0FFFFFFEC'

    def test_cpp_32720(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFEh') == '0x0FFFFFFE'

    def test_cpp_32730(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFF0h') == '0x0FFFFFFF0'

    def test_cpp_32740(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFF7h') == '0x0FFFFFFF7'

    def test_cpp_32750(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFFAh') == '0x0FFFFFFFA'

    def test_cpp_32760(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFFh') == '0x0FFFFFFF'

    def test_cpp_32770(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFFh') == '0x0FFFFFF'

    def test_cpp_32780(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFFh') == '0x0FFFFF'

    def test_cpp_32790(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFFh') == '0x0FFFF'

    def test_cpp_32800(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFFh') == '0x0FFF'

    def test_cpp_32810(self):
        assert self.cpp.convert_asm_number_into_c(expr='0FFh') == '0x0FF'

    def test_cpp_32820(self):
        assert self.cpp.convert_asm_number_into_c(expr='0Fh') == '0x0F'

    def test_cpp_32830(self):
        assert self.cpp.convert_asm_number_into_c(expr='0a0000h') == '0x0a0000'

    def test_cpp_32840(self):
        assert self.cpp.convert_asm_number_into_c(expr='0a000h') == '0x0a000'

    def test_cpp_32850(self):
        assert self.cpp.convert_asm_number_into_c(expr='0aabbccddh') == '0x0aabbccdd'

    def test_cpp_32860(self):
        assert self.cpp.convert_asm_number_into_c(expr='0abcdef77h') == '0x0abcdef77'

    def test_cpp_32870(self):
        assert self.cpp.convert_asm_number_into_c(expr='0af222h') == '0x0af222'

    def test_cpp_32880(self):
        assert self.cpp.convert_asm_number_into_c(expr='0cch') == '0x0cc'

    def test_cpp_32890(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ddh') == '0x0dd'

    def test_cpp_32900(self):
        assert self.cpp.convert_asm_number_into_c(expr='0df01h') == '0x0df01'

    def test_cpp_32910(self):
        assert self.cpp.convert_asm_number_into_c(expr='0dff1h') == '0x0dff1'

    def test_cpp_32920(self):
        assert self.cpp.convert_asm_number_into_c(expr='0f0ffh') == '0x0f0ff'

    def test_cpp_32930(self):
        assert self.cpp.convert_asm_number_into_c(expr='0f0h') == '0x0f0'

    def test_cpp_32940(self):
        assert self.cpp.convert_asm_number_into_c(expr='0f222h') == '0x0f222'

    def test_cpp_32950(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffff0003h') == '0x0ffff0003'

    def test_cpp_32960(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffff00f3h') == '0x0ffff00f3'

    def test_cpp_32970(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffff01ffh') == '0x0ffff01ff'

    def test_cpp_32980(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffffff00h') == '0x0ffffff00'

    def test_cpp_32990(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffffff03h') == '0x0ffffff03'

    def test_cpp_33000(self):
        assert self.cpp.convert_asm_number_into_c(expr='0fffffff3h') == '0x0fffffff3'

    def test_cpp_33010(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffffffffh') == '0x0ffffffff'

    def test_cpp_33020(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffffh') == '0x0ffff'

    def test_cpp_33030(self):
        assert self.cpp.convert_asm_number_into_c(expr='0ffh') == '0x0ff'

    def test_cpp_33040(self):
        assert self.cpp.convert_asm_number_into_c(expr='0x0C') == '0x0C'

    def test_cpp_33050(self):
        assert self.cpp.convert_asm_number_into_c(expr='0x10') == '0x10'

    def test_cpp_33060(self):
        assert self.cpp.convert_asm_number_into_c(expr='0x14') == '0x14'

    def test_cpp_33070(self):
        assert self.cpp.convert_asm_number_into_c(expr='1') == '1'

    def test_cpp_33080(self):
        assert self.cpp.convert_asm_number_into_c(expr='10') == '10'

    def test_cpp_33090(self):
        assert self.cpp.convert_asm_number_into_c(expr='10000h') == '0x10000'

    def test_cpp_33100(self):
        assert self.cpp.convert_asm_number_into_c(expr='1000h') == '0x1000'

    def test_cpp_33110(self):
        assert self.cpp.convert_asm_number_into_c(expr='100h') == '0x100'

    def test_cpp_33120(self):
        assert self.cpp.convert_asm_number_into_c(expr='1024*10/16') == '1024*10/16'

    def test_cpp_33130(self):
        assert self.cpp.convert_asm_number_into_c(expr='1024*1024') == '1024*1024'

    def test_cpp_33140(self):
        assert self.cpp.convert_asm_number_into_c(expr='10B') == '0x2'

    def test_cpp_33150(self):
        assert self.cpp.convert_asm_number_into_c(expr='10h') == '0x10'

    def test_cpp_33160(self):
        assert self.cpp.convert_asm_number_into_c(expr='11') == '11'

    def test_cpp_33170(self):
        assert self.cpp.convert_asm_number_into_c(expr='111') == '111'

    def test_cpp_33180(self):
        assert self.cpp.convert_asm_number_into_c(expr='114h') == '0x114'

    def test_cpp_33190(self):
        assert self.cpp.convert_asm_number_into_c(expr='11h') == '0x11'

    def test_cpp_33200(self):
        assert self.cpp.convert_asm_number_into_c(expr='12') == '12'

    def test_cpp_33210(self):
        assert self.cpp.convert_asm_number_into_c(expr='12340004h') == '0x12340004'

    def test_cpp_33220(self):
        assert self.cpp.convert_asm_number_into_c(expr='1234001Dh') == '0x1234001D'

    def test_cpp_33230(self):
        assert self.cpp.convert_asm_number_into_c(expr='12341h') == '0x12341'

    def test_cpp_33240(self):
        assert self.cpp.convert_asm_number_into_c(expr='12343h') == '0x12343'

    def test_cpp_33250(self):
        assert self.cpp.convert_asm_number_into_c(expr='12345') == '12345'

    def test_cpp_33260(self):
        assert self.cpp.convert_asm_number_into_c(expr='1234561Dh') == '0x1234561D'

    def test_cpp_33270(self):
        assert self.cpp.convert_asm_number_into_c(expr='12345678h') == '0x12345678'

    def test_cpp_33280(self):
        assert self.cpp.convert_asm_number_into_c(expr='12345h') == '0x12345'

    def test_cpp_33290(self):
        assert self.cpp.convert_asm_number_into_c(expr='12347F7Fh') == '0x12347F7F'

    def test_cpp_33300(self):
        assert self.cpp.convert_asm_number_into_c(expr='12347FFFh') == '0x12347FFF'

    def test_cpp_33310(self):
        assert self.cpp.convert_asm_number_into_c(expr='12348000h') == '0x12348000'

    def test_cpp_33320(self):
        assert self.cpp.convert_asm_number_into_c(expr='12348080h') == '0x12348080'

    def test_cpp_33330(self):
        assert self.cpp.convert_asm_number_into_c(expr='1234h') == '0x1234'

    def test_cpp_33340(self):
        assert self.cpp.convert_asm_number_into_c(expr='127Eh') == '0x127E'

    def test_cpp_33350(self):
        assert self.cpp.convert_asm_number_into_c(expr='12Ch') == '0x12C'

    def test_cpp_33360(self):
        assert self.cpp.convert_asm_number_into_c(expr='13') == '13'

    def test_cpp_33370(self):
        assert self.cpp.convert_asm_number_into_c(expr='132') == '132'

    def test_cpp_33380(self):
        assert self.cpp.convert_asm_number_into_c(expr='133') == '133'

    def test_cpp_33390(self):
        assert self.cpp.convert_asm_number_into_c(expr='13h') == '0x13'

    def test_cpp_33400(self):
        assert self.cpp.convert_asm_number_into_c(expr='14') == '14'

    def test_cpp_33410(self):
        assert self.cpp.convert_asm_number_into_c(expr='14*320') == '14*320'

    def test_cpp_33420(self):
        assert self.cpp.convert_asm_number_into_c(expr='14h') == '0x14'

    def test_cpp_33430(self):
        assert self.cpp.convert_asm_number_into_c(expr='15') == '15'

    def test_cpp_33440(self):
        assert self.cpp.convert_asm_number_into_c(expr='1500') == '1500'

    def test_cpp_33450(self):
        assert self.cpp.convert_asm_number_into_c(expr='16') == '16'

    def test_cpp_33460(self):
        assert self.cpp.convert_asm_number_into_c(expr='17') == '17'

    def test_cpp_33470(self):
        assert self.cpp.convert_asm_number_into_c(expr='17h') == '0x17'

    def test_cpp_33480(self):
        assert self.cpp.convert_asm_number_into_c(expr='18') == '18'

    def test_cpp_33490(self):
        assert self.cpp.convert_asm_number_into_c(expr='18h') == '0x18'

    def test_cpp_33500(self):
        assert self.cpp.convert_asm_number_into_c(expr='19') == '19'

    def test_cpp_33510(self):
        assert self.cpp.convert_asm_number_into_c(expr='192') == '192'

    def test_cpp_33520(self):
        assert self.cpp.convert_asm_number_into_c(expr='193') == '193'

    def test_cpp_33530(self):
        assert self.cpp.convert_asm_number_into_c(expr='1Ch') == '0x1C'

    def test_cpp_33540(self):
        assert self.cpp.convert_asm_number_into_c(expr='1Eh') == '0x1E'

    def test_cpp_33550(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FEh') == '0x1FE'

    def test_cpp_33560(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FF7Fh') == '0x1FF7F'

    def test_cpp_33570(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FF80h') == '0x1FF80'

    def test_cpp_33580(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FF81h') == '0x1FF81'

    def test_cpp_33590(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFEh') == '0x1FFE'

    def test_cpp_33600(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFEh') == '0x1FFFE'

    def test_cpp_33610(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFEh') == '0x1FFFFE'

    def test_cpp_33620(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFFEh') == '0x1FFFFFE'

    def test_cpp_33630(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFFFEh') == '0x1FFFFFFE'

    def test_cpp_33640(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFFFFh') == '0x1FFFFFFF'

    def test_cpp_33650(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFFFh') == '0x1FFFFFF'

    def test_cpp_33660(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFFh') == '0x1FFFFF'

    def test_cpp_33670(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFFh') == '0x1FFFF'

    def test_cpp_33680(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFFh') == '0x1FFF'

    def test_cpp_33690(self):
        assert self.cpp.convert_asm_number_into_c(expr='1FFh') == '0x1FF'

    def test_cpp_33700(self):
        assert self.cpp.convert_asm_number_into_c(expr='1Fh') == '0x1F'

    def test_cpp_33710(self):
        assert self.cpp.convert_asm_number_into_c(expr='2') == '2'

    def test_cpp_33720(self):
        assert self.cpp.convert_asm_number_into_c(expr='20') == '20'

    def test_cpp_33730(self):
        assert self.cpp.convert_asm_number_into_c(expr='20000h') == '0x20000'

    def test_cpp_33740(self):
        assert self.cpp.convert_asm_number_into_c(expr='20h') == '0x20'

    def test_cpp_33750(self):
        assert self.cpp.convert_asm_number_into_c(expr='21') == '21'

    def test_cpp_33760(self):
        assert self.cpp.convert_asm_number_into_c(expr='21AD3D34h') == '0x21AD3D34'

    def test_cpp_33770(self):
        assert self.cpp.convert_asm_number_into_c(expr='21h') == '0x21'

    def test_cpp_33780(self):
        assert self.cpp.convert_asm_number_into_c(expr='22') == '22'

    def test_cpp_33790(self):
        assert self.cpp.convert_asm_number_into_c(expr='23') == '23'

    def test_cpp_33800(self):
        assert self.cpp.convert_asm_number_into_c(expr='24') == '24'

    def test_cpp_33810(self):
        assert self.cpp.convert_asm_number_into_c(expr='24h') == '0x24'

    def test_cpp_33820(self):
        assert self.cpp.convert_asm_number_into_c(expr='25') == '25'

    def test_cpp_33830(self):
        assert self.cpp.convert_asm_number_into_c(expr='255') == '255'

    def test_cpp_33840(self):
        assert self.cpp.convert_asm_number_into_c(expr='256') == '256'

    def test_cpp_33850(self):
        assert self.cpp.convert_asm_number_into_c(expr='256*3') == '256*3'

    def test_cpp_33860(self):
        assert self.cpp.convert_asm_number_into_c(expr='256+3') == '256+3'

    def test_cpp_33870(self):
        assert self.cpp.convert_asm_number_into_c(expr='256+3+65536') == '256+3+65536'

    def test_cpp_33880(self):
        assert self.cpp.convert_asm_number_into_c(expr='26') == '26'

    def test_cpp_33890(self):
        assert self.cpp.convert_asm_number_into_c(expr='27') == '27'

    def test_cpp_33900(self):
        assert self.cpp.convert_asm_number_into_c(expr='28') == '28'

    def test_cpp_33910(self):
        assert self.cpp.convert_asm_number_into_c(expr='29') == '29'

    def test_cpp_33920(self):
        assert self.cpp.convert_asm_number_into_c(expr='2Ch') == '0x2C'

    def test_cpp_33930(self):
        assert self.cpp.convert_asm_number_into_c(expr='2Dh') == '0x2D'

    def test_cpp_33940(self):
        assert self.cpp.convert_asm_number_into_c(expr='3') == '3'

    def test_cpp_33950(self):
        assert self.cpp.convert_asm_number_into_c(expr='3*4') == '3*4'

    def test_cpp_33960(self):
        assert self.cpp.convert_asm_number_into_c(expr='30') == '30'

    def test_cpp_33970(self):
        assert self.cpp.convert_asm_number_into_c(expr='303Bh') == '0x303B'

    def test_cpp_33980(self):
        assert self.cpp.convert_asm_number_into_c(expr='30h') == '0x30'

    def test_cpp_33990(self):
        assert self.cpp.convert_asm_number_into_c(expr='31') == '31'

    def test_cpp_34000(self):
        assert self.cpp.convert_asm_number_into_c(expr='31h') == '0x31'

    def test_cpp_34010(self):
        assert self.cpp.convert_asm_number_into_c(expr='32') == '32'

    def test_cpp_34020(self):
        assert self.cpp.convert_asm_number_into_c(expr='320*200/4') == '320*200/4'

    def test_cpp_34030(self):
        assert self.cpp.convert_asm_number_into_c(expr='32432434h') == '0x32432434'

    def test_cpp_34040(self):
        assert self.cpp.convert_asm_number_into_c(expr='340128h') == '0x340128'

    def test_cpp_34050(self):
        assert self.cpp.convert_asm_number_into_c(expr='35') == '35'

    def test_cpp_34060(self):
        assert self.cpp.convert_asm_number_into_c(expr='37') == '37'

    def test_cpp_34070(self):
        assert self.cpp.convert_asm_number_into_c(expr='39h') == '0x39'

    def test_cpp_34080(self):
        assert self.cpp.convert_asm_number_into_c(expr='3Ch') == '0x3C'

    def test_cpp_34090(self):
        assert self.cpp.convert_asm_number_into_c(expr='3DAh') == '0x3DA'

    def test_cpp_34100(self):
        assert self.cpp.convert_asm_number_into_c(expr='3Eh') == '0x3E'

    def test_cpp_34110(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FEh') == '0x3FE'

    def test_cpp_34120(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFEh') == '0x3FFE'

    def test_cpp_34130(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFEh') == '0x3FFFE'

    def test_cpp_34140(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFEh') == '0x3FFFFE'

    def test_cpp_34150(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFFEh') == '0x3FFFFFE'

    def test_cpp_34160(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFFFEh') == '0x3FFFFFFE'

    def test_cpp_34170(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFFFFh') == '0x3FFFFFFF'

    def test_cpp_34180(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFFFh') == '0x3FFFFFF'

    def test_cpp_34190(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFFh') == '0x3FFFFF'

    def test_cpp_34200(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFFh') == '0x3FFFF'

    def test_cpp_34210(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFFh') == '0x3FFF'

    def test_cpp_34220(self):
        assert self.cpp.convert_asm_number_into_c(expr='3FFh') == '0x3FF'

    def test_cpp_34230(self):
        assert self.cpp.convert_asm_number_into_c(expr='3Fh') == '0x3F'

    def test_cpp_34240(self):
        assert self.cpp.convert_asm_number_into_c(expr='3c8h') == '0x3c8'

    def test_cpp_34250(self):
        assert self.cpp.convert_asm_number_into_c(expr='3c9h') == '0x3c9'

    def test_cpp_34260(self):
        assert self.cpp.convert_asm_number_into_c(expr='3h') == '0x3'

    def test_cpp_34270(self):
        assert self.cpp.convert_asm_number_into_c(expr='4') == '4'

    def test_cpp_34280(self):
        assert self.cpp.convert_asm_number_into_c(expr='4+5*256') == '4+5*256'

    def test_cpp_34290(self):
        assert self.cpp.convert_asm_number_into_c(expr='4000000') == '4000000'

    def test_cpp_34300(self):
        assert self.cpp.convert_asm_number_into_c(expr='40h') == '0x40'

    def test_cpp_34310(self):
        assert self.cpp.convert_asm_number_into_c(expr='43210123h') == '0x43210123'

    def test_cpp_34320(self):
        assert self.cpp.convert_asm_number_into_c(expr='48h') == '0x48'

    def test_cpp_34330(self):
        assert self.cpp.convert_asm_number_into_c(expr='49h') == '0x49'

    def test_cpp_34340(self):
        assert self.cpp.convert_asm_number_into_c(expr='4Ah') == '0x4A'

    def test_cpp_34350(self):
        assert self.cpp.convert_asm_number_into_c(expr='4Ch') == '0x4C'

    def test_cpp_34360(self):
        assert self.cpp.convert_asm_number_into_c(expr='4ch') == '0x4c'

    def test_cpp_34370(self):
        assert self.cpp.convert_asm_number_into_c(expr='5') == '5'

    def test_cpp_34380(self):
        assert self.cpp.convert_asm_number_into_c(expr='50') == '50'

    def test_cpp_34390(self):
        assert self.cpp.convert_asm_number_into_c(expr='501h') == '0x501'

    def test_cpp_34400(self):
        assert self.cpp.convert_asm_number_into_c(expr='511') == '511'

    def test_cpp_34410(self):
        assert self.cpp.convert_asm_number_into_c(expr='55') == '55'

    def test_cpp_34420(self):
        assert self.cpp.convert_asm_number_into_c(expr='56') == '56'

    def test_cpp_34430(self):
        assert self.cpp.convert_asm_number_into_c(expr='57') == '57'

    def test_cpp_34440(self):
        assert self.cpp.convert_asm_number_into_c(expr='6') == '6'

    def test_cpp_34450(self):
        assert self.cpp.convert_asm_number_into_c(expr='6*256+5') == '6*256+5'

    def test_cpp_34460(self):
        assert self.cpp.convert_asm_number_into_c(expr='60') == '60'

    def test_cpp_34470(self):
        assert self.cpp.convert_asm_number_into_c(expr='65324h') == '0x65324'

    def test_cpp_34480(self):
        assert self.cpp.convert_asm_number_into_c(expr='65423456h') == '0x65423456'

    def test_cpp_34490(self):
        assert self.cpp.convert_asm_number_into_c(expr='6789ABCDh') == '0x6789ABCD'

    def test_cpp_34500(self):
        assert self.cpp.convert_asm_number_into_c(expr='7') == '7'

    def test_cpp_34510(self):
        assert self.cpp.convert_asm_number_into_c(expr='7Eh') == '0x7E'

    def test_cpp_34520(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FEh') == '0x7FE'

    def test_cpp_34530(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFEh') == '0x7FFE'

    def test_cpp_34540(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFEh') == '0x7FFFE'

    def test_cpp_34550(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFEh') == '0x7FFFFE'

    def test_cpp_34560(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFFEh') == '0x7FFFFFE'

    def test_cpp_34570(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFFFEh') == '0x7FFFFFFE'

    def test_cpp_34580(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFFFFh') == '0x7FFFFFFF'

    def test_cpp_34590(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFFFh') == '0x7FFFFFF'

    def test_cpp_34600(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFFh') == '0x7FFFFF'

    def test_cpp_34610(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFFh') == '0x7FFFF'

    def test_cpp_34620(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFFh') == '0x7FFF'

    def test_cpp_34630(self):
        assert self.cpp.convert_asm_number_into_c(expr='7FFh') == '0x7FF'

    def test_cpp_34640(self):
        assert self.cpp.convert_asm_number_into_c(expr='7Fh') == '0x7F'

    def test_cpp_34650(self):
        assert self.cpp.convert_asm_number_into_c(expr='8') == '8'

    def test_cpp_34660(self):
        assert self.cpp.convert_asm_number_into_c(expr='80000000h') == '0x80000000'

    def test_cpp_34670(self):
        assert self.cpp.convert_asm_number_into_c(expr='80000001h') == '0x80000001'

    def test_cpp_34680(self):
        assert self.cpp.convert_asm_number_into_c(expr='80008481h') == '0x80008481'

    def test_cpp_34690(self):
        assert self.cpp.convert_asm_number_into_c(expr='80008688h') == '0x80008688'

    def test_cpp_34700(self):
        assert self.cpp.convert_asm_number_into_c(expr='8000h') == '0x8000'

    def test_cpp_34710(self):
        assert self.cpp.convert_asm_number_into_c(expr='801h') == '0x801'

    def test_cpp_34720(self):
        assert self.cpp.convert_asm_number_into_c(expr='80h') == '0x80'

    def test_cpp_34730(self):
        assert self.cpp.convert_asm_number_into_c(expr='81234567h') == '0x81234567'

    def test_cpp_34740(self):
        assert self.cpp.convert_asm_number_into_c(expr='81238567h') == '0x81238567'

    def test_cpp_34750(self):
        assert self.cpp.convert_asm_number_into_c(expr='812FADAh') == '0x812FADA'

    def test_cpp_34760(self):
        assert self.cpp.convert_asm_number_into_c(expr='813F3421h') == '0x813F3421'

    def test_cpp_34770(self):
        assert self.cpp.convert_asm_number_into_c(expr='81h') == '0x81'

    def test_cpp_34780(self):
        assert self.cpp.convert_asm_number_into_c(expr='82345679h') == '0x82345679'

    def test_cpp_34790(self):
        assert self.cpp.convert_asm_number_into_c(expr='8234A6F8h') == '0x8234A6F8'

    def test_cpp_34800(self):
        assert self.cpp.convert_asm_number_into_c(expr='8345A1F2h') == '0x8345A1F2'

    def test_cpp_34810(self):
        assert self.cpp.convert_asm_number_into_c(expr='8C5h') == '0x8C5'

    def test_cpp_34820(self):
        assert self.cpp.convert_asm_number_into_c(expr='8D5h') == '0x8D5'

    def test_cpp_34830(self):
        assert self.cpp.convert_asm_number_into_c(expr='9') == '9'

    def test_cpp_34840(self):
        assert self.cpp.convert_asm_number_into_c(expr='9ABCDEFh') == '0x9ABCDEF'

    def test_cpp_34850(self):
        assert self.cpp.convert_asm_number_into_c(expr='AL') == 'AL'

    def test_cpp_34860(self):
        assert self.cpp.convert_asm_number_into_c(expr='B') == 'B'

    def test_cpp_34870(self):
        assert self.cpp.convert_asm_number_into_c(expr='CC') == 'CC'

    def test_cpp_34880(self):
        assert self.cpp.convert_asm_number_into_c(expr='DDD') == 'DDD'

    def test_cpp_34890(self):
        assert self.cpp.convert_asm_number_into_c(expr='DX') == 'DX'

    def test_cpp_34900(self):
        assert self.cpp.convert_asm_number_into_c(expr='OFFSET ASCiI') == 'OFFSET ASCiI'

    def test_cpp_34910(self):
        assert self.cpp.convert_asm_number_into_c(expr='OFFSET AsCii') == 'OFFSET AsCii'

    def test_cpp_34920(self):
        assert self.cpp.convert_asm_number_into_c(expr='TWO') == 'TWO'

    def test_cpp_34930(self):
        assert self.cpp.convert_asm_number_into_c(expr='[a+1]') == '[a+1]'

    def test_cpp_34940(self):
        assert self.cpp.convert_asm_number_into_c(expr='[a]') == '[a]'

    def test_cpp_34950(self):
        assert self.cpp.convert_asm_number_into_c(expr='[cs:table+ax]') == '[cs:table+ax]'

    def test_cpp_34960(self):
        assert self.cpp.convert_asm_number_into_c(expr='[doublequote+4]') == '[doublequote+4]'

    """
    def test_cpp_34970(self):
        self.assertEqual(convert_number_to_c(expr=u'[eax+4000h]'), u'[eax+0x4000]')

    def test_cpp_34980(self):
        self.assertEqual(convert_number_to_c(expr=u'[eax+40h]'), u'[eax+0x40]')

    def test_cpp_34990(self):
        self.assertEqual(convert_number_to_c(expr=u'[eax+ecx+40h]'), u'[eax+ecx+0x40]')
    """

    def test_cpp_35000(self):
        assert self.cpp.convert_asm_number_into_c(expr='[eax+ecx]') == '[eax+ecx]'

    def test_cpp_35010(self):
        assert self.cpp.convert_asm_number_into_c(expr='[eax]') == '[eax]'

    def test_cpp_35020(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+ecx_0]') == '[ebp+ecx_0]'

    def test_cpp_35030(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+ecx_vals]') == '[ebp+ecx_vals]'

    def test_cpp_35040(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+edx_0]') == '[ebp+edx_0]'

    def test_cpp_35050(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+i*4+ecx_vals]') == '[ebp+i*4+ecx_vals]'

    def test_cpp_35060(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+i+table]') == '[ebp+i+table]'

    def test_cpp_35070(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+iflags]') == '[ebp+iflags]'

    def test_cpp_35080(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+op0]') == '[ebp+op0]'

    def test_cpp_35090(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+op0h]') == '[ebp+op0h]'

    def test_cpp_35100(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+s0]') == '[ebp+s0]'

    def test_cpp_35110(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+s1]') == '[ebp+s1]'

    def test_cpp_35120(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+s2]') == '[ebp+s2]'

    def test_cpp_35130(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+table]') == '[ebp+table]'

    def test_cpp_35140(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+var_1C]') == '[ebp+var_1C]'

    def test_cpp_35150(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+var_20]') == '[ebp+var_20]'

    def test_cpp_35160(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebp+var_4]') == '[ebp+var_4]'

    """
    def test_cpp_35170(self):
        self.assertEqual(convert_number_to_c(expr=u'[ebx+4000h]'), u'[ebx+0x4000]')

    def test_cpp_35180(self):
        self.assertEqual(convert_number_to_c(expr=u'[ebx+40h]'), u'[ebx+0x40]')

    def test_cpp_35190(self):
        self.assertEqual(convert_number_to_c(expr=u'[ebx+edx+4000h]'), u'[ebx+edx+0x4000]')
    """

    def test_cpp_35200(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebx+edx]') == '[ebx+edx]'

    def test_cpp_35210(self):
        assert self.cpp.convert_asm_number_into_c(expr='[ebx]') == '[ebx]'

    """
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
    """

    def test_cpp_35810(self):
        assert self.cpp.convert_asm_number_into_c(expr='ah') == 'ah'

    def test_cpp_35820(self):
        assert self.cpp.convert_asm_number_into_c(expr='al') == 'al'

    def test_cpp_35830(self):
        assert self.cpp.convert_asm_number_into_c(expr='ax') == 'ax'

    def test_cpp_35840(self):
        assert self.cpp.convert_asm_number_into_c(expr='b') == 'b'

    def test_cpp_35850(self):
        assert self.cpp.convert_asm_number_into_c(expr='beginningdata') == 'beginningdata'

    def test_cpp_35860(self):
        assert self.cpp.convert_asm_number_into_c(expr='bh') == 'bh'

    def test_cpp_35870(self):
        assert self.cpp.convert_asm_number_into_c(expr='bl') == 'bl'

    def test_cpp_35880(self):
        assert self.cpp.convert_asm_number_into_c(expr='bp') == 'bp'

    def test_cpp_35890(self):
        assert self.cpp.convert_asm_number_into_c(expr='buffer') == 'buffer'

    def test_cpp_35900(self):
        assert self.cpp.convert_asm_number_into_c(expr='bx') == 'bx'

    def test_cpp_35910(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [a]') == 'byte ptr [a]'

    def test_cpp_35920(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [ebp+var_20]') == 'byte ptr [ebp+var_20]'

    def test_cpp_35930(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [edi+1]') == 'byte ptr [edi+1]'

    def test_cpp_35940(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [edi+7]') == 'byte ptr [edi+7]'

    def test_cpp_35950(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [esi]') == 'byte ptr [esi]'

    def test_cpp_35960(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [h2]') == 'byte ptr [h2]'

    def test_cpp_35970(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [h]') == 'byte ptr [h]'

    def test_cpp_35980(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [testOVerlap+1]') == 'byte ptr [testOVerlap+1]'

    def test_cpp_35990(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [var1+1]') == 'byte ptr [var1+1]'

    def test_cpp_36000(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr [var1+2]') == 'byte ptr [var1+2]'

    def test_cpp_36010(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr dl') == 'byte ptr dl'

    def test_cpp_36020(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr ds:[0]') == 'byte ptr ds:[0]'

    def test_cpp_36030(self):
        assert self.cpp.convert_asm_number_into_c(expr='byte ptr es:[0]') == 'byte ptr es:[0]'

    def test_cpp_36040(self):
        assert self.cpp.convert_asm_number_into_c(expr='ch') == 'ch'

    def test_cpp_36050(self):
        assert self.cpp.convert_asm_number_into_c(expr='cl') == 'cl'

    def test_cpp_36060(self):
        assert self.cpp.convert_asm_number_into_c(expr='cx') == 'cx'

    def test_cpp_36070(self):
        assert self.cpp.convert_asm_number_into_c(expr='di') == 'di'

    def test_cpp_36080(self):
        assert self.cpp.convert_asm_number_into_c(expr='dl') == 'dl'

    def test_cpp_36090(self):
        assert self.cpp.convert_asm_number_into_c(expr='ds') == 'ds'

    def test_cpp_36100(self):
        assert self.cpp.convert_asm_number_into_c(expr='ds:0[eax*2]') == 'ds:0[eax*2]'

    def test_cpp_36110(self):
        assert self.cpp.convert_asm_number_into_c(expr='ds:0[ebx*4]') == 'ds:0[ebx*4]'

    def test_cpp_36120(self):
        assert self.cpp.convert_asm_number_into_c(expr='ds:0[ecx*8]') == 'ds:0[ecx*8]'

    #def test_cpp_36130(self):

    #def test_cpp_36140(self):

    #def test_cpp_36150(self):

    def test_cpp_36160(self):
        assert self.cpp.convert_asm_number_into_c(expr='ds:[edi]') == 'ds:[edi]'

    def test_cpp_36170(self):
        assert self.cpp.convert_asm_number_into_c(expr='ds:byte_41411F[eax]') == 'ds:byte_41411F[eax]'

    def test_cpp_36180(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr [ebp+var_20+4]') == 'dword ptr [ebp+var_20+4]'

    def test_cpp_36190(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr [ebp+var_20]') == 'dword ptr [ebp+var_20]'

    def test_cpp_36200(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr [ebx-4]') == 'dword ptr [ebx-4]'

    """
    def test_cpp_36210(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+0Ch]'), u'dword ptr [esp+0x0C]')

    def test_cpp_36220(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+10h]'), u'dword ptr [esp+0x10]')

    def test_cpp_36230(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+14h]'), u'dword ptr [esp+0x14]')

    def test_cpp_36240(self):
        self.assertEqual(convert_number_to_c(expr=u'dword ptr [esp+1Ch]'), u'dword ptr [esp+0x1C]')
    """

    def test_cpp_36250(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr [esp+4]') == 'dword ptr [esp+4]'

    def test_cpp_36260(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr [esp+8]') == 'dword ptr [esp+8]'

    def test_cpp_36270(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr [esp]') == 'dword ptr [esp]'

    def test_cpp_36280(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr buffer') == 'dword ptr buffer'

    def test_cpp_36290(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr es:[0]') == 'dword ptr es:[0]'

    def test_cpp_36300(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr es:[20*320+160]') == 'dword ptr es:[20*320+160]'

    def test_cpp_36310(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword ptr var4') == 'dword ptr var4'

    def test_cpp_36320(self):
        assert self.cpp.convert_asm_number_into_c(expr='dword') == 'dword'

    def test_cpp_36330(self):
        assert self.cpp.convert_asm_number_into_c(expr='dx') == 'dx'

    def test_cpp_36340(self):
        assert self.cpp.convert_asm_number_into_c(expr='eax') == 'eax'

    def test_cpp_36350(self):
        assert self.cpp.convert_asm_number_into_c(expr='eax_0') == 'eax_0'

    def test_cpp_36360(self):
        assert self.cpp.convert_asm_number_into_c(expr='ebp') == 'ebp'

    def test_cpp_36370(self):
        assert self.cpp.convert_asm_number_into_c(expr='ebx') == 'ebx'

    def test_cpp_36380(self):
        assert self.cpp.convert_asm_number_into_c(expr='ecx') == 'ecx'

    def test_cpp_36390(self):
        assert self.cpp.convert_asm_number_into_c(expr='ecx_0') == 'ecx_0'

    def test_cpp_36400(self):
        assert self.cpp.convert_asm_number_into_c(expr='ecx_0_0') == 'ecx_0_0'

    def test_cpp_36410(self):
        assert self.cpp.convert_asm_number_into_c(expr='edi') == 'edi'

    def test_cpp_36420(self):
        assert self.cpp.convert_asm_number_into_c(expr='edi_0') == 'edi_0'

    def test_cpp_36430(self):
        assert self.cpp.convert_asm_number_into_c(expr='edx') == 'edx'

    def test_cpp_36440(self):
        assert self.cpp.convert_asm_number_into_c(expr='edx_0_0') == 'edx_0_0'

    def test_cpp_36450(self):
        assert self.cpp.convert_asm_number_into_c(expr='eflags') == 'eflags'

    def test_cpp_36460(self):
        assert self.cpp.convert_asm_number_into_c(expr='enddata') == 'enddata'

    def test_cpp_36470(self):
        assert self.cpp.convert_asm_number_into_c(expr='es') == 'es'

    def test_cpp_36480(self):
        assert self.cpp.convert_asm_number_into_c(expr='esi') == 'esi'

    def test_cpp_36490(self):
        assert self.cpp.convert_asm_number_into_c(expr='esi_0') == 'esi_0'

    def test_cpp_36500(self):
        assert self.cpp.convert_asm_number_into_c(expr='esp') == 'esp'

    def test_cpp_36510(self):
        assert self.cpp.convert_asm_number_into_c(expr='f') == 'f'

    def test_cpp_36520(self):
        assert self.cpp.convert_asm_number_into_c(expr='fileName') == 'fileName'

    def test_cpp_36530(self):
        assert self.cpp.convert_asm_number_into_c(expr='flags') == 'flags'

    def test_cpp_36540(self):
        assert self.cpp.convert_asm_number_into_c(expr='fs') == 'fs'

    def test_cpp_36550(self):
        assert self.cpp.convert_asm_number_into_c(expr='i') == 'i'

    #def test_cpp_36560(self):

    def test_cpp_36570(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset _msg') == 'offset _msg'

    def test_cpp_36580(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset _test_btc') == 'offset _test_btc'

    def test_cpp_36590(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000') == 'offset a0x4000'

    def test_cpp_36600(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000Eax') == 'offset a0x4000Eax'

    def test_cpp_36610(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000Ebx') == 'offset a0x4000Ebx'

    def test_cpp_36620(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000EbxEdx') == 'offset a0x4000EbxEdx'

    def test_cpp_36630(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000Ecx') == 'offset a0x4000Ecx'

    def test_cpp_36640(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000EcxEcx2') == 'offset a0x4000EcxEcx2'

    def test_cpp_36650(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000Edi') == 'offset a0x4000Edi'

    def test_cpp_36660(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000Edx') == 'offset a0x4000Edx'

    def test_cpp_36670(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000EdxEcx4') == 'offset a0x4000EdxEcx4'

    def test_cpp_36680(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000Esi') == 'offset a0x4000Esi'

    def test_cpp_36690(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x4000EsiEcx8') == 'offset a0x4000EsiEcx8'

    def test_cpp_36700(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Eax') == 'offset a0x40Eax'

    def test_cpp_36710(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Eax2') == 'offset a0x40Eax2'

    def test_cpp_36720(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40EaxEcx') == 'offset a0x40EaxEcx'

    def test_cpp_36730(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Ebx') == 'offset a0x40Ebx'

    def test_cpp_36740(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Ebx4') == 'offset a0x40Ebx4'

    def test_cpp_36750(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Ecx') == 'offset a0x40Ecx'

    def test_cpp_36760(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Ecx8') == 'offset a0x40Ecx8'

    def test_cpp_36770(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Edi') == 'offset a0x40Edi'

    def test_cpp_36780(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Edx') == 'offset a0x40Edx'

    def test_cpp_36790(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a0x40Esi') == 'offset a0x40Esi'

    def test_cpp_36800(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10EcxEcx2') == 'offset a10EcxEcx2'

    def test_cpp_36810(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10EdxEcx4') == 'offset a10EdxEcx4'

    def test_cpp_36820(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10EsiEcx8') == 'offset a10EsiEcx8'

    def test_cpp_36830(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxB08lx') == 'offset a10sA08lxB08lx'

    def test_cpp_36840(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxB08lxC') == 'offset a10sA08lxB08lxC'

    def test_cpp_36850(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxB08lxR') == 'offset a10sA08lxB08lxR'

    def test_cpp_36860(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxB08lxR_0') == 'offset a10sA08lxB08lxR_0'

    def test_cpp_36870(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxR08lx') == 'offset a10sA08lxR08lx'

    def test_cpp_36880(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxR08lx0') == 'offset a10sA08lxR08lx0'

    def test_cpp_36890(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxR08lxC') == 'offset a10sA08lxR08lxC'

    def test_cpp_36900(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxR08lxL') == 'offset a10sA08lxR08lxL'

    def test_cpp_36910(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08lxR08lx_0') == 'offset a10sA08lxR08lx_0'

    def test_cpp_36920(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sA08xR08xCci') == 'offset a10sA08xR08xCci'

    def test_cpp_36930(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sAh08lxAl08l') == 'offset a10sAh08lxAl08l'

    def test_cpp_36940(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sD') == 'offset a10sD'

    def test_cpp_36950(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sEax08lxA08l') == 'offset a10sEax08lxA08l'

    def test_cpp_36960(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sEcx08lxZfLd') == 'offset a10sEcx08lxZfLd'

    def test_cpp_36970(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset a10sEsi08lxEdi0') == 'offset a10sEsi08lxEdi0'

    def test_cpp_36980(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAaa') == 'offset aAaa'

    def test_cpp_36990(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAad') == 'offset aAad'

    def test_cpp_37000(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAam') == 'offset aAam'

    def test_cpp_37010(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAas') == 'offset aAas'

    def test_cpp_37020(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAdcb') == 'offset aAdcb'

    def test_cpp_37030(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAdcl') == 'offset aAdcl'

    def test_cpp_37040(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAdcw') == 'offset aAdcw'

    def test_cpp_37050(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAddb') == 'offset aAddb'

    def test_cpp_37060(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAddl') == 'offset aAddl'

    def test_cpp_37070(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAddw') == 'offset aAddw'

    def test_cpp_37080(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAndb') == 'offset aAndb'

    def test_cpp_37090(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAndl') == 'offset aAndl'

    def test_cpp_37100(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aAndw') == 'offset aAndw'

    def test_cpp_37110(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBsfl') == 'offset aBsfl'

    def test_cpp_37120(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBsfw') == 'offset aBsfw'

    def test_cpp_37130(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBsrl') == 'offset aBsrl'

    def test_cpp_37140(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBsrw') == 'offset aBsrw'

    def test_cpp_37150(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBswapl') == 'offset aBswapl'

    def test_cpp_37160(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtcl') == 'offset aBtcl'

    def test_cpp_37170(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtcw') == 'offset aBtcw'

    def test_cpp_37180(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtl') == 'offset aBtl'

    def test_cpp_37190(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtrl') == 'offset aBtrl'

    def test_cpp_37200(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtrw') == 'offset aBtrw'

    def test_cpp_37210(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtsl') == 'offset aBtsl'

    def test_cpp_37220(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtsw') == 'offset aBtsw'

    def test_cpp_37230(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aBtw') == 'offset aBtw'

    def test_cpp_37240(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCbw') == 'offset aCbw'

    def test_cpp_37250(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCdq') == 'offset aCdq'

    def test_cpp_37260(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpb') == 'offset aCmpb'

    def test_cpp_37270(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpl') == 'offset aCmpl'

    def test_cpp_37280(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpsb') == 'offset aCmpsb'

    def test_cpp_37290(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpsl') == 'offset aCmpsl'

    def test_cpp_37300(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpsw') == 'offset aCmpsw'

    def test_cpp_37310(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpw') == 'offset aCmpw'

    def test_cpp_37320(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpxchg8bEax08') == 'offset aCmpxchg8bEax08'

    def test_cpp_37330(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpxchgb') == 'offset aCmpxchgb'

    def test_cpp_37340(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpxchgl') == 'offset aCmpxchgl'

    def test_cpp_37350(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCmpxchgw') == 'offset aCmpxchgw'

    def test_cpp_37360(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCwd') == 'offset aCwd'

    def test_cpp_37370(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aCwde') == 'offset aCwde'

    def test_cpp_37380(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDaa') == 'offset aDaa'

    def test_cpp_37390(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDas') == 'offset aDas'

    def test_cpp_37400(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDecb') == 'offset aDecb'

    def test_cpp_37410(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDecl') == 'offset aDecl'

    def test_cpp_37420(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDecw') == 'offset aDecw'

    def test_cpp_37430(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDivb') == 'offset aDivb'

    def test_cpp_37440(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDivl') == 'offset aDivl'

    def test_cpp_37450(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aDivw') == 'offset aDivw'

    def test_cpp_37460(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEax') == 'offset aEax'

    def test_cpp_37470(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEax2') == 'offset aEax2'

    def test_cpp_37480(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEaxEcx') == 'offset aEaxEcx'

    def test_cpp_37490(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEbx') == 'offset aEbx'

    def test_cpp_37500(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEbx4') == 'offset aEbx4'

    def test_cpp_37510(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEbxEdx') == 'offset aEbxEdx'

    def test_cpp_37520(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEcx') == 'offset aEcx'

    def test_cpp_37530(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEcx8') == 'offset aEcx8'

    def test_cpp_37540(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEcxEcx') == 'offset aEcxEcx'

    def test_cpp_37550(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEcxEcx2') == 'offset aEcxEcx2'

    def test_cpp_37560(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEdi') == 'offset aEdi'

    def test_cpp_37570(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEdiEcx') == 'offset aEdiEcx'

    def test_cpp_37580(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEdx') == 'offset aEdx'

    def test_cpp_37590(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEdxEcx') == 'offset aEdxEcx'

    def test_cpp_37600(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEdxEcx4') == 'offset aEdxEcx4'

    def test_cpp_37610(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEsi') == 'offset aEsi'

    def test_cpp_37620(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEsiEcx') == 'offset aEsiEcx'

    def test_cpp_37630(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aEsiEcx8') == 'offset aEsiEcx8'

    def test_cpp_37640(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aIdivb') == 'offset aIdivb'

    def test_cpp_37650(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aIdivl') == 'offset aIdivl'

    def test_cpp_37660(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aIdivw') == 'offset aIdivw'

    def test_cpp_37670(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aImulb') == 'offset aImulb'

    def test_cpp_37680(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aImull') == 'offset aImull'

    def test_cpp_37690(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aImullIm') == 'offset aImullIm'

    def test_cpp_37700(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aImulw') == 'offset aImulw'

    def test_cpp_37710(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aImulwIm') == 'offset aImulwIm'

    def test_cpp_37720(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aIncb') == 'offset aIncb'

    def test_cpp_37730(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aIncl') == 'offset aIncl'

    def test_cpp_37740(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aIncw') == 'offset aIncw'

    def test_cpp_37750(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJa') == 'offset aJa'

    def test_cpp_37760(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJae') == 'offset aJae'

    def test_cpp_37770(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJb') == 'offset aJb'

    def test_cpp_37780(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJbe') == 'offset aJbe'

    def test_cpp_37790(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJcxz') == 'offset aJcxz'

    def test_cpp_37800(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJe') == 'offset aJe'

    def test_cpp_37810(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJecxz') == 'offset aJecxz'

    def test_cpp_37820(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJg') == 'offset aJg'

    def test_cpp_37830(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJge') == 'offset aJge'

    def test_cpp_37840(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJl') == 'offset aJl'

    def test_cpp_37850(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJle') == 'offset aJle'

    def test_cpp_37860(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJne') == 'offset aJne'

    def test_cpp_37870(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJns') == 'offset aJns'

    def test_cpp_37880(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aJs') == 'offset aJs'

    def test_cpp_37890(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLeaS08lx') == 'offset aLeaS08lx'

    def test_cpp_37900(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLodsb') == 'offset aLodsb'

    def test_cpp_37910(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLodsl') == 'offset aLodsl'

    def test_cpp_37920(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLodsw') == 'offset aLodsw'

    def test_cpp_37930(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLoopl') == 'offset aLoopl'

    def test_cpp_37940(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLoopnzl') == 'offset aLoopnzl'

    def test_cpp_37950(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aLoopzl') == 'offset aLoopzl'

    def test_cpp_37960(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aMovsb') == 'offset aMovsb'

    def test_cpp_37970(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aMovsl') == 'offset aMovsl'

    def test_cpp_37980(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aMovsw') == 'offset aMovsw'

    def test_cpp_37990(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aMulb') == 'offset aMulb'

    def test_cpp_38000(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aMull') == 'offset aMull'

    def test_cpp_38010(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aMulw') == 'offset aMulw'

    def test_cpp_38020(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aNegb') == 'offset aNegb'

    def test_cpp_38030(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aNegl') == 'offset aNegl'

    def test_cpp_38040(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aNegw') == 'offset aNegw'

    def test_cpp_38050(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aNotb') == 'offset aNotb'

    def test_cpp_38060(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aNotl') == 'offset aNotl'

    def test_cpp_38070(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aNotw') == 'offset aNotw'

    def test_cpp_38080(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aOrb') == 'offset aOrb'

    def test_cpp_38090(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aOrl') == 'offset aOrl'

    def test_cpp_38100(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aOrw') == 'offset aOrw'

    def test_cpp_38110(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aPopcntA08lxR08') == 'offset aPopcntA08lxR08'

    def test_cpp_38120(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aPoplEsp08lx') == 'offset aPoplEsp08lx'

    def test_cpp_38130(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aPopwEsp08lx') == 'offset aPopwEsp08lx'

    def test_cpp_38140(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRclb') == 'offset aRclb'

    def test_cpp_38150(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRcll') == 'offset aRcll'

    def test_cpp_38160(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRclw') == 'offset aRclw'

    def test_cpp_38170(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRcrb') == 'offset aRcrb'

    def test_cpp_38180(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRcrl') == 'offset aRcrl'

    def test_cpp_38190(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRcrw') == 'offset aRcrw'

    def test_cpp_38200(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepLodsb') == 'offset aRepLodsb'

    def test_cpp_38210(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepLodsl') == 'offset aRepLodsl'

    def test_cpp_38220(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepLodsw') == 'offset aRepLodsw'

    def test_cpp_38230(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepMovsb') == 'offset aRepMovsb'

    def test_cpp_38240(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepMovsl') == 'offset aRepMovsl'

    def test_cpp_38250(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepMovsw') == 'offset aRepMovsw'

    def test_cpp_38260(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepStosb') == 'offset aRepStosb'

    def test_cpp_38270(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepStosl') == 'offset aRepStosl'

    def test_cpp_38280(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepStosw') == 'offset aRepStosw'

    def test_cpp_38290(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepnzCmpsb') == 'offset aRepnzCmpsb'

    def test_cpp_38300(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepnzCmpsl') == 'offset aRepnzCmpsl'

    def test_cpp_38310(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepnzCmpsw') == 'offset aRepnzCmpsw'

    def test_cpp_38320(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepnzScasb') == 'offset aRepnzScasb'

    def test_cpp_38330(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepnzScasl') == 'offset aRepnzScasl'

    def test_cpp_38340(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepnzScasw') == 'offset aRepnzScasw'

    def test_cpp_38350(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepzCmpsb') == 'offset aRepzCmpsb'

    def test_cpp_38360(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepzCmpsl') == 'offset aRepzCmpsl'

    def test_cpp_38370(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepzCmpsw') == 'offset aRepzCmpsw'

    def test_cpp_38380(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepzScasb') == 'offset aRepzScasb'

    def test_cpp_38390(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepzScasl') == 'offset aRepzScasl'

    def test_cpp_38400(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRepzScasw') == 'offset aRepzScasw'

    def test_cpp_38410(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRolb') == 'offset aRolb'

    def test_cpp_38420(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRoll') == 'offset aRoll'

    def test_cpp_38430(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRolw') == 'offset aRolw'

    def test_cpp_38440(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRorb') == 'offset aRorb'

    def test_cpp_38450(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRorl') == 'offset aRorl'

    def test_cpp_38460(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aRorw') == 'offset aRorw'

    def test_cpp_38470(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSarb') == 'offset aSarb'

    def test_cpp_38480(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSarl') == 'offset aSarl'

    def test_cpp_38490(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSarw') == 'offset aSarw'

    def test_cpp_38500(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSbbb') == 'offset aSbbb'

    def test_cpp_38510(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSbbl') == 'offset aSbbl'

    def test_cpp_38520(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSbbw') == 'offset aSbbw'

    def test_cpp_38530(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aScasb') == 'offset aScasb'

    def test_cpp_38540(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aScasl') == 'offset aScasl'

    def test_cpp_38550(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aScasw') == 'offset aScasw'

    def test_cpp_38560(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSetb') == 'offset aSetb'

    def test_cpp_38570(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSete') == 'offset aSete'

    def test_cpp_38580(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSetne') == 'offset aSetne'

    def test_cpp_38590(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShlb') == 'offset aShlb'

    def test_cpp_38600(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShldl') == 'offset aShldl'

    def test_cpp_38610(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShldw') == 'offset aShldw'

    def test_cpp_38620(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShll') == 'offset aShll'

    def test_cpp_38630(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShlw') == 'offset aShlw'

    def test_cpp_38640(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShrb') == 'offset aShrb'

    def test_cpp_38650(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShrdl') == 'offset aShrdl'

    def test_cpp_38660(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShrdw') == 'offset aShrdw'

    def test_cpp_38670(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShrl') == 'offset aShrl'

    def test_cpp_38680(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aShrw') == 'offset aShrw'

    def test_cpp_38690(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aStosb') == 'offset aStosb'

    def test_cpp_38700(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aStosl') == 'offset aStosl'

    def test_cpp_38710(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aStosw') == 'offset aStosw'

    def test_cpp_38720(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSubb') == 'offset aSubb'

    def test_cpp_38730(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSubl') == 'offset aSubl'

    def test_cpp_38740(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aSubw') == 'offset aSubw'

    def test_cpp_38750(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXaddb') == 'offset aXaddb'

    def test_cpp_38760(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXaddl') == 'offset aXaddl'

    def test_cpp_38770(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXaddlSameRes08') == 'offset aXaddlSameRes08'

    def test_cpp_38780(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXaddw') == 'offset aXaddw'

    def test_cpp_38790(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXchgb') == 'offset aXchgb'

    def test_cpp_38800(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXchgl') == 'offset aXchgl'

    def test_cpp_38810(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXchgw') == 'offset aXchgw'

    def test_cpp_38820(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXlatEax08lx') == 'offset aXlatEax08lx'

    def test_cpp_38830(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXorb') == 'offset aXorb'

    def test_cpp_38840(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXorl') == 'offset aXorl'

    def test_cpp_38850(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset aXorw') == 'offset aXorw'

    def test_cpp_38860(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset pal_jeu') == 'offset pal_jeu'

    def test_cpp_38870(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset str1') == 'offset str1'

    def test_cpp_38880(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset str2') == 'offset str2'

    def test_cpp_38890(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset str3') == 'offset str3'

    #def test_cpp_38900(self):

    #def test_cpp_38910(self):

    def test_cpp_38920(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset testOVerlap') == 'offset testOVerlap'

    def test_cpp_38930(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset unk_40E008') == 'offset unk_40E008'

    def test_cpp_38940(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset unk_40F064') == 'offset unk_40F064'

    def test_cpp_38950(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var1') == 'offset var1'

    def test_cpp_38960(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var1+1') == 'offset var1+1'

    def test_cpp_38970(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var2') == 'offset var2'

    def test_cpp_38980(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var3') == 'offset var3'

    def test_cpp_38990(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var3+4') == 'offset var3+4'

    def test_cpp_39000(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var4') == 'offset var4'

    def test_cpp_39010(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var4+1') == 'offset var4+1'

    def test_cpp_39020(self):
        assert self.cpp.convert_asm_number_into_c(expr='offset var4+4') == 'offset var4+4'

    def test_cpp_39030(self):
        assert self.cpp.convert_asm_number_into_c(expr='op0') == 'op0'

    def test_cpp_39040(self):
        assert self.cpp.convert_asm_number_into_c(expr='op1') == 'op1'

    def test_cpp_39050(self):
        assert self.cpp.convert_asm_number_into_c(expr='printf') == 'printf'

    def test_cpp_39060(self):
        assert self.cpp.convert_asm_number_into_c(expr='ptr') == 'ptr'

    def test_cpp_39070(self):
        assert self.cpp.convert_asm_number_into_c(expr='r') == 'r'

    def test_cpp_39080(self):
        assert self.cpp.convert_asm_number_into_c(expr='res') == 'res'

    def test_cpp_39090(self):
        assert self.cpp.convert_asm_number_into_c(expr='resh') == 'resh'

    def test_cpp_39100(self):
        assert self.cpp.convert_asm_number_into_c(expr='resz') == 'resz'

    def test_cpp_39110(self):
        assert self.cpp.convert_asm_number_into_c(expr='rh') == 'rh'

    def test_cpp_39120(self):
        assert self.cpp.convert_asm_number_into_c(expr='s0_0') == 's0_0'

    def test_cpp_39130(self):
        assert self.cpp.convert_asm_number_into_c(expr='s1_0') == 's1_0'

    def test_cpp_39140(self):
        assert self.cpp.convert_asm_number_into_c(expr='si') == 'si'

    def test_cpp_39150(self):
        assert self.cpp.convert_asm_number_into_c(expr='small') == 'small'

    def test_cpp_39160(self):
        assert self.cpp.convert_asm_number_into_c(expr='t') == 't'

    def test_cpp_39170(self):
        assert self.cpp.convert_asm_number_into_c(expr='taille_moire') == 'taille_moire'

    def test_cpp_39180(self):
        assert self.cpp.convert_asm_number_into_c(expr='teST2') == 'teST2'

    def test_cpp_39190(self):
        assert self.cpp.convert_asm_number_into_c(expr='testOVerlap') == 'testOVerlap'

    def test_cpp_39200(self):
        assert self.cpp.convert_asm_number_into_c(expr='var1') == 'var1'

    def test_cpp_39210(self):
        assert self.cpp.convert_asm_number_into_c(expr='var1[1]') == 'var1[1]'

    def test_cpp_39220(self):
        assert self.cpp.convert_asm_number_into_c(expr='var1[bx+si]') == 'var1[bx+si]'

    def test_cpp_39230(self):
        assert self.cpp.convert_asm_number_into_c(expr='var1[bx]') == 'var1[bx]'

    def test_cpp_39240(self):
        assert self.cpp.convert_asm_number_into_c(expr='var2') == 'var2'

    def test_cpp_39250(self):
        assert self.cpp.convert_asm_number_into_c(expr='var3+3*4') == 'var3+3*4'

    def test_cpp_39260(self):
        assert self.cpp.convert_asm_number_into_c(expr='var3+ebp') == 'var3+ebp'

    def test_cpp_39270(self):
        assert self.cpp.convert_asm_number_into_c(expr='var5') == 'var5'

    def test_cpp_39280(self):
        assert self.cpp.convert_asm_number_into_c(expr='word ptr [d]') == 'word ptr [d]'

    def test_cpp_39290(self):
        assert self.cpp.convert_asm_number_into_c(expr='word ptr [e]') == 'word ptr [e]'

    def test_cpp_39300(self):
        assert self.cpp.convert_asm_number_into_c(expr='word ptr [ebp+var_20]') == 'word ptr [ebp+var_20]'

    def test_cpp_39310(self):
        assert self.cpp.convert_asm_number_into_c(expr='word ptr [var5+2]') == 'word ptr [var5+2]'

    def test_cpp_39320(self):
        assert self.cpp.convert_asm_number_into_c(expr='word ptr var5') == 'word ptr var5'

    def test_cpp_39330(self):
        assert self.cpp.convert_asm_number_into_c(expr='word') == 'word'

    def test_cpp_36335(self):
        assert self.cpp.convert_asm_number_into_c(expr='7o') == '07'

    def test_cpp_39340(self):
        assert self.cpp.cpp_mangle_label(name='loc_40458F') == 'loc_40458f'

    def test_cpp_39350(self):
        assert self.cpp.cpp_mangle_label(name='_start') == '_start'

    def test_cpp_39360(self):
        assert self.cpp.cpp_mangle_label(name='_st$art$') == '_st_tmpart_tmp'


if __name__ == "__main__":
    unittest.main()
