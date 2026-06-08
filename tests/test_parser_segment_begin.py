import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserSegmentBeginTest(unittest.TestCase):
    def test_begin_simple_segment_forwards_to_action(self):
        parser = Parser([])
        with patch.object(parser, "action_simplesegment", return_value=None) as ass:
            parser.begin_simple_segment("code")
        ass.assert_called_once_with("code", None)


if __name__ == "__main__":
    unittest.main()
