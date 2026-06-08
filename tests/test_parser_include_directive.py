import unittest
from unittest.mock import patch

from masm2c.parser import Parser


class ParserIncludeDirectiveTest(unittest.TestCase):
    def test_parse_include_directive_resolves_and_parses(self):
        parser = Parser([])
        parser._current_file = "/tmp/proj/main.asm"

        with patch.object(parser, "parse_include_file_lines", return_value="ok") as p:
            out = parser.parse_include_directive("inc/a.inc")

        p.assert_called_once_with("/tmp/proj/inc/a.inc")
        self.assertEqual(out, "ok")


if __name__ == "__main__":
    unittest.main()
