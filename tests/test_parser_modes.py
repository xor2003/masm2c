import os
import unittest
from unittest.mock import patch

from masm2c.parser import Parser
from masm2c.pgparser import LarkParser


class ParserModesTest(unittest.TestCase):
    def test_parser_engine_defaults_to_lark_postlex(self):
        original_engine = LarkParser._parser_engine
        try:
            LarkParser._parser_engine = None
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(LarkParser._configured_parser_engine(), "postlex")
        finally:
            LarkParser._parser_engine = original_engine

    def test_is_lst_mode_reflects_flag(self):
        parser = Parser([])

        parser.itislst = False
        self.assertFalse(parser.is_lst_mode())

        parser.itislst = True
        self.assertTrue(parser.is_lst_mode())


if __name__ == "__main__":
    unittest.main()
