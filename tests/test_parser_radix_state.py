import unittest

from masm2c.parser import Parser
from masm2c.pgparser import Asm2IR


class ParserRadixStateTest(unittest.TestCase):
    def test_set_radix_accepts_valid_range(self):
        parser = Parser([])
        parser.set_radix(16)
        self.assertEqual(parser.radix, 16)
        parser.set_radix(2)
        self.assertEqual(parser.radix, 2)

    def test_set_radix_rejects_invalid_values(self):
        parser = Parser([])
        with self.assertRaises(ValueError):
            parser.set_radix(1)
        with self.assertRaises(ValueError):
            parser.set_radix(17)

    def test_radixdir_updates_parser_context(self):
        parser = Parser([])
        transformer = Asm2IR(parser)
        transformer.radixdir(["16"])
        self.assertEqual(parser.radix, 16)


if __name__ == "__main__":
    unittest.main()
