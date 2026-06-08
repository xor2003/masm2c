import unittest

from masm2c.parser import Parser


class ParserStructureMatchTest(unittest.TestCase):
    def test_match_known_structure_name(self):
        parser = Parser([])
        parser.declare_structure_name("abc")

        self.assertEqual(parser.match_known_structure_name("ABC"), "abc")
        self.assertIsNone(parser.match_known_structure_name("zzz"))


if __name__ == "__main__":
    unittest.main()
