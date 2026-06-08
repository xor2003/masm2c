import unittest

from masm2c.op import Struct
from masm2c.parser import Parser


class ParserStructRedefinitionLstTest(unittest.TestCase):
    def test_action_ends_allows_lst_pass1_struct_redefinition(self):
        parser = Parser([])
        parser.pass_number = 1
        parser.itislst = True
        parser.struct_names_stack = ["gamekey"]
        parser.current_struct = Struct("gamekey", "struc")
        parser.symbols.set_pass_info(1, False)
        parser.symbols.set_global("gamekey", Struct("gamekey", "struc"))

        parser.action_ends()

        result = parser.symbols.get_global("gamekey")
        self.assertIs(result, parser.structures["gamekey"])


if __name__ == "__main__":
    unittest.main()
