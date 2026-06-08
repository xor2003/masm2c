import unittest

from masm2c.Token import Expression
from masm2c.parser import Parser


class ParserRepeatCountTest(unittest.TestCase):
    def test_evaluate_repeat_count_pass1_unknown_symbol_fallback_zero(self):
        parser = Parser([])
        parser.pass_number = 1

        repeat = Expression("expr", ["max_args"])
        value = parser.evaluate_repeat_count(repeat)

        self.assertEqual(value, 0)


if __name__ == "__main__":
    unittest.main()
