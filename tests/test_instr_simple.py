from __future__ import absolute_import, print_function

import unittest

from masm2c import cpp
from masm2c.parser import Parser
from masm2c.proc import Proc


class ParserTestSimple(unittest.TestCase):
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
        self.__class__.results = {}

    def doTest(self, input, second):
        result = self.proc.generate_c_cmd(self.cpp, self.parser.action_code(input))
        #self.__class__.results[input] = result
        return (result, second)

    def test_instr_3720(self):
        self.assertEqual(*self.doTest('imul    ax, cx', 'IMUL2_2(ax,cx)'))

    def test_instr_3730(self):
        self.assertEqual(*self.doTest('imul    ax, cx, 2Dh', 'IMUL3_2(ax,cx,0x2D)'))

    def test_instr_3740(self):
        self.assertEqual(*self.doTest('imul    ax, di, 8000h', 'IMUL3_2(ax,di,0x8000)'))

    def test_instr_3750(self):
        self.assertEqual(*self.doTest('imul    ax, dx, -2Dh', 'IMUL3_2(ax,dx,-0x2D)'))

    def test_instr_3760(self):
        self.assertEqual(*self.doTest('imul    ax, si, 7FFFh', 'IMUL3_2(ax,si,0x7FFF)'))

    def test_instr_3770(self):
        self.assertEqual(*self.doTest('imul    cl', 'IMUL1_1(cl)'))

    def test_instr_3780(self):
        self.assertEqual(*self.doTest('imul    cx', 'IMUL1_2(cx)'))

    def test_instr_3790(self):
        self.assertEqual(*self.doTest('imul    eax, ecx, 2Dh', 'IMUL3_4(eax,ecx,0x2D)'))

    def test_instr_3800(self):
        self.assertEqual(*self.doTest('imul    eax, edi, 8000h', 'IMUL3_4(eax,edi,0x8000)'))

    def test_instr_3810(self):
        self.assertEqual(*self.doTest('imul    eax, edx, -2Dh', 'IMUL3_4(eax,edx,-0x2D)'))

    def test_instr_3900(self):
        self.assertEqual(*self.doTest('inc byte ptr [edi+7]', 'INC(*(raddr(ds,edi+7)))'))

    def test_instr_3910(self):
        self.assertEqual(*self.doTest('inc byte ptr es:[0]', 'INC(*(raddr(es,0)))'))

    def test_instr_3950(self):
        self.assertEqual(*self.doTest('inc edi              ; increase target address', 'INC(edi)'))

    def test_instr_9610(self):
        self.assertEqual(*self.doTest('movsx ecx,cx', 'MOVSX(ecx, cx)'))

    def test_instr_9630(self):
        self.assertEqual(*self.doTest('movzx ecx,bx', 'MOVZX(ecx, bx)'))

    def test_instr_9640(self):
        self.assertEqual(*self.doTest('bsf     eax, ebx', 'BSF(eax, ebx)'))

    def test_instr_9650(self):
        self.assertEqual(*self.doTest('mul     cl', 'MUL1_1(cl)'))

    def test_instr_9660(self):
        self.assertEqual(*self.doTest('mul     cx', 'MUL1_2(cx)'))

    def test_instr_9680(self):
        self.assertEqual(*self.doTest('neg     dl', 'NEG(dl)'))

    def test_instr_9690(self):
        self.assertEqual(*self.doTest('neg     dx', 'NEG(dx)'))

    def test_instr_9710(self):
        self.assertEqual(*self.doTest('neg     edx', 'NEG(edx)'))

    def test_instr_9740(self):
        self.assertEqual(*self.doTest('not     dl', 'NOT(dl)'))

    def test_instr_9750(self):
        self.assertEqual(*self.doTest('bsf     eax, edi', 'BSF(eax, edi)'))

    def test_instr_9760(self):
        self.assertEqual(*self.doTest('not     dx', 'NOT(dx)'))

    def test_instr_9770(self):
        self.assertEqual(*self.doTest('not     edx', 'NOT(edx)'))

    def test_instr_9780(self):
        self.assertEqual(*self.doTest('not ax', 'NOT(ax)'))

    def test_instr_9790(self):
        self.assertEqual(*self.doTest('not eax', 'NOT(eax)'))

    def test_instr_9800(self):
        self.assertEqual(*self.doTest('or      dl, cl', 'OR(dl, cl)'))

    def test_instr_9810(self):
        self.assertEqual(*self.doTest('or      dx, cx', 'OR(dx, cx)'))

    def test_instr_9820(self):
        self.assertEqual(*self.doTest('or      ebx, 0FFFFFFFFh', 'OR(ebx, 0x0FFFFFFFF)'))

    def test_instr_9830(self):
        self.assertEqual(*self.doTest('or      edx, ecx', 'OR(edx, ecx)'))

    def test_instr_990(self):
        self.assertEqual(*self.doTest('lea     eax, ds:40h[ebx*4]', 'eax = 0x40+ebx*4'))

    def test_instr_380(self):
        self.assertEqual(*self.doTest('test    ebx, ebx', 'TEST(ebx, ebx)'))

    def test_instr_390(self):
        self.assertEqual(*self.doTest('test al,010B', 'TEST(al, 0x2)'))

    def test_instr_400(self):
        self.assertEqual(*self.doTest('test al,0B', 'TEST(al, 0x0)'))

    def test_instr_410(self):
        self.assertEqual(*self.doTest('test ax,ax', 'TEST(ax, ax)'))

    def test_instr_420(self):
        self.assertEqual(*self.doTest('test bh,01h', 'TEST(bh, 0x01)'))

    def test_instr_430(self):
        self.assertEqual(*self.doTest('test bh,02h', 'TEST(bh, 0x02)'))

    def test_instr_440(self):
        self.assertEqual(*self.doTest('test eax,eax', 'TEST(eax, eax)'))

    def test_instr_450(self):
        self.assertEqual(*self.doTest('bt      cx, dx', 'BT(cx, dx)'))

    def test_instr_6740(self):
        self.assertEqual(*self.doTest('mov     dword ptr [esp+8], 0 ; op1', 'MOV(*(dd*)(raddr(ss,esp+8)), 0)'))

    def test_instr_20(self):
        self.assertEqual(*self.doTest('bsr     eax, edx', 'BSR(eax, edx)'))

    def test_instr_30(self):
        self.assertEqual(*self.doTest('scasw', 'SCASW'))

    def test_instr_40(self):
        self.assertEqual(*self.doTest('setb    al', 'SETB(al)'))

    def test_instr_50(self):
        self.assertEqual(*self.doTest('setnz bh', 'SETNZ(bh)'))

    def test_instr_60(self):
        self.assertEqual(*self.doTest('setz    cl', 'SETZ(cl)'))

    def test_instr_70(self):
        self.assertEqual(*self.doTest('shl     dl, cl', 'SHL(dl, cl)'))

    def test_instr_80(self):
        self.assertEqual(*self.doTest('shl     dx, cl', 'SHL(dx, cl)'))

    def test_instr_90(self):
        self.assertEqual(*self.doTest('shl     edx, cl', 'SHL(edx, cl)'))

    def test_instr_100(self):
        self.assertEqual(*self.doTest('shld    dx, bx, cl', 'SHLD(dx, bx, cl)'))

    def test_instr_110(self):
        self.assertEqual(*self.doTest('shld    edx, ebx, cl', 'SHLD(edx, ebx, cl)'))

    def test_instr_120(self):
        self.assertEqual(*self.doTest('shr     dl, cl', 'SHR(dl, cl)'))

    def test_instr_130(self):
        self.assertEqual(*self.doTest('bsr     eax, esi', 'BSR(eax, esi)'))

    def test_instr_140(self):
        self.assertEqual(*self.doTest('shr     dx, cl', 'SHR(dx, cl)'))

    def test_instr_150(self):
        self.assertEqual(*self.doTest('shr     edx, cl', 'SHR(edx, cl)'))

    def test_instr_160(self):
        self.assertEqual(*self.doTest('shr eax,16', 'SHR(eax, 16)'))

    def test_instr_170(self):
        self.assertEqual(*self.doTest('shr ecx,16', 'SHR(ecx, 16)'))

    def test_instr_180(self):
        self.assertEqual(*self.doTest('shrd    dx, bx, cl', 'SHRD(dx, bx, cl)'))

    def test_instr_190(self):
        self.assertEqual(*self.doTest('shrd    edx, ebx, cl', 'SHRD(edx, ebx, cl)'))

    def test_instr_200(self):
        self.assertEqual(*self.doTest('shrd eax, edx, 8', 'SHRD(eax, edx, 8)'))

    def test_instr_210(self):
        self.assertEqual(*self.doTest('stc', 'STC'))

    def test_instr_220(self):
        self.assertEqual(*self.doTest('std', 'STD'))

    def test_instr_230(self):
        self.assertEqual(*self.doTest('sti                             ; Set The Interrupt Flag', 'STI'))

    def test_instr_240(self):
        self.assertEqual(*self.doTest('bsr     edx, eax', 'BSR(edx, eax)'))

    def test_instr_250(self):
        self.assertEqual(*self.doTest('stosb', 'STOSB'))

    def test_instr_260(self):
        self.assertEqual(*self.doTest('stosd', 'STOSD'))

    def test_instr_270(self):
        self.assertEqual(*self.doTest('stosw', 'STOSW'))

    def test_instr_280(self):
        self.assertEqual(*self.doTest('sub     dl, cl', 'SUB(dl, cl)'))

    def test_instr_290(self):
        self.assertEqual(*self.doTest('sub     dx, cx', 'SUB(dx, cx)'))

    def test_instr_300(self):
        self.assertEqual(*self.doTest('sub     edx, ecx', 'SUB(edx, ecx)'))

    def test_instr_310(self):
        self.assertEqual(*self.doTest('sub     esp, 10h', 'SUB(esp, 0x10)'))

    def test_instr_320(self):
        self.assertEqual(*self.doTest('sub     esp, 114h', 'SUB(esp, 0x114)'))

    def test_instr_330(self):
        self.assertEqual(*self.doTest('sub     esp, 14h', 'SUB(esp, 0x14)'))

    def test_instr_340(self):
        self.assertEqual(*self.doTest('sub eax,eax', 'SUB(eax, eax)'))

    def test_instr_350(self):
        self.assertEqual(*self.doTest('bswap   eax', 'BSWAP(eax)'))

    def test_instr_360(self):
        self.assertEqual(*self.doTest('sub eax,ebx', 'SUB(eax, ebx)'))

    def test_instr_1830(self):
        self.assertEqual(*self.doTest('mov     eax, fs:8', 'MOV(eax, *(dd*)(raddr(fs,8)))'))

    def test_instr_590(self):
        self.assertEqual(*self.doTest('xchg    eax, edx', 'XCHG(eax, edx)'))

    def test_instr_600(self):
        self.assertEqual(*self.doTest('xchg eax,ebx', 'XCHG(eax, ebx)'))

    def test_instr_610(self):
        self.assertEqual(*self.doTest('xlat', 'XLAT'))

    def test_instr_620(self):
        self.assertEqual(*self.doTest('xor     dl, cl', 'XOR(dl, cl)'))

    def test_instr_630(self):
        self.assertEqual(*self.doTest('xor     dx, cx', 'XOR(dx, cx)'))

    def test_instr_640(self):
        self.assertEqual(*self.doTest('bt eax,0', 'BT(eax, 0)'))

    def test_instr_650(self):
        self.assertEqual(*self.doTest('xor     edx, ecx', 'XOR(edx, ecx)'))

    def test_instr_660(self):
        self.assertEqual(*self.doTest('xor al,bl', 'XOR(al, bl)'))

    def test_instr_670(self):
        self.assertEqual(*self.doTest('xor ax,bx', 'XOR(ax, bx)'))

    def test_instr_680(self):
        self.assertEqual(*self.doTest('xor ch,bh', 'XOR(ch, bh)'))

    def test_instr_690(self):
        self.assertEqual(*self.doTest('bt eax,2', 'BT(eax, 2)'))

    def test_instr_700(self):
        self.assertEqual(*self.doTest('xor eax,ebx', 'XOR(eax, ebx)'))

    def test_instr_710(self):
        self.assertEqual(*self.doTest('xor edx,edx', 'XOR(edx, edx)'))

    def test_instr_720(self):
        self.assertEqual(*self.doTest('iret', 'IRET'))

    def test_instr_730(self):
        self.assertEqual(*self.doTest('btc     cx, dx', 'BTC(cx, dx)'))

    def test_instr_740(self):
        self.assertEqual(*self.doTest('retf', 'RETF(0)'))

    def test_instr_750(self):
        self.assertEqual(*self.doTest('retf 2', 'RETF(2)'))
