from __future__ import absolute_import
from __future__ import print_function

from masm2c import cpp, op
import logging
from mock import patch
from masm2c.parser import Parser
from masm2c.proc import Proc
import unittest

from random import randint


# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


class ParserTest(unittest.TestCase):

    def test_instructions_list(self):
        masm_instr_list = ['aaa', 'aad', 'aam', 'aas', 'adc', 'add', 'and', 'call', 'cbw', 'clc', 'cld', 'cli', 'cmc', 'cmp', 'cmps', 'cmpsb', 'cmpsw', 'cmpxchg8b ', 'cwd', 'daa', 'das', 'dec', 'div', 'esc', 'hlt', 'idiv', 'imul', 'in', 'inc', 'int', 'into', 'iret', 'ja', 'jae', 'jb', 'jbe', 'jc', 'jcxz', 'je', 'jg', 'jge', 'jl', 'jle', 'jmp', 'jna', 'jnae', 'jnb', 'jnbe', 'jnc', 'jne', 'jng', 'jnge', 'jnl', 'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp', 'jpe', 'jpo', 'js', 'jz', 'lahf', 'lds', 'lea', 'les', 'lods', 'lodsb', 'lodsw', 'loop', 'loope', 'loopew', 'loopne', 'loopnew', 'loopnz', 'loopnzw', 'loopw', 'loopz', 'loopzw', 'mov', 'movs', 'movsb', 'movsw', 'mul', 'neg', 'nop', 'not', 'or', 'out', 'pop', 'popf', 'push', 'pushf', 'rcl', 'rcr', 'ret', 'retf', 'retn', 'rol', 'ror', 'sahf', 'sal', 'sar', 'sbb', 'scas', 'scasb', 'scasw', 'shl', 'shr', 'stc', 'std', 'sti', 'stos', 'stosb', 'stosw', 'sub', 'test', 'wait', 'xchg', 'xlat', 'xlatb', 'xor', 'bound', 'enter', 'ins', 'insb', 'insw', 'leave', 'outs', 'outsb', 'outsw', 'popa', 'pusha', 'pushw', 'arpl', 'lar', 'lsl', 'sgdt', 'sidt', 'sldt', 'smsw', 'str', 'verr', 'verw', 'clts', 'lgdt', 'lidt', 'lldt', 'lmsw', 'ltr', 'bsf', 'bsr', 'bt', 'btc', 'btr', 'bts', 'cdq', 'cmpsd', 'cwde', 'insd', 'iretd', 'iretdf', 'iretf', 'jecxz', 'lfs', 'lgs', 'lodsd', 'loopd', 'looped', 'loopned', 'loopnzd', 'loopzd', 'lss', 'movsd', 'movsx', 'movzx', 'outsd', 'popad', 'popfd', 'pushad', 'pushd', 'pushfd', 'scasd', 'seta', 'setae', 'setb', 'setbe', 'setc', 'sete', 'setg', 'setge', 'setl', 'setle', 'setna', 'setnae', 'setnb', 'setnbe', 'setnc', 'setne', 'setng', 'setnge', 'setnl', 'setnle', 'setno', 'setnp', 'setns', 'setnz', 'seto', 'setp', 'setpe', 'setpo', 'sets', 'setz', 'shld', 'shrd', 'stosd', 'bswap', 'cmpxchg', 'invd', 'invlpg', 'wbinvd', 'xadd']
        proc_instance = Proc('someproc')
        [proc_instance.find_op_common_class(i, []) for i in masm_instr_list]

    @patch.object(logging, 'debug')
    @patch.object(logging, 'info')
    # @patch.object(parser, 'get_global')
    def test_convert_data(self, mock_info, mock_debug):

        mock_info.return_value = None
        mock_debug.return_value = None
        parser_instance = Parser([])

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=256, v=u'2*2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=256, v=u'3)')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=256, v=u'5*5 dup (0')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=256, v=u'testEqu*2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=4294967296, v=u'test2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=65536, v=u'2*2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=65536, v=u'3)')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=65536, v=u'5*5 dup (0')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=65536, v=u'test2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(base=65536, v=u'testEqu*2')

        # self.assertEqual(parser_instance.convert_data(base=4294967296,v=u'var5'),u'offset(_data,var5)')

    @patch.object(logging, 'debug')
    def test_fix_dollar(self, mock_debug):
        mock_debug.return_value = None
        parser_instance = Parser([])
        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='3'), '3')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='1'), '1')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='-13'), '-13')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='13'), '13')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='4'), '4')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='var1'), 'var1')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='1'), '1')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='2'), '2')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='(00+38*3)*320+1/2+33*(3-1)'), '(00+38*3)*320+1/2+33*(3-1)')

        self.assertEqual(parser_instance.replace_dollar_w_segoffst(v='1500 ; 8*2*3 ;+1 +19*13*2*4'), '1500 ; 8*2*3 ;+1 +19*13*2*4')

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

        self.assertEqual(parser_instance.parse_int(v=u'14*320'), 4480)
        self.assertEqual(parser_instance.parse_int(v=u'2*2'), 4)
        self.assertEqual(parser_instance.parse_int(v=u'3*4'), 12)
        self.assertEqual(parser_instance.parse_int(v=u'-1-(-2+3)'), -2)
        self.assertEqual(parser_instance.parse_int(v=u'-1'), -1)
        self.assertEqual(parser_instance.parse_int(v=u'-11'), -11)
        self.assertEqual(parser_instance.parse_int(v=u'-2'), -2)
        self.assertEqual(parser_instance.parse_int(v=u'0'), 0)
        self.assertEqual(parser_instance.parse_int(v=u'00h'), 0)
        self.assertEqual(parser_instance.parse_int(v=u'03dh'), 61)
        self.assertEqual(parser_instance.parse_int(v=u'03eh'), 62)
        self.assertEqual(parser_instance.parse_int(v=u'03fh'), 63)
        self.assertEqual(parser_instance.parse_int(v=u'042h'), 66)
        self.assertEqual(parser_instance.parse_int(v=u'0Ah'), 10)
        self.assertEqual(parser_instance.parse_int(v=u'0Dh'), 13)
        self.assertEqual(parser_instance.parse_int(v=u'0Fh'), 15)
        self.assertEqual(parser_instance.parse_int(v=u'0ffffff00h'), 4294967040)
        self.assertEqual(parser_instance.parse_int(v=u'1'), 1)
        self.assertEqual(parser_instance.parse_int(v=u'10'), 10)
        self.assertEqual(parser_instance.parse_int(v=u'100'), 100)
        self.assertEqual(parser_instance.parse_int(v=u'1000h'), 4096)
        self.assertEqual(parser_instance.parse_int(v=u'11'), 11)
        self.assertEqual(parser_instance.parse_int(v=u'111'), 111)
        self.assertEqual(parser_instance.parse_int(v=u'12'), 12)
        self.assertEqual(parser_instance.parse_int(v=u'13'), 13)
        self.assertEqual(parser_instance.parse_int(v=u'131'), 131)
        self.assertEqual(parser_instance.parse_int(v=u'16'), 16)
        self.assertEqual(parser_instance.parse_int(v=u'2'), 2)
        self.assertEqual(parser_instance.parse_int(v=u'21h'), 33)
        self.assertEqual(parser_instance.parse_int(v=u'22'), 22)
        self.assertEqual(parser_instance.parse_int(v=u'223'), 223)
        self.assertEqual(parser_instance.parse_int(v=u'25'), 25)
        self.assertEqual(parser_instance.parse_int(v=u'3'), 3)
        self.assertEqual(parser_instance.parse_int(v=u'30h'), 48)
        self.assertEqual(parser_instance.parse_int(v=u'34'), 34)
        self.assertEqual(parser_instance.parse_int(v=u'35'), 35)
        self.assertEqual(parser_instance.parse_int(v=u'37'), 37)
        self.assertEqual(parser_instance.parse_int(v=u'39h'), 57)
        self.assertEqual(parser_instance.parse_int(v=u'4'), 4)
        self.assertEqual(parser_instance.parse_int(v=u'4000000'), 4000000)
        self.assertEqual(parser_instance.parse_int(v=u'4ch'), 76)
        self.assertEqual(parser_instance.parse_int(v=u'5'), 5)
        self.assertEqual(parser_instance.parse_int(v=u'50'), 50)
        self.assertEqual(parser_instance.parse_int(v=u'6'), 6)
        self.assertEqual(parser_instance.parse_int(v=u'64000'), 64000)
        self.assertEqual(parser_instance.parse_int(v=u'7'), 7)
        self.assertEqual(parser_instance.parse_int(v=u'0h'), 0)
        self.assertEqual(parser_instance.parse_int(v=u'0b'), 0)

    def test_calculate_data_size(self):

        self.assertEqual(Parser.typetosize('db'), 1)
        self.assertEqual(Parser.typetosize('dd'), 4)
        self.assertEqual(Parser.typetosize('dq'), 8)
        self.assertEqual(Parser.typetosize('dw'), 2)
        self.assertEqual(Parser.typetosize('dt'), 10)

    @patch.object(logging, 'debug')
    @patch.object(logging, 'info')
    # @patch.object(parser, 'get_global')
    def test_equ(self, mock_info, mock_debug):

        mock_info.return_value = None
        mock_debug.return_value = None
        parser_instance = Parser([])

        cpp_instance = cpp.Cpp(parser_instance)
        proc_instance = Proc('mainproc', False)
        cpp_instance.proc = proc_instance
        parser_instance.set_global("_data", op.var(1, 0, issegment=True))
        parser_instance.set_global("var1", op.var(size=1, offset=1, name="var1", segment="_data", elements=1))
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'aaaa = 1')), '#undef aaaa\n#define aaaa 1\n')

        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'B = 1')), '#undef B\n#define B 1\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'DDD = var1 ; actually it is address of var1')), '#undef DDD\n#define DDD m.var1\n')

        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'left equ 0')), '#define left 0\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'col equ 40')), '#define col 40\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'right equ left+col')), '#define right left+col\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'scale_mod equ -19*32*4; ')), '#define scale_mod -19*32*4\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'tempo equ 1193182/256/targetFPS')), '#define tempo 1193182/256/targetFPS\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'sierp_color equ 2Ah')), '#define sierp_color 0x2A\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'tilt_plate_pattern equ 4+8+16')), '#define tilt_plate_pattern 4+8+16\n')

        # wrong
        # TODO
        # self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'l equ byte ptr aaa')), '#define l byte aaa\n')
        self.assertEqual(proc_instance.generate_c_cmd(cpp_instance, parser_instance.action_data(u'res = edx ; int')), '#undef res\n#define res edx\n')


if __name__ == "__main__":
    unittest.main()
