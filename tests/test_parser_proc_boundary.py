import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserProcBoundaryTest(unittest.TestCase):
    def test_begin_procedure_forwards_to_action_proc(self):
        parser = Parser([])
        with patch.object(parser, "action_proc", return_value=None) as ap:
            parser.begin_procedure("foo", ["near"], line_number=10, raw="foo proc near")
        ap.assert_called_once_with("foo", ["near"], line_number=10, raw="foo proc near")

    def test_end_procedure_forwards_to_action_endp(self):
        parser = Parser([])
        with patch.object(parser, "action_endp", return_value=None) as ae:
            parser.end_procedure()
        ae.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
