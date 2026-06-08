import unittest

from masm2c import cpp
from masm2c.parser import Parser
from masm2c.proc import Proc


class ParserCommentPreservationTest(unittest.TestCase):
    def test_standalone_comment_is_preserved_as_stmt_raw_line(self):
        parser = Parser([])
        parser.action_data("; hello from asm")

        self.assertTrue(any("hello from asm" in s.raw_line for s in parser.proc.stmts))

    def test_instruction_comment_not_duplicated(self):
        parser = Parser([])
        stmt = parser.action_code("mov ax,1 ; cmt")
        self.assertIn("; cmt", stmt.raw_line)
        self.assertEqual(stmt.raw_line.count("; cmt"), 1)

    def test_generated_body_keeps_comment_text(self):
        parser = Parser([])
        c = cpp.Cpp(parser)
        p = Proc("mainproc")
        c.proc = p
        stmt = parser.action_code("mov ax,1 ; keepme")
        body = p.generate_full_cmd_line(c, stmt)
        self.assertIn("ax = 1", body)
        self.assertIn("; keepme", stmt.raw_line)

    def test_standalone_comment_reaches_generated_c_body(self):
        parser = Parser([])
        parser.action_data("; keep this standalone comment")

        c = cpp.Cpp(parser)
        c.proc = parser.proc
        assert parser.proc is not None
        parser.proc.visit(c)

        self.assertIn("keep this standalone comment", c.body)


if __name__ == "__main__":
    unittest.main()
