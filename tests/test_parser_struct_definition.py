import unittest

from masm2c.parser import Parser
from masm2c.op import Struct


class ParserStructDefinitionTest(unittest.TestCase):
    def test_begin_structure_definition_sets_state(self):
        parser = Parser([])

        parser.begin_structure_definition("MYSTRUC", "struc")

        self.assertIsNotNone(parser.current_struct)
        self.assertEqual(parser.current_struct.name, "mystruc")
        self.assertEqual(parser.current_struct.gettype(), Struct.STRUCT)
        self.assertEqual(parser.struct_names_stack[-1], "mystruc")


if __name__ == "__main__":
    unittest.main()
