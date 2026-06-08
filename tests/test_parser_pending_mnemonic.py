import unittest

from masm2c.parser import Parser


class ParserPendingMnemonicTest(unittest.TestCase):
    def test_pending_mnemonic_set_consume(self):
        parser = Parser([])

        parser.set_pending_mnemonic("mov")
        self.assertEqual(parser.consume_pending_mnemonic(), "mov")
        self.assertEqual(parser.consume_pending_mnemonic(), "")


if __name__ == "__main__":
    unittest.main()
