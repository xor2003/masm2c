import unittest

from masm2c import op
from masm2c.parser import Parser


class ParserSymbolLookupTest(unittest.TestCase):
    def test_lookup_global_symbol_marks_usage(self):
        parser = Parser([])
        parser.symbols.set_global("foo", op.var(size=1, offset=0, name="foo", segment="_data", elements=1))

        found = parser.lookup_global_symbol("foo")

        self.assertIsNotNone(found)
        self.assertEqual(found.name, "foo")

    def test_lookup_mangled_symbol(self):
        parser = Parser([])
        parser.symbols.set_global("aarbb", op.var(size=1, offset=0, name="a@b", segment="_data", elements=1))

        found = parser.lookup_mangled_symbol("a@b")

        self.assertIsNotNone(found)
        self.assertEqual(found.name, "a@b")


if __name__ == "__main__":
    unittest.main()
