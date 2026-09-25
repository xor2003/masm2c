import unittest

from masm2c import op
from masm2c.parser import Parser


class ParserNegativeDataElementsTest(unittest.TestCase):
    """`DB` elements after an unsized EQU must keep the declared element width.

    An EQU whose value carries no size used to zero the size calculator's
    element width, so two's-complement conversion of later negative literals
    wrapped at 2**0 (-1 -> 0, -2 -> -1).  Tornado face lists such as
    ``DB 8,COL_GREEN2,6,8,4,0,-1`` lost every -1 terminator this way.
    """

    @staticmethod
    def _parse(source: str) -> list:
        parser = Parser([])
        parser.itislst = True
        parser.create_segment("dseg")
        result = parser.parse_file_inside(source, file_name="test.lst")
        parser.process_ast(source, result)
        return [d for d in parser.segments["dseg"].children if isinstance(d, op.Data)]

    def test_negative_literal_after_unsized_equate(self):
        datas = self._parse(
            "COL_GREEN2 EQU 039h\n"
            " DB 8,COL_GREEN2,6,8,4,0,-1\n"
            " DB 8,COL_GREEN2,6,8,4,0,-2\n"
            " DB -1\n"
        )
        self.assertEqual(datas[0].getdata()[3][-1], 255)
        self.assertEqual(datas[1].getdata()[3][-1], 254)
        self.assertEqual(datas[2].getdata()[3][-1], 255)

    def test_negative_literal_after_unsized_equate_dw(self):
        datas = self._parse(
            "VAL EQU 5\n"
            " DW 1,VAL,-1\n"
        )
        self.assertEqual(datas[0].getdata()[3][-1], 65535)


if __name__ == "__main__":
    unittest.main()
