from pathlib import Path

from masm2c.parser import Parser


def test_macro_parameter_can_be_addr_keyword(tmp_path: Path) -> None:
    src = tmp_path / "macro_addr.asm"
    src.write_text(
        """
M MACRO addr
    DW OFFSET addr
ENDM
END
""".lstrip(),
        encoding="utf-8",
    )

    parser = Parser()
    parser.parse_file(str(src))
