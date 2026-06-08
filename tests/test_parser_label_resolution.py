import unittest

from masm2c.Token import Expression
from masm2c.parser import Parser


class ParserLabelResolutionTest(unittest.TestCase):
    def test_resolve_label_for_expression_with_equ_sets_element_size(self):
        parser = Parser([])
        parser.action_equ_test(label="eq1", value="word ptr 1")
        expr = Expression()

        normalized = parser.resolve_label_for_expression("eq1", expr)

        self.assertEqual(normalized, "eq1")
        self.assertEqual(expr.element_size, 2)

    def test_resolve_label_for_expression_with_struct_sets_element_size(self):
        parser = Parser([])
        parser.declare_structure_name("mystr")
        s = parser.structures["mystr"]
        s.size = 7
        expr = Expression()

        normalized = parser.resolve_label_for_expression("mystr", expr)

        self.assertEqual(normalized, "mystr")
        self.assertEqual(expr.element_size, 7)


if __name__ == "__main__":
    unittest.main()
