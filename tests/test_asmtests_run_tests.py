from pathlib import Path

from asmTests.run_tests import generated_cpp_sources


def test_generated_cpp_sources_include_segment_files(tmp_path: Path) -> None:
    for name in ("snake_seg001.cpp", "snake.cpp", "snake_seg000.cpp", "other_seg000.cpp"):
        (tmp_path / name).write_text("", encoding="utf-8")

    assert generated_cpp_sources(tmp_path, "snake") == [
        "snake.cpp",
        "snake_seg000.cpp",
        "snake_seg001.cpp",
    ]
