"""Regression: typed stack-frame equates render as scalar displacements.

IDA listings declare locals/args as ``var_4 = byte ptr -4`` /
``arg_0 = dword ptr 6``.  Inside ``[bp+var_4]`` the label must expand to the
constant, not a dereference of ``ds:offset`` — the latter corrupts stack
frames by reading a memory value as the displacement.
"""
from masm2c.cpp import Cpp
from masm2c.parser import Parser


def _cpp_with_assignment(decl: str, name: str) -> Cpp:
    context = Parser([])
    context.test_mode = True
    cpp = Cpp(context, outfile="")
    expr = context.action_assign(
        name,
        context.process_ast(decl, context.parse_text(decl, start_rule="expr")),
        raw=f"{name} = {decl}",
        line_number=1,
    )
    cpp._assignments[name] = expr.value
    return cpp


def test_byte_ptr_negative_offset_renders_scalar():
    cpp = _cpp_with_assignment("byte ptr -4", "var_4")
    assert cpp.convert_label_("var_4") == "(-4)"


def test_word_ptr_negative_offset_renders_scalar():
    cpp = _cpp_with_assignment("word ptr -2", "var_2")
    assert cpp.convert_label_("var_2") == "(-2)"


def test_dword_ptr_positive_arg_renders_scalar():
    cpp = _cpp_with_assignment("dword ptr 6", "arg_0")
    assert cpp.convert_label_("arg_0") == "6"


def test_near_ptr_call_to_data_label_renders_offset_not_deref(tmp_path, monkeypatch):
    """``call near ptr off_X+N`` (opcode E8) is a direct near call.

    IDA renders the computed target as ``data_label+const``; the operand is an
    address expression, not a memory location to dereference.
    """
    listing = tmp_path / "direct_call.lst"
    listing.write_text(
        "cseg10 segment para public 'CODE'\n"
        "cseg10:1000 myproc          proc far\n"
        "cseg10:1001                 call    near ptr off_1010+1\n"
        "cseg10:1004                 retf\n"
        "cseg10:1004 myproc          endp\n"
        "cseg10:1010 off_1010        dd 12345678h\n"
        "cseg10 ends\n"
    )
    from masm2c.cli import process

    monkeypatch.chdir(tmp_path)
    process(str(listing), args={"passes": 1})
    rendered = (tmp_path / "direct_call_cseg10.cpp").read_text()
    assert "*(dw*)(((db*)&off_1010)" not in rendered
    assert "offset(cseg10,off_1010)+1" in rendered or "near_offset_external(off_1010)+1" in rendered


def test_hex_literal_ending_in_e_is_parenthesized():
    # 0x0E abutting '+': "bp+0x0E+2" lexes as a pp-number (E+2 = exponent).
    cpp = _cpp_with_assignment("byte ptr 0Eh", "arg_8")
    assert cpp.convert_label_("arg_8") == "(0x0E)"


def test_assignment_equ_renders_scalar_via_op_path():
    context = Parser([])
    cpp = Cpp(context, outfile="")
    # The op._assignment/_equ branch of convert_label_ renders g.value
    # directly; it must also be forced to a scalar.  (test_mode would short-
    # circuit this branch, so exercise the production path.)
    context.action_assign(
        "var_10",
        context.process_ast("byte ptr -16", context.parse_text("byte ptr -16", start_rule="expr")),
        raw="var_10 = byte ptr -16",
        line_number=1,
    )
    result = cpp.convert_label_("var_10")
    assert "raddr" not in result and "*" not in result, result
