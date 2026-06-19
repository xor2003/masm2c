import unittest

from masm2c.parser import Parser


class PgParserExternDefTest(unittest.TestCase):
    def test_externdef_far_is_accepted(self):
        parser = Parser([])
        content = "EXTERNDEF RunLenDecode:FAR\n"
        tree = parser.parse_text(content, start_rule="_directivelist")
        parser.process_ast(content, tree)
        self.assertIn("runlendecode", parser.externals_procs)
        self.assertNotIn("runlendecode", parser.externals_vars)
        self.assertTrue(parser.symbols.get_global("runlendecode").far)


if __name__ == "__main__":
    unittest.main()
