import unittest

from masm2c.parser import Parser


class ParserModesTest(unittest.TestCase):
    def test_is_lst_mode_reflects_flag(self):
        parser = Parser([])

        parser.itislst = False
        self.assertFalse(parser.is_lst_mode())

        parser.itislst = True
        self.assertTrue(parser.is_lst_mode())


if __name__ == "__main__":
    unittest.main()
