import unittest

from masm2c.parser import Parser


class ParserUnknownMnemonicTest(unittest.TestCase):
    def test_parses_label_like_mnemonic_as_instruction(self):
        parser = Parser([])
        tree = parser.parse_text("SETREGV EGA_SEQ,EGA_SEQ_MAPMSK,00fh\n", start_rule="instruction")
        stmt = parser.process_ast("SETREGV EGA_SEQ,EGA_SEQ_MAPMSK,00fh\n", tree)
        self.assertEqual("setregv", stmt.cmd)


if __name__ == "__main__":
    unittest.main()
