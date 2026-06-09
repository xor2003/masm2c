from pathlib import Path

from masm2c.parser import Parser


def test_struct_instance_line_without_label_after_first_entry(tmp_path: Path) -> None:
    src = tmp_path / 'struct_rows.asm'
    src.write_text(
        """
DATA SEGMENT
REC STRUC
  V DB 0
REC ENDS

Rows REC <1>
     REC <2>
DATA ENDS
END
""".lstrip(),
        encoding='utf-8',
    )

    parser = Parser()
    parser.parse_file(str(src))


def test_ida_inferred_struct_instance_line_without_label_after_first_entry(tmp_path: Path) -> None:
    src = tmp_path / 'ida_struct_rows.asm'
    src.write_text(
        """
DATA SEGMENT
str_24461 struc_0 <6, 9, 49h, 9, offset kb_1957F>
          struc_0 <6, 19h, 49h, 19h, offset kb_1953C>
kb_1957F db 0
kb_1953C db 0
DATA ENDS
END
""".lstrip(),
        encoding='utf-8',
    )

    parser = Parser()
    parser.parse_file(str(src))
