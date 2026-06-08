import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserProgramFinishTest(unittest.TestCase):
    def test_finish_program_forwards_to_action_end(self):
        parser = Parser([])
        with patch.object(parser, "action_end", return_value=None) as ae:
            parser.finish_program("start")
        ae.assert_called_once_with("start")


if __name__ == "__main__":
    unittest.main()
