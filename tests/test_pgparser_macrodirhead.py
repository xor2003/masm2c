import unittest

from lark import Token

from masm2c.pgparser import Asm2IR
from masm2c.parser import Parser


class PgParserMacroDirHeadTest(unittest.TestCase):
    def test_macrodirhead_accepts_lark_children_shape(self):
        parser = Parser([])
        transformer = Asm2IR(parser, "")
        nodes = [Token("LABEL", "SETREGV"), Token("MACRO", "MACRO"), Token("LABEL", "Device")]
        transformer.macrodirhead(nodes)
        self.assertIsNotNone(parser.current_macro)


if __name__ == "__main__":
    unittest.main()

