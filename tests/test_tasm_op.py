
import logging
import unittest
from random import randint
from unittest.mock import patch

from masm2c import cpp, op
from masm2c.parser import Parser
from masm2c.proc import Proc

# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


class ParserTest(unittest.TestCase):

    def test_instructions_list(self):
        masm_instr_list = ['aaa', 'aad', 'aam', 'aas', 'adc', 'add', 'and', 'call', 'cbw', 'clc', 'cld', 'cli', 'cmc', 'cmp', 'cmps', 'cmpsb', 'cmpsw', 'cmpxchg8b ', 'cwd', 'daa', 'das', 'dec', 'div', 'esc', 'hlt', 'idiv', 'imul', 'in', 'inc', 'int', 'into', 'iret', 'ja', 'jae', 'jb', 'jbe', 'jc', 'jcxz', 'je', 'jg', 'jge', 'jl', 'jle', 'jmp', 'jna', 'jnae', 'jnb', 'jnbe', 'jnc', 'jne', 'jng', 'jnge', 'jnl', 'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp', 'jpe', 'jpo', 'js', 'jz', 'lahf', 'lds', 'lea', 'les', 'lods', 'lodsb', 'lodsw', 'loop', 'loope', 'loopew', 'loopne', 'loopnew', 'loopnz', 'loopnzw', 'loopw', 'loopz', 'loopzw', 'mov', 'movs', 'movsb', 'movsw', 'mul', 'neg', 'nop', 'not', 'or', 'out', 'pop', 'popf', 'push', 'pushf', 'rcl', 'rcr', 'ret', 'retf', 'retn', 'rol', 'ror', 'sahf', 'sal', 'sar', 'sbb', 'scas', 'scasb', 'scasw', 'shl', 'shr', 'stc', 'std', 'sti', 'stos', 'stosb', 'stosw', 'sub', 'test', 'wait', 'xchg', 'xlat', 'xlatb', 'xor', 'bound', 'enter', 'ins', 'insb', 'insw', 'leave', 'outs', 'outsb', 'outsw', 'popa', 'pusha', 'pushw', 'arpl', 'lar', 'lsl', 'sgdt', 'sidt', 'sldt', 'smsw', 'str', 'verr', 'verw', 'clts', 'lgdt', 'lidt', 'lldt', 'lmsw', 'ltr', 'bsf', 'bsr', 'bt', 'btc', 'btr', 'bts', 'cdq', 'cmpsd', 'cwde', 'insd', 'iretd', 'iretdf', 'iretf', 'jecxz', 'lfs', 'lgs', 'lodsd', 'loopd', 'looped', 'loopned', 'loopnzd', 'loopzd', 'lss', 'movsd', 'movsx', 'movzx', 'outsd', 'popad', 'popfd', 'pushad', 'pushd', 'pushfd', 'scasd', 'seta', 'setae', 'setb', 'setbe', 'setc', 'sete', 'setg', 'setge', 'setl', 'setle', 'setna', 'setnae', 'setnb', 'setnbe', 'setnc', 'setne', 'setng', 'setnge', 'setnl', 'setnle', 'setno', 'setnp', 'setns', 'setnz', 'seto', 'setp', 'setpe', 'setpo', 'sets', 'setz', 'shld', 'shrd', 'stosd', 'bswap', 'cmpxchg', 'invd', 'invlpg', 'wbinvd', 'xadd']
        proc_instance = Proc('someproc')
        [proc_instance.find_op_common_class(i, []) for i in masm_instr_list]

    """
    @patch.object(logging, 'debug')
    @patch.object(logging, 'info')
    # @patch.object(parser, 'get_global')
    def test_convert_data(self, mock_info, mock_debug):

        mock_info.return_value = None
        mock_debug.return_value = None
        parser_instance = Parser([])

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'2*2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'3)')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'5*5 dup (0')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'testEqu*2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'test2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'2*2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'3)')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'5*5 dup (0')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'test2')

        with self.assertRaises(KeyError):
            parser_instance.get_global_value(v=u'testEqu*2')

        # self.assertEqual(parser_instance.convert_data(base=4294967296,v=u'var5'),u'offset(_data,var5)')
    """

    @patch.object(logging, 'debug')
    def test_fix_dollar(self, mock_debug):
        mock_debug.return_value = None
        parser_instance = Parser([])
        assert parser_instance.replace_dollar_w_segoffst(v='-13') == '-13'

        assert parser_instance.replace_dollar_w_segoffst(v='13') == '13'

        assert parser_instance.replace_dollar_w_segoffst(v='var1') == 'var1'

        assert parser_instance.replace_dollar_w_segoffst(v='(00+38*3)*320+1/2+33*(3-1)') == '(00+38*3)*320+1/2+33*(3-1)'

    def test_parse_int(self):
        parser_instance = Parser([])

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v="'Z' - 'A' +1")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v="'a'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v="'c'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v="'d'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v="'tseT'")

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='3)')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='5*5 dup (0')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='B')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='CC')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='DDD')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='OFFSET ASCiI')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='OFFSET AsCii')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[doublequote+4]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[edi+1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[edi]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[load_handle]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var+3]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var+4]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var-1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var0+5]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var1+1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var2+2]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var2-1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var2]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var3+3*4]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var3+ebp]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var3]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='[var]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='_data')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='al')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='beginningdata')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='bl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='buffer')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='bx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='byte ptr [edi+1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='byte ptr [edi+7]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='byte ptr dl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='cl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='cx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='dl')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='ds')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='ds:[edi]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='dword ptr buffer')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='dx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='eax')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='ebp')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='ebx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='ecx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='edi')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='edx')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='enddata')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='es')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='esi')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='fileName')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='offset _msg')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='offset var1')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='offset var2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='offset var5')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='teST2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='test2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='testEqu*2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var1')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var1[1]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var1[bx+si]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var1[bx]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var2')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var3')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var3+3*4')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='var3+ebp')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='word ptr [var5+2]')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='word ptr var5')

        with self.assertRaises(ValueError):
            parser_instance.parse_int(v='ah')

        assert parser_instance.parse_int(v='14*320') == 4480
        assert parser_instance.parse_int(v='2*2') == 4
        assert parser_instance.parse_int(v='3*4') == 12
        assert parser_instance.parse_int(v='-1-(-2+3)') == -2
        assert parser_instance.parse_int(v='-1') == -1
        assert parser_instance.parse_int(v='-11') == -11
        assert parser_instance.parse_int(v='-2') == -2
        assert parser_instance.parse_int(v='0') == 0
        assert parser_instance.parse_int(v='00h') == 0
        assert parser_instance.parse_int(v='03dh') == 61
        assert parser_instance.parse_int(v='03eh') == 62
        assert parser_instance.parse_int(v='03fh') == 63
        assert parser_instance.parse_int(v='042h') == 66
        assert parser_instance.parse_int(v='0Ah') == 10
        assert parser_instance.parse_int(v='0Dh') == 13
        assert parser_instance.parse_int(v='0Fh') == 15
        assert parser_instance.parse_int(v='0ffffff00h') == 4294967040
        assert parser_instance.parse_int(v='1') == 1
        assert parser_instance.parse_int(v='10') == 10
        assert parser_instance.parse_int(v='100') == 100
        assert parser_instance.parse_int(v='1000h') == 4096
        assert parser_instance.parse_int(v='11') == 11
        assert parser_instance.parse_int(v='111') == 111
        assert parser_instance.parse_int(v='12') == 12
        assert parser_instance.parse_int(v='13') == 13
        assert parser_instance.parse_int(v='131') == 131
        assert parser_instance.parse_int(v='16') == 16
        assert parser_instance.parse_int(v='2') == 2
        assert parser_instance.parse_int(v='21h') == 33
        assert parser_instance.parse_int(v='22') == 22
        assert parser_instance.parse_int(v='223') == 223
        assert parser_instance.parse_int(v='25') == 25
        assert parser_instance.parse_int(v='3') == 3
        assert parser_instance.parse_int(v='30h') == 48
        assert parser_instance.parse_int(v='34') == 34
        assert parser_instance.parse_int(v='35') == 35
        assert parser_instance.parse_int(v='37') == 37
        assert parser_instance.parse_int(v='39h') == 57
        assert parser_instance.parse_int(v='4') == 4
        assert parser_instance.parse_int(v='4000000') == 4000000
        assert parser_instance.parse_int(v='4ch') == 76
        assert parser_instance.parse_int(v='5') == 5
        assert parser_instance.parse_int(v='50') == 50
        assert parser_instance.parse_int(v='6') == 6
        assert parser_instance.parse_int(v='64000') == 64000
        assert parser_instance.parse_int(v='7') == 7
        assert parser_instance.parse_int(v='0h') == 0
        assert parser_instance.parse_int(v='0b') == 0

    def test_calculate_data_size(self):
        p = Parser()
        assert p.typetosize('db') == 1
        assert p.typetosize('dd') == 4
        assert p.typetosize('dq') == 8
        assert p.typetosize('dw') == 2
        assert p.typetosize('dt') == 10

    @unittest.skip("was working for parglare")
    @patch.object(logging, 'debug')
    @patch.object(logging, 'info')
    # @patch.object(parser, 'get_global')
    def test_equ(self, mock_info, mock_debug):

        mock_info.return_value = None
        mock_debug.return_value = None
        parser_instance = Parser([])

        cpp_instance = cpp.Cpp(parser_instance)
        proc_instance = Proc('mainproc')
        cpp_instance.proc = proc_instance
        parser_instance.set_global("_data", op.var(1, 0, issegment=True))
        parser_instance.set_global("var1", op.var(size=1, offset=1, name="var1", segment="_data", elements=1))
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('aaaa = 1')) == '#undef aaaa\n#define aaaa 1\n'

        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('B = 1')) == '#undef b\n#define b 1\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('DDD = var1 ; actually it is address of var1')) == '#undef ddd\n#define ddd var1\n'

        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('left equ 0')) == '#define left 0\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('col equ 40')) == '#define col 40\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('right equ left+col')) == '#define right left+col\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('scale_mod equ -19*32*4; ')) == '#define scale_mod -19*32*4\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('tempo equ 1193182/256/targetfps')) == '#define tempo 1193182/256/targetfps\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('sierp_color equ 2Ah')) == '#define sierp_color 0x2A\n'
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('tilt_plate_pattern equ 4+8+16')) == '#define tilt_plate_pattern 4+8+16\n'

        # wrong
        # TODO
        assert proc_instance.generate_full_cmd_line(cpp_instance, parser_instance.action_data('res = edx ; int')) == '#undef res\n#define res edx\n'


if __name__ == "__main__":
    unittest.main()
