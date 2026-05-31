from pathlib import Path

from masm2c.parser import Parser


def test_keyword_can_be_used_as_label_with_colon(tmp_path: Path) -> None:
    src = tmp_path / 'keyword_label.asm'
    src.write_text(
        """
CODE SEGMENT
Enter:  nop
CODE ENDS
END
""".lstrip(),
        encoding='utf-8',
    )

    parser = Parser()
    parser.parse_file(str(src))
