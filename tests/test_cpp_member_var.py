from masm2c import op
from masm2c.cpp import Cpp
from masm2c.enumeration import IndirectionType
from masm2c.parser import Parser


def test_convert_member_var_promotes_nontrivial_value_expr_to_pointer():
    context = Parser([])
    cpp = Cpp(context, outfile="")
    cpp._expr_state.is_just_label = False
    cpp._expr_state.indirection = IndirectionType.VALUE

    g = op.var(size=8, offset=0, name="waypoints", segment="dseg", elements=4, original_type="waypoint")
    cpp.calculate_member_size = lambda label: 2  # type: ignore[method-assign]

    result = cpp._convert_member_var(g, ["waypoints", "y"])

    assert result == "((db*)waypoints.y)"
    assert cpp._expr_state.indirection == IndirectionType.POINTER
    assert cpp._expr_state.size_changed is True


def test_convert_member_equ_materializes_assignment_alias_before_member_access():
    context = Parser([])
    cpp = Cpp(context, outfile="")
    expr_tree = context.parse_text("word ptr 4", start_rule="expr")
    expr = context.process_ast("word ptr 4", expr_tree)
    assign = context.action_assign("var_8", expr, raw="var_8 = word ptr 4", line_number=1)
    assign.value.original_type = "framestruc"
    cpp._expr_state.is_just_label = False

    result = cpp._convert_member_equ(assign, ["var_8", "_ds"])

    assert result == ""
    assert assign.implemented is True
    assert "#define var_8" in cpp._cmdlabel
    assert cpp._expr_state.struct_type == "framestruc"
    assert cpp._expr_state.need_pointer_to_member == ["var_8", "_ds"]


def test_calculate_member_size_follows_struct_member_alias_chain():
    context = Parser([])
    weapon = op.Struct("weapon", "struct")
    weapon.append(op.Data("wpn_userw1", "dw", op.DataType.NUMBER, [], 1, 2))
    context.symbols.set_global("weapon", weapon)
    context.symbols.set_global(
        "wpn_weapon",
        op.var(size=2, offset=0, name="wpn_weapon", segment="data", elements=1, original_type="weapon"),
    )
    context.action_equ_test("WPN_BOMB_HVEL", "WPN_USERW1")
    context.action_equ_test("WPN_DECOY_HVEL", "WPN_BOMB_HVEL")
    cpp = Cpp(context, outfile="")

    assert cpp.calculate_member_size(["wpn_weapon", "wpn_decoy_hvel"]) == 2
