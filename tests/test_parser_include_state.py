import unittest
from unittest.mock import patch
import hashlib
import os

from masm2c.parser import Parser


class ParserIncludeStateTest(unittest.TestCase):
    @staticmethod
    def _file_hash(path: str) -> str:
        return hashlib.blake2s(os.path.basename(path).encode("utf8")).hexdigest()

    def test_parse_include_restores_current_file_on_success(self):
        parser = Parser([])
        parser._current_file = "root.asm"

        with patch("masm2c.utils.read_whole_file", return_value=""):
            with patch.object(parser, "parse_file_inside", return_value="ok"):
                result = parser.parse_include_file_lines("inc1.inc")

        self.assertEqual(result, "ok")
        self.assertEqual(parser._current_file, "root.asm")

    def test_parse_include_restores_current_file_on_error(self):
        parser = Parser([])
        parser._current_file = "root.asm"

        with patch("masm2c.utils.read_whole_file", return_value=""):
            with patch.object(parser, "parse_file_inside", side_effect=RuntimeError("boom")):
                with self.assertRaises(RuntimeError):
                    parser.parse_include_file_lines("inc1.inc")

        self.assertEqual(parser._current_file, "root.asm")

    def test_nested_includes_restore_lifo_order(self):
        parser = Parser([])
        parser._current_file = "root.asm"

        def fake_parse_file_inside(_text, file_name=None):
            if file_name == "inc1.inc":
                self.assertEqual(parser._current_file, "inc1.inc")
                nested = parser.parse_include_file_lines("inc2.inc")
                self.assertEqual(nested, "inc2.inc")
                self.assertEqual(parser._current_file, "inc1.inc")
                return "inc1.inc"
            if file_name == "inc2.inc":
                self.assertEqual(parser._current_file, "inc2.inc")
                return "inc2.inc"
            raise AssertionError(f"Unexpected include file: {file_name}")

        with patch("masm2c.utils.read_whole_file", return_value=""):
            with patch.object(parser, "parse_file_inside", side_effect=fake_parse_file_inside):
                result = parser.parse_include_file_lines("inc1.inc")

        self.assertEqual(result, "inc1.inc")
        self.assertEqual(parser._current_file, "root.asm")

    def test_parse_include_updates_and_restores_file_hash(self):
        parser = Parser([])
        parser._current_file = "root.asm"
        parser._Parser__current_file_hash = self._file_hash("root.asm")
        root_hash = parser._Parser__current_file_hash

        def fake_parse_file_inside(_text, file_name=None):
            self.assertEqual(file_name, "inc1.inc")
            self.assertEqual(parser._current_file, "inc1.inc")
            self.assertEqual(parser._Parser__current_file_hash, self._file_hash("inc1.inc"))
            return "ok"

        with patch("masm2c.utils.read_whole_file", return_value=""):
            with patch.object(parser, "parse_file_inside", side_effect=fake_parse_file_inside):
                parser.parse_include_file_lines("inc1.inc")

        self.assertEqual(parser._current_file, "root.asm")
        self.assertEqual(parser._Parser__current_file_hash, root_hash)

    def test_parse_file_lines_sets_file_and_hash_for_parse(self):
        parser = Parser([])

        def fake_parse_text(_text, file_name="", start_rule="start"):
            self.assertEqual(file_name, "dir/top.asm")
            self.assertEqual(start_rule, "start")
            self.assertEqual(parser._current_file, "dir/top.asm")
            self.assertEqual(parser._Parser__current_file_hash, self._file_hash("top.asm"))
            return "ast"

        with patch("masm2c.utils.read_whole_file", return_value="mov ax, 1"):
            with patch.object(parser, "parse_text", side_effect=fake_parse_text):
                with patch.object(parser, "process_ast", return_value=None):
                    parser.parse_file_lines("dir/top.asm")

        self.assertEqual(parser._current_file, "dir/top.asm")
        self.assertEqual(parser._Parser__current_file_hash, self._file_hash("top.asm"))


if __name__ == "__main__":
    unittest.main()
