import unittest

from masm2c.Token import Expression
from masm2c.parser import Parser


class ParserInstructionArgsTest(unittest.TestCase):
    def test_prepare_instruction_args_marks_destination(self):
        parser = Parser([])
        a0 = Expression()
        a1 = Expression()

        out = parser.prepare_instruction_args("mov", [a0, a1])

        self.assertIs(out[0], a0)
        self.assertIn("destination", a0.mods)
        self.assertNotIn("lea", a0.mods)

    def test_prepare_instruction_args_marks_lea(self):
        parser = Parser([])
        a0 = Expression()
        a1 = Expression()

        out = parser.prepare_instruction_args("lea", [a0, a1])

        self.assertIn("destination", out[0].mods)
        self.assertIn("lea", out[0].mods)
        self.assertIn("lea", out[1].mods)


if __name__ == "__main__":
    unittest.main()
