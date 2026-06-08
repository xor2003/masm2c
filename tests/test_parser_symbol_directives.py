import unittest
from unittest.mock import patch

from masm2c.Token import Expression
from masm2c.parser import Parser


class ParserSymbolDirectivesTest(unittest.TestCase):
    def test_declare_external_symbol_forwards_to_add_extern(self):
        parser = Parser([])
        with patch.object(parser, "add_extern", return_value=None) as ae:
            parser.declare_external_symbol("x", "word")
        ae.assert_called_once_with("x", "word")

    def test_define_equ_forwards_to_action_equ(self):
        parser = Parser([])
        expr = Expression()
        with patch.object(parser, "action_equ", return_value="ok") as ae:
            out = parser.define_equ("k", expr, raw="k equ 1", line_number=9)
        ae.assert_called_once_with("k", expr, raw="k equ 1", line_number=9)
        self.assertEqual(out, "ok")

    def test_define_assignment_forwards_to_action_assign(self):
        parser = Parser([])
        expr = Expression()
        with patch.object(parser, "action_assign", return_value="ok") as aa:
            out = parser.define_assignment("v", expr, raw="v = 1", line_number=10)
        aa.assert_called_once_with("v", expr, raw="v = 1", line_number=10)
        self.assertEqual(out, "ok")


if __name__ == "__main__":
    unittest.main()
