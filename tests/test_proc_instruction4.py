import unittest

from masm2c.Token import Expression
from masm2c.proc import Proc


class ProcInstruction4Test(unittest.TestCase):
    def test_create_instruction_object_supports_four_args(self):
        proc = Proc("p")
        args = [Expression("expr", ["1"]), Expression("expr", ["2"]), Expression("expr", ["3"]), Expression("expr", ["4"])]

        op = proc.create_instruction_object("shake", args)

        self.assertEqual(op.cmd, "shake")
        self.assertEqual(len(op.children), 4)


if __name__ == "__main__":
    unittest.main()
