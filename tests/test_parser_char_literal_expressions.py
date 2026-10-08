import unittest

from masm2c.cpp import Cpp
from masm2c.parser import Parser


class ParserCharLiteralExpressionsTest(unittest.TestCase):
    """Quoted literals used as arithmetic operands are character constants.

    ``DB "="+128D`` (GW-BASIC SPCTAB) must emit one byte with the ASCII
    value plus 128.  Previously the ``AsmData2IR`` visitor flattened the
    operator node into a character list (``['=', '+', 128]``), which the
    string renderer then emitted as three bytes ``{'=','+','\\x80'}``,
    corrupting every table that mixes them.
    """

    def setUp(self):
        self.parser = Parser()
        self.cpp = Cpp(self.parser)
        self.parser.action_label(far=False, name="lbl", isproc=False)

    def convert_data(self, line=""):
        ir = self.parser.action_data(line=line)
        return tuple(self.cpp.visit(ir))

    def test_char_plus_integer_folds_to_single_byte(self):
        assert self.convert_data(line='db "=" +128D') == ("189, // lbl\n", "db lbl;\n", 1)

    def test_char_minus_integer(self):
        assert self.convert_data(line='db "="-1') == ("60, // lbl\n", "db lbl;\n", 1)

    def test_symbol_char_and_plain_int_variants(self):
        assert self.convert_data(line='db "+"+128D,"-"+128D,"*"+128D') == (
            "{171,173,170}, // lbl\n", "db lbl[3];\n", 3)

    def test_mixed_string_record_folds_expression_element(self):
        assert self.convert_data(line='db "a"+1,"bc"') == ("{98,'b','c'}, // lbl\n", "char lbl[3];\n", 3)

    def test_plain_numeric_expression_unchanged(self):
        assert self.convert_data(line="db 62+128D") == ("62+128, // lbl\n", "db lbl;\n", 1)

    def test_plain_string_unchanged(self):
        assert self.convert_data(line='db "AB"') == ("{'A','B'}, // lbl\n", "char lbl[2];\n", 2)

    def test_label_expression_unchanged(self):
        assert self.convert_data(line="db lbl+5") == ("lbl+5, // lbl\n", "db lbl;\n", 1)

    def test_shift_expression_renders_cpp_operator(self):
        assert self.convert_data(line="db 1 shl 4") == ("1<<4, // lbl\n", "db lbl;\n", 1)

    def test_unary_minus_on_char_literal(self):
        assert self.convert_data(line='db -"a"') == ("db(-97), // lbl\n", "db lbl;\n", 1)

    def test_parenthesized_char_literal(self):
        assert self.convert_data(line='db ("a")+1') == ("98, // lbl\n", "db lbl;\n", 1)

    def test_high_word_operator(self):
        code, _decl, size = self.convert_data(line="db high 1234h")
        assert "& 0xff" in code and ">> 8" in code and size == 1

    def test_two_char_literal_operand_little_endian(self):
        code, _, _ = self.convert_data(line='dw "AB"+1')
        assert code == "16962, // lbl\n"


if __name__ == "__main__":
    unittest.main()
