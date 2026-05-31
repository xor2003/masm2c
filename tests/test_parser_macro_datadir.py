from pathlib import Path

from masm2c.parser import Parser


def test_macro_body_allows_db_directive(tmp_path: Path) -> None:
    src = tmp_path / "macro_db.asm"
    src.write_text(
        """
MyData MACRO
    DB 1,2,3
ENDM

.code
start:
    MyData
END
""".lstrip(),
        encoding="utf-8",
    )

    parser = Parser()
    parser.parse_file(str(src))
