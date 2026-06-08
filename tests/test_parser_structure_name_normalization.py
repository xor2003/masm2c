import unittest

from masm2c.parser import Parser


class ParserStructureNameNormalizationTest(unittest.TestCase):
    def test_begin_structure_definition_normalizes_name(self):
        parser = Parser([])
        parser.begin_structure_definition("MyStruc", "struc")

        self.assertEqual(parser.struct_names_stack[-1], "mystruc")
        assert parser.current_struct is not None
        self.assertEqual(parser.current_struct.name, "mystruc")


if __name__ == "__main__":
    unittest.main()
