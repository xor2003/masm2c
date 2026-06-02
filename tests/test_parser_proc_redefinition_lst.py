import unittest

from masm2c import op
from masm2c.parser import Parser
from masm2c.proc import Proc


class ParserProcRedefinitionLstTest(unittest.TestCase):
    def test_add_proc_allows_lst_pass1_label_to_proc_upgrade(self):
        parser = Parser([])
        parser.pass_number = 1
        parser.itislst = True
        parser.symbols.set_pass_info(1, False)
        parser.create_segment("_TEXT")
        parser.proc = None

        parser.symbols.set_global(
            "RestoreInt9Handler",
            op.label("restoreint9handler", proc="mainproc", line_number=1),
        )

        result = parser.add_proc("restoreint9handler", "restoreInt9Handler proc far", 2, True)

        self.assertIsInstance(result, Proc)
        self.assertIs(parser.symbols.get_global("restoreint9handler"), result)
        self.assertTrue(result.far)


if __name__ == "__main__":
    unittest.main()
