import unittest

from masm2c.cli import parse_args, should_merge_data_segments


class CliArgsTest(unittest.TestCase):
    def test_passes_default_is_int(self):
        args = parse_args(["input.asm"])
        self.assertEqual(args.passes, 2)
        self.assertIsInstance(args.passes, int)

    def test_passes_flag_is_int(self):
        args = parse_args(["--passes", "1", "input.asm"])
        self.assertEqual(args.passes, 1)
        self.assertIsInstance(args.passes, int)

    def test_single_listing_conversion_does_not_merge_data_segments(self):
        self.assertFalse(should_merge_data_segments(["game.lst"]))

    def test_mixed_multi_module_conversion_merges_data_segments(self):
        self.assertTrue(should_merge_data_segments(["main.asm", "overlay.lst"]))


if __name__ == "__main__":
    unittest.main()
