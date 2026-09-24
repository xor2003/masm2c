import unittest
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from masm2c.cli import (
    collect_shared_equates,
    default_jobs,
    filter_code_symbol_equates,
    parse_args,
    should_merge_data_segments,
    source_files,
)


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

    def test_collect_shared_equates_scans_simple_numeric_assignments(self):
        with TemporaryDirectory() as tmpdir:
            main = Path(tmpdir) / "main.asm"
            sibling = Path(tmpdir) / "sibling.asm"
            main.write_text(
                "NMKEYT=14\n"
                "NMCOMT=4\n"
                "NMPENT=1\n"
                "NMSTRT=4\n"
                "NUMTRP=NMKEYT+NMCOMT+NMPENT+NMSTRT\n"
                "END\n",
                encoding="utf-8",
            )
            sibling.write_text("OTHER = 3 * NUMTRP\nEND\n", encoding="utf-8")

            shared = collect_shared_equates([str(main), str(sibling)], Namespace())

        self.assertEqual(shared["numtrp"], "23")
        self.assertEqual(shared["other"], "69")

    def test_collect_shared_equates_skips_complex_textual_assignments(self):
        with TemporaryDirectory() as tmpdir:
            main = Path(tmpdir) / "main.asm"
            sibling = Path(tmpdir) / "sibling.asm"
            main.write_text("MASK = 1 OR 2\nTEXT EQU <abc>\nEND\n", encoding="utf-8")
            sibling.write_text("OTHER = 4\nEND\n", encoding="utf-8")

            shared = collect_shared_equates([str(main), str(sibling)], Namespace())

        self.assertNotIn("mask", shared)
        self.assertNotIn("text", shared)
        self.assertEqual(shared["other"], "4")

    def test_collect_shared_equates_seeds_from_existing_equates_header(self):
        with TemporaryDirectory() as tmpdir:
            main = Path(tmpdir) / "main.asm"
            sibling = Path(tmpdir) / "sibling.asm"
            header = Path(tmpdir) / "_equates.h"
            main.write_text("TEMPST LABEL WORD\nDB STRSIZ*NUMTMP DUP(?)\nEND\n", encoding="utf-8")
            sibling.write_text("END\n", encoding="utf-8")
            header.write_text(
                "#define strsiz (3)\n"
                "static const int numtmp = (10);\n",
                encoding="utf-8",
            )

            shared = collect_shared_equates([str(main), str(sibling)], Namespace())

        self.assertEqual(shared["strsiz"], "3")
        self.assertEqual(shared["numtmp"], "10")

    def test_collect_shared_equates_source_assignment_overrides_header_seed(self):
        with TemporaryDirectory() as tmpdir:
            main = Path(tmpdir) / "main.asm"
            sibling = Path(tmpdir) / "sibling.asm"
            header = Path(tmpdir) / "_equates.h"
            main.write_text("SIZE = 4\nEND\n", encoding="utf-8")
            sibling.write_text("END\n", encoding="utf-8")
            header.write_text("#define size (3)\n", encoding="utf-8")

            shared = collect_shared_equates([str(main), str(sibling)], Namespace())

        self.assertEqual(shared["size"], "4")

    def test_collect_shared_equates_keeps_header_seed_for_location_counter_assignment(self):
        with TemporaryDirectory() as tmpdir:
            main = Path(tmpdir) / "main.asm"
            sibling = Path(tmpdir) / "sibling.asm"
            header = Path(tmpdir) / "_equates.h"
            main.write_text("RAMLOW = $\nEND\n", encoding="utf-8")
            sibling.write_text("END\n", encoding="utf-8")
            header.write_text("#define ramlow (256)\n", encoding="utf-8")

            shared = collect_shared_equates([str(main), str(sibling)], Namespace())

        self.assertEqual(shared["ramlow"], "256")

    def test_filter_code_symbol_equates_removes_code_export_name(self):
        shared = {"window": "0", "ramlow": "256"}

        filtered = filter_code_symbol_equates(shared, set(), {"window"})

        self.assertEqual(filtered, {"ramlow": "256"})

    def test_collect_shared_equates_uses_last_numeric_assignment(self):
        with TemporaryDirectory() as tmpdir:
            main = Path(tmpdir) / "main.asm"
            sibling = Path(tmpdir) / "sibling.asm"
            main.write_text("STRSIZ = 4\nSTRSIZ = 3\nNUMTMP = 3\nNUMTMP = 10\nEND\n", encoding="utf-8")
            sibling.write_text("TOTAL = STRSIZ * NUMTMP\nEND\n", encoding="utf-8")

            shared = collect_shared_equates([str(main), str(sibling)], Namespace())

        self.assertEqual(shared["strsiz"], "3")
        self.assertEqual(shared["numtmp"], "10")
        self.assertEqual(shared["total"], "30")


if __name__ == "__main__":
    unittest.main()
