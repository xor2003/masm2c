import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserOffsetDirectiveTest(unittest.TestCase):
    def test_apply_offset_directive_align(self):
        parser = Parser([])
        with patch.object(parser, "align") as align:
            parser.apply_offset_directive("align", "10h")
        align.assert_called_once_with(0x10)

    def test_apply_offset_directive_even(self):
        parser = Parser([])
        with patch.object(parser, "align") as align:
            parser.apply_offset_directive("even", "ignored")
        align.assert_called_once_with(2)

    def test_apply_offset_directive_org(self):
        parser = Parser([])
        with patch.object(parser, "org") as org:
            parser.apply_offset_directive("org", "20h")
        org.assert_called_once_with(0x20)


if __name__ == "__main__":
    unittest.main()
