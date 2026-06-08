import unittest
from unittest.mock import patch

from lark import Tree

from masm2c.parser import Parser


class ParserDataDirectivesTest(unittest.TestCase):
    def test_define_struct_instance_forwards(self):
        parser = Parser([])
        with patch.object(parser, "add_structinstance", return_value=None) as asi:
            parser.define_struct_instance("lbl", "mystruct", [1], raw="lbl mystruct <>")
        asi.assert_called_once_with("lbl", "mystruct", [1], raw="lbl mystruct <>")

    def test_define_data_forwards(self):
        parser = Parser([])
        values = Tree("data", [])
        with patch.object(parser, "datadir_action", return_value=[]) as da:
            out = parser.define_data("x", "db", values, is_string=False, raw="x db 1", line_number=3)
        da.assert_called_once_with("x", "db", values, is_string=False, raw="x db 1", line_number=3)
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
