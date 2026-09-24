from masm2c.parser import Parser


def test_segment_attribute_keyword_can_be_expression_symbol():
    parser = Parser([])
    source = "DATA SEGMENT\nvalue dw COMMON\nDATA ENDS\nEND\n"

    tree = parser.parse_text(source)
    parser.process_ast(source, tree)


def test_segment_attribute_keyword_can_be_public_symbol():
    parser = Parser([])
    source = "CODE SEGMENT\nPUBLIC CHAIN,COMMON\nEXTRN COMMON:NEAR\nCODE ENDS\nEND\n"

    tree = parser.parse_text(source)
    parser.process_ast(source, tree)


def test_segment_attribute_keyword_can_be_label():
    parser = Parser([])
    source = "CODE SEGMENT\nCOMMON:\nret\nCODE ENDS\nEND\n"

    tree = parser.parse_text(source)
    parser.process_ast(source, tree)
