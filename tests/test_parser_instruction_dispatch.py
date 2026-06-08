import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserInstructionDispatchTest(unittest.TestCase):
    def test_dispatch_instruction_forwards_to_action_instruction(self):
        parser = Parser([])
        with patch.object(parser, "action_instruction", return_value="ok") as ai:
            out = parser.dispatch_instruction("mov", ["ax", "1"], raw="mov ax,1", line_number=12)
        ai.assert_called_once_with("mov", ["ax", "1"], raw="mov ax,1", line_number=12)
        self.assertEqual(out, "ok")


if __name__ == "__main__":
    unittest.main()
