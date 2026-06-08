import unittest

from masm2c.parser import Parser


class ParserNumericParseTest(unittest.TestCase):
    def test_parse_numeric_value_matches_parse_int(self):
        parser = Parser([])
        samples = ["10", "0Ah", "17o", "101b", "-3"]

        for s in samples:
            self.assertEqual(parser.parse_numeric_value(s), Parser.parse_int(s))


if __name__ == "__main__":
    unittest.main()
