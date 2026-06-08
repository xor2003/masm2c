import unittest

from masm2c.parser import Parser


class ParserLabelNormalizationTest(unittest.TestCase):
    def test_normalize_label_matches_mangle(self):
        parser = Parser([])
        samples = ["A@B", "X$Y", "Q?W", "Plain"]

        for s in samples:
            self.assertEqual(parser.normalize_label(s), Parser.mangle_label(s))


if __name__ == "__main__":
    unittest.main()
