from __future__ import absolute_import
from __future__ import print_function

from masm2c import cpp
from masm2c import op
from masm2c.parser import Parser
from masm2c.proc import Proc
import traceback
import unittest

from random import randint


# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
#unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


class ParserTest(unittest.TestCase):
    # First define a class variable that determines
    # if setUp was ever run
    ClassIsSetup = False

    def setUp(self):
        # If it was not setup yet, do it
        if not self.ClassIsSetup:
            print("Initializing testing environment")
            # run the real setup
            self.setupClass()
            # remember that it was setup already
            self.__class__.ClassIsSetup = True

    def setupClass(self):
        # Do the real setup
        unittest.TestCase.setUp(self)
        self.__class__.parser = Parser([])
        self.__class__.parser.test_mode = True
        self.__class__.cpp = cpp.Cpp(self.__class__.parser)
        self.__class__.proc = Proc('mainproc')
        self.__class__.cpp.proc = self.__class__.proc

        self.__class__.parser.action_assign_test(line_number=0, label='B', value=u'1')
        self.__class__.parser.action_assign_test(line_number=0, label='DDD', value=u'singlebyte2')
        self.__class__.parser.action_assign_test(line_number=0, label='argc', value=u'8')
        self.__class__.parser.action_assign_test(line_number=0, label='argv', value=u'0x0C')
        self.__class__.parser.action_assign_test(line_number=0, label='eax_0', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='ecx_0', value=u'-0x2C')
        self.__class__.parser.action_assign_test(line_number=0, label='ecx_0_0', value=u'ecx')
        self.__class__.parser.action_assign_test(line_number=0, label='ecx_vals', value=u'-0x28')
        self.__class__.parser.action_assign_test(line_number=0, label='edi_0', value=u'edi')
        self.__class__.parser.action_assign_test(line_number=0, label='edx_0', value=u'-0x2C')
        self.__class__.parser.action_assign_test(line_number=0, label='edx_0_0', value=u'edx')
        self.__class__.parser.action_assign_test(line_number=0, label='eflags', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='esi_0', value=u'ebx')
        self.__class__.parser.action_assign_test(line_number=0, label='esi_0', value=u'esi')
        self.__class__.parser.action_assign_test(line_number=0, label='flags', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='i', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='iflags', value=u'0x10')
        self.__class__.parser.action_assign_test(line_number=0, label='iflags', value=u'0x14')
        self.__class__.parser.action_assign_test(line_number=0, label='op0', value=u'0x0C')
        self.__class__.parser.action_assign_test(line_number=0, label='op0h', value=u'8')
        self.__class__.parser.action_assign_test(line_number=0, label='op1', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='r', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='res', value=u'eax')
        self.__class__.parser.action_assign_test(line_number=0, label='resh', value=u'ebx')
        self.__class__.parser.action_assign_test(line_number=0, label='resz', value=u'ecx')
        self.__class__.parser.action_assign_test(line_number=0, label='rh', value=u'edx')
        self.__class__.parser.action_assign_test(line_number=0, label='s0', value=u'0x0C')
        self.__class__.parser.action_assign_test(line_number=0, label='s0_0', value=u'ebx')
        self.__class__.parser.action_assign_test(line_number=0, label='s1', value=u'0x0C')
        self.__class__.parser.action_assign_test(line_number=0, label='s1_0', value=u'ecx')
        self.__class__.parser.action_assign_test(line_number=0, label='s2', value=u'8')
        #self.__class__.parser.action_assign_test(line_number=0, label='table', value=u'-0x108')
        self.__class__.parser.action_assign_test(line_number=0, label='val', value=u'-0x1C')
        self.__class__.parser.action_assign_test(line_number=0, label='var_1C', value=u'-0x1C')
        self.__class__.parser.action_assign_test(line_number=0, label='var_20', value=u'-0x20')
        self.__class__.parser.action_assign_test(line_number=0, label='var_2C', value=u'-0x2C')
        self.__class__.parser.action_assign_test(line_number=0, label='var_4', value=u'-4')
        self.__class__.parser.action_equ_test(line_number=0, label='CC', value=u'4')
        self.__class__.parser.action_equ_test(line_number=0, label='T', value=u'4')
        self.__class__.parser.action_equ_test(line_number=0, label='TEST2', value=u'-13')
        self.__class__.parser.action_equ_test(line_number=0, label='dubsize', value=u'13')
        self.__class__.parser.action_equ_test(line_number=0, label='tWO', value=u'2')
        self.__class__.parser.action_equ_test(line_number=0, label='taille_moire', value=u'((((2030080+64000*26)/4096)+1)*4096)-1')
        self.__class__.parser.action_equ_test(line_number=0, label='test1', value=u'(00+38*3)*320+1/2+33*(3-1)')
        self.__class__.parser.action_equ_test(line_number=0, label='test3', value=u'1500')
        self.__class__.parser.action_equ_test(line_number=0, label='testEqu', value=u'1')


        self.__class__.parser.set_global("_data", op.var(1, 0, issegment=True))
        self.__class__.parser.set_global("singlebyte2", op.var(size=1, offset=1, name="singlebyte2", segment="_data", elements=1))
        self.__class__.parser.set_global('_msg', op.var(elements=2, name=u'_msg', offset=1, segment=u'_data', size=1))
        # p.set_global('_msg', op.var(name=u'_msg', offset=1, segment=u'dseg', size=1))
        self.__class__.parser.set_global('_test_btc', op.var(name=u'_test_btc', offset=1, segment=u'initcall', size=4))
        self.__class__.parser.set_global('a', op.var(elements=3, name=u'a', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('a10sa08lxb08lx', op.var(elements=2, name=u'a10sA08lxB08lx', offset=1, segment=u'_rdata', size=1))
        self.__class__.parser.set_global('a10sah08lxal08l', op.var(elements=2, name=u'a10sAh08lxAl08l', offset=1, segment=u'_rdata', size=1))
        self.__class__.parser.set_global('a10sd', op.var(elements=2, name=u'a10sD', offset=1, segment=u'_rdata', size=1))
        self.__class__.parser.set_global('a10seax08lxa08l', op.var(elements=2, name=u'a10sEax08lxA08l', offset=1, segment=u'_rdata', size=1))
        self.__class__.parser.set_global('ascii', op.var(elements=2, name=u'ASCII', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('axorw', op.var(name=u'aXorw', offset=1, segment=u'_rdata', size=1))
        self.__class__.parser.set_global('beginningdata', op.var(name=u'beginningdata', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('buffer', op.var(elements=64000, name=u'buffer', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('byte_41411f', op.var(name=u'byte_41411F', offset=1, segment=u'_bss', size=1))
        self.__class__.parser.set_global('d', op.var(name=u'd', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('doublequote', op.var(elements=0, name=u'doublequote', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('e', op.var(name=u'e', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('enddata', op.var(name=u'enddata', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('f', op.var(name=u'f', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('filename', op.var(name=u'fileName', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('g', op.var(name=u'g', offset=1, segment=u'_data', size=4))
        self.__class__.parser.set_global('h', op.var(name=u'h', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('h2', op.var(name=u'h2', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('load_handle', op.var(name=u'load_handle', offset=1, segment=u'_data', size=4))
        self.__class__.parser.set_global('pal_jeu', op.var(elements=16, name=u'pal_jeu', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('str1', op.var(elements=0, name=u'str1', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('str2', op.var(elements=0, name=u'str2', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('str3', op.var(elements=0, name=u'str3', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('str_buffer', op.var(elements=4096, name=u'str_buffer', offset=1, segment=u'_bss', size=1))
        self.__class__.parser.set_global('table', op.var(name=u'table', offset=1, segment=u'_text', size=2))
        self.__class__.parser.set_global('testoverlap', op.var(elements=14, name=u'testOVerlap', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('unk_40e008', op.var(name=u'unk_40E008', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('unk_40f064', op.var(name=u'unk_40F064', offset=1, segment=u'initcall', size=1))
        self.__class__.parser.set_global('var', op.var(elements=4, name=u'var', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('bytearray2', op.var(elements=10, name=u'bytearray2', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('wordarray', op.var(elements=3, name=u'wordarray', offset=1, segment=u'_data', size=2))
        self.__class__.parser.set_global('singlebyte', op.var(elements=1, name=u'singlebyte', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('bytearray', op.var(elements=100, name=u'bytearray', offset=1, segment=u'_data', size=1))
        self.__class__.parser.set_global('singlequad', op.var(elements=1, name=u'singlequad', offset=1, segment=u'_data', size=4))
        #self.__class__.parser.set_global('gameconfig', op.var(elements=1, name=u'gameconfig', offset=1, segment=u'_data', size=1))
        self.__class__.parser.action_data(line='''GAMEINFO struc
game_opponenttype dw ?
game_opponentmaterial dd ?
game_opponentcarid db 4 dup (?)
GAMEINFO ends
extrn gameconfig:GAMEINFO
head db '^',10,10
''')
        self.__class__.parser.action_data(line='''
 VECTOR struc
    vx dw ?
 VECTOR ends
 TRANSFORMEDSHAPE struc
    ts_shapeptr dw ?
    ts_rectptr dw ?
    ts_rOTvec VECTOR <>
    ts_vec VECTOR 3 dup (<>)
 TRANSFORMEDSHAPE ends
 var_transshape = TRANSFORMEDSHAPE ptr -50
''')
        self.__class__.parser.get_global('var_transshape').implemented = True
        #?self.__class__.cpp._assignment('var_transshape',self.__class__.parser.get_global('var_transshape'))
        self.__class__.parser.action_label(far=False, name='@@saaccvaaaax', isproc=False)
        self.__class__.parser.action_label(far=False, name='@VBL1', isproc=False)
        self.__class__.parser.action_label(far=False, name='@VBL12', isproc=False)
        self.__class__.parser.action_label(far=False, name='@VBL2', isproc=False)
        self.__class__.parser.action_label(far=False, name='@VBL22', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@1', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@2', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@3', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@4', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@5', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@6', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@7', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@8', isproc=False)
        self.__class__.parser.action_label(far=False, name='@df@@@@9', isproc=False)
        self.__class__.parser.action_label(far=False, name='OK', isproc=False)
        self.__class__.parser.action_label(far=False, name='P1', isproc=False)
        self.__class__.parser.action_label(far=False, name='P2', isproc=False)
        self.__class__.parser.action_label(far=False, name='dffd', isproc=False)
        self.__class__.parser.action_label(far=False, name='exitLabel', isproc=False)
        self.__class__.parser.action_label(far=False, name='failure', isproc=False)
        self.__class__.parser.action_label(far=False, name='finTest', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40458F', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_4046D6', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_406B3F', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_406CF8', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_406EBA', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40707C', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40723E', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40752C', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_4075C2', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_407658', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_4076EE', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_407784', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_407E46', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_407F72', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_408008', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40809E', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_408139', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_4081F6', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_4083E9', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_408464', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_4084DF', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40855A', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_409652', isproc=False)
        self.__class__.parser.action_label(far=False, name='loc_40D571', isproc=False)
        self.__class__.parser.action_label(far=False, name='next', isproc=False)
        self.__class__.parser.action_label(far=False, name='noerror', isproc=False)
        self.__class__.parser.action_label(far=False, name='toto1', isproc=False)
        self.__class__.parser.action_label(far=False, name=u'exec_adc', isproc=True)
        self.__class__.parser.action_label(far=False, name=u'exec_rclb', isproc=True)
        self.__class__.parser.action_label(far=False, name=u'printeax', isproc=True)
        self.__class__.parser.action_label(far=True, name=u'test_bcd', isproc=True)

    def test_instr_09(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov    ax, offset     failure')), u'MOV(ax, m2c::kfailure)')

    #def test_instr_10(self):
    #    self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     small word ptr [esp]')), u'POP(*(dw*)(raddr(ss,esp)))')

    def test_instr_20(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call dx')), u'CALL(__dispatch_call,dx)')

    #def test_instr_30(self):
    #    self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     dword ptr [esp] eax edx')), u'POP(*(dd*)(raddr(ss,esp))));\n\tR(POP(eax));\n\tR(POP(edx)')

    '''
    def test_instr_40(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pOp  ebx ebp    eax')), u'POP(ebx));\n\tR(POP(ebp));\n\tR(POP(eax)')

    def test_instr_50(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop  dx cx ; linear address of allocated memory block')), u'POP(dx));\n\tR(POP(cx)')

    def test_instr_60(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop ds es')), u'POP(ds));\n\tR(POP(es)')

    def test_instr_70(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push  eax ebp  ebx')), u'PUSH(eax));\n\tR(PUSH(ebp));\n\tR(PUSH(ebx)')

    def test_instr_80(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push bx cx ; linear address of allocated memory block')), u'PUSH(bx));\n\tR(PUSH(cx)')

    def test_instr_90(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push bx fs')), u'PUSH(bx));\n\tR(PUSH(fs)')

    def test_instr_100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push es ds')), u'PUSH(es));\n\tR(PUSH(ds)')
    '''

    def test_instr_110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp a,1')), u'CMP(*(a), 1)')

    @unittest.skip("undefined behaviour")
    def test_instr_120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+i+table], dl')), u'MOV(*(dw*)(raddr(ss,ebp+i+offset(_text,table))), dl)')

    def test_instr_130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP [wordarray],1')), u'CMP(*(wordarray), 1)')

    def test_instr_140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP [wordarray],13')), u'CMP(*(wordarray), 13)')

    def test_instr_150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP [singlebyte],35')), u'CMP(singlebyte, 35)')

    def test_instr_160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP eax,133')), u'CMP(eax, 133)')

    def test_instr_170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP eax,2')), u'CMP(eax, 2)')

    def test_instr_180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP eax,3')), u'CMP(eax, 3)')

    def test_instr_190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('INC [singlebyte2]')), u'INC(singlebyte2)')

    def test_instr_200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('INC [wordarray]')), u'INC(*(wordarray))')

    def test_instr_210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('INC [singlebyte]')), u'INC(singlebyte)')

    def test_instr_220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('INC eax')), u'INC(eax)')

    def test_instr_230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('INC edx')), u'INC(edx)')

    def test_instr_240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp b,256+3')), u'CMP(b, 256+3)')

    def test_instr_250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call [cs:table+ax]')), 'CALL(__dispatch_call,*(dw*)(((db*)&table)+ax))')

    def test_instr_260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP eax,1')), u'CMP(eax, 1)')

    def test_instr_270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("cmp ebx,'dcba'")), u'CMP(ebx, 0x64636261)')

    def test_instr_280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("sub dl,'a'")), u"SUB(dl, 'a')")

    def test_instr_290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte2[bx],2')), u'CMP(*((&singlebyte2)+bx), 2)')

    def test_instr_300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("cmp [doublequote+4],'d'")), u"CMP(*((doublequote)+4), 'd')")

    def test_instr_310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("cmp dword ptr buffer,'tseT'")), u'CMP(*(dd*)((buffer)), 0x74736554)')

    def test_instr_320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("mov ah,9            ; DS:DX->'$'-terminated string")), u'MOV(ah, 9)')

    def test_instr_330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("mov dl,'c'")), u"MOV(dl, 'c')")

    def test_instr_340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("mov ecx,'dcba'")), u'MOV(ecx, 0x64636261)')

    def test_instr_350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('CMP [singlebyte2],111')), u'CMP(singlebyte2, 111)')

    def test_instr_360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JA failure')), u'JA(failure)')

    def test_instr_370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JAE failure')), u'JNC(failure)')

    def test_instr_380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JB failure')), u'JC(failure)')

    def test_instr_390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JE @VBL2    ;on attends la fin du retrace')), u'JZ(arbvbl2)')

    def test_instr_400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JE @VBL22    ;on attends la fin du retrace')), u'JZ(arbvbl22)')

    def test_instr_410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JE failure')), u'JZ(failure)')

    def test_instr_420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JMP exitLabel')), u'JMP(exitlabel)')

    def test_instr_430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JNE @VBL1    ;on attends le retrace')), u'JNZ(arbvbl1)')

    def test_instr_440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JNE @VBL12    ;on attends le retrace')), u'JNZ(arbvbl12)')

    def test_instr_460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('JNZ  @@saaccvaaaax')), u'JNZ(arbarbsaaccvaaaax)')

    def test_instr_480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('MOV DX,3DAh')), u'MOV(dx, 0x3DA)')

    def test_instr_490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('MOV al,0')), u'MOV(al, 0)')

    def test_instr_500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('MOV ds, _data')), u'MOV(ds, seg_offset(_data))')

    def test_instr_510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('SHL ch,2')), u'SHL(ch, 2)')

    def test_instr_520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('SHR bl,1')), u'SHR(bl, 1)')

    def test_instr_530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('SHR ch,1')), u'SHR(ch, 1)')

    def test_instr_540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('SHR eax,1')), u'SHR(eax, 1)')

    def test_instr_550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('TEST AL,8')), u'TEST(al, 8)')

    def test_instr_570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('aaa')), 'AAA')

    def test_instr_580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('aad')), 'AAD')

    def test_instr_590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('aam')), 'AAM')

    def test_instr_600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('aas')), 'AAS')

    def test_instr_610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('adc     dl, cl')), u'ADC(dl, cl)')

    def test_instr_620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('adc     dx, cx')), u'ADC(dx, cx)')

    def test_instr_630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('adc     edx, ecx')), u'ADC(edx, ecx)')

    def test_instr_640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     dl, cl')), u'ADD(dl, cl)')

    def test_instr_650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     dx, cx')), u'ADD(dx, cx)')

    def test_instr_660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     ebx, 4')), u'ADD(ebx, 4)')

    def test_instr_670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     edx, ecx')), u'ADD(edx, ecx)')

    def test_instr_680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     esp, 10h')), u'ADD(esp, 0x10)')

    def test_instr_690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     esp, 114h')), u'ADD(esp, 0x114)')

    def test_instr_700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     esp, 2')), u'ADD(esp, 2)')

    def test_instr_710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     esp, 20h')), u'ADD(esp, 0x20)')

    def test_instr_720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     esp, 4Ch')), u'ADD(esp, 0x4C)')

    def test_instr_730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add bl,30h          ; convert to ASCII')), u'ADD(bl, 0x30)')

    def test_instr_740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add bl,7            ; "A" to "F"')), u'ADD(bl, 7)')

    def test_instr_750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add edi,14*320')), u'ADD(edi, 14*320)')

    def test_instr_760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add word ptr [singlequad+2],50')), u'ADD(*(dw*)(((db*)&singlequad)+2), 50)')

    def test_instr_770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     ah, 0F7h')), u'AND(ah, 0x0F7)')

    def test_instr_780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     dl, cl')), u'AND(dl, cl)')

    def test_instr_790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     dx, cx')), u'AND(dx, cx)')

    def test_instr_800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     ecx, 40h')), u'AND(ecx, 0x40)')

    def test_instr_810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     edx, ecx')), u'AND(edx, ecx)')

    def test_instr_820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     eflags, 40h')), u'AND(eflags, 0x40)')

    def test_instr_830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     eflags, 8D5h')), u'AND(eflags, 0x8D5)')

    def test_instr_840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     esp, 0FFFFFFF0h')), u'AND(esp, 0x0FFFFFFF0)')

    def test_instr_850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     flags, 0D5h')), u'AND(flags, 0x0D5)')

    def test_instr_860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     flags, 1')), u'AND(flags, 1)')

    def test_instr_870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     flags, 11h')), u'AND(flags, 0x11)')

    def test_instr_880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     flags, 801h')), u'AND(flags, 0x801)')

    def test_instr_890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     flags, 8C5h')), u'AND(flags, 0x8C5)')

    def test_instr_900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and     flags, 8D5h')), u'AND(flags, 0x8D5)')

    def test_instr_910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('and bl,0Fh          ; only low-Nibble')), u'AND(bl, 0x0F)')

    def test_instr_920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsf     ax, bx')), u'BSF(ax, bx)')

    def test_instr_930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsf     ax, di')), u'BSF(ax, di)')

    def test_instr_940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsf     ax, si')), u'BSF(ax, si)')

    def test_instr_950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsf     eax, ebx')), u'BSF(eax, ebx)')

    def test_instr_960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsf     eax, edi')), u'BSF(eax, edi)')

    def test_instr_970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsr     ax, bx')), u'BSR(ax, bx)')

    def test_instr_980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsr     ax, di')), u'BSR(ax, di)')

    def test_instr_990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsr     eax, ebx')), u'BSR(eax, ebx)')

    def test_instr_1000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsr     eax, edx')), u'BSR(eax, edx)')

    def test_instr_1010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsr     eax, esi')), u'BSR(eax, esi)')

    def test_instr_1020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bsr     edx, eax')), u'BSR(edx, eax)')

    def test_instr_1030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bswap   eax')), u'BSWAP(eax)')

    def test_instr_1040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bt      cx, dx')), u'BT(cx, dx)')

    def test_instr_1050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bt      ecx, edx')), u'BT(ecx, edx)')

    def test_instr_1060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bt eax,0')), u'BT(eax, 0)')

    def test_instr_1070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bt eax,2')), u'BT(eax, 2)')

    def test_instr_1080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btc     cx, dx')), u'BTC(cx, dx)')

    def test_instr_1090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btc     ecx, edx')), u'BTC(ecx, edx)')

    def test_instr_1100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btc eax,0')), u'BTC(eax, 0)')

    def test_instr_1110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btc eax,2')), u'BTC(eax, 2)')

    def test_instr_1120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btr     cx, dx')), u'BTR(cx, dx)')

    def test_instr_1130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btr     ecx, edx')), u'BTR(ecx, edx)')

    def test_instr_1140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btr eax,0')), u'BTR(eax, 0)')

    def test_instr_1150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('btr eax,2')), u'BTR(eax, 2)')

    def test_instr_1160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bts     cx, dx')), u'BTS(cx, dx)')

    def test_instr_1170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bts     ecx, edx')), u'BTS(ecx, edx)')

    def test_instr_1180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bts eax,0')), u'BTS(eax, 0)')

    def test_instr_1190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('bts eax,2')), u'BTS(eax, 2)')

    def test_instr_1200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cbw')), 'CBW')

    def test_instr_1210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cdq')), 'CDQ')

    def test_instr_1220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('clc')), 'CLC')

    def test_instr_1230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cld')), 'CLD')

    def test_instr_1240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmc')), 'CMC')

    def test_instr_1250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     dl, cl')), u'CMP(dl, cl)')

    def test_instr_1260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     dx, cx')), u'CMP(dx, cx)')

    def test_instr_1270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     ebx, ebx')), u'CMP(ebx, ebx)')

    def test_instr_1280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     ebx, edi')), u'CMP(ebx, edi)')

    def test_instr_1290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     ebx, esi')), u'CMP(ebx, esi)')

    def test_instr_1300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     ebx, offset unk_40F064')), u'CMP(ebx, offset(initcall,unk_40f064))')

    def test_instr_1310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     ecx, 1')), u'CMP(ecx, 1)')

    def test_instr_1320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     edi, ebx')), u'CMP(edi, ebx)')

    def test_instr_1330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     edx, 1')), u'CMP(edx, 1)')

    def test_instr_1340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     edx, ecx')), u'CMP(edx, ecx)')

    def test_instr_1350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     esi, ebx')), u'CMP(esi, ebx)')

    def test_instr_1360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     esi, edi')), u'CMP(esi, edi)')

    def test_instr_1370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     esi, esi')), u'CMP(esi, esi)')

    def test_instr_1380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     i, 1000h')), u'CMP(i, 0x1000)')

    def test_instr_1390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     i, 100h')), u'CMP(i, 0x100)')

    def test_instr_1400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     i, 10h')), u'CMP(i, 0x10)')

    def test_instr_1410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     i, 20h')), u'CMP(i, 0x20)')

    def test_instr_1420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp     i, 4')), u'CMP(i, 4)')

    def test_instr_1430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [a],5')), u'CMP(*(a), 5)')

    def test_instr_1440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [var+3],5')), u'CMP(*((var)+3), 5)')

    def test_instr_1450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [var+4],0')), u'CMP(*((var)+4), 0)')

    def test_instr_1460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [var-1],0')), u'CMP(*((var)-1), 0)')

    def test_instr_1470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [bytearray2+5],0')), u'CMP(*((bytearray2)+5), 0)')

    def test_instr_1480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [singlebyte2+1],5')), u'CMP(*((&singlebyte2)+1), 5)')

    def test_instr_1490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [singlebyte2],2')), u'CMP(singlebyte2, 2)')

    def test_instr_1500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [wordarray+2],6')), u'CMP(*(dw*)(((db*)wordarray)+2), 6)')

    def test_instr_1510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [wordarray-1],5')), u'CMP(*(dw*)(((db*)wordarray)-1), 5)')

    def test_instr_1520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [wordarray],4')), u'CMP(*(wordarray), 4)')

    def test_instr_1530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [singlebyte+3*4],40')), u'CMP(*((&singlebyte)+3*4), 40)')

    def test_instr_1540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [singlebyte+ebp],4000000')), u'CMP(*(raddr(ss,offset(_data,singlebyte)+ebp)), 4000000)')

    def test_instr_1550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [bytearray+t],1')), u'CMP(*((bytearray)+t), 1)')

    def test_instr_1560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [bytearray],2')), u'CMP(*(bytearray), 2)')

    def test_instr_1570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp [var],5')), u'CMP(*(var), 5)')

    def test_instr_1580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ah,-1')), u'CMP(ah, -1)')

    def test_instr_1590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ah,0ffh')), u'CMP(ah, 0x0ff)')

    def test_instr_1600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp al,2')), u'CMP(al, 2)')

    def test_instr_1610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp al,ah')), u'CMP(al, ah)')

    def test_instr_1620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ax,-5')), u'CMP(ax, -5)')

    def test_instr_1630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bh,0cch')), u'CMP(bh, 0x0cc)')

    def test_instr_1640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bl,001111111B')), u'CMP(bl, 0x7f)')

    def test_instr_1650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bl,0ddh')), u'CMP(bl, 0x0dd)')

    def test_instr_1660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bl,192')), u'CMP(bl, 192)')

    def test_instr_1670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bl,193')), u'CMP(bl, 193)')

    def test_instr_1680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bl,39h          ; above 9?')), u'CMP(bl, 0x39)')

    def test_instr_1690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bl,al')), u'CMP(bl, al)')

    def test_instr_1700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bx,-1')), u'CMP(bx, -1)')

    def test_instr_1710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bx,1')), u'CMP(bx, 1)')

    def test_instr_1720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bx,4+5*256')), u'CMP(bx, 4+5*256)')

    def test_instr_1730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp bx,6*256+5')), u'CMP(bx, 6*256+5)')

    def test_instr_1740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [a],5')), u'CMP(*(a), 5)')

    def test_instr_1750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [edi+1],6')), u'CMP(*(raddr(ds,edi+1)), 6)')

    def test_instr_1760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [edi+7],132')), u'CMP(*(raddr(ds,edi+7)), 132)')

    def test_instr_1770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [esi],1')), u'CMP(*(raddr(ds,esi)), 1)')

    def test_instr_1780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [esi],4')), u'CMP(*(raddr(ds,esi)), 4)')

    def test_instr_1790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [testOVerlap+1],1')), u'CMP(*((testoverlap)+1), 1)')

    def test_instr_1800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [singlebyte2+1],5')), u'CMP(*((&singlebyte2)+1), 5)')

    def test_instr_1810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr [singlebyte2+2],5')), u'CMP(*((&singlebyte2)+2), 5)')

    def test_instr_1820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr es:[0],55')), u'CMP(*(raddr(es,0)), 55)')

    def test_instr_1830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr es:[0],56')), u'CMP(*(raddr(es,0)), 56)')

    def test_instr_1840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp byte ptr es:[0],57')), u'CMP(*(raddr(es,0)), 57)')

    def test_instr_1850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ch,001111111B')), u'CMP(ch, 0x7f)')

    def test_instr_1860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ch,011111100B')), u'CMP(ch, 0xfc)')

    def test_instr_1870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dl,2')), u'CMP(dl, 2)')

    def test_instr_1880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dl,4')), u'CMP(dl, 4)')

    def test_instr_1890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dl,5')), u'CMP(dl, 5)')

    def test_instr_1900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dword ptr bytearray,11')), u'CMP(*(dd*)((bytearray)), 11)')

    def test_instr_1910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dx,-1')), u'CMP(dx, -1)')

    def test_instr_1920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dx,0')), u'CMP(dx, 0)')

    def test_instr_1930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dx,11')), u'CMP(dx, 11)')

    def test_instr_1940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp dx,5')), u'CMP(dx, 5)')

    def test_instr_1950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,-13')), u'CMP(eax, -13)')

    def test_instr_1960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,-2')), u'CMP(eax, -2)')

    def test_instr_1970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,-5')), u'CMP(eax, -5)')

    def test_instr_1980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0')), u'CMP(eax, 0)')

    def test_instr_1990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,000f3h')), u'CMP(eax, 0x000f3)')

    def test_instr_2000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0101010101010101b')), u'CMP(eax, 0x5555)')

    def test_instr_2010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0101b')), u'CMP(eax, 0x5)')

    def test_instr_2020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,077123456h')), u'CMP(eax, 0x077123456)')

    def test_instr_2030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0ffff0003h')), u'CMP(eax, 0x0ffff0003)')

    def test_instr_2040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0ffff00f3h')), u'CMP(eax, 0x0ffff00f3)')

    def test_instr_2050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0ffffff03h')), u'CMP(eax, 0x0ffffff03)')

    def test_instr_2060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,0fffffff3h')), u'CMP(eax, 0x0fffffff3)')

    def test_instr_2070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,1')), u'CMP(eax, 1)')

    def test_instr_2080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,2')), u'CMP(eax, 2)')

    def test_instr_2090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,256')), u'CMP(eax, 256)')

    def test_instr_2100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,3')), u'CMP(eax, 3)')

    def test_instr_2110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,4')), u'CMP(eax, 4)')

    def test_instr_2120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,5')), u'CMP(eax, 5)')

    def test_instr_2130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,6')), u'CMP(eax, 6)')

    def test_instr_2140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp eax,ebx')), u'CMP(eax, ebx)')

    def test_instr_2150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebp,9')), u'CMP(ebp, 9)')

    def test_instr_2160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,0')), u'CMP(ebx, 0)')

    def test_instr_2170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,010B')), u'CMP(ebx, 0x2)')

    def test_instr_2180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,0ffffff00h')), u'CMP(ebx, 0x0ffffff00)')

    def test_instr_2190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,1')), u'CMP(ebx, 1)')

    def test_instr_2200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,100h')), u'CMP(ebx, 0x100)')

    def test_instr_2210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,12345')), u'CMP(ebx, 12345)')

    def test_instr_2220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,2')), u'CMP(ebx, 2)')

    def test_instr_2230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,3')), u'CMP(ebx, 3)')

    def test_instr_2240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ebx,TWO')), u'CMP(ebx, two)')

    def test_instr_2250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ecx,-5')), u'CMP(ecx, -5)')

    def test_instr_2260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ecx,0af222h')), u'CMP(ecx, 0x0af222)')

    def test_instr_2270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ecx,0dff1h')), u'CMP(ecx, 0x0dff1)')

    def test_instr_2280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ecx,0ffffh')), u'CMP(ecx, 0x0ffff)')

    def test_instr_2290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ecx,3')), u'CMP(ecx, 3)')

    def test_instr_2300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp ecx,5')), u'CMP(ecx, 5)')

    def test_instr_2310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edi,0')), u'CMP(edi, 0)')

    def test_instr_2320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edi,esi')), u'CMP(edi, esi)')

    def test_instr_2330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edi,offset bytearray+1')), u'CMP(edi, offset(_data,bytearray)+1)')

    def test_instr_2340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edi,offset bytearray+4')), u'CMP(edi, offset(_data,bytearray)+4)')

    def test_instr_2350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edx,-2')), u'CMP(edx, -2)')

    def test_instr_2360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edx,0')), u'CMP(edx, 0)')

    def test_instr_2370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edx,0abcdef77h')), u'CMP(edx, 0x0abcdef77)')

    def test_instr_2380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edx,0ffffh')), u'CMP(edx, 0x0ffff)')

    def test_instr_2390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edx,1')), u'CMP(edx, 1)')

    def test_instr_2400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp edx,10')), u'CMP(edx, 10)')

    def test_instr_2410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp esi,0')), u'CMP(esi, 0)')

    def test_instr_2420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp esi,offset singlebyte2+1')), u'CMP(esi, offset(_data,singlebyte2)+1)')

    def test_instr_2430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp esi,offset singlebyte+4')), u'CMP(esi, offset(_data,singlebyte)+4)')

    def test_instr_2440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte2[1],2')), u'CMP(*((&singlebyte2)+1), 2)')

    def test_instr_2450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte2[bx+si],2')), u'CMP(*((&singlebyte2)+bx+si), 2)')

    def test_instr_2460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte2[bx],2')), u'CMP(*((&singlebyte2)+bx), 2)')

    def test_instr_2470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte+3*4,4000000')), u'CMP(*((&singlebyte)+3*4), 4000000)')

    def test_instr_2480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte+ebp,4000000')), u'CMP(*(raddr(ss,offset(_data,singlebyte)+ebp)), 4000000)')

    def test_instr_2490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp word ptr [singlequad+2],25')), u'CMP(*(dw*)(((db*)&singlequad)+2), 25)')

    def test_instr_2500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp word ptr [singlequad+2],50')), u'CMP(*(dw*)(((db*)&singlequad)+2), 50)')

    def test_instr_2510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp word ptr singlequad,0')), u'CMP(*(dw*)(((db*)&singlequad)), 0)')

    def test_instr_2520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpsb')), 'CMPSB')

    def test_instr_2530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpsd')), 'CMPSD')

    def test_instr_2540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpsw')), 'CMPSW')

    def test_instr_2550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg al, dl')), u'CMPXCHG(al, dl)')

    def test_instr_2560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg ax, dx')), u'CMPXCHG(ax, dx)')

    def test_instr_2570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg byte ptr [ebp+var_20], bl')), u'CMPXCHG(*(raddr(ss,ebp+var_20)), bl)')

    def test_instr_2580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg byte ptr [ebp+var_20], dl')), u'CMPXCHG(*(raddr(ss,ebp+var_20)), dl)')

    def test_instr_2590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg cl, dl')), u'CMPXCHG(cl, dl)')

    def test_instr_2600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg cx, dx')), u'CMPXCHG(cx, dx)')

    def test_instr_2610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg dword ptr [ebp+var_20], edx')), u'CMPXCHG(*(dd*)(raddr(ss,ebp+var_20)), edx)')

    def test_instr_2620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg eax, edx')), u'CMPXCHG(eax, edx)')

    def test_instr_2630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg ecx, edx')), u'CMPXCHG(ecx, edx)')

    def test_instr_2640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg word ptr [ebp+var_20], dx')), u'CMPXCHG(*(dw*)(raddr(ss,ebp+var_20)), dx)')

    def test_instr_2650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmpxchg8b [ebp+var_20]')), u'CMPXCHG8B(*(raddr(ss,ebp+var_20)))')

    def test_instr_2660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cwd')), 'CWD')

    def test_instr_2670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cwde')), 'CWDE')

    def test_instr_2680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('daa')), 'DAA')

    def test_instr_2690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('das')), 'DAS')

    def test_instr_2700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('dec     dl')), u'DEC(dl)')

    def test_instr_2710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('dec     dx')), u'DEC(dx)')

    def test_instr_2720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('dec     edx')), u'DEC(edx)')

    def test_instr_2730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('dec cl              ; decrease loop counter')), u'DEC(cl)')

    def test_instr_2740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('dec cx')), u'DEC(cx)')

    def test_instr_2750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('dec eax')), u'DEC(eax)')

    def test_instr_2760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('div     cx')), u'DIV2(cx)')

    def test_instr_2770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('div     dl')), u'DIV1(dl)')

    def test_instr_2780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('div     s1_0')), u'DIV4(s1_0)')

    def test_instr_2790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('idiv    cx')), u'IDIV2(cx)')

    def test_instr_2800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('idiv    dl')), u'IDIV1(dl)')

    def test_instr_2810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('idiv    s1_0')), u'IDIV4(s1_0)')

    def test_instr_2820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    ax, cx')), u'IMUL2_2(ax,cx)')

    def test_instr_2830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    ax, cx, 2Dh')), u'IMUL3_2(ax,cx,0x2D)')

    def test_instr_2840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    ax, di, 8000h')), u'IMUL3_2(ax,di,0x8000)')

    def test_instr_2850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    ax, dx, -2Dh')), u'IMUL3_2(ax,dx,-0x2D)')

    def test_instr_2860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    ax, si, 7FFFh')), u'IMUL3_2(ax,si,0x7FFF)')

    def test_instr_2870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    cl')), u'IMUL1_1(cl)')

    def test_instr_2880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    cx')), u'IMUL1_2(cx)')

    def test_instr_2890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    eax, ecx, 2Dh')), u'IMUL3_4(eax,ecx,0x2D)')

    def test_instr_2900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    eax, edi, 8000h')), u'IMUL3_4(eax,edi,0x8000)')

    def test_instr_2910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    eax, edx, -2Dh')), u'IMUL3_4(eax,edx,-0x2D)')

    def test_instr_2920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    eax, s1_0')), u'IMUL2_4(eax,s1_0)')

    def test_instr_2930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    ebx, esi, 7FFFh')), u'IMUL3_4(ebx,esi,0x7FFF)')

    def test_instr_2940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('imul    s1_0')), u'IMUL1_4(s1_0)')

    def test_instr_2950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc     dl')), u'INC(dl)')

    def test_instr_2960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc     dx')), u'INC(dx)')

    def test_instr_2980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc     i')), u'INC(i)')

    def test_instr_2990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc byte ptr [edi+1]')), u'INC(*(raddr(ds,edi+1)))')

    def test_instr_3000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc byte ptr [edi+7]')), u'INC(*(raddr(ds,edi+7)))')

    def test_instr_3010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc byte ptr es:[0]')), u'INC(*(raddr(es,0)))')

    def test_instr_3020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc eax')), u'INC(eax)')

    def test_instr_3030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc ebx')), u'INC(ebx)')

    def test_instr_3040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc ecx')), u'INC(ecx)')

    def test_instr_3050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc edi              ; increase target address')), u'INC(edi)')

    def test_instr_3060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc edi')), u'INC(edi)')

    def test_instr_3070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc edx')), u'INC(edx)')

    def test_instr_3080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('int 10h')), u'_INT(0x10)')

    def test_instr_3090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('int 21h                         ; DOS INT 21h')), u'_INT(0x21)')

    def test_instr_3100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('int 31h')), u'_INT(0x31)')

    def test_instr_3120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jNC OK')), u'JNC(ok)')

    def test_instr_3130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('ja      short loc_407784')), u'JA(loc_407784)')

    def test_instr_3150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnbe failure')), u'JA(failure)')

    def test_instr_3160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jb      short loc_40723E')), u'JC(loc_40723e)')

    def test_instr_3170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jb failure  ; // because unsigned comparaiso\n')), u'JC(failure)')

    def test_instr_3180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jbe     short loc_40752C')), u'JBE(loc_40752c)')

    def test_instr_3190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jc failure')), u'JC(failure)')

    def test_instr_3200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jcxz    loc_4081F6')), u'JCXZ(loc_4081f6)')

    def test_instr_3210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jcxz @df@@@@7')), u'JCXZ(arbdfarbarbarbarb7)')

    def test_instr_3220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jcxz failure')), u'JCXZ(failure)')

    def test_instr_3230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('je failure ; http://blog.rewolf.pl/blog/?p=177')), u'JZ(failure)')

    def test_instr_3240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('je failure')), u'JZ(failure)')

    def test_instr_3250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('je ok')), u'JZ(ok)')

    def test_instr_3260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jecxz   short loc_4083E9')), u'JECXZ(loc_4083e9)')

    def test_instr_3270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jg      short loc_40707C')), u'JG(loc_40707c)')

    def test_instr_3280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jg @df@@@@1')), u'JG(arbdfarbarbarbarb1)')

    def test_instr_3290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jg failure')), u'JG(failure)')

    def test_instr_3300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jge     short loc_406EBA')), u'JGE(loc_406eba)')

    def test_instr_3310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jge @df@@@@2')), u'JGE(arbdfarbarbarbarb2)')

    def test_instr_3320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jge failure')), u'JGE(failure)')

    def test_instr_3330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jl      short loc_406B3F')), u'JL(loc_406b3f)')

    def test_instr_3340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jl @df@@@@4')), u'JL(arbdfarbarbarbarb4)')

    def test_instr_3350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jl failure')), u'JL(failure)')

    def test_instr_3360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jle     short loc_406CF8')), u'JLE(loc_406cf8)')

    def test_instr_3370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jle @df@@@@5')), u'JLE(arbdfarbarbarbarb5)')

    def test_instr_3380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jle failure')), u'JLE(failure)')

    def test_instr_3390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp     exec_rclb')), u'JMP(exec_rclb)')

    def test_instr_3400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp     short loc_40D571')), u'JMP(loc_40d571)')

    def test_instr_3410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp exitLabel')), u'JMP(exitlabel)')

    def test_instr_3420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp failure')), u'JMP(failure)')

    def test_instr_3430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp finTest')), u'JMP(fintest)')

    def test_instr_3440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp next')), u'JMP(next)')

    def test_instr_3450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnC failure')), u'JNC(failure)')

    def test_instr_3460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jna short P2')), u'JBE(p2)')

    def test_instr_3470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnb     short loc_4075C2')), u'JNC(loc_4075c2)')

    def test_instr_3480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnb     short loc_407658')), u'JNC(loc_407658)')

    def test_instr_3490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnb     short loc_4076EE')), u'JNC(loc_4076ee)')

    def test_instr_3500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnb failure')), u'JNC(failure)')

    def test_instr_3520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnc noerror')), u'JNC(noerror)')

    def test_instr_3530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jne exitLabel')), u'JNZ(exitlabel)')

    def test_instr_3540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jne failure')), u'JNZ(failure)')

    def test_instr_3550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jns     short loc_408008')), u'JNS(loc_408008)')

    def test_instr_3560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jns     short loc_40809E')), u'JNS(loc_40809e)')

    def test_instr_3570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jns     short loc_408139')), u'JNS(loc_408139)')

    def test_instr_3580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jns failure')), u'JNS(failure)')

    def test_instr_3590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnz     loc_409652')), u'JNZ(loc_409652)')

    def test_instr_3600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnz     short loc_4046D6')), u'JNZ(loc_4046d6)')

    def test_instr_3610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnz P1              ; jump if cl is not equal 0 (zeroflag is not set)')), u'JNZ(p1)')

    def test_instr_3620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jnz failure')), u'JNZ(failure)')

    def test_instr_3630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('js      short loc_407E46')), u'JS(loc_407e46)')

    def test_instr_3640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('js      short loc_407F72')), u'JS(loc_407f72)')

    def test_instr_3650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('js @df@@@@')), u'JS(arbdfarbarbarbarb)')

    def test_instr_3660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('js failure')), u'JS(failure)')

    def test_instr_3670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jz      short loc_40458F')), u'JZ(loc_40458f)')

    def test_instr_3680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jz failure')), u'JZ(failure)')

    def test_instr_3690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [eax+4000h]')), u'eax = eax+0x4000')

    def test_instr_3700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [eax+40h]')), u'eax = eax+0x40')

    def test_instr_3710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [eax+ecx+40h]')), u'eax = eax+ecx+0x40')

    def test_instr_3720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [eax+ecx]')), u'eax = eax+ecx')

    def test_instr_3730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [eax]')), u'eax = eax')

    def test_instr_3740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ebx+4000h]')), u'eax = ebx+0x4000')

    def test_instr_3750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ebx+40h]')), u'eax = ebx+0x40')

    def test_instr_3760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ebx+edx+4000h]')), u'eax = ebx+edx+0x4000')

    def test_instr_3770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ebx+edx]')), u'eax = ebx+edx')

    def test_instr_3780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ebx]')), u'eax = ebx')

    def test_instr_3790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx+4000h]')), u'eax = ecx+0x4000')

    def test_instr_3800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx+40h]')), u'eax = ecx+0x40')

    def test_instr_3810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx+ecx*2+4000h]')), u'eax = ecx+ecx*2+0x4000')

    def test_instr_3820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx+ecx*2-0Ah]')), u'eax = ecx+ecx*2-0x0A')

    def test_instr_3830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx+ecx*2]')), u'eax = ecx+ecx*2')

    def test_instr_3840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx+ecx]')), u'eax = ecx+ecx')

    def test_instr_3850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [ecx]')), u'eax = ecx')

    def test_instr_3860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edi+4000h]')), u'eax = edi+0x4000')

    def test_instr_3870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edi+40h]')), u'eax = edi+0x40')

    def test_instr_3880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edi+ecx]')), u'eax = edi+ecx')

    def test_instr_3890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edi]')), u'eax = edi')

    def test_instr_3900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx+4000h]')), u'eax = edx+0x4000')

    def test_instr_3910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx+40h]')), u'eax = edx+0x40')

    def test_instr_3920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx+ecx*4+4000h]')), u'eax = edx+ecx*4+0x4000')

    def test_instr_3930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx+ecx*4-0Ah]')), u'eax = edx+ecx*4-0x0A')

    def test_instr_3940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx+ecx*4]')), u'eax = edx+ecx*4')

    def test_instr_3950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx+ecx]')), u'eax = edx+ecx')

    def test_instr_3960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [edx]')), u'eax = edx')

    def test_instr_3970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [esi+4000h]')), u'eax = esi+0x4000')

    def test_instr_3980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [esi+40h]')), u'eax = esi+0x40')

    def test_instr_3990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [esi+ecx*8-0Ah]')), u'eax = esi+ecx*8-0x0A')

    def test_instr_4000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [esi+ecx*8]')), u'eax = esi+ecx*8')

    def test_instr_4010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [esi+ecx]')), u'eax = esi+ecx')

    def test_instr_4020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, [esi]')), u'eax = esi')

    def test_instr_4030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, ds:0[eax*2]')), u'eax = 0+eax*2')

    def test_instr_4040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, ds:0[ebx*4]')), u'eax = 0+ebx*4')

    def test_instr_4050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, ds:0[ecx*8]')), u'eax = 0+ecx*8')

    def test_instr_4060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     ebx, [ebp+table]')), u'ebx = ebp+offset(_text,table)')

    def test_instr_4070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     ebx, [esi+ecx*8+4000h]')), u'ebx = esi+ecx*8+0x4000')

    def test_instr_4080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edi, [ebp+ecx_vals]')), u'edi = ebp+ecx_vals')

    def test_instr_4090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edi, [i+2]')), u'edi = i+2')

    def test_instr_4100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edi, [i+3]')), u'edi = i+3')

    def test_instr_4110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edi, [i+4]')), u'edi = i+4')

    def test_instr_4120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edi, [i+5]')), u'edi = i+5')

    def test_instr_4130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edi, [i-10h]')), u'edi = i-0x10')

    def test_instr_4140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     edx, [i+56h]')), u'edx = i+0x56')

    def test_instr_4150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     esi, [i+1]')), u'esi = i+1')

    def test_instr_4160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea eax,enddata')), u'eax = offset(_data,enddata)')

    def test_instr_4170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea ebx,beginningdata')), u'ebx = offset(_data,beginningdata)')

    def test_instr_4180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea edi,buffer')), u'edi = offset(_data,buffer)')

    def test_instr_4190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea edi,f')), u'edi = offset(_data,f)')

    def test_instr_4200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea edi,testOVerlap')), u'edi = offset(_data,testoverlap)')

    def test_instr_4210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea edi,singlebyte2')), u'edi = offset(_data,singlebyte2)')

    def test_instr_4220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea edx,fileName')), u'edx = offset(_data,filename)')

    def test_instr_4230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea esi,b')), u'esi = b')

    def test_instr_4240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea esi,f')), u'esi = offset(_data,f)')

    def test_instr_4250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea esi,wordarray')), u'esi = offset(_data,wordarray)')

    def test_instr_4260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea esi,singlequad')), u'esi = offset(_data,singlequad)')

    def test_instr_4270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('leave')), 'LEAVE')

    def test_instr_4280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lodsb')), 'LODSB')

    def test_instr_4290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lodsd')), 'LODSD')

    def test_instr_4300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lodsw')), 'LODSW')

    def test_instr_4310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('loop    loc_408464')), u'LOOP(loc_408464)')

    def test_instr_4320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('loop dffd')), u'LOOP(dffd)')

    def test_instr_4330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('loope   loc_4084DF')), u'LOOPE(loc_4084df)')

    def test_instr_4340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('loope toto1')), u'LOOPE(toto1)')

    def test_instr_4350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('loopne  loc_40855A')), u'LOOPNE(loc_40855a)')

    def test_instr_4360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+ecx_0], ecx_0_0')), u'MOV(*(dd*)(raddr(ss,ebp+ecx_0)), ecx_0_0)')

    def test_instr_4370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+edx_0], edx')), u'MOV(*(dd*)(raddr(ss,ebp+edx_0)), edx)')

    def test_instr_4380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+s0], esi')), u'MOV(*(dd*)(raddr(ss,ebp+s0)), esi)')

    def test_instr_4390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+s1], 0')), u'MOV(*(raddr(ss,ebp+s1)), 0)')

    def test_instr_4400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+s1], 1')), u'MOV(*(raddr(ss,ebp+s1)), 1)')

    def test_instr_4410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+s2], ebx')), u'MOV(*(dd*)(raddr(ss,ebp+s2)), ebx)')

    def test_instr_4420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+var_1C], edx')), u'MOV(*(dd*)(raddr(ss,ebp+var_1c)), edx)')

    def test_instr_4430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [ebp+var_20], ecx')), u'MOV(*(dd*)(raddr(ss,ebp+var_20)), ecx)')

    def test_instr_4440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], ebx')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), ebx)')

    def test_instr_4450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], ecx')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), ecx)')

    def test_instr_4460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], edi')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), edi)')

    def test_instr_4470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], edi_0')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), edi_0)')

    def test_instr_4480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], edx')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), edx)')

    def test_instr_4490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], op0')), u'MOV(*(raddr(ss,esp+0x0C)), op0)')

    def test_instr_4500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], op1')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), op1)')

    def test_instr_4510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], r')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), r)')

    def test_instr_4520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], res')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), res)')

    def test_instr_4530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], resz')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), resz)')

    def test_instr_4540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+0Ch], s1_0')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), s1_0)')

    def test_instr_4550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], eax')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), eax)')

    def test_instr_4560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], eax_0')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), eax_0)')

    def test_instr_4570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], ebx')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), ebx)')

    def test_instr_4580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], ecx')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), ecx)')

    def test_instr_4590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], op1')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), op1)')

    def test_instr_4600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], res')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), res)')

    def test_instr_4610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], resz')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), resz)')

    def test_instr_4620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], rh')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), rh)')

    def test_instr_4630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+10h], s1_0')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), s1_0)')

    def test_instr_4640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], eax')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), eax)')

    def test_instr_4650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], ebx')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), ebx)')

    def test_instr_4660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], ecx')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), ecx)')

    def test_instr_4670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], ecx_0')), u'MOV(*(raddr(ss,esp+0x14)), ecx_0)')

    def test_instr_4680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], edi')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), edi)')

    def test_instr_4690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], edx')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), edx)')

    def test_instr_4700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], esi')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), esi)')

    def test_instr_4710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], flags')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), flags)')

    def test_instr_4720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], res')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), res)')

    def test_instr_4730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+14h], resh')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), resh)')

    def test_instr_4740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+18h], eax')), u'MOV(*(dd*)(raddr(ss,esp+0x18)), eax)')

    def test_instr_4750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+18h], edi')), u'MOV(*(dd*)(raddr(ss,esp+0x18)), edi)')

    def test_instr_4760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+18h], edx')), u'MOV(*(dd*)(raddr(ss,esp+0x18)), edx)')

    def test_instr_4770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+18h], res')), u'MOV(*(dd*)(raddr(ss,esp+0x18)), res)')

    def test_instr_4780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+1Ch], eax')), u'MOV(*(dd*)(raddr(ss,esp+0x1C)), eax)')

    def test_instr_4790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+1Ch], ebx')), u'MOV(*(dd*)(raddr(ss,esp+0x1C)), ebx)')

    def test_instr_4800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], eax_0')), u'MOV(*(dd*)(raddr(ss,esp+4)), eax_0)')

    def test_instr_4810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], ebx    ; s0')), u'MOV(*(dd*)(raddr(ss,esp+4)), ebx)')

    def test_instr_4820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], edi    ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), edi)')

    def test_instr_4830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], esi    ; s0')), u'MOV(*(dd*)(raddr(ss,esp+4)), esi)')

    def test_instr_4840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], esi    ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), esi)')

    def test_instr_4850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], i      ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), i)')

    def test_instr_4860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+4], res')), u'MOV(*(dd*)(raddr(ss,esp+4)), res)')

    def test_instr_4870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], eax')), u'MOV(*(dd*)(raddr(ss,esp+8)), eax)')

    def test_instr_4880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], ebx    ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), ebx)')

    def test_instr_4890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], ebx')), u'MOV(*(dd*)(raddr(ss,esp+8)), ebx)')

    def test_instr_4900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], ecx')), u'MOV(*(dd*)(raddr(ss,esp+8)), ecx)')

    def test_instr_4910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], ecx_0_0')), u'MOV(*(dd*)(raddr(ss,esp+8)), ecx_0_0)')

    def test_instr_4920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], edi    ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), edi)')

    def test_instr_4930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], edi    ; s1')), u'MOV(*(dd*)(raddr(ss,esp+8)), edi)')

    def test_instr_4940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], edx_0_0')), u'MOV(*(dd*)(raddr(ss,esp+8)), edx_0_0)')

    def test_instr_4950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], esi    ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), esi)')

    def test_instr_4960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], esi    ; s1')), u'MOV(*(dd*)(raddr(ss,esp+8)), esi)')

    def test_instr_4970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], esi')), u'MOV(*(dd*)(raddr(ss,esp+8)), esi)')

    def test_instr_4980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], esi_0')), u'MOV(*(dd*)(raddr(ss,esp+8)), esi_0)')

    def test_instr_4990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], i      ; s1')), u'MOV(*(dd*)(raddr(ss,esp+8)), i)')

    def test_instr_5000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], i')), u'MOV(*(dd*)(raddr(ss,esp+8)), i)')

    def test_instr_5010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], op0')), u'MOV(*(raddr(ss,esp+8)), op0)')

    def test_instr_5020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], res')), u'MOV(*(dd*)(raddr(ss,esp+8)), res)')

    def test_instr_5030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], resh')), u'MOV(*(dd*)(raddr(ss,esp+8)), resh)')

    def test_instr_5040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], s0_0')), u'MOV(*(dd*)(raddr(ss,esp+8)), s0_0)')

    def test_instr_5050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp], ebx      ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), ebx)')

    def test_instr_5060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp], ebx      ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), ebx)')

    def test_instr_5070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp], edi      ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), edi)')

    def test_instr_5080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dl, al')), u'MOV(dl, al)')

    def test_instr_5090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [ebp+var_20+4], 0FBCA7h')), u'MOV(*(dd*)(raddr(ss,ebp+var_20+4)), 0x0FBCA7)')

    def test_instr_5100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [ebp+var_20+4], 12345h')), u'MOV(*(dd*)(raddr(ss,ebp+var_20+4)), 0x12345)')

    def test_instr_5110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [ebp+var_20], 0FBCA7654h')), u'MOV(*(dd*)(raddr(ss,ebp+var_20)), 0x0FBCA7654)')

    def test_instr_5120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [ebp+var_20], 65423456h')), u'MOV(*(dd*)(raddr(ss,ebp+var_20)), 0x65423456)')

    def test_instr_5130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [ebp+var_20], 6789ABCDh')), u'MOV(*(dd*)(raddr(ss,ebp+var_20)), 0x6789ABCD)')

    def test_instr_5140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 0 ; iflags')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 0)')

    def test_instr_5150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 0')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 0)')

    def test_instr_5160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 1 ; iflags')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 1)')

    def test_instr_5170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 1000h')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x1000)')

    def test_instr_5180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 1234h')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x1234)')

    def test_instr_5190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 17h')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x17)')

    def test_instr_5200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+0Ch], 80000000h')), u'MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x80000000)')

    def test_instr_5210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+10h], 0')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), 0)')

    def test_instr_5220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+10h], 1')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), 1)')

    def test_instr_5230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+10h], 10h')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), 0x10)')

    def test_instr_5240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+10h], 11h')), u'MOV(*(dd*)(raddr(ss,esp+0x10)), 0x11)')

    def test_instr_5250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+14h], 0')), u'MOV(*(dd*)(raddr(ss,esp+0x14)), 0)')

    def test_instr_5260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+1Ch], 0')), u'MOV(*(dd*)(raddr(ss,esp+0x1C)), 0)')

    def test_instr_5270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 0 ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0)')

    def test_instr_5300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 0FFFC70F9h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x0FFFC70F9)')

    def test_instr_5310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 0FFFFFFD3h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x0FFFFFFD3)')

    def test_instr_5320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 0FFFFFFFFh ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x0FFFFFFFF)')

    def test_instr_5350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 10000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x10000)')

    def test_instr_5390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 100h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x100)')

    def test_instr_5400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 10h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x10)')

    def test_instr_5410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 1234001Dh ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x1234001D)')

    def test_instr_5420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 12341h ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x12341)')

    def test_instr_5430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 12345678h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x12345678)')

    def test_instr_5440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 12345678h ; s0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x12345678)')

    def test_instr_5450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 12348000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x12348000)')

    def test_instr_5460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 127Eh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x127E)')

    def test_instr_5470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 17h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x17)')

    def test_instr_5480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 1FF7Fh ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x1FF7F)')

    def test_instr_5490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 1FF80h ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x1FF80)')

    def test_instr_5500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 1FF81h ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x1FF81)')

    def test_instr_5510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 1FFFFh ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x1FFFF)')

    def test_instr_5520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 2 ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 2)')

    def test_instr_5530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 2 ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 2)')

    def test_instr_5540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 20000h ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x20000)')

    def test_instr_5550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 2Dh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x2D)')

    def test_instr_5560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 3 ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 3)')

    def test_instr_5570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 3 ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 3)')

    def test_instr_5580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 4 ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 4)')

    def test_instr_5590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 7FFFFFFFh ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x7FFFFFFF)')

    def test_instr_5600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 80000000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x80000000)')

    def test_instr_5610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 80000000h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x80000000)')

    def test_instr_5620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 80000001h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x80000001)')

    def test_instr_5630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 80008688h ; s0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x80008688)')

    def test_instr_5640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 8000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x8000)')

    def test_instr_5650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 8000h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x8000)')

    def test_instr_5660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 80h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x80)')

    def test_instr_5670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 80h ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x80)')

    def test_instr_5680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 812FADAh ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x812FADA)')

    def test_instr_5690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 81h ; s1')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x81)')

    def test_instr_5700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], 82345679h ; s0')), u'MOV(*(dd*)(raddr(ss,esp+4)), 0x82345679)')

    def test_instr_5710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+4], offset aXorw ; "xorw"')), u'MOV(*(dd*)(raddr(ss,esp+4)), offset(_rdata,axorw))')

    def test_instr_5720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0 ; iflags')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0)')

    def test_instr_5730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0 ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0)')

    def test_instr_5740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0)')

    def test_instr_5750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FBCA7654h')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FBCA7654)')

    def test_instr_5760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFFFF)')

    def test_instr_5770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFFFFFFh')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFFFF)')

    def test_instr_5780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFFF)')

    def test_instr_5790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFF)')

    def test_instr_5800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFF)')

    def test_instr_5810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFF)')

    def test_instr_5820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFF)')

    def test_instr_5830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0FFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0FF)')

    def test_instr_5840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 0Fh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x0F)')

    def test_instr_5850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1 ; iflags')), u'MOV(*(dd*)(raddr(ss,esp+8)), 1)')

    def test_instr_5860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1 ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 1)')

    def test_instr_5870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 10000h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x10000)')

    def test_instr_5880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 100h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x100)')

    def test_instr_5890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 12340128h')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x12340128)')

    def test_instr_5900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 12Ch ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x12C)')

    def test_instr_5910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1FFFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFFFFF)')

    def test_instr_5920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1FFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFFFF)')

    def test_instr_5930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1FFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFFF)')

    def test_instr_5940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1FFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFF)')

    def test_instr_5950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1FFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFF)')

    def test_instr_5960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1FFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1FF)')

    def test_instr_5970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 1Fh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x1F)')

    def test_instr_5980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 2 ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 2)')

    def test_instr_5990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 2Dh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x2D)')

    def test_instr_6000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 2Dh')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x2D)')

    def test_instr_6010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3 ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 3)')

    def test_instr_6020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 303Bh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x303B)')

    def test_instr_6030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 340128h')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x340128)')

    def test_instr_6040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3FFFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFFFFF)')

    def test_instr_6050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3FFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFFFF)')

    def test_instr_6060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3FFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFFF)')

    def test_instr_6070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3FFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFF)')

    def test_instr_6080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3FFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFF)')

    def test_instr_6090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3FFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3FF)')

    def test_instr_6100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 3Fh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x3F)')

    def test_instr_6110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFFFF)')

    def test_instr_6120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFFFFFh')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFFFF)')

    def test_instr_6130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFFF)')

    def test_instr_6140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFF)')

    def test_instr_6150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFF)')

    def test_instr_6160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFF)')

    def test_instr_6170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFFh')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFF)')

    def test_instr_6180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7FFh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7FF)')

    def test_instr_6190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 7Fh ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x7F)')

    def test_instr_6200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 80000000h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x80000000)')

    def test_instr_6210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 8000h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x8000)')

    def test_instr_6220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 8000h')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x8000)')

    def test_instr_6230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 81234567h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x81234567)')

    def test_instr_6240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 81238567h ; op1')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x81238567)')

    def test_instr_6250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp+8], 8234A6F8h')), u'MOV(*(dd*)(raddr(ss,esp+8)), 0x8234A6F8)')

    def test_instr_6260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0 ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0)')

    def test_instr_6270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0 ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), 0)')

    def test_instr_6280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0Eh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0E)')

    def test_instr_6290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FE)')

    def test_instr_6300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFE)')

    def test_instr_6310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFE0080h ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFE0080)')

    def test_instr_6320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFE0080h ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFE0080)')

    def test_instr_6330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFE)')

    def test_instr_6340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFE)')

    def test_instr_6350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFE)')

    def test_instr_6360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFECh ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFEC)')

    def test_instr_6370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFECh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFEC)')

    def test_instr_6380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFE)')

    def test_instr_6390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFFDh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFD)')

    def test_instr_6400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFE)')

    def test_instr_6410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFFFh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFF)')

    def test_instr_6420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFFFh ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFF)')

    def test_instr_6430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 0FFFFFFFFh ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFF)')

    def test_instr_6440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1 ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 1)')

    def test_instr_6450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 10000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x10000)')

    def test_instr_6460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 100h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x100)')

    def test_instr_6470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 10h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x10)')

    def test_instr_6480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 12340004h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x12340004)')

    def test_instr_6490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 12341h ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x12341)')

    def test_instr_6500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 12343h ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x12343)')

    def test_instr_6510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1234561Dh ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1234561D)')

    def test_instr_6520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 14h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x14)')

    def test_instr_6530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 14h ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x14)')

    def test_instr_6540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 17h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x17)')

    def test_instr_6550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1Eh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1E)')

    def test_instr_6560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1FEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1FE)')

    def test_instr_6570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1FFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1FFE)')

    def test_instr_6580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1FFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1FFFE)')

    def test_instr_6590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1FFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1FFFFE)')

    def test_instr_6600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1FFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1FFFFFE)')

    def test_instr_6610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 1FFFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x1FFFFFFE)')

    def test_instr_6620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 2 ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 2)')

    def test_instr_6630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 21AD3D34h ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), 0x21AD3D34)')

    def test_instr_6640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3 ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 3)')

    def test_instr_6650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3 ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 3)')

    def test_instr_6660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3Eh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3E)')

    def test_instr_6670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3FEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3FE)')

    def test_instr_6680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3FFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3FFE)')

    def test_instr_6690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3FFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3FFFE)')

    def test_instr_6700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3FFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3FFFFE)')

    def test_instr_6710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3FFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3FFFFFE)')

    def test_instr_6720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 3FFFFFFEh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x3FFFFFFE)')

    def test_instr_6730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 4 ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 4)')

    def test_instr_6740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 43210123h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x43210123)')

    def test_instr_6750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 7Eh ; op0h')), u'MOV(*(dd*)(raddr(ss,esp)), 0x7E)')

    def test_instr_6760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 7FFFFFFFh ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x7FFFFFFF)')

    def test_instr_6770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 80000000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x80000000)')

    def test_instr_6780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 80000000h ; s0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x80000000)')

    def test_instr_6790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 80008481h ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), 0x80008481)')

    def test_instr_6800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 8000h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x8000)')

    def test_instr_6810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 80h ; op0')), u'MOV(*(dd*)(raddr(ss,esp)), 0x80)')

    def test_instr_6820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], 813F3421h ; s2')), u'MOV(*(dd*)(raddr(ss,esp)), 0x813F3421)')

    def test_instr_6830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], offset a10sA08lxB08lx ; "%-10s A=%08lx B=%08lx"')), u'MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10sa08lxb08lx))')

    def test_instr_6840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], offset a10sAh08lxAl08l ; "%-10s AH=%08lx AL=%08lx B=%08lx RH=%08l"...')), u'MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10sah08lxal08l))')

    def test_instr_6850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], offset a10sD ; "%-10s %d"')), u'MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10sd))')

    def test_instr_6860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dword ptr [esp], offset a10sEax08lxA08l ; "%-10s EAX=%08lx A=%08lx C=%08lx CC=%02l"...')), u'MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10seax08lxa08l))')

    def test_instr_6870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, 0')), u'MOV(eax, 0)')

    def test_instr_6880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, 0FFFF7FFFh')), u'MOV(eax, 0x0FFFF7FFF)')

    def test_instr_6890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, 1')), u'MOV(eax, 1)')

    def test_instr_6900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, 12340407h')), u'MOV(eax, 0x12340407)')

    def test_instr_6910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, 7FFFFFFFh')), u'MOV(eax, 0x7FFFFFFF)')

    def test_instr_6920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, dword ptr [ebp+var_20]')), u'MOV(eax, *(dd*)(raddr(ss,ebp+var_20)))')

    def test_instr_6930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, ebx')), u'MOV(eax, ebx)')

    def test_instr_6940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, edi')), u'MOV(eax, edi)')

    def test_instr_6950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, edx')), u'MOV(eax, edx)')

    def test_instr_6960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, esi')), u'MOV(eax, esi)')

    def test_instr_6970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, flags')), u'MOV(eax, flags)')

    def test_instr_6980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, res')), u'MOV(eax, res)')

    def test_instr_6990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     eax, s0_0')), u'MOV(eax, s0_0)')

    def test_instr_7000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebp, esp')), u'MOV(ebp, esp)')

    def test_instr_7010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, (offset str_buffer+800h)')), u'MOV(ebx, offset(_bss,str_buffer)+0x800)')

    def test_instr_7020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, 1')), u'MOV(ebx, 1)')

    def test_instr_7030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, 1234040Ah')), u'MOV(ebx, 0x1234040A)')

    def test_instr_7040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, 12340506h')), u'MOV(ebx, 0x12340506)')

    def test_instr_7050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, 12345678h')), u'MOV(ebx, 0x12345678)')

    def test_instr_7060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, 2')), u'MOV(ebx, 2)')

    def test_instr_7070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, 8234A6F8h')), u'MOV(ebx, 0x8234A6F8)')

    def test_instr_7080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, [ebp+iflags]')), u'MOV(ebx, *(dd*)(raddr(ss,ebp+iflags)))')

    def test_instr_7090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, [ebp+op0h]')), u'MOV(ebx, *(dd*)(raddr(ss,ebp+op0h)))')

    def test_instr_7100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, [ebp+s0]')), u'MOV(ebx, *(dd*)(raddr(ss,ebp+s0)))')

    def test_instr_7110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, [ebp+s2]')), u'MOV(ebx, *(dd*)(raddr(ss,ebp+s2)))')

    def test_instr_7120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, [ebp+var_4]')), u'MOV(ebx, *(dd*)(raddr(ss,ebp+var_4)))')

    def test_instr_7130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, dword ptr [ebp+var_20+4]')), u'MOV(ebx, *(dd*)(raddr(ss,ebp+var_20+4)))')

    def test_instr_7140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, edi')), u'MOV(ebx, edi)')

    def test_instr_7150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, i')), u'MOV(ebx, i)')

    def test_instr_7160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, 1')), u'MOV(ecx, 1)')

    def test_instr_7170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, 10h')), u'MOV(ecx, 0x10)')

    def test_instr_7180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, 11h')), u'MOV(ecx, 0x11)')

    def test_instr_7190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, 1234h')), u'MOV(ecx, 0x1234)')

    def test_instr_7200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, 4')), u'MOV(ecx, 4)')

    def test_instr_7210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, 65324h')), u'MOV(ecx, 0x65324)')

    def test_instr_7220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, [ebp+ecx_0]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+ecx_0)))')

    def test_instr_7230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, [ebp+edx_0]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+edx_0)))')

    def test_instr_7240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, [ebp+i*4+ecx_vals]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+i*4+ecx_vals)))')

    def test_instr_7250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, [ebp+s0]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+s0)))')

    def test_instr_7260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, [ebp+s1]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+s1)))')

    def test_instr_7270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, [ebp+var_20]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+var_20)))')

    def test_instr_7280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, dword ptr [ebp+var_20+4]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+var_20+4)))')

    def test_instr_7290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, dword ptr [ebp+var_20]')), u'MOV(ecx, *(dd*)(raddr(ss,ebp+var_20)))')

    def test_instr_7300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, edi')), u'MOV(ecx, edi)')

    def test_instr_7310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ecx, res')), u'MOV(ecx, res)')

    def test_instr_7320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, (offset str_buffer+810h)')), u'MOV(edi, offset(_bss,str_buffer)+0x810)')

    def test_instr_7330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 0FBCA7654h')), u'MOV(edi, 0x0FBCA7654)')

    def test_instr_7340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 0FFFFFFF7h')), u'MOV(edi, 0x0FFFFFFF7)')

    def test_instr_7350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 1')), u'MOV(edi, 1)')

    def test_instr_7360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 12340128h')), u'MOV(edi, 0x12340128)')

    def test_instr_7370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 12340205h')), u'MOV(edi, 0x12340205)')

    def test_instr_7380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 123405A0h')), u'MOV(edi, 0x123405A0)')

    def test_instr_7390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 12345h')), u'MOV(edi, 0x12345)')

    def test_instr_7400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 20h')), u'MOV(edi, 0x20)')

    def test_instr_7410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, 80000000h')), u'MOV(edi, 0x80000000)')

    def test_instr_7420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, [ebp+iflags]')), u'MOV(edi, *(dd*)(raddr(ss,ebp+iflags)))')

    def test_instr_7430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, [ebp+op0]')), u'MOV(edi, *(dd*)(raddr(ss,ebp+op0)))')

    def test_instr_7440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, [ebp+s1]')), u'MOV(edi, *(dd*)(raddr(ss,ebp+s1)))')

    def test_instr_7450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi, [ebp+s2]')), u'MOV(edi, *(dd*)(raddr(ss,ebp+s2)))')

    def test_instr_7460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edi_0, (offset str_buffer+810h)')), u'MOV(edi_0, offset(_bss,str_buffer)+0x810)')

    def test_instr_7470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 1')), u'MOV(edx, 1)')

    def test_instr_7480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 10h')), u'MOV(edx, 0x10)')

    def test_instr_7490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 11h')), u'MOV(edx, 0x11)')

    def test_instr_7500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 12340507h')), u'MOV(edx, 0x12340507)')

    def test_instr_7510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 12345678h')), u'MOV(edx, 0x12345678)')

    def test_instr_7520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 17h')), u'MOV(edx, 0x17)')

    def test_instr_7530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 340128h')), u'MOV(edx, 0x340128)')

    def test_instr_7540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, 8')), u'MOV(edx, 8)')

    def test_instr_7550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, [ebp+s1]')), u'MOV(edx, *(dd*)(raddr(ss,ebp+s1)))')

    def test_instr_7560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, [ebp+var_1C]')), u'MOV(edx, *(dd*)(raddr(ss,ebp+var_1c)))')

    def test_instr_7570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, dword ptr [ebp+var_20]')), u'MOV(edx, *(dd*)(raddr(ss,ebp+var_20)))')

    def test_instr_7580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, ebx')), u'MOV(edx, ebx)')

    def test_instr_7590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, edi')), u'MOV(edx, edi)')

    def test_instr_7600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, esi')), u'MOV(edx, esi)')

    def test_instr_7610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, res')), u'MOV(edx, res)')

    def test_instr_7620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, resh')), u'MOV(edx, resh)')

    def test_instr_7630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     edx, dword ptr [ebp+var_20]')), u'MOV(edx, *(dd*)(raddr(ss,ebp+var_20)))')

    def test_instr_7640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, 0FFFEFDFCh')), u'MOV(esi, 0x0FFFEFDFC)')

    def test_instr_7650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, 1000h')), u'MOV(esi, 0x1000)')

    def test_instr_7660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, 10h')), u'MOV(esi, 0x10)')

    def test_instr_7670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, 12340306h')), u'MOV(esi, 0x12340306)')

    def test_instr_7680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, [ebp+iflags]')), u'MOV(esi, *(dd*)(raddr(ss,ebp+iflags)))')

    def test_instr_7690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, [ebp+op0]')), u'MOV(esi, *(dd*)(raddr(ss,ebp+op0)))')

    def test_instr_7700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, [ebp+op0h]')), u'MOV(esi, *(dd*)(raddr(ss,ebp+op0h)))')

    def test_instr_7710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, [ebp+s0]')), u'MOV(esi, *(dd*)(raddr(ss,ebp+s0)))')

    def test_instr_7720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, [ebp+s1]')), u'MOV(esi, *(dd*)(raddr(ss,ebp+s1)))')

    def test_instr_7730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, esi_0')), u'MOV(esi, esi_0)')

    def test_instr_7740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi, offset unk_40E008')), u'MOV(esi, offset(_data,unk_40e008))')

    def test_instr_7750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     esi_0, ebx')), u'MOV(esi_0, ebx)')

    def test_instr_7760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     i, 12345678h')), u'MOV(i, 0x12345678)')

    def test_instr_7770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     i, esi')), u'MOV(i, esi)')

    def test_instr_7780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     op0, 32432434h')), u'MOV(op0, 0x32432434)')

    def test_instr_7790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov   al,0')), u'MOV(al, 0)')

    def test_instr_7800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov   dx,3c8h')), u'MOV(dx, 0x3c8)')

    def test_instr_7810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov   dx,3c9h')), u'MOV(dx, 0x3c9)')

    def test_instr_7820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov   esi,offset pal_jeu')), u'MOV(esi, offset(_data,pal_jeu))')

    def test_instr_7830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov  bx,ax')), u'MOV(bx, ax)')

    def test_instr_7840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov  fs,ax')), u'MOV(fs, ax)')

    def test_instr_7850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov [a],5')), u'MOV(*(a), 5)')

    def test_instr_7860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov [load_handle],eax')), u'MOV(load_handle, eax)')

    def test_instr_7870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ah,03dh')), u'MOV(ah, 0x03d)')

    def test_instr_7880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ah,48h')), u'MOV(ah, 0x48)')

    def test_instr_7890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ah,4Ah')), u'MOV(ah, 0x4A)')

    def test_instr_7900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ah,4ch                    ; AH=4Ch - Exit To DOS')), u'MOV(ah, 0x4c)')

    def test_instr_7910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ah,7')), u'MOV(ah, 7)')

    def test_instr_7920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ah,9                        ; AH=09h - Print DOS Message')), u'MOV(ah, 9)')

    def test_instr_7930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov al,-5')), u'MOV(al, -5)')

    def test_instr_7940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov al,00h  ;ouverture du fichier pour lecture.')), u'MOV(al, 0x00)')

    def test_instr_7950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov al,00h ;debut du fichier')), u'MOV(al, 0x00)')

    def test_instr_7960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov al,1')), u'MOV(al, 1)')

    def test_instr_7970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov al,7')), u'MOV(al, 7)')

    def test_instr_7980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov al,[a]')), u'MOV(al, *(a))')

    def test_instr_7990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,-1')), u'MOV(ax, -1)')

    def test_instr_8000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,0002h')), u'MOV(ax, 0x0002)')

    def test_instr_8010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,0007')), u'MOV(ax, 0007)')

    def test_instr_8020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,01010101010101010b')), u'MOV(ax, 0xaaaa)')

    def test_instr_8030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,01111111111111111b')), u'MOV(ax, 0xffff)')

    def test_instr_8040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,08h')), u'MOV(ax, 0x08)')

    def test_instr_8050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,13h')), u'MOV(ax, 0x13)')

    def test_instr_8060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,3h')), u'MOV(ax, 0x3)')

    def test_instr_8070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,4')), u'MOV(ax, 4)')

    def test_instr_8080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,501h')), u'MOV(ax, 0x501)')

    def test_instr_8090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,6')), u'MOV(ax, 6)')

    def test_instr_8100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax,bp')), u'MOV(ax, bp)')

    def test_instr_8110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,-1')), u'MOV(bl, -1)')

    def test_instr_8120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,0')), u'MOV(bl, 0)')

    def test_instr_8130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,011111111B')), u'MOV(bl, 0xff)')

    def test_instr_8140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,1')), u'MOV(bl, 1)')

    def test_instr_8150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,192')), u'MOV(bl, 192)')

    def test_instr_8160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,[a+1]')), u'MOV(bl, *((a)+1))')

    def test_instr_8170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bl,al')), u'MOV(bl, al)')

    def test_instr_8180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,(1024*10/16)+5')), u'MOV(bx, (1024*10/16)+5)')

    def test_instr_8190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,(1024*10/16)-1')), u'MOV(bx, (1024*10/16)-1)')

    def test_instr_8200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,10')), u'MOV(bx, 10)')

    def test_instr_8210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,1024*10/16')), u'MOV(bx, 1024*10/16)')

    def test_instr_8220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,5')), u'MOV(bx, 5)')

    def test_instr_8230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,ax')), u'MOV(bx, ax)')

    def test_instr_8240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,fs')), u'MOV(bx, fs)')

    def test_instr_8250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,word ptr [d]')), u'MOV(bx, *(dw*)((&d)))')

    def test_instr_8260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov bx,word ptr [e]')), u'MOV(bx, *(dw*)((&e)))')

    def test_instr_8270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov byte ptr [a],5')), u'MOV(*(a), 5)')

    def test_instr_8280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov byte ptr [esi],-2')), u'MOV(*(raddr(ds,esi)), -2)')

    def test_instr_8290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov byte ptr [singlebyte2+1],5')), u'MOV(*((&singlebyte2)+1), 5)')

    def test_instr_8300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dl,byte ptr [edi]')), u'MOV(dl, *(raddr(ds,edi)))')

    def test_instr_8310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov byte ptr ds:[0],55')), u'MOV(*(raddr(ds,0)), 55)')

    def test_instr_8320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov byte ptr es:[0],55')), u'MOV(*(raddr(es,0)), 55)')

    def test_instr_8330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov byte ptr es:[0],56')), u'MOV(*(raddr(es,0)), 56)')

    def test_instr_8340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ch,011111111B')), u'MOV(ch, 0xff)')

    def test_instr_8350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cl,2')), u'MOV(cl, 2)')

    def test_instr_8360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cl,8            ; number of ASCII')), u'MOV(cl, 8)')

    def test_instr_8370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cx,-1')), u'MOV(cx, -1)')

    def test_instr_8380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cx,-5')), u'MOV(cx, -5)')

    def test_instr_8390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cx,0')), u'MOV(cx, 0)')

    def test_instr_8400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cx,1')), u'MOV(cx, 1)')

    def test_instr_8410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cx,256*3')), u'MOV(cx, 256*3)')

    def test_instr_8420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov cx,ax')), u'MOV(cx, ax)')

    def test_instr_8430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dl,[edi+1]')), u'MOV(dl, *(raddr(ds,edi+1)))')

    def test_instr_8440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dl,[edi]')), u'MOV(dl, *(raddr(ds,edi)))')

    def test_instr_8450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ds, _data')), u'MOV(ds, seg_offset(_data))')

    def test_instr_8460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ds:[edi],cl')), u'MOV(*(raddr(ds,edi)), cl)')

    def test_instr_8470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dword ptr es:[0],077aaFF00h')), u'MOV(*(dd*)(raddr(es,0)), 0x077aaFF00)')

    def test_instr_8480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dword ptr es:[20*320+160],077aaFF00h')), u'MOV(*(dd*)(raddr(es,20*320+160)), 0x077aaFF00)')

    def test_instr_8490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dx,-1')), u'MOV(dx, -1)')

    def test_instr_8500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dx,0')), u'MOV(dx, 0)')

    def test_instr_8510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dx,5')), u'MOV(dx, 5)')

    def test_instr_8520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dx,[edi+1]')), u'MOV(dx, *(dw*)(raddr(ds,edi+1)))')

    def test_instr_8530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dx,cx')), u'MOV(dx, cx)')

    def test_instr_8540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax, 0ffffffffh')), u'MOV(eax, 0x0ffffffff)')

    def test_instr_8550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax, B')), u'MOV(eax, b)')

    def test_instr_8560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax, CC')), u'MOV(eax, cc)')

    def test_instr_8570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,-1')), u'MOV(eax, -1)')

    def test_instr_8580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,-1-(-2+3)')), u'MOV(eax, -1-(-2+3))')

    def test_instr_8590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,-4')), u'MOV(eax, -4)')

    def test_instr_8600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,-5')), u'MOV(eax, -5)')

    def test_instr_8610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,-8')), u'MOV(eax, -8)')

    def test_instr_8620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,0')), u'MOV(eax, 0)')

    def test_instr_8630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,0100b')), u'MOV(eax, 0x4)')

    def test_instr_8640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,011111111111111111111111111111111b')), u'MOV(eax, 0xffffffff)')

    def test_instr_8650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,012345678h')), u'MOV(eax, 0x012345678)')

    def test_instr_8660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,077aaFF00h')), u'MOV(eax, 0x077aaFF00)')

    def test_instr_8670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,0ffff00f3h')), u'MOV(eax, 0x0ffff00f3)')

    def test_instr_8680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,0ffffff03h')), u'MOV(eax, 0x0ffffff03)')

    def test_instr_8690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,1')), u'MOV(eax, 1)')

    def test_instr_8700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,1024*1024')), u'MOV(eax, 1024*1024)')

    def test_instr_8710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,10B')), u'MOV(eax, 0x2)')

    def test_instr_8720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,2')), u'MOV(eax, 2)')

    def test_instr_8730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,256+3+65536')), u'MOV(eax, 256+3+65536)')

    def test_instr_8740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,3')), u'MOV(eax, 3)')

    def test_instr_8750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,4')), u'MOV(eax, 4)')

    def test_instr_8760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,5')), u'MOV(eax, 5)')

    def test_instr_8770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,511')), u'MOV(eax, 511)')

    def test_instr_8780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,taille_moire  ;::!300000h-1 ;182400h-1 ;1582080 ;0300000h-1 ;2mega 182400h-1')), u'MOV(eax, taille_moire)')

    def test_instr_8790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov eax,teST2')), u'MOV(eax, test2)')

    def test_instr_8800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebp,10')), u'MOV(ebp, 10)')

    def test_instr_8810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebp,2')), u'MOV(ebp, 2)')

    def test_instr_8820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebp,20')), u'MOV(ebp, 20)')

    def test_instr_8830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebp,3')), u'MOV(ebp, 3)')

    def test_instr_8840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebp,3*4')), u'MOV(ebp, 3*4)')

    def test_instr_8850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebp,30')), u'MOV(ebp, 30)')

    def test_instr_8860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,-1')), u'MOV(ebx, -1)')

    def test_instr_8870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0')), u'MOV(ebx, 0)')

    def test_instr_8880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,00fffh')), u'MOV(ebx, 0x00fff)')

    def test_instr_8890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,01B')), u'MOV(ebx, 0x1)')

    def test_instr_8900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0FFFFFFFFh')), u'MOV(ebx, 0x0FFFFFFFF)')

    def test_instr_8910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0a000h')), u'MOV(ebx, 0x0a000)')

    def test_instr_8920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0aabbccddh')), u'MOV(ebx, 0x0aabbccdd)')

    def test_instr_8930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0f222h')), u'MOV(ebx, 0x0f222)')

    def test_instr_8940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0ffff01ffh')), u'MOV(ebx, 0x0ffff01ff)')

    def test_instr_8950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,0ffffffffh')), u'MOV(ebx, 0x0ffffffff)')

    def test_instr_8960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,2')), u'MOV(ebx, 2)')

    def test_instr_8970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,255')), u'MOV(ebx, 255)')

    def test_instr_8980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,3')), u'MOV(ebx, 3)')

    def test_instr_8990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,5')), u'MOV(ebx, 5)')

    def test_instr_9000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,[g]')), u'MOV(ebx, g)')

    def test_instr_9010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,[load_handle]')), u'MOV(ebx, load_handle)')

    def test_instr_9020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,eax')), u'MOV(ebx, eax)')

    def test_instr_9030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,-1')), u'MOV(ecx, -1)')

    def test_instr_9040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,000ff00ffh')), u'MOV(ecx, 0x000ff00ff)')

    def test_instr_9050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,0a0000h')), u'MOV(ecx, 0x0a0000)')

    def test_instr_9060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,0df01h')), u'MOV(ecx, 0x0df01)')

    def test_instr_9070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,0f0ffh')), u'MOV(ecx, 0x0f0ff)')

    def test_instr_9080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,0ffffffffh')), u'MOV(ecx, 0x0ffffffff)')

    def test_instr_9090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,10')), u'MOV(ecx, 10)')

    def test_instr_9100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,2')), u'MOV(ecx, 2)')

    def test_instr_9110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,3')), u'MOV(ecx, 3)')

    def test_instr_9120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,320*200/4')), u'MOV(ecx, 320*200/4)')

    def test_instr_9130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,5')), u'MOV(ecx, 5)')

    def test_instr_9140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,60')), u'MOV(ecx, 60)')

    def test_instr_9150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ecx,t')), u'MOV(ecx, t)')

    def test_instr_9160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,1')), u'MOV(edi, 1)')

    def test_instr_9170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,8')), u'MOV(edi, 8)')

    def test_instr_9180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,OFFSET AsCii ; get the offset address')), u'MOV(edi, offset(_data,ascii))')

    def test_instr_9190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,esi')), u'MOV(edi, esi)')

    def test_instr_9200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,offset str2')), u'MOV(edi, offset(_data,str2))')

    def test_instr_9210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,offset str3')), u'MOV(edi, offset(_data,str3))')

    def test_instr_9220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,offset singlebyte2')), u'MOV(edi, offset(_data,singlebyte2))')

    def test_instr_9230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,offset wordarray')), u'MOV(edi, offset(_data,wordarray))')

    def test_instr_9240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edi,offset bytearray')), u'MOV(edi, offset(_data,bytearray))')

    def test_instr_9250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,0')), u'MOV(edx, 0)')

    def test_instr_9260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,0abcdef77h')), u'MOV(edx, 0x0abcdef77)')

    def test_instr_9270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,2')), u'MOV(edx, 2)')

    def test_instr_9280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,4')), u'MOV(edx, 4)')

    def test_instr_9290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,OFFSET ASCiI ; DOS 1+ WRITE STRING TO STANDARD OUTPUT')), u'MOV(edx, offset(_data,ascii))')

    def test_instr_9300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,edi')), u'MOV(edx, edi)')

    def test_instr_9310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov edx,offset _msg             ; DS:EDX -> $ Terminated String')), u'MOV(edx, offset(_data,_msg))')

    def test_instr_9320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov es,ax')), u'MOV(es, ax)')

    def test_instr_9330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,2')), u'MOV(esi, 2)')

    def test_instr_9340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,6')), u'MOV(esi, 6)')

    def test_instr_9350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,offset str1')), u'MOV(esi, offset(_data,str1))')

    def test_instr_9360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,offset testOVerlap')), u'MOV(esi, offset(_data,testoverlap))')

    def test_instr_9370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,offset singlebyte2')), u'MOV(esi, offset(_data,singlebyte2))')

    def test_instr_9380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,offset wordarray')), u'MOV(esi, offset(_data,wordarray))')

    def test_instr_9390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov esi,offset singlebyte')), u'MOV(esi, offset(_data,singlebyte))')

    def test_instr_9400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsb')), 'MOVSB')

    def test_instr_9410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsd')), 'MOVSD')

    def test_instr_9420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsw')), 'MOVSW')

    def test_instr_9430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsx bx,[h2]')), u'MOVSX(bx, h2)')

    def test_instr_9440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsx bx,bl')), u'MOVSX(bx, bl)')

    def test_instr_9450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsx bx,byte ptr [h2]')), u'MOVSX(bx, h2)')

    def test_instr_9460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsx bx,byte ptr [h]')), u'MOVSX(bx, h)')

    def test_instr_9470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movsx ecx,cx')), u'MOVSX(ecx, cx)')

    def test_instr_9480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movzx eax, DDD')), u'MOVZX(eax, ddd)')  # ERROR

    def test_instr_9490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movzx ecx,bx')), u'MOVZX(ecx, bx)')

    def test_instr_9500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mul     cl')), u'MUL1_1(cl)')

    def test_instr_9510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mul     cx')), u'MUL1_2(cx)')

    def test_instr_9520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mul     s1_0')), u'MUL1_4(s1_0)')

    def test_instr_9530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('neg     dl')), u'NEG(dl)')

    def test_instr_9540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('neg     dx')), u'NEG(dx)')

    def test_instr_9550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('neg     ebx')), u'NEG(ebx)')

    def test_instr_9560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('neg     edx')), u'NEG(edx)')

    def test_instr_9570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('neg ebx')), u'NEG(ebx)')

    def test_instr_9580(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('neg edx')), u'NEG(edx)')

    def test_instr_9590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('not     dl')), u'NOT(dl)')

    def test_instr_9600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('not     dx')), u'NOT(dx)')

    def test_instr_9610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('not     edx')), u'NOT(edx)')

    def test_instr_9620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('not ax')), u'NOT(ax)')

    def test_instr_9630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('not eax')), u'NOT(eax)')

    def test_instr_9640(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or      dl, cl')), u'OR(dl, cl)')

    def test_instr_9650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or      dx, cx')), u'OR(dx, cx)')

    def test_instr_9660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or      ebx, 0FFFFFFFFh')), u'OR(ebx, 0x0FFFFFFFF)')

    def test_instr_9670(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or      edx, ecx')), u'OR(edx, ecx)')

    def test_instr_9680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or      res, 0FFFFFFFFh')), u'OR(res, 0x0FFFFFFFF)')

    def test_instr_9690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or cl,0f0h')), u'OR(cl, 0x0f0)')

    def test_instr_9700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or cx,cx')), u'OR(cx, cx)')

    def test_instr_9710(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('or eax,eax')), u'OR(eax, eax)')

    def test_instr_9720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('out   dx,al')), u'OUT(dx, al)')

    def test_instr_9730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rcl     dl, cl')), u'RCL(dl, cl)')

    def test_instr_9740(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rcl     dx, cl')), u'RCL(dx, cl)')

    def test_instr_9750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rcl     edx, cl')), u'RCL(edx, cl)')

    def test_instr_9760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rcr     dl, cl')), u'RCR(dl, cl)')

    def test_instr_9770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rcr     dx, cl')), u'RCR(dx, cl)')

    def test_instr_9780(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rcr     edx, cl')), u'RCR(edx, cl)')

    def test_instr_9800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('ret')), 'RETN(0)')

    def test_instr_9810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rol     dl, cl')), u'ROL(dl, cl)')

    def test_instr_9820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rol     dx, cl')), u'ROL(dx, cl)')

    def test_instr_9830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rol     edx, cl')), u'ROL(edx, cl)')

    def test_instr_9840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rol ebx,1')), u'ROL(ebx, 1)')

    def test_instr_9850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('rol ebx,31')), u'ROL(ebx, 31)')

    def test_instr_9860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('ror     dl, cl')), u'ROR(dl, cl)')

    def test_instr_9870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('ror     dx, cl')), u'ROR(dx, cl)')

    def test_instr_9880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('ror     edx, cl')), u'ROR(edx, cl)')

    def test_instr_9890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sar     dl, cl')), u'SAR(dl, cl)')

    def test_instr_9900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sal     dl, cl')), u'SAL(dl, cl)')

    def test_instr_9910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sar     dx, cl')), u'SAR(dx, cl)')

    def test_instr_9920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sar     edx, cl')), u'SAR(edx, cl)')

    def test_instr_9930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sar eax,1')), u'SAR(eax, 1)')

    def test_instr_9940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sar eax,2')), u'SAR(eax, 2)')

    def test_instr_9950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sbb     dl, cl')), u'SBB(dl, cl)')

    def test_instr_9960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sbb     dx, cx')), u'SBB(dx, cx)')

    def test_instr_9970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sbb     edx, ecx')), u'SBB(edx, ecx)')

    def test_instr_9980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('scasb')), 'SCASB')

    def test_instr_9990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('scasd')), 'SCASD')

    def test_instr_10000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('scasw')), 'SCASW')

    def test_instr_10010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('setb    al')), u'SETB(al)')

    def test_instr_10020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('setnz bh')), u'SETNZ(bh)')

    def test_instr_10030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('setz    cl')), u'SETZ(cl)')

    def test_instr_10040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shl     dl, cl')), u'SHL(dl, cl)')

    def test_instr_10050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shl     dx, cl')), u'SHL(dx, cl)')

    def test_instr_10060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shl     edx, cl')), u'SHL(edx, cl)')

    def test_instr_10070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shld    dx, bx, cl')), u'SHLD(dx, bx, cl)')

    def test_instr_10080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shld    edx, ebx, cl')), u'SHLD(edx, ebx, cl)')

    def test_instr_10090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shr     dl, cl')), u'SHR(dl, cl)')

    def test_instr_10100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shr     dx, cl')), u'SHR(dx, cl)')

    def test_instr_10110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shr     edx, cl')), u'SHR(edx, cl)')

    def test_instr_10120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shr eax,16')), u'SHR(eax, 16)')

    def test_instr_10130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shr ecx,16')), u'SHR(ecx, 16)')

    def test_instr_10140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shrd    dx, bx, cl')), u'SHRD(dx, bx, cl)')

    def test_instr_10150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shrd    edx, ebx, cl')), u'SHRD(edx, ebx, cl)')

    def test_instr_10160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shrd eax, edx, 8')), u'SHRD(eax, edx, 8)')

    def test_instr_10170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('stc')), 'STC')

    def test_instr_10180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('std')), 'STD')

    def test_instr_10190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sti                             ; Set The Interrupt Flag')), 'STI')

    def test_instr_10200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('stosb')), 'STOSB')

    def test_instr_10210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('stosd')), 'STOSD')

    def test_instr_10220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('stosw')), 'STOSW')

    def test_instr_10230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     dl, cl')), u'SUB(dl, cl)')

    def test_instr_10240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     dx, cx')), u'SUB(dx, cx)')

    def test_instr_10250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     edx, ecx')), u'SUB(edx, ecx)')

    def test_instr_10260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     esp, 10h')), u'SUB(esp, 0x10)')

    def test_instr_10270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     esp, 114h')), u'SUB(esp, 0x114)')

    def test_instr_10280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     esp, 14h')), u'SUB(esp, 0x14)')

    def test_instr_10290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub eax,eax')), u'SUB(eax, eax)')

    def test_instr_10300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub eax,ebx')), u'SUB(eax, ebx)')

    def test_instr_10320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub word ptr [singlequad+2],25')), u'SUB(*(dw*)(((db*)&singlequad)+2), 25)')

    def test_instr_10330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test    ebx, ebx')), u'TEST(ebx, ebx)')

    def test_instr_10340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test al,010B')), u'TEST(al, 0x2)')

    def test_instr_10350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test al,0B')), u'TEST(al, 0x0)')

    def test_instr_10360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test ax,ax')), u'TEST(ax, ax)')

    def test_instr_10370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test bh,01h')), u'TEST(bh, 0x01)')

    def test_instr_10380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test bh,02h')), u'TEST(bh, 0x02)')

    def test_instr_10390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('test eax,eax')), u'TEST(eax, eax)')

    def test_instr_10400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    byte ptr [ebp+var_20], al')), u'XADD(*(raddr(ss,ebp+var_20)), al)')

    def test_instr_10410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    dl, al')), u'XADD(dl, al)')

    def test_instr_10420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    dword ptr [ebp+var_20], eax')), u'XADD(*(dd*)(raddr(ss,ebp+var_20)), eax)')

    def test_instr_10430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    dx, ax')), u'XADD(dx, ax)')

    def test_instr_10440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    eax, eax')), u'XADD(eax, eax)')

    def test_instr_10450(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    edx, eax')), u'XADD(edx, eax)')

    def test_instr_10460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xadd    word ptr [ebp+var_20], ax')), u'XADD(*(dw*)(raddr(ss,ebp+var_20)), ax)')

    def test_instr_10470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg    al, byte ptr [ebp+var_20]')), u'XCHG(al, *(raddr(ss,ebp+var_20)))')

    def test_instr_10480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg    al, dl')), u'XCHG(al, dl)')

    def test_instr_10490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg    ax, dx')), u'XCHG(ax, dx)')

    def test_instr_10500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg    ax, word ptr [ebp+var_20]')), u'XCHG(ax, *(dw*)(raddr(ss,ebp+var_20)))')

    def test_instr_10510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg    eax, dword ptr [ebp+var_20]')), u'XCHG(eax, *(dd*)(raddr(ss,ebp+var_20)))')

    def test_instr_10520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg    eax, edx')), u'XCHG(eax, edx)')

    def test_instr_10530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xchg eax,ebx')), u'XCHG(eax, ebx)')

    def test_instr_10540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xlat')), 'XLAT')

    def test_instr_10550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor     dl, cl')), u'XOR(dl, cl)')

    def test_instr_10560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor     dx, cx')), u'XOR(dx, cx)')

    def test_instr_10610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor     edx, ecx')), u'XOR(edx, ecx)')

    def test_instr_10660(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor al,bl')), u'XOR(al, bl)')

    def test_instr_10680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor ax,bx')), u'XOR(ax, bx)')

    def test_instr_10690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor ch,bh')), u'XOR(ch, bh)')

    def test_instr_10720(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor eax,ebx')), u'XOR(eax, ebx)')

    def test_instr_10770(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('xor edx,edx')), u'XOR(edx, edx)')

    def test_instr_10790(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'iret')), 'IRET')

    def test_instr_10800(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'retf')), 'RETF(0)')

    def test_instr_10805(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'retf 2')), 'RETF(2)')

    def test_instr_10810(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lds     bx, offset unk_40F064')), u'LDS(bx, offset(initcall,unk_40f064))')

    def test_instr_10820(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('les     bx, offset unk_40F064')), u'LES(bx, offset(initcall,unk_40f064))')

    def test_instr_10830(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lfs     bx, offset unk_40F064')), u'LFS(bx, offset(initcall,unk_40f064))')

    def test_instr_10840(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lgs     bx, offset unk_40F064')), u'LGS(bx, offset(initcall,unk_40f064))')

    def test_instr_10850(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'pusha')), 'PUSHA')

    def test_instr_10860(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'popa')), 'POPA')

    def test_instr_10870(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'cli')), 'CLI')

    def test_instr_10880(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('in   dx,al')), u'IN(dx, al)')

    def test_instr_10890(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shrd ax, dx, 3')), u'SHRD(ax, dx, 3)')

    def test_instr_10900(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('shld ax, dx, 3')), u'SHLD(ax, dx, 3)')

    def test_instr_10910(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('enter 0,0')), u'ENTER(0, 0)')

    def test_instr_10920(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp $+2')), u'{;}')

    def test_instr_10930(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'nop')), 'NOP')

    def test_instr_10940(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lods	[byte ptr fs:si]')), u'LODS(*(raddr(fs,si)),si,1)')

    def test_instr_10950(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('scas	[word ptr fs:si]')), u'SCAS(*(dw*)(raddr(fs,si)),si,2)')

    def test_instr_10960(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movs [dword ptr es:di], [dword ptr fs:si]')), u'MOVS(*(dd*)(raddr(es,di)), *(dd*)(raddr(fs,si)), di, si, 4)')

    def test_instr_10970(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("mov al, 'Z' - 'A' +1")), u"MOV(al, 'Z'-'A'+1)")

    def test_instr_10980(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'mov ax,  not 1')), 'MOV(ax, ~1)')

    def test_instr_10990(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     [esp+8], eax')), 'MOV(*(dd*)(raddr(ss,esp+8)), eax)')

    def test_instr_11000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, ds:40h[eax*2]')), u'eax = 0x40+eax*2')

    def test_instr_11010(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, ds:40h[ebx*4]')), u'eax = 0x40+ebx*4')

    def test_instr_11020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, ds:40h[ecx*8]')), u'eax = 0x40+ecx*8')

    def test_instr_11030(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ds:byte_41411F[eax], dl')), u'MOV(*((&byte_41411f)+eax), dl)')

    def test_instr_11040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     eax, large ds:4000h')), u'eax = 0x4000')

    def test_instr_11050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ebx, offset _test_btc')), u'MOV(ebx, offset(initcall,_test_btc))')

    def test_instr_11060(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     dword ptr [esp]')), u'POP(*(dd*)(raddr(ss,esp)))')

    def test_instr_11070(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     eax')), u'POP(eax)')

    def test_instr_11080(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     ebp')), u'POP(ebp)')

    def test_instr_11090(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     ebx')), u'POP(ebx)')

    def test_instr_11100(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     ecx')), u'POP(ecx)')

    def test_instr_11110(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     edi')), u'POP(edi)')

    def test_instr_11120(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     edi_0')), u'POP(edi_0)')

    def test_instr_11130(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     edx')), u'POP(edx)')

    def test_instr_11140(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     esi')), u'POP(esi)')

    def test_instr_11150(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     esi_0')), u'POP(esi_0)')

    def test_instr_11160(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     i')), u'POP(i)')

    def test_instr_11170(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     res')), u'POP(res)')

    def test_instr_11180(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop     s0_0')), u'POP(s0_0)')

    def test_instr_11190(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop ds')), u'POP(ds)')

    def test_instr_11200(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop eax')), u'POP(eax)')

    def test_instr_11210(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pop es')), u'POP(es)')

    def test_instr_11220(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('popad')), 'POPAD')

    def test_instr_11230(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('popf')), 'POPF')

    def test_instr_11240(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push    0')), u'PUSH(0)')

    def test_instr_11250(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push    0BC6058h')), u'PUSH(0x0BC6058)')

    def test_instr_11260(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push    9ABCDEFh')), u'PUSH(0x9ABCDEF)')

    def test_instr_11270(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push    esi')), u'PUSH(esi)')

    def test_instr_11280(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push ds')), u'PUSH(ds)')

    def test_instr_11290(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push ebx')), u'PUSH(ebx)')

    def test_instr_11300(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push es')), u'PUSH(es)')

    def test_instr_11310(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pushad')), 'PUSHAD')

    def test_instr_11320(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('pushf')), 'PUSHF')

    @unittest.skip("it works but test broken. non masm")
    def test_instr_11330(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'rep')), '\tREP\n')

    @unittest.skip("it works but test broken. non masm")
    def test_instr_11340(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'repe')), '\tREPE\n')

    @unittest.skip("it works but test broken. non masm")
    def test_instr_11350(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'repne')), '\tREPNE\n')

    def test_instr_11360(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code(u'repne lodsb')), 'LODSB')

    def test_instr_11370(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call    dword ptr [ebx-4]')), 'CALLF(__dispatch_call,*(dd*)(raddr(ds,ebx-4)))')

    def test_instr_11380(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call    exec_adc')), u'CALL(exec_adc,0)')

    def test_instr_11390(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call    printf')), 'CALL(__dispatch_call,printf)')

    def test_instr_11400(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call    test_bcd')), u'CALLF(test_bcd,0)')

    def test_instr_11410(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call printeax')), u'CALL(printeax,0)')

    def test_instr_11420(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp wordarray,2')), u'CMP(*(wordarray), 2)')

    def test_instr_11430(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp wordarray,bx')), u'CMP(*(wordarray), bx)')

    def test_instr_11440(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte,-12')), u'CMP(singlebyte, -12)')

    def test_instr_11450(self): # singlebyte is byte!
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte,ecx')), u'CMP(singlebyte, ecx)')

    def test_instr_11460(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc singlebyte')), u'INC(singlebyte)')

    def test_instr_11470(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp [cs:table+ax]')), 'JMP(__dispatch_call)')

    def test_instr_11480(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov a,5')), u'MOV(*(a), 5)')

    def test_instr_11490(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov a,ah')), u'MOV(*(a), ah)')

    def test_instr_11500(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp b,256+3+65536')), u'CMP(b, 256+3+65536)')

    def test_instr_11510(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte2,1')), u'CMP(singlebyte2, 1)')

    def test_instr_11520(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp singlebyte2,al')), u'CMP(singlebyte2, al)')

    def test_instr_11530(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov b,ax')), u'MOV(b, ax)')

    def test_instr_11540(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov dl,singlebyte2')), u'MOV(dl, singlebyte2)')

    def test_instr_11550(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ebx,g')), u'MOV(ebx, g)')
        #r=list(filter(lambda x: not x.used, p.get_globals().values()))
        #print([g.name for g in r])

    def test_instr_11590(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp loc_406B3F')), u'JMP(loc_406b3f)')

    def test_instr_11600(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('jmp cs:[bx]')), u'JMP(__dispatch_call)')

    def test_instr_11610(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call exec_adc')),u'CALL(exec_adc,0)')

    def test_instr_11620(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call far ptr test_bcd')),u'CALLF(test_bcd,0)')

    def test_instr_11560(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp gameconfig.game_opponenttype, 0')), u'CMP(gameconfig.game_opponenttype, 0)')

    def test_instr_11570(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ax, offset gameconfig.game_opponenttype+t')), u'MOV(ax, offset(default_seg,gameconfig.game_opponenttype)+t)')

    def test_instr_11630(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('cmp gameconfig.game_opponenttype, 0')), u'CMP(gameconfig.game_opponenttype, 0)')

    def test_instr_struct_11640(self): # TODO asmtest
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov[bp + var_transshape.ts_rotvec.vx], 3')), u'MOV(((transformedshape*)raddr(ss,bp+var_transshape))->ts_rotvec.vx, 3)')

    def test_instr_11650(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax, (offset gameconfig.game_opponenttype+0AA8h)')),
                     u'MOV(ax, offset(default_seg,gameconfig.game_opponenttype)+0x0AA8)')

    def test_instr_11660(self):
        self.assertEqual(self.proc.generate_full_cmd_line(self.cpp, self.parser.action_data('var_104_rc equ TRANSFORMEDSHAPE ptr -260')), u'#define var_104_rc -260\n')

    #def test_instr_11670(self):
    #    self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov (transformedshape + bp - 3).ts_rotvec.vx, 3')),
    #        u'MOV(((transformedshape*)raddr(ss,(bp-3)))->ts_rotvec.vx, 3)')

    def test_instr_11680(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     si, [bx+di+TRANSFORMEDSHAPE.ts_rotvec]')),
            u'si = bx+di+offsetof(transformedshape,ts_rotvec)')

    def test_instr_11690(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('lea     ax, [si+(size TRANSFORMEDSHAPE)]')),
            u'ax = si+(sizeof(transformedshape))')

    def test_instr_11700(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dx, word ptr (oppresources+2)[bx]')),
            u'MOV(dx, *(dw*)(raddr(ds,(oppresources+2)+bx)))')

    def test_instr_11710(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code('push    [bp+var_TransshapE.ts_rotvec.vx]')),
            u'PUSH(((transformedshape*)raddr(ss,bp+var_transshape))->ts_rotvec.vx)')

    def test_instr_11720(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     word ptr [bx+transformedshape.ts_rotvec], ax')),
            u'ADD(((transformedshape*)raddr(ds,bx))->ts_rotvec, ax)')

    def test_instr_11730(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov ax, (offset gameconfig.game_opponenTType+0AA8h)')),
                     u'MOV(ax, offset(default_seg,gameconfig.game_opponenttype)+0x0AA8)')

    def test_instr_11740(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp,
                                     self.parser.action_code('adc     word ptr [bx+(transformedshape.ts_rotvec+2)], dx')),
            u'ADC(((transformedshape*)raddr(ds,bx+2))->ts_rotvec, dx)')

    def test_instr_11750(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     gameconfig.game_opponenTType[di], 10h')),
                     u'ADD(*(dw*)(((db*)&gameconfig.game_opponenttype)+di), 0x10)')

    def test_instr_11760(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('inc     gameconfig.game_opponenTType')),
                     u'INC(gameconfig.game_opponenttype)')

    def test_instr_11770(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     dx, word ptr [bx+(gameinfo.game_opponenTType+2)]')),
            u'MOV(dx, ((gameinfo*)raddr(ds,bx+2))->game_opponenttype)')

    def test_instr_11780(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code('add     ax, gameInfo.game_opponenTType')),
            u'ADD(ax, offsetof(gameinfo,game_opponenttype))')

    def test_instr_11790(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code('adc     dx, word ptr [bp+var_transshape.ts_rectptr+0Eh]')),
            u'ADC(dx, ((transformedshape*)raddr(ss,bp+0x0E +var_transshape))->ts_rectptr)')

    def test_instr_11800(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code('sub     ax, es:[bx+di+(transformedshape.ts_rotvec+24h)]')),
            u'SUB(ax, ((transformedshape*)raddr(es,bx+di+0x24))->ts_rotvec)')

    def test_instr_11810(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r"cmp al, '\'")), u"CMP(al, '\\\\')")

    def test_instr_11820(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov     ds:2, si')), u"MOV(*(dw*)(raddr(ds,2)), si)")

    def test_instr_11830(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov     ax, word ptr cs:gameconfig.game_opponentmaterial+2')),
            u"MOV(ax, *(dw*)(((db*)&gameconfig.game_opponentmaterial)+2))")

    def test_instr_11840(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov     al, byte ptr [bx+GAMEINFO.game_opponenttype]')),
            u"MOV(al, TODB(((gameinfo*)raddr(ds,bx))->game_opponenttype))")

    @unittest.skip("Minor syntax")
    def test_instr_11850(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov	bl, byte ptr es:[table]')),
            u"MOV(bl, *((db*)&table))")

    @unittest.skip("Minor syntax")
    def test_instr_11860(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov	ch, es:[singlebyte]')),
            u"MOV(ch, singlebyte)")

    @unittest.skip("Minor syntax")
    def test_instr_11870(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov	eax, es:[g]')),
            u"MOV(eax, g)")

    def test_instr_11880(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov     eax, fs:8')),
            u"MOV(eax, *(dd*)(raddr(fs,8)))")

    def test_instr_11890(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'mov     ax, fs:8')),
            u"MOV(ax, *(dw*)(raddr(fs,8)))")

    def test_instr_11900(self):
        self.assertEqual(
            self.proc.generate_c_cmd(self.cpp, self.parser.action_code(r'movs dword ptr es:[di], dword ptr fs:[si]')),
            u"MOVS(*(dd*)(raddr(es,di)), *(dd*)(raddr(fs,si)), di, si, 4)")

    def test_instr_12000(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call  near ptr  test_bcd')), u'CALL(test_bcd,0)')

    def test_instr_12010(self):
        #self.parser.action_data(line='loc_40458f:')
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('call    far ptr test_bcd')), u'CALLF(test_bcd,0)')

    def test_instr_12020(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("xlat    byte ptr cs:[bx]")), u'XLATP(raddr(cs,bx))')


    def test_instr_12040(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('movs byte ptr es:[di], byte ptr cs:[si]')),
                     u'MOVS(*(raddr(es,di)), *(raddr(cs,si)), di, si, 1)')

    def test_instr_12050(self):
        self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code('mov     ds:_byte_2D196_in_transition?, al')),
                     u'MOV(_byte_2D196_in_transitionque, al)')

    #def test_instr_12030(self):
    #    self.assertEqual(self.proc.generate_c_cmd(self.cpp, self.parser.action_code("cmp head, 'v'")), u"CMP(*(head), 'v')")

if __name__ == "__main__":
    unittest.main()
