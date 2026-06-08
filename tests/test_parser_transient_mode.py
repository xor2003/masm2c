import unittest
from collections import OrderedDict

from masm2c.parser import Parser


class ParserTransientModeTest(unittest.TestCase):
    def test_parse_arg_restores_test_mode_and_segments(self):
        parser = Parser([])
        parser.test_mode = False
        parser.segments = OrderedDict([("sentinel", object())])
        old_segments = parser.segments

        _ = parser.parse_arg("1", def_size=0, destination=False)

        self.assertFalse(parser.test_mode)
        self.assertIs(parser.segments, old_segments)
        self.assertIn("sentinel", parser.segments)

    def test_action_code_restores_need_label(self):
        parser = Parser([])
        parser.need_label = True

        _ = parser.action_code("nop")

        self.assertTrue(parser.need_label)


if __name__ == "__main__":
    unittest.main()
