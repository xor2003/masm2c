import unittest

from masm2c.parser import Parser


class ParserLstPreambleTest(unittest.TestCase):
    def test_extract_addresses_comments_masm_banner_and_page_header(self):
        parser = Parser([])
        content = (
            "Microsoft (R) Macro Assembler Version 6.11    05/30/26 16:33:26\n"
            "CGA_DRVR.ASM                        Page 1 - 1\n"
            "\tOPTION\tM510\n"
        )
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        lines = output.splitlines()
        self.assertTrue(lines[0].startswith("; Microsoft (R) Macro Assembler"))
        self.assertTrue(lines[1].startswith("; CGA_DRVR.ASM"))
        self.assertIn("OPTION", lines[2])

    def test_extract_addresses_removes_listing_offset_and_object_columns(self):
        parser = Parser([])
        content = " 0000 C0            ColMask    DB 11000000b\n = B800           CGA_REAL_SCR EQU 0b800h\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        lines = output.splitlines()
        self.assertTrue(lines[0].lstrip().startswith("ColMask"))
        self.assertTrue(lines[1].lstrip().startswith("CGA_REAL_SCR"))

    def test_extract_addresses_removes_signed_equal_prefix(self):
        parser = Parser([])
        content = " =-8000            DUMMY_MIN EQU -32768\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("DUMMY_MIN EQU -32768"))

    def test_extract_addresses_removes_symbolic_equal_prefix(self):
        parser = Parser([])
        content = " = EGA_MODEL            VIDEO_BUF_SIZE EQU EGA_MODEL\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("VIDEO_BUF_SIZE EQU EGA_MODEL"))

    def test_extract_addresses_keeps_binary_literal_suffix_after_cleanup(self):
        parser = Parser([])
        content = " 0001  30                    DB 00110000b\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertIn("00110000b", output)

    def test_extract_addresses_strips_relocation_marker_column(self):
        parser = Parser([])
        content = " 0008 0100 R            OctTable DW Oct2\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("OctTable"))

    def test_extract_addresses_strips_short_offset_relocation_prefix(self):
        parser = Parser([])
        content = "000D R            mov RxQWtPtr,OFFSET RxQHead\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("mov RxQWtPtr,OFFSET RxQHead"))

    def test_extract_addresses_strips_bracketed_listing_continuation_lines(self):
        parser = Parser([])
        content = "[\n00\n]\nDB 130 DUP(0)\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertNotIn("[", output)
        self.assertNotIn("\n00\n", output)
        self.assertNotIn("]\n", output)
        self.assertIn("DB 130 DUP(0)", output)

    def test_extract_addresses_strips_inline_leading_bracket_before_directive(self):
        parser = Parser([])
        content = "[\t\tDB\t130 DUP(0)\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("DB\t130 DUP(0)"))

    def test_extract_addresses_strips_masm_dash_address_prefix(self):
        parser = Parser([])
        content = "---- 0000 E                call ResetMouse\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("call ResetMouse"))

    def test_extract_addresses_strips_slash_suffixed_object_bytes(self):
        parser = Parser([])
        content = " 003A F3/ A4               rep movsb\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("rep movsb"))

    def test_extract_addresses_strips_segment_prefixed_hex_bytes(self):
        parser = Parser([])
        content = "26: 22 05                and al,es:[di]\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("and al,es:[di]"))

    def test_extract_addresses_strips_opcode_bytes_before_instruction(self):
        parser = Parser([])
        content = " 0078  86 DF                    xchg    bl,bh\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("xchg"))

    def test_extract_addresses_strips_single_hex_opcode_prefix(self):
        parser = Parser([])
        content = "DD                    mov bx,bp\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("mov bx,bp"))

    def test_extract_addresses_strips_macro_expansion_index_prefix(self):
        parser = Parser([])
        content = "1            mov ax,es:[di]\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("mov ax,es:[di]"))

    def test_extract_addresses_strips_single_hex_prefix_before_label(self):
        parser = Parser([])
        content = "04      CGA_PrtC2Com: add PrtCl,4\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("CGA_PrtC2Com:"))

    def test_extract_addresses_truncates_after_end_directive(self):
        parser = Parser([])
        content = "mov ax,bx\nEND\nMicrosoft (R) Macro Assembler Version 6.11\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertEqual("mov ax,bx\nEND\n", output)

    def test_extract_addresses_strips_include_expansion_marker_prefix(self):
        parser = Parser([])
        content = "      C ;* KEYS.INC\n      C INCLUDE KEYS.INC\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        lines = output.splitlines()
        self.assertTrue(lines[0].startswith(";* KEYS.INC"))
        self.assertTrue(lines[1].startswith("INCLUDE KEYS.INC"))

    def test_extract_addresses_strips_column1_include_marker_prefix(self):
        parser = Parser([])
        content = "C ;* KEYS.INC\nC INCLUDE KEYS.INC\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        lines = output.splitlines()
        self.assertTrue(lines[0].startswith(";* KEYS.INC"))
        self.assertTrue(lines[1].startswith("INCLUDE KEYS.INC"))

    def test_extract_addresses_normalizes_simple_angle_text_items(self):
        parser = Parser([])
        content = "IFNB <fn>\nIFIDNI <fn>,<_AND_>\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertIn("IFNB <fn >", output)
        self.assertIn("IFIDNI <fn >,<_AND_ >", output)

    def test_extract_addresses_strips_macro_index_before_local_label(self):
        parser = Parser([])
        content = "1    @@:   inc cx\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertTrue(output.lstrip().startswith("@@:"))

    def test_extract_addresses_preserves_empty_angle_initializer(self):
        parser = Parser([])
        content = "M_TEST VIEWPOINT <>\n"
        output = parser.extract_addresses_from_lst("/tmp/sample.lst", content)
        self.assertIn("VIEWPOINT <>", output)


if __name__ == "__main__":
    unittest.main()

def test_extract_addresses_preserves_empty_struct_initializer() -> None:
    parser = Parser()
    source = " 001C  000A \t\t\tOptTable\tACTION\tNUM_OPTIONS DUP(<>)\n"

    result = parser.extract_addresses_from_lst("/tmp/demo.lst", source)

    assert "DUP(<>)" in result
