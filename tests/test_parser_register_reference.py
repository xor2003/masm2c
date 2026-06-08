import unittest

from masm2c.Token import Expression
from masm2c.parser import Parser


class ParserRegisterReferenceTest(unittest.TestCase):
    def test_apply_register_reference_sets_size_and_register_set(self):
        parser = Parser([])
        expr = Expression()

        parser.apply_register_reference(expr, "eax")

        self.assertEqual(expr.element_size, 4)
        self.assertIn("eax", expr.registers)

    def test_apply_segment_register_reference_sets_segment_and_size(self):
        parser = Parser([])
        expr = Expression()

        parser.apply_segment_register_reference(expr, "ds")

        self.assertEqual(expr.element_size, 2)
        self.assertEqual(expr.segment_register, "ds")


if __name__ == "__main__":
    unittest.main()
