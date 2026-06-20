from pathlib import Path

from asmTests.run_tests import generated_cpp_sources, generated_data_sources


def test_generated_cpp_sources_include_segment_files(tmp_path: Path) -> None:
    for name in ("snake_seg001.cpp", "snake.cpp", "snake_seg000.cpp", "other_seg000.cpp"):
        (tmp_path / name).write_text("", encoding="utf-8")

    assert generated_cpp_sources(tmp_path, "snake") == [
        "snake.cpp",
        "snake_seg000.cpp",
        "snake_seg001.cpp",
    ]


def test_generated_data_sources_include_split_reference_files(tmp_path: Path) -> None:
    for name in ("_data_refs_002.cpp", "_data.cpp", "_data_refs_000.cpp"):
        (tmp_path / name).write_text("", encoding="utf-8")

    assert generated_data_sources(tmp_path) == [
        "_data.cpp",
        "_data_refs_000.cpp",
        "_data_refs_002.cpp",
    ]
