import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserLstModeLeakTest(unittest.TestCase):
    def test_parse_file_lines_restores_lst_mode_after_lst_file(self):
        parser = Parser([])
        parser.itislst = False

        with patch("masm2c.utils.read_whole_file", return_value="SEG1:0001 mov ax,1\n"):
            with patch.object(parser, "read_segments_map", return_value={"SEG1": "1234"}):
                with patch.object(parser, "parse_text", return_value="ast"):
                    with patch.object(parser, "process_ast", return_value=None):
                        parser.parse_file_lines("x.lst")

        self.assertFalse(parser.itislst)
        self.assertTrue(parser.is_listing_source())


if __name__ == "__main__":
    unittest.main()
