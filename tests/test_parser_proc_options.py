import unittest

from masm2c.parser import Parser


class ParserProcOptionsTest(unittest.TestCase):
    def test_consume_proc_options_returns_and_clears(self):
        parser = Parser([])
        parser.set_pending_proc_options(["near", "public"])

        out = parser.consume_proc_options()
        self.assertEqual(out, ["near", "public"])
        self.assertEqual(parser.consume_proc_options(), [])


if __name__ == "__main__":
    unittest.main()
