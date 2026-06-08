import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserDefineLabelTest(unittest.TestCase):
    def test_define_label_forwards_to_action_label(self):
        parser = Parser([])
        with patch.object(parser, "action_label", return_value=None) as al:
            parser.define_label("L1", raw="L1:", line_number=7, globl=True)
        al.assert_called_once_with("L1", isproc=False, raw="L1:", line_number=7, globl=True)


if __name__ == "__main__":
    unittest.main()
