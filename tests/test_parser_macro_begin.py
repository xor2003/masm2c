import unittest

from masm2c.parser import Parser


class ParserMacroBeginTest(unittest.TestCase):
    def test_begin_named_macro_creates_pending_macro(self):
        parser = Parser([])
        parser.begin_named_macro("m1", ["a", "b"])

        self.assertEqual(parser.macro_names_stack[-1], "m1")
        assert parser.current_macro is not None
        self.assertEqual(parser.current_macro.getparameters(), ["a", "b"])

    def test_begin_repeat_macro_creates_pending_macro(self):
        parser = Parser([])
        parser.begin_repeat_macro(3)

        self.assertEqual(parser.macro_names_stack[-1], "")
        assert parser.current_macro is not None
        self.assertEqual(parser.current_macro.getparameters(), [])


if __name__ == "__main__":
    unittest.main()
