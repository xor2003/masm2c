from masm2c.parser import Parser


def test_parser_accepts_blank_lines_after_end():
    parser = Parser([])

    tree = parser.parse_text(parser._trim_trailing_lines_after_end("END\n\n"))

    assert tree is not None


def test_parser_accepts_dos_eof_after_end():
    parser = Parser([])

    tree = parser.parse_text(parser._trim_trailing_lines_after_end("END\n\n\x1a\n"))

    assert tree is not None
