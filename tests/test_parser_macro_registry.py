import unittest

from masm2c.Macro import Macro
from masm2c.parser import Parser


class ParserMacroRegistryTest(unittest.TestCase):
    def test_macro_registry_begin_get_end(self):
        parser = Parser([])
        macro = Macro("m1", ["a"])

        parser.begin_macro_definition("m1", macro)
        self.assertFalse(parser.is_known_macro("m1"))
        self.assertEqual(parser.current_macro, macro)

        parser.end_macro_definition()

        self.assertIsNone(parser.current_macro)
        self.assertTrue(parser.is_known_macro("m1"))
        stored = parser.get_macro("m1")
        self.assertIs(stored, macro)
        self.assertEqual(stored.getparameters(), ["a"])


if __name__ == "__main__":
    unittest.main()
