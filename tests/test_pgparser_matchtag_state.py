import unittest

from masm2c.parser import Parser


class PgParserMatchTagStateTest(unittest.TestCase):
    def test_bind_context_resets_matchtag_state(self):
        parser = Parser([])
        lex = parser._Parser__lex
        postlex = lex._postlex
        lexer_callback = getattr(lex, "_lexer_callback", None)
        if postlex is None and lexer_callback is None:
            self.skipTest("dynamic token classifier is disabled for this parser mode")

        if postlex is not None:
            postlex.last_type = "LABEL"
            postlex.last = "stale"
        if lexer_callback is not None:
            lexer_callback.last_type = "LABEL"
            lexer_callback.last = "stale"

        lex.bind_context(parser)

        if postlex is not None:
            self.assertEqual(postlex.last_type, "")
            self.assertEqual(postlex.last, "")
        if lexer_callback is not None:
            self.assertEqual(lexer_callback.last_type, "")
            self.assertEqual(lexer_callback.last, "")


if __name__ == "__main__":
    unittest.main()
