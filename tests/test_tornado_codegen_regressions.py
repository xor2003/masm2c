import unittest
import os
from collections import OrderedDict
from pathlib import Path
from tempfile import TemporaryDirectory

from masm2c import op
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
        second = op.Segment("wpndata", 0, options={"public"}, segclass="data")
        second.append(op.Data("weaponlist", "dw", op.DataType.NUMBER, [2], 1, 2))
        cpp = Cpp(Parser([]), merge_data_segments=True)

        segments, _ = cpp.merge_segments(OrderedDict([("data", first)]), OrderedDict(), OrderedDict([("wpndata", second)]), OrderedDict())

        self.assertEqual(segments["data"].segment_aliases["data"], 0)
        self.assertEqual(segments["data"].segment_aliases["wpndata"], 2)
        self.assertEqual(segments["data"].getdata()[1].offset, 2)

    def test_duplicate_public_segment_data_offsets_are_relocated_during_merge(self):
        first = op.Segment("data", 0, options={"public"}, segclass="data")
        first.append(op.Data("jumpinitlist", "dw", op.DataType.NUMBER, [0], 1, 2, offset=0x14A))
        second = op.Segment("data", 0, options={"public"}, segclass="data")
        second.append(op.Data("gameplaydata", "db", op.DataType.ARRAY, [0], 1, 1, offset=0x180))
        cpp = Cpp(Parser([]), merge_data_segments=True)

        segments, _ = cpp.merge_segments(OrderedDict([("data", first)]), OrderedDict(), OrderedDict([("data", second)]), OrderedDict())

        self.assertEqual(segments["data"].getdata()[1].offset, 0x182)

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
                self.assertEqual(alias.offset, 0x182)
            finally:
                os.chdir(old_cwd)

    def test_data_alias_from_merged_segment_alias_is_rendered(self):
        parser = Parser([])
        segment = op.Segment("data", 0)
        segment.segment_aliases["wpndata"] = 2
        parser.segments = OrderedDict([("data", segment)])
        parser.data_aliases = [
            op.var(2, 0, "weaponlist", segment="wpndata", elements=1, original_type="word")
        ]

        _, _, data_cpp, hpp = Cpp(parser).render_data_c(parser.segments)

        self.assertIn("db& wpndata=*((db*)&m2c::m+0x2);", data_cpp)
        self.assertIn("word& weaponlist=*((word*)(&wpndata+0x0));", data_cpp)
        self.assertIn("extern word& weaponlist;", hpp)

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
                self.assertIn("dw& localref = m2c::m.localref;", data_refs)
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

    def test_external_offset_instruction_does_not_update_segment_register(self):
        parser = Parser([])
        parser.add_extern("PilotPanel", "BYTE")
        rendered = Proc("mainproc").generate_c_cmd(Cpp(parser), parser.action_code("mov dx, OFFSET PilotPanel"))

        self.assertEqual(rendered, "dx = m2c::near_offset_external(pilotpanel);")

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

        self.assertIn("static const word vp_pitch = offsetof(viewpoint, vp_pitch);", structures)

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
            "bool drawfeatures2(m2c::_offsets, struct m2c::_STATE* _state){return drawfeatures1(m2c::kdrawfeatures2, _state);}",
            wrappers,
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

    def test_external_scalar_data_declares_reference_to_aggregate_storage(self):
        parser = Parser([])
        source = "EXTRN PSP:WORD\nCODE SEGMENT\nmain PROC\nmov PSP, ax\nret\nmain ENDP\nCODE ENDS\nEND\n"
        tree = parser.parse_text(source)
        parser.process_ast(source, tree)
        cpp = Cpp(parser)

        declarations = cpp.produce_externals(parser)

        self.assertIn("extern dw& psp;", declarations)
        self.assertNotIn("extern word psp;", declarations)

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
                self.assertIn("{reinterpret_cast<const db*>(&::data), 0x0}", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::wsdata), 0x200}", data_cpp)
                self.assertIn("{reinterpret_cast<const db*>(&::stack), 0x550}", data_cpp)
                self.assertNotIn("{reinterpret_cast<const db*>(&::code), 0x10}", data_cpp)
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

        self.assertIn("return __dispatch_call(__disp, _state);", rendered)
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

        self.assertEqual(rendered, "*((db*)raddr(ds,wpptr+wp_id))")

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

        self.assertIn("static const word __m2c_member_tab_has_mouse = offsetof(tab, tab_has_mouse);", structures)
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

        self.assertIn("static const word __m2c_member_dummy8_0 = offsetof(endroute, dummy8_0);", structures)
        self.assertNotIn("static const word dummy8_0 = offsetof(endroute, dummy8_0);", structures)

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


if __name__ == "__main__":
    unittest.main()
