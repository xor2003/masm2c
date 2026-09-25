import unittest
import os
from argparse import Namespace
from collections import OrderedDict
from pathlib import Path
from tempfile import TemporaryDirectory

from masm2c import op
from masm2c.cli import collect_code_exports
from masm2c.cpp import Cpp
from masm2c.gen import mangle_asm_labels
from masm2c.parser import Parser
from masm2c.proc import Proc


class ParserExternDistanceTest(unittest.TestCase):
    def test_extrn_far_declares_proc_not_variable(self):
        parser = Parser([])
        tree = parser.parse_text("EXTRN RestoreKbd:FAR\n", start_rule="_directivelist")
        parser.process_ast("EXTRN RestoreKbd:FAR\n", tree)

        self.assertIn("restorekbd", parser.externals_procs)
        self.assertNotIn("restorekbd", parser.externals_vars)
        self.assertTrue(parser.symbols.get_global("restorekbd").far)

    def test_extrn_abs_declares_absolute_symbol_not_storage(self):
        parser = Parser([])
        tree = parser.parse_text("EXTRN MAX_AUTO_HDG:ABS\n", start_rule="_directivelist")
        parser.process_ast("EXTRN MAX_AUTO_HDG:ABS\n", tree)

        self.assertNotIn("max_auto_hdg", parser.externals_vars)
        self.assertIsNone(parser.symbols.get_global("max_auto_hdg"))
        self.assertIn("max_auto_hdg", parser.externals_abs)


class CppDataArraySizeTest(unittest.TestCase):
    def test_char_array_decl_uses_flattened_initializer_size(self):
        data = op.Data(
            "promptdol",
            "db",
            op.DataType.ARRAY_STRING,
            ["cr", "lf", "S", "e", "$"],
            3,
            3,
        )
        value, declaration = Cpp(Parser([])).produce_c_data_array_string(data)

        self.assertEqual(value, "{cr,lf,'S','e','$'}")
        self.assertEqual(declaration, "char promptdol[5]")


class LabelManglingTest(unittest.TestCase):
    def test_main_label_is_mangled_case_insensitively(self):
        self.assertEqual(mangle_asm_labels("Main"), "asmmain")
        self.assertEqual(Cpp(Parser([])).mangle_label("Main"), "asmmain")

    def test_cpp_keyword_label_is_mangled(self):
        self.assertEqual(mangle_asm_labels("delete"), "asm_delete")
        self.assertEqual(Cpp(Parser([])).mangle_label("Delete"), "asm_delete")
        self.assertEqual(Parser.mangle_label("Delete"), "asm_delete")

    def test_c_runtime_name_label_is_mangled(self):
        self.assertEqual(mangle_asm_labels("tan"), "asm_tan")
        self.assertEqual(Cpp(Parser([])).mangle_label("TAN"), "asm_tan")
        self.assertEqual(Parser.mangle_label("TAN"), "asm_tan")
        self.assertEqual(mangle_asm_labels("alarm"), "asm_alarm")
        self.assertEqual(Cpp(Parser([])).mangle_label("Alarm"), "asm_alarm")
        self.assertEqual(Parser.mangle_label("Alarm"), "asm_alarm")


class ProcRawCommentTest(unittest.TestCase):
    def test_multiline_raw_line_is_emitted_as_one_cpp_comment(self):
        from masm2c.proc import Proc

        parser = Parser([])
        cpp = Cpp(parser)
        proc = Proc("mainproc")
        stmt = proc.create_instruction_object("cld", [])
        stmt.raw_line = "first\n; second"
        stmt.line_number = 9
        proc.stmts.append(stmt)

        proc.visit(cpp)

        self.assertIn("// 9 first ; second", cpp.body)
        self.assertNotIn("\n; second", cpp.body)

class MasmOperatorRenderingTest(unittest.TestCase):
    def test_not_hex_keeps_valid_c_integer(self):
        parser = Parser([])
        self.assertEqual(parser.parse_arg("NOT 008h"), "~0x008")

    def test_data_and_expression_preserves_operator(self):
        parser = Parser([])
        source = (
            "EVEN_HATCH EQU 1010b\n"
            "DATA SEGMENT\n"
            "x db 00001111b AND EVEN_HATCH\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        data = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "x")

        value, declaration, size = Cpp(parser).produce_c_data_single_(data)

        self.assertEqual(value, "15 & even_hatch")
        self.assertEqual(declaration, "db x")
        self.assertEqual(size, 1)


class CppDataInitTest(unittest.TestCase):
    def test_empty_data_initializer_does_not_emit_invalid_assignment(self):
        cpp = Cpp(Parser([]))

        self.assertEqual(cpp._build_data_assignment("dummyc_3f0", "", "dw tmp999", False), "")

    def test_empty_dummy_data_does_not_emit_declaration_or_reference(self):
        data = op.Data("dummyc_5f0", "dw", op.DataType.NUMBER, [], 1, 2)
        cpp = Cpp(Parser([]))

        self.assertEqual(
            cpp._render_data_assignment_and_refs(data, "", "dw dummyc_5f0;\n"),
            ("", "", "", ""),
        )

    def test_data_current_location_symbol_uses_record_offset(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "target dw 0\n"
            "rel dw OFFSET target - $ - 2\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        rel = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "rel")

        value, declaration, size = Cpp(parser).produce_c_data_single_(rel)

        self.assertEqual(value, "offset(data,target)-2-2")
        self.assertEqual(declaration, "dw rel")
        self.assertEqual(size, 2)

    def test_macro_if_decimal_suffix_reserves_distinct_storage(self):
        source = (
            "DSEG SEGMENT PUBLIC 'DATASG'\n"
            "R MACRO NAME,SIZE\n"
            "    PUBLIC NAME\n"
            "NAME LABEL WORD\n"
            "IF SIZE\n"
            "    DB SIZE DUP(?)\n"
            "ENDIF\n"
            "ENDM\n"
            "    R MSWSIZ,2D\n"
            "    R MSWFLG,1D\n"
            "    R CSWSIZ,2D\n"
            "DSEG ENDS\n"
            "END\n"
        )
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "macro_if_decimal.asm"
            path.write_text(source, encoding="utf-8")
            parser = Parser([])
            parser.parse_file(str(path))
        segment_data = parser.segments["dseg"].getdata()
        aliases = {alias.name: alias for alias in parser.data_aliases}

        self.assertEqual(
            [(data.offset, data.size) for data in segment_data],
            [
                (0, 2),
                (2, 1),
                (3, 2),
            ],
        )
        self.assertEqual(aliases["mswsiz"].offset, 0)
        self.assertEqual(aliases["mswflg"].offset, 2)
        self.assertEqual(aliases["cswsiz"].offset, 3)

    def test_macro_dup_reservation_can_use_shared_equate_count(self):
        source = (
            "DSEG SEGMENT PUBLIC 'DATASG'\n"
            "R MACRO NAME,SIZE\n"
            "    PUBLIC NAME\n"
            "NAME LABEL WORD\n"
            "IF SIZE\n"
            "    DB SIZE DUP(?)\n"
            "ENDIF\n"
            "ENDM\n"
            "    R TRPTBL,3*NUMTRP\n"
            "    R ONGSBF,1\n"
            "DSEG ENDS\n"
            "END\n"
        )
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "macro_shared_equ.asm"
            path.write_text(source, encoding="utf-8")
            parser = Parser({"shared_equates": {"numtrp": "14+4+1+4"}})
            parser.parse_file(str(path))

        segment_data = parser.segments["dseg"].getdata()
        aliases = {alias.name: alias for alias in parser.data_aliases}

        self.assertEqual([(data.offset, data.size) for data in segment_data], [(0, 69), (69, 1)])
        self.assertEqual(aliases["trptbl"].offset, 0)
        self.assertEqual(aliases["ongsbf"].offset, 69)

    def test_local_label_can_override_shared_equate_seed(self):
        source = (
            "CODE SEGMENT\n"
            "STPTRP:\n"
            "ret\n"
            "CODE ENDS\n"
            "END\n"
        )
        parser = Parser({"shared_equates": {"stptrp": "7"}})
        parser.process_ast(source, parser.parse_text(source))

        self.assertIsInstance(parser.symbols.get_global("stptrp"), op.label)

    def test_even_directive_advances_data_symbol_offset(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "bytestr db 65,66,0\n"
            "EVEN\n"
            "table dw 1234h\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        segment_data = parser.segments["data"].getdata()

        self.assertEqual([(data.label, data.offset, data.size) for data in segment_data], [
            ("bytestr", 0, 3),
            ("dummy0_data_3", 3, 1),
            ("table", 4, 2),
        ])
        self.assertEqual(parser.symbols.get_global("table").offset, 4)

    def test_external_offset_in_data_initializer_does_not_use_register_state(self):
        parser = Parser([])
        source = (
            "EXTRN PolyCount:WORD\n"
            "DATA SEGMENT\n"
            "rel dw OFFSET PolyCount\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        rel = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "rel")

        value, declaration, size = Cpp(parser).data(rel)

        self.assertEqual(value, "offset(default_seg,polycount), // rel\n")
        self.assertEqual(declaration, "dw rel;\n")
        self.assertEqual(size, 2)

    def test_seg_operator_uses_symbol_segment_not_symbol_value(self):
        parser = Parser([])
        parser.symbols.set_global("prog_end", op.var(size=1, offset=0, name="prog_end", segment="stack"))

        rendered = parser.parse_arg("SEG PROG_END")

        self.assertEqual(rendered, "seg_offset(stack)")

    def test_seg_operator_for_external_symbol_uses_linked_reference_address(self):
        parser = Parser([])
        parser.symbols.set_global("prog_end", op.var(size=1, offset=0, name="prog_end", segment="default_seg", external=True))

        rendered = parser.parse_arg("SEG PROG_END")

        self.assertEqual(rendered, "m2c::segment_of_external(prog_end)")

    def test_seg_operator_for_code_label_uses_label_segment(self):
        parser = Parser([])
        source = (
            "_TEXT SEGMENT\n"
            "main PROC\n"
            "GameIntr20:\n"
            "mov dx, SEG GameIntr20\n"
            "ret\n"
            "main ENDP\n"
            "_TEXT ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = Proc("main").generate_c_cmd(Cpp(parser), parser.action_code("mov dx, SEG GameIntr20"))

        self.assertEqual(rendered, "dx = seg_offset(_text);")

    def test_struct_initializer_empty_fields_render_as_zero(self):
        parser = Parser([])
        source = (
            "VEHICLE STRUCT\n"
            "VA DW 0\n"
            "VB DW 0\n"
            "VC DW 0\n"
            "VD DW 0\n"
            "VEHICLE ENDS\n"
            "DATA SEGMENT\n"
            "row VEHICLE <1,,,4>\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        row = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "row")

        value, declaration, size = Cpp(parser).produce_c_data_single_(row)

        self.assertEqual(value, "{1,0,0,4}")
        self.assertEqual(declaration, "vehicle row")
        self.assertEqual(size, 8)

    def test_struct_member_array_extent_and_string_initializer_are_valid_c(self):
        parser = Parser([])
        source = (
            "MODEL STRUCT\n"
            "MOD_FILENAME DB 8 DUP (' ')\n"
            "MOD_CAT DW 0\n"
            "MODEL ENDS\n"
            "DATA SEGMENT\n"
            "gr4 MODEL <\"GR4_1\",2>\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        gr4 = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "gr4")
        cpp = Cpp(parser)

        structures = cpp.produce_structures(parser.structures)
        value, declaration, size = cpp.produce_c_data_single_(gr4)

        self.assertIn("db mod_filename[8];", structures)
        self.assertEqual(value, "{{'G','R','4','_','1'},2}")
        self.assertEqual(declaration, "model gr4")
        self.assertEqual(size, 10)

    def test_struct_name_that_conflicts_with_c_runtime_uses_tagged_type(self):
        parser = Parser([])
        source = (
            "CLOCK STRUCT\n"
            "CLK_HRS DB 0\n"
            "CLOCK ENDS\n"
            "DATA SEGMENT\n"
            "clock24 CLOCK <0>\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        clock24 = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "clock24")
        cpp = Cpp(parser)

        value, declaration, _ = cpp.produce_c_data_single_(clock24)
        rendered = cpp._render_data_assignment_and_refs(clock24, value, f"{declaration};\n")

        self.assertEqual(declaration, "struct clock clock24")
        self.assertIn("struct clock tmp999={0};", rendered[0])
        self.assertIn("extern struct clock& clock24;", rendered[2])

    def test_struct_name_that_conflicts_with_data_label_uses_tagged_type(self):
        parser = Parser([])
        landing = op.Struct("landing", "struct")
        member = op.Data("lnd_decel", "dw", op.DataType.NUMBER, [0], 1, 2)
        landing.append(member)
        parser.structures["landing"] = landing
        parser.segments["default_seg"].append(op.Data("landing", "db", op.DataType.NUMBER, [0], 1, 1))
        landing1 = op.Data("landing1", "landing", op.DataType.OBJECT, [0], 1, 2)
        landing1.setmembers([member])

        _, declaration, _ = Cpp(parser).produce_c_data_single_(landing1)

        self.assertEqual(declaration, "struct landing landing1")

    def test_db_expression_array_is_not_split_into_character_tokens(self):
        parser = Parser([])
        source = (
            "DAM_HARD4 EQU 1\n"
            "DAM_DEBRIS1 EQU 2\n"
            "DATA SEGMENT\n"
            "flags DB DAM_HARD4+DAM_DEBRIS1\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        flags = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "flags")

        value, declaration, size = Cpp(parser).produce_c_data_single_(flags)

        self.assertEqual(value, "dam_hard4+dam_debris1")
        self.assertEqual(declaration, "db flags")
        self.assertEqual(size, 1)

    def test_single_character_db_struct_fields_are_quoted(self):
        parser = Parser([])
        source = (
            "KERN STRUCT\n"
            "FIRST DB 0\n"
            "SECOND DB 0\n"
            "ADJUST DB 0\n"
            "KERN ENDS\n"
            "DATA SEGMENT\n"
            "row KERN <'L','T',5>\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        row = next(d for segment in parser.segments.values() for d in segment.getdata() if d.label == "row")

        value, declaration, size = Cpp(parser).produce_c_data_single_(row)

        self.assertEqual(value, "{'L','T',5}")
        self.assertEqual(declaration, "kern row")
        self.assertEqual(size, 3)

    def test_duplicate_named_data_segments_are_concatenated_during_seg_merge(self):
        first = op.Segment("data", 0)
        first.append(op.Data("first", "dw", op.DataType.NUMBER, [1], 1, 2))
        second = op.Segment("data", 0)
        second.append(op.Data("second", "dw", op.DataType.NUMBER, [2], 1, 2))
        cpp = Cpp(Parser([]))

        segments, _ = cpp.merge_segments(OrderedDict([("data", first)]), OrderedDict(), OrderedDict([("data", second)]), OrderedDict())

        self.assertEqual([data.label for data in segments["data"].getdata()], ["first", "second"])
        self.assertEqual(segments["data"].getsize(), 4)

    def test_public_segment_class_merge_preserves_segment_alias_offsets(self):
        first = op.Segment("data", 0, options={"public"}, segclass="data")
        first.append(op.Data("first", "dw", op.DataType.NUMBER, [1], 1, 2))
        second = op.Segment("data", 0, options={"public"}, segclass="data")
        second.append(op.Data("weaponlist", "dw", op.DataType.NUMBER, [2], 1, 2))
        cpp = Cpp(Parser([]), merge_data_segments=True)

        segments, _ = cpp.merge_segments(OrderedDict([("data", first)]), OrderedDict(), OrderedDict([("data", second)]), OrderedDict())

        self.assertEqual([data.label for data in segments["data"].getdata()], ["first", "weaponlist"])
        self.assertEqual(segments["data"].getdata()[1].offset, 2)

    def test_public_data_segment_class_storage_is_laid_out_after_code(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                code = op.Segment("cseg", 0, options={"public"}, segclass="codesg")
                code.append(op.Data("opcode_table", "db", op.DataType.ARRAY, [0] * 0x21, 0x21, 0x21))
                data = op.Segment("dseg", 0, options={"public"}, segclass="datasg")
                data.append(op.Data("begdsg", "dw", op.DataType.NUMBER, [0], 1, 2))

                writer = Cpp(Parser([]))
                writer.write_segment_file(OrderedDict([("cseg", code)]), OrderedDict(), "CODE.ASM")
                writer.write_segment_file(OrderedDict([("dseg", data)]), OrderedDict(), "DATA.ASM")

                segments, _ = Cpp(Parser([]), merge_data_segments=True).read_segment_files(["CODE.ASM", "DATA.ASM"])

                self.assertEqual(segments["codesg"].offset, 0)
                self.assertEqual(segments["dseg"].offset, 0x30)
            finally:
                os.chdir(old_cwd)

    def test_merged_public_segment_data_references_use_relocated_linear_offsets(self):
        first = op.Segment("data", 0, options={"public"}, segclass="data")
        first.append(op.Data("first", "dw", op.DataType.NUMBER, [1], 1, 2))
        second = op.Segment("data", 0, options={"public"}, segclass="data")
        second.append(op.Data("palette", "db", op.DataType.ARRAY, [1, 2, 3], 3, 3))
        cpp = Cpp(Parser([]), merge_data_segments=True)

        segments, _ = cpp.merge_segments(
            OrderedDict([("data", first)]),
            OrderedDict(),
            OrderedDict([("data", second)]),
            OrderedDict(),
        )
        _, _, data_cpp, _ = cpp.render_data_c(segments)

        self.assertIn("db (& palette)[3] = *((db (*)[3])(&data+0x2));", data_cpp)

    def test_duplicate_public_segment_data_offsets_are_relocated_during_merge(self):
        first = op.Segment("data", 0, options={"public"}, segclass="data")
        first.append(op.Data("jumpinitlist", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0x14A))
        second = op.Segment("data", 0, options={"public"}, segclass="data")
        second.append(op.Data("gameplaydata", "db", op.DataType.ARRAY, [0], 1, 1, offset=0x180))
        cpp = Cpp(Parser([]), merge_data_segments=True)

        segments, _ = cpp.merge_segments(OrderedDict([("data", first)]), OrderedDict(), OrderedDict([("data", second)]), OrderedDict())

        self.assertEqual(segments["data"].getdata()[1].offset, 0x2CC)

    def test_public_segment_merge_uses_extent_not_record_size(self):
        first = op.Segment("paldata", 0, options={"public"}, segclass="data")
        first.append(op.Data("vga_infra_red", "db", op.DataType.ARRAY, [0], 104, 104, offset=0xA42))
        second = op.Segment("paldata", 0, options={"public"}, segclass="data")
        second.append(op.Data("rotateswitch", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0x8E))
        cpp = Cpp(Parser([]), merge_data_segments=True)

        segments, _ = cpp.merge_segments(
            OrderedDict([("paldata", first)]),
            OrderedDict(),
            OrderedDict([("paldata", second)]),
            OrderedDict(),
        )

        self.assertEqual(segments["paldata"].getdata()[1].offset, 0xB38)

    def test_duplicate_public_segment_label_aliases_are_relocated_when_reading_sidecars(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                first = op.Segment("data", 0, options={"public"}, segclass="data")
                first.append(op.Data("jumpinitlist", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0x14A))
                second = op.Segment("data", 0, options={"public"}, segclass="data")
                second.append(op.Data("tail", "db", op.DataType.NUMBER, [0], 1, 1, offset=0x180))
                Cpp(Parser([])).write_segment_file(OrderedDict([("data", first)]), OrderedDict(), "COM_DRVR.ASM", [])
                Cpp(Parser([])).write_segment_file(
                    OrderedDict([("data", second)]),
                    OrderedDict(),
                    "MAINDATA.ASM",
                    [op.var(1, 0x180, "gameplaydata", segment="data", elements=1, original_type="byte")],
                )

                merger = Cpp(Parser([]), merge_data_segments=True)
                merger.read_segment_files(["COM_DRVR.ASM", "MAINDATA.ASM"])

                alias = merger._context.data_aliases[0]
                self.assertEqual(alias.segment, "data")
                self.assertEqual(alias.offset, 0x2CC)
            finally:
                os.chdir(old_cwd)

    def test_data_alias_from_merged_segment_alias_is_rendered(self):
        parser = Parser([])
        segment = op.Segment("data", 0)
        segment.segment_aliases["wpndata"] = 2
        parser.segments = OrderedDict([("data", segment)])
        parser.data_aliases = [
            op.var(2, 0, "weaponlist", segment="wpndata", elements=1, original_type="word"),
            op.var(2, 4, "canonical_weapon", segment="data", elements=1, original_type="word"),
        ]

        _, _, data_cpp, hpp = Cpp(parser).render_data_c(parser.segments)

        self.assertIn("db& data=*((db*)&m2c::m+0x0);", data_cpp)
        self.assertIn("db& wpndata=*((db*)&m2c::m+0x2);", data_cpp)
        self.assertIn("word& weaponlist=*((word*)(&wpndata+0x0));", data_cpp)
        self.assertIn("word& canonical_weapon=*((word*)(&data+0x4));", data_cpp)
        self.assertIn("extern word& weaponlist;", hpp)
        self.assertIn("extern word& canonical_weapon;", hpp)

    def test_rinit_macro_call_registers_data_alias(self):
        parser = Parser([])
        source = """DATA SEGMENT PUBLIC 'DATA'
RINIT F_EDIT,1
DB 0
DATA ENDS
END
"""
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        aliases = {alias.name: alias for alias in parser.data_aliases}
        self.assertIn("f_edit", aliases)
        self.assertEqual(aliases["f_edit"].offset, 0)
        self.assertEqual(aliases["f_edit"].original_type, "word")

    def test_rinit_inside_expanded_macro_registers_data_alias(self):
        source = """DATA SEGMENT PUBLIC 'DATA'
RINIT MACRO NAME,SIZE
PUBLIC NAME
NAME LABEL WORD
ENDM
PDIRAM MACRO
RINIT KEYSW,1
DB 0
ENDM
PDIRAM
DATA ENDS
END
"""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nested_rinit.asm"
            path.write_text(source)
            parser = Parser([])
            parser.parse_file(str(path))

        aliases = {alias.name: alias for alias in parser.data_aliases}
        self.assertIn("keysw", aliases)
        self.assertEqual(aliases["keysw"].offset, 0)
        self.assertEqual(aliases["keysw"].original_type, "word")

    def test_duplicate_data_alias_names_are_renamed_for_aggregate_data(self):
        first = op.var(1, 0x10, "setupdol", segment="data", original_type="byte", filename="A.ASM")
        second = op.var(1, 0x20, "setupdol", segment="data", original_type="byte", filename="B.ASM")

        aliases = Cpp(Parser([]))._deduplicate_data_alias_names([first, second])

        self.assertEqual(aliases[0].name, "setupdol")
        self.assertEqual(aliases[1].name, "setupdol__b_data_20")

    def test_duplicate_memory_field_labels_are_renamed_in_aggregate_data(self):
        segment = op.Segment("data", 0)
        segment.append(op.Data("local", "dw", op.DataType.NUMBER, [1], 1, 2, filename="A.ASM", line_number=10))
        segment.append(op.Data("local", "dw", op.DataType.NUMBER, [2], 1, 2, filename="B.ASM", line_number=20))
        cpp = Cpp(Parser([]))

        segments = cpp._deduplicate_memory_field_labels(OrderedDict([("data", segment)]))

        labels = [data.label for data in segments["data"].getdata()]
        self.assertEqual(labels[0], "local")
        self.assertEqual(labels[1], "local__b_0_20")
        self.assertEqual(cpp._data_label_renames, [("M2C_MODULE_B", "local", "local__b_0_20")])

    def test_duplicate_memory_field_label_renames_are_emitted_for_modules(self):
        with TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                segment = op.Segment("data", 0)
                segment.append(op.Data("localref", "dw", op.DataType.NUMBER, [1], 1, 2, filename="A.ASM", line_number=10))
                segment.append(op.Data("localref", "dw", op.DataType.NUMBER, [2], 1, 2, filename="B.ASM", line_number=20))
                cpp = Cpp(Parser([]), outfile="b")

                cpp.write_data_segments_cpp(OrderedDict([("data", segment)]), OrderedDict())

                renames = Path("_data_renames.h").read_text(encoding="utf-8")
                data_cpp = Path("_data.cpp").read_text(encoding="utf-8")
                data_refs = Path("_data_refs_000.cpp").read_text(encoding="utf-8")
                data_h = Path("_data.h").read_text(encoding="utf-8")
                data_types = Path("_data_types.h").read_text(encoding="utf-8")
                self.assertIn("#if defined(M2C_MODULE_B)", renames)
                self.assertIn("#define localref localref__b_0_20", renames)
                self.assertIn('#include "_data.h"', data_cpp)
                self.assertNotIn("localref = m2c::m.localref", data_cpp)
                self.assertIn('#include "_data.h"', data_refs)
                self.assertIn("dw& localref = *((dw*)(&data+0x0));", data_refs)
                self.assertIn("extern dw& localref;", data_h)
                self.assertIn('#include "_data_types.h"', data_h)
                self.assertIn('#include "asm.h"', data_types)
                self.assertIn("#define M2C_MODULE_B 1", cpp._module_data_rename_header())
                self.assertIn('#include "_data_renames.h"', cpp._module_data_rename_header())
            finally:
                os.chdir(cwd)

    def test_external_data_offset_uses_linked_reference_address(self):
        external = op.var(1, 0xA042, "pilotpanel", segment="default_seg", external=True, original_type="byte")

        rendered = Cpp(Parser([])).convert_member_offset(external, ["pilotpanel"])

        self.assertEqual(rendered, "m2c::near_offset_external(pilotpanel)")

    def test_external_data_offset_initializer_does_not_use_register_state(self):
        external = op.var(1, 0xA042, "pilotpanel", segment="default_seg", external=True, original_type="byte")
        cpp = Cpp(Parser([]))
        cpp._expr_state.data_label_size = 2

        rendered = cpp.convert_member_offset(external, ["pilotpanel"])

        self.assertEqual(rendered, "offset(default_seg,pilotpanel)")

    def test_external_offset_loaded_into_dx_is_pure_offset_value(self):
        parser = Parser([])
        parser.add_extern("PilotPanel", "BYTE")
        rendered = Proc("mainproc").generate_c_cmd(Cpp(parser), parser.action_code("mov dx, OFFSET PilotPanel"))

        self.assertEqual(rendered, "dx = m2c::near_offset_external(pilotpanel);")

    def test_external_proc_offset_is_available_to_indirect_dispatch(self):
        source = (
            "CSEG segment public 'CODE'\n"
            "EXTRN $FLGOC:NEAR,INTXT:NEAR\n"
            "MOV SI,OFFSET $FLGOC\n"
            "MOV BX,OFFSET INTXT\n"
            "CSEG ends\n"
            "END\n"
        )
        with TemporaryDirectory() as tmp:
            asm = Path(tmp) / "extern_offset.asm"
            asm.write_text(source, encoding="ascii")
            parser = Parser([])
            parser.parse_file_lines(str(asm))

            dispatch = Cpp(parser).produce_global_jump_table(parser.symbols.get_globals().items(), False)

        self.assertIn("dolflgoc", parser.extern_code_refs)
        self.assertNotIn("intxt", parser.extern_code_refs)
        self.assertIn("case m2c::kdolflgoc:", dispatch)
        self.assertNotIn("case m2c::kintxt:", dispatch)

    def test_external_dx_offset_does_not_restore_ds_after_following_call(self):
        parser = Parser([])
        parser.add_extern("PilotPanel", "BYTE")
        parser.add_extern("LoadFile", "FAR")
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov dx, OFFSET PilotPanel\n"
            "call LoadFile\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        proc.visit(cpp)

        self.assertIn("R(dx = m2c::near_offset_external(pilotpanel););", cpp.body)
        self.assertIn("J(CALLF(loadfile,0));", cpp.body)
        self.assertNotIn("restore_external_offset_ds(ds)", cpp.body)

    def test_linked_data_offset_does_not_change_ds_before_following_call(self):
        parser = Parser({"mergeprocs": "separate", "filenames": ["a.asm", "b.asm"]})
        parser.add_extern("PrintText", "NEAR")
        source = (
            "DATA SEGMENT\n"
            "Message db 'READY',0\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov bx, OFFSET Message\n"
            "call PrintText\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        proc.visit(cpp)

        self.assertIn("R(bx = m2c::near_offset_external(message););", cpp.body)
        self.assertIn("J(CALL(printtext,0));", cpp.body)
        self.assertNotIn("restore_data_offset_ds(ds)", cpp.body)

    def test_external_offset_instruction_keeps_ds_for_independent_filename_pointer(self):
        parser = Parser([])
        parser.add_extern("GamePlayData", "BYTE")
        source = (
            "DATA SEGMENT\n"
            "GamePlayIn db 'GAMEPLAY.IN',0\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov dx, OFFSET GamePlayIn\n"
            "mov di, OFFSET GamePlayData\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("dx = offset(data,gameplayin);", rendered)
        self.assertIn("di = m2c::near_offset_external(gameplaydata);", rendered)
        self.assertNotIn("near_offset_external(gameplaydata, ds)", rendered)

    def test_external_offset_loaded_into_si_is_pure_offset_value(self):
        parser = Parser([])
        parser.add_extern("CopyBuffer", "BYTE")

        rendered = Proc("mainproc").generate_c_cmd(Cpp(parser), parser.action_code("mov si, OFFSET CopyBuffer"))

        self.assertEqual(rendered, "si = m2c::near_offset_external(copybuffer);")

    def test_internal_offset_in_multi_source_translation_uses_linked_offset_value(self):
        parser = Parser({"mergeprocs": "separate", "filenames": ["polyfill.asm", "horizon.asm"]})
        source = (
            "DATA SEGMENT\n"
            "Octant dw 0\n"
            "OctantBase dw 0\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov ax, OFFSET Octant\n"
            "mov OctantBase, ax\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("ax = m2c::near_offset_external(octant);", rendered)
        self.assertIn("octantbase = ax;", rendered)

    def test_internal_dx_offset_in_multi_source_translation_does_not_change_ds(self):
        parser = Parser({"mergeprocs": "separate", "filenames": ["polyfill.asm", "horizon.asm"]})
        source = (
            "DATA SEGMENT\n"
            "Buf db 32 dup (0)\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov dx, OFFSET Buf\n"
            "mov al, [bx]\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("dx = m2c::near_offset_external(buf);", rendered)
        self.assertNotIn("near_offset_external_for_ds_arg(buf, ds)", rendered)
        self.assertNotIn("near_offset_data(buf, ds)", rendered)

    def test_internal_si_offset_in_multi_source_translation_does_not_change_ds(self):
        parser = Parser({"mergeprocs": "separate", "filenames": ["polyfill.asm", "horizon.asm"]})
        source = (
            "DATA SEGMENT\n"
            "Buf db 32 dup (0)\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov si, OFFSET Buf\n"
            "lodsb\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("si = m2c::near_offset_external(buf);", rendered)
        self.assertNotIn("near_offset_data(buf, ds)", rendered)

    def test_internal_seg_in_multi_source_translation_uses_linked_symbol_segment(self):
        parser = Parser({"mergeprocs": "separate", "filenames": ["polyfill.asm", "horizon.asm"]})
        parser.symbols.set_global("octant", op.var(2, 0, name="octant", segment="data"))

        rendered = Proc("mainproc").generate_c_cmd(Cpp(parser), parser.action_code("mov dx, SEG Octant"))

        self.assertEqual(rendered, "dx = m2c::segment_of_external(octant);")

    def test_internal_offset_in_single_source_translation_keeps_plain_segment_offset(self):
        parser = Parser({"mergeprocs": "separate", "filenames": ["polyfill.asm"]})
        parser.symbols.set_global("octant", op.var(2, 0, name="octant", segment="data"))

        rendered = Proc("mainproc").generate_c_cmd(Cpp(parser), parser.action_code("mov ax, OFFSET Octant"))

        self.assertEqual(rendered, "ax = offset(data,octant);")

    def test_plain_ret_in_far_proc_renders_far_return(self):
        parser = Parser([])
        proc = Proc("loadfile", far=True)
        cpp = Cpp(parser)
        cpp.proc = proc

        rendered = proc.generate_c_cmd(cpp, parser.action_code("ret"))

        self.assertEqual(rendered, "RETF(0)")

    def test_plain_ret_in_grouped_far_proc_label_renders_far_return(self):
        parser = Parser([])
        far_proc = Proc("createfile", far=True)
        parser.symbols.set_global("createfile", far_proc)
        wrapper = Proc("libcode_0_proc", far=False)
        wrapper.add_label("createfile", op.label("createfile", proc="libcode_0_proc", isproc=False, far=True))
        wrapper.stmts.append(parser.action_code("ret"))
        cpp = Cpp(parser)
        cpp.proc = wrapper

        wrapper.visit(cpp)

        self.assertIn("RETF(0)", cpp.body)
        self.assertNotIn("RETN(0)", cpp.body)


class MasmLabelDirectiveTest(unittest.TestCase):
    def test_label_directive_defines_alias_without_advancing_offset(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "Alias LABEL WORD\n"
            "value db 1,2\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        alias = parser.symbols.get_global("alias")
        value = parser.symbols.get_global("value")

        self.assertIsInstance(alias, op.var)
        self.assertEqual(alias.offset, 0)
        self.assertEqual(alias.size, 2)
        self.assertEqual(alias.original_type, "word")
        self.assertEqual(value.offset, 0)
        self.assertEqual(parser.data_aliases[0].name, "alias")

    def test_label_directive_renders_typed_reference(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "Alias LABEL WORD\n"
            "value db 1,2\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        _, _, data_cpp, hpp = Cpp(parser).render_data_c(parser.segments)

        self.assertIn("word& alias=*((word*)(&data+0x0));", data_cpp)
        self.assertIn("extern word& alias;", hpp)

    def test_near_label_directive_defines_code_label_not_data_alias(self):
        parser = Parser([])
        source = (
            ".code\n"
            "ArmOk LABEL NEAR\n"
            "    ret\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        symbol = parser.symbols.get_global("armok")

        self.assertIsInstance(symbol, op.label)
        self.assertEqual(parser.data_aliases, [])

class Masm510StructCompatibilityTest(unittest.TestCase):
    def test_struct_alignment_emits_padding_and_aligned_member_offsets(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "MOBILE STRUCT 2\n"
            "MOB_NUM DB 0\n"
            "MOB_TYPE DB 0\n"
            "MOB_ANIM DB 0\n"
            "MOB_LINK_PTR DW -1\n"
            "MOBILE ENDS\n"
            "MOB_REC_SIZE EQU TYPE MOBILE\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        structures = Cpp(parser).produce_structures(parser.structures)

        self.assertEqual(parser.structures["mobile"].getsize(), 6)
        self.assertIn("db __m2c_pad_3_3;", structures)
        self.assertIn("dw mob_link_ptr;", structures)
        self.assertIn("static const word mob_link_ptr = offsetof(struct mobile, mob_link_ptr);", structures)
        self.assertEqual(parser.eval_expression_to_int(parser.symbols.get_global("mob_rec_size").value), 6)

    def test_option_m510_emits_global_struct_member_offset_constants(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "VIEWPOINT STRUCT\n"
            "VP_PITCH DW 0\n"
            "VIEWPOINT ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        structures = Cpp(parser).produce_structures(parser.structures)

        self.assertIn("static const word vp_pitch = offsetof(struct viewpoint, vp_pitch);", structures)

    def test_type_operator_renders_sizeof_for_record_size_equ(self):
        parser = Parser([])
        source = (
            "VIEWPOINT STRUCT\n"
            "VP_PITCH DW 0\n"
            "VIEWPOINT ENDS\n"
            "VIEW_REC_SIZE EQU TYPE VIEWPOINT\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("view_rec_size").accept(cpp)

        self.assertIn("static const int view_rec_size = 2;", cpp._cmdlabel)

    def test_size_operator_on_array_renders_total_byte_size(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "LhsX DW 200 DUP(0)\n"
            "BUF_SIZE EQU SIZE LhsX\n"
            "TYPE_SIZE EQU TYPE LhsX\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        equates = Cpp(parser).produce_equates()

        self.assertIn("static const int buf_size = 400;", equates)
        self.assertIn("static const int type_size = 2;", equates)

    def test_text_equ_partial_expression_expands_before_parsing_operand(self):
        with TemporaryDirectory() as tmp:
            source = Path(tmp) / "text_equ.asm"
            source.write_text(
                (
                    "TAIL EQU <+ 2>\n"
                    ".code\n"
                    "main PROC\n"
                    "    mov ax, 4 TAIL\n"
                    "    ret\n"
                    "main ENDP\n"
                    "END\n"
                ),
                encoding="utf-8",
            )
            parser = Parser([])
            parser.parse_file(str(source))

        rendered = Cpp(parser).write_procedures("", "text_equ.h")

        self.assertIn("R(ax = 4+2;);", rendered)
        self.assertIn("#define tail + 2", rendered)

    def test_text_equ_does_not_expand_inside_quoted_strings(self):
        parser = Parser([])
        parser._text_equates["tail"] = "+ 2"

        self.assertEqual(parser._substitute_text_equates_in_code('msg db "TAIL", TAIL'), 'msg db "TAIL", + 2')

    def test_text_equ_shadowed_by_numeric_assignment_stops_text_expansion(self):
        parser = Parser([])
        source = (
            "TAIL EQU <+ 2>\n"
            "value1 dw 4 TAIL\n"
            "TAIL = 9\n"
            "value2 dw TAIL\n"
            "END\n"
        )

        expanded = parser._expand_text_equates(source)

        self.assertIn("value1 dw 4 + 2", expanded)
        self.assertIn("value2 dw TAIL", expanded)

    def test_public_data_segment_keeps_class_metadata(self):
        parser = Parser([])
        source = "DATA SEGMENT PARA PUBLIC 'DATA'\nDATA ENDS\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        segment = parser.segments["data"]

        self.assertIn("public", segment.options)
        self.assertEqual(segment.segclass, "data")

    def test_m510_struct_name_equ_renders_structure_size(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "RWR STRUCT\n"
            "RWR_TYPE DW 0\n"
            "RWR ENDS\n"
            "RWR_REC_SIZE EQU RWR\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        equates = Cpp(parser).produce_equates()

        self.assertIn("static const int rwr_rec_size = (int)sizeof(rwr);", equates)

    def test_equates_emit_once_for_header_scope(self):
        parser = Parser([])
        source = "NUL EQU 0\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        self.assertEqual(cpp.produce_equates(), "static const int nul = 0;\n")
        self.assertEqual(cpp.produce_equates(), "")

    def test_equ_forward_alias_emits_as_textual_macro(self):
        parser = Parser([])
        source = "COL_RAD_MISS EQU COL_MAP_ENEMY\nCOL_MAP_ENEMY EQU 4\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        equates = Cpp(parser).produce_equates()

        self.assertIn("#define col_rad_miss (col_map_enemy)", equates)
        self.assertIn("static const int col_map_enemy = 4;", equates)

    def test_text_equate_emits_raw_macro_body(self):
        parser = Parser([])
        source = "PAIR EQU <WORD PTR>\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        equates = Cpp(parser).produce_equates()

        self.assertEqual(equates, "#define pair WORD PTR\n")

    def test_text_equate_can_hold_partial_expression_text(self):
        parser = Parser([])
        source = "TAIL EQU <+ 2>\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        equates = Cpp(parser).produce_equates()

        self.assertEqual(equates, "#define tail + 2\n")

    def test_numeric_equ_resolves_dup_repeat_count(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "MAX_ARGS EQU 32\n"
            "ARGV DW MAX_ARGS DUP(0)\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        data = {d.label: d for segment in parser.segments.values() for d in segment.getdata()}

        self.assertEqual(data["argv"].elements, 32)
        self.assertEqual(Cpp(parser).produce_c_data_single_(data["argv"])[0], "{0}")

    def test_public_near_label_inside_proc_gets_callable_wrapper(self):
        parser = Parser([])
        source = (
            "PUBLIC DrawFeatures2\n"
            "CODE SEGMENT\n"
            "DrawFeatures1 PROC NEAR\n"
            "ret\n"
            "DrawFeatures2 LABEL NEAR\n"
            "ret\n"
            "DrawFeatures1 ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="features")
        cpp.process()

        wrappers = cpp.render_function_wrappers_c()

        self.assertIn(
            "bool drawfeatures2(m2c::_offsets _i, struct m2c::_STATE* _state){return drawfeatures1(_i ? _i : m2c::kdrawfeatures2, _state);}",
            wrappers,
        )

    def test_public_label_before_inline_data_remains_callable_code(self):
        parser = Parser([])
        source = (
            "PUBLIC Entry\n"
            "CODE SEGMENT\n"
            "Start PROC NEAR\n"
            "ret\n"
            "Entry:\n"
            "db 0B1h\n"
            "ret\n"
            "Start ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="inline_data")
        cpp.process()

        self.assertIsInstance(parser.symbols.get_global("entry"), op.label)
        self.assertNotIn("entry", [data.label for data in parser.segments["code"].getdata()])
        self.assertIn(
            "bool entry(m2c::_offsets _i, struct m2c::_STATE* _state){return start(_i ? _i : m2c::kentry, _state);}",
            cpp.render_function_wrappers_c(),
        )

    def test_non_public_procs_are_static_but_public_procs_are_exported(self):
        parser = Parser([])
        source = (
            "PUBLIC Exported\n"
            "CODE SEGMENT\n"
            "Hidden PROC NEAR\n"
            "ret\n"
            "Hidden ENDP\n"
            "Exported PROC NEAR\n"
            "ret\n"
            "Exported ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="module")
        cpp.process()

        declarations = cpp.proc_strategy.write_declarations(cpp._procs + list(cpp.grouped), parser)

        self.assertIn("static bool hidden(m2c::_offsets, struct m2c::_STATE*);", declarations)
        self.assertIn("bool exported(m2c::_offsets, struct m2c::_STATE*);", declarations)
        self.assertNotIn("static bool exported", declarations)

    def test_public_proc_uses_weak_linkage_in_multi_file_output(self):
        parser = Parser({"filenames": ["one.asm", "two.asm"]})
        source = (
            "PUBLIC Exported\n"
            "CODE SEGMENT\n"
            "Exported PROC NEAR\n"
            "ret\n"
            "Exported ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="module")
        cpp.process()

        declarations = cpp.proc_strategy.write_declarations(cpp._procs + list(cpp.grouped), parser)

        self.assertIn("__attribute__((weak)) bool exported(m2c::_offsets, struct m2c::_STATE*);", declarations)

    def test_public_code_export_proc_uses_weak_linkage(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["helper"]})
        source = (
            "CODE SEGMENT\n"
            "PUBLIC Helper\n"
            "Helper PROC NEAR\n"
            "ret\n"
            "Helper ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="module")
        cpp.process()

        declarations = cpp.proc_strategy.write_declarations(cpp._procs + list(cpp.grouped), parser)

        self.assertIn("__attribute__((weak)) bool helper(m2c::_offsets, struct m2c::_STATE*);", declarations)
        self.assertNotIn("static bool helper", declarations)

    def test_public_code_export_label_wrapper_uses_weak_linkage(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["entry"]})
        source = (
            "CODE SEGMENT\n"
            "PUBLIC Entry\n"
            "Owner PROC NEAR\n"
            "ret\n"
            "Entry LABEL NEAR\n"
            "ret\n"
            "Owner ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="module")
        cpp.process()

        wrappers = cpp.render_function_wrappers_c()

        self.assertIn(
            "__attribute__((weak)) bool entry(m2c::_offsets _i, struct m2c::_STATE* _state){return owner(_i ? _i : m2c::kentry, _state);}",
            wrappers,
        )

    def test_grouped_dispatcher_falls_back_to_module_dispatcher(self):
        cpp = Cpp(Parser([]))
        cpp.proc = Proc("_group1")
        cpp.groups["owner"] = "_group1"

        jump_table = cpp.produce_jump_table([("local", "local")])

        self.assertIn("case m2c::klocal:", jump_table)
        self.assertIn("default: return __dispatch_call(__disp, _state);", jump_table)
        self.assertNotIn("Don't know how to jump", jump_table)

    def test_external_code_export_does_not_globalize_non_public_local_collision(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["getq"], "public_code_exports": ["getq"]})
        source = (
            "CODE SEGMENT\n"
            "GetQ PROC NEAR\n"
            "ret\n"
            "GetQ ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="local_owner")
        cpp.process()

        declarations = cpp.proc_strategy.write_declarations(cpp._procs + list(cpp.grouped), parser)

        self.assertIn("static bool getq(m2c::_offsets, struct m2c::_STATE*);", declarations)
        self.assertNotIn("__attribute__((weak)) bool getq", declarations)

    def test_external_code_export_without_public_owner_uses_weak_linkage(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["helper"], "public_code_exports": []})
        source = (
            "CODE SEGMENT\n"
            "Helper PROC NEAR\n"
            "ret\n"
            "Helper ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="module")
        cpp.process()

        declarations = cpp.proc_strategy.write_declarations(cpp._procs + list(cpp.grouped), parser)

        self.assertIn("__attribute__((weak)) bool helper(m2c::_offsets, struct m2c::_STATE*);", declarations)
        self.assertNotIn("static bool helper", declarations)

    def test_continuation_module_owns_public_code_export_label(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["target"]})
        source = (
            "CODE SEGMENT\n"
            "Owner PROC NEAR\n"
            "ret\n"
            "Target LABEL NEAR\n"
            "ret\n"
            "Owner ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, outfile="math2")
        cpp.process()

        wrappers = cpp.render_function_wrappers_c()

        self.assertIn(
            "__attribute__((weak)) bool target(m2c::_offsets _i, struct m2c::_STATE* _state){return owner(_i ? _i : m2c::ktarget, _state);}",
            wrappers,
        )

    def test_public_code_export_offset_renders_as_aggregate_code_constant(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["shared_table"]})
        source = (
            "CODE SEGMENT\n"
            "main PROC NEAR\n"
            "mov bx, OFFSET Shared_Table\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)
        proc.visit(cpp)

        self.assertIn("R(bx = m2c::kglobal_shared_table;)", cpp.body)

    def test_external_var_offset_renders_as_public_code_export_constant(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["target"]})
        source = (
            "EXTRN Target:BYTE\n"
            "CODE SEGMENT\n"
            "main PROC NEAR\n"
            "mov bx, OFFSET Target\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)

        rendered = Proc("mainproc").generate_c_cmd(Cpp(parser), proc.stmts[0])

        self.assertEqual("bx = m2c::kglobal_target;", rendered)

    def test_external_var_data_offset_renders_as_public_code_export_constant(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["target"]})
        source = (
            "EXTRN Target:WORD\n"
            "DATA SEGMENT\n"
            "Token db LOW OFFSET Target\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        data = parser.segments["data"].getdata()[0]

        rendered, _, _ = Cpp(parser).produce_c_data_single_(data)

        self.assertIn("m2c::kglobal_target", rendered)

    def test_local_public_code_data_entry_renders_as_global_code_constant(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["target"],
                         "filenames": ["mod_a.asm", "mod_b.asm"]})
        source = (
            "CODE SEGMENT\n"
            "Table dw Target\n"
            "Table2 dw OFFSET Target\n"
            "Target:\n"
            "ret\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        rows = parser.segments["code"].getdata()
        cpp = Cpp(parser)

        rendered = "\n".join(cpp.produce_c_data_single_(row)[0] for row in rows)

        self.assertIn("m2c::kglobal_target", rendered)
        self.assertNotIn("m2c::ktarget", rendered)

    def test_local_code_label_stored_in_data_is_exported_for_indirect_dispatch(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "Dispatch dw Handler\n"
            "Handler:\n"
            "ret\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)
        data = parser.segments["code"].getdata()[0]
        rendered, _, _ = cpp.produce_c_data_single_(data)

        self.assertIn("handler", cpp.export_external_code_symbol_names())
        self.assertEqual(cpp.wrapper_linkage("handler"), "__attribute__((weak)) ")
        self.assertIn("m2c::kglobal_handler", rendered)

    def test_instruction_offset_code_label_uses_local_dispatch_constant(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "Dispatch dw Handler\n"
            "mov ax, OFFSET Handler\n"
            "Handler:\n"
            "ret\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("mainproc").visit(cpp)

        self.assertIn("handler", cpp.export_external_code_symbol_names())
        self.assertIn("R(ax = m2c::khandler;)", cpp.body)
        self.assertNotIn("R(ax = m2c::kglobal_handler;)", cpp.body)

    def test_external_proc_does_not_emit_local_code_offset_constant(self):
        parser = Parser({"mergeprocs": "separate", "public_code_exports": ["target"]})
        source = (
            "EXTRN Target:NEAR\n"
            "CODE SEGMENT\n"
            "main PROC NEAR\n"
            "mov bx, OFFSET Target\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        label_offsets = Cpp(parser).produce_label_offsets()

        self.assertNotIn("static const dd ktarget", label_offsets)

    def test_unresolved_external_proc_keeps_local_code_offset_placeholder(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["target"]})
        source = (
            "EXTRN Target:NEAR\n"
            "CODE SEGMENT\n"
            "main PROC NEAR\n"
            "call Target\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        label_offsets = Cpp(parser).produce_label_offsets()

        self.assertIn("static const dd ktarget", label_offsets)

    def test_equates_header_emits_collision_free_global_code_offset_alias(self):
        with TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                Cpp(Parser([]))._write_equates_header([], set(), {"target": 0x1234})

                header = Path("_equates.h").read_text(encoding="utf-8")
            finally:
                os.chdir(cwd)

        self.assertIn("static const dd ktarget = (0x1234);", header)
        self.assertIn("static const dd kglobal_target = (0x1234);", header)

    def test_defined_proc_exports_code_offset_for_aggregate_equates(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["target"]})
        source = (
            "PUBLIC Target\n"
            "CODE SEGMENT\n"
            "Target PROC NEAR\n"
            "ret\n"
            "Target ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        offsets = Cpp(parser).export_defined_code_symbol_offsets()

        self.assertIn("target", offsets)

    def test_defined_label_exports_code_offset_for_aggregate_equates(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "Target:\n"
            "ret\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        offsets = Cpp(parser).export_defined_code_symbol_offsets()

        self.assertIn("target", offsets)

    def test_data_label_exports_offset_for_near_external_aliases(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "DATA SEGMENT\n"
            "Target LABEL WORD\n"
            "dw 0\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        offsets = Cpp(parser).export_defined_code_symbol_offsets()

        self.assertIn("target", offsets)

    def test_public_label_before_inline_data_exports_storage_offset(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "PUBLIC Table\n"
            "CODE SEGMENT\n"
            "db 0\n"
            "Table:\n"
            "dw 1234h\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        offsets = Cpp(parser).export_defined_code_symbol_offsets()

        self.assertEqual(offsets["table"], 1)

    def test_public_table_label_before_labeled_data_exports_storage_offset(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "PUBLIC Table\n"
            "CODE SEGMENT\n"
            "Table:\n"
            "Entry dw 1234h\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        aliases = {alias.name: alias.offset for alias in parser.code_offset_aliases}

        self.assertEqual(aliases["table"], 0)

    def test_collect_code_exports_matches_external_var_to_public_code_label(self):
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            target = temp / "target.asm"
            target.write_text(
                "PUBLIC Target\n"
                "CODE SEGMENT\n"
                "Target:\n"
                "db 0\n"
                "CODE ENDS\n"
                "END\n",
                encoding="utf-8",
            )
            user = temp / "user.asm"
            user.write_text(
                "EXTRN Target:BYTE\n"
                "CODE SEGMENT\n"
                "main PROC NEAR\n"
                "mov bx, OFFSET Target\n"
                "ret\n"
                "main ENDP\n"
                "CODE ENDS\n"
                "END\n",
                encoding="utf-8",
            )

            _, public_code_exports = collect_code_exports(
                [str(target), str(user)],
                Namespace(passes=1),
            )

        self.assertEqual(public_code_exports, {"target"})

    def test_collect_code_exports_matches_external_proc_to_public_proc(self):
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            target = temp / "target.asm"
            target.write_text(
                "PUBLIC GetQ\n"
                "CODE SEGMENT\n"
                "GetQ PROC NEAR\n"
                "ret\n"
                "GetQ ENDP\n"
                "CODE ENDS\n"
                "END\n",
                encoding="utf-8",
            )
            user = temp / "user.asm"
            user.write_text(
                "EXTRN GetQ:NEAR\n"
                "CODE SEGMENT\n"
                "main PROC NEAR\n"
                "call GetQ\n"
                "ret\n"
                "main ENDP\n"
                "CODE ENDS\n"
                "END\n",
                encoding="utf-8",
            )

            external_exports, public_code_exports = collect_code_exports(
                [str(target), str(user)],
                Namespace(passes=1),
            )

        self.assertIn("getq", external_exports)
        self.assertEqual(public_code_exports, {"getq"})

    def test_equates_header_emits_aggregate_code_offsets(self):
        with TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                Cpp(Parser([]))._write_equates_header([], set(), {"shared_table": 0x1234})

                equates = Path("_equates.h").read_text(encoding="utf-8")
            finally:
                os.chdir(cwd)

        self.assertIn("#define M2C_CODE_EQUATE_shared_table 1", equates)
        self.assertIn("static const dd kshared_table = (0x1234);", equates)

    def test_external_code_dispatcher_skips_duplicate_offsets(self):
        parser = Parser([])
        parser.exported_code_symbol_offsets = {"first": 0x1234, "second": 0x1234}

        dispatcher = Cpp(parser)._produce_external_code_dispatcher()

        self.assertEqual(dispatcher.count("case 0x1234:"), 1)

    def test_external_code_dispatcher_uses_only_callable_offsets(self):
        parser = Parser([])
        parser.exported_code_symbol_offsets = {"begdsg": 0x0, "target": 0x1234}
        parser.exported_callable_code_symbol_offsets = {"target": 0x1234}

        cpp = Cpp(parser)
        dispatcher = cpp._produce_external_code_dispatcher()
        declarations = cpp._produce_external_code_declarations()

        self.assertIn("target", dispatcher)
        self.assertNotIn("begdsg", dispatcher)
        self.assertIn("target", declarations)
        self.assertNotIn("begdsg", declarations)

    def test_merged_code_segment_data_offsets_are_not_callable_exports(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                segment = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                segment.append(op.Data("BegDsg", "dw", op.DataType.NUMBER, [0], 1, 2))
                writer = Cpp(Parser([]))
                writer.write_segment_file(
                    OrderedDict([("cseg", segment)]),
                    OrderedDict(),
                    "module.asm",
                    defined_code_symbols={"target"},
                    extern_code_symbols={"begdsg", "target"},
                    defined_code_symbol_offsets={"begdsg": 0x0, "target": 0x100b},
                )

                merger = Cpp(Parser([]), merge_data_segments=True)
                merger.read_segment_files(["module.asm"])

                self.assertIn("begdsg", merger._context.exported_code_symbol_offsets)
                self.assertNotIn("begdsg", merger._context.exported_callable_code_symbol_offsets)
                self.assertIn("target", merger._context.exported_callable_code_symbol_offsets)
            finally:
                os.chdir(old_cwd)

    def test_external_scalar_data_declares_reference_to_aggregate_storage(self):
        parser = Parser([])
        source = "EXTRN PSP:WORD\nCODE SEGMENT\nmain PROC\nmov PSP, ax\nret\nmain ENDP\nCODE ENDS\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        declarations = cpp.produce_externals(parser)

        self.assertIn("extern dw& psp;", declarations)

    def test_near_external_memory_operand_renders_as_data_reference(self):
        parser = Parser([])
        source = (
            "EXTRN Target:NEAR\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov bx, WORD PTR Target\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)

        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)
        declarations = cpp.produce_externals(parser)

        self.assertIn("bx = target;", rendered)
        self.assertNotIn("raddr(ds,m2c::ktarget)", rendered)
        self.assertIn("extern dw& target;", declarations)
        self.assertNotIn("target", cpp.export_external_code_symbol_names())

    def test_near_external_offset_operand_keeps_code_offset_export(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["Target"],
                         "filenames": ["mod_a.asm", "mod_b.asm"]})
        source = (
            "EXTRN Target:NEAR\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov bx, OFFSET Target\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)

        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("bx = m2c::kglobal_target;", rendered)
        self.assertNotIn("extern dw& target;", cpp.produce_externals(parser))

    def test_cs_near_external_memory_operand_keeps_code_offset_reference(self):
        parser = Parser({"mergeprocs": "separate", "external_code_exports": ["Target"]})
        source = (
            "EXTRN Target:NEAR\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "push CS:Target[si]\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        self.assertIsInstance(proc, Proc)
        cpp = Cpp(parser)

        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("m2c::ktarget", rendered)
        self.assertNotIn("&target", rendered)
        self.assertNotIn("extern dw& target;", cpp.produce_externals(parser))
        self.assertIn("target", cpp.export_external_code_symbol_names())

    def test_segment_sidecar_exports_expression_equates_for_aggregate_header(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                parser = Parser([])
                source = "PUBLIC MAX_AUTO_HDG\nMAX_AUTO_HDG EQU 359\nEND\n"
                tree = parser.parse_text(source)
                parser.process_ast(source, tree)
                cpp = Cpp(parser, outfile="avionics")
                cpp.write_segment_file(parser.segments, parser.structures, "avionics.asm", [], cpp.export_equates())

                merger = Cpp(Parser([]))
                merger.write_data_segments_cpp(*merger.read_segment_files(["avionics.asm"]))

                self.assertIn("#define max_auto_hdg (359)", Path("_equates.h").read_text(encoding="cp437"))
            finally:
                os.chdir(old_cwd)

    def test_data_cpp_exports_linked_segment_offset_helpers(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                data = op.Segment("DATA", 0)
                data.segment_aliases = {"data": 0, "wsdata": 0x200}
                data.append(op.Data("x", "db", op.DataType.NUMBER, [0], 1, 1))
                stack = op.Segment("STACK", 0x550)
                stack.append(op.Data("y", "db", op.DataType.NUMBER, [0], 1, 1))
                code = op.Segment("CODE", 0x10, segclass="code")
                code.append(op.Data("embedded", "db", op.DataType.NUMBER, [0], 1, 1))
                segments = OrderedDict([("data", data), ("code", code), ("stack", stack)])

                Cpp(Parser([])).write_data_segments_cpp(segments, OrderedDict())

                data_cpp = Path("_data.cpp").read_text(encoding="cp437")
                self.assertIn("dw near_offset_linked_address(const void* symbol)", data_cpp)
                self.assertIn("const size_t linear = anchor->linear +", data_cpp)
                self.assertIn("linear - ((anchor->linear >> 4) << 4)", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::data), 0x0, true}", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::wsdata), 0x200, true}", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::stack), 0x550, true}", data_cpp)
                self.assertNotIn("{reinterpret_cast<const db*>(&::code), 0x10}", data_cpp)
            finally:
                os.chdir(old_cwd)

    def test_linked_data_segment_base_uses_exported_offset_alias(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                data = op.Segment("DSEG", 0x1a20, options={"public"}, segclass="DATASG")
                data.segment_aliases = {"dseg": 0}
                data.append(op.Data("", "db", op.DataType.ARRAY, [0], 0x100, 0x100, offset=0))
                data.append(op.Data("value", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0x100))
                segments = OrderedDict([("datasg", data)])
                parser = Parser({"filenames": ["one.asm", "two.asm"], "loadsegment": "0x192"})
                parser.data_aliases = [
                    op.var(2, 0, "DataStart", segment="datasg", original_type="word"),
                ]
                parser.exported_code_symbol_offsets = {"datastart": 0x1EA}

                Cpp(parser).write_data_segments_cpp(segments, OrderedDict())

                data_refs = Path("_data_refs_000.cpp").read_text(encoding="cp437")
                self.assertIn("db& datasg=*((db*)&m2c::m+0x1b00);", data_refs)
                self.assertIn("db& dseg=*((db*)&m2c::m+0x1b00);", data_refs)
                data_cpp = Path("_data.cpp").read_text(encoding="cp437")
                self.assertIn("{reinterpret_cast<const db*>(&::datasg), 0x1b00, true}", data_cpp)
            finally:
                os.chdir(old_cwd)

    def test_relocated_public_data_segment_overrides_exported_offset_alias_base(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                code = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                code.append(op.Data("code_blob", "db", op.DataType.ARRAY, [0], 0x1334, 0x1334, offset=0))
                data = op.Segment("DSEG", 0x1E0, options={"public"}, segclass="DATASG")
                data.segment_aliases = {"dseg": 0}
                data.append(op.Data("data_blob", "db", op.DataType.ARRAY, [0], 0xA92, 0xA92, offset=0))
                segments = OrderedDict([("codesg", code), ("datasg", data)])
                Cpp._layout_public_segment_class_storage(segments)
                parser = Parser({"filenames": ["one.asm", "two.asm"], "loadsegment": "0x192"})
                parser.data_aliases = [
                    op.var(2, 0, "DataStart", segment="datasg", original_type="word"),
                ]
                parser.exported_code_symbol_offsets = {"datastart": 0x1EA}

                Cpp(parser).write_data_segments_cpp(segments, OrderedDict())

                data_refs = Path("_data_refs_000.cpp").read_text(encoding="cp437")
                self.assertIn("db& datasg=*((db*)&m2c::m+0x2c60);", data_refs)
                self.assertIn("db& dseg=*((db*)&m2c::m+0x2c60);", data_refs)
                self.assertNotIn("db& dseg=*((db*)&m2c::m+0x1b00);", data_refs)
                data_cpp = Path("_data.cpp").read_text(encoding="cp437")
                self.assertIn("{reinterpret_cast<const db*>(&::datasg), 0x2c60, true}", data_cpp)
            finally:
                os.chdir(old_cwd)

    def test_aggregate_equates_header_uses_all_defined_code_offsets(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                data = op.Segment("DSEG", 0, options={"public"}, segclass="DATASG")
                data.append(op.Data("value", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0))
                segments = OrderedDict([("datasg", data)])
                parser = Parser({"filenames": ["one.asm", "two.asm"]})
                parser.exported_code_symbol_offsets = {}
                parser.all_defined_code_symbol_offsets = {"chrgtr": 0x1234, "stprdy": 0x1235}

                Cpp(parser).write_data_segments_cpp(segments, OrderedDict())

                equates = Path("_equates.h").read_text(encoding="cp437")
                self.assertIn("static const dd kchrgtr = (0x1234);", equates)
                self.assertIn("static const dd kglobal_chrgtr = (0x1234);", equates)
                self.assertIn("static const dd kstprdy = (0x1235);", equates)
                self.assertIn("static const dd kglobal_stprdy = (0x1235);", equates)
            finally:
                os.chdir(old_cwd)

    def test_extern_near_data_label_offset_uses_relocated_public_data_segment(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                code = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                code.append(op.Data("code_blob", "db", op.DataType.ARRAY, [0], 0x1334, 0x1334, offset=0))
                data = op.Segment("DSEG", 0x1E0, options={"public"}, segclass="DATASG")
                data.segment_aliases = {"dseg": 0}
                data.append(op.Data("begdsg", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0))
                provider_segments = OrderedDict([("cseg", code), ("dseg", data)])
                Cpp(Parser([])).write_segment_file(
                    provider_segments,
                    OrderedDict(),
                    "provider.asm",
                    data_aliases=[op.var(2, 0, "begdsg", segment="dseg", original_type="word")],
                    defined_code_symbols={"begdsg"},
                    defined_code_symbol_offsets={"begdsg": 0},
                )
                Cpp(Parser([])).write_segment_file(
                    OrderedDict(),
                    OrderedDict(),
                    "consumer.asm",
                    extern_code_symbols={"begdsg"},
                )

                merger = Cpp(
                    Parser({"filenames": ["provider.asm", "consumer.asm"], "loadsegment": "0x192"}),
                    merge_data_segments=True,
                )
                merger.write_data_segments_cpp(*merger.read_segment_files(["provider.asm", "consumer.asm"]))

                equates = Path("_equates.h").read_text(encoding="cp437")
                self.assertIn("static const dd kglobal_begdsg = (0x1340);", equates)
                data_refs = Path("_data_refs_000.cpp").read_text(encoding="cp437")
                self.assertIn("db& dseg=*((db*)&m2c::m+0x2c60);", data_refs)
            finally:
                os.chdir(old_cwd)

    def test_location_counter_equates_relocate_with_merged_code_segment(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                first = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                first.append(op.Data("filler", "db", op.DataType.NUMBER, [0] * 0x20, 0x20, 0x20))
                second = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                second.append(op.Data("rom_bytes", "db", op.DataType.NUMBER, [0], 1, 1, offset=0x100))
                writer = Cpp(Parser([]))
                writer.write_segment_file(OrderedDict([("cseg", first)]), OrderedDict(), "first.asm")
                writer.write_segment_file(
                    OrderedDict([("cseg", second)]),
                    OrderedDict(),
                    "second.asm",
                    equates=[
                        ("copy_start", "256", True, "cseg", True),
                        ("copy_len", "259-256", True, "cseg", True),
                        ("plain_count", "75+1", True, "cseg", False),
                    ],
                )

                merger = Cpp(Parser([]), merge_data_segments=True)
                merger.read_segment_files(["first.asm", "second.asm"])

                exported = {name: value for name, value, _is_code in merger._context.exported_equates}
                self.assertEqual(exported["copy_start"], "288")
                self.assertEqual(exported["copy_len"], "291-288")
                self.assertEqual(exported["plain_count"], "75+1")
            finally:
                os.chdir(old_cwd)

    def test_linked_code_segment_storage_maps_load_segment_addresses(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                code = op.Segment("CODESG", 0, options={"public"}, segclass="CODESG")
                code.segment_aliases = {"codesg": 0, "cseg": 0}
                code.append(op.Data("table", "dw", op.DataType.NUMBER, [0], 1, 2))
                segments = OrderedDict([("codesg", code)])
                parser = Parser({"filenames": ["one.asm", "two.asm"], "loadsegment": "0x192"})

                Cpp(parser).write_data_segments_cpp(segments, OrderedDict())

                data_refs = Path("_data_refs_000.cpp").read_text(encoding="cp437")
                self.assertIn("db& codesg=*((db*)&m2c::m+0x1920);", data_refs)
                self.assertIn("db& cseg=*((db*)&m2c::m+0x1920);", data_refs)
                data_cpp = Path("_data.cpp").read_text(encoding="cp437")
                self.assertIn("db* linked_code_segment_raddr(dw segment, dw offset)", data_cpp)
                self.assertIn("if (segment != 0x192) { return nullptr; }", data_cpp)
                self.assertIn("if (offset >= 0x0 && offset < 0x2) { return (db*)&m + 0x1920 + offset; }", data_cpp)
                self.assertIn("void copy_linked_program_segment_prefix(dw segment, const void* source, size_t size)", data_cpp)
                self.assertIn("static dw linked_data_runtime_segments[8]", data_cpp)
                self.assertIn("remember_linked_data_runtime_segment(value);", data_cpp)
                self.assertNotIn("mirror_linked_code_segments", data_cpp)
            finally:
                os.chdir(old_cwd)

    def test_linked_code_segment_address_mapping_keeps_overlapping_data_records(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                code = op.Segment("CODESG", 0, options={"public"}, segclass="CODESG")
                code.segment_aliases = {"codesg": 0, "cseg": 0}
                code.append(op.Data("table", "db", op.DataType.NUMBER, [0, 1, 2, 3], 4, 4))
                data = op.Segment("DATA", 0x1921)
                data.append(op.Data("live", "dw", op.DataType.NUMBER, [0], 1, 2))
                segments = OrderedDict([("codesg", code), ("data", data)])
                parser = Parser({"filenames": ["one.asm", "two.asm"], "loadsegment": "0x192"})

                Cpp(parser).write_data_segments_cpp(segments, OrderedDict())

                data_cpp = Path("_data.cpp").read_text(encoding="cp437")
                self.assertIn("if (offset >= 0x0 && offset < 0x4) { return (db*)&m + 0x1920 + offset; }", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::codesg), 0x1920, false}", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::data), 0x1921, true}", data_cpp)
                self.assertIn("anchor.linear != 0 && anchor.is_data", data_cpp)
                self.assertIn("segment == 0 || segment >= 0xa000 || is_linked_data_runtime_segment(segment)", data_cpp)
                self.assertNotIn("std::memcpy", data_cpp)
            finally:
                os.chdir(old_cwd)

    def test_linked_code_segment_address_mapping_uses_array_element_span(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                code = op.Segment("CODESG", 0, options={"public"}, segclass="CODESG")
                code.segment_aliases = {"codesg": 0, "cseg": 0}
                code.append(op.Data("table", "db", op.DataType.ARRAY, [0], 0x20, 1, offset=0x12F6))
                segments = OrderedDict([("codesg", code)])
                parser = Parser({"filenames": ["one.asm", "two.asm"], "loadsegment": "0x192"})

                Cpp(parser).write_data_segments_cpp(segments, OrderedDict())

                data_cpp = Path("_data.cpp").read_text(encoding="cp437")
                self.assertIn("if (offset >= 0x12f6 && offset < 0x1316) { return (db*)&m + 0x1920 + offset; }", data_cpp)
            finally:
                os.chdir(old_cwd)

    def test_merged_public_code_exports_relocate_duplicate_local_offsets(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                first = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                first.append(op.Data("first_table", "db", op.DataType.NUMBER, [0, 1, 2, 3], 4, 4))
                second = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                second.append(op.Data("second_table", "db", op.DataType.NUMBER, [0, 1], 2, 2))
                writer = Cpp(Parser([]))
                writer.write_segment_file(
                    OrderedDict([("cseg", first)]),
                    OrderedDict(),
                    "first.asm",
                    defined_code_symbols={"firstproc"},
                    extern_code_symbols={"firstproc", "secondproc"},
                    defined_code_symbol_offsets={"firstproc": 0x100b},
                )
                writer.write_segment_file(
                    OrderedDict([("cseg", second)]),
                    OrderedDict(),
                    "second.asm",
                    defined_code_symbols={"secondproc"},
                    extern_code_symbols={"firstproc", "secondproc"},
                    defined_code_symbol_offsets={"secondproc": 0x100b},
                )

                merger = Cpp(Parser([]), merge_data_segments=True)
                merger.read_segment_files(["first.asm", "second.asm"])

                self.assertIn("firstproc", merger._context.exported_callable_code_symbol_offsets)
                self.assertIn("secondproc", merger._context.exported_callable_code_symbol_offsets)
                self.assertNotEqual(
                    merger._context.exported_callable_code_symbol_offsets["firstproc"],
                    merger._context.exported_callable_code_symbol_offsets["secondproc"],
                )
            finally:
                os.chdir(old_cwd)

    def test_aggregate_code_exports_avoid_all_module_local_offsets(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                first = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                first.append(op.Data("first_table", "db", op.DataType.NUMBER, [0] * 0x10, 0x10, 0x10))
                second = op.Segment("CSEG", 0, options={"public"}, segclass="CODESG")
                second.append(op.Data("second_table", "db", op.DataType.NUMBER, [0], 1, 1))
                writer = Cpp(Parser([]))
                writer.write_segment_file(
                    OrderedDict([("cseg", first)]),
                    OrderedDict(),
                    "first.asm",
                    defined_code_symbols={"target"},
                    extern_code_symbols={"target"},
                    defined_code_symbol_offsets={"target": 0x1000},
                )
                writer.write_segment_file(
                    OrderedDict([("cseg", second)]),
                    OrderedDict(),
                    "second.asm",
                    defined_code_symbols={"local_only"},
                    extern_code_symbols=set(),
                    defined_code_symbol_offsets={"local_only": 0x1001},
                )

                merger = Cpp(Parser([]), merge_data_segments=True)
                merger.read_segment_files(["first.asm", "second.asm"])

                aggregate = merger._context.exported_callable_code_symbol_offsets["target"]
                self.assertNotIn(aggregate, {0x1000, 0x1001})
            finally:
                os.chdir(old_cwd)

    def test_segment_sidecar_exports_abs_extern_equates_for_aggregate_header(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                provider = Parser([])
                source = "BAUD1200 EQU 6\nEND\n"
                tree = provider.parse_text(source)
                provider.process_ast(source, tree)
                cpp = Cpp(provider, outfile="comms")
                cpp.write_segment_file(
                    provider.segments,
                    provider.structures,
                    "comms.asm",
                    [],
                    cpp.export_equates(),
                    provider.externals_abs,
                )

                consumer = Parser([])
                source = "EXTRN BAUD1200:ABS\nEND\n"
                tree = consumer.parse_text(source)
                consumer.process_ast(source, tree)
                cpp = Cpp(consumer, outfile="control")
                cpp.write_segment_file(
                    consumer.segments,
                    consumer.structures,
                    "control.asm",
                    [],
                    cpp.export_equates(),
                    consumer.externals_abs,
                )

                merger = Cpp(Parser([]))
                merger.write_data_segments_cpp(*merger.read_segment_files(["comms.asm", "control.asm"]))

                self.assertIn("#define baud1200 (6)", Path("_equates.h").read_text(encoding="cp437"))
            finally:
                os.chdir(old_cwd)

    def test_segment_sidecar_does_not_export_equate_colliding_with_data_symbol(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                provider = Parser([])
                source = "PUBLIC ZT\nZT EQU 256\nEND\n"
                tree = provider.parse_text(source)
                provider.process_ast(source, tree)
                cpp = Cpp(provider, outfile="equates")
                cpp.write_segment_file(
                    provider.segments,
                    provider.structures,
                    "equates.asm",
                    [],
                    cpp.export_equates(),
                    provider.externals_abs,
                )

                data_owner = Parser([])
                source = "DATA SEGMENT\nZT DW 0\nDATA ENDS\nEND\n"
                tree = data_owner.parse_text(source)
                data_owner.process_ast(source, tree)
                cpp = Cpp(data_owner, outfile="data")
                cpp.write_segment_file(
                    data_owner.segments,
                    data_owner.structures,
                    "data.asm",
                    [],
                    cpp.export_equates(),
                    data_owner.externals_abs,
                )

                merger = Cpp(Parser([]))
                merger.write_data_segments_cpp(*merger.read_segment_files(["equates.asm", "data.asm"]))

                self.assertNotIn("#define zt", Path("_equates.h").read_text(encoding="cp437"))
            finally:
                os.chdir(old_cwd)

    def test_masm_macro_redefinition_rept_and_paste_materialize_data_label(self):
        source = """_DATA segment use16 word public 'DATA'
INCLUDE CFG.INC
NDEV MACRO NAM,N
    DEV NAM&N
ENDM
NAMES MACRO
    NLPT=0
REPT NMLPT
    NLPT=NLPT+1
    NDEV LPT,%NLPT
ENDM
ENDM
NUM=377O
DEV MACRO NAM
    PUBLIC $_&NAM
    $_&NAM=NUM
    DB "&NAM&"
    DB OFFSET NUM
    NUM=NUM-1
ENDM
table:
    NAMES
    DB 0
_DATA ends
END
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "CFG.INC").write_text("NMLPT=2\n", encoding="ascii")
            asm = path / "sample.asm"
            asm.write_text(source, encoding="ascii")

            parser = Parser([])
            parser.parse_file_lines(str(asm))
            rows = parser.segments["_data"].getdata()

            self.assertEqual([(row.label, row.offset, row.getsize()) for row in rows[:5]], [
                ("table", 0, 4),
                (rows[1].label, 4, 1),
                (rows[2].label, 5, 4),
                (rows[3].label, 9, 1),
                (rows[4].label, 10, 1),
            ])
            self.assertIsInstance(parser.symbols.get_global("table"), op.var)
            cpp = Cpp(parser)
            self.assertEqual(cpp.render_equate_value(parser.symbols.get_global("dol_lpt1")), "0377")
            self.assertEqual(cpp.render_equate_value(parser.symbols.get_global("dol_lpt2")), "255-1")

    def test_low_offset_octal_literals_keep_numeric_radix(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "TRMNUL EQU 200O\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "and al, LOW OFFSET 377O-TRMNUL\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("AND(al, (0377 & 0xff)-0200)", cpp.body)
        self.assertNotIn("(377 & 0xff)", cpp.body)

    def test_data_byte_offset_string_plus_constant_is_numeric_expression(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "Table db OFFSET \"E\"+40\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        row = parser.segments["code"].getdata()[0]
        cpp = Cpp(parser)

        value, declaration, size = cpp.produce_c_data_single_(row)

        self.assertEqual(row.getinttype(), op.DataType.NUMBER)
        self.assertEqual(value, "109")
        self.assertEqual(declaration, "db table")
        self.assertEqual(size, 1)

    def test_irpc_reserved_word_macro_materializes_bytes_and_token(self):
        source = """
R MACRO RESWRD
        extrn   RESWRD:NEAR
        DW      RESWRD
        QQ=QQ+1
        PUBLIC  $&RESWRD
        $&RESWRD=QQ
ENDM
Q MACRO RESWRD
 IFDEF  $&RESWRD
        $F=0
  IRPC  XX,<RESWRD>
   IF   $F
        $Q="&XX&"
        DB      "&XX&"
   ENDIF
   IFE  $F-1
        .XLIST
   ENDIF
        $F=$F+1
  ENDM
        .LIST
        ORG     $-1
        DB      $Q+128D
        DB      $&RESWRD
 ELSE
        un_def  RESWRD
 ENDIF
ENDM
QQ=128
R SYSTEM
Q SYSTEM
"""
        parser = Parser([])
        parser._collect_text_macros_from_content(source)

        expanded = parser._expand_text_macros(parser._strip_text_macro_definitions(source))

        self.assertNotIn("&XX&", expanded)
        self.assertNotIn("un_def", expanded)
        self.assertIn('DB      "Y"', expanded)
        self.assertIn('DB      "S"', expanded)
        self.assertIn('DB      "T"', expanded)
        self.assertIn('DB      "E"', expanded)
        self.assertIn('DB      "M"', expanded)
        self.assertIn("DB      77+128D", expanded)
        self.assertIn("DB      129", expanded)

    def test_org_current_minus_one_rewinds_next_data_offset(self):
        parser = Parser([])
        source = (
            "_DATA segment use16 word public 'DATA'\n"
            "table db \"A\"\n"
            "ORG $-1\n"
            "db 80h\n"
            "tail db 0\n"
            "_DATA ends\n"
            "END\n"
        )

        with TemporaryDirectory() as tmp:
            asm = Path(tmp) / "org.asm"
            asm.write_text(source, encoding="ascii")
            parser.parse_file_lines(str(asm))
            rows = parser.segments["_data"].getdata()

            self.assertEqual([(row.label, row.offset, row.getsize()) for row in rows], [
                ("table", 0, 1),
                (rows[1].label, 0, 1),
                ("tail", 1, 1),
            ])

    def test_code_labels_survive_later_data_label_conversion(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "start:\n"
            "    jz keep\n"
            "keep: mov al,1\n"
            "table:\n"
            "    db 1\n"
            "    ret\n"
            "CODE ENDS\n"
            "END start\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        proc = parser.symbols.get_global("mainproc")
        labels = [stmt.name for stmt in proc.stmts if isinstance(stmt, op.label)]

        self.assertIn("start", labels)
        self.assertIn("keep", labels)
        # A standalone label before data inside a code segment keeps its
        # code label (it may be a jump target, e.g. an ES_LODSB-style
        # prefix byte) while still registering as a data variable.
        self.assertIn("table", labels)
        self.assertIsInstance(parser.symbols.get_global("table"), op.var)

    def test_offset_array_plus_constant_renders_offset_not_pointer(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "arr db 8 dup(?)\n"
            "start:\n"
            "    mov bx, OFFSET arr+4\n"
            "    ret\n"
            "CODE ENDS\n"
            "END start\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        rendered = Cpp(parser).write_procedures("", "sample.h")

        self.assertIn("bx = offset(code,arr)+4;", rendered)
        self.assertNotIn("bx = arr+4;", rendered)

    def test_dummy_labels_use_stable_wide_file_hash_prefix(self):
        parser = Parser([])
        parser._switch_file_context("/tmp/TORNADO/SMOKE.ASM")

        label = parser.get_dummy_label()

        self.assertRegex(label, r"^dummy[0-9a-f]{8}_default_seg_0$")

    def test_dummy_data_labels_include_line_number_when_available(self):
        parser = Parser([])
        parser._switch_file_context("/tmp/TORNADO/SECDATA1.ASM")

        first = parser.get_dummy_label(50)
        second = parser.get_dummy_label(1)

        self.assertNotEqual(first, second)
        self.assertTrue(first.endswith("_50"))
        self.assertTrue(second.endswith("_1"))

    def test_cross_proc_local_conditional_jump_dispatches_in_separate_mode(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "First PROC FAR\n"
            "test ax, ax\n"
            "jz @F\n"
            "ret\n"
            "First ENDP\n"
            "Second PROC FAR\n"
            "@@: ret\n"
            "Second ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        rendered = cpp.write_procedures("", "sample.h")

        self.assertIn("if (GET_ZF()) return __dispatch_call(m2c::kdummylabel1, _state);", rendered)
        self.assertNotIn("JZ(dummylabel1)", rendered)

    def test_cross_proc_unconditional_jump_dispatches_in_single_mode(self):
        parser = Parser({"mergeprocs": "single"})
        source = (
            "CODE SEGMENT\n"
            "First PROC FAR\n"
            "jmp Next\n"
            "ret\n"
            "First ENDP\n"
            "Next PROC FAR\n"
            "ret\n"
            "Next ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        rendered = cpp.write_procedures("", "sample.h")

        self.assertIn("return next(0, _state);", rendered)
        self.assertNotIn("J(JMP(next))", rendered)

    def test_cross_proc_local_conditional_jump_dispatches_in_single_mode(self):
        parser = Parser({"mergeprocs": "single"})
        source = (
            "CODE SEGMENT\n"
            "First PROC FAR\n"
            "test ax, ax\n"
            "jz @F\n"
            "ret\n"
            "First ENDP\n"
            "Second PROC FAR\n"
            "@@: ret\n"
            "Second ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        rendered = cpp.write_procedures("", "sample.h")

        self.assertIn("if (GET_ZF()) return __dispatch_call(m2c::kdummylabel1, _state);", rendered)
        self.assertNotIn("JZ(dummylabel1)", rendered)

    def test_table_driven_jump_dispatch_keeps_synthetic_label_id(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "DATA SEGMENT\n"
            "Switch DW Target\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "Main PROC FAR\n"
            "mov bx,0\n"
            "jmp Switch[bx]\n"
            "Target: ret\n"
            "Main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        rendered = cpp.write_procedures("", "sample.h")

        self.assertIn("return __dispatch_call_ext(__disp, _state);", rendered)
        self.assertIn("case m2c::ktarget:", rendered)
        self.assertIn("m2c::stackDump(_state);", rendered)
        self.assertNotIn("__disp |= ((dd)cs) << 16", rendered)

    def test_assignment_codegen_is_noop(self):
        parser = Parser([])
        parser.action_assign_test(label="count", value="1")
        assignment = parser.symbols.get_global("count")
        cpp = Cpp(parser)

        self.assertEqual(cpp._assignment(assignment.children), "")
        self.assertEqual(cpp._cmdlabel, "")

    def test_assignment_values_are_snapshotted_for_data_initializers(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "X = 0\n"
            "Y = 0\n"
            "xy dw X,Y\n"
            "Y = Y+6\n"
            "xy2 dw X,Y\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        data = {d.label: d for segment in parser.segments.values() for d in segment.getdata()}
        cpp = Cpp(parser)

        self.assertEqual(cpp.produce_c_data_single_(data["xy"])[0], "{0,0}")
        self.assertEqual(cpp.produce_c_data_single_(data["xy2"])[0], "{0,0+6}")

    def test_assignment_values_are_resolved_in_instruction_operands(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "COUNT = 32\n"
            "MIDVAL = COUNT*2\n"
            "INDEX = COUNT*2\n"
            "start: mov [di+MIDVAL-INDEX], ax\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("mainproc").visit(cpp)

        self.assertIn("di+32*2-32*2", cpp.body)
        self.assertNotIn("#define", cpp.body)

    def test_parenthesized_location_counter_assignment_folds_to_integer_operand(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "Table dw 1,2,3,4\n"
            "TableWords = ($ - Table) / 2\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "cmp al, TableWords\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("CMP(al, 4)", cpp.body)
        self.assertNotIn("$", cpp.body)

    def test_structure_type_symbol_renders_as_type_size_in_instruction_operands(self):
        parser = Parser([])
        source = (
            "PACKET STRUCT\n"
            "Tag db 0\n"
            "Value dw 0\n"
            "PACKET ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov al, PACKET\n"
            "add bx, PACKET\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("R(al = 3;)", cpp.body)
        self.assertIn("ADD(bx, 3)", cpp.body)

    def test_equ_alias_to_proc_renders_as_call_target(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "Target PROC\n"
            "ret\n"
            "Target ENDP\n"
            "ProcAlias EQU Target\n"
            "main PROC\n"
            "call ProcAlias\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("CALL(target,0)", cpp.body)
        self.assertNotIn("CALL(procalias,0)", cpp.body)

    def test_call_followed_by_code_data_uses_inline_return_address(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "EQULTK EQU 0E7h\n"
            "SYNCHR PROC\n"
            "ret\n"
            "SYNCHR ENDP\n"
            "main PROC\n"
            "call SYNCHR\n"
            "db LOW OFFSET EQULTK\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("J(CALLI(synchr,0,m2c::near_offset_external(dummy0_code_0_8)));", cpp.body)

    def test_cmpsb_with_source_segment_override_renders_segment_macro(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            "cmpsb cs:[si], es:[di]\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("R(CMPSB_SEG(cs));", cpp.body)

    def test_data_label_displacement_destination_stays_addressable(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "Patch LABEL WORD\n"
            "db 3 dup(?)\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov Patch+1, bx\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("patch", cpp.body)
        self.assertIn("+1", cpp.body)
        self.assertNotIn("R(1 = bx;)", cpp.body)

    def test_data_label_difference_renders_as_offset_difference(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "Table db 1,2,3\n"
            "EndTable:\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov cx, EndTable - Table\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("R(cx = offset(data,endtable)-offset(data,table);)", cpp.body)

    def test_offset_equ_code_label_plus_constant_keeps_symbolic_base(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "Entry:\n"
            "BufPtr EQU Entry+128\n"
            "main PROC\n"
            "mov bx, OFFSET BufPtr\n"
            "mov dx, BufPtr\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("R(bx = m2c::kentry+128;)", cpp.body)
        self.assertIn("R(dx = m2c::kentry+128;)", cpp.body)
        self.assertNotIn("= 128;", cpp.body)

    def test_offset_external_word_keeps_shared_absolute_equate(self):
        parser = Parser({"shared_equates": {"ramlow": "256"}})
        source = (
            "DATA SEGMENT\n"
            "EXTRN RAMLOW:WORD\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov bx, OFFSET RAMLOW\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("R(bx = 256;)", cpp.body)
        self.assertNotIn("near_offset_external(ramlow)", cpp.body)

    def test_unresolved_continuation_data_reference_uses_external_offset(self):
        parser = Parser({"filenames": ["math1.asm", "math2.asm"], "mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            "mov bx, WORD PTR FacValue\n"
            "mov WORD PTR FacValue, bx\n"
            "mov di, OFFSET FacValue\n"
            "mov si, OFFSET ?CSLAB\n"
            "ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser, "math2.cpp")

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("raddr(ds,m2c::near_offset_external(facvalue))", cpp.body)
        self.assertIn("R(di = m2c::near_offset_external(facvalue);)", cpp.body)
        self.assertIn("R(si = m2c::kquecslab;)", cpp.body)
        self.assertNotIn("raddr(ds,facvalue)", cpp.body)

    def test_offset_of_materialized_code_label_uses_aggregate_dispatch_constant(self):
        parser = Parser({
            "filenames": ["producer.asm", "consumer.asm"],
            "mergeprocs": "separate",
        })
        source = (
            "CODE SEGMENT\n"
            "PUBLIC Target\n"
            "Target:\n"
            "    ret\n"
            "main PROC\n"
            "    mov cx, OFFSET Target\n"
            "    ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        parser.symbols.get_global("main").visit(cpp)

        self.assertIn("R(cx = m2c::kglobal_target;)", cpp.body)
        self.assertNotIn("R(cx = m2c::ktarget;)", cpp.body)

    def test_nested_segment_restores_outer_location_counter(self):
        parser = Parser([])
        source = (
            "CSEG SEGMENT PUBLIC 'CODESG'\n"
            "ORG 100h\n"
            "CopyLen=CopyEnd-CopyStart\n"
            "StartBytes db 1\n"
            "CopyStart=$\n"
            "DSEG SEGMENT PUBLIC 'DATASG'\n"
            "ORG 2\n"
            "DataBytes db 2\n"
            "DSEG ENDS\n"
            "MoreCode db 3\n"
            "CopyEnd=$\n"
            "CSEG ENDS\n"
            "END\n"
        )

        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        cseg_rows = {data.label: data.offset for data in parser.segments["cseg"].getdata()}
        dseg_rows = {data.label: data.offset for data in parser.segments["dseg"].getdata()}

        self.assertEqual(cseg_rows["startbytes"], 0x100)
        self.assertEqual(cseg_rows["morecode"], 0x101)
        self.assertEqual(dseg_rows["databytes"], 0x2)
        self.assertEqual(Cpp(parser).render_equate_value(parser.symbols.get_global("copylen")), "258-257")

    def test_two_pass_forward_location_counter_assignment_uses_captured_offsets(self):
        source = (
            "CSEG SEGMENT PUBLIC 'CODESG'\n"
            "ORG 100h\n"
            "CopyLen=CopyEnd-CopyStart\n"
            "CopyStart=$\n"
            "db 1,2,3\n"
            "CopyEnd=$\n"
            "CSEG ENDS\n"
            "END\n"
        )
        with TemporaryDirectory() as tmp:
            asm = Path(tmp) / "copy.asm"
            asm.write_text(source, encoding="ascii")
            parser = Parser([])
            parser.parse_file(str(asm))
            parser.next_pass(0)
            parser.parse_file(str(asm))

        self.assertEqual(Cpp(parser).render_equate_value(parser.symbols.get_global("copylen")), "259-256")

    def test_assignment_to_data_label_records_addressable_alias(self):
        parser = Parser([])
        source = (
            "DATA SEGMENT\n"
            "Base LABEL WORD\n"
            "db 4 dup(?)\n"
            "DataAlias = Base + 1\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        aliases = {alias.name: alias for alias in parser.data_aliases}

        self.assertEqual(aliases["dataalias"].segment, "data")
        self.assertEqual(aliases["dataalias"].offset, 1)

    def test_public_code_label_after_data_is_not_trailing_data_alias(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "PUBLIC EntryPoint\n"
            "Table db 1,2,3\n"
            "EntryPoint:\n"
            "ret\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        aliases = {alias.name for alias in parser.data_aliases}

        self.assertNotIn("entrypoint", aliases)
        self.assertIsInstance(parser.symbols.get_global("entrypoint"), op.label)

    def test_code_label_after_code_segment_data_remains_callable(self):
        parser = Parser([])
        source = (
            "CODE SEGMENT\n"
            "Entry:\n"
            "call Handler\n"
            "ret\n"
            "Table dw OFFSET Target\n"
            "Handler:\n"
            "call Target\n"
            "DATA SEGMENT\n"
            "EXTRN SomeVar:WORD\n"
            "DATA ENDS\n"
            "ret\n"
            "Target:\n"
            "ret\n"
            "CODE ENDS\n"
            "END Entry\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        aliases = {alias.name for alias in parser.data_aliases}
        rendered = Cpp(parser).write_procedures("", "sample.h")

        self.assertNotIn("handler", aliases)
        self.assertIsInstance(parser.symbols.get_global("handler"), op.label)
        self.assertIn("J(CALL(mainproc,m2c::khandler));", rendered)
        self.assertNotIn("CALL(__dispatch_call,handler)", rendered)

    def test_code_segment_db_skip_opcode_skips_following_byte_on_fallthrough(self):
        parser = Parser([])
        source = (
            "CSEG SEGMENT PUBLIC 'CODESG'\n"
            "main PROC\n"
            "start:\n"
            "mov dx, 1234h\n"
            "db 260O ; SKIP next opcode byte\n"
            "SkipTarget:\n"
            "push dx\n"
            "mov ax, 1\n"
            "ret\n"
            "main ENDP\n"
            "CSEG ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = Cpp(parser).write_procedures("", "sample.h")

        self.assertIn("R({al = 0x52;goto __m2c_skip_1;});", rendered)
        self.assertIn("skiptarget:\n", rendered)
        self.assertIn("R(PUSH(dx));\n__m2c_skip_1:", rendered)

    def test_code_segment_data_byte_without_skip_comment_stays_data_only(self):
        parser = Parser([])
        source = (
            "CSEG SEGMENT PUBLIC 'CODESG'\n"
            "main PROC\n"
            "start:\n"
            "db 271O\n"
            "ret\n"
            "main ENDP\n"
            "CSEG ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = Cpp(parser).write_procedures("", "sample.h")

        self.assertNotIn("__m2c_skip_", rendered)

    def test_code_segment_skip_opcode_can_skip_symbolic_mov_immediate(self):
        parser = Parser([])
        source = (
            "CSEG SEGMENT PUBLIC 'CODESG'\n"
            "ERRSN EQU 2\n"
            "ERRNF EQU 1\n"
            "main PROC\n"
            "SnErr: mov dl, LOW OFFSET ERRSN\n"
            "db 271O ; SKIP over next error setter\n"
            "NfErr: mov dl, LOW OFFSET ERRNF\n"
            "Done: ret\n"
            "main ENDP\n"
            "CSEG ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = Cpp(parser).write_procedures("", "sample.h")

        self.assertIn("R(dl = 2 & 0xff;);", rendered)
        self.assertIn("R(dl = 1 & 0xff;);\n__m2c_skip_1:", rendered)

    def test_member_access_promotes_scalar_external_to_unique_struct_type(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "EXTRN V_VIEW:WORD\n"
            "VIEWPOINT STRUCT\n"
            "VP_PITCH DW 0\n"
            "VIEWPOINT ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = parser.parse_arg("V_VIEW.VP_PITCH")

        self.assertEqual(rendered, "v_view.vp_pitch")
        self.assertEqual(parser.symbols.get_global("v_view").original_type, "viewpoint")

    def test_m510_register_pointer_member_renders_memory_lvalue(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "PACK STRUCT\n"
            "PACK_WEAP_TYPE DW 0\n"
            "PACK ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = parser.parse_arg("[si].PACK_WEAP_TYPE")

        self.assertEqual(rendered, "*((dw*)raddr(ds,si+pack_weap_type))")

    def test_m510_member_before_register_pointer_renders_memory_lvalue(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "TAB STRUCT\n"
            "TAB_HAS_MOUSE DB 0\n"
            "TAB ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = parser.parse_arg("TAB_HAS_MOUSE.[si]")

        self.assertEqual(rendered, "*((db*)raddr(ds,si+tab_has_mouse))")

    def test_m510_array_member_pointer_uses_operand_size_not_array_size(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "MODEL STRUCT\n"
            "MOD_FILENAME DB 8 DUP (' ')\n"
            "MODEL ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = parser.parse_arg("[si].MOD_FILENAME", def_size=1)

        self.assertEqual(rendered, "*((db*)raddr(ds,si+mod_filename))")

    def test_m510_bracketed_member_uses_member_width_for_store(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "MOBSORT STRUCT\n"
            "MSORT_XSEC DW 0\n"
            "MSORT_YSEC DW 0\n"
            "MSORT_PTR DW 0\n"
            "MOBSORT ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = Proc("x").generate_c_cmd(Cpp(parser), parser.action_code("mov MSORT_PTR[bx], -1"))

        self.assertEqual(rendered, "MOV(*(dw*)(raddr(ds,msort_ptr+bx)), -1)")

    def test_m510_bracketed_label_member_renders_memory_lvalue(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "PACK STRUCT\n"
            "WP_ID DB 0\n"
            "PACK ENDS\n"
            "DATA SEGMENT\n"
            "WPPtr DW 0\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = parser.parse_arg("[WPPtr].WP_ID")

        self.assertEqual(rendered, "*((db*)raddr(ds,offset(data,wpptr)+wp_id))")

    def test_m510_old_struct_member_offset_constant_is_renamed_when_global_conflicts(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "TAB STRUCT\n"
            "TAB_HAS_MOUSE DB 0\n"
            "TAB ENDS\n"
            "DATA SEGMENT\n"
            "TAB_HAS_MOUSE DB 1\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        structures = Cpp(parser).produce_structures(parser.structures)
        rendered = parser.parse_arg("TAB_HAS_MOUSE.[si]")

        self.assertIn("static const word __m2c_member_tab_has_mouse = offsetof(struct tab, tab_has_mouse);", structures)
        self.assertEqual(rendered, "*((db*)raddr(ds,si+__m2c_member_tab_has_mouse))")

    def test_m510_old_struct_member_offset_constant_is_renamed_when_data_label_conflicts(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "ENDROUTE STRUCT\n"
            "DUMMY8_0 DB 0\n"
            "ENDROUTE ENDS\n"
            "DATA SEGMENT\n"
            "DUMMY8_0 DB 1\n"
            "DATA ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        structures = Cpp(parser).produce_structures(parser.structures)

        self.assertIn("static const word __m2c_member_dummy8_0 = offsetof(struct endroute, dummy8_0);", structures)
        self.assertNotIn("static const word dummy8_0 = offsetof(struct endroute, dummy8_0);", structures)

    def test_struct_member_equ_alias_renders_offset_lvalue(self):
        parser = Parser([])
        source = (
            "OPTION M510\n"
            "EXTRN V_VIEW:VIEWPOINT\n"
            "VIEWPOINT STRUCT\n"
            "VP_ZFT DD 0\n"
            "VIEWPOINT ENDS\n"
            "VP_ZFT_HI EQU VP_ZFT+2\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        rendered = parser.parse_arg("V_VIEW.VP_ZFT_HI")

        self.assertEqual(rendered, "*((dw*)((db*)&v_view+vp_zft_hi))")

    def test_exported_code_symbols_dispatch_by_sidecar_offsets(self):
        parser = Parser([])
        label = op.label("shared_handler", proc="mainproc")
        label.used = True
        label.public_export = True
        label.real_offset = 0x2345
        parser.symbols.set_global("shared_handler", label)

        cpp = Cpp(parser)
        offsets = cpp.export_defined_code_symbol_offsets()

        self.assertEqual(offsets["shared_handler"], 0x2345)

        parser.exported_code_symbol_offsets = {"shared_handler": 0x2345}
        parser.exported_callable_code_symbol_offsets = {"shared_handler": 0x2345}
        declarations = cpp._produce_external_code_declarations()
        dispatcher = cpp._produce_external_code_dispatcher()

        self.assertIn("extern bool shared_handler(m2c::_offsets, struct m2c::_STATE*);", declarations)
        self.assertIn("case 0x2345:", dispatcher)
        self.assertIn("return shared_handler(0, _state);", dispatcher)

    def test_non_public_code_labels_do_not_export_for_merged_dispatch(self):
        parser = Parser([])
        label = op.label("local_handler", proc="mainproc")
        label.used = True
        label.real_offset = 0x3456
        parser.symbols.set_global("local_handler", label)

        cpp = Cpp(parser)
        offsets = cpp.export_defined_code_symbol_offsets()
        parser.exported_code_symbol_offsets = {}
        parser.exported_callable_code_symbol_offsets = {}

        self.assertEqual(offsets["local_handler"], 0x3456)
        self.assertNotIn("local_handler", cpp._produce_external_code_declarations())
        self.assertNotIn("local_handler", cpp._produce_external_code_dispatcher())

    def test_sidecar_code_offsets_reserve_synthetic_begin_dispatch_id(self):
        self.assertEqual(Cpp(Parser([])).export_defined_code_symbol_offsets()["begin"], 0x1001)

    def test_aggregate_code_offsets_keep_exported_main_label(self):
        exported, callable_offsets = Cpp(Parser([]))._assign_aggregate_code_offsets(
            {"main": 0x2000},
            {"main"},
            {"main"},
            {},
            set(),
            set(),
        )

        self.assertIn("main", exported)
        self.assertIn("main", callable_offsets)


class DuplicateLocalCodeSymbolTest(unittest.TestCase):
    """Module-local code symbols defined in several modules must not collide.

    Tornado's VSCREEN and COM_CLIP both define private PolyClipRight procs
    (NEAR, not PUBLIC, never EXTRN-referenced).  The generated TUs still emit
    them with weak linkage (translate-time export scans mark them), so the
    linker would otherwise silently merge two different procedures.
    """

    def _merge_two_local_definers(self):
        tmp = TemporaryDirectory()
        old_cwd = os.getcwd()
        os.chdir(tmp.name)
        self.addCleanup(os.chdir, old_cwd)
        self.addCleanup(tmp.cleanup)
        writer = Cpp(Parser([]))
        for mod in ("com_clip.asm", "vscreen.asm"):
            writer.write_segment_file(
                OrderedDict(),
                OrderedDict(),
                mod,
                defined_code_symbols={"polyclipright"},
                defined_code_symbol_offsets={"polyclipright": 0x100},
            )
        merger = Cpp(Parser([]), merge_data_segments=True)
        merger.write_data_segments_cpp(*merger.read_segment_files(["com_clip.asm", "vscreen.asm"]))
        return merger

    def test_non_keeper_definer_gets_module_qualified_rename(self):
        self._merge_two_local_definers()
        equates = Path("_equates.h").read_text(encoding="cp437")

        self.assertIn("#if defined(M2C_MODULE_COM_CLIP)", equates)
        self.assertIn("#define polyclipright polyclipright__com_clip", equates)

    def test_last_definer_keeps_canonical_name(self):
        self._merge_two_local_definers()
        equates = Path("_equates.h").read_text(encoding="cp437")

        self.assertNotIn("polyclipright__vscreen", equates)

    def test_code_segment_db_label_renders_goto_case_and_no_wrapper(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            "loop1: db 026h\n"
            "    lodsb\n"
            "    cmp al,-1\n"
            "    jz done\n"
            "    jmp loop1\n"
            "done: ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        cpp.generate_label_to_proc_map()
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        # The label stays a code position: the jump dispatches by code offset
        # into the owning proc rather than reading the data byte's value.
        self.assertIn("loop1", cpp.label_to_proc)
        self.assertIn("kloop1", rendered)
        self.assertNotIn("__disp=loop1", rendered)
        # The ES prefix byte applies to the lodsb (raddr(es,si), not ds).
        self.assertIn("raddr(es,si)", rendered)
        # The name is also a data variable for byte-level references.
        self.assertIsInstance(parser.symbols.get_global("loop1"), op.var)
        # A wrapper function would collide with the data symbol; the label is
        # reached through the owning proc's dispatch instead.
        self.assertNotIn("loop1", cpp._label_wrapper_targets())
        # The exported code offset is the label's position, not a data slot.
        self.assertGreater(
            cpp.export_defined_code_symbol_offsets().get("loop1", 0), 0x1000
        )

    def test_code_segment_db_prefix_is_consumed_by_next_instruction_only(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            "    db 02eh\n"
            "    lodsb\n"
            "    lodsb\n"
            "    ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        # CS prefix applies to the first lodsb only; the second falls back to
        # the plain ds-based LODSB macro.
        self.assertEqual(rendered.count("raddr(cs,si)"), 1)
        self.assertIn("LODSB", rendered)

    def test_data_segment_db_prefix_byte_does_not_override(self):
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "DATA SEGMENT\n"
            "byte26 db 026h\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            "    lodsb\n"
            "    ret\n"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)

        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

        self.assertIn("LODSB", rendered)
        self.assertNotIn("raddr(es,si)", rendered)

    def test_mainproc_is_never_qualified(self):
        with TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                writer = Cpp(Parser([]))
                for mod in ("alpha.asm", "beta.asm"):
                    writer.write_segment_file(
                        OrderedDict(),
                        OrderedDict(),
                        mod,
                        defined_code_symbols={"mainproc"},
                        defined_code_symbol_offsets={"mainproc": 0x100},
                    )
                merger = Cpp(Parser([]), merge_data_segments=True)
                merger.write_data_segments_cpp(*merger.read_segment_files(["alpha.asm", "beta.asm"]))

                equates = Path("_equates.h").read_text(encoding="cp437")
                self.assertNotIn("mainproc__", equates)
            finally:
                os.chdir(old_cwd)


class IndirectDispatchPointerSizeTest(unittest.TestCase):
    def _render_main(self, body: str) -> str:
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            f"{body}"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        return "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

    def _render_main_with_dispatch(self, body: str) -> str:
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "CODE SEGMENT\n"
            "main PROC\n"
            f"{body}"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        rendered = "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)
        return rendered + "\n" + cpp.dispatch

    def test_unsized_indirect_jump_reads_word(self):
        # ``jmp [bx]`` is a near jump through a word pointer; without an
        # explicit ``word ptr`` annotation it must still dereference a dw.
        rendered = self._render_main_with_dispatch("    jmp [bx]\n")
        self.assertIn("__disp=*(dw*)(raddr(ds,bx))", rendered)

    def test_unsized_indirect_call_reads_word(self):
        rendered = self._render_main("    call [si]\n")
        self.assertIn("*(dw*)(raddr(ds,si))", rendered)

    def test_annotated_far_indirect_call_reads_dword(self):
        rendered = self._render_main("    call dword ptr [bp]\n")
        self.assertIn("*(dd*)(raddr(ss,bp))", rendered)


class OperatorEquateInstructionTest(unittest.TestCase):
    """EQU values built on SIZE/TYPE/SEG must not degrade to label offsets.

    ``_render_known_offset_expression`` used to descend into single-child
    operator nodes and render only the label operand, so ``SIZE LhsX``
    became ``offset(data,lhsx)`` in instruction operands such as
    ``add ax,BUF_SIZE``.  Tornado's polygon filler relies on
    ``BUF_SIZE EQU SIZE LhsX`` (0x190) to jump between the lhs/rhs scanline
    tables; the miscompiled add poisoned RhsPtr and corrupted memory.
    """

    @staticmethod
    def _render(body: str) -> str:
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "DATA SEGMENT\n"
            "LhsX DW 200 DUP(0)\n"
            "BUF_SIZE EQU SIZE LhsX\n"
            "SEG_EQU EQU SEG LhsX\n"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            f"{body}"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        return "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

    def test_size_equate_renders_total_byte_size(self):
        rendered = self._render("    add ax,BUF_SIZE\n    sub ax,BUF_SIZE\n")
        self.assertIn("ADD(ax, 400)", rendered)
        self.assertIn("SUB(ax, 400)", rendered)
        self.assertNotIn("offset(data,lhsx)", rendered)

    def test_size_equate_memory_operand_uses_constant_base(self):
        rendered = self._render("    cmp ax,BUF_SIZE[di]\n    cmp ax,-BUF_SIZE[di]\n")
        self.assertIn("raddr(ds,400+di)", rendered)
        self.assertIn("raddr(ds,-400+di)", rendered)
        self.assertNotIn("offset(data,lhsx)", rendered)

    def test_type_operator_renders_element_size(self):
        rendered = self._render("    add ax,TYPE LhsX\n")
        self.assertIn("ADD(ax, 2)", rendered)

    def test_seg_operator_renders_segment_offset(self):
        rendered = self._render("    mov ax,SEG_EQU\n")
        self.assertIn("seg_offset(", rendered)
        self.assertNotIn("offset(data,lhsx)", rendered)


class BracketedBaseMemberTest(unittest.TestCase):
    """``expr[reg].member`` must keep every addend of the bracketed base.

    ``memberdir`` used to emit only ``__memptr_<reg>`` whenever the bracket
    contained a register, silently dropping label/equate siblings.  Tornado
    corrupts its mobile list because ``MOB_REC_SIZE[si].VP_XFT``
    (``MOB_REC_SIZE EQU TYPE MOBILE`` = 6) rendered ``si+vp_xft`` -> ``si+4``,
    which is the MOBILE.MOB_LINK_PTR field.  The same drop hit
    ``RWRThreats[bp].X`` / ``EWRTable[bx].X`` array-of-struct accesses.
    """

    @staticmethod
    def _render(body: str, extra_data: str = "") -> str:
        parser = Parser({"mergeprocs": "separate"})
        source = (
            "MOBILE STRUCT\n"
            "MOB_NUM DB 0\n"
            "MOB_TYPE DB 0\n"
            "MOB_ANIM DB 0\n"
            "MOB_LINK_PTR DW -1\n"
            "MOBILE ENDS\n"
            "VIEWPOINT STRUCT\n"
            "VP_XSEC DW 0\n"
            "VP_YSEC DW 0\n"
            "VP_XFT DW 0\n"
            "VP_YFT DW 0\n"
            "VIEWPOINT ENDS\n"
            "MOB_REC_SIZE EQU TYPE MOBILE\n"
            "DATA SEGMENT\n"
            "mobarr MOBILE 5 DUP(<>)\n"
            f"{extra_data}"
            "DATA ENDS\n"
            "CODE SEGMENT\n"
            "main PROC\n"
            f"{body}"
            "main ENDP\n"
            "CODE ENDS\n"
            "END\n"
        )
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        proc = parser.symbols.get_global("main")
        cpp = Cpp(parser)
        return "\n".join(proc.generate_c_cmd(cpp, stmt) for stmt in proc.stmts)

    def test_scalar_equ_base_preserves_displacement(self):
        rendered = self._render(
            "    add ax,MOB_REC_SIZE[si].VP_XFT\n"
            "    mov MOB_REC_SIZE[si].VP_YFT,ax\n"
        )
        self.assertIn("raddr(ds,mob_rec_size+si+vp_xft)", rendered)
        self.assertIn("raddr(ds,mob_rec_size+si+vp_yft)", rendered)
        self.assertNotIn("raddr(ds,si+vp_xft)", rendered)

    def test_var_array_base_preserves_offset(self):
        rendered = self._render("    add ax,mobarr[si].MOB_LINK_PTR\n")
        self.assertIn("raddr(ds,offset(data,mobarr)+si+mob_link_ptr)", rendered)

    def test_bracket_expression_keeps_constant_term(self):
        rendered = self._render("    add ax,mobarr[si+2].MOB_NUM\n")
        self.assertIn("raddr(ds,offset(data,mobarr)+si+2+mob_num)", rendered)

    def test_bare_register_member_unchanged(self):
        rendered = self._render("    add ax,[si].MOB_LINK_PTR\n")
        self.assertIn("raddr(ds,si+mob_link_ptr)", rendered)


if __name__ == "__main__":
    unittest.main()
