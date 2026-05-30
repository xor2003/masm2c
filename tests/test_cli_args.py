import unittest

from masm2c.cli import parse_args


class CliArgsTest(unittest.TestCase):
    def test_passes_default_is_int(self):
        args = parse_args(["input.asm"])
        self.assertEqual(args.passes, 2)
        self.assertIsInstance(args.passes, int)

    def test_passes_flag_is_int(self):
        args = parse_args(["--passes", "1", "input.asm"])
        self.assertEqual(args.passes, 1)
        self.assertIsInstance(args.passes, int)


if __name__ == "__main__":
    unittest.main()
