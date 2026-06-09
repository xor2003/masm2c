from pathlib import Path
from types import MethodType

from masm2c.cpp import Cpp
from masm2c.parser import Parser


def test_lst_source_writes_procedures_to_segment_files_after_mode_restore(tmp_path: Path, monkeypatch) -> None:
    parser = Parser({"mergeprocs": "separate"})
    parser.proc_list = ["first", "second"]
    parser.itislst = False
    parser.source_is_lst = True

    cpp = Cpp(parser, outfile="sample")

    def render_procedure(self: Cpp, name: str) -> tuple[str, str]:
        segment = "seg000" if name == "first" else "seg001"
        return f"bool {name}() {{ return true; }}", segment

    monkeypatch.setattr(cpp, "_render_procedure", MethodType(render_procedure, cpp))
    monkeypatch.chdir(tmp_path)

    inline_text = cpp.write_procedures("/* banner */\n", "sample.h")

    assert inline_text == ""
    assert (tmp_path / "sample_seg000.cpp").read_text(encoding="cp437").count("bool first()") == 1
    assert (tmp_path / "sample_seg001.cpp").read_text(encoding="cp437").count("bool second()") == 1
    assert parser.itislst is False
