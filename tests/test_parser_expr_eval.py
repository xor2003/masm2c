import unittest

from masm2c.parser import Parser
from masm2c.Token import Expression
from masm2c.enumeration import IndirectionType


class ParserExprEvalTest(unittest.TestCase):
    def test_eval_expression_to_int_uses_injected_evaluator(self):
        parser = Parser([])
        parser.expr_int_evaluator = lambda _parser, _expr: 77

        value = parser.eval_expression_to_int(Expression())

        self.assertEqual(value, 77)

    def test_evaluate_repeat_count_uses_parser_evaluator(self):
        parser = Parser([])
        expr = Expression()
        expr.indirection = IndirectionType.POINTER

        def evaluator(_parser: Parser, repeat_expr: Expression) -> int:
            self.assertEqual(repeat_expr.indirection, IndirectionType.VALUE)
            return 5

        parser.expr_int_evaluator = evaluator
        self.assertEqual(parser.evaluate_repeat_count(expr), 5)
        self.assertEqual(expr.indirection, IndirectionType.POINTER)


if __name__ == "__main__":
    unittest.main()
