import unittest

from masm2c.parser import Parser


class PgParserMatchTagStateTest(unittest.TestCase):
    def test_bind_context_resets_matchtag_state(self):
        parser = Parser([])
        lex = parser._Parser__lex
        postlex = lex._postlex

        postlex.last_type = "LABEL"
        postlex.last = "stale"

        lex.bind_context(parser)

        self.assertEqual(postlex.last_type, "")
        self.assertEqual(postlex.last, "")


if __name__ == "__main__":
    unittest.main()
