import unittest

from masm2c.parser import Parser


class ParserLabelRedefinitionTest(unittest.TestCase):
    def test_action_label_allows_local_redefinition_in_pass1(self):
        parser = Parser([])
        parser.pass_number = 1
        parser.symbols.set_pass_info(1, False)
        parser.make_sure_proc_exists(1, "")

        parser.action_label("_skip", raw="", globl=False, line_number=1)
        parser.action_label("_skip", raw="", globl=False, line_number=2)

        symbol = parser.symbols.get_global("_skip")
        self.assertIsNotNone(symbol)


if __name__ == "__main__":
    unittest.main()
