import unittest

from masm2c.parser import Parser


class ParserTypeSizeTest(unittest.TestCase):
    def test_sizeof_type_matches_typetosize(self):
        parser = Parser([])
        samples = ["byte", "word", "dword", "qword", "near", "far"]

        for s in samples:
            self.assertEqual(parser.sizeof_type(s), parser.typetosize(s))


if __name__ == "__main__":
    unittest.main()
