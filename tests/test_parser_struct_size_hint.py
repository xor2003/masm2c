import unittest

from masm2c.parser import Parser


class ParserStructSizeHintTest(unittest.TestCase):
    def test_struct_size_hint_for_label_from_registry(self):
        parser = Parser([])
        parser.declare_structure_name("mystr")
        parser.structures["mystr"].size = 11

        self.assertEqual(parser.struct_size_hint_for_label("mystr"), 11)
        self.assertIsNone(parser.struct_size_hint_for_label("unknown"))


if __name__ == "__main__":
    unittest.main()
