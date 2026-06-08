import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserNamedSegmentTest(unittest.TestCase):
    def test_begin_named_segment_forwards_to_create_segment(self):
        parser = Parser([])
        with patch.object(parser, "create_segment", return_value=None) as cs:
            parser.begin_named_segment("text", options={"public"}, segclass="CODE", raw="text segment")
        cs.assert_called_once_with("text", options={"public"}, segclass="CODE", raw="text segment")

    def test_raw_segment_without_ends_still_rejected(self):
        parser = Parser([])
        source = (
            "seg000 segment byte public 'CODE' use16\n"
            "db 0\n"
            "seg001 segment byte public 'CODE' use16\n"
            "db 1\n"
            "end\n"
        )

        with self.assertRaises(SystemExit):
            parser.parse_text(source)

    def test_ida_lst_does_not_repair_missing_mandatory_segment_ends(self):
        parser = Parser([])
        source = (
            "seg000:0000 seg000 segment byte public 'CODE' use16\n"
            "seg000:0000 db 0\n"
            "seg001:0002 seg001 segment byte public 'CODE' use16\n"
            "seg001:0002 sub_1 proc far\n"
            "seg001:0002 arg_6= byte ptr  0Ch\n"
            "seg001:0002 sub_1 endp\n"
            "seg001:0002 db 1\n"
            "seg001:0003 end\n"
        )

        processed = parser.extract_addresses_from_lst("/tmp/sample.lst", source)

        self.assertNotIn("seg000 ends", processed.lower())
        self.assertNotIn("seg001 ends", processed.lower())
        with self.assertRaises(SystemExit):
            parser.parse_text(processed)


if __name__ == "__main__":
    unittest.main()
