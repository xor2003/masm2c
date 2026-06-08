import unittest

from masm2c.parser import Parser


class ParserLstMapOptionalTest(unittest.TestCase):
    def test_read_segments_map_missing_file_returns_empty_mapping(self):
        parser = Parser([])
        segmap = parser.read_segments_map("/tmp/masm2c-not-existing.lst")
        self.assertEqual({}, dict(segmap))


if __name__ == "__main__":
    unittest.main()

