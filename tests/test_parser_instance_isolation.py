import unittest

from masm2c.parser import Parser


class ParserInstanceIsolationTest(unittest.TestCase):
    def test_parser_instances_do_not_share_postlex_context(self):
        parser1 = Parser([])
        parser2 = Parser([])

        src = "MYSTRUC struc\nfld dw ?\nMYSTRUC ends\n"
        tree = parser2.parse_text(src, start_rule="insegdirlist")
        parser2.process_ast(src, tree)

        self.assertIn("mystruc", parser2.structures)
        self.assertNotIn("mystruc", parser1.structures)


if __name__ == "__main__":
    unittest.main()
