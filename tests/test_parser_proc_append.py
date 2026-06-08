import unittest

from masm2c.parser import Parser
from masm2c.proc import Proc


class ParserProcAppendTest(unittest.TestCase):
    def test_append_current_statements(self):
        parser = Parser([])
        parser.proc = Proc("mainproc")
        item = object()

        parser.append_current_statements([item])

        self.assertEqual(len(parser.proc.stmts), 1)
        self.assertIs(parser.proc.stmts[0], item)

    def test_append_current_statement(self):
        parser = Parser([])
        parser.proc = Proc("mainproc")
        item = object()

        parser.append_current_statement(item)

        self.assertEqual(len(parser.proc.stmts), 1)
        self.assertIs(parser.proc.stmts[0], item)


if __name__ == "__main__":
    unittest.main()
