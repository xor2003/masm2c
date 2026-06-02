import unittest

from masm2c import op
from masm2c.parser import Parser


class ParserDataRedefinitionLstTest(unittest.TestCase):
    def test_data_decl_allows_lst_pass1_assignment_placeholder_upgrade(self):
        parser = Parser([])
        parser.pass_number = 1
        parser.itislst = True
        parser.symbols.set_pass_info(1, False)
        parser.create_segment("dseg")

        source = "argc = word ptr 4\nargc dw 0\n"
        result = parser.parse_file_inside(source, file_name="test.lst")
        parser.process_ast(source, result)

        symbol = parser.symbols.get_global("argc")
        self.assertIsInstance(symbol, op.var)
        self.assertEqual(symbol.segment, "dseg")


if __name__ == "__main__":
    unittest.main()
