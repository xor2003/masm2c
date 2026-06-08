import unittest

from lark import Tree, Token

from masm2c.pgparser import Asm2IR
from masm2c.parser import Parser


class PgParserRepeatBeginTest(unittest.TestCase):
    def test_repeatbegin_accepts_lark_children_shape(self):
        parser = Parser([])
        transformer = Asm2IR(parser, "")
        nodes = [Tree("repeatdir", []), Tree("expr", [Token("INTEGER", "2")])]
        transformer.repeatbegin(nodes)
        self.assertIsNotNone(parser.current_macro)


if __name__ == "__main__":
    unittest.main()
