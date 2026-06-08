import unittest

from masm2c.parser import Parser
from masm2c.proc import Proc
from masm2c import cpp


class ParserCommentSemanticsTest(unittest.TestCase):
    def test_instruction_comment_does_not_change_codegen(self):
        parser = Parser([])
        c = cpp.Cpp(parser)
        p = Proc("mainproc")
        c.proc = p

        a = p.generate_c_cmd(c, parser.action_code("mov ax,1"))
        b = p.generate_c_cmd(c, parser.action_code("mov ax,1 ; trailing comment"))

        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
