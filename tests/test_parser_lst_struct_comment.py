import unittest

from masm2c.parser import Parser


class ParserLstStructCommentTest(unittest.TestCase):
    def test_predeclare_structure_names_uses_lst_struct_comment_hint(self):
        parser = Parser([])

        parser._predeclare_structure_names("; struct Sam sams[39]\n")

        self.assertTrue(parser.has_structure("sam"))


if __name__ == "__main__":
    unittest.main()
