import unittest
import os
from unittest.mock import patch

from masm2c.parser import Parser


class ParserIncludePathTest(unittest.TestCase):
    def test_resolve_include_path_relative_to_current_file(self):
        parser = Parser([])
        parser._current_file = "/tmp/project/src/main.asm"

        path = parser.resolve_include_path("inc/macros.inc")

        self.assertEqual(path, os.path.join("/tmp/project/src", "inc/macros.inc"))

    def test_resolve_include_path_normalizes_windows_separators(self):
        parser = Parser([])
        parser._current_file = "/tmp/project/src/main.asm"

        path = parser.resolve_include_path(r"inc\macros.inc")

        self.assertEqual(path, os.path.join("/tmp/project/src", "inc", "macros.inc"))

    def test_resolve_include_path_rooted_include_probes_parent_dirs(self):
        parser = Parser([])
        parser._current_file = "/tmp/project/sub/module/main.asm"
        expected = "/tmp/project/VISUAL/VISDATA.INC"

        with patch("os.path.exists", side_effect=lambda p: p == expected):
            path = parser.resolve_include_path(r"\VISUAL\VISDATA.INC")

        self.assertEqual(path, expected)

    def test_resolve_include_path_windows_drive_style_probes_parent_dirs(self):
        parser = Parser([])
        parser._current_file = "/tmp/project/sub/module/main.asm"
        expected = "/tmp/project/LIB8086/KEYS.INC"

        with patch("os.path.exists", side_effect=lambda p: p == expected):
            path = parser.resolve_include_path(r"C:\LIB8086\KEYS.INC")

        self.assertEqual(path, expected)


if __name__ == "__main__":
    unittest.main()
