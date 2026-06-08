import unittest

from masm2c.Macro import Macro
from masm2c.parser import Parser
from masm2c.pgparser import Asm2IR


class PgParserMacroScopeTest(unittest.TestCase):
    def test_macroname_lookup_is_parser_local(self):
        parser1 = Parser([])
        parser2 = Parser([])
        parser1.macroses["m1"] = Macro("m1", [])

        asm1 = Asm2IR(parser1, "")
        asm2 = Asm2IR(parser2, "")

        self.assertEqual(asm1.macroname("m1", 0), "m1")
        self.assertIsNone(asm2.macroname("m1", 0))


if __name__ == "__main__":
    unittest.main()
