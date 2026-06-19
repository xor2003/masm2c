import unittest
from unittest.mock import patch

from masm2c import op
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

    def test_offset_of_struct_sized_var_defaults_to_near_pointer(self):
        parser = Parser([])
        parser.symbols.set_global(
            "packages",
            op.var(size=7, offset=0, name="packages", segment="data", elements=3, original_type="package"),
        )
        parser.action_equ_test("NUM_PACKAGES", "3")
        parser.action_equ_test("PACK_REC_SIZE", "7")

        rendered = parser.parse_arg("OFFSET packages+(NUM_PACKAGES*PACK_REC_SIZE)")

        self.assertEqual(rendered, "offset(data,packages)+(num_packages*pack_rec_size)")

    def test_offset_of_parenthesized_expression_renders_operand(self):
        parser = Parser([])
        parser.symbols.set_global(
            "ze",
            op.var(size=2, offset=0, name="ze", segment="data", elements=1),
        )

        rendered = parser.parse_arg("OFFSET (ze+0)")

        self.assertEqual(rendered, "offset(data,ze)+0")


if __name__ == "__main__":
    unittest.main()
