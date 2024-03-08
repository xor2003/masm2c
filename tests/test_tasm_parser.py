
import os
import unittest

from masm2c import cpp, op
from masm2c.parser import Parser
from masm2c.proc import Proc

# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).


class ParserInstructionsTest(unittest.TestCase):
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
        self.__class__.proc = Proc("mainproc")
        self.__class__.cpp.proc = self.__class__.proc

        self.__class__.parser.action_assign_test(label="B", value="word ptr ds:1")
        self.__class__.parser.action_assign_test(label="DDD", value="singlebyte2")
        self.__class__.parser.action_assign_test(label="arg_2", value="word ptr 6")
        self.__class__.parser.action_assign_test(label="arg_4", value="dword ptr 6")
        self.__class__.parser.action_assign_test(label="argc", value="8")
        self.__class__.parser.action_assign_test(label="argv", value="0Ch")
        self.__class__.parser.action_assign_test(label="eax_0", value="eax")
        self.__class__.parser.action_assign_test(label="ecx_0", value="-2Ch")
        self.__class__.parser.action_assign_test(label="ecx_0_0", value="ecx")
        self.__class__.parser.action_assign_test(label="ecx_vals", value="-28h")
        self.__class__.parser.action_assign_test(label="edi_0", value="edi")
        self.__class__.parser.action_assign_test(label="edx_0", value="-2Ch")
        self.__class__.parser.action_assign_test(label="edx_0_0", value="edx")
        self.__class__.parser.action_assign_test(label="eflags", value="eax")
        self.__class__.parser.action_assign_test(label="esi_0", value="ebx")
        self.__class__.parser.action_assign_test(label="esi_0", value="esi")
        self.__class__.parser.action_assign_test(label="flags", value="eax")
        self.__class__.parser.action_assign_test(label="i", value="eax")
        self.__class__.parser.action_assign_test(label="iflags", value="10H")
        self.__class__.parser.action_assign_test(label="iflags", value="14h")
        self.__class__.parser.action_assign_test(label="op0", value="0Ch")
        self.__class__.parser.action_assign_test(label="op0h", value="8")
        self.__class__.parser.action_assign_test(label="op1", value="eax")
        self.__class__.parser.action_assign_test(label="r", value="eax")
        self.__class__.parser.action_assign_test(label="res", value="eax")
        self.__class__.parser.action_assign_test(label="resh", value="ebx")
        self.__class__.parser.action_assign_test(label="resz", value="ecx")
        self.__class__.parser.action_assign_test(label="rh", value="edx")
        self.__class__.parser.action_assign_test(label="s0", value="0Ch")
        self.__class__.parser.action_assign_test(label="s0_0", value="ebx")
        self.__class__.parser.action_assign_test(label="s1", value="0Ch")
        self.__class__.parser.action_assign_test(label="s1_0", value="ecx")
        self.__class__.parser.action_assign_test(label="s2", value="8")
        self.__class__.parser.action_assign_test(label="val", value="-1Ch")
        self.__class__.parser.action_assign_test(label="var_1C", value="-1Ch")
        self.__class__.parser.action_assign_test(label="var_20", value="-20h")
        self.__class__.parser.action_assign_test(label="var_2C", value="-2Ch")
        self.__class__.parser.action_assign_test(label="var_4", value="-4")
        self.__class__.parser.action_equ_test(line_number=0, label="CC", value="4")
        self.__class__.parser.action_equ_test(line_number=0, label="T", value="4")
        self.__class__.parser.action_equ_test(line_number=0, label="TEST2", value="-13")
        self.__class__.parser.action_equ_test(line_number=0, label="dubsize", value="13")
        self.__class__.parser.action_equ_test(line_number=0, label="tWO", value="2")
        self.__class__.parser.action_equ_test(line_number=0, label="taille_moire", value="((((2030080+64000*26)/4096)+1)*4096)-1")
        self.__class__.parser.action_equ_test(line_number=0, label="test1", value="(00+38*3)*320+1/2+33*(3-1)")
        self.__class__.parser.action_equ_test(line_number=0, label="test3", value="1500")
        self.__class__.parser.action_equ_test(line_number=0, label="testEqu", value="1")


        self.__class__.parser.set_global("_data", op.var(1, 0, issegment=True))
        self.__class__.parser.set_global("singlebyte2", op.var(size=1, offset=1, name="singlebyte2", segment="_data", elements=1))
        self.__class__.parser.set_global("word_0", op.var(size=2, offset=1, name="word_0", segment="_data", elements=1))
        self.__class__.parser.set_global("_msg", op.var(elements=2, name="_msg", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("_test_btc", op.var(name="_test_btc", offset=1, segment="initcall", size=4))
        self.__class__.parser.set_global("a", op.var(elements=3, name="a", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("a10sa08lxb08lx", op.var(elements=2, name="a10sA08lxB08lx", offset=1, segment="_rdata", size=1))
        self.__class__.parser.set_global("a10sah08lxal08l", op.var(elements=2, name="a10sAh08lxAl08l", offset=1, segment="_rdata", size=1))
        self.__class__.parser.set_global("a10sd", op.var(elements=2, name="a10sD", offset=1, segment="_rdata", size=1))
        self.__class__.parser.set_global("a10seax08lxa08l", op.var(elements=2, name="a10sEax08lxA08l", offset=1, segment="_rdata", size=1))
        self.__class__.parser.set_global("ascii", op.var(elements=2, name="ASCII", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("axorw", op.var(name="aXorw", offset=1, segment="_rdata", size=1))
        self.__class__.parser.set_global("beginningdata", op.var(name="beginningdata", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("buffer", op.var(elements=64000, name="buffer", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("byte_41411f", op.var(name="byte_41411F", offset=1, segment="_bss", size=1))
        self.__class__.parser.set_global("d", op.var(name="d", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("doublequote", op.var(elements=0, name="doublequote", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("e", op.var(name="e", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("enddata", op.var(name="enddata", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("f", op.var(name="f", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("filename", op.var(name="fileName", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("g", op.var(name="g", offset=1, segment="_data", size=4))
        self.__class__.parser.set_global("h", op.var(name="h", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("h2", op.var(name="h2", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("load_handle", op.var(name="load_handle", offset=1, segment="_data", size=4))
        self.__class__.parser.set_global("pal_jeu", op.var(elements=16, name="pal_jeu", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("str1", op.var(elements=10, name="str1", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("str2", op.var(elements=10, name="str2", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("str3", op.var(elements=10, name="str3", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("str_buffer", op.var(elements=4096, name="str_buffer", offset=1, segment="_bss", size=1))
        self.__class__.parser.set_global("wordtable", op.var(name="wordtable", elements=1, offset=1, segment="_text", size=2))
        self.__class__.parser.set_global("testoverlap", op.var(elements=14, name="testOVerlap", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("unk_40e008", op.var(name="unk_40E008", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("unk_40f064", op.var(name="unk_40F064", offset=1, segment="initcall", size=1))
        self.__class__.parser.set_global("var", op.var(elements=4, name="var", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("bytearray2", op.var(elements=10, name="bytearray2", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("wordarray", op.var(elements=3, name="wordarray", offset=1, segment="_data", size=2))
        self.__class__.parser.set_global("singlebyte", op.var(elements=1, name="singlebyte", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("bytearray", op.var(elements=100, name="bytearray", offset=1, segment="_data", size=1))
        self.__class__.parser.set_global("singlequad", op.var(elements=1, name="singlequad", offset=1, segment="_data", size=4))
        self.__class__.parser.action_data(line="""GAMEINFOSTRUC struc
game_oppttypedw dw ?
game_opponentmaterial dd ?
struc_member_dup db 4 dup (?)
GAMEINFOSTRUC ends
extrn extrn_struc_inst:GAMEINFOSTRUC
h_array db '^',10,10

 VECTORSTRUC struc
    vxdw dw ?
 VECTORSTRUC ends
 TRANSSHAPESTRUC struc
    ts_shapeptr dw ?
    ts_rectptr dw ?
    ts_rOTv_membr_strinst VECTORSTRUC <>
    struc_mmbr_dup_othr_struc VECTORSTRUC 3 dup (<>)
 TRANSSHAPESTRUC ends
 asgn_aptr_in_struc = TRANSSHAPESTRUC ptr -50
""")
        #var_transshape TRANSSHAPESTRUC <>
        self.__class__.parser.get_global("asgn_aptr_in_struc").implemented = True
        #?self.__class__.cpp._assignment('asgn_aptr_in_struc',self.__class__.parser.get_global('asgn_aptr_in_struc'))
        self.__class__.parser.action_label(far=False, name="@@saaccvaaaax", isproc=False)
        self.__class__.parser.action_label(far=False, name="@VBL1", isproc=False)
        self.__class__.parser.action_label(far=False, name="@VBL12", isproc=False)
        self.__class__.parser.action_label(far=False, name="@VBL2", isproc=False)
        self.__class__.parser.action_label(far=False, name="@VBL22", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@1", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@2", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@3", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@4", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@5", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@6", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@7", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@8", isproc=False)
        self.__class__.parser.action_label(far=False, name="@df@@@@9", isproc=False)
        self.__class__.parser.action_label(far=False, name="OK", isproc=False)
        self.__class__.parser.action_label(far=False, name="P1", isproc=False)
        self.__class__.parser.action_label(far=False, name="P2", isproc=False)
        self.__class__.parser.action_label(far=False, name="dffd", isproc=False)
        self.__class__.parser.action_label(far=False, name="exitLabel", isproc=False)
        self.__class__.parser.action_label(far=False, name="failure", isproc=False)
        self.__class__.parser.action_label(far=False, name="finTest", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40458F", isproc=False)
        self.__class__.cpp.label_to_proc["loc_40458f"] = "mainproc"
        self.__class__.parser.action_label(far=False, name="loc_4046D6", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_406B3F", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_406CF8", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_406EBA", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40707C", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40723E", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40752C", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_4075C2", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_407658", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_4076EE", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_407784", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_407E46", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_407F72", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_408008", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40809E", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_408139", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_4081F6", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_4083E9", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_408464", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_4084DF", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40855A", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_409652", isproc=False)
        self.__class__.parser.action_label(far=False, name="loc_40D571", isproc=False)
        self.__class__.parser.action_label(far=False, name="next", isproc=False)
        self.__class__.parser.action_label(far=False, name="noerror", isproc=False)
        self.__class__.parser.action_label(far=False, name="toto1", isproc=False)
        self.__class__.parser.action_label(far=False, name="exec_adc", isproc=True)
        self.__class__.parser.action_label(far=False, name="exec_rclb", isproc=True)
        self.__class__.parser.action_label(far=False, name="printeax", isproc=True)
        self.__class__.parser.action_label(far=True, name="test_bcd", isproc=True)
        self.__class__.parser.set_global("test_bcd_ofs", op.var(elements=1, name="test_bcd_ofs", offset=1, segment="_data", size=2))
        self.__class__.results = {}

    def doTest(self, input, second):
        result = self.proc.generate_c_cmd(self.cpp, self.parser.action_code(input))
        return (result, second)

    def disable__del__(self):
        id = 10
        if os.path.exists("result.txt"):
                os.remove("result.txt")
        with open("result.txt","a") as f:
            for k, v in self.__class__.results.items():
                f.write(f"""    def test_instr_{id}(self):
        self.assertEqual(*self.doTest("""+repr(k)+", "+repr(v)+"""))

""")
                id += 10

    def test_instr_10(self):
        self.assertEqual(*self.doTest("mov    ax, offset     failure", "ax = m2c::kfailure;"))


    def test_instr_370(self):
        self.assertEqual(*self.doTest("sub word ptr [singlequad+2],25", "SUB(*(dw*)(((db*)&singlequad)+2), 25)"))


    def test_instr_460(self):
        self.assertEqual(*self.doTest("xadd    byte ptr [ebp+var_20], al", "XADD(*(raddr(ss,ebp+var_20)), al)"))

    def test_instr_470(self):
        self.assertEqual(*self.doTest("xadd    dl, al", "XADD(dl, al)"))

    def test_instr_480(self):
        self.assertEqual(*self.doTest("xadd    dword ptr [ebp+var_20], eax", "XADD(*(dd*)(raddr(ss,ebp+var_20)), eax)"))

    def test_instr_490(self):
        self.assertEqual(*self.doTest("xadd    dx, ax", "XADD(dx, ax)"))

    def test_instr_500(self):
        self.assertEqual(*self.doTest("xadd    eax, eax", "XADD(eax, eax)"))

    def test_instr_510(self):
        self.assertEqual(*self.doTest("xadd    edx, eax", "XADD(edx, eax)"))

    def test_instr_520(self):
        self.assertEqual(*self.doTest("xadd    word ptr [ebp+var_20], ax", "XADD(*(dw*)(raddr(ss,ebp+var_20)), ax)"))

    def test_instr_530(self):
        self.assertEqual(*self.doTest("xchg    al, byte ptr [ebp+var_20]", "XCHG(al, *(raddr(ss,ebp+var_20)))"))

    def test_instr_540(self):
        self.assertEqual(*self.doTest("xchg    al, dl", "XCHG(al, dl)"))

    def test_instr_550(self):
        self.assertEqual(*self.doTest("xchg    ax, dx", "XCHG(ax, dx)"))

    def test_instr_560(self):
        self.assertEqual(*self.doTest("bt      ecx, edx", "BT(ecx, edx)"))

    def test_instr_570(self):
        self.assertEqual(*self.doTest("xchg    ax, word ptr [ebp+var_20]", "XCHG(ax, *(dw*)(raddr(ss,ebp+var_20)))"))

    def test_instr_580(self):
        self.assertEqual(*self.doTest("xchg    eax, dword ptr [ebp+var_20]", "XCHG(eax, *(dd*)(raddr(ss,ebp+var_20)))"))


    def test_instr_760(self):
        self.assertEqual(*self.doTest("lds     bx, offset unk_40F064", "LDS(bx, offset(initcall,unk_40f064))"))

    def test_instr_770(self):
        self.assertEqual(*self.doTest("les     bx, offset unk_40F064", "LES(bx, offset(initcall,unk_40f064))"))

    def test_instr_780(self):
        self.assertEqual(*self.doTest("lfs     bx, offset unk_40F064", "LFS(bx, offset(initcall,unk_40f064))"))

    def test_instr_790(self):
        self.assertEqual(*self.doTest("lgs     bx, offset unk_40F064", "LGS(bx, offset(initcall,unk_40f064))"))

    def test_instr_800(self):
        self.assertEqual(*self.doTest("pusha", "PUSHA"))

    def test_instr_810(self):
        self.assertEqual(*self.doTest("popa", "POPA"))

    def test_instr_820(self):
        self.assertEqual(*self.doTest("cli", "CLI"))

    def test_instr_830(self):
        self.assertEqual(*self.doTest("in   dx,al", "IN(dx, al)"))

    def test_instr_840(self):
        self.assertEqual(*self.doTest("shrd ax, dx, 3", "SHRD(ax, dx, 3)"))

    def test_instr_850(self):
        self.assertEqual(*self.doTest("btc     ecx, edx", "BTC(ecx, edx)"))

    def test_instr_860(self):
        self.assertEqual(*self.doTest("shld ax, dx, 3", "SHLD(ax, dx, 3)"))

    def test_instr_870(self):
        self.assertEqual(*self.doTest("enter 0,0", "ENTER(0, 0)"))

    def test_instr_880(self):
        self.assertEqual(*self.doTest("jmp $+2", "{;}"))

    def test_instr_890(self):
        self.assertEqual(*self.doTest("nop", "NOP"))

    def test_instr_900(self):
        self.assertEqual(*self.doTest("lods\t[byte ptr fs:si]", "LODS(*(raddr(fs,si)),si,1)"))

    def test_instr_910(self):
        self.assertEqual(*self.doTest("scas\t[word ptr fs:si]", "SCAS(*(dw*)(raddr(fs,si)),si,2)"))

    def test_instr_920(self):
        self.assertEqual(*self.doTest("movs [dword ptr es:di], [dword ptr fs:si]", "MOVS(*(dd*)(raddr(es,di)), *(dd*)(raddr(fs,si)), di, si, 4)"))

    def test_instr_930(self):
        self.assertEqual(*self.doTest("mov al, 'Z' - 'A' +1", "al = 'Z'-'A'+1;"))

    def test_instr_940(self):
        self.assertEqual(*self.doTest("mov ax,  not 1", "ax = ~1;"))

    def test_instr_941(self):
        self.assertEqual(*self.doTest("mov ax, 2 or 1", "ax = 2 | 1;"))

    def test_instr_950(self):
        self.assertEqual(*self.doTest("mov     [esp+8], eax", "MOV(*(dd*)(raddr(ss,esp+8)), eax)"))

    def test_instr_960(self):
        self.assertEqual(*self.doTest("cmp a,1", "CMP(*(a), 1)"))

    def test_instr_970(self):
        self.assertEqual(*self.doTest("btc eax,0", "BTC(eax, 0)"))


    def test_instr_1010(self):
        self.assertEqual(*self.doTest("mov     ds:byte_41411F[eax], dl", "*((&byte_41411f)+eax) = dl;"))

    def test_instr_1020(self):
        self.assertEqual(*self.doTest("lea     eax, large ds:4000h", "eax = 0x4000"))

    def test_instr_1030(self):
        self.assertEqual(*self.doTest("mov     ebx, offset _test_btc", "ebx = offset(initcall,_test_btc);"))

    def test_instr_1040(self):
        self.assertEqual(*self.doTest("pop     dword ptr [esp]", "POP(*(dd*)(raddr(ss,esp)))"))

    def test_instr_1050(self):
        self.assertEqual(*self.doTest("pop     eax", "POP(eax)"))

    def test_instr_1060(self):
        self.assertEqual(*self.doTest("pop     ebp", "POP(ebp)"))

    def test_instr_1070(self):
        self.assertEqual(*self.doTest("pop     ebx", "POP(ebx)"))

    def test_instr_1080(self):
        self.assertEqual(*self.doTest("btc eax,2", "BTC(eax, 2)"))

    def test_instr_1090(self):
        self.assertEqual(*self.doTest("pop     ecx", "POP(ecx)"))

    def test_instr_1100(self):
        self.assertEqual(*self.doTest("pop     edi", "POP(edi)"))

    def test_instr_1110(self):
        self.assertEqual(*self.doTest("pop     edi_0", "POP(edi_0)"))

    def test_instr_1120(self):
        self.assertEqual(*self.doTest("pop     edx", "POP(edx)"))

    def test_instr_1130(self):
        self.assertEqual(*self.doTest("pop     esi", "POP(esi)"))

    def test_instr_1140(self):
        self.assertEqual(*self.doTest("pop     esi_0", "POP(esi_0)"))

    def test_instr_1150(self):
        self.assertEqual(*self.doTest("pop     i", "POP(i)"))

    def test_instr_1160(self):
        self.assertEqual(*self.doTest("pop     res", "POP(res)"))

    def test_instr_1170(self):
        self.assertEqual(*self.doTest("pop     s0_0", "POP(s0_0)"))

    def test_instr_1180(self):
        self.assertEqual(*self.doTest("pop ds", "POP(ds)"))

    def test_instr_1190(self):
        self.assertEqual(*self.doTest("btr     cx, dx", "BTR(cx, dx)"))

    def test_instr_1200(self):
        self.assertEqual(*self.doTest("pop eax", "POP(eax)"))

    def test_instr_1210(self):
        self.assertEqual(*self.doTest("pop es", "POP(es)"))

    def test_instr_1220(self):
        self.assertEqual(*self.doTest("popad", "POPAD"))

    def test_instr_1230(self):
        self.assertEqual(*self.doTest("popf", "POPF"))

    def test_instr_1240(self):
        self.assertEqual(*self.doTest("push    0", "PUSH(0)"))

    def test_instr_1250(self):
        self.assertEqual(*self.doTest("push    0BC6058h", "PUSH(0x0BC6058)"))

    def test_instr_1260(self):
        self.assertEqual(*self.doTest("push    9ABCDEFh", "PUSH(0x9ABCDEF)"))

    def test_instr_1270(self):
        self.assertEqual(*self.doTest("push    esi", "PUSH(esi)"))

    def test_instr_1280(self):
        self.assertEqual(*self.doTest("push ds", "PUSH(ds)"))

    def test_instr_1290(self):
        self.assertEqual(*self.doTest("push ebx", "PUSH(ebx)"))

    def test_instr_1300(self):
        self.assertEqual(*self.doTest("btr     ecx, edx", "BTR(ecx, edx)"))

    def test_instr_1310(self):
        self.assertEqual(*self.doTest("push es", "PUSH(es)"))

    def test_instr_1320(self):
        self.assertEqual(*self.doTest("pushad", "PUSHAD"))

    def test_instr_1330(self):
        self.assertEqual(*self.doTest("pushf", "PUSHF"))

    def test_instr_1340(self):
        self.assertEqual(*self.doTest("repne lodsb", "LODSB"))

    def test_instr_1350(self):
        self.assertEqual(*self.doTest("call    dword ptr [ebx-4]", "CALLF(__dispatch_call,*(dd*)(raddr(ds,ebx-4)))"))

    def test_instr_1360(self):
        self.assertEqual(*self.doTest("call    exec_adc", "CALL(exec_adc,0)"))

    def test_instr_1370(self):
        self.assertEqual(*self.doTest("call    printf", "CALL(__dispatch_call,printf)"))

    def test_instr_1375(self):  # TODO is it right?
        self.assertEqual(*self.doTest("call    [test_bcd_ofs]", "CALL(__dispatch_call,test_bcd_ofs)"))

    def test_instr_1380(self):
        self.assertEqual(*self.doTest("btr eax,0", "BTR(eax, 0)"))

    def test_instr_1390(self):
        self.assertEqual(*self.doTest("call    test_bcd", "CALLF(test_bcd,0)"))

    def test_instr_1400(self):
        self.assertEqual(*self.doTest("call printeax", "CALL(printeax,0)"))

    def test_instr_1410(self):
        self.assertEqual(*self.doTest("cmp wordarray,2", "CMP(*(wordarray), 2)"))

    def test_instr_1420(self):
        self.assertEqual(*self.doTest("cmp wordarray,bx", "CMP(*(wordarray), bx)"))

    def test_instr_1430(self):
        self.assertEqual(*self.doTest("cmp singlebyte,-12", "CMP(singlebyte, -12)"))

    def test_instr_1440(self):
        self.assertEqual(*self.doTest("cmp singlebyte,ecx", "CMP(singlebyte, ecx)"))

    def test_instr_1450(self):
        self.assertEqual(*self.doTest("inc singlebyte", "INC(singlebyte)"))

    def test_instr_1460(self):
        self.assertEqual(*self.doTest("jmp [cs:wordtable+ax]", "return __dispatch_call(__disp, _state);"))

    def test_instr_1470(self):
        self.assertEqual(*self.doTest("mov a,5", "*(a) = 5;"))

    def test_instr_1480(self):
        self.assertEqual(*self.doTest("mov a,ah", "*(a) = ah;"))

    def test_instr_1490(self):
        self.assertEqual(*self.doTest("btr eax,2", "BTR(eax, 2)"))

    def test_instr_1500(self):
        self.assertEqual(*self.doTest("cmp b,256+3+65536", "CMP(b, 256+3+65536)"))

    def test_instr_1510(self):
        self.assertEqual(*self.doTest("cmp singlebyte2,1", "CMP(singlebyte2, 1)"))

    def test_instr_1520(self):
        self.assertEqual(*self.doTest("cmp singlebyte2,al", "CMP(singlebyte2, al)"))

    def test_instr_1530(self):
        self.assertEqual(*self.doTest("mov b,ax", "b = ax;"))

    def test_instr_1540(self):
        self.assertEqual(*self.doTest("mov dl,singlebyte2", "dl = singlebyte2;"))

    def test_instr_1550(self):
        self.assertEqual(*self.doTest("mov ebx,g", "ebx = g;"))

    def test_instr_1560(self):
        self.assertEqual(*self.doTest("cmp extrn_struc_inst.game_oppttypedw, 0", "CMP(extrn_struc_inst.game_oppttypedw, 0)"))

    def test_instr_1570(self):
        self.assertEqual(*self.doTest("mov     ax, offset extrn_struc_inst.game_oppttypedw+t", "ax = offset(default_seg,extrn_struc_inst.game_oppttypedw)+t;"))

    def test_instr_1580(self):
        self.assertEqual(*self.doTest("jmp loc_406B3F", "JMP(loc_406b3f)"))

    def test_instr_1590(self):
        self.assertEqual(*self.doTest("bts     cx, dx", "BTS(cx, dx)"))

    def test_instr_1600(self):
        self.assertEqual(*self.doTest("jmp cs:[bx]", "return __dispatch_call(__disp, _state);"))

    def test_instr_1610(self):
        self.assertEqual(*self.doTest("call exec_adc", "CALL(exec_adc,0)"))

    def test_instr_1620(self):
        self.assertEqual(*self.doTest("call far ptr test_bcd", "CALLF(test_bcd,0)"))

    def test_instr_1630(self):
        self.assertEqual(*self.doTest("mov ax, (offset extrn_struc_inst.game_oppttypedw+0AA8h)", "ax = offset(default_seg,extrn_struc_inst.game_oppttypedw)+0x0AA8;"))

    def test_instr_1640(self):
        self.assertEqual(*self.doTest("lea     si, [bx+di+TRANSSHAPESTRUC.ts_rotv_membr_strinst]", "si = bx+di+offsetof(transshapestruc,ts_rotv_membr_strinst)"))

    def test_instr_1650(self):
        self.assertEqual(*self.doTest("lea     ax, [si+(size TRANSSHAPESTRUC)]", "ax = si+(sizeof(transshapestruc))"))

    def test_instr_1660(self):
        self.assertEqual(*self.doTest("bts     ecx, edx", "BTS(ecx, edx)"))

    def test_instr_1670(self):
        self.assertEqual(*self.doTest("mov     dx, word ptr (oppresources+2)[bx]", "MOV(dx, *(dw*)(raddr(ds,(oppresources+2)+bx)))"))

    def test_instr_1680(self):
        self.assertEqual(*self.doTest("push    [bp+asgN_Aptr_in_struc.ts_rotv_membr_strinst.vxdw]", "PUSH(((transshapestruc*)raddr(ss,bp+asgn_aptr_in_struc))->ts_rotv_membr_strinst.vxdw)"))

    def test_instr_1690(self):
        self.assertEqual(*self.doTest("add     word ptr [bx+transshapestruc.ts_rotv_membr_strinst], ax", "ADD(*(dw*)(raddr(ds,bx+offsetof(transshapestruc,ts_rotv_membr_strinst))), ax)"))

    def test_instr_1700(self):
        self.assertEqual(*self.doTest("mov ax, (offset extrn_struc_inst.game_oppTTypeDW+0AA8h)", "ax = offset(default_seg,extrn_struc_inst.game_oppttypedw)+0x0AA8;"))

    def test_instr_1710(self):
        self.assertEqual(*self.doTest("adc     word ptr [bx+(transshapestruc.ts_rotv_membr_strinst+2)], dx", "ADC(*(dw*)(raddr(ds,bx+(offsetof(transshapestruc,ts_rotv_membr_strinst)+2))), dx)"))

    def test_instr_1720(self):
        self.assertEqual(*self.doTest("add     extrn_struc_inst.game_oppTTypeDW[di], 10h", "ADD(*(dw*)(((db*)&extrn_struc_inst.game_oppttypedw)+di), 0x10)"))

    def test_instr_1730(self):
        self.assertEqual(*self.doTest("inc     extrn_struc_inst.game_oppTTypeDW", "INC(extrn_struc_inst.game_oppttypedw)"))

    def test_instr_1740(self):
        self.assertEqual(*self.doTest("mov     dx, word ptr [bx+(gameinfostruc.game_oppTTypeDW+2)]", "MOV(dx, *(dw*)(raddr(ds,bx+(offsetof(gameinfostruc,game_oppttypedw)+2))))"))

    def test_instr_1750(self):
        self.assertEqual(*self.doTest("add     ax, gameInfoStruc.game_oppTTypeDW", "ADD(ax, offsetof(gameinfostruc,game_oppttypedw))"))

    def test_instr_1760(self):
        self.assertEqual(*self.doTest("adc     dx, word ptr [bp+asgn_aptr_in_struc.ts_rectptr+0Eh]", "ADC(dx, ((transshapestruc*)raddr(ss,bp+0x0E+asgn_aptr_in_struc))->ts_rectptr)"))

    def test_instr_1770(self):
        self.assertEqual(*self.doTest("bts eax,0", "BTS(eax, 0)"))

    def test_instr_1780(self):
        self.assertEqual(*self.doTest("sub     ax, es:[bx+di+(transshapestruc.ts_rotv_membr_strinst+24h)]", "SUB(ax, *(dw*)(raddr(es,bx+di+(offsetof(transshapestruc,ts_rotv_membr_strinst)+0x24))))"))

    def test_instr_1790(self):
        self.assertEqual(*self.doTest("cmp al, '\\'", "CMP(al, '\\\\')"))

    def test_instr_1800(self):
        self.assertEqual(*self.doTest("mov     ds:2, si", "MOV(*(dw*)(raddr(ds,2)), si)"))

    def test_instr_1810(self):
        self.assertEqual(*self.doTest("mov     ax, word ptr cs:extrn_struc_inst.game_opponentmaterial+2", "ax = *(dw*)(((db*)&extrn_struc_inst.game_opponentmaterial)+2);"))

    def test_instr_1820(self):
        self.assertEqual(*self.doTest("mov     al, byte ptr [bx+GAMEINFOSTRUC.game_oppttypedw]", "MOV(al, *(raddr(ds,bx+offsetof(gameinfostruc,game_oppttypedw))))"))

    def test_instr_1840(self):
        self.assertEqual(*self.doTest("mov     ax, fs:8", "MOV(ax, *(dw*)(raddr(fs,8)))"))

    def test_instr_1850(self):
        self.assertEqual(*self.doTest("bts eax,2", "BTS(eax, 2)"))

    def test_instr_1860(self):
        self.assertEqual(*self.doTest("movs dword ptr es:[di], dword ptr fs:[si]", "MOVS(*(dd*)(raddr(es,di)), *(dd*)(raddr(fs,si)), di, si, 4)"))

    def test_instr_1870(self):
        self.assertEqual(*self.doTest("cbw", "CBW"))

    def test_instr_1880(self):
        self.assertEqual(*self.doTest("call  near ptr  test_bcd", "CALL(test_bcd,0)"))

    def test_instr_1890(self):
        self.assertEqual(*self.doTest("call    far ptr test_bcd", "CALLF(test_bcd,0)"))

    def test_instr_1900(self):
        self.assertEqual(*self.doTest("xlat    byte ptr cs:[bx]", "XLATP(raddr(cs,bx))"))

    def test_instr_1910(self):
        self.assertEqual(*self.doTest("movs byte ptr es:[di], byte ptr cs:[si]", "MOVS(*(raddr(es,di)), *(raddr(cs,si)), di, si, 1)"))

    def test_instr_1920(self):
        self.assertEqual(*self.doTest("mov     ds:_byte_2D196_in_transition?, al", "_byte_2d196_in_transitionque = al;"))

    def test_instr_1930(self):
        self.assertEqual(*self.doTest("mov al, 4", "al = 4;"))

    def test_instr_1940(self):
        self.assertEqual(*self.doTest("cdq", "CDQ"))

    def test_instr_1950(self):
        self.assertEqual(*self.doTest("clc", "CLC"))

    def test_instr_1960(self):
        self.assertEqual(*self.doTest("cld", "CLD"))

    def test_instr_1970(self):
        self.assertEqual(*self.doTest("cmc", "CMC"))

    def test_instr_1980(self):
        self.assertEqual(*self.doTest("cmp     dl, cl", "CMP(dl, cl)"))

    def test_instr_1990(self):
        self.assertEqual(*self.doTest("cmp     dx, cx", "CMP(dx, cx)"))

    def test_instr_2000(self):
        self.assertEqual(*self.doTest("cmp     ebx, ebx", "CMP(ebx, ebx)"))

    def test_instr_2010(self):
        self.assertEqual(*self.doTest("cmp     ebx, edi", "CMP(ebx, edi)"))

    def test_instr_2020(self):
        self.assertEqual(*self.doTest("cmp     ebx, esi", "CMP(ebx, esi)"))

    def test_instr_2030(self):
        self.assertEqual(*self.doTest("CMP [wordarray],1", "CMP(*(wordarray), 1)"))

    def test_instr_2040(self):
        self.assertEqual(*self.doTest("cmp     ebx, offset unk_40F064", "CMP(ebx, offset(initcall,unk_40f064))"))

    def test_instr_2050(self):
        self.assertEqual(*self.doTest("cmp     ecx, 1", "CMP(ecx, 1)"))

    def test_instr_2060(self):
        self.assertEqual(*self.doTest("cmp     edi, ebx", "CMP(edi, ebx)"))

    def test_instr_2070(self):
        self.assertEqual(*self.doTest("cmp     edx, 1", "CMP(edx, 1)"))

    def test_instr_2080(self):
        self.assertEqual(*self.doTest("cmp     edx, ecx", "CMP(edx, ecx)"))

    def test_instr_2090(self):
        self.assertEqual(*self.doTest("cmp     esi, ebx", "CMP(esi, ebx)"))

    def test_instr_2100(self):
        self.assertEqual(*self.doTest("cmp     esi, edi", "CMP(esi, edi)"))

    def test_instr_2110(self):
        self.assertEqual(*self.doTest("cmp     esi, esi", "CMP(esi, esi)"))

    def test_instr_2120(self):
        self.assertEqual(*self.doTest("cmp     i, 1000h", "CMP(i, 0x1000)"))

    def test_instr_2130(self):
        self.assertEqual(*self.doTest("cmp     i, 100h", "CMP(i, 0x100)"))

    def test_instr_2140(self):
        self.assertEqual(*self.doTest("CMP [wordarray],13", "CMP(*(wordarray), 13)"))

    def test_instr_2150(self):
        self.assertEqual(*self.doTest("cmp     i, 10h", "CMP(i, 0x10)"))

    def test_instr_2160(self):
        self.assertEqual(*self.doTest("cmp     i, 20h", "CMP(i, 0x20)"))

    def test_instr_2170(self):
        self.assertEqual(*self.doTest("cmp     i, 4", "CMP(i, 4)"))

    def test_instr_2180(self):
        self.assertEqual(*self.doTest("cmp [a],5", "CMP(*(a), 5)"))

    def test_instr_2190(self):
        self.assertEqual(*self.doTest("cmp [var+3],5", "CMP(*((var)+3), 5)"))

    def test_instr_2200(self):
        self.assertEqual(*self.doTest("cmp [var+4],0", "CMP(*((var)+4), 0)"))

    def test_instr_2210(self):
        self.assertEqual(*self.doTest("cmp [var-1],0", "CMP(*((var)-1), 0)"))

    def test_instr_2220(self):
        self.assertEqual(*self.doTest("cmp [bytearray2+5],0", "CMP(*((bytearray2)+5), 0)"))

    def test_instr_2230(self):
        self.assertEqual(*self.doTest("cmp [singlebyte2+1],5", "CMP(*((&singlebyte2)+1), 5)"))

    def test_instr_2240(self):
        self.assertEqual(*self.doTest("cmp [singlebyte2],2", "CMP(singlebyte2, 2)"))

    def test_instr_2250(self):
        self.assertEqual(*self.doTest("CMP [singlebyte],35", "CMP(singlebyte, 35)"))

    def test_instr_2260(self):  # array of 3 words
        self.assertEqual(*self.doTest("cmp [wordarray+2],6", "CMP(*(dw*)(((db*)wordarray)+2), 6)"))

    def test_instr_2270(self):
        self.assertEqual(*self.doTest("cmp [wordarray-1],5", "CMP(*(dw*)(((db*)wordarray)-1), 5)"))

    def test_instr_2280(self):
        self.assertEqual(*self.doTest("cmp [wordarray],4", "CMP(*(wordarray), 4)"))

    def test_instr_2290(self):
        self.assertEqual(*self.doTest("cmp [singlebyte+3*4],40", "CMP(*((&singlebyte)+3*4), 40)"))

    def test_instr_2310(self):
        self.assertEqual(*self.doTest("cmp [bytearray+t],1", "CMP(*((bytearray)+t), 1)"))

    def test_instr_2320(self):
        self.assertEqual(*self.doTest("cmp [bytearray],2", "CMP(*(bytearray), 2)"))

    def test_instr_2330(self):
        self.assertEqual(*self.doTest("cmp [var],5", "CMP(*(var), 5)"))

    def test_instr_2340(self):
        self.assertEqual(*self.doTest("cmp ah,-1", "CMP(ah, -1)"))

    def test_instr_2350(self):
        self.assertEqual(*self.doTest("cmp ah,0ffh", "CMP(ah, 0x0ff)"))

    def test_instr_2360(self):
        self.assertEqual(*self.doTest("CMP eax,133", "CMP(eax, 133)"))

    def test_instr_2370(self):
        self.assertEqual(*self.doTest("cmp al,2", "CMP(al, 2)"))

    def test_instr_2380(self):
        self.assertEqual(*self.doTest("cmp al,ah", "CMP(al, ah)"))

    def test_instr_2390(self):
        self.assertEqual(*self.doTest("cmp ax,-5", "CMP(ax, -5)"))

    def test_instr_2400(self):
        self.assertEqual(*self.doTest("cmp bh,0cch", "CMP(bh, 0x0cc)"))

    def test_instr_2410(self):
        self.assertEqual(*self.doTest("cmp bl,001111111B", "CMP(bl, 0x7f)"))

    def test_instr_2420(self):
        self.assertEqual(*self.doTest("cmp bl,0ddh", "CMP(bl, 0x0dd)"))

    def test_instr_2430(self):
        self.assertEqual(*self.doTest("cmp bl,192", "CMP(bl, 192)"))

    def test_instr_2440(self):
        self.assertEqual(*self.doTest("cmp bl,193", "CMP(bl, 193)"))

    def test_instr_2450(self):
        self.assertEqual(*self.doTest("cmp bl,39h          ; above 9?", "CMP(bl, 0x39)"))

    def test_instr_2460(self):
        self.assertEqual(*self.doTest("cmp bl,al", "CMP(bl, al)"))

    def test_instr_2470(self):
        self.assertEqual(*self.doTest("CMP eax,2", "CMP(eax, 2)"))

    def test_instr_2480(self):
        self.assertEqual(*self.doTest("cmp bx,-1", "CMP(bx, -1)"))

    def test_instr_2490(self):
        self.assertEqual(*self.doTest("cmp bx,1", "CMP(bx, 1)"))

    def test_instr_2500(self):
        self.assertEqual(*self.doTest("cmp bx,4+5*256", "CMP(bx, 4+5*256)"))

    def test_instr_2510(self):
        self.assertEqual(*self.doTest("cmp bx,6*256+5", "CMP(bx, 6*256+5)"))

    def test_instr_2520(self):
        self.assertEqual(*self.doTest("cmp byte ptr [a],5", "CMP(*(a), 5)"))

    def test_instr_2530(self):
        self.assertEqual(*self.doTest("cmp byte ptr [edi+1],6", "CMP(*(raddr(ds,edi+1)), 6)"))

    def test_instr_2540(self):
        self.assertEqual(*self.doTest("cmp byte ptr [edi+7],132", "CMP(*(raddr(ds,edi+7)), 132)"))

    def test_instr_2550(self):
        self.assertEqual(*self.doTest("cmp byte ptr [esi],1", "CMP(*(raddr(ds,esi)), 1)"))

    def test_instr_2560(self):
        self.assertEqual(*self.doTest("cmp byte ptr [esi],4", "CMP(*(raddr(ds,esi)), 4)"))

    def test_instr_2570(self):
        self.assertEqual(*self.doTest("cmp byte ptr [testOVerlap+1],1", "CMP(*((testoverlap)+1), 1)"))

    def test_instr_2580(self):
        self.assertEqual(*self.doTest("CMP eax,3", "CMP(eax, 3)"))

    def test_instr_2590(self):
        self.assertEqual(*self.doTest("cmp byte ptr [singlebyte2+1],5", "CMP(*((&singlebyte2)+1), 5)"))

    def test_instr_2600(self):
        self.assertEqual(*self.doTest("cmp byte ptr [singlebyte2+2],5", "CMP(*((&singlebyte2)+2), 5)"))

    def test_instr_2610(self):
        self.assertEqual(*self.doTest("cmp byte ptr es:[0],55", "CMP(*(raddr(es,0)), 55)"))

    def test_instr_2620(self):
        self.assertEqual(*self.doTest("cmp byte ptr es:[0],56", "CMP(*(raddr(es,0)), 56)"))

    def test_instr_2630(self):
        self.assertEqual(*self.doTest("cmp byte ptr es:[0],57", "CMP(*(raddr(es,0)), 57)"))

    def test_instr_2640(self):
        self.assertEqual(*self.doTest("cmp ch,001111111B", "CMP(ch, 0x7f)"))

    def test_instr_2650(self):
        self.assertEqual(*self.doTest("cmp ch,011111100B", "CMP(ch, 0xfc)"))

    def test_instr_2660(self):
        self.assertEqual(*self.doTest("cmp dl,2", "CMP(dl, 2)"))

    def test_instr_2670(self):
        self.assertEqual(*self.doTest("cmp dl,4", "CMP(dl, 4)"))

    def test_instr_2680(self):
        self.assertEqual(*self.doTest("cmp dl,5", "CMP(dl, 5)"))

    def test_instr_2690(self):
        self.assertEqual(*self.doTest("INC [singlebyte2]", "INC(singlebyte2)"))

    def test_instr_2700(self):
        self.assertEqual(*self.doTest("cmp dword ptr bytearray,11", "CMP(*(dd*)(bytearray), 11)"))

    def test_instr_2710(self):
        self.assertEqual(*self.doTest("cmp dx,-1", "CMP(dx, -1)"))

    def test_instr_2720(self):
        self.assertEqual(*self.doTest("cmp dx,0", "CMP(dx, 0)"))

    def test_instr_2730(self):
        self.assertEqual(*self.doTest("cmp dx,11", "CMP(dx, 11)"))

    def test_instr_2740(self):
        self.assertEqual(*self.doTest("cmp dx,5", "CMP(dx, 5)"))

    def test_instr_2750(self):
        self.assertEqual(*self.doTest("cmp eax,-13", "CMP(eax, -13)"))

    def test_instr_2760(self):
        self.assertEqual(*self.doTest("cmp eax,-2", "CMP(eax, -2)"))

    def test_instr_2770(self):
        self.assertEqual(*self.doTest("cmp eax,-5", "CMP(eax, -5)"))

    def test_instr_2780(self):
        self.assertEqual(*self.doTest("cmp eax,0", "CMP(eax, 0)"))

    def test_instr_2790(self):
        self.assertEqual(*self.doTest("cmp eax,000f3h", "CMP(eax, 0x000f3)"))

    def test_instr_2800(self):
        self.assertEqual(*self.doTest("call dx", "CALL(__dispatch_call,dx)"))

    def test_instr_2810(self):
        self.assertEqual(*self.doTest("INC [wordarray]", "INC(*(wordarray))"))

    def test_instr_2820(self):
        self.assertEqual(*self.doTest("cmp eax,0101010101010101b", "CMP(eax, 0x5555)"))

    def test_instr_2830(self):
        self.assertEqual(*self.doTest("cmp eax,0101b", "CMP(eax, 0x5)"))

    def test_instr_2840(self):
        self.assertEqual(*self.doTest("cmp eax,077123456h", "CMP(eax, 0x077123456)"))

    def test_instr_2850(self):
        self.assertEqual(*self.doTest("cmp eax,0ffff0003h", "CMP(eax, 0x0ffff0003)"))

    def test_instr_2860(self):
        self.assertEqual(*self.doTest("cmp eax,0ffff00f3h", "CMP(eax, 0x0ffff00f3)"))

    def test_instr_2870(self):
        self.assertEqual(*self.doTest("cmp eax,0ffffff03h", "CMP(eax, 0x0ffffff03)"))

    def test_instr_2880(self):
        self.assertEqual(*self.doTest("cmp eax,0fffffff3h", "CMP(eax, 0x0fffffff3)"))

    def test_instr_2890(self):
        self.assertEqual(*self.doTest("cmp eax,1", "CMP(eax, 1)"))

    def test_instr_2900(self):
        self.assertEqual(*self.doTest("cmp eax,2", "CMP(eax, 2)"))

    def test_instr_2910(self):
        self.assertEqual(*self.doTest("cmp eax,256", "CMP(eax, 256)"))

    def test_instr_2920(self):
        self.assertEqual(*self.doTest("INC [singlebyte]", "INC(singlebyte)"))

    def test_instr_2930(self):
        self.assertEqual(*self.doTest("cmp eax,3", "CMP(eax, 3)"))

    def test_instr_2940(self):
        self.assertEqual(*self.doTest("cmp eax,4", "CMP(eax, 4)"))

    def test_instr_2950(self):
        self.assertEqual(*self.doTest("cmp eax,5", "CMP(eax, 5)"))

    def test_instr_2960(self):
        self.assertEqual(*self.doTest("cmp eax,6", "CMP(eax, 6)"))

    def test_instr_2970(self):
        self.assertEqual(*self.doTest("cmp eax,ebx", "CMP(eax, ebx)"))

    def test_instr_2980(self):
        self.assertEqual(*self.doTest("cmp ebp,9", "CMP(ebp, 9)"))

    def test_instr_2990(self):
        self.assertEqual(*self.doTest("cmp ebx,0", "CMP(ebx, 0)"))

    def test_instr_3000(self):
        self.assertEqual(*self.doTest("cmp ebx,010B", "CMP(ebx, 0x2)"))

    def test_instr_3010(self):
        self.assertEqual(*self.doTest("cmp ebx,0ffffff00h", "CMP(ebx, 0x0ffffff00)"))

    def test_instr_3020(self):
        self.assertEqual(*self.doTest("cmp ebx,1", "CMP(ebx, 1)"))

    def test_instr_3030(self):
        self.assertEqual(*self.doTest("INC eax", "INC(eax)"))

    def test_instr_3040(self):
        self.assertEqual(*self.doTest("cmp ebx,100h", "CMP(ebx, 0x100)"))

    def test_instr_3050(self):
        self.assertEqual(*self.doTest("cmp ebx,12345", "CMP(ebx, 12345)"))

    def test_instr_3060(self):
        self.assertEqual(*self.doTest("cmp ebx,2", "CMP(ebx, 2)"))

    def test_instr_3070(self):
        self.assertEqual(*self.doTest("cmp ebx,3", "CMP(ebx, 3)"))

    def test_instr_3080(self):
        self.assertEqual(*self.doTest("cmp ebx,TWO", "CMP(ebx, two)"))

    def test_instr_3090(self):
        self.assertEqual(*self.doTest("cmp ecx,-5", "CMP(ecx, -5)"))

    def test_instr_3100(self):
        self.assertEqual(*self.doTest("cmp ecx,0af222h", "CMP(ecx, 0x0af222)"))

    def test_instr_3110(self):
        self.assertEqual(*self.doTest("cmp ecx,0dff1h", "CMP(ecx, 0x0dff1)"))

    def test_instr_3120(self):
        self.assertEqual(*self.doTest("cmp ecx,0ffffh", "CMP(ecx, 0x0ffff)"))

    def test_instr_3130(self):
        self.assertEqual(*self.doTest("cmp ecx,3", "CMP(ecx, 3)"))

    def test_instr_3140(self):
        self.assertEqual(*self.doTest("INC edx", "INC(edx)"))

    def test_instr_3150(self):
        self.assertEqual(*self.doTest("cmp ecx,5", "CMP(ecx, 5)"))

    def test_instr_3160(self):
        self.assertEqual(*self.doTest("cmp edi,0", "CMP(edi, 0)"))

    def test_instr_3170(self):
        self.assertEqual(*self.doTest("cmp edi,esi", "CMP(edi, esi)"))

    def test_instr_3180(self):
        self.assertEqual(*self.doTest("cmp edi,offset bytearray+1", "CMP(edi, offset(_data,bytearray)+1)"))

    def test_instr_3190(self):
        self.assertEqual(*self.doTest("cmp edi,offset bytearray+4", "CMP(edi, offset(_data,bytearray)+4)"))

    def test_instr_3200(self):
        self.assertEqual(*self.doTest("cmp edx,-2", "CMP(edx, -2)"))

    def test_instr_3210(self):
        self.assertEqual(*self.doTest("cmp edx,0", "CMP(edx, 0)"))

    def test_instr_3220(self):
        self.assertEqual(*self.doTest("cmp edx,0abcdef77h", "CMP(edx, 0x0abcdef77)"))

    def test_instr_3230(self):
        self.assertEqual(*self.doTest("cmp edx,0ffffh", "CMP(edx, 0x0ffff)"))

    def test_instr_3240(self):
        self.assertEqual(*self.doTest("cmp edx,1", "CMP(edx, 1)"))

    def test_instr_3250(self):
        self.assertEqual(*self.doTest("cmp b,256+3", "CMP(b, 256+3)"))

    def test_instr_3260(self):
        self.assertEqual(*self.doTest("cmp edx,10", "CMP(edx, 10)"))

    def test_instr_3270(self):
        self.assertEqual(*self.doTest("cmp esi,0", "CMP(esi, 0)"))

    def test_instr_3280(self):
        self.assertEqual(*self.doTest("cmp esi,offset singlebyte2+1", "CMP(esi, offset(_data,singlebyte2)+1)"))

    def test_instr_3290(self):
        self.assertEqual(*self.doTest("cmp esi,offset singlebyte+4", "CMP(esi, offset(_data,singlebyte)+4)"))

    def test_instr_3300(self):
        self.assertEqual(*self.doTest("cmp singlebyte2[1],2", "CMP(*((&singlebyte2)+1), 2)"))

    def test_instr_3310(self):
        self.assertEqual(*self.doTest("cmp singlebyte2[bx+si],2", "CMP(*((&singlebyte2)+bx+si), 2)"))

    def test_instr_3320(self):
        self.assertEqual(*self.doTest("cmp singlebyte2[bx],2", "CMP(*((&singlebyte2)+bx), 2)"))

    def test_instr_3350(self):
        self.assertEqual(*self.doTest("cmp word ptr [singlequad+2],25", "CMP(*(dw*)(((db*)&singlequad)+2), 25)"))

    def test_instr_3360(self):
        self.assertEqual(*self.doTest("call [cs:wordtable+ax]", "CALL(__dispatch_call,*(dw*)(((db*)&wordtable)+ax))"))

    def test_instr_3370(self):
        self.assertEqual(*self.doTest("cmp word ptr [singlequad+2],50", "CMP(*(dw*)(((db*)&singlequad)+2), 50)"))

    def test_instr_3380(self):
        self.assertEqual(*self.doTest("cmp word ptr singlequad,0", "CMP(*(dw*)(&singlequad), 0)"))

    def test_instr_3390(self):
        self.assertEqual(*self.doTest("cmpsb", "CMPSB"))

    def test_instr_3400(self):
        self.assertEqual(*self.doTest("cmpsd", "CMPSD"))

    def test_instr_3410(self):
        self.assertEqual(*self.doTest("cmpsw", "CMPSW"))

    def test_instr_3420(self):
        self.assertEqual(*self.doTest("cmpxchg al, dl", "CMPXCHG(al, dl)"))

    def test_instr_3430(self):
        self.assertEqual(*self.doTest("cmpxchg ax, dx", "CMPXCHG(ax, dx)"))

    def test_instr_3440(self):
        self.assertEqual(*self.doTest("cmpxchg byte ptr [ebp+var_20], bl", "CMPXCHG(*(raddr(ss,ebp+var_20)), bl)"))

    def test_instr_3450(self):
        self.assertEqual(*self.doTest("cmpxchg byte ptr [ebp+var_20], dl", "CMPXCHG(*(raddr(ss,ebp+var_20)), dl)"))

    def test_instr_3460(self):
        self.assertEqual(*self.doTest("cmpxchg cl, dl", "CMPXCHG(cl, dl)"))

    def test_instr_3470(self):
        self.assertEqual(*self.doTest("CMP eax,1", "CMP(eax, 1)"))

    def test_instr_3480(self):
        self.assertEqual(*self.doTest("cmpxchg cx, dx", "CMPXCHG(cx, dx)"))

    def test_instr_3490(self):
        self.assertEqual(*self.doTest("cmpxchg dword ptr [ebp+var_20], edx", "CMPXCHG(*(dd*)(raddr(ss,ebp+var_20)), edx)"))

    def test_instr_3500(self):
        self.assertEqual(*self.doTest("cmpxchg eax, edx", "CMPXCHG(eax, edx)"))

    def test_instr_3510(self):
        self.assertEqual(*self.doTest("cmpxchg ecx, edx", "CMPXCHG(ecx, edx)"))

    def test_instr_3520(self):
        self.assertEqual(*self.doTest("cmpxchg word ptr [ebp+var_20], dx", "CMPXCHG(*(dw*)(raddr(ss,ebp+var_20)), dx)"))

    def test_instr_3530(self):
        self.assertEqual(*self.doTest("cmpxchg8b [ebp+var_20]", "CMPXCHG8B(*(raddr(ss,ebp+var_20)))"))

    def test_instr_3540(self):
        self.assertEqual(*self.doTest("cwd", "CWD"))

    def test_instr_3550(self):
        self.assertEqual(*self.doTest("cwde", "CWDE"))

    def test_instr_3560(self):
        self.assertEqual(*self.doTest("daa", "DAA"))

    def test_instr_3570(self):
        self.assertEqual(*self.doTest("das", "DAS"))

    def test_instr_3580(self):
        self.assertEqual(*self.doTest("cmp ebx,'dcba'", "CMP(ebx, 0x64636261)"))

    def test_instr_3590(self):
        self.assertEqual(*self.doTest("dec     dl", "DEC(dl)"))

    def test_instr_3600(self):
        self.assertEqual(*self.doTest("dec     dx", "DEC(dx)"))

    def test_instr_3610(self):
        self.assertEqual(*self.doTest("dec     edx", "DEC(edx)"))

    def test_instr_3620(self):
        self.assertEqual(*self.doTest("dec cl              ; decrease loop counter", "DEC(cl)"))

    def test_instr_3630(self):
        self.assertEqual(*self.doTest("dec cx", "DEC(cx)"))

    def test_instr_3640(self):
        self.assertEqual(*self.doTest("dec eax", "DEC(eax)"))

    def test_instr_3650(self):
        self.assertEqual(*self.doTest("div     cx", "DIV2(cx)"))

    def test_instr_3660(self):
        self.assertEqual(*self.doTest("div     dl", "DIV1(dl)"))

    def test_instr_3670(self):
        self.assertEqual(*self.doTest("div     s1_0", "DIV4(s1_0)"))

    def test_instr_3680(self):
        self.assertEqual(*self.doTest("idiv    cx", "IDIV2(cx)"))

    def test_instr_3690(self):
        self.assertEqual(*self.doTest("sub dl,'a'", "SUB(dl, 'a')"))

    def test_instr_3700(self):
        self.assertEqual(*self.doTest("idiv    dl", "IDIV1(dl)"))

    def test_instr_3710(self):
        self.assertEqual(*self.doTest("idiv    s1_0", "IDIV4(s1_0)"))

    def test_instr_9670(self):
        self.assertEqual(*self.doTest("mul     s1_0", "MUL1_4(s1_0)"))


    def test_instr_3820(self):
        self.assertEqual(*self.doTest("imul    eax, s1_0", "IMUL2_4(eax,s1_0)"))

    def test_instr_3830(self):
        self.assertEqual(*self.doTest("imul    ebx, esi, 7FFFh", "IMUL3_4(ebx,esi,0x7FFF)"))

    def test_instr_3840(self):
        self.assertEqual(*self.doTest("imul    s1_0", "IMUL1_4(s1_0)"))

    def test_instr_3850(self):
        self.assertEqual(*self.doTest("inc     dl", "INC(dl)"))

    def test_instr_3860(self):
        self.assertEqual(*self.doTest("inc     dx", "INC(dx)"))

    def test_instr_3870(self):
        self.assertEqual(*self.doTest("inc     i", "INC(i)"))

    def test_instr_3880(self):
        self.assertEqual(*self.doTest("inc byte ptr [edi+1]", "INC(*(raddr(ds,edi+1)))"))

    def test_instr_3890(self):
        self.assertEqual(*self.doTest("cmp [doublequote+4],'d'", "CMP(*((doublequote)+4), 'd')"))

    def test_instr_3990(self):
        self.assertEqual(*self.doTest("int 21h                         ; DOS INT 21h", "_INT(0x21)"))

    def test_instr_4000(self):
        self.assertEqual(*self.doTest("cmp dword ptr buffer,'tseT'", "CMP(*(dd*)(buffer), 0x74736554)"))

    def test_instr_4020(self):
        self.assertEqual(*self.doTest("jNC OK", "JNC(ok)"))

    def test_instr_4030(self):
        self.assertEqual(*self.doTest("ja      short loc_407784", "JA(loc_407784)"))

    def test_instr_4040(self):
        self.assertEqual(*self.doTest("jnbe failure", "JA(failure)"))

    def test_instr_4050(self):
        self.assertEqual(*self.doTest("jb      short loc_40723E", "JC(loc_40723e)"))

    def test_instr_4060(self):
        self.assertEqual(*self.doTest("jb failure  ; // because unsigned comparaiso\n", "JC(failure)"))

    def test_instr_4070(self):
        self.assertEqual(*self.doTest("jbe     short loc_40752C", "JBE(loc_40752c)"))

    def test_instr_4080(self):
        self.assertEqual(*self.doTest("jc failure", "JC(failure)"))

    def test_instr_4090(self):
        self.assertEqual(*self.doTest("jcxz    loc_4081F6", "JCXZ(loc_4081f6)"))

    def test_instr_4100(self):
        self.assertEqual(*self.doTest("jcxz @df@@@@7", "JCXZ(arbdfarbarbarbarb7)"))

    def test_instr_4110(self):
        self.assertEqual(*self.doTest("jcxz failure", "JCXZ(failure)"))

    def test_instr_4120(self):
        self.assertEqual(*self.doTest("je failure ; http://blog.rewolf.pl/blog/?p=177", "JZ(failure)"))

    def test_instr_4130(self):
        self.assertEqual(*self.doTest("je failure", "JZ(failure)"))

    def test_instr_4140(self):
        self.assertEqual(*self.doTest("je ok", "JZ(ok)"))

    def test_instr_4150(self):
        self.assertEqual(*self.doTest("jecxz   short loc_4083E9", "JECXZ(loc_4083e9)"))

    def test_instr_4160(self):
        self.assertEqual(*self.doTest("jg      short loc_40707C", "JG(loc_40707c)"))

    def test_instr_4170(self):
        self.assertEqual(*self.doTest("jg @df@@@@1", "JG(arbdfarbarbarbarb1)"))

    def test_instr_4180(self):
        self.assertEqual(*self.doTest("jg failure", "JG(failure)"))

    def test_instr_4190(self):
        self.assertEqual(*self.doTest("mov dl,'c'", "dl = 'c';"))

    def test_instr_4200(self):
        self.assertEqual(*self.doTest("jge     short loc_406EBA", "JGE(loc_406eba)"))

    def test_instr_4210(self):
        self.assertEqual(*self.doTest("jge @df@@@@2", "JGE(arbdfarbarbarbarb2)"))

    def test_instr_4220(self):
        self.assertEqual(*self.doTest("jge failure", "JGE(failure)"))

    def test_instr_4230(self):
        self.assertEqual(*self.doTest("jl      short loc_406B3F", "JL(loc_406b3f)"))

    def test_instr_4240(self):
        self.assertEqual(*self.doTest("jl @df@@@@4", "JL(arbdfarbarbarbarb4)"))

    def test_instr_4250(self):
        self.assertEqual(*self.doTest("jl failure", "JL(failure)"))

    def test_instr_4260(self):
        self.assertEqual(*self.doTest("jle     short loc_406CF8", "JLE(loc_406cf8)"))

    def test_instr_4270(self):
        self.assertEqual(*self.doTest("jle @df@@@@5", "JLE(arbdfarbarbarbarb5)"))

    def test_instr_4280(self):
        self.assertEqual(*self.doTest("jle failure", "JLE(failure)"))

    def test_instr_4290(self):
        self.assertEqual(*self.doTest("jmp     exec_rclb", "JMP(exec_rclb)"))

    def test_instr_4300(self):
        self.assertEqual(*self.doTest("mov ecx,'dcba'", "ecx = 0x64636261;"))

    def test_instr_4310(self):
        self.assertEqual(*self.doTest("jmp     short loc_40D571", "JMP(loc_40d571)"))

    def test_instr_4320(self):
        self.assertEqual(*self.doTest("jmp exitLabel", "JMP(exitlabel)"))

    def test_instr_4330(self):
        self.assertEqual(*self.doTest("jmp failure", "JMP(failure)"))

    def test_instr_4340(self):
        self.assertEqual(*self.doTest("jmp finTest", "JMP(fintest)"))

    def test_instr_4350(self):
        self.assertEqual(*self.doTest("jmp next", "JMP(next)"))

    def test_instr_4360(self):
        self.assertEqual(*self.doTest("jnC failure", "JNC(failure)"))

    def test_instr_4370(self):
        self.assertEqual(*self.doTest("jna short P2", "JBE(p2)"))

    def test_instr_4380(self):
        self.assertEqual(*self.doTest("jnb     short loc_4075C2", "JNC(loc_4075c2)"))

    def test_instr_4390(self):
        self.assertEqual(*self.doTest("jnb     short loc_407658", "JNC(loc_407658)"))

    def test_instr_4400(self):
        self.assertEqual(*self.doTest("jnb     short loc_4076EE", "JNC(loc_4076ee)"))

    def test_instr_4410(self):
        self.assertEqual(*self.doTest("CMP [singlebyte2],111", "CMP(singlebyte2, 111)"))

    def test_instr_4420(self):
        self.assertEqual(*self.doTest("jnb failure", "JNC(failure)"))

    def test_instr_4430(self):
        self.assertEqual(*self.doTest("jnc noerror", "JNC(noerror)"))

    def test_instr_4440(self):
        self.assertEqual(*self.doTest("jne exitLabel", "JNZ(exitlabel)"))

    def test_instr_4450(self):
        self.assertEqual(*self.doTest("jne failure", "JNZ(failure)"))

    def test_instr_4460(self):
        self.assertEqual(*self.doTest("jns     short loc_408008", "JNS(loc_408008)"))

    def test_instr_4470(self):
        self.assertEqual(*self.doTest("jns     short loc_40809E", "JNS(loc_40809e)"))

    def test_instr_4480(self):
        self.assertEqual(*self.doTest("jns     short loc_408139", "JNS(loc_408139)"))

    def test_instr_4490(self):
        self.assertEqual(*self.doTest("jns failure", "JNS(failure)"))

    def test_instr_4500(self):
        self.assertEqual(*self.doTest("jnz     loc_409652", "JNZ(loc_409652)"))

    def test_instr_4510(self):
        self.assertEqual(*self.doTest("JA failure", "JA(failure)"))

    def test_instr_4520(self):
        self.assertEqual(*self.doTest("jnz     short loc_4046D6", "JNZ(loc_4046d6)"))

    def test_instr_4530(self):
        self.assertEqual(*self.doTest("jnz P1              ; jump if cl is not equal 0 (zeroflag is not set)", "JNZ(p1)"))

    def test_instr_4540(self):
        self.assertEqual(*self.doTest("jnz failure", "JNZ(failure)"))

    def test_instr_4550(self):
        self.assertEqual(*self.doTest("js      short loc_407E46", "JS(loc_407e46)"))

    def test_instr_4560(self):
        self.assertEqual(*self.doTest("js      short loc_407F72", "JS(loc_407f72)"))

    def test_instr_4570(self):
        self.assertEqual(*self.doTest("js @df@@@@", "JS(arbdfarbarbarbarb)"))

    def test_instr_4580(self):
        self.assertEqual(*self.doTest("js failure", "JS(failure)"))

    def test_instr_4590(self):
        self.assertEqual(*self.doTest("jz      short loc_40458F", "JZ(loc_40458f)"))

    def test_instr_4600(self):
        self.assertEqual(*self.doTest("jz failure", "JZ(failure)"))

    def test_instr_4610(self):
        self.assertEqual(*self.doTest("lea     eax, [eax+4000h]", "eax = eax+0x4000"))

    def test_instr_4620(self):
        self.assertEqual(*self.doTest("JAE failure", "JNC(failure)"))

    def test_instr_4630(self):
        self.assertEqual(*self.doTest("lea     eax, [eax+40h]", "eax = eax+0x40"))

    def test_instr_4640(self):
        self.assertEqual(*self.doTest("lea     eax, [eax+ecx+40h]", "eax = eax+ecx+0x40"))

    def test_instr_4650(self):
        self.assertEqual(*self.doTest("lea     eax, [eax+ecx]", "eax = eax+ecx"))

    def test_instr_4660(self):
        self.assertEqual(*self.doTest("lea     eax, [eax]", "eax = eax"))

    def test_instr_4670(self):
        self.assertEqual(*self.doTest("lea     eax, [ebx+4000h]", "eax = ebx+0x4000"))

    def test_instr_4680(self):
        self.assertEqual(*self.doTest("lea     eax, [ebx+40h]", "eax = ebx+0x40"))

    def test_instr_4690(self):
        self.assertEqual(*self.doTest("lea     eax, [ebx+edx+4000h]", "eax = ebx+edx+0x4000"))

    def test_instr_4700(self):
        self.assertEqual(*self.doTest("lea     eax, [ebx+edx]", "eax = ebx+edx"))

    def test_instr_4710(self):
        self.assertEqual(*self.doTest("lea     eax, [ebx]", "eax = ebx"))

    def test_instr_4720(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx+4000h]", "eax = ecx+0x4000"))

    def test_instr_4730(self):
        self.assertEqual(*self.doTest("JB failure", "JC(failure)"))

    def test_instr_4740(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx+40h]", "eax = ecx+0x40"))

    def test_instr_4750(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx+ecx*2+4000h]", "eax = ecx+ecx*2+0x4000"))

    def test_instr_4760(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx+ecx*2-0Ah]", "eax = ecx+ecx*2-0x0A"))

    def test_instr_4770(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx+ecx*2]", "eax = ecx+ecx*2"))

    def test_instr_4780(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx+ecx]", "eax = ecx+ecx"))

    def test_instr_4790(self):
        self.assertEqual(*self.doTest("lea     eax, [ecx]", "eax = ecx"))

    def test_instr_4800(self):
        self.assertEqual(*self.doTest("lea     eax, [edi+4000h]", "eax = edi+0x4000"))

    def test_instr_4810(self):
        self.assertEqual(*self.doTest("lea     eax, [edi+40h]", "eax = edi+0x40"))

    def test_instr_4820(self):
        self.assertEqual(*self.doTest("lea     eax, [edi+ecx]", "eax = edi+ecx"))

    def test_instr_4830(self):
        self.assertEqual(*self.doTest("lea     eax, [edi]", "eax = edi"))

    def test_instr_4840(self):
        self.assertEqual(*self.doTest("JE @VBL2    ;on attends la fin du retrace", "JZ(arbvbl2)"))

    def test_instr_4850(self):
        self.assertEqual(*self.doTest("lea     eax, [edx+4000h]", "eax = edx+0x4000"))

    def test_instr_4860(self):
        self.assertEqual(*self.doTest("lea     eax, [edx+40h]", "eax = edx+0x40"))

    def test_instr_4870(self):
        self.assertEqual(*self.doTest("lea     eax, [edx+ecx*4+4000h]", "eax = edx+ecx*4+0x4000"))

    def test_instr_4880(self):
        self.assertEqual(*self.doTest("lea     eax, [edx+ecx*4-0Ah]", "eax = edx+ecx*4-0x0A"))

    def test_instr_4890(self):
        self.assertEqual(*self.doTest("lea     eax, [edx+ecx*4]", "eax = edx+ecx*4"))

    def test_instr_4900(self):
        self.assertEqual(*self.doTest("lea     eax, [edx+ecx]", "eax = edx+ecx"))

    def test_instr_4910(self):
        self.assertEqual(*self.doTest("lea     eax, [edx]", "eax = edx"))

    def test_instr_4920(self):
        self.assertEqual(*self.doTest("lea     eax, [esi+4000h]", "eax = esi+0x4000"))

    def test_instr_4930(self):
        self.assertEqual(*self.doTest("lea     eax, [esi+40h]", "eax = esi+0x40"))

    def test_instr_4940(self):
        self.assertEqual(*self.doTest("lea     eax, [esi+ecx*8-0Ah]", "eax = esi+ecx*8-0x0A"))

    def test_instr_4950(self):
        self.assertEqual(*self.doTest("JE @VBL22    ;on attends la fin du retrace", "JZ(arbvbl22)"))

    def test_instr_4960(self):
        self.assertEqual(*self.doTest("lea     eax, [esi+ecx*8]", "eax = esi+ecx*8"))

    def test_instr_4970(self):
        self.assertEqual(*self.doTest("lea     eax, [esi+ecx]", "eax = esi+ecx"))

    def test_instr_4980(self):
        self.assertEqual(*self.doTest("lea     eax, [esi]", "eax = esi"))

    def test_instr_4990(self):
        self.assertEqual(*self.doTest("lea     eax, ds:0[eax*2]", "eax = 0+eax*2"))

    def test_instr_5000(self):
        self.assertEqual(*self.doTest("lea     eax, ds:0[ebx*4]", "eax = 0+ebx*4"))

    def test_instr_5010(self):
        self.assertEqual(*self.doTest("lea     eax, ds:0[ecx*8]", "eax = 0+ecx*8"))

    def test_instr_5020(self):
        self.assertEqual(*self.doTest("lea     ebx, [ebp+wordtable]", "ebx = ebp+offset(_text,wordtable)"))

    def test_instr_5030(self):
        self.assertEqual(*self.doTest("lea     ebx, [esi+ecx*8+4000h]", "ebx = esi+ecx*8+0x4000"))

    def test_instr_5040(self):
        self.assertEqual(*self.doTest("lea     edi, [ebp+ecx_vals]", "edi = ebp+ecx_vals"))

    def test_instr_5050(self):
        self.assertEqual(*self.doTest("lea     edi, [i+2]", "edi = i+2"))

    def test_instr_5060(self):
        self.assertEqual(*self.doTest("JE failure", "JZ(failure)"))

    def test_instr_5070(self):
        self.assertEqual(*self.doTest("lea     edi, [i+3]", "edi = i+3"))

    def test_instr_5080(self):
        self.assertEqual(*self.doTest("lea     edi, [i+4]", "edi = i+4"))

    def test_instr_5090(self):
        self.assertEqual(*self.doTest("lea     edi, [i+5]", "edi = i+5"))

    def test_instr_5100(self):
        self.assertEqual(*self.doTest("lea     edi, [i-10h]", "edi = i-0x10"))

    def test_instr_5110(self):
        self.assertEqual(*self.doTest("lea     edx, [i+56h]", "edx = i+0x56"))

    def test_instr_5120(self):
        self.assertEqual(*self.doTest("lea     esi, [i+1]", "esi = i+1"))

    def test_instr_5130(self):
        self.assertEqual(*self.doTest("lea eax,enddata", "eax = offset(_data,enddata)"))

    def test_instr_5140(self):
        self.assertEqual(*self.doTest("lea ebx,beginningdata", "ebx = offset(_data,beginningdata)"))

    def test_instr_5150(self):
        self.assertEqual(*self.doTest("lea edi,buffer", "edi = offset(_data,buffer)"))

    def test_instr_5160(self):
        self.assertEqual(*self.doTest("lea edi,f", "edi = offset(_data,f)"))

    def test_instr_5170(self):
        self.assertEqual(*self.doTest("JMP exitLabel", "JMP(exitlabel)"))

    def test_instr_5180(self):
        self.assertEqual(*self.doTest("lea edi,testOVerlap", "edi = offset(_data,testoverlap)"))

    def test_instr_5190(self):
        self.assertEqual(*self.doTest("lea edi,singlebyte2", "edi = offset(_data,singlebyte2)"))

    def test_instr_5200(self):
        self.assertEqual(*self.doTest("lea edx,fileName", "edx = offset(_data,filename)"))

    def test_instr_5210(self):
        self.assertEqual(*self.doTest("lea esi,b", "esi = b"))

    def test_instr_5220(self):
        self.assertEqual(*self.doTest("lea esi,f", "esi = offset(_data,f)"))

    def test_instr_5230(self):
        self.assertEqual(*self.doTest("lea esi,wordarray", "esi = offset(_data,wordarray)"))

    def test_instr_5240(self):
        self.assertEqual(*self.doTest("lea esi,singlequad", "esi = offset(_data,singlequad)"))

    def test_instr_5250(self):
        self.assertEqual(*self.doTest("leave", "LEAVE"))

    def test_instr_5260(self):
        self.assertEqual(*self.doTest("lodsb", "LODSB"))

    def test_instr_5270(self):
        self.assertEqual(*self.doTest("lodsd", "LODSD"))

    def test_instr_5280(self):
        self.assertEqual(*self.doTest("JNE @VBL1    ;on attends le retrace", "JNZ(arbvbl1)"))

    def test_instr_5290(self):
        self.assertEqual(*self.doTest("lodsw", "LODSW"))

    def test_instr_5300(self):
        self.assertEqual(*self.doTest("loop    loc_408464", "LOOP(loc_408464)"))

    def test_instr_5310(self):
        self.assertEqual(*self.doTest("loop dffd", "LOOP(dffd)"))

    def test_instr_5320(self):
        self.assertEqual(*self.doTest("loope   loc_4084DF", "LOOPE(loc_4084df)"))

    def test_instr_5330(self):
        self.assertEqual(*self.doTest("loope toto1", "LOOPE(toto1)"))

    def test_instr_5340(self):
        self.assertEqual(*self.doTest("loopne  loc_40855A", "LOOPNE(loc_40855a)"))

    def test_instr_5350(self):
        self.assertEqual(*self.doTest("mov     [ebp+ecx_0], ecx_0_0", "MOV(*(dd*)(raddr(ss,ebp+ecx_0)), ecx_0_0)"))

    def test_instr_5360(self):
        self.assertEqual(*self.doTest("mov     [ebp+edx_0], edx", "MOV(*(dd*)(raddr(ss,ebp+edx_0)), edx)"))

    def test_instr_5370(self):
        self.assertEqual(*self.doTest("mov     [ebp+s0], esi", "MOV(*(dd*)(raddr(ss,ebp+s0)), esi)"))

    def test_instr_5380(self):
        self.assertEqual(*self.doTest("mov     [ebp+s1], 0", "MOV(*(raddr(ss,ebp+s1)), 0)"))

    def test_instr_5390(self):
        self.assertEqual(*self.doTest("JNE @VBL12    ;on attends le retrace", "JNZ(arbvbl12)"))

    def test_instr_5400(self):
        self.assertEqual(*self.doTest("mov     [ebp+s1], 1", "MOV(*(raddr(ss,ebp+s1)), 1)"))

    def test_instr_5410(self):
        self.assertEqual(*self.doTest("mov     [ebp+s2], ebx", "MOV(*(dd*)(raddr(ss,ebp+s2)), ebx)"))

    def test_instr_5420(self):
        self.assertEqual(*self.doTest("mov     [ebp+var_1C], edx", "MOV(*(dd*)(raddr(ss,ebp+var_1c)), edx)"))

    def test_instr_5430(self):
        self.assertEqual(*self.doTest("mov     [ebp+var_20], ecx", "MOV(*(dd*)(raddr(ss,ebp+var_20)), ecx)"))

    def test_instr_5440(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], ebx", "MOV(*(dd*)(raddr(ss,esp+0x0C)), ebx)"))

    def test_instr_5450(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], ecx", "MOV(*(dd*)(raddr(ss,esp+0x0C)), ecx)"))

    def test_instr_5460(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], edi", "MOV(*(dd*)(raddr(ss,esp+0x0C)), edi)"))

    def test_instr_5470(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], edi_0", "MOV(*(dd*)(raddr(ss,esp+0x0C)), edi_0)"))

    def test_instr_5480(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], edx", "MOV(*(dd*)(raddr(ss,esp+0x0C)), edx)"))

    def test_instr_5490(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], op0", "MOV(*(raddr(ss,esp+0x0C)), op0)"))

    def test_instr_5500(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], op1", "MOV(*(dd*)(raddr(ss,esp+0x0C)), op1)"))

    def test_instr_5510(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], r", "MOV(*(dd*)(raddr(ss,esp+0x0C)), r)"))

    def test_instr_5520(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], res", "MOV(*(dd*)(raddr(ss,esp+0x0C)), res)"))

    def test_instr_5530(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], resz", "MOV(*(dd*)(raddr(ss,esp+0x0C)), resz)"))

    def test_instr_5540(self):
        self.assertEqual(*self.doTest("mov     [esp+0Ch], s1_0", "MOV(*(dd*)(raddr(ss,esp+0x0C)), s1_0)"))

    def test_instr_5550(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], eax", "MOV(*(dd*)(raddr(ss,esp+0x10)), eax)"))

    def test_instr_5560(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], eax_0", "MOV(*(dd*)(raddr(ss,esp+0x10)), eax_0)"))

    def test_instr_5570(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], ebx", "MOV(*(dd*)(raddr(ss,esp+0x10)), ebx)"))

    def test_instr_5580(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], ecx", "MOV(*(dd*)(raddr(ss,esp+0x10)), ecx)"))

    def test_instr_5590(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], op1", "MOV(*(dd*)(raddr(ss,esp+0x10)), op1)"))

    def test_instr_5600(self):
        self.assertEqual(*self.doTest("JNZ  @@saaccvaaaax", "JNZ(arbarbsaaccvaaaax)"))

    def test_instr_5610(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], res", "MOV(*(dd*)(raddr(ss,esp+0x10)), res)"))

    def test_instr_5620(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], resz", "MOV(*(dd*)(raddr(ss,esp+0x10)), resz)"))

    def test_instr_5630(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], rh", "MOV(*(dd*)(raddr(ss,esp+0x10)), rh)"))

    def test_instr_5640(self):
        self.assertEqual(*self.doTest("mov     [esp+10h], s1_0", "MOV(*(dd*)(raddr(ss,esp+0x10)), s1_0)"))

    def test_instr_5650(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], eax", "MOV(*(dd*)(raddr(ss,esp+0x14)), eax)"))

    def test_instr_5660(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], ebx", "MOV(*(dd*)(raddr(ss,esp+0x14)), ebx)"))

    def test_instr_5670(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], ecx", "MOV(*(dd*)(raddr(ss,esp+0x14)), ecx)"))

    def test_instr_5680(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], ecx_0", "MOV(*(raddr(ss,esp+0x14)), ecx_0)"))

    def test_instr_5690(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], edi", "MOV(*(dd*)(raddr(ss,esp+0x14)), edi)"))

    def test_instr_5700(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], edx", "MOV(*(dd*)(raddr(ss,esp+0x14)), edx)"))

    def test_instr_5710(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], esi", "MOV(*(dd*)(raddr(ss,esp+0x14)), esi)"))

    def test_instr_5720(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], flags", "MOV(*(dd*)(raddr(ss,esp+0x14)), flags)"))

    def test_instr_5730(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], res", "MOV(*(dd*)(raddr(ss,esp+0x14)), res)"))

    def test_instr_5740(self):
        self.assertEqual(*self.doTest("mov     [esp+14h], resh", "MOV(*(dd*)(raddr(ss,esp+0x14)), resh)"))

    def test_instr_5750(self):
        self.assertEqual(*self.doTest("mov     [esp+18h], eax", "MOV(*(dd*)(raddr(ss,esp+0x18)), eax)"))

    def test_instr_5760(self):
        self.assertEqual(*self.doTest("mov     [esp+18h], edi", "MOV(*(dd*)(raddr(ss,esp+0x18)), edi)"))

    def test_instr_5770(self):
        self.assertEqual(*self.doTest("mov     [esp+18h], edx", "MOV(*(dd*)(raddr(ss,esp+0x18)), edx)"))

    def test_instr_5780(self):
        self.assertEqual(*self.doTest("mov     [esp+18h], res", "MOV(*(dd*)(raddr(ss,esp+0x18)), res)"))

    def test_instr_5790(self):
        self.assertEqual(*self.doTest("mov     [esp+1Ch], eax", "MOV(*(dd*)(raddr(ss,esp+0x1C)), eax)"))

    def test_instr_5800(self):
        self.assertEqual(*self.doTest("mov     [esp+1Ch], ebx", "MOV(*(dd*)(raddr(ss,esp+0x1C)), ebx)"))

    def test_instr_5810(self):
        self.assertEqual(*self.doTest("MOV DX,3DAh", "dx = 0x3DA;"))

    def test_instr_5820(self):
        self.assertEqual(*self.doTest("mov     [esp+4], eax_0", "MOV(*(dd*)(raddr(ss,esp+4)), eax_0)"))

    def test_instr_5830(self):
        self.assertEqual(*self.doTest("mov     [esp+4], ebx    ; s0", "MOV(*(dd*)(raddr(ss,esp+4)), ebx)"))

    def test_instr_5840(self):
        self.assertEqual(*self.doTest("mov     [esp+4], edi    ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), edi)"))

    def test_instr_5850(self):
        self.assertEqual(*self.doTest("mov     [esp+4], esi    ; s0", "MOV(*(dd*)(raddr(ss,esp+4)), esi)"))

    def test_instr_5860(self):
        self.assertEqual(*self.doTest("mov     [esp+4], esi    ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), esi)"))

    def test_instr_5870(self):
        self.assertEqual(*self.doTest("mov     [esp+4], i      ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), i)"))

    def test_instr_5880(self):
        self.assertEqual(*self.doTest("mov     [esp+4], res", "MOV(*(dd*)(raddr(ss,esp+4)), res)"))

    def test_instr_5890(self):
        self.assertEqual(*self.doTest("mov     [esp+8], ebx    ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), ebx)"))

    def test_instr_5900(self):
        self.assertEqual(*self.doTest("mov     [esp+8], ebx", "MOV(*(dd*)(raddr(ss,esp+8)), ebx)"))

    def test_instr_5910(self):
        self.assertEqual(*self.doTest("mov     [esp+8], ecx", "MOV(*(dd*)(raddr(ss,esp+8)), ecx)"))

    def test_instr_5920(self):
        self.assertEqual(*self.doTest("mov     [esp+8], ecx_0_0", "MOV(*(dd*)(raddr(ss,esp+8)), ecx_0_0)"))

    def test_instr_5930(self):
        self.assertEqual(*self.doTest("mov     [esp+8], edi    ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), edi)"))

    def test_instr_5940(self):
        self.assertEqual(*self.doTest("mov     [esp+8], edi    ; s1", "MOV(*(dd*)(raddr(ss,esp+8)), edi)"))

    def test_instr_5950(self):
        self.assertEqual(*self.doTest("mov     [esp+8], edx_0_0", "MOV(*(dd*)(raddr(ss,esp+8)), edx_0_0)"))

    def test_instr_5960(self):
        self.assertEqual(*self.doTest("mov     [esp+8], esi    ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), esi)"))

    def test_instr_5970(self):
        self.assertEqual(*self.doTest("mov     [esp+8], esi    ; s1", "MOV(*(dd*)(raddr(ss,esp+8)), esi)"))

    def test_instr_5980(self):
        self.assertEqual(*self.doTest("mov     [esp+8], esi", "MOV(*(dd*)(raddr(ss,esp+8)), esi)"))

    def test_instr_5990(self):
        self.assertEqual(*self.doTest("mov     [esp+8], esi_0", "MOV(*(dd*)(raddr(ss,esp+8)), esi_0)"))

    def test_instr_6000(self):
        self.assertEqual(*self.doTest("mov     [esp+8], i      ; s1", "MOV(*(dd*)(raddr(ss,esp+8)), i)"))

    def test_instr_6010(self):
        self.assertEqual(*self.doTest("MOV ds, _data", "ds = seg_offset(_data);"))

    def test_instr_6020(self):
        self.assertEqual(*self.doTest("mov     [esp+8], i", "MOV(*(dd*)(raddr(ss,esp+8)), i)"))

    def test_instr_6030(self):
        self.assertEqual(*self.doTest("mov     [esp+8], op0", "MOV(*(raddr(ss,esp+8)), op0)"))

    def test_instr_6040(self):
        self.assertEqual(*self.doTest("mov     [esp+8], res", "MOV(*(dd*)(raddr(ss,esp+8)), res)"))

    def test_instr_6050(self):
        self.assertEqual(*self.doTest("mov     [esp+8], resh", "MOV(*(dd*)(raddr(ss,esp+8)), resh)"))

    def test_instr_6060(self):
        self.assertEqual(*self.doTest("mov     [esp+8], s0_0", "MOV(*(dd*)(raddr(ss,esp+8)), s0_0)"))

    def test_instr_6070(self):
        self.assertEqual(*self.doTest("mov     [esp], ebx      ; s0", "MOV(*(dd*)(raddr(ss,esp)), ebx)"))

    def test_instr_6080(self):
        self.assertEqual(*self.doTest("mov     [esp], ebx      ; s2", "MOV(*(dd*)(raddr(ss,esp)), ebx)"))

    def test_instr_6090(self):
        self.assertEqual(*self.doTest("mov     [esp], edi      ; s2", "MOV(*(dd*)(raddr(ss,esp)), edi)"))

    def test_instr_6100(self):
        self.assertEqual(*self.doTest("mov     dl, al", "dl = al;"))

    def test_instr_6110(self):
        self.assertEqual(*self.doTest("mov     dword ptr [ebp+var_20+4], 0FBCA7h", "MOV(*(dd*)(raddr(ss,ebp+var_20+4)), 0x0FBCA7)"))

    def test_instr_6120(self):
        self.assertEqual(*self.doTest("SHL ch,2", "SHL(ch, 2)"))

    def test_instr_6130(self):
        self.assertEqual(*self.doTest("mov     dword ptr [ebp+var_20+4], 12345h", "MOV(*(dd*)(raddr(ss,ebp+var_20+4)), 0x12345)"))

    def test_instr_6140(self):
        self.assertEqual(*self.doTest("mov     dword ptr [ebp+var_20], 0FBCA7654h", "MOV(*(dd*)(raddr(ss,ebp+var_20)), 0x0FBCA7654)"))

    def test_instr_6150(self):
        self.assertEqual(*self.doTest("mov     dword ptr [ebp+var_20], 65423456h", "MOV(*(dd*)(raddr(ss,ebp+var_20)), 0x65423456)"))

    def test_instr_6160(self):
        self.assertEqual(*self.doTest("mov     dword ptr [ebp+var_20], 6789ABCDh", "MOV(*(dd*)(raddr(ss,ebp+var_20)), 0x6789ABCD)"))

    def test_instr_6170(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+0Ch], 0 ; iflags", "MOV(*(dd*)(raddr(ss,esp+0x0C)), 0)"))

    def test_instr_6180(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+0Ch], 0", "MOV(*(dd*)(raddr(ss,esp+0x0C)), 0)"))

    def test_instr_6190(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+0Ch], 1 ; iflags", "MOV(*(dd*)(raddr(ss,esp+0x0C)), 1)"))

    def test_instr_6210(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+0Ch], 1234h", "MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x1234)"))

    def test_instr_6220(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+0Ch], 17h", "MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x17)"))

    def test_instr_6230(self):
        self.assertEqual(*self.doTest("SHR bl,1", "SHR(bl, 1)"))

    def test_instr_6240(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+0Ch], 80000000h", "MOV(*(dd*)(raddr(ss,esp+0x0C)), 0x80000000)"))

    def test_instr_6250(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+10h], 0", "MOV(*(dd*)(raddr(ss,esp+0x10)), 0)"))

    def test_instr_6260(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+10h], 1", "MOV(*(dd*)(raddr(ss,esp+0x10)), 1)"))

    def test_instr_6270(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+10h], 10h", "MOV(*(dd*)(raddr(ss,esp+0x10)), 0x10)"))

    def test_instr_6280(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+10h], 11h", "MOV(*(dd*)(raddr(ss,esp+0x10)), 0x11)"))

    def test_instr_6300(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+1Ch], 0", "MOV(*(dd*)(raddr(ss,esp+0x1C)), 0)"))

    def test_instr_6310(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 0 ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0)"))

    def test_instr_6320(self):
        self.assertEqual(*self.doTest("SHR ch,1", "SHR(ch, 1)"))

    def test_instr_6330(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 0FFFC70F9h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x0FFFC70F9)"))

    def test_instr_6340(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 0FFFFFFD3h ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x0FFFFFFD3)"))

    def test_instr_6350(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 0FFFFFFFFh ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x0FFFFFFFF)"))

    def test_instr_6360(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 10000h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x10000)"))

    def test_instr_6370(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 100h ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x100)"))

    def test_instr_6380(self):
        self.assertEqual(*self.doTest("SHR eax,1", "SHR(eax, 1)"))

    def test_instr_6390(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 10h ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x10)"))

    def test_instr_6400(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 1234001Dh ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x1234001D)"))

    def test_instr_6410(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 12341h ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x12341)"))

    def test_instr_6420(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 12345678h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x12345678)"))

    def test_instr_6430(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 12345678h ; s0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x12345678)"))

    def test_instr_6440(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 12348000h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x12348000)"))

    def test_instr_6450(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 127Eh ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x127E)"))

    def test_instr_6460(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 17h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x17)"))

    def test_instr_6470(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 1FF7Fh ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x1FF7F)"))

    def test_instr_6480(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 1FF80h ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x1FF80)"))

    def test_instr_6490(self):
        self.assertEqual(*self.doTest("TEST AL,8", "TEST(al, 8)"))

    def test_instr_6500(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 1FF81h ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x1FF81)"))

    def test_instr_6510(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 1FFFFh ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x1FFFF)"))

    def test_instr_6520(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 2 ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 2)"))

    def test_instr_6530(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 2 ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 2)"))

    def test_instr_6540(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 20000h ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x20000)"))

    def test_instr_6550(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 2Dh ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x2D)"))

    def test_instr_6560(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 3 ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 3)"))

    def test_instr_6570(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 3 ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 3)"))

    def test_instr_6580(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 4 ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 4)"))

    def test_instr_6590(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 7FFFFFFFh ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x7FFFFFFF)"))

    def test_instr_6600(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 80000000h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x80000000)"))

    def test_instr_6610(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 80000000h ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x80000000)"))

    def test_instr_6620(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 80000001h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x80000001)"))

    def test_instr_6630(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 80008688h ; s0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x80008688)"))

    def test_instr_6640(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 8000h ; op0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x8000)"))

    def test_instr_6650(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 8000h ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x8000)"))

    def test_instr_6660(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 80h ; op1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x80)"))

    def test_instr_6670(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 80h ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x80)"))

    def test_instr_6680(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 812FADAh ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x812FADA)"))

    def test_instr_6690(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 81h ; s1", "MOV(*(dd*)(raddr(ss,esp+4)), 0x81)"))

    def test_instr_6700(self):
        self.assertEqual(*self.doTest("aaa", "AAA"))

    def test_instr_6710(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+4], 82345679h ; s0", "MOV(*(dd*)(raddr(ss,esp+4)), 0x82345679)"))

    def test_instr_6720(self):
        self.assertEqual(*self.doTest('mov     dword ptr [esp+4], offset aXorw ; "xorw"', "MOV(*(dd*)(raddr(ss,esp+4)), offset(_rdata,axorw))"))

    def test_instr_6730(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0 ; iflags", "MOV(*(dd*)(raddr(ss,esp+8)), 0)"))

    def test_instr_6760(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FBCA7654h", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FBCA7654)"))

    def test_instr_6770(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFFFF)"))

    def test_instr_6780(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFFFFFFh", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFFFF)"))

    def test_instr_6790(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFFF)"))

    def test_instr_6800(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFFF)"))

    def test_instr_6810(self):
        self.assertEqual(*self.doTest("aad", "AAD"))

    def test_instr_6820(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFFF)"))

    def test_instr_6830(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFFF)"))

    def test_instr_6840(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FFF)"))

    def test_instr_6850(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0FFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0FF)"))

    def test_instr_6860(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 0Fh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x0F)"))

    def test_instr_6870(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1 ; iflags", "MOV(*(dd*)(raddr(ss,esp+8)), 1)"))

    def test_instr_6880(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1 ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 1)"))

    def test_instr_6890(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 10000h ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x10000)"))

    def test_instr_6900(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 100h ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x100)"))

    def test_instr_6910(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 12340128h", "MOV(*(dd*)(raddr(ss,esp+8)), 0x12340128)"))

    def test_instr_6920(self):
        self.assertEqual(*self.doTest("aam", "AAM"))

    def test_instr_6930(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 12Ch ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x12C)"))

    def test_instr_6940(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1FFFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFFFFF)"))

    def test_instr_6950(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1FFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFFFF)"))

    def test_instr_6960(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1FFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFFF)"))

    def test_instr_6970(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1FFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFFF)"))

    def test_instr_6980(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1FFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1FFF)"))

    def test_instr_6990(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1FFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1FF)"))

    def test_instr_7000(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 1Fh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x1F)"))

    def test_instr_7010(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 2 ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 2)"))

    def test_instr_7020(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 2Dh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x2D)"))

    def test_instr_7030(self):
        self.assertEqual(*self.doTest("aas", "AAS"))

    def test_instr_7040(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 2Dh", "MOV(*(dd*)(raddr(ss,esp+8)), 0x2D)"))

    def test_instr_7050(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3 ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 3)"))

    def test_instr_7060(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 303Bh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x303B)"))

    def test_instr_7070(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 340128h", "MOV(*(dd*)(raddr(ss,esp+8)), 0x340128)"))

    def test_instr_7080(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3FFFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFFFFF)"))

    def test_instr_7090(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3FFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFFFF)"))

    def test_instr_7100(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3FFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFFF)"))

    def test_instr_7110(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3FFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFFF)"))

    def test_instr_7120(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3FFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3FFF)"))

    def test_instr_7130(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3FFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3FF)"))

    def test_instr_7140(self):
        self.assertEqual(*self.doTest("adc     dl, cl", "ADC(dl, cl)"))

    def test_instr_7150(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 3Fh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x3F)"))

    def test_instr_7160(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFFFF)"))

    def test_instr_7170(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFFFFFh", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFFFF)"))

    def test_instr_7180(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFFF)"))

    def test_instr_7190(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFFF)"))

    def test_instr_7200(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFFF)"))

    def test_instr_7210(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFF)"))

    def test_instr_7220(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFFh", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FFF)"))

    def test_instr_7230(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7FFh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7FF)"))

    def test_instr_7240(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 7Fh ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x7F)"))

    def test_instr_7250(self):
        self.assertEqual(*self.doTest("adc     dx, cx", "ADC(dx, cx)"))

    def test_instr_7260(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 80000000h ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x80000000)"))

    def test_instr_7270(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 8000h ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x8000)"))

    def test_instr_7280(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 8000h", "MOV(*(dd*)(raddr(ss,esp+8)), 0x8000)"))

    def test_instr_7290(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 81234567h ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x81234567)"))

    def test_instr_7300(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 81238567h ; op1", "MOV(*(dd*)(raddr(ss,esp+8)), 0x81238567)"))

    def test_instr_7310(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp+8], 8234A6F8h", "MOV(*(dd*)(raddr(ss,esp+8)), 0x8234A6F8)"))

    def test_instr_7320(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0 ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0)"))

    def test_instr_7330(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0 ; s0", "MOV(*(dd*)(raddr(ss,esp)), 0)"))

    def test_instr_7340(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0Eh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0E)"))

    def test_instr_7350(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FE)"))

    def test_instr_7360(self):
        self.assertEqual(*self.doTest("adc     edx, ecx", "ADC(edx, ecx)"))

    def test_instr_7370(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFE)"))

    def test_instr_7380(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFE0080h ; s0", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFE0080)"))

    def test_instr_7390(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFE0080h ; s2", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFE0080)"))

    def test_instr_7400(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFE)"))

    def test_instr_7410(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFE)"))

    def test_instr_7420(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFE)"))

    def test_instr_7430(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFECh ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFEC)"))

    def test_instr_7440(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFECh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFEC)"))

    def test_instr_7450(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFE)"))

    def test_instr_7460(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFFDh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFD)"))

    def test_instr_7470(self):
        self.assertEqual(*self.doTest("add     dl, cl", "ADD(dl, cl)"))

    def test_instr_7480(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFE)"))

    def test_instr_7490(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFFFh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFF)"))

    def test_instr_7500(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFFFh ; s0", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFF)"))

    def test_instr_7510(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 0FFFFFFFFh ; s2", "MOV(*(dd*)(raddr(ss,esp)), 0x0FFFFFFFF)"))

    def test_instr_7520(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1 ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 1)"))

    def test_instr_7530(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 10000h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x10000)"))

    def test_instr_7540(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 100h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x100)"))

    def test_instr_7550(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 10h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x10)"))

    def test_instr_7560(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 12340004h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x12340004)"))

    def test_instr_7570(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 12341h ; s0", "MOV(*(dd*)(raddr(ss,esp)), 0x12341)"))

    def test_instr_7580(self):
        self.assertEqual(*self.doTest("add     dx, cx", "ADD(dx, cx)"))

    def test_instr_7590(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 12343h ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x12343)"))

    def test_instr_7600(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1234561Dh ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x1234561D)"))

    def test_instr_7610(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 14h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x14)"))

    def test_instr_7620(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 14h ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x14)"))

    def test_instr_7630(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 17h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x17)"))

    def test_instr_7640(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1Eh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1E)"))

    def test_instr_7650(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1FEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1FE)"))

    def test_instr_7660(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1FFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1FFE)"))

    def test_instr_7670(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1FFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1FFFE)"))

    def test_instr_7680(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1FFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1FFFFE)"))

    def test_instr_7690(self):
        self.assertEqual(*self.doTest("add     ebx, 4", "ADD(ebx, 4)"))

    def test_instr_7700(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1FFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1FFFFFE)"))

    def test_instr_7710(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 1FFFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x1FFFFFFE)"))

    def test_instr_7720(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 2 ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 2)"))

    def test_instr_7730(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 21AD3D34h ; s2", "MOV(*(dd*)(raddr(ss,esp)), 0x21AD3D34)"))

    def test_instr_7740(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3 ; op0", "MOV(*(dd*)(raddr(ss,esp)), 3)"))

    def test_instr_7750(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3 ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 3)"))

    def test_instr_7760(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3Eh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3E)"))

    def test_instr_7770(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3FEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3FE)"))

    def test_instr_7780(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3FFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3FFE)"))

    def test_instr_7790(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3FFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3FFFE)"))

    def test_instr_7800(self):
        self.assertEqual(*self.doTest("add     edx, ecx", "ADD(edx, ecx)"))

    def test_instr_7810(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3FFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3FFFFE)"))

    def test_instr_7820(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3FFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3FFFFFE)"))

    def test_instr_7830(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 3FFFFFFEh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x3FFFFFFE)"))

    def test_instr_7840(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 4 ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 4)"))

    def test_instr_7850(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 43210123h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x43210123)"))

    def test_instr_7860(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 7Eh ; op0h", "MOV(*(dd*)(raddr(ss,esp)), 0x7E)"))

    def test_instr_7870(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 7FFFFFFFh ; s0", "MOV(*(dd*)(raddr(ss,esp)), 0x7FFFFFFF)"))

    def test_instr_7880(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 80000000h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x80000000)"))

    def test_instr_7890(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 80000000h ; s0", "MOV(*(dd*)(raddr(ss,esp)), 0x80000000)"))

    def test_instr_7900(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 80008481h ; s2", "MOV(*(dd*)(raddr(ss,esp)), 0x80008481)"))

    def test_instr_7910(self):
        self.assertEqual(*self.doTest("add     esp, 10h", "ADD(esp, 0x10)"))

    def test_instr_7920(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 8000h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x8000)"))

    def test_instr_7930(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 80h ; op0", "MOV(*(dd*)(raddr(ss,esp)), 0x80)"))

    def test_instr_7940(self):
        self.assertEqual(*self.doTest("mov     dword ptr [esp], 813F3421h ; s2", "MOV(*(dd*)(raddr(ss,esp)), 0x813F3421)"))

    def test_instr_7950(self):
        self.assertEqual(*self.doTest('mov     dword ptr [esp], offset a10sA08lxB08lx ; "%-10s A=%08lx B=%08lx"', "MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10sa08lxb08lx))"))

    def test_instr_7960(self):
        self.assertEqual(*self.doTest('mov     dword ptr [esp], offset a10sAh08lxAl08l ; "%-10s AH=%08lx AL=%08lx B=%08lx RH=%08l"...', "MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10sah08lxal08l))"))

    def test_instr_7970(self):
        self.assertEqual(*self.doTest('mov     dword ptr [esp], offset a10sD ; "%-10s %d"', "MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10sd))"))

    def test_instr_7980(self):
        self.assertEqual(*self.doTest('mov     dword ptr [esp], offset a10sEax08lxA08l ; "%-10s EAX=%08lx A=%08lx C=%08lx CC=%02l"...', "MOV(*(dd*)(raddr(ss,esp)), offset(_rdata,a10seax08lxa08l))"))

    def test_instr_7990(self):
        self.assertEqual(*self.doTest("add     esp, 114h", "ADD(esp, 0x114)"))

    def test_instr_8000(self):
        self.assertEqual(*self.doTest("mov     eax, dword ptr [ebp+var_20]", "MOV(eax, *(dd*)(raddr(ss,ebp+var_20)))"))

    def test_instr_8010(self):
        self.assertEqual(*self.doTest("mov     eax, ebx", "eax = ebx;"))

    def test_instr_8050(self):
        self.assertEqual(*self.doTest("mov     eax, flags", "eax = flags;"))

    def test_instr_8060(self):
        self.assertEqual(*self.doTest("mov     eax, res", "eax = res;"))

    def test_instr_8070(self):
        self.assertEqual(*self.doTest("mov     eax, s0_0", "eax = s0_0;"))

    def test_instr_8080(self):
        self.assertEqual(*self.doTest("add     esp, 2", "ADD(esp, 2)"))

    def test_instr_8090(self):
        self.assertEqual(*self.doTest("mov     ebp, esp", "ebp = esp;"))

    def test_instr_8100(self):
        self.assertEqual(*self.doTest("mov     ebx, (offset str_buffer+800h)", "ebx = offset(_bss,str_buffer)+0x800;"))

    def test_instr_8110(self):
        self.assertEqual(*self.doTest("mov     ebx, 8234A6F8h", "ebx = 0x8234A6F8;"))

    def test_instr_8120(self):
        self.assertEqual(*self.doTest("mov     ebx, [ebp+iflags]", "MOV(ebx, *(dd*)(raddr(ss,ebp+iflags)))"))

    def test_instr_8130(self):
        self.assertEqual(*self.doTest("mov     ebx, [ebp+op0h]", "MOV(ebx, *(dd*)(raddr(ss,ebp+op0h)))"))

    def test_instr_8140(self):
        self.assertEqual(*self.doTest("add     esp, 20h", "ADD(esp, 0x20)"))

    def test_instr_8150(self):
        self.assertEqual(*self.doTest("mov     ebx, [ebp+s0]", "MOV(ebx, *(dd*)(raddr(ss,ebp+s0)))"))

    def test_instr_8160(self):
        self.assertEqual(*self.doTest("mov     ebx, [ebp+s2]", "MOV(ebx, *(dd*)(raddr(ss,ebp+s2)))"))

    def test_instr_8170(self):
        self.assertEqual(*self.doTest("mov     ebx, [ebp+var_4]", "MOV(ebx, *(dd*)(raddr(ss,ebp+var_4)))"))

    def test_instr_8180(self):
        self.assertEqual(*self.doTest("mov     ebx, dword ptr [ebp+var_20+4]", "MOV(ebx, *(dd*)(raddr(ss,ebp+var_20+4)))"))

    def test_instr_8190(self):
        self.assertEqual(*self.doTest("mov     ebx, edi", "ebx = edi;"))

    def test_instr_8200(self):
        self.assertEqual(*self.doTest("mov     ebx, i", "ebx = i;"))

    def test_instr_8210(self):
        self.assertEqual(*self.doTest("add     esp, 4Ch", "ADD(esp, 0x4C)"))

    def test_instr_8220(self):
        self.assertEqual(*self.doTest("mov     ecx, [ebp+ecx_0]", "MOV(ecx, *(dd*)(raddr(ss,ebp+ecx_0)))"))

    def test_instr_8230(self):
        self.assertEqual(*self.doTest("mov     ecx, [ebp+edx_0]", "MOV(ecx, *(dd*)(raddr(ss,ebp+edx_0)))"))

    def test_instr_8240(self):
        self.assertEqual(*self.doTest("mov     ecx, [ebp+i*4+ecx_vals]", "MOV(ecx, *(dd*)(raddr(ss,ebp+i*4+ecx_vals)))"))

    def test_instr_8250(self):
        self.assertEqual(*self.doTest("mov     ecx, [ebp+s0]", "MOV(ecx, *(dd*)(raddr(ss,ebp+s0)))"))

    def test_instr_8260(self):
        self.assertEqual(*self.doTest("mov     ecx, [ebp+s1]", "MOV(ecx, *(dd*)(raddr(ss,ebp+s1)))"))

    def test_instr_8270(self):
        self.assertEqual(*self.doTest("mov     ecx, [ebp+var_20]", "MOV(ecx, *(dd*)(raddr(ss,ebp+var_20)))"))

    def test_instr_8280(self):
        self.assertEqual(*self.doTest("mov     ecx, dword ptr [ebp+var_20+4]", "MOV(ecx, *(dd*)(raddr(ss,ebp+var_20+4)))"))

    def test_instr_8290(self):
        self.assertEqual(*self.doTest("mov     ecx, dword ptr [ebp+var_20]", "MOV(ecx, *(dd*)(raddr(ss,ebp+var_20)))"))

    def test_instr_8300(self):
        self.assertEqual(*self.doTest("add bl,30h          ; convert to ASCII", "ADD(bl, 0x30)"))

    def test_instr_8310(self):
        self.assertEqual(*self.doTest("mov     ecx, edi", "ecx = edi;"))

    def test_instr_8320(self):
        self.assertEqual(*self.doTest("mov     ecx, res", "ecx = res;"))

    def test_instr_8330(self):
        self.assertEqual(*self.doTest("mov     edi, (offset str_buffer+810h)", "edi = offset(_bss,str_buffer)+0x810;"))

    def test_instr_8340(self):
        self.assertEqual(*self.doTest('add bl,7            ; "A" to "F"', "ADD(bl, 7)"))

    def test_instr_8350(self):
        self.assertEqual(*self.doTest("mov     edi, [ebp+iflags]", "MOV(edi, *(dd*)(raddr(ss,ebp+iflags)))"))

    def test_instr_8360(self):
        self.assertEqual(*self.doTest("mov     edi, [ebp+op0]", "MOV(edi, *(dd*)(raddr(ss,ebp+op0)))"))

    def test_instr_8370(self):
        self.assertEqual(*self.doTest("mov     edi, [ebp+s1]", "MOV(edi, *(dd*)(raddr(ss,ebp+s1)))"))

    def test_instr_8380(self):
        self.assertEqual(*self.doTest("mov     edi, [ebp+s2]", "MOV(edi, *(dd*)(raddr(ss,ebp+s2)))"))

    def test_instr_8390(self):
        self.assertEqual(*self.doTest("mov     edi_0, (offset str_buffer+810h)", "edi_0 = offset(_bss,str_buffer)+0x810;"))

    def test_instr_8400(self):
        self.assertEqual(*self.doTest("add edi,14*320", "ADD(edi, 14*320)"))

    def test_instr_8410(self):
        self.assertEqual(*self.doTest("mov     edx, [ebp+s1]", "MOV(edx, *(dd*)(raddr(ss,ebp+s1)))"))

    def test_instr_8420(self):
        self.assertEqual(*self.doTest("mov     edx, [ebp+var_1C]", "MOV(edx, *(dd*)(raddr(ss,ebp+var_1c)))"))

    def test_instr_8430(self):
        self.assertEqual(*self.doTest("mov     edx, dword ptr [ebp+var_20]", "MOV(edx, *(dd*)(raddr(ss,ebp+var_20)))"))

    def test_instr_8440(self):
        self.assertEqual(*self.doTest("mov     edx, ebx", "edx = ebx;"))

    def test_instr_8450(self):
        self.assertEqual(*self.doTest("mov     edx, edi", "edx = edi;"))

    def test_instr_8460(self):
        self.assertEqual(*self.doTest("add word ptr [singlequad+2],50", "ADD(*(dw*)(((db*)&singlequad)+2), 50)"))

    def test_instr_8470(self):
        self.assertEqual(*self.doTest("mov     edx, esi", "edx = esi;"))

    def test_instr_8480(self):
        self.assertEqual(*self.doTest("mov     edx, res", "edx = res;"))

    def test_instr_8490(self):
        self.assertEqual(*self.doTest("mov     edx, resh", "edx = resh;"))

    def test_instr_8500(self):
        self.assertEqual(*self.doTest("mov     esi, 12340306h", "esi = 0x12340306;"))

    def test_instr_8510(self):
        self.assertEqual(*self.doTest("mov     esi, [ebp+iflags]", "MOV(esi, *(dd*)(raddr(ss,ebp+iflags)))"))

    def test_instr_8520(self):
        self.assertEqual(*self.doTest("mov     esi, [ebp+op0]", "MOV(esi, *(dd*)(raddr(ss,ebp+op0)))"))

    def test_instr_8530(self):
        self.assertEqual(*self.doTest("and     ah, 0F7h", "AND(ah, 0x0F7)"))

    def test_instr_8540(self):
        self.assertEqual(*self.doTest("mov     esi, [ebp+op0h]", "MOV(esi, *(dd*)(raddr(ss,ebp+op0h)))"))

    def test_instr_8550(self):
        self.assertEqual(*self.doTest("mov     esi, [ebp+s0]", "MOV(esi, *(dd*)(raddr(ss,ebp+s0)))"))

    def test_instr_8560(self):
        self.assertEqual(*self.doTest("mov     esi, [ebp+s1]", "MOV(esi, *(dd*)(raddr(ss,ebp+s1)))"))

    def test_instr_8570(self):
        self.assertEqual(*self.doTest("mov     esi, esi_0", "esi = esi_0;"))

    def test_instr_8580(self):
        self.assertEqual(*self.doTest("mov     esi, offset unk_40E008", "esi = offset(_data,unk_40e008);"))

    def test_instr_8590(self):
        self.assertEqual(*self.doTest("mov     esi_0, ebx", "esi_0 = ebx;"))

    def test_instr_8600(self):
        self.assertEqual(*self.doTest("mov     i, 12345678h", "i = 0x12345678;"))

    def test_instr_8610(self):
        self.assertEqual(*self.doTest("mov     i, esi", "i = esi;"))

    def test_instr_8620(self):
        self.assertEqual(*self.doTest("mov     op0, 32432434h", "op0 = 0x32432434;"))

    def test_instr_8630(self):
        self.assertEqual(*self.doTest("and     dl, cl", "AND(dl, cl)"))

    def test_instr_8640(self):
        self.assertEqual(*self.doTest("mov   esi,offset pal_jeu", "esi = offset(_data,pal_jeu);"))

    def test_instr_8650(self):
        self.assertEqual(*self.doTest("mov  bx,ax", "bx = ax;"))

    def test_instr_8660(self):
        self.assertEqual(*self.doTest("mov  fs,ax", "fs = ax;"))

    def test_instr_8670(self):
        self.assertEqual(*self.doTest("mov [a],5", "*(a) = 5;"))

    def test_instr_8680(self):
        self.assertEqual(*self.doTest("mov [load_handle],eax", "load_handle = eax;"))

    def test_instr_8690(self):
        self.assertEqual(*self.doTest("and     dx, cx", "AND(dx, cx)"))

    def test_instr_8700(self):
        self.assertEqual(*self.doTest("mov al,-5", "al = -5;"))

    def test_instr_8710(self):
        self.assertEqual(*self.doTest("mov al,00h", "al = 0x00;"))

    def test_instr_8720(self):
        self.assertEqual(*self.doTest("mov al,[a]", "al = *(a);"))

    def test_instr_8730(self):
        self.assertEqual(*self.doTest("mov ax,-1", "ax = -1;"))

    def test_instr_8740(self):
        self.assertEqual(*self.doTest("and     ecx, 40h", "AND(ecx, 0x40)"))

    def test_instr_8750(self):
        self.assertEqual(*self.doTest("mov ax,0002h", "ax = 0x0002;"))

    def test_instr_8760(self):
        self.assertEqual(*self.doTest("mov ax,0007", "ax = 0007;"))

    def test_instr_8770(self):
        self.assertEqual(*self.doTest("mov ax,01010101010101010b", "ax = 0xaaaa;"))

    def test_instr_8780(self):
        self.assertEqual(*self.doTest("mov ax,501h", "ax = 0x501;"))

    def test_instr_8790(self):
        self.assertEqual(*self.doTest("and     edx, ecx", "AND(edx, ecx)"))

    def test_instr_8810(self):
        self.assertEqual(*self.doTest("mov bl,-1", "bl = -1;"))

    def test_instr_8820(self):  # a is an array of bytes
        self.assertEqual(*self.doTest("mov bl,[a+1]", "bl = *((a)+1);"))

    def test_instr_8830(self):
        self.assertEqual(*self.doTest("mov bl,al", "bl = al;"))

    def test_instr_8840(self):
        self.assertEqual(*self.doTest("mov bx,(1024*10/16)+5", "bx = (1024*10/16)+5;"))

    def test_instr_8850(self):
        self.assertEqual(*self.doTest("mov bx,(1024*10/16)-1", "bx = (1024*10/16)-1;"))

    def test_instr_8860(self):
        self.assertEqual(*self.doTest("and     eflags, 40h", "AND(eflags, 0x40)"))

    def test_instr_8870(self):
        self.assertEqual(*self.doTest("mov bx,1024*10/16", "bx = 1024*10/16;"))

    def test_instr_8880(self):
        self.assertEqual(*self.doTest("mov bx,ax", "bx = ax;"))

    def test_instr_8890(self):
        self.assertEqual(*self.doTest("mov bx,fs", "bx = fs;"))

    def test_instr_8900(self):
        self.assertEqual(*self.doTest("mov bx,word ptr [d]", "bx = *(dw*)(&d);"))

    def test_instr_8910(self):
        self.assertEqual(*self.doTest("mov bx,word ptr [e]", "bx = *(dw*)(&e);"))

    def test_instr_8920(self):
        self.assertEqual(*self.doTest("mov byte ptr [a],5", "*(a) = 5;"))

    def test_instr_8930(self):
        self.assertEqual(*self.doTest("mov byte ptr [esi],-2", "MOV(*(raddr(ds,esi)), -2)"))

    def test_instr_8940(self):
        self.assertEqual(*self.doTest("mov byte ptr [singlebyte2+1],5", "*((&singlebyte2)+1) = 5;"))

    def test_instr_8950(self):
        self.assertEqual(*self.doTest("and     eflags, 8D5h", "AND(eflags, 0x8D5)"))

    def test_instr_8960(self):
        self.assertEqual(*self.doTest("mov dl,byte ptr [edi]", "MOV(dl, *(raddr(ds,edi)))"))

    def test_instr_8970(self):
        self.assertEqual(*self.doTest("mov byte ptr ds:[0],55", "MOV(*(raddr(ds,0)), 55)"))

    def test_instr_8980(self):
        self.assertEqual(*self.doTest("mov byte ptr es:[0],55", "MOV(*(raddr(es,0)), 55)"))

    def test_instr_8990(self):
        self.assertEqual(*self.doTest("mov byte ptr es:[0],56", "MOV(*(raddr(es,0)), 56)"))

    def test_instr_9000(self):
        self.assertEqual(*self.doTest("and     esp, 0FFFFFFF0h", "AND(esp, 0x0FFFFFFF0)"))

    def test_instr_9010(self):
        self.assertEqual(*self.doTest("mov cx,256*3", "cx = 256*3;"))

    def test_instr_9020(self):
        self.assertEqual(*self.doTest("mov cx,ax", "cx = ax;"))

    def test_instr_9030(self):
        self.assertEqual(*self.doTest("mov dl,[edi+1]", "MOV(dl, *(raddr(ds,edi+1)))"))

    def test_instr_9040(self):
        self.assertEqual(*self.doTest("mov dl,[edi]", "MOV(dl, *(raddr(ds,edi)))"))

    def test_instr_9050(self):
        self.assertEqual(*self.doTest("mov ds, _data", "ds = seg_offset(_data);"))

    def test_instr_9060(self):
        self.assertEqual(*self.doTest("mov ds:[edi],cl", "MOV(*(raddr(ds,edi)), cl)"))

    def test_instr_9070(self):
        self.assertEqual(*self.doTest("mov dword ptr es:[0],077aaFF00h", "MOV(*(dd*)(raddr(es,0)), 0x077aaFF00)"))

    def test_instr_9080(self):
        self.assertEqual(*self.doTest("mov dword ptr es:[20*320+160],077aaFF00h", "MOV(*(dd*)(raddr(es,20*320+160)), 0x077aaFF00)"))

    def test_instr_9090(self):
        self.assertEqual(*self.doTest("and     flags, 0D5h", "AND(flags, 0x0D5)"))

    def test_instr_9100(self):
        self.assertEqual(*self.doTest("mov dx,[edi+1]", "MOV(dx, *(dw*)(raddr(ds,edi+1)))"))

    def test_instr_9110(self):
        self.assertEqual(*self.doTest("mov dx,cx", "dx = cx;"))

    def test_instr_9120(self):
        self.assertEqual(*self.doTest("mov eax, B", "eax = b;"))

    def test_instr_9130(self):
        self.assertEqual(*self.doTest("mov eax, CC", "eax = cc;"))

    def test_instr_9140(self):
        self.assertEqual(*self.doTest("mov eax,-1-(-2+3)", "eax = -1-(-2+3);"))

    def test_instr_9150(self):
        self.assertEqual(*self.doTest("and     flags, 1", "AND(flags, 1)"))

    def test_instr_9160(self):
        self.assertEqual(*self.doTest("mov eax,0100b", "eax = 0x4;"))

    def test_instr_9170(self):
        self.assertEqual(*self.doTest("mov eax,011111111111111111111111111111111b", "eax = 0xffffffff;"))

    def test_instr_9180(self):
        self.assertEqual(*self.doTest("and     flags, 11h", "AND(flags, 0x11)"))

    def test_instr_9190(self):
        self.assertEqual(*self.doTest("mov eax,1024*1024", "eax = 1024*1024;"))

    def test_instr_9200(self):
        self.assertEqual(*self.doTest("mov eax,10B", "eax = 0x2;"))

    def test_instr_9210(self):
        self.assertEqual(*self.doTest("mov eax,256+3+65536", "eax = 256+3+65536;"))

    def test_instr_9220(self):
        self.assertEqual(*self.doTest("mov eax,taille_moire  ;::!300000h-1 ;182400h-1 ;1582080 ;0300000h-1 ;2mega 182400h-1", "eax = taille_moire;"))

    def test_instr_9230(self):
        self.assertEqual(*self.doTest("mov eax,teST2", "eax = test2;"))

    def test_instr_9240(self):
        self.assertEqual(*self.doTest("and     flags, 801h", "AND(flags, 0x801)"))

    def test_instr_9250(self):
        self.assertEqual(*self.doTest("mov ebp,3*4", "ebp = 3*4;"))

    def test_instr_9260(self):
        self.assertEqual(*self.doTest("mov ebx,01B", "ebx = 0x1;"))

    def test_instr_9270(self):
        self.assertEqual(*self.doTest("and     flags, 8C5h", "AND(flags, 0x8C5)"))

    def test_instr_9280(self):
        self.assertEqual(*self.doTest("and     flags, 8D5h", "AND(flags, 0x8D5)"))

    def test_instr_9290(self):
        self.assertEqual(*self.doTest("mov ebx,[g]", "ebx = g;"))

    def test_instr_9300(self):
        self.assertEqual(*self.doTest("mov ebx,[load_handle]", "ebx = load_handle;"))

    def test_instr_9310(self):
        self.assertEqual(*self.doTest("mov ebx,eax", "ebx = eax;"))

    def test_instr_9320(self):
        self.assertEqual(*self.doTest("and bl,0Fh          ; only low-Nibble", "AND(bl, 0x0F)"))

    def test_instr_9330(self):
        self.assertEqual(*self.doTest("mov ecx,320*200/4", "ecx = 320*200/4;"))

    def test_instr_9340(self):
        self.assertEqual(*self.doTest("mov ecx,t", "ecx = t;"))

    def test_instr_9350(self):
        self.assertEqual(*self.doTest("mov edi,OFFSET AsCii ; get the offset address", "edi = offset(_data,ascii);"))

    def test_instr_9360(self):
        self.assertEqual(*self.doTest("mov edi,esi", "edi = esi;"))

    def test_instr_9370(self):
        self.assertEqual(*self.doTest("bsf     ax, bx", "BSF(ax, bx)"))

    def test_instr_9380(self):
        self.assertEqual(*self.doTest("mov edi,offset str2", "edi = offset(_data,str2);"))

    def test_instr_9390(self):
        self.assertEqual(*self.doTest("mov edi,offset str3", "edi = offset(_data,str3);"))

    def test_instr_9400(self):
        self.assertEqual(*self.doTest("mov edi,offset singlebyte2", "edi = offset(_data,singlebyte2);"))

    def test_instr_9410(self):
        self.assertEqual(*self.doTest("mov edi,offset wordarray", "edi = offset(_data,wordarray);"))

    def test_instr_9420(self):
        self.assertEqual(*self.doTest("mov edi,offset bytearray", "edi = offset(_data,bytearray);"))

    def test_instr_9430(self):
        self.assertEqual(*self.doTest("mov edx,OFFSET ASCiI ; DOS 1+ WRITE STRING TO STANDARD OUTPUT", "edx = offset(_data,ascii);"))

    def test_instr_9440(self):
        self.assertEqual(*self.doTest("bsf     ax, di", "BSF(ax, di)"))

    def test_instr_9450(self):
        self.assertEqual(*self.doTest("mov edx,edi", "edx = edi;"))

    def test_instr_9460(self):
        self.assertEqual(*self.doTest("mov edx,offset _msg             ; DS:EDX -> $ Terminated String", "edx = offset(_data,_msg);"))

    def test_instr_9470(self):
        self.assertEqual(*self.doTest("mov es,ax", "es = ax;"))

    def test_instr_9480(self):
        self.assertEqual(*self.doTest("mov esi,offset str1", "esi = offset(_data,str1);"))

    def test_instr_9490(self):
        self.assertEqual(*self.doTest("mov esi,offset testOVerlap", "esi = offset(_data,testoverlap);"))

    def test_instr_9500(self):
        self.assertEqual(*self.doTest("mov esi,offset singlebyte2", "esi = offset(_data,singlebyte2);"))

    def test_instr_9510(self):
        self.assertEqual(*self.doTest("mov esi,offset wordarray", "esi = offset(_data,wordarray);"))

    def test_instr_9520(self):
        self.assertEqual(*self.doTest("mov esi,offset singlebyte", "esi = offset(_data,singlebyte);"))

    def test_instr_9530(self):
        self.assertEqual(*self.doTest("bsf     ax, si", "BSF(ax, si)"))

    def test_instr_9540(self):
        self.assertEqual(*self.doTest("movsb", "MOVSB"))

    def test_instr_9550(self):
        self.assertEqual(*self.doTest("movsd", "MOVSD"))

    def test_instr_9560(self):
        self.assertEqual(*self.doTest("movsw", "MOVSW"))

    def test_instr_9570(self):
        self.assertEqual(*self.doTest("movsx bx,[h2]", "MOVSX(bx, h2)"))

    def test_instr_9580(self):
        self.assertEqual(*self.doTest("movsx bx,bl", "MOVSX(bx, bl)"))

    def test_instr_9590(self):
        self.assertEqual(*self.doTest("movsx bx,byte ptr [h2]", "MOVSX(bx, h2)"))

    def test_instr_9600(self):
        self.assertEqual(*self.doTest("movsx bx,byte ptr [h]", "MOVSX(bx, h)"))

    def test_instr_9620(self):
        self.assertEqual(*self.doTest("movzx eax, DDD", "MOVZX(eax, ddd)"))


    def test_instr_9840(self):
        self.assertEqual(*self.doTest("or      res, 0FFFFFFFFh", "OR(res, 0x0FFFFFFFF)"))

    def test_instr_9850(self):
        self.assertEqual(*self.doTest("or cl,0f0h", "OR(cl, 0x0f0)"))

    def test_instr_9860(self):
        self.assertEqual(*self.doTest("bsr     ax, bx", "BSR(ax, bx)"))

    def test_instr_9870(self):
        self.assertEqual(*self.doTest("or cx,cx", "OR(cx, cx)"))

    def test_instr_9880(self):
        self.assertEqual(*self.doTest("or eax,eax", "OR(eax, eax)"))

    def test_instr_9890(self):
        self.assertEqual(*self.doTest("out   dx,al", "OUT(dx, al)"))

    def test_instr_9900(self):
        self.assertEqual(*self.doTest("rcl     dl, cl", "RCL(dl, cl)"))

    def test_instr_9910(self):
        self.assertEqual(*self.doTest("rcl     dx, cl", "RCL(dx, cl)"))

    def test_instr_9920(self):
        self.assertEqual(*self.doTest("rcl     edx, cl", "RCL(edx, cl)"))

    def test_instr_9930(self):
        self.assertEqual(*self.doTest("rcr     dl, cl", "RCR(dl, cl)"))

    def test_instr_9940(self):
        self.assertEqual(*self.doTest("rcr     dx, cl", "RCR(dx, cl)"))

    def test_instr_9950(self):
        self.assertEqual(*self.doTest("rcr     edx, cl", "RCR(edx, cl)"))

    def test_instr_9960(self):
        self.assertEqual(*self.doTest("bsr     ax, di", "BSR(ax, di)"))

    def test_instr_9970(self):
        self.assertEqual(*self.doTest("ret", "RETN(0)"))

    def test_instr_9980(self):
        self.assertEqual(*self.doTest("rol     dl, cl", "ROL(dl, cl)"))

    def test_instr_9990(self):
        self.assertEqual(*self.doTest("rol     dx, cl", "ROL(dx, cl)"))

    def test_instr_10000(self):
        self.assertEqual(*self.doTest("rol     edx, cl", "ROL(edx, cl)"))

    def test_instr_10010(self):
        self.assertEqual(*self.doTest("rol ebx,1", "ROL(ebx, 1)"))

    def test_instr_10020(self):
        self.assertEqual(*self.doTest("rol ebx,31", "ROL(ebx, 31)"))

    def test_instr_10030(self):
        self.assertEqual(*self.doTest("ror     dl, cl", "ROR(dl, cl)"))

    def test_instr_10040(self):
        self.assertEqual(*self.doTest("ror     dx, cl", "ROR(dx, cl)"))

    def test_instr_10050(self):
        self.assertEqual(*self.doTest("ror     edx, cl", "ROR(edx, cl)"))

    def test_instr_10060(self):
        self.assertEqual(*self.doTest("sar     dl, cl", "SAR(dl, cl)"))

    def test_instr_10070(self):
        self.assertEqual(*self.doTest("bsr     eax, ebx", "BSR(eax, ebx)"))

    def test_instr_10080(self):
        self.assertEqual(*self.doTest("sal     dl, cl", "SAL(dl, cl)"))

    def test_instr_10090(self):
        self.assertEqual(*self.doTest("sar     dx, cl", "SAR(dx, cl)"))

    def test_instr_10100(self):
        self.assertEqual(*self.doTest("sar     edx, cl", "SAR(edx, cl)"))

    def test_instr_10110(self):
        self.assertEqual(*self.doTest("sar eax,1", "SAR(eax, 1)"))

    def test_instr_10120(self):
        self.assertEqual(*self.doTest("sar eax,2", "SAR(eax, 2)"))

    def test_instr_10130(self):
        self.assertEqual(*self.doTest("sbb     dl, cl", "SBB(dl, cl)"))

    def test_instr_10140(self):
        self.assertEqual(*self.doTest("sbb     dx, cx", "SBB(dx, cx)"))

    def test_instr_10150(self):
        self.assertEqual(*self.doTest("sbb     edx, ecx", "SBB(edx, ecx)"))

    def test_instr_10155(self):
        self.assertEqual(*self.doTest("mul     test_bcd_ofs", "MUL1_2(test_bcd_ofs)"))

    def test_instr_10157(self):
        self.assertEqual(*self.doTest("mov     bx, test_bcd_ofs+1", "bx = *(dw*)(((db*)&test_bcd_ofs)+1);"))

    def test_instr_10160(self):
        self.assertEqual(*self.doTest("scasb", "SCASB"))

    def test_instr_10170(self):
        self.assertEqual(*self.doTest("scasd", "SCASD"))

    def test_instr_10180(self):
        self.assertEqual(*self.doTest("mov[bp + asgn_aptr_in_struc.ts_rotv_membr_strinst.vxdw], 3", "MOV(((transshapestruc*)raddr(ss,bp+asgn_aptr_in_struc))->ts_rotv_membr_strinst.vxdw, 3)"))

    @unittest.skip("it works but test broken. non masm")
    def test_instr_11330(self):
        print(*self.doTest("rep",  "\tREP\n"))

    @unittest.skip("it works but test broken. non masm")
    def test_instr_11340(self):
        print(*self.doTest("repe",  "\tREPE\n"))

    @unittest.skip("undefined behaviour")
    def test_instr_11350(self):
        print(*self.doTest("mov     [ebp+i+wordtable], dl","MOV(*(dw*)(raddr(ss,ebp+i+offset(_text,wordtable),  dl)"))

    @unittest.skip("Minor syntax")
    def test_instr_11850(self):
        print(*self.doTest(r"mov	bl, byte ptr es:[wordtable]", "MOV(bl, *((db*)&wordtable))"))

    @unittest.skip("Minor syntax")
    def test_instr_11860(self):
        print(*self.doTest(r"mov	ch, es:[singlebyte]", "MOV(ch, singlebyte)"))

    @unittest.skip("Minor syntax")
    def test_instr_11870(self):
        print(*self.doTest(r"mov	eax, es:[g]", "MOV(eax, g)"))


    def test_instr_10890(self):
        self.assertEqual(*self.doTest("retn 6", "RETN(6)"))

    def test_instr_10900(self):
        self.assertEqual(*self.doTest("cmp wordarray+3*4,4000000", "CMP(*(dw*)(((db*)wordarray)+3*4), 4000000)"))

    @unittest.skip("Probably wrong")
    def test_instr_2300(self):
        self.assertEqual(*self.doTest("cmp [singlebyte+ebp],4000000", "CMP(*(raddr(ss,offset(_data,singlebyte)+ebp)), 4000000)"))

    @unittest.skip("Probably wrong")
    def test_instr_3330(self):
        self.assertEqual(*self.doTest("cmp singlebyte+3*4,4000000", "CMP(*((&singlebyte)+3*4), 4000000)"))

    @unittest.skip("Probably wrong")
    def test_instr_3340(self):
        self.assertEqual(*self.doTest("cmp singlebyte+ebp,4000000", "CMP(*(raddr(ss,offset(_data,singlebyte)+ebp)), 4000000)"))

    @unittest.skip("Don't know how to test properly yet")
    def test_instr_11880(self):
        assert self.proc.generate_full_cmd_line(self.cpp, self.parser.action_data("var_104_rc equ TRANSSHAPESTRUC ptr -260")) == "#define var_104_rc -260\n"

    def test_instr_10905(self):
        self.assertEqual(*self.doTest("call    near ptr loc_40458f", "CALL(mainproc,m2c::kloc_40458f)"))

    def test_instr_10910(self):
        self.assertEqual(*self.doTest("call    far ptr loc_40458f+1", "CALLF(mainproc,m2c::kloc_40458f)"))

    def test_instr_10920(self):
        self.assertEqual(*self.doTest("push    [bp+arg_2]", "PUSH(*(dw*)(raddr(ss,bp+arg_2)))"))

    def test_instr_10930(self):
        self.assertEqual(*self.doTest("les     di, [bp+arg_4]", "LES(di, *(dd*)(raddr(ss,bp+arg_4)))"))

    def test_instr_10940(self):
        self.cpp._context.itislst = True
        assert self.proc.generate_full_cmd_line(self.cpp, self.parser.action_code("mov ss,ax")) == "\tS(ss = ax;);"
        self.cpp._context.itislst = False

    def test_instr_10950(self):
        self.assertEqual(*self.doTest("jmp far ptr 0:0", "LES(di, *(dd*)(raddr(ss,bp+arg_4)))"))

    def test_instr_10960(self):
        self.assertEqual(*self.doTest("call far ptr 0:0", "LES(di, *(dd*)(raddr(ss,bp+arg_4)))"))

    def test_instr_10970(self):
        self.assertEqual(*self.doTest("imul    word_0", "IMUL1_2(word_0)"))

    #def test_instr_12030(self):
    #    print(*self.doTest("cmp h_array, 'v'",  u"CMP(*(h_array), 'v')"))
if __name__ == "__main__":
    unittest.main()
