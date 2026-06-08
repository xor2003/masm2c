import unittest

from masm2c.parser import Parser


class ParserMacroStackTest(unittest.TestCase):
    def test_macro_name_stack_is_lifo_list(self):
        parser = Parser([])

        self.assertIsInstance(parser.macro_names_stack, list)
        parser.macro_names_stack.append("m1")
        parser.macro_names_stack.append("m2")

        self.assertEqual(parser.macro_names_stack.pop(), "m2")
        self.assertEqual(parser.macro_names_stack.pop(), "m1")


if __name__ == "__main__":
    unittest.main()
