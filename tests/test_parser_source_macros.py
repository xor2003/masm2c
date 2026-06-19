from masm2c.parser import Parser


def test_repeat_expands_percent_symbols_and_updates_assignments():
    parser = Parser([])

    out = parser._expand_repeat_blocks("COUNT = 0\nREPT 3\nDB %COUNT\nCOUNT = COUNT+1\nENDM\n")

    assert "DB 0" in out
    assert "DB 1" in out
    assert "DB 2" in out
    assert "COUNT = COUNT+1" not in out


def test_labeled_macro_call_preserves_label_on_first_expanded_line():
    parser = Parser([])
    parser._collect_text_macros_from_content("SETAL MACRO value\nmov al,value\nENDM\n")
    source = parser._strip_text_macro_definitions("SETAL MACRO value\nmov al,value\nENDM\nlabel1: SETAL 6\n")

    out = parser._expand_text_macros(source)

    assert "label1:\tmov al,6" in out


def test_chained_macro_call_splits_before_expansion():
    parser = Parser([])
    parser._collect_text_macros_from_content("TOUCH MACRO value\ninc value\nENDM\n")
    source = parser._strip_text_macro_definitions("TOUCH MACRO value\ninc value\nENDM\nTOUCH ax and TOUCH bx\n")

    out = parser._expand_text_macros(source)

    assert "inc ax" in out
    assert "inc bx" in out


def test_record_instance_rewrites_to_packed_byte_data():
    parser = Parser([])
    content = "HATCH4 RECORD C3:2,C2:2,C1:2,C0:2\npal HATCH4 <0, 1, 2, 3>\n"
    parser._predeclare_structure_names(content)

    out = parser._normalize_struct_instance_rows(content)

    assert "pal DB ((0) * 64) + ((1) * 16) + ((2) * 4) + (3)" in out
