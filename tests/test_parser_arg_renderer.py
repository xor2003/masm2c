import unittest

from masm2c.parser import Parser


class _FakeRenderer:
    def __init__(self, _context):
        self.seen = []

    def render_instruction_argument(self, expr, def_size=0, destination=False):
        self.seen.append((expr, def_size, destination))
        return f"FAKE[{def_size}:{int(destination)}]"


class ParserArgRendererTest(unittest.TestCase):
    def test_parse_arg_uses_injected_renderer_factory(self):
        parser = Parser([])
        parser.arg_renderer_factory = _FakeRenderer

        out = parser.parse_arg("1", def_size=2, destination=True)

        self.assertEqual(out, "FAKE[2:1]")

    def test_parse_arg_uses_render_expression_hook(self):
        parser = Parser([])
        parser.render_expression = lambda _expr, def_size=0, destination=False: f"HOOK[{def_size}:{int(destination)}]"

        out = parser.parse_arg("1", def_size=4, destination=False)

        self.assertEqual(out, "HOOK[4:0]")


if __name__ == "__main__":
    unittest.main()
