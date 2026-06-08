import unittest

from masm2c.parser import Parser


class ParserRegisterSizeTest(unittest.TestCase):
    def test_register_size_matches_is_register(self):
        parser = Parser([])
        samples = ["al", "ax", "eax", "ds", "notareg"]

        for s in samples:
            self.assertEqual(parser.register_size(s), Parser.is_register(s))


if __name__ == "__main__":
    unittest.main()
