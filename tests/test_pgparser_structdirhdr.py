import unittest

from lark import Token

from masm2c.parser import Parser
from masm2c.pgparser import Asm2IR


class PgParserStructdirhdrTest(unittest.TestCase):
    def test_structdirhdr_accepts_optional_tail_nodes(self):
        parser = Parser([])
        transformer = Asm2IR(parser, "")
        nodes = [
            Token("LABEL", "MyStruct"),
            Token("STRUCTHDR", "STRUC"),
            Token("INTEGER", "4"),
            Token("LABEL", "NONUNIQUE"),
        ]

        transformer.structdirhdr(nodes)

        self.assertIsNotNone(parser.current_struct)
        self.assertEqual(parser.current_struct.name, "mystruct")


if __name__ == "__main__":
    unittest.main()
