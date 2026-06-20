import unittest
from unittest import mock

from masm2c.cli import default_jobs, parse_args, should_merge_data_segments, source_files


class CliArgsTest(unittest.TestCase):
    def test_passes_default_is_int(self):
        args = parse_args(["input.asm"])
        self.assertEqual(args.passes, 2)
        self.assertIsInstance(args.passes, int)

    def test_passes_flag_is_int(self):
        args = parse_args(["--passes", "1", "input.asm"])
        self.assertEqual(args.passes, 1)
        self.assertIsInstance(args.passes, int)

    def test_jobs_flag_is_int(self):
        args = parse_args(["--jobs", "3", "input.asm"])
        self.assertEqual(args.jobs, 3)
        self.assertIsInstance(args.jobs, int)

    def test_jobs_default_is_cpu_count(self):
        with mock.patch.dict("os.environ", {}, clear=True), mock.patch("masm2c.cli.os.cpu_count", return_value=7):
            self.assertEqual(default_jobs(), 7)
            self.assertEqual(parse_args(["input.asm"]).jobs, 7)

    def test_jobs_default_can_be_overridden_by_environment(self):
        with mock.patch.dict("os.environ", {"JOBS": "5"}):
            self.assertEqual(default_jobs(), 5)
            self.assertEqual(parse_args(["input.asm"]).jobs, 5)

    def test_single_listing_conversion_does_not_merge_data_segments(self):
        self.assertFalse(should_merge_data_segments(["game.lst"]))

    def test_mixed_multi_module_conversion_merges_data_segments(self):
        self.assertTrue(should_merge_data_segments(["main.asm", "overlay.lst"]))

    def test_source_files_include_asm_and_lst_only(self):
        self.assertEqual(source_files(["main.asm", "overlay.lst", "data.seg"]), ["main.asm", "overlay.lst"])


if __name__ == "__main__":
    unittest.main()
