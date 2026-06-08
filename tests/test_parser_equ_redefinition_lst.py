import unittest

from masm2c.Token import Expression
from masm2c.parser import Parser


class ParserEquRedefinitionLstTest(unittest.TestCase):
    @staticmethod
    def _expr(parser: Parser, text: str) -> Expression:
        tree = parser.parse_text(text, start_rule="expr")
        expr = parser.process_ast(text, tree)
        assert isinstance(expr, Expression)
        return expr

    def test_action_equ_allows_lst_pass1_redefinition(self):
        parser = Parser([])
        parser.pass_number = 1
        parser.itislst = True
        parser.symbols.set_pass_info(1, False)

        parser.action_equ("NUL", self._expr(parser, "0"), raw="NUL EQU 0", line_number=1)
        parser.action_equ("NUL", self._expr(parser, "1"), raw="NUL EQU 1", line_number=2)

        symbol = parser.symbols.get_global("nul")
        self.assertIsNotNone(symbol)
        self.assertEqual(getattr(symbol, "line_number", None), 2)


if __name__ == "__main__":
    unittest.main()
