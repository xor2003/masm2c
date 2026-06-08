import unittest

from masm2c.parser import Parser
from masm2c.pgparser import Asm2IR


class ParserStructureRegistryTest(unittest.TestCase):
    def test_structure_registry_api(self):
        parser = Parser([])

        self.assertFalse(parser.has_any_structures())
        self.assertFalse(parser.has_structure("mystruc"))

        parser.declare_structure_name("mystruc")

        self.assertTrue(parser.has_any_structures())
        self.assertTrue(parser.has_structure("mystruc"))

    def test_asm2ir_structname_uses_parser_registry(self):
        parser = Parser([])
        parser.declare_structure_name("abc")
        asm = Asm2IR(parser, "")

        self.assertEqual(asm.structname("abc", 0), "abc")
        self.assertIsNone(asm.structname("zzz", 0))


if __name__ == "__main__":
    unittest.main()
