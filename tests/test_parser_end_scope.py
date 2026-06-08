import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserEndScopeTest(unittest.TestCase):
    def test_end_current_scope_forwards_to_action_ends(self):
        parser = Parser([])
        with patch.object(parser, "action_ends", return_value=None) as ae:
            parser.end_current_scope()
        ae.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
