"""
Responsible for generating C++ code specifically.
It might handle tasks like converting assembly labels to C++ identifiers, generating function prototypes,
and handling C++ specific constructs.
"""
# Masm2c S2S translator (initially based on SCUMMVM tasmrecover)
#
# Masm2c is the legal property of its developers, whose names
# are too numerous to list here. Please refer to the COPYRIGHT
# file distributed with this source distribution.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
import logging
from typing import TYPE_CHECKING, Any, Union

from lark.lexer import Token
from lark.tree import Tree

from masm2c.Token import Token as Token_, Expression
from masm2c.op import Data, Struct

if TYPE_CHECKING:
    from masm2c.parser import Parser

import os
import re
import glob
from collections import OrderedDict
from copy import copy, deepcopy

from lark import lark

from . import op
from masm2c.proc import Proc
from .enumeration import IndirectionType
from .gen import Gen, mangle_asm_labels
from .pgparser import LABEL, MEMBERDIR, REGISTER, SQEXPR, Asm2IR


def flatten(s: list) -> list:
    if not s:
        return s
    if isinstance(s[0], list):
        return flatten(s[0]) + flatten(s[1:])
    return s[:1] + flatten(s[1:])


RT_DATA_OFFSET = 1 << 0
RT_CODE_OFFSET = 1 << 1
RT_STRING = 1 << 2
RT_SEGMENT = 1 << 3
RT_FAR_POINTER = 1 << 4
CPP_STRUCT_TAG_REQUIRED = {"clock"}
DATA_REF_LINES_PER_FILE = 2000


def _parse_runtime_int(value: Any) -> int | None:
    try:
        if isinstance(value, str):
            try:
                return int(value, 0)
            except Exception:
                if re.search(r"[a-fA-F]", value):
                    return int(value, 16)
                return int(value)
        return int(value)
    except Exception:
        return None


class _ExprRenderState:
    __slots__ = (
        "needs_dereference",
        "is_pointer",
        "struct_type",
        "is_variable",
        "is_label",
        "is_just_label",
        "is_just_member",
        "is_member",
        "need_pointer_to_member",
        "size_changed",
        "variable_size",
        "work_segment",
        "indirection",
        "element_size",
        "data_label_size",
    )

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.needs_dereference = False
        self.is_pointer = False
        self.struct_type: str | None = None
        self.is_variable = False
        self.is_label = False
        self.is_just_label = False
        self.is_just_member = False
        self.is_member = False
        self.need_pointer_to_member: list[str] = []
        self.size_changed = False
        self.variable_size = 0
        self.work_segment = "ds"
        self.indirection = IndirectionType.VALUE
        self.element_size = -1
        self.data_label_size = 0


class SeparateProcStrategy:

    def __init__(self, renderer: "Cpp") -> None:
        self.renderer = renderer

    def produce_proc_start(self, name):
        return f" // Procedure {name}() start\n{self.renderer.mangle_label(name)}()\n{{\n"

    def function_header(self, name, entry_point=""):
        linkage = self.renderer.function_linkage(name)
        header = """

 %sbool %s(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;
""" % (linkage, self.renderer.mangle_label(name))

        if entry_point != "":
            header += """
    if (__disp == kbegin) goto %s;
""" % entry_point

        header += """
    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    %s:
    _begin:
""" % self.renderer.mangle_label(name)
        return header

    def write_declarations(self, procs, context):
        result = ""
        external_proc_data_refs = getattr(context, "external_proc_data_refs", {})
        for p in sorted(procs):  # TODO only if used or public
            result += "%sbool %s(m2c::_offsets, struct m2c::_STATE*);\n" % (
                self.renderer.wrapper_linkage(p),
                self.renderer.mangle_label(p),
            )

        for i in sorted(context.externals_procs):
            v = context.symbols.get_global(i)
            if isinstance(v, Proc) and v.used and i not in external_proc_data_refs:
                result += f"extern bool {self.renderer.mangle_label(v.name)}(m2c::_offsets, struct m2c::_STATE*);\n"

        result += """
static bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state);
static bool __dispatch_call_ext(m2c::_offsets __disp, struct m2c::_STATE* _state);
"""
        return result


class Cpp(Gen):
    """Visitor which can produce C++ equivalents for asm instructions."""

    def __init__(self, context: "Parser", outfile: str = "", merge_data_segments: bool = True) -> None:
        # proc_strategy = SingleProcStrategy()):
        """:param context: pointer to Parser data
        :param outfile: Output filename
        """
        self._expr_state = _ExprRenderState()
        self._data_label_renames: list[tuple[str, str, str]] = []
        super().__init__(context, outfile=outfile, merge_data_segments=merge_data_segments)
        self.proc_strategy = SeparateProcStrategy(self)
        self.renderer: Gen = self
        self._namespace = os.path.basename(outfile)
        self.__codeset = "cp437"

        #
        self.__proc_done: list[str] = []
        self.__failed: list[str] = []
        self._proc_addr: list[tuple[str,int]] = []
        #self.__used_data_offsets = set()
        self.__methods: list[str] = []
        self.__pushpop_count = 0
        self._rt_symbol_exact_by_linear: dict[int, tuple[str, Any]] | None = None
        self._rt_var_ranges_by_linear: list[tuple[int, int, str, Any]] | None = None
        self._linked_data_offsets_enabled_cache: bool | None = None
        self._assignments: dict[str, Expression] = {}
        self._expr_state.is_member = False

        self.far = False
        self._active_proc_far = False
        self._pending_external_offset_ds_restore = False
        self._pending_data_offset_ds_restore = False
        self._pending_code_skip: dict[str, Any] | None = None
        self._code_skip_label_counter = 0
        self._current_stmt: op.baseop | None = None
        self._next_stmt: op.baseop | None = None
        self._expr_state.reset()

        self.itisjump = False
        self.itiscall = False
        self.__type_table = {op.DataType.NUMBER: self.produce_c_data_number,
                             op.DataType.ARRAY: self.produce_c_data_array,
                             op.DataType.ZERO_STRING: self.produce_c_data_zero_string,
                             op.DataType.ARRAY_STRING: self.produce_c_data_array_string,
                             op.DataType.OBJECT: self.produce_c_data_object,
                             }

    def _linked_data_offsets_enabled(self) -> bool:
        if self._linked_data_offsets_enabled_cache is not None:
            return self._linked_data_offsets_enabled_cache

        filenames = self._context.args.get("filenames", []) if isinstance(self._context.args, dict) else []
        if isinstance(filenames, str):
            filenames = [filenames]

        sources: list[str] = []
        for filename in filenames:
            matches = glob.glob(filename)
            sources.extend(matches or [filename])

        asm_sources = [source for source in sources if source.lower().endswith((".asm", ".lst"))]
        self._linked_data_offsets_enabled_cache = len(asm_sources) > 1
        return self._linked_data_offsets_enabled_cache

    def _should_emit_linked_data_offset(self, symbol: op.var) -> bool:
        return (
            not symbol.external
            and not symbol.issegment
            and not self._expr_state.data_label_size
            and self._linked_data_offsets_enabled()
        )

    def _near_data_offset_expr(self, symbol: op.var, label: str) -> str:
        """Render a 16-bit OFFSET expression without changing register state."""
        if self._should_emit_linked_data_offset(symbol):
            return f"m2c::near_offset_external({label})"
        return f"offset({symbol.segment},{label})"

    def _far_data_offset_expr(self, symbol: op.var, label: str) -> str:
        if self._should_emit_linked_data_offset(symbol):
            return f"m2c::far_offset_external({label})"
        return f"far_offset({symbol.segment},{label})"

    def function_linkage(self, name: str) -> str:
        if self._uses_weak_code_linkage(name):
            return "__attribute__((weak)) "
        if name in getattr(self._context, "public_symbols", set()):
            return ""
        return "static "

    def _uses_weak_code_linkage(self, name: str) -> bool:
        """Return true for exported code definitions in multi-module output."""
        if self._is_cross_module_code_definition(name):
            return True
        if name in self._data_referenced_code_symbol_names():
            return True
        if name in self._instruction_offset_referenced_code_symbol_names():
            return True
        return name in getattr(self._context, "public_symbols", set()) and self._linked_data_offsets_enabled()

    def _is_cross_module_code_definition(self, name: str) -> bool:
        """Return true when this module owns the exported code symbol."""
        symbol = self._context.symbols.get_global(name)
        if isinstance(symbol, Proc) and symbol.extern:
            return False
        if not isinstance(symbol, (Proc, op.label)):
            return False
        if getattr(symbol, "public_export", False):
            return True
        if name in getattr(self._context, "public_symbols", set()):
            return True
        if self._is_continuation_module() and self._is_cross_module_code_export(name):
            return True
        if self._is_public_code_offset_export(name):
            return False
        return self._is_cross_module_code_export(name)

    def _is_cross_module_code_export(self, name: str) -> bool:
        """Return true when a code symbol may be referenced across modules."""
        args = self._context.args if isinstance(self._context.args, dict) else {}
        exports = list(args.get("external_code_exports", [])) + list(args.get("public_code_exports", []))
        return self.sanitize_label_name(name) in {self.sanitize_label_name(str(item)) for item in exports}

    def _is_public_code_offset_export(self, name: str) -> bool:
        """Return true when the aggregate equates header owns a code offset."""
        args = self._context.args if isinstance(self._context.args, dict) else {}
        exports = args.get("public_code_exports", [])
        return self.sanitize_label_name(name) in {self.sanitize_label_name(str(item)) for item in exports}

    def _is_continuation_module(self) -> bool:
        namespace = os.path.splitext(self._namespace.lower() or "")[0]
        return re.fullmatch(r".*[A-Za-z][2-9]", namespace) is not None and not namespace.endswith("86")

    @staticmethod
    def _is_mangled_internal_code_label(name: str) -> bool:
        """Return true for MASM generated/internal labels mangled from '?' names."""
        return str(name).lower().startswith("que")

    def wrapper_linkage(self, name: str, *, public: bool | None = None) -> str:
        if name.lower() == "mainproc":
            return self.function_linkage(name)
        if self._uses_weak_code_linkage(name):
            return "__attribute__((weak)) "
        if public is not None:
            return "" if public else "static "
        return self.function_linkage(name)

    def _is_listing_source(self) -> bool:
        return self._context.is_listing_source()

    def convert_label_(self, original_name: Token) -> str:
        """Converts a label to its corresponding value.

        :param original_name: The original label name.
        :type original_name: Token
        :return: The corresponding value of the label.
        :rtype: str
        """
        name = str(original_name)
        if self._is_old_struct_member_offset_context(name):
            self._remember_old_struct_member_size(name)
            return self._old_struct_member_offset_constant_name(name)
        if name in self._assignments:
            if (
                isinstance(symbol := self._context.symbols.get_global(name), (op._equ, op._assignment))
                and self._contains_location_counter(getattr(symbol, "value", None))
                and (folded := self._fold_location_counter_expression(symbol)) is not None
            ):
                return folded
            return self.render_instruction_argument(self._assignments[name])
        if (g := self._context.symbols.get_and_mark_global(name)) is None:
            if str(name).lower() in getattr(self._context, "old_struct_member_offsets", {}):
                return self._old_struct_member_offset_constant_name(name)
            if str(name).lower() in getattr(self._context, "externals_abs", ()):
                return str(name)
            if self._is_cross_module_code_export(name) and not self.itisjump:
                return f"m2c::k{self.sanitize_label_name(name)}"
            if self._is_continuation_module() and len(name) > 1 and not self.itisjump:
                if self._is_mangled_internal_code_label(name):
                    return f"m2c::k{self.sanitize_label_name(name)}"
                if self._expr_state.indirection in {IndirectionType.POINTER, IndirectionType.OFFSET}:
                    return f"m2c::near_offset_external({self.sanitize_label_name(name)})"
                return f"m2c::k{self.sanitize_label_name(name)}"
            return name

        state = self._expr_state
        state.is_label = True

        if isinstance(g, op.var):
            return self.convert_label_var(g, name, original_name)
        elif isinstance(g, Proc):
            if self._is_external_proc_data_reference(g):
                return self._convert_external_proc_data_reference(g, name)
            return f"m2c::k{name}" if self._expr_state.data_label_size or not self.itisjump else name
        elif isinstance(g, op.label):
            return f"m2c::k{name}" if self._expr_state.data_label_size or not self.itisjump else name
        elif isinstance(g, op._assignment):
            if self._context.test_mode:
                self._apply_assignment_symbol_state(g)
                return name
            if (symbolic_offset := self._render_single_base_offset_expression(g.value)) is not None:
                return symbolic_offset
            if (folded := self._fold_location_counter_expression(g)) is not None:
                return folded
            return self._parenthesize_compound(self.render_instruction_argument(g.value))
        elif isinstance(g, op._equ):
            if self.itiscall or self.itisjump:
                if (target := self._code_equate_target(g)) is not None:
                    return target
            if self._context.test_mode:
                return g.name
            if (symbolic_offset := self._render_single_base_offset_expression(g.value)) is not None:
                return symbolic_offset
            if (folded := self._fold_location_counter_expression(g)) is not None:
                return folded
            return self._parenthesize_compound(self.render_equate_value(g))
        elif isinstance(g, op.Struct):
            return str(g.size)
        return name

    def _code_equate_target(self, symbol: op._equ) -> str | None:
        """Resolve an EQU alias to a code symbol when rendering control flow."""
        target = self._single_label_expression(symbol.value)
        if target is None:
            return None
        seen = {symbol.name}
        while isinstance(next_symbol := self._context.symbols.get_global(target), op._equ):
            if next_symbol.name in seen:
                return None
            seen.add(next_symbol.name)
            next_target = self._single_label_expression(next_symbol.value)
            if next_target is None:
                return None
            target = next_target
        resolved = self._context.symbols.get_global(target)
        if isinstance(resolved, (Proc, op.label)):
            return target
        return None

    @staticmethod
    def _single_label_expression(value: Any) -> str | None:
        """Return the sole label represented by an expression, if there is one."""
        if isinstance(value, Expression):
            if len(value.children) != 1:
                return None
            return Cpp._single_label_expression(value.children[0])
        if isinstance(value, Tree):
            if len(value.children) != 1:
                return None
            return Cpp._single_label_expression(value.children[0])
        if isinstance(value, list):
            if len(value) != 1:
                return None
            return Cpp._single_label_expression(value[0])
        if isinstance(value, Token) and value.type in {"LABEL", "COMMON"}:
            return str(value)
        return None

    def _is_external_proc_data_reference(self, symbol: Proc) -> bool:
        """Return true when an external NEAR/FAR name is used as storage."""
        return (
            symbol.extern
            and not self.itiscall
            and not self.itisjump
            and not self._expr_state.data_label_size
            and self._expr_state.indirection != IndirectionType.OFFSET
            and self._expr_state.is_just_label
            and str(self._expr_state.work_segment).lower() != "cs"
        )

    def _convert_external_proc_data_reference(self, symbol: Proc, name: str) -> str:
        """Render an ambiguous external procedure symbol as a data reference."""
        size = self._expr_state.element_size or self._middle_size or 2
        original_type = self._external_data_type_for_size(size)
        refs = getattr(self._context, "external_proc_data_refs", None)
        if refs is None:
            refs = {}
            self._context.external_proc_data_refs = refs
        refs[self.sanitize_label_name(name)] = original_type

        data_symbol = op.var(size, 0, name=name, external=True, original_type=original_type)
        data_symbol.used = getattr(symbol, "used", False)
        return self.convert_label_var(data_symbol, name, Token("LABEL", name))

    @staticmethod
    def _external_data_type_for_size(size: int) -> str:
        """Return a MASM scalar data type name for an explicit memory width."""
        return {
            1: "byte",
            2: "word",
            4: "dword",
            8: "qword",
        }.get(size, "word")

    def _apply_assignment_symbol_state(self, symbol: op._assignment) -> None:
        expr = symbol.value
        state = self._expr_state
        size = expr.size() or expr.ptr_size or expr.element_size
        if size:
            state.variable_size = size
        if expr.original_type:
            state.struct_type = expr.original_type

    def convert_label_var(self, g, name, original_name) -> str:
        logging.debug("Variable detected. Size: %s", g.size)
        self._expr_state.variable_size = source_var_size = g.size

        if g.issegment:
            self._expr_state.indirection = IndirectionType.VALUE
            return f"seg_offset({original_name.lower()})"

        if source_var_size == 0:
            # EQU-like aliases can be represented as zero-sized vars in symbol tables.
            # Keep them as scalar symbols instead of treating them as addressable objects.
            self._expr_state.indirection = IndirectionType.VALUE
            self._expr_state.is_variable = False
            return name

        self._expr_state.is_variable = True
        if self._middle_size == 0:  # TODO check
            self._middle_size = source_var_size

        return self._convert_label_var_non_segment(g, name)

    def _convert_label_var_non_segment(self, g, name):
        state = self._expr_state
        state.needs_dereference = False
        state.is_pointer = False
        if g.elements != 1:  # array
            state.needs_dereference = True
            state.is_pointer = True

            if not self.lea and self._expr_state.indirection != IndirectionType.OFFSET:
                self._expr_state.indirection = IndirectionType.POINTER

        #print("\ng.elements == 1 %s, self._expr_state.is_just_label=%s, not self.lea=%s, g.size == self.element_size %s" %(
        #      g.elements == 1, self._expr_state.is_just_label, not self.lea, g.size == self.element_size))
        simple_argument = (
            g.elements == 1
            and state.is_just_label
            and not self.lea
            and g.size == state.element_size
            and self._expr_state.indirection != IndirectionType.OFFSET
        )
        if simple_argument:
            self._expr_state.indirection = IndirectionType.VALUE
            result = g.name
        else:
            result = self._convert_label_var_non_segment_complex(g, name)
        return result

    def _convert_label_var_non_segment_complex(self, g, name):
        state = self._expr_state
        if self._expr_state.work_segment == "cs":
            self.body += "\tcs=seg_offset(" + g.segment + ");\n"

        #print("\nnot self._expr_state.is_just_label=%s ?not self.lea=%s? self._expr_state.indirection == IndirectionType.VALUE %s" %(
        #      not self._expr_state.is_just_label, not self.lea, self._expr_state.indirection == IndirectionType.VALUE))
        if not state.is_just_label and not self.lea and self._expr_state.indirection == IndirectionType.VALUE:
            self._expr_state.indirection = IndirectionType.POINTER

        if self._expr_state.indirection == IndirectionType.POINTER:
            result = g.name
            if not state.is_just_label:  # if not just single label: [a+3] address arithmetics
                state.needs_dereference = True
                state.is_pointer = True
                if g.elements == 1:  # array generates pointer himself
                    result = f"&{result}"

                if g.getsize() == 1:  # it is already a byte
                    result = f"({result})"
                else:
                    result = f"((db*){result})"
                    state.size_changed = True
                    self._middle_size = 1
        elif self._expr_state.indirection == IndirectionType.OFFSET:
            result = self._near_data_offset_expr(g, g.name)
            state.needs_dereference = False
            state.is_pointer = False
        else:
            result = name

        return result

    def render_data_c(self, segments):
        """It takes a list of DOS segments, and for each segment, it takes a list of data items, and for each data item, it
        produces a C++ assignment statement, a C++ extern statement, and a C++ reference statement.

        :param segments: a dictionary of segments, where the key is the segment name and the value is the segment object
        :return: cpp_file, data_hpp_file, data_cpp_file, hpp_file
        """
        prev_data_label_size = self._expr_state.data_label_size
        self._expr_state.data_label_size = 2
        try:
            cpp_file = ""
            data_hpp_file = ""
            data_cpp_file = ""
            hpp_file = ""
            for segment_name, segment in segments.items():
                segment_data_cpp, segment_hpp = self._emit_segment_binding_declarations(segment, segment_name)
                data_cpp_file += segment_data_cpp
                hpp_file += segment_hpp

                for data in segment.getdata():
                    rendered = self._render_data_declaration(data, segment)
                    cpp_file += rendered["cpp_init"]
                    data_hpp_file += rendered["data_hpp_decl"]
                    data_cpp_file += rendered["data_cpp_ref"]
                    hpp_file += rendered["extern_hpp_decl"]
                for alias in self._iter_data_aliases_for_segment(segment, segment_name):
                    # An alias whose name resolves to a merged field is the same
                    # EXTRN->definition binding a linker would make; emitting a
                    # second declaration (often with a different width) is a
                    # conflicting redeclaration.
                    if alias.name.lower() in getattr(self, "_merged_field_label_names", ()):
                        continue
                    data_cpp_file += self._render_data_alias_reference(alias)
                    hpp_file += self._render_data_alias_extern(alias)
            return cpp_file, data_hpp_file, data_cpp_file, hpp_file
        finally:
            self._expr_state.data_label_size = prev_data_label_size

    def _iter_data_aliases_for_segment(self, segment: Any, segment_name: str | None = None):
        segment_names = set(getattr(segment, "segment_aliases", {segment.name: 0}))
        segment_names.add(segment.name)
        if segment_name:
            segment_names.add(segment_name)
        for alias in getattr(self._context, "data_aliases", []):
            if alias.segment in segment_names:
                yield alias

    def _render_data_alias_reference(self, alias: op.var) -> str:
        c_type = self._data_alias_c_type(alias)
        return f"{c_type}& {alias.name}=*(({c_type}*)(&{alias.segment}+0x{alias.offset:x}));\n"

    def _render_data_alias_extern(self, alias: op.var) -> str:
        return f"extern {self._data_alias_c_type(alias)}& {alias.name};\n"

    @staticmethod
    def _data_alias_c_type(alias: op.var) -> str:
        type_map = {
            "db": "db",
            "byte": "byte",
            "sbyte": "byte",
            "dw": "dw",
            "word": "word",
            "sword": "word",
            "near": "word",
            "near16": "word",
            "dd": "dd",
            "dword": "dword",
            "sdword": "dword",
            "far": "dword",
            "far16": "dword",
            "far32": "dword",
            "df": "df",
            "fword": "fword",
            "dq": "dq",
            "qword": "qword",
            "dt": "dt",
            "tbyte": "tbyte",
            "real4": "real4",
            "real8": "real8",
            "real10": "real10",
        }
        return type_map.get(alias.original_type, alias.original_type)

    def _emit_segment_binding_declarations(self, segment: Any, segment_name: str | None = None) -> tuple[str, str]:
        data_cpp = ""
        hpp = ""
        aliases = getattr(segment, "segment_aliases", {segment.name: 0})
        aliases = {segment.name: 0, **aliases}
        if segment_name:
            aliases = {segment_name: 0, **aliases}
        for name, relative_offset in aliases.items():
            linear = self._segment_binding_linear(segment, relative_offset, segment_name)
            data_cpp += f"db& {name}=*((db*)&m2c::m+0x{linear:x});\n"
            hpp += f"extern db& {name};\n"
        return data_cpp, hpp

    def _segment_binding_linear(
        self,
        segment: Any,
        relative_offset: int = 0,
        segment_name: str | None = None,
    ) -> int:
        """Return the linear memory address used for a segment binding."""
        linear = int(segment.offset) + int(relative_offset)
        if self._linked_data_offsets_enabled() and self._is_code_storage_segment(segment):
            return self._load_segment_linear_base() + linear
        if self._linked_data_offsets_enabled() and self._uses_authoritative_linked_storage(segment):
            return self._load_segment_linear_base() + linear
        linked_base = self._linked_data_segment_base(segment, segment_name)
        if linked_base is not None:
            return linked_base + int(relative_offset)
        return linear

    @staticmethod
    def _uses_authoritative_linked_storage(segment: Any) -> bool:
        """Return true when merge layout must override inferred linked bases."""
        return bool(getattr(segment, "linked_storage_offset_authoritative", False))

    def _linked_data_segment_base(self, segment: Any, segment_name: str | None = None) -> int | None:
        """Infer a linked data segment's runtime base from exported offset aliases."""
        if not self._linked_data_offsets_enabled() or self._is_code_storage_segment(segment):
            return None

        exports = getattr(self._context, "exported_code_symbol_offsets", {})
        if not exports:
            return None

        segment_names = self._segment_names(segment, segment_name)
        candidates: set[int] = set()
        for alias in getattr(self._context, "data_aliases", []):
            if str(getattr(alias, "segment", "")).lower() not in segment_names:
                continue
            name = str(getattr(alias, "name", "")).lower()
            if name not in exports:
                continue
            export_offset = int(exports[name])
            alias_offset = int(getattr(alias, "offset", 0))
            candidates.add((export_offset - alias_offset) & ~0xF)

        if len(candidates) == 1:
            return self._load_segment_linear_base() + candidates.pop()
        return None

    @staticmethod
    def _segment_names(segment: Any, segment_name: str | None = None) -> set[str]:
        """Return all known names that can identify a segment."""
        names = {str(getattr(segment, "name", "")).lower()}
        names.update(str(name).lower() for name in getattr(segment, "segment_aliases", {segment.name: 0}))
        if segment_name:
            names.add(str(segment_name).lower())
        names.discard("")
        return names

    def _load_segment_linear_base(self) -> int:
        """Return the configured DOS load segment as a linear address."""
        args = self._context.args if isinstance(self._context.args, dict) else {}
        loadsegment = args.get("loadsegment", "0x1a2")
        if isinstance(loadsegment, int):
            segment = loadsegment
        elif loadsegment is None:
            segment = 0x1A2
        else:
            segment = int(str(loadsegment), 0)
        return segment << 4

    def _render_data_declaration(self, data: Data, segment: Any | None = None) -> dict[str, str]:
        value, type_and_name, _ = self.produce_c_data_single_(data)
        type_and_name += ";\n"
        cpp_init = ""
        extern_hpp_decl = ""
        data_cpp_ref = ""

        if not data.is_align():
            (
                cpp_init,
                type_and_name,
                extern_hpp_decl,
                data_cpp_ref,
            ) = self._render_data_assignment_and_refs(data, value, type_and_name, segment)

        return {
            "cpp_init": cpp_init,
            "data_hpp_decl": type_and_name,
            "data_cpp_ref": data_cpp_ref,
            "extern_hpp_decl": extern_hpp_decl,
        }

    def _render_data_assignment_and_refs(
            self,
            data: Data,
            value: str,
            type_and_name: str,
            segment: Any | None = None,
    ) -> tuple[str, str, str, str]:
        match = re.match(r"^((?:struct\s+)?\w+)\s+(\w+)(\[\d+\])?;\n", type_and_name)
        if not match:
            logging.error(f"Failed to parse {value} {type_and_name}")
            return "", type_and_name, "", ""

        name = match[2]
        if name.startswith("dummy") and value == "":
            return "", "", "", ""
        type_and_size = re.sub(
            r"^(?P<type>(?:struct\s+)?\w+)\s+\w+(\[\d+\])?;\n",
            r"\g<type> tmp999\g<2>",
            type_and_name,
        )
        cpp_init = self._build_data_assignment(name, value, type_and_size, bool(match[3]))
        data_cpp_ref = self._generate_dataref_from_declaration_c(type_and_name, data, segment)
        extern_hpp_decl = self._generate_extern_from_declaration_c(type_and_name)
        if cpp_init:
            cpp_init, type_and_name = self._append_real_address_comment(data, cpp_init, type_and_name)
            cpp_init += "\n"
        return cpp_init, type_and_name, extern_hpp_decl, data_cpp_ref

    def _build_data_assignment(self, name: str, value: str, type_and_size: str, is_array: bool) -> str:
        if value == "":
            return ""
        if name.startswith("dummy") and value == "0":
            return ""
        if is_array:
            return "" if value == "{}" else f"    {{{type_and_size}={value};MYCOPY({name})}}"
        return f"    {{{type_and_size}={value};MYCOPY({name})}}"

    def _append_real_address_comment(self, data: Data, value: str, type_and_name: str) -> tuple[str, str]:
        real_seg, real_offset = data.getrealaddr()
        if not real_seg:
            return value, type_and_name
        comment = f" // {real_seg:04x}:{real_offset:04x}"
        return value + comment, f"{type_and_name[:-1]}{comment}\n"

    def _generate_extern_from_declaration_c(self, _hpp):
        """It takes a C++ declaration and returns a extern declaration to the same.

        :param _hpp: The C++ header file
        :return: The extern declaration of the function or variable.
        """
        m = re.match(r"^char\s+([A-Za-z0-9_]+)\[1\];(?:\s*//.*)?$", _hpp.strip())
        if m:
            return f"extern char& {m.group(1)};\n"
        _extern = re.sub(
            r"^((?:struct\s+)?\w+)\s+([\w\[\]]+)(\[\d+\]);",
            r"extern \g<1> (& \g<2>)\g<3>;",
            _hpp,
        )
        _extern = re.sub(r"^((?:struct\s+)?\w+)\s+([\w\[\]]+);", r"extern \g<1>& \g<2>;", _extern)
        return _extern

    def _generate_dataref_from_declaration_c(
            self,
            _hpp: str,
            data: Data | None = None,
            segment: Any | None = None,
    ) -> str:
        """It takes a C++ declaration and returns a reference to the same variable.

        :param _hpp: declaration string
        :return: The reference to the same data
        """
        if data is not None and segment is not None:
            return self._generate_linear_dataref_from_declaration_c(_hpp, data, segment)
        m = re.match(r"^char\s+([A-Za-z0-9_]+)\[1\];(?:\s*//.*)?$", _hpp.strip())
        if m:
            name = m.group(1)
            return f"char& {name} = m2c::m.{name}[0];\n"
        _reference = re.sub(r"^((?:struct\s+)?\w+)\s+([\w\[\]]+)(\[\d+\]);",
                            r"\g<1> (& \g<2>)\g<3> = m2c::m.\g<2>;", _hpp)
        _reference = re.sub(
            r"^((?:struct\s+)?\w+)\s+([\w\[\]]+);",
            r"\g<1>& \g<2> = m2c::m.\g<2>;",
            _reference,
        )
        return _reference

    @staticmethod
    def _generate_linear_dataref_from_declaration_c(_hpp: str, data: Data, segment: Any) -> str:
        match = re.match(
            r"^(?P<type>(?:struct\s+)?\w+)\s+(?P<name>\w+)(?P<array>\[\d+\])?;\s*(?://.*)?$",
            _hpp.strip(),
        )
        if not match:
            logging.error("Failed to parse data declaration for reference: %s", _hpp)
            return ""

        c_type = match["type"]
        name = match["name"]
        array_suffix = match["array"] or ""
        address = f"&{segment.name}+0x{data.offset:x}"
        if c_type == "char" and array_suffix == "[1]":
            return f"char& {name} = *((char*)({address}));\n"
        if array_suffix:
            return f"{c_type} (& {name}){array_suffix} = *(({c_type} (*){array_suffix})({address}));\n"
        return f"{c_type}& {name} = *(({c_type}*)({address}));\n"

    @staticmethod
    def _flatten_data_values(values: list[Any]) -> list[Any]:
        result: list[Any] = []
        for value in values:
            if isinstance(value, list):
                if len(value) == 1:
                    result.extend(Cpp._flatten_data_values(value))
                elif all(isinstance(item, str) and len(item) == 1 for item in value):
                    result.extend(value)
                else:
                    result.append(value)
            else:
                result.append(value)
        return result

    def memberdir(self, tree: Tree) -> list[str]:
        assert isinstance(tree.children, list) and all(isinstance(child, str)for child in tree.children)
        return [self.convert_member_(tree.children)]


    def convert_member_(self, label: list[str]) -> str:
        state = self._expr_state
        state.struct_type = None
        value = ".".join(label)

        if label and label[0].startswith("__memptr_"):
            return self._convert_pointer_member(label)

        if self._expr_state.indirection == IndirectionType.OFFSET and (g := self._context.symbols.get_global(label[0])):
            return self.convert_member_offset(g, label)

        if (g := self._context.symbols.get_and_mark_global(label[0])) is None:
            logging.error("global '%s' is missing", label)
            return ".".join(label)

        if isinstance(g, (op._equ, op._assignment)):
            value = self._convert_member_equ(g, label)
        elif isinstance(g, op.var):
            value = self._convert_member_var(g, label)
        elif isinstance(g, op.Struct):
            #if self._expr_state.is_just_member:
            value = self._offsetof_expr(label[0], ".".join(label[1:]))

        if self._expr_state.indirection == IndirectionType.POINTER and state.needs_dereference and state.struct_type:
            state.is_member = True
            state.needs_dereference = False

        return value

    def _offsetof_expr(self, type_name: str, members: str) -> str:
        """Render offsetof with an elaborated struct/union tag so that names
        hidden by C library functions (e.g. clock()) still resolve."""
        tag = "struct"
        structures = getattr(self._context, "structures", None) or {}
        struct = structures.get(type_name) or structures.get(str(type_name).lower())
        if isinstance(struct, op.Struct) and struct.gettype() == op.Struct.UNION:
            tag = "union"
        return f"offsetof({tag} {type_name},{members})"

    def _offsetof_decl(self, type_name: str, members: str) -> str:
        return self._offsetof_expr(type_name, members).replace(",", ", ", 1)

    def _convert_pointer_member(self, label: list[str]) -> str:
        state = self._expr_state
        base = label[0].removeprefix("__memptr_")
        member = label[-1]
        member_size = state.element_size or self._middle_size or self._calculate_known_struct_member_size(member) or 1
        state.variable_size = member_size
        if self._middle_size == 0:
            self._middle_size = member_size
        state.is_variable = False
        state.is_label = False
        state.is_pointer = False
        state.needs_dereference = False
        state.indirection = IndirectionType.VALUE
        c_type = {1: "db", 2: "dw", 4: "dd", 8: "dq"}.get(member_size, "db")
        return f"*(({c_type}*)raddr({state.work_segment},{base}+{self._old_struct_member_offset_constant_name(member)}))"

    def _convert_member_var(self, g, label):
        state = self._expr_state
        self._promote_scalar_external_member_base(g, label)
        if alias_member := self._render_struct_alias_member(g, label):
            return alias_member
        source_var_size = self.calculate_member_size(label)
        if source_var_size == 0:
            raise Exception(f"invalid var {label} size {source_var_size}")

        state.variable_size = source_var_size
        logging.debug("it is var %s", source_var_size)
        if self._middle_size == 0:
            self._middle_size = source_var_size
        state.is_variable = True
        state.is_label = True
        if g.elements == 1 and state.is_just_label and not self.lea and source_var_size == self._middle_size:
            state.needs_dereference = False
            state.is_pointer = False
            value = ".".join(label)
            self._expr_state.indirection = IndirectionType.VALUE
        else:
            state.needs_dereference = True
            state.is_pointer = True
            if not state.is_just_label and not self.lea and self._expr_state.indirection == IndirectionType.VALUE:
                self._expr_state.indirection = IndirectionType.POINTER
            if self._expr_state.indirection == IndirectionType.POINTER:
                value = ".".join(label)
                if not state.is_just_label:  # if not just single label
                    if g.elements == 1:  # array generates pointer himself
                        value = f"&{value}"

                    if source_var_size == 1:  # it is already a byte
                        value = f"({value})"
                    else:
                        value = f"((db*){value})"
                        state.size_changed = True
                        self._middle_size = 1
            elif self._expr_state.indirection == IndirectionType.OFFSET:
                value = self._near_data_offset_expr(g, ".".join(label))
            else:
                value = ".".join(label)

            if self._expr_state.work_segment == "cs":
                self.body += "\tcs=seg_offset(" + g.segment + ");\n"
        return value

    def _render_struct_alias_member(self, g: op.var, label: list[str]) -> str:
        if len(label) < 2 or g.original_type not in self._context.structures:
            return ""
        struct = self._context.structures[g.original_type]
        member = label[1]
        try:
            struct.getitem(member)
            return ""
        except KeyError:
            pass
        member_size = self._calculate_struct_alias_member_size(g.original_type, member)
        if member_size == 0:
            return ""
        if member_size > 2 and member.endswith(("_hi", "_lo")):
            member_size = 2
        c_type = {1: "db", 2: "dw", 4: "dd", 8: "dq"}.get(member_size, "db")
        state = self._expr_state
        state.variable_size = member_size
        state.is_variable = True
        state.is_label = True
        state.is_pointer = False
        state.needs_dereference = False
        state.indirection = IndirectionType.VALUE
        return f"*(({c_type}*)((db*)&{g.name}+{member}))"

    def _promote_scalar_external_member_base(self, g: op.var, label: list[str]) -> None:
        if not g.external or len(label) < 2 or g.original_type in self._context.structures:
            return
        inferred_type = self.infer_struct_type_for_member(label[1])
        if inferred_type:
            g.original_type = inferred_type
            g.size = self._context.typetosize(inferred_type)

    def _convert_member_equ(self, g, label):
        state = self._expr_state
        logging.debug("%s", g)
        if not g.implemented:
            g.accept(self)

        if state.is_just_label:
            value = ".".join(label)
        elif not isinstance(g.value, Expression):
            value = ".".join(label)
        else:
            state.struct_type = g.value.original_type
            state.needs_dereference = True
            state.is_pointer = False
            state.need_pointer_to_member = label
            value = ""
        logging.debug("equ: %s -> %s", label[0], value)
        return value

    def convert_member_offset(self, g, label: list[str]):
        if isinstance(g, op.var):
            joined_label = ".".join(label)
            if g.external and len(label) == 1 and not self._expr_state.data_label_size:
                if self._is_cross_module_code_export(joined_label):
                    value = f"m2c::k{self.sanitize_label_name(joined_label)}"
                else:
                    value = f"m2c::near_offset_external({joined_label})"
            else:
                value = self._near_data_offset_expr(g, joined_label)
        elif isinstance(g, op.Struct):
            value = self._offsetof_expr(label[0], ".".join(label[1:]))
        elif isinstance(g, (op._equ, op._assignment)):
            value = f'({label[0]})+{self._offsetof_expr(g.original_type, ".".join(label[1:]))}'
        else:
            raise Exception(f"Not handled type {type(g)!s}")

        self._expr_state.indirection = IndirectionType.VALUE
        return value

    def convert_sqbr_reference(self, segment: str, expr: str, size: int) -> str:
        state = self._expr_state
        if not state.is_label or not state.is_variable:
            state.needs_dereference = True
            state.is_pointer = True
            expr = self._continuation_external_label_offset(expr)
            if size == 1:
                expr = f"raddr({segment},{expr})"
            elif size == 2:
                expr = f"(dw*)(raddr({segment},{expr}))"
            elif size == 4:
                expr = f"(dd*)(raddr({segment},{expr}))"
            elif size == 8:
                expr = f"(dq*)(raddr({segment},{expr}))"
            else:
                logging.error(f"~{expr}~ invalid size {size}")
                expr = f"raddr({segment},{expr})"
        elif state.size_changed:  # or not state.is_just_label:
                expr = Cpp.render_new_pointer_size(state.is_pointer, expr, size)
                state.size_changed = False

        logging.debug("expr: %s", expr)
        return expr

    def _continuation_external_label_offset(self, expr: str) -> str:
        if not self._is_continuation_module():
            return expr
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", expr):
            return expr
        if self._context.symbols.get_global(expr) is not None:
            return expr
        if self._is_mangled_internal_code_label(expr):
            return f"m2c::k{self.sanitize_label_name(expr)}"
        if expr.startswith(("dummy", "edummy")):
            return f"m2c::near_offset_external({self.sanitize_label_name(expr)})"
        return f"m2c::k{self.sanitize_label_name(expr)}"

    @staticmethod
    def render_new_pointer_size(itispointer: bool, expr: str, target_size: int) -> str:
        """:param expr: the expression to be rendered
        :param target_size: the new size of the pointer
        :return: The expression with the new size.
        """
        if not itispointer:
            expr = f"&{expr}"

        if target_size == 1:
            expr = f"(db*)({expr})"
        elif target_size == 2:
            expr = f"(dw*)({expr})"
        elif target_size == 4:
            expr = f"(dd*)({expr})"
        elif target_size == 8:
            expr = f"(dq*)({expr})"
        else:
            logging.error(f"~{expr}~ unknown size {target_size}")

        if not itispointer:
            expr = f"*{expr}"
        return expr



    def jump_post(self, expr: Expression) -> tuple[str, bool]:
        result = self._render_with_flags(expr, is_jump=True)  # TODO why need something else?
        name = result
        far = self.get_global_far(name)
        if "far" in expr.mods:
            far = True
        elif "near" in expr.mods:
            far = False

        if isinstance(name, str) and ((g := self._context.symbols.get_and_mark_global(name)) is None or isinstance(g, op.var)):
            # jumps feat purpose:
            # * in sub __dispatch_call - for address based jumps or grouped subs
            # * direct jumps

            # how to handle jumps:
            # subs - direct jump to internal sub (maybe merged) - directly
            # labels - directly
            # offset - internal sub __dispatch_call disp=cs + offset
            #   register
            #   exact value
            # seg:offset - in sub __dispatch_call disp= seg:offset ?
            # if self._context.has_global(name):
            if self._is_indirect_dispatch_expr(name):
                # Near indirect targets (jmp word ptr [x], jmp ax) hold the
                # bare aggregate/local code offset that OFFSET and code-pointer
                # tables store; far targets already carry seg:off in a dd read.
                self.dispatch += f"__disp={name};\n"
                name = "__dispatch_call_ext"
            else:
                self.dispatch += f"__disp={name};\n"
                name = "__dispatch_call"

        return name, far

    _DISPATCH_INDIRECT_REGS = {
        "ax", "bx", "cx", "dx", "si", "di", "bp", "sp",
        "ah", "al", "bh", "bl", "ch", "cl", "dh", "dl",
        "eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp",
    }

    def _is_indirect_dispatch_expr(self, rendered: str) -> bool:
        """Return true when a call/jump target is a register or memory expression.

        Indirect targets carry aggregate (linked) code offsets: OFFSET emits
        ``m2c::kglobal_*`` constants and code-pointer tables store them too.
        Bare identifiers and ``label+const`` expressions instead produce
        module-local ``m2c::k*`` offsets handled by the local dispatch switch.
        """
        text = rendered.strip()
        if text.lower() in self._DISPATCH_INDIRECT_REGS:
            return True
        return "raddr" in text or "*" in text or "[" in text

    def get_global_far(self, name: str) -> bool:  # TODO Remove this!!!
        """Convert argument tokens which for jump operations into C string
        :param name: Tokens
        :return: C string.
        """
        logging.debug("jump_to_label(%s)", name)
        far = False
        if isinstance(name, str) and (g := self._context.symbols.get_global(name)) and isinstance(g, Proc | op.label):
            far = g.far  # make far calls to far procs
        return far

    def _label(self, name, isproc):
        if isproc:
            raise RuntimeError("Dead code?")
        self._cmdlabel = "%s:\n" % self.mangle_label(name)
        return ""

    def _call(self, expr: Expression) -> str:
        logging.debug("cpp._call(%s)", expr)
        ret = ""
        expr_render = self._clone_expression_for_render(expr)
        if expr_render.ptr_size == 0:
            expr_render.ptr_size = 2
        size = self.calculate_size(expr_render)
        proc_name = self._render_with_flags(expr_render, is_jump=True, is_call=True)  # TODO why need something else?
        far = self.get_global_far(proc_name)
        if size == 4 or "far" in expr.mods:
            far = True
        elif "near" in expr.mods:
            far = False

        label_ip = "0"
        if isinstance(proc_name, str) and (g := self._context.symbols.get_global(proc_name)):
            if isinstance(g, op.label) and not g.isproc and proc_name not in self._procs and proc_name not in self.grouped:
                label_ip = f"m2c::k{proc_name}"
                proc_name = self.label_to_proc[g.name]
            elif isinstance(g, op.var):
                label_ip = proc_name
                proc_name = "__dispatch_call_ext"

            # calls feat purpose:
        # * grouped sub wrapper, exact subs  - direct name for external references
        #   intern sub jump dispatcher - for grouped subs
        # * global __dispatch_call - for address based calls CALL[es:bx]

        # how to handle call instr:
        # subs - (disp = 0) direct calls CALL(sub_0123)
        # labels
        #    in sub - self call the sub( with disp= klabel) ? or global dispatcher?
        #    other sub - __dispatch_call the sub( with disp= klabel)
        # offset - __dispatch_call disp=cs + offset
        #   register
        #   memory reference
        # seg:offset  - __dispatch_call disp= seg:offset
        else:
            if self._is_indirect_dispatch_expr(proc_name):
                label_ip = proc_name
                proc_name = "__dispatch_call_ext"
            else:
                proc_name, label_ip = "__dispatch_call", proc_name

        proc_name = self.mangle_label(proc_name)
        inline_return_ip = self._inline_data_return_ip_after_current_call()

        if far and inline_return_ip is not None:
            ret += f"CALLFI({proc_name},{label_ip},{inline_return_ip})"
        elif far:
            ret += f"CALLF({proc_name},{label_ip})"
        elif inline_return_ip is not None:
            ret += f"CALLI({proc_name},{label_ip},{inline_return_ip})"
        else:
            ret += f"CALL({proc_name},{label_ip})"
        return ret

    def _inline_data_return_ip_after_current_call(self) -> str | None:
        """Return the code-data offset used as a call return IP, if present."""
        stmt = self._current_stmt
        if not isinstance(stmt, op._call):
            return None
        data = self._inline_code_data_after_stmt(stmt)
        if data is None:
            return None
        label = str(getattr(data, "label", "") or "")
        if label:
            return f"m2c::near_offset_external({self.mangle_label(label)})"
        return f"0x{int(getattr(data, 'offset', 0)):x}"

    def _inline_code_data_after_stmt(self, stmt: op.baseop) -> op.Data | None:
        """Find code-segment data located between a statement and its successor."""
        line_number = int(getattr(stmt, "line_number", 0) or 0)
        if line_number <= 0:
            return None
        next_line = int(getattr(self._next_stmt, "line_number", 0) or 0)
        filename = self._normalized_source_name(getattr(stmt, "filename", ""))
        candidates: list[tuple[int, int, op.Data]] = []
        for segment in self._context.segments.values():
            if not self._looks_like_code_segment(segment):
                continue
            for data in segment.getdata():
                data_line = int(getattr(data, "line_number", 0) or 0)
                if data_line <= line_number:
                    continue
                if next_line > 0 and data_line >= next_line:
                    continue
                data_filename = self._normalized_source_name(getattr(data, "filename", ""))
                if filename and data_filename and filename != data_filename:
                    continue
                candidates.append((data_line, int(getattr(data, "offset", 0)), data))
        if not candidates:
            return None
        return min(candidates, key=lambda item: (item[0], item[1]))[2]

    @staticmethod
    def _normalized_source_name(filename: str) -> str:
        """Normalize source names enough to compare parser metadata."""
        return os.path.normcase(os.path.abspath(filename)) if filename else ""

    @staticmethod
    def _looks_like_code_segment(segment: Any) -> bool:
        """Return true for segments that can hold executable bytes."""
        name = str(getattr(segment, "name", "") or "").strip("'\"").lower()
        segclass = str(getattr(segment, "segclass", "") or "").strip("'\"").lower()
        return (
            name in {"code", "cseg", "codesg", "_text"}
            or name.endswith("code")
            or "code" in name
            or "code" in segclass
        )

    def _skipbytes(self, opcode: int, byte_count: int) -> str:
        """Render a code-segment data opcode that swallows following bytes."""
        self._code_skip_label_counter += 1
        label = f"__m2c_skip_{self._code_skip_label_counter}"
        self._pending_code_skip = {
            "label": label,
            "remaining": byte_count,
            "just_created": True,
        }
        effect = self._render_skip_opcode_effect(opcode, byte_count, self._next_stmt)
        return f"{{{effect}goto {label};}}"

    def consume_code_skip_after_stmt(self, stmt: op.baseop, command: str) -> str:
        """Place a pending skip target after the swallowed source bytes."""
        pending = self._pending_code_skip
        if pending is None:
            return ""
        if pending.pop("just_created", False):
            return ""
        if isinstance(stmt, op.label) or not command:
            return ""
        remaining = int(pending["remaining"])
        remaining -= max(1, len(self._estimate_instruction_bytes(stmt)))
        if remaining > 0:
            pending["remaining"] = remaining
            return ""
        label = str(pending["label"])
        self._pending_code_skip = None
        return f"\n{label}:\n"

    def _render_skip_opcode_effect(self, opcode: int, byte_count: int, stmt: op.baseop | None) -> str:
        """Render the visible effect of an immediate opcode used as a skip."""
        skipped = self._estimate_instruction_bytes(stmt)[:byte_count]
        if len(skipped) < byte_count:
            return ""
        if 0xB0 <= opcode <= 0xB7:
            reg = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"][opcode - 0xB0]
            return f"{reg} = {skipped[0]:#04x};"
        if 0xB8 <= opcode <= 0xBF:
            reg = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"][opcode - 0xB8]
            value = skipped[0] | (skipped[1] << 8)
            return f"{reg} = {value:#06x};"
        if opcode == 0x0D:
            value = skipped[0] | (skipped[1] << 8)
            return f"OR(ax, {value:#06x});"
        if opcode == 0x3C:
            return f"CMP(al, {skipped[0]:#04x});"
        return ""

    @classmethod
    def _estimate_instruction_bytes(cls, stmt: op.baseop | None) -> list[int]:
        """Return known leading bytes for simple instructions used by skip idioms."""
        if stmt is None:
            return []
        raw = cls._normalized_raw_instruction(getattr(stmt, "raw_line", ""))
        if not raw:
            return []
        reg16 = {"ax": 0, "cx": 1, "dx": 2, "bx": 3, "sp": 4, "bp": 5, "si": 6, "di": 7}
        reg8 = {"al": 0, "cl": 1, "dl": 2, "bl": 3, "ah": 4, "ch": 5, "dh": 6, "bh": 7}
        if match := re.match(r"push\s+([a-d]x|[sb]p|[sd]i)\b", raw, re.IGNORECASE):
            return [0x50 + reg16[match.group(1).lower()]]
        if match := re.match(r"pop\s+([a-d]x|[sb]p|[sd]i)\b", raw, re.IGNORECASE):
            return [0x58 + reg16[match.group(1).lower()]]
        if match := re.match(r"mov\s+([a-d][lh])\s*,\s*(?:low\s+)?(.+)$", raw, re.IGNORECASE):
            value = cls._estimate_immediate_byte(match.group(2))
            return [0xB0 + reg8[match.group(1).lower()], value or 0]
        if match := re.match(r"mov\s+([a-d]x|[sb]p|[sd]i)\s*,\s*(?:offset\s+)?(.+)$", raw, re.IGNORECASE):
            value = cls._estimate_immediate_word(match.group(2))
            value = value or 0
            return [0xB8 + reg16[match.group(1).lower()], value & 0xff, (value >> 8) & 0xff]
        if re.match(r"xor\s+al\s*,\s*al\b", raw, re.IGNORECASE):
            return [0x30, 0xC0]
        return []

    @staticmethod
    def _normalized_raw_instruction(raw: str) -> str:
        """Strip labels and comments from a source instruction line."""
        code = raw.split(";", 1)[0].strip()
        if ":" in code:
            code = code.split(":", 1)[1].strip()
        return re.sub(r"\s+", " ", code)

    @staticmethod
    def _estimate_immediate_byte(expr: str) -> int | None:
        """Best-effort parse of a byte immediate used in skip tests."""
        value = Cpp._estimate_immediate_word(expr)
        return None if value is None else value & 0xff

    @staticmethod
    def _estimate_immediate_word(expr: str) -> int | None:
        """Best-effort parse of a simple immediate used by skip opcode lookahead."""
        cleaned = expr.strip().strip("()")
        cleaned = re.sub(r"(?i)\blow\s+", "", cleaned)
        cleaned = re.sub(r"(?i)\boffset\s+", "", cleaned)
        if match := re.fullmatch(r"'(.)'|\"(.)\"", cleaned):
            return ord(match.group(1) or match.group(2))
        if match := re.fullmatch(r"([0-9a-f]+)h", cleaned, re.IGNORECASE):
            return int(match.group(1), 16)
        if match := re.fullmatch(r"([0-7]+)o", cleaned, re.IGNORECASE):
            return int(match.group(1), 8)
        if match := re.fullmatch(r"[0-9]+", cleaned):
            return int(match.group(0), 10)
        return None

    def consume_external_offset_ds_restore(self, stmt: op.baseop) -> str:
        if not stmt.cmd.startswith("call"):
            return ""
        restore = ""
        if self._pending_external_offset_ds_restore:
            self._pending_external_offset_ds_restore = False
            restore += "\tR(m2c::restore_external_offset_ds(ds));"
        if self._pending_data_offset_ds_restore:
            self._pending_data_offset_ds_restore = False
            restore += "\tR(m2c::restore_data_offset_ds(ds));"
        return restore

    def _render_with_flags(self, expr: Expression, *, is_jump: bool = False, is_call: bool = False) -> str:
        prev_jump, prev_call = self.itisjump, self.itiscall
        self.itisjump, self.itiscall = is_jump, is_call
        try:
            return self.render_instruction_argument(expr, 0)
        finally:
            self.itisjump, self.itiscall = prev_jump, prev_call

    def _ret(self, src: list[Union[Expression, Any]]) -> str:
        arg = self.render_instruction_argument(src[0]) if src else "0"
        proc = getattr(self, "proc", None)
        if getattr(proc, "far", False) or getattr(self, "_active_proc_far", False):
            return f"RETF({arg})"
        return f"RETN({arg})"

    def _retf(self, src: list[Union[Expression, Any]]) -> str:
        arg = self.render_instruction_argument(src[0]) if src else "0"
        return f"RETF({arg})"

    def _xlat(self, src: list[Union[Expression, Any]]) -> str:
        if not src:
            return "XLAT"
        arg = self.render_instruction_argument(src[0])[2:-1]
        arg = self._rewrite_continuation_raddr_label(arg)
        return f"XLATP({arg})"

    def _rewrite_continuation_raddr_label(self, arg: str) -> str:
        if not self._is_continuation_module():
            return arg

        def replace(match: re.Match[str]) -> str:
            segment, label = match.groups()
            if self._context.symbols.get_global(label) is not None:
                return match.group(0)
            return f"raddr({segment},m2c::k{self.sanitize_label_name(label)})"

        return re.sub(r"\braddr\(([^,]+),([A-Za-z_][A-Za-z0-9_]*)\)", replace, arg)

    def parse2(self, dst: Expression, src: Expression, *, lea: bool = False) -> tuple[str, str]:
        dst_size, src_size = self.calculate_size(dst), self.calculate_size(src)
        if dst_size == 0:
            if src_size == 0:
                logging.debug("parse2: %s %s both sizes are 0", dst, src)
            dst_size = src_size
        if src_size == 0:
            src_size = dst_size

        dst_str = self.render_instruction_argument(dst, dst_size, destination=True, lea=lea)
        src_str = self.render_instruction_argument(src, src_size, lea=lea)
        return dst_str, src_str

    def _add(self, dst: Expression, src: Expression) -> str:
        a, b = self.parse2(dst, src)
        # if self.d in ['sp', 'esp'] and check_int(self.s):
        return f"ADD({a}, {b})"

    def _mul(self, src: list[Expression]) -> str:
        size = 0
        res: list[str] = []
        for arg in src:
            rendered, state = self.render_instruction_argument_with_state(arg, size)
            res.append(rendered)
            if size:
                continue
            size = self.calculate_size(arg) or state.variable_size or arg.ptr_size or arg.element_size
        if size == 0:
            size = self._middle_size
        return "MUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _imul(self, src: list[Expression]) -> str:
        size = 0
        res: list[str] = []
        for arg in src:
            rendered, state = self.render_instruction_argument_with_state(arg, size)
            res.append(rendered)
            if size:
                continue
            size = self.calculate_size(arg) or state.variable_size or arg.ptr_size or arg.element_size
        if size == 0:
            size = self._middle_size
        return "IMUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _div(self, src: Expression) -> str:
        a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        return "DIV%d(%s)" % (size, a)

    def _idiv(self, src: Expression) -> str:
        a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        return "IDIV%d(%s)" % (size, a)

    def _jz(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label_str, _ = self.jump_post(label)  # TODO
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "GET_ZF()"):
            return dispatch
        return f"JZ({label_str})"

    def _jnz(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label_str, _ = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "!GET_ZF()"):
            return dispatch
        return f"JNZ({label_str})"

    def _jbe(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label_str, _ = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "GET_CF() || GET_ZF()"):
            return dispatch
        return f"JBE({label_str})"

    def _ja(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label_str, far = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "!GET_CF() && !GET_ZF()"):
            return dispatch
        return f"JA({label_str})"

    def _jc(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label_str, far = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "GET_CF()"):
            return dispatch
        return f"JC({label_str})"

    def _jnc(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label_str, far = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "!GET_CF()"):
            return dispatch
        return f"JNC({label_str})"

    def _conditional_cross_proc_dispatch(self, label: str, condition: str) -> str:
        if not self._context.args:
            return ""
        mergeprocs = self._context.args.get("mergeprocs")
        if mergeprocs not in {"separate", "single"}:
            return ""
        label = str(label)
        target_proc = self.label_to_proc.get(label)
        proc = getattr(self, "proc", None)
        current_proc = proc if isinstance(proc, str) else getattr(proc, "name", "")
        if not target_proc or not current_proc or target_proc == current_proc:
            return ""
        return f"if ({condition}) return __dispatch_call(m2c::k{label}, _state);"

    """
    def _push(self, regs):
        p = ""
        for r in regs:
            if self.get_size(r):
                self.__pushpop_count += 2
                r = self.expand(r)
                p += "PUSH(%s)" % (r)
        return p

    def _pop(self, regs):
        p = ""
        for r in regs:
            self.__pushpop_count -= 2
            r = self.expand(r)
            p += "POP(%s)" % r
        return p
    """

    def _rep(self):
        self.prefix = "\tREP "
        return ""

    def _cmpsb(self) -> str:
        return self._cmps_with_source_segment("CMPSB")

    def _cmps_with_source_segment(self, macro: str) -> str:
        """Render CMPS with a source segment override when the source uses one."""
        segment = self._cmps_source_segment_override()
        if segment and segment != "ds":
            return f"{macro}_SEG({segment})"
        return macro

    def _cmps_source_segment_override(self) -> str | None:
        """Return the explicit source segment from a CMPS source operand."""
        raw_line = str(getattr(self._current_stmt, "raw_line", "") or "")
        match = re.search(r"\bcmps[bdw]?\s+(?P<segment>cs|ds|es|fs|gs|ss)\s*:", raw_line, re.IGNORECASE)
        return match.group("segment").lower() if match else None

    def _lodsb(self) -> str:
        return "LODSB"

    def _cmpsw(self) -> str:
        return self._cmps_with_source_segment("CMPSW")

    def _cmpsd(self) -> str:
        return self._cmps_with_source_segment("CMPSD")

    def _lodsw(self) -> str:
        return "LODSW"

    def _lodsd(self) -> str:
        return "LODSD"

    def _stosb(self) -> str:
        return "STOSB"

    def _stosw(self) -> str:
        return "STOSW"

    def _stosd(self) -> str:
        return "STOSD"

    def _movsb(self) -> str:
        return "MOVSB"

    def _movsw(self) -> str:
        return "MOVSW"

    def _movsd(self) -> str:
        return "MOVSD"

    def _scasb(self) -> str:
        return "SCASB"

    def _scasw(self) -> str:
        return "SCASW"

    def _scasd(self) -> str:
        return "SCASD"

    def _scas(self, src: Expression) -> str:
        a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        srcr = Token_.find_tokens(src, REGISTER)
        assert srcr
        return "SCAS(%s,%s,%d)" % (a, srcr[0], size)

    def process(self):
        self.merge_procs()
        self._remove_hacks()

    def _remove_hacks(self):
        for proc_name in self._procs:
            proc = self._context.symbols.get_global(proc_name)
            i = 0
            while i < len(proc.stmts):
                self._remove_hacks_popf(i, proc)
                #self._remove_hacks_pushpush_retf(i, proc)
                i += 1

    def _remove_hacks_pushpush_retf(self, i, proc):
        if len(proc.stmts) - i >= 3 and \
                proc.stmts[i].cmd == "push" and \
                proc.stmts[i + 1].cmd == "push" and \
                proc.stmts[i + 2].cmd == "retf":
            o = proc.create_instruction_object("jmp", [])
            o.children = [lark.Tree("expr",
                                    [lark.Tree("adddir",
                                               [lark.Tree(lark.Token("RULE", "braces"),
                                                          [lark.Token("LPAR", "("),
                                                           lark.Tree("shiftdir",
                                                                     [lark.Token("INTEGER", "1234"),
                                                                      lark.Token("SHOP", "SHL"),
                                                                      lark.Token("INTEGER", "4")]),
                                                           lark.Token("RPAR", ")")]),
                                                lark.Token("SIGN", "+"),
                                                lark.Token("INTEGER", "5678")])])]
            o.children[0].children[0].children[0].children[1].children[0] = proc.stmts[i + 1].children[0].children
            o.children[0].children[0].children[2] = proc.stmts[i].children[0].children
            o.filename = ""
            o.line_number = 0
            o.raw_line = ""
            o.syntetic = True
            proc.stmts[i] = o
            del proc.stmts[i + 1]
            del proc.stmts[i + 2]

    def _remove_hacks_popf(self, i, proc):
        # replace popf hack: or bh, 0; push cs; call loc+1
        if self._matches_popf_hack(proc, i, with_middle_label=True):
            logging.info("Patching popf hack")
            self._apply_popf_patch(proc, i, call_idx=i + 4, push_idx=i + 3)
        elif self._matches_popf_hack(proc, i, with_middle_label=False):
            logging.info("Patching popf hack")
            self._apply_popf_patch(proc, i, call_idx=i + 3, push_idx=i + 2)

    @staticmethod
    def _is_label_stmt(stmt: Any) -> bool:
        return stmt.cmd == "" and stmt.data == "label"

    @staticmethod
    def _single_child_tree(node: Any, data: str) -> lark.Tree | None:
        if not isinstance(node, lark.Tree) or node.data != data or len(node.children) != 1:
            return None
        child = node.children[0]
        return child if isinstance(child, lark.Tree) else None

    @staticmethod
    def _is_integer_expr_token(node: Any, value: str) -> bool:
        if not isinstance(node, lark.Tree) or node.data != "expr" or len(node.children) != 1:
            return False
        token = node.children[0]
        return isinstance(token, lark.Token) and token.type == "INTEGER" and token.value == value

    @staticmethod
    def _is_named_tree_expr(node: Any, expr_data: str, child_data: str, child_values: list[str]) -> bool:
        expr_child = Cpp._single_child_tree(node, expr_data)
        return bool(expr_child and expr_child.data == child_data and expr_child.children == child_values)

    @staticmethod
    def _is_or_bh_zero_stmt(stmt: Any) -> bool:
        if stmt.cmd != "or" or len(stmt.children) != 2:
            return False
        left, right = stmt.children
        return Cpp._is_named_tree_expr(left, "expr", "register", ["bh"]) and Cpp._is_integer_expr_token(right, "0")

    @staticmethod
    def _is_push_cs_stmt(stmt: Any) -> bool:
        if stmt.cmd != "push" or len(stmt.children) != 1:
            return False
        return Cpp._is_named_tree_expr(stmt.children[0], "expr", "segmentregister", ["cs"])

    @staticmethod
    def _is_call_adddir_stmt(stmt: Any) -> bool:
        return (
            stmt.cmd == "call"
            and stmt.children[0].data == "expr"
            and stmt.children[0].children[0].data == "adddir"
        )

    def _matches_popf_hack(self, proc: Any, i: int, *, with_middle_label: bool) -> bool:
        min_len, middle_label_idx, push_idx, call_idx = (
            (5, i + 2, i + 3, i + 4)
            if with_middle_label
            else (4, None, i + 2, i + 3)
        )
        if len(proc.stmts) - i < min_len:
            return False
        if not self._is_label_stmt(proc.stmts[i]):
            return False
        if not self._is_or_bh_zero_stmt(proc.stmts[i + 1]):
            return False
        if middle_label_idx is not None and not self._is_label_stmt(proc.stmts[middle_label_idx]):
            return False
        if not self._is_push_cs_stmt(proc.stmts[push_idx]):
            return False
        return self._is_call_adddir_stmt(proc.stmts[call_idx])

    def _apply_popf_patch(self, proc: Any, i: int, *, call_idx: int, push_idx: int) -> None:
        del proc.stmts[call_idx]
        del proc.stmts[push_idx]
        o = proc.create_instruction_object("popf", [])
        o.filename = ""
        o.line_number = 0
        o.raw_line = ""
        o.syntetic = True
        proc.stmts[i + 1] = o

    def save_cpp_files(self, fname):
        cpp_assigns, _, _, cpp_extern = self.render_data_c(self._context.segments)
        equates = self.produce_equates()

        header_id = f"__M2C_{self._namespace.upper().replace('-', '_').replace('.', '_')}_STUBS_H__"

        banner = """/* THIS IS GENERATED FILE */

        """

        cpp_fname = f"{self._namespace.lower()}.cpp"
        header_fname = f"{self._namespace.lower()}.h"

        logging.info(f" *** Generating output files in C++ {cpp_fname} {header_fname}")
        initializer_name = self._initializer_function_name(self._namespace)

        with open(cpp_fname, "w", encoding=self.__codeset) as cpp_file:
            hpp_file = open(header_fname, "w", encoding=self.__codeset)

            cpp_file.write(f"""{banner}
        /* Include STL headers before generated headers: MASM EQUs can coin
           names like "count" that would otherwise macro-break <algorithm>. */
        #include <algorithm>
        #include <iterator>
        #ifdef DOSBOX_CUSTOM
        #include <numeric>
        #endif
	        #include \"{header_fname}\"

	{self.render_function_wrappers_c()}
	{self.render_entrypoint_c()}
	{self.write_procedures(banner, header_fname)}
	{self.produce_global_jump_table(list(self._context.symbols.get_globals().items()), self._is_listing_source())}

        #include <algorithm>
        #include <iterator>
        #ifdef DOSBOX_CUSTOM
        #include <numeric>
         #define MYCOPY(x) {{m2c::set_type(x);m2c::mycopy((db*)&x,(db*)&tmp999,sizeof(tmp999),#x);}}
        #else
         #define MYCOPY(x) memcpy(&x,&tmp999,sizeof(tmp999));
        #endif

         namespace m2c {{
          void {initializer_name}()
          {{
          {cpp_assigns}
          }}
         }}
        #ifdef M2C_LEGACY_STATIC_INITIALIZERS
        #ifndef DOSBOX_CUSTOM
         namespace {{
          struct Initializer {{
           Initializer() {{ m2c::{initializer_name}(); }}
          }};
          static const Initializer i;
         }}
        #endif
        #endif
        """)
        hpp_file.write(f"""{banner}
#ifndef {header_id}
#define {header_id}

#include "asm.h"

{self.produce_structures(self._context.structures)}
	{equates}
	{self._module_data_rename_header()}
	{cpp_extern}
	{self._continuation_module_include()}
{self.produce_label_offsets()}
	#if __has_include("_equates.h")
	#include "_equates.h"
	#endif
{self.proc_strategy.write_declarations(self._procs + list(self.grouped), self._context)}
{self.produce_externals(self._context)}
#endif
""")

        hpp_file.close()
        self._write_module_data_header(cpp_extern + self.produce_externals(self._context))

        self.__methods += self.__failed
        done, failed = len(self.__proc_done), len(self.__failed)
        logging.info("%d ok, %d failed of %d, %3g%% translated", done, failed, done + failed,
                     100.0 * done / (done + failed))

        logging.info("\n".join(self.__failed))

        self.write_segment_file(
            self._context.segments,
            self._context.structures,
            fname,
            self._context.data_aliases,
            self.export_equates(),
            self._context.externals_abs,
            self.export_code_symbol_names(),
            self.export_defined_code_symbol_names(),
            self.export_external_code_symbol_names(),
            self.export_defined_code_symbol_offsets(),
            getattr(self._context, "code_offset_aliases", []),
            module_name=self._namespace,
            public_code_symbols={
                str(name).lower()
                for name in getattr(self._context, "public_symbols", set())
            },
        )

    def export_code_symbol_names(self) -> set[str]:
        return {
            name
            for name, symbol in self._context.symbols.get_globals().items()
            if isinstance(symbol, (op.label, Proc))
        }

    def export_defined_code_symbol_names(self) -> set[str]:
        return {
            name
            for name, symbol in self._context.symbols.get_globals().items()
            if isinstance(symbol, op.label) or (isinstance(symbol, Proc) and not symbol.extern)
        }

    def export_external_code_symbol_names(self) -> set[str]:
        external_proc_data_refs = getattr(self._context, "external_proc_data_refs", {})
        return {
            name
            for name, symbol in self._context.symbols.get_globals().items()
            if isinstance(symbol, Proc) and symbol.extern and name not in external_proc_data_refs
        } | self._data_referenced_code_symbol_names() | self._instruction_offset_referenced_code_symbol_names()

    def _data_referenced_code_symbol_names(self) -> set[str]:
        """Return code symbols stored in data initializers as indirect targets."""
        names: set[str] = set()
        data_labels = {
            str(data.label).lower()
            for segment in self._context.segments.values()
            for data in segment.getdata()
            if getattr(data, "label", "")
        }
        for segment in self._context.segments.values():
            for data in segment.getdata():
                for label in self._iter_data_value_labels(data.children):
                    if label in data_labels:
                        continue
                    symbol = self._context.symbols.get_global(label)
                    if isinstance(symbol, (op.label, Proc)):
                        names.add(label)
        return names

    def _iter_data_value_labels(self, value: Any):
        """Yield normalized label tokens nested inside data initializer values."""
        if isinstance(value, Token) and value.type in {"LABEL", "COMMON"}:
            yield self.sanitize_label_name(str(value))
            return
        if isinstance(value, Tree):
            for child in value.children:
                yield from self._iter_data_value_labels(child)
            return
        if isinstance(value, Data):
            yield from self._iter_data_value_labels(value.children)
            return
        if isinstance(value, (list, tuple)):
            for child in value:
                yield from self._iter_data_value_labels(child)

    def _instruction_offset_referenced_code_symbol_names(self) -> set[str]:
        """Return code labels whose OFFSET value is materialized by instructions."""
        names: set[str] = set()
        for symbol in self._context.symbols.get_globals().values():
            for label in self._iter_instruction_offset_labels(getattr(symbol, "stmts", [])):
                target = self._context.symbols.get_global(label)
                if isinstance(target, (op.label, Proc)):
                    names.add(label)
        return names

    def _iter_instruction_offset_labels(self, value: Any):
        """Yield labels that appear below an instruction OFFSET operator."""
        if isinstance(value, Tree):
            if value.data == "offsetdir":
                yield from self._iter_data_value_labels(value)
                return
            for child in value.children:
                yield from self._iter_instruction_offset_labels(child)
            return
        if isinstance(value, (list, tuple)):
            for child in value:
                yield from self._iter_instruction_offset_labels(child)

    def export_defined_code_symbol_offsets(self) -> dict[str, int]:
        """Return generated `m2c::k<label>` offsets for defined code symbols."""
        offsets: dict[str, int] = {"begin": 0x1001}
        current = 0x1001
        for name, symbol in self._context.symbols.get_globals().items():
            label = self.sanitize_label_name(name)
            if isinstance(symbol, op.var) and not symbol.external:
                offsets[label] = int(symbol.offset)
                continue
            if not isinstance(symbol, (op.label, Proc)):
                continue
            current += 1
            real_seg = getattr(symbol, "real_seg", None) or 0
            real_offset = getattr(symbol, "real_offset", None) or 0
            if real_offset or real_seg:
                current = real_seg * 0x10000 + real_offset
            if isinstance(symbol, Proc) and symbol.extern:
                continue
            offsets[label] = current
        for alias in getattr(self._context, "code_offset_aliases", []):
            if getattr(alias, "name", ""):
                offsets[self.sanitize_label_name(alias.name)] = int(alias.offset)
        return offsets

    def write_procedures(self, banner, header_fname):
        cpp_file_text = ""
        split_segment_includes: list[str] = []
        segment_texts: dict[str, str] = {}
        self.generate_label_to_proc_map()
        for name in self._procs:
            proc_text, segment = self._render_procedure(name)
            proc_text = self._postprocess_rendered_procedure(proc_text)
            if self._is_listing_source():  # If .lst write to separate segments
                if segment not in segment_texts:
                    segment_texts[segment] = ""
                    cpp_segment_fname = f"{self._namespace.lower()}_{segment}.cpp"
                    split_segment_includes.append(cpp_segment_fname)
                segment_texts[segment] += f"{proc_text}\n"
            else:
                cpp_file_text += f"{proc_text}\n"
            self.__proc_done.append(name)
            self.__methods.append(name)

        for i, segment in enumerate(segment_texts):
            cpp_segment_fname = split_segment_includes[i]
            logging.info(f" *** Generating output file in C++ {cpp_segment_fname}")
            with open(cpp_segment_fname, "w", encoding=self.__codeset) as cpp_segment_file:
                cpp_segment_file.write(f"""{banner}
#include "{header_fname}"

                """)
                cpp_segment_file.write(segment_texts[segment])

        if split_segment_includes:
            cpp_file_text += "\n".join(f'#include "{name}"' for name in split_segment_includes)
            cpp_file_text += "\n"

        return cpp_file_text

    @staticmethod
    def _postprocess_rendered_procedure(proc_text: str) -> str:
        return proc_text

    def produce_equates(self) -> str:
        result = ""
        for symbol in self._context.symbols.get_globals().values():
            if not isinstance(symbol, op._equ) or symbol.implemented:
                continue
            result += self.render_equate_definition(symbol.name, symbol)
            symbol.implemented = True
        self._cmdlabel = ""
        return result

    def export_equates(self) -> list[tuple[str, str, bool, str, bool]]:
        equates: list[tuple[str, str, bool, str, bool]] = []
        public_symbols: set[str] = getattr(self._context, "public_symbols", set())
        for symbol in self._context.symbols.get_globals().values():
            if not isinstance(symbol, (op._equ, op._assignment)):
                continue
            name = symbol.name if isinstance(symbol, op._equ) else str(symbol.children[0])
            scalar_equate = not isinstance(symbol.value, Expression)
            rendered = self.render_equate_value(symbol) if not scalar_equate else str(symbol.value)
            if (
                rendered
                and not self._is_module_local_equate_value(rendered)
                and not self._is_non_numeric_bare_equate_value(rendered)
            ):
                public = scalar_equate or isinstance(symbol, op._assignment) or name in public_symbols
                equates.append((
                    name,
                    rendered,
                    public,
                    getattr(symbol, "segment", ""),
                    bool(getattr(symbol, "location_counter_equate", False)),
                ))
        return equates

    @staticmethod
    def _is_module_local_equate_value(rendered: str) -> bool:
        return any(token in rendered for token in ("sizeof(", "offset(", "far_offset(", "seg_offset("))

    @staticmethod
    def _is_non_numeric_bare_equate_value(rendered: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z_@$?][A-Za-z0-9_@$?]*", rendered.strip()))

    def render_equate_definition(self, name: str, symbol: op._equ) -> str:
        if isinstance(symbol.value, str):
            return f"#define {name} {symbol.value}\n"
        if (alias := self._equ_alias_target(symbol)) is not None:
            return f"#define {name} ({alias})\n"
        rendered = self.render_equate_value(symbol)
        if not rendered:
            return ""
        code_label = re.fullmatch(r"m2c::k([A-Za-z_][A-Za-z0-9_]*)", rendered)
        if code_label:
            return f"#define {name} {code_label.group(1)}\n"
        if rendered.startswith("sizeof("):
            return f"static const int {name} = (int){rendered};\n"
        if not re.search(r"[A-Za-z_]", rendered):
            return f"static const int {name} = {rendered};\n"
        return f"#define {name} ({rendered})\n"

    def _equ_alias_target(self, symbol: op._equ) -> str | None:
        """Return the label name for a bare EQU alias to another equate."""
        value = symbol.value
        if not isinstance(value, Expression) or len(value.children) != 1:
            return None
        child = value.children[0]
        if isinstance(child, list) and len(child) == 1:
            child = child[0]
        if isinstance(child, Token) and child.type == "LABEL":
            target = self._context.symbols.get_global(str(child).lower())
            if isinstance(target, (op._equ, op._assignment)) and target is not symbol:
                return str(child).lower()
        return None

    def render_equate_value(self, symbol: Union[op._equ, op._assignment]) -> str:
        src = symbol.value
        if not isinstance(src, Expression):
            return ""
        if (folded := self._fold_location_counter_expression(symbol)) is not None:
            return folded
        if struct_size := self._equ_struct_size_name(src):
            return f"sizeof({struct_size})"
        src_render = self._clone_expression_for_render(src)
        src_render.indirection = IndirectionType.VALUE
        return self.render_instruction_argument(src_render)

    def render_entrypoint_c(self):
        if not self._context.main_file:
            return ""

        entry_point_text = ""
        g = self._context.symbols.get_global(self._context.entry_point)
        if isinstance(g, op.label) and self._context.entry_point not in self.grouped:
            entry_point_text = f"""
             bool {self.mangle_label(self._context.entry_point)}(m2c::_offsets, struct m2c::_STATE* _state){{return {self.label_to_proc[g.name]}(m2c::k{self._context.entry_point}, _state);}}
            """

        entry_point_text += f"""namespace m2c{{ m2cf* _ENTRY_POINT_ = &{self.mangle_label(self._context.entry_point)};}}
        """
        return entry_point_text

    def render_function_wrappers_c(self):
        grouped_wrappers = "".join(
            self._render_function_wrapper(p, self.groups[p], public=None)
            for p in sorted(self.grouped)
        )
        label_wrappers = "".join(
            self._render_function_wrapper(name, owner, public=public)
            for name, (owner, public) in sorted(self._label_wrapper_targets().items())
        )
        return grouped_wrappers + label_wrappers

    def _render_function_wrapper(self, name: str, owner: str, *, public: bool | None) -> str:
        linkage = self.wrapper_linkage(name, public=public)
        label = self.renderer.mangle_label(name)
        return f"""
 {linkage}bool {label}(m2c::_offsets _i, struct m2c::_STATE* _state){{return {owner}(_i ? _i : m2c::k{name}, _state);}}
"""

    def _label_wrapper_targets(self) -> dict[str, tuple[str, bool]]:
        targets: dict[str, tuple[str, bool]] = {}
        entry_point = getattr(self._context, "entry_point", "")
        externally_referenced = (
            self._data_referenced_code_symbol_names()
            | self._instruction_offset_referenced_code_symbol_names()
        )
        for proc_name in self._procs:
            proc = self._context.symbols.get_global(proc_name)
            if not proc or not hasattr(proc, "stmts"):
                continue
            for symbol in proc.stmts:
                if not isinstance(symbol, op.label):
                    continue
                name = symbol.name
                if name == entry_point:
                    continue
                if self._is_internal_label_wrapper_name(name) and name not in externally_referenced:
                    continue
                owner = self.label_to_proc.get(name)
                if not owner or owner == name or name in self._procs or name in self.grouped:
                    continue
                targets[name] = (owner, bool(getattr(symbol, "public_export", False)))
        return targets

    @staticmethod
    def _is_internal_label_wrapper_name(name: str) -> bool:
        lower = name.lower()
        return (
            lower.startswith("dummylabel")
            or lower.startswith("edummylabel")
            or lower.startswith("quequel")
            or "_arb" in lower
        )

    def convert_segment_files_into_datacpp(self, asm_files):
        """It reads .seg files, and writes the data segments to _data.cpp/h file.

        :param asm_files: A list of the assembly files
        """
        self.write_data_segments_cpp(*self.read_segment_files(asm_files), asm_files=asm_files)

    def write_data_segments_cpp(self, segments, structures, asm_files=None):
        """It writes the _data.cpp and _data.h files.

        :param segments: a list of segments, each segment is a list of data items
        :param structures: a list of structures that are defined in the program
        """
        logging.info(" *** Producing _data.cpp and _data.h files")
        segments = self._deduplicate_memory_field_labels(segments)
        previous_segments = self._context.segments
        previous_structures = self._context.structures
        self._context.segments = segments
        self._context.structures = structures
        try:
            _, data_h, data_cpp_reference, data_externs = self.render_data_c(segments)
        finally:
            self._context.segments = previous_segments
            self._context.structures = previous_structures
        data_labels = self._data_label_names(segments)
        data_labels.update(
            str(alias.name).lower()
            for alias in getattr(self._context, "data_aliases", [])
            if getattr(alias, "name", "")
        )
        self._write_equates_header(
            getattr(self._context, "exported_equates", []),
            data_labels,
            getattr(
                self._context,
                "all_defined_code_symbol_offsets",
                getattr(self._context, "exported_code_symbol_offsets", {}),
            ),
        )
        self._write_data_renames_header()
        self._write_data_reference_chunks(data_cpp_reference)
        fname = "_data.cpp"
        header = "_data.h"
        types_header = "_data_types.h"
        linked_segment_helpers = self._produce_linked_segment_helpers(segments)
        linked_code_segment_address_helper = self._produce_linked_code_segment_address_helper(segments)
        aggregate_initializer = self._produce_aggregate_initializer(asm_files or [])
        with open(fname, "w", encoding=self.__codeset) as fd:
            fd.write("""#include "_data.h"
#if __has_include("_equates.h")
#include "_equates.h"
#endif
""" + self._produce_external_code_declarations() + """
namespace m2c{

struct Memory m;

struct Memory types;

db(& stack)[STACK_SIZE]=m.stack;
db(& heap)[HEAP_SIZE]=m.heap;
""" + linked_segment_helpers + """
""" + self._produce_external_code_dispatcher() + """
""" + linked_code_segment_address_helper + """
""" + aggregate_initializer + """
}

""")

        with open(types_header, "w", encoding=self.__codeset) as th:
            th.write("""
#ifndef ___DATA_TYPES_H__
#define ___DATA_TYPES_H__
#include "asm.h"
""" + self.produce_structures(structures) + """
#endif
""")

        with open(header, "w", encoding=self.__codeset) as hd:
            hd.write("""
#ifndef ___DATA_H__
#define ___DATA_H__
#include "_data_types.h"
""" + self.produce_data(data_h) + data_externs + """
#endif
""")

    def _write_data_reference_chunks(self, data_cpp_reference: str) -> None:
        self._remove_old_data_reference_chunks()
        lines = data_cpp_reference.splitlines()
        if not lines:
            return
        for index in range(0, len(lines), DATA_REF_LINES_PER_FILE):
            chunk = lines[index:index + DATA_REF_LINES_PER_FILE]
            chunk_name = f"_data_refs_{index // DATA_REF_LINES_PER_FILE:03d}.cpp"
            with open(chunk_name, "w", encoding=self.__codeset) as fd:
                fd.write('#include "_data.h"\n')
                fd.write("\n".join(chunk))
                fd.write("\n")

    def _remove_old_data_reference_chunks(self) -> None:
        for name in os.listdir("."):
            if re.fullmatch(r"_data_refs_\d{3}\.cpp", name):
                os.remove(name)

    def _produce_external_code_dispatcher(self) -> str:
        """Build a merged dispatcher for code offsets defined by other modules."""
        offsets = getattr(
            self._context,
            "exported_callable_code_symbol_offsets",
            getattr(self._context, "exported_code_symbol_offsets", {}),
        )
        lines = [
            "bool dispatch_external_code(_offsets __disp, _STATE* _state, bool* handled) {",
            "    if (handled) { *handled = false; }",
            "    switch (__disp) {",
        ]
        emitted_offsets: set[int] = set()
        for name in sorted(offsets):
            label = self.sanitize_label_name(str(name))
            function = self.mangle_label(label)
            offset = int(offsets[name])
            if offset in emitted_offsets:
                continue
            emitted_offsets.add(offset)
            lines.extend([
                f"        case 0x{offset:x}:",
                "            if (handled) { *handled = true; }",
                f"            return {function}(0, _state);",
            ])
        lines.extend([
            "        default: {",
            "            bool res = true;",
            "            if (host_try_overlay_retf(__disp, _state, &res)) {",
            "                if (handled) { *handled = true; }",
            "                return res;",
            "            }",
            "            return true;",
            "        }",
            "    }",
            "}",
            "",
        ])
        return "\n".join(lines)

    def _produce_external_code_declarations(self) -> str:
        """Declare callable code wrappers needed only by the merged dispatcher."""
        offsets = getattr(
            self._context,
            "exported_callable_code_symbol_offsets",
            getattr(self._context, "exported_code_symbol_offsets", {}),
        )
        lines = []
        for name in sorted(offsets):
            label = self.sanitize_label_name(str(name))
            lines.append(f"extern bool {self.mangle_label(label)}(m2c::_offsets, struct m2c::_STATE*);")
        if not lines:
            return ""
        return "\n".join(lines) + "\n"

    def _write_equates_header(
        self,
        equates: list[tuple[str, str]],
        data_labels: set[str] | None = None,
        code_symbol_offsets: dict[str, int] | None = None,
    ) -> None:
        with open("_equates.h", "w", encoding=self.__codeset) as f:
            f.write("#ifndef __M2C_EQUATES_H__\n#define __M2C_EQUATES_H__\n\n#include \"asm.h\"\n\n")
            code_equates: list[tuple[str, str]] = []
            code_offset_equates = [
                (str(name), f"0x{int(offset):x}")
                for name, offset in (code_symbol_offsets or {}).items()
            ]
            for item in equates:
                if len(item) == 2:
                    name, value = item
                    is_code_symbol = False
                else:
                    name, value, is_code_symbol = item
                if is_code_symbol:
                    code_equates.append((name, value))
                    continue
                if data_labels and str(name).lower() in data_labels:
                    continue
                f.write(f"#ifndef {name}\n#define {name} ({value})\n#endif\n")
            code_equate_names = {self.sanitize_label_name(name) for name, _value in code_equates}
            for name, value in code_offset_equates:
                if self.sanitize_label_name(name) not in code_equate_names:
                    code_equates.append((name, value))
            code_renames = getattr(self._context, "code_label_renames", []) or []
            qualified_constants = sorted({
                str(new)
                for _macro, old, new in code_renames
                if str(old).startswith("kglobal_")
            })
            if code_equates or qualified_constants:
                exported_offsets = getattr(self._context, "exported_code_symbol_offsets", {}) or {}
                f.write("\n")
                self._write_known_code_equate_externs(f, code_equates)
                f.write("\nnamespace m2c{\n")
                for name, value in code_equates:
                    label = self.sanitize_label_name(str(name))
                    guard = self.code_equate_guard_name(label)
                    global_offset = exported_offsets.get(str(name).lower())
                    global_value = f"0x{int(global_offset):x}" if global_offset is not None else value
                    f.write(f"#ifndef {guard}\n#define {guard} 1\n")
                    f.write(f"static const dd k{label} = ({value});\n#endif\n")
                    f.write(f"static const dd {self.global_code_offset_constant(label)} = ({global_value});\n")
                for constant in qualified_constants:
                    qualified = self.sanitize_label_name(constant[len("kglobal_"):])
                    offset = exported_offsets.get(qualified)
                    if offset is None:
                        continue
                    f.write(f"static const dd {constant} = (0x{int(offset):x});\n")
                f.write("}\n")
            # Module-scoped renames for code symbols defined in several merged
            # modules.  Emitted after every kglobal_* constant so the macros
            # only rewrite use sites (function definitions, dispatch tables),
            # never the constant declarations above.
            for module_macro, old_name, new_name in code_renames:
                f.write(
                    f"\n#if defined({module_macro})\n"
                    f"#ifndef {old_name}\n"
                    f"#define {old_name} {new_name}\n"
                    "#endif\n"
                    "#endif\n"
                )
            f.write("\n#endif\n")

    @staticmethod
    def _data_label_names(segments) -> set[str]:
        labels: set[str] = set()
        for segment in segments.values():
            for data in segment.getdata():
                label = getattr(data, "label", "")
                if label:
                    labels.add(str(label).lower())
        return labels

    @classmethod
    def _write_known_code_equate_externs(cls, f, code_equates: list[tuple[str, str]]) -> None:
        """Emit extra declarations for code-equate constants."""

    @staticmethod
    def sanitize_label_name(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_]", "_", str(name)).lower()

    @classmethod
    def code_equate_guard_name(cls, name: str) -> str:
        return f"M2C_CODE_EQUATE_{cls.sanitize_label_name(name)}"

    @classmethod
    def global_code_offset_constant(cls, name: str) -> str:
        """Return the collision-free aggregate code offset constant name."""
        return f"kglobal_{cls.sanitize_label_name(name)}"

    def _write_data_renames_header(self) -> None:
        with open("_data_renames.h", "w", encoding=self.__codeset) as f:
            f.write("#ifndef __M2C_DATA_RENAMES_H__\n#define __M2C_DATA_RENAMES_H__\n\n")
            for module_macro, old_name, new_name in self._data_label_renames:
                f.write(
                    f"#if defined({module_macro})\n"
                    f"#ifndef {old_name}\n"
                    f"#define {old_name} {new_name}\n"
                    "#endif\n"
                    "#endif\n\n"
                )
            f.write("#endif\n")

    def _module_data_rename_header(self) -> str:
        module_macro = self._module_macro_name(self._namespace)
        return (
            f"#define {module_macro} 1\n"
            '#if __has_include("_data_renames.h")\n'
            '#include "_data_renames.h"\n'
            "#endif\n"
        )

    def _continuation_module_include(self) -> str:
        match = re.fullmatch(r"(?P<prefix>.+?)(?P<index>[2-9])", self._namespace.lower())
        if not match:
            return ""
        previous = f"{match.group('prefix')}{int(match.group('index')) - 1}_data.h"
        return (
            f'#if __has_include("{previous}")\n'
            f'#include "{previous}"\n'
            "#endif\n"
        )

    def _write_module_data_header(self, cpp_extern: str) -> None:
        if not cpp_extern.strip():
            return
        header = f"{self._namespace.lower()}_data.h"
        guard = f"__M2C_{self._namespace.upper()}_DATA_H__"
        with open(header, "w", encoding=self.__codeset) as f:
            offset_constants, offset_aliases = self._module_label_offset_aliases()
            shared_data_include = (
                '#if __has_include("gwdata_data.h")\n#include "gwdata_data.h"\n#endif\n\n'
                if self._namespace.lower() == "math1"
                else ""
            )
            f.write(
                f"#ifndef {guard}\n"
                f"#define {guard}\n\n"
                '#include "asm.h"\n\n'
                f"{shared_data_include}"
                f"{cpp_extern}"
                f"{offset_constants}"
                f"{offset_aliases}"
                "\n#endif\n"
            )

    def _module_label_offset_aliases(self) -> tuple[str, str]:
        from masm2c.proc import Proc

        result = "namespace m2c{\n"
        offset = 0x1001
        for name, symbol in list(self._context.symbols.get_globals().items()):
            if not isinstance(symbol, (op.label, Proc)):
                continue
            label = re.sub(r"[^A-Za-z0-9_]", "_", name).lower()
            offset += 1
            real_seg = getattr(symbol, "real_seg", None) or 0
            real_offset = getattr(symbol, "real_offset", None) or 0
            if real_offset or real_seg:
                offset = real_seg * 0x10000 + real_offset
            if not isinstance(symbol, op.label):
                continue
            if label in getattr(self._context, "externals_procs", set()):
                continue
            guard = self.code_equate_guard_name(label)
            result += f"#ifndef {guard}\n#define {guard} 1\n"
            result += f"static const dd k{label} = 0x{offset:x};\n#endif\n"
        result += "}\n"
        data_aliases = self._module_data_offset_aliases()
        return result + data_aliases + "\n", "\n"

    def _module_data_offset_aliases(self) -> str:
        result = "namespace m2c{\n"
        aliases = ""
        emitted: set[str] = set()
        for segment in self._context.segments.values():
            for data in segment.getdata():
                if not getattr(data, "label", ""):
                    continue
                label = self.sanitize_label_name(data.label)
                if label.startswith(("dummy", "edummy")):
                    continue
                if label in emitted:
                    continue
                emitted.add(label)
                guard = self.code_equate_guard_name(label)
                result += f"#ifndef {guard}\n#define {guard} 1\n"
                result += f"static const dd k{label} = (m2c::near_offset_external(::{label}));\n#endif\n"
                aliases += f"#ifndef {label}\n#define {label} m2c::k{label}\n#endif\n"
        if not emitted:
            return ""
        return result + "}\n" + aliases

    @staticmethod
    def _module_macro_name(name: str) -> str:
        normalized = re.sub(r"[^A-Za-z0-9_]", "_", name).upper()
        return f"M2C_MODULE_{normalized or 'UNKNOWN'}"

    def _deduplicate_memory_field_labels(self, segments: OrderedDict) -> OrderedDict:
        result = deepcopy(segments)
        self._data_label_renames = []
        seen: set[str] = set()
        for segment in result.values():
            for data in segment.getdata():
                if not data.label:
                    continue
                label = data.label.lower()
                if label not in seen:
                    seen.add(label)
                    continue
                old_label = data.label.lower()
                data.label = self._unique_memory_field_label(data, seen)
                module = os.path.splitext(os.path.basename(data.filename or ""))[0]
                self._data_label_renames.append(
                    (self._module_macro_name(module), old_label, data.label.lower())
                )
                seen.add(data.label.lower())
        self._merged_field_label_names = seen
        return result

    @staticmethod
    def _unique_memory_field_label(data: Data, seen: set[str]) -> str:
        base = data.label.lower()
        source = os.path.splitext(os.path.basename(data.filename or ""))[0].lower()
        suffix_parts = [part for part in (source, f"{data.offset:x}", str(data.line_number)) if part]
        suffix = "_".join(re.sub(r"[^A-Za-z0-9_]", "_", part) for part in suffix_parts) or "dup"
        candidate = f"{base}__{suffix}"
        index = 2
        while candidate.lower() in seen:
            candidate = f"{base}__{suffix}_{index}"
            index += 1
        return candidate

    def _produce_linked_segment_helpers(self, segments: OrderedDict) -> str:
        anchors = self._linked_segment_anchors(segments)
        if not anchors:
            return """

dw near_offset_linked_address(const void* symbol) {
    const size_t linear = reinterpret_cast<const db*>(symbol) - reinterpret_cast<const db*>(&m);
    return static_cast<dw>(RM_OFFSET(linear));
}

dw segment_of_linked_address(const void* symbol) {
    const size_t linear = reinterpret_cast<const db*>(symbol) - reinterpret_cast<const db*>(&m);
    return static_cast<dw>(RM_SEGMENT(linear));
}

dd far_offset_linked_address(const void* symbol) {
    return static_cast<dd>(near_offset_linked_address(symbol) | (segment_of_linked_address(symbol) << 16));
}

void copy_linked_program_segment_prefix(dw segment, const void* source, size_t size) {
    std::memmove((db*)&m + (static_cast<size_t>(segment) << 4), source, size);
}
"""

        entries = "\n".join(
            f"    {{reinterpret_cast<const db*>(&::{name}), 0x{linear:x}, {str(is_data).lower()}}},"
            for linear, name, is_data in anchors
        )
        linked_data_raddr_body = """    for (const LinkedSegmentAnchor& anchor : linked_segment_anchors) {
        if (anchor.is_data && segment == static_cast<dw>(anchor.linear >> 4)) {
            return const_cast<db*>(anchor.base) + offset;
        }
    }
    return nullptr;"""
        return f"""

struct LinkedSegmentAnchor {{
    const db* base;
    size_t linear;
    bool is_data;
}};

dw linked_data_runtime_segment = 0;
static dw linked_data_runtime_segments[8] = {{}};

static const LinkedSegmentAnchor linked_segment_anchors[] = {{
{entries}
}};

static const LinkedSegmentAnchor* find_linked_segment_anchor(const void* symbol) {{
    const db* ptr = reinterpret_cast<const db*>(symbol);
    const LinkedSegmentAnchor* selected = nullptr;
    for (const LinkedSegmentAnchor& anchor : linked_segment_anchors) {{
        if (ptr >= anchor.base && (selected == nullptr || anchor.base >= selected->base)) {{
            selected = &anchor;
        }}
    }}
    return selected;
}}

static const LinkedSegmentAnchor* primary_linked_data_anchor() {{
    for (const LinkedSegmentAnchor& anchor : linked_segment_anchors) {{
        if (anchor.linear != 0 && anchor.is_data) {{
            return &anchor;
        }}
    }}
    return nullptr;
}}

static bool is_linked_data_runtime_segment(dw segment) {{
    if (segment == 0) {{
        return false;
    }}
    if (segment == linked_data_runtime_segment) {{
        return true;
    }}
    for (dw known_segment : linked_data_runtime_segments) {{
        if (segment == known_segment) {{
            return true;
        }}
    }}
    return false;
}}

static void remember_linked_data_runtime_segment(dw segment) {{
    if (segment == 0 || segment >= 0xa000 || is_linked_data_runtime_segment(segment)) {{
        return;
    }}
    linked_data_runtime_segment = segment;
    for (dw& known_segment : linked_data_runtime_segments) {{
        if (known_segment == 0) {{
            known_segment = segment;
            return;
        }}
    }}
    for (size_t i = 1; i < sizeof(linked_data_runtime_segments) / sizeof(linked_data_runtime_segments[0]); ++i) {{
        linked_data_runtime_segments[i - 1] = linked_data_runtime_segments[i];
    }}
    linked_data_runtime_segments[sizeof(linked_data_runtime_segments) / sizeof(linked_data_runtime_segments[0]) - 1] = segment;
}}

db* linked_data_segment_raddr(dw segment, dw offset) {{
{linked_data_raddr_body}
}}

void set_segment_register(dw& reg, dw value) {{
    reg = value;
    remember_linked_data_runtime_segment(value);
}}

dw near_offset_linked_address(const void* symbol) {{
    if (const LinkedSegmentAnchor* anchor = find_linked_segment_anchor(symbol)) {{
        const size_t linear = anchor->linear + (reinterpret_cast<const db*>(symbol) - anchor->base);
        return static_cast<dw>(linear - ((anchor->linear >> 4) << 4));
    }}
    const size_t linear = reinterpret_cast<const db*>(symbol) - reinterpret_cast<const db*>(&m);
    return static_cast<dw>(RM_OFFSET(linear));
}}

dw segment_of_linked_address(const void* symbol) {{
    if (const LinkedSegmentAnchor* anchor = find_linked_segment_anchor(symbol)) {{
        return static_cast<dw>(anchor->linear >> 4);
    }}
    const size_t linear = reinterpret_cast<const db*>(symbol) - reinterpret_cast<const db*>(&m);
    return static_cast<dw>(RM_SEGMENT(linear));
}}

dd far_offset_linked_address(const void* symbol) {{
    return static_cast<dd>(near_offset_linked_address(symbol) | (segment_of_linked_address(symbol) << 16));
}}

void copy_linked_program_segment_prefix(dw segment, const void* source, size_t size) {{
    bool copied = false;
    for (const LinkedSegmentAnchor& anchor : linked_segment_anchors) {{
        if ((anchor.linear >> 4) == segment) {{
                std::memmove(const_cast<db*>(anchor.base), source, size);
            copied = true;
        }}
    }}
    if (!copied) {{
        std::memmove((db*)&m + (static_cast<size_t>(segment) << 4), source, size);
    }}
}}
"""

    def _linked_segment_anchors(self, segments: OrderedDict) -> list[tuple[int, str, bool]]:
        anchors_by_linear: dict[int, tuple[str, bool]] = {}
        for segment_name, segment in segments.items():
            if not segment.getdata() or str(getattr(segment, "segclass", "")).lower() == "code":
                continue
            is_data = not self._is_code_storage_segment(segment)
            aliases = {segment.name: 0, **getattr(segment, "segment_aliases", {segment.name: 0})}
            aliases = {segment_name: 0, **aliases}
            for name, relative_offset in aliases.items():
                linear = self._segment_binding_linear(segment, relative_offset, segment_name)
                anchors_by_linear.setdefault(linear, (name, is_data))
        return [(linear, name, is_data) for linear, (name, is_data) in sorted(anchors_by_linear.items())]

    def _produce_linked_code_segment_address_helper(self, segments: OrderedDict) -> str:
        """Build runtime address mapping for linked code-segment data records."""
        range_groups: dict[tuple[int, tuple[int, ...]], list[tuple[int, int]]] = {}
        for segment_name, segment in segments.items():
            if not (self._is_code_storage_segment(segment) or self._looks_like_code_segment(segment)):
                continue
            linear_base = self._segment_binding_linear(segment, 0, segment_name)
            runtime_segments = self._runtime_code_segments_for_base(linear_base)
            key = (linear_base, tuple(sorted(runtime_segments)))
            intervals = range_groups.setdefault(key, [])
            for data in segment.getdata():
                start = int(data.offset)
                end = start + self._linked_code_data_span(data)
                if end > start:
                    intervals.append((start, end))
        if not range_groups:
            return ""
        all_segments = sorted({segment for _, segments_key in range_groups for segment in segments_key})
        segment_guard = self._render_segment_reject_guard(all_segments)
        range_lines: list[str] = []
        for (linear_base, runtime_segment_key), intervals in sorted(range_groups.items()):
            segment_match = "" if list(runtime_segment_key) == all_segments else f"{self._render_segment_match(runtime_segment_key)} && "
            for start, end in self._merge_intervals(intervals):
                range_lines.append(
                    f"    if ({segment_match}offset >= 0x{start:x} && offset < 0x{end:x}) "
                    f"{{ return (db*)&m + 0x{linear_base:x} + offset; }}"
                )
        ranges = "\n".join(range_lines)
        return f"""

db* linked_code_segment_raddr(dw segment, dw offset) {{
{segment_guard}
{ranges}
    return nullptr;
}}
"""

    def _runtime_code_segments_for_base(self, linear_base: int) -> set[int]:
        """Return segment values that may address generated code bytes."""
        segments = {int(linear_base) >> 4, self._load_segment_linear_base() >> 4}
        segments.add(0x192)
        return segments

    @staticmethod
    def _render_segment_match(segments: tuple[int, ...]) -> str:
        """Render a C++ expression that matches any accepted segment."""
        if len(segments) == 1:
            return f"segment == 0x{segments[0]:x}"
        return "(" + " || ".join(f"segment == 0x{segment:x}" for segment in segments) + ")"

    def _render_segment_reject_guard(self, segments: list[int]) -> str:
        """Render a fast reject guard for code segment address lookup."""
        if len(segments) == 1:
            return f"    if (segment != 0x{segments[0]:x}) {{ return nullptr; }}"
        reject = " && ".join(f"segment != 0x{segment:x}" for segment in segments)
        return f"    if ({reject}) {{ return nullptr; }}"

    def _linked_code_data_span(self, data: Data) -> int:
        """Return the byte span that a code-segment data record occupies."""
        stored_size = int(data.getsize() or 0)
        element_count = int(getattr(data, "elements", 0) or 0)
        try:
            element_size = int(self._context.typetosize(data.data_type) or 0)
        except Exception:
            element_size = 0
        declared_size = element_count * element_size
        return max(stored_size, declared_size)

    @staticmethod
    def _merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Merge overlapping or adjacent half-open intervals."""
        merged: list[tuple[int, int]] = []
        for start, end in sorted(intervals):
            if not merged or start > merged[-1][1]:
                merged.append((start, end))
            else:
                previous_start, previous_end = merged[-1]
                merged[-1] = (previous_start, max(previous_end, end))
        return merged

    def _produce_aggregate_initializer(self, asm_files: list[str]) -> str:
        sources = [str(f) for f in asm_files if str(f).lower().endswith((".asm", ".lst", ".seg"))]
        by_basename: dict[str, list[str]] = {}
        for source in sources:
            base = os.path.splitext(os.path.basename(source))[0].lower()
            by_basename.setdefault(base, []).append(source)
        module_names: dict[str, str] = {}
        for base, paths in by_basename.items():
            if len(paths) < 2:
                continue
            for path in paths:
                parent = os.path.basename(os.path.dirname(os.path.abspath(path))).lower() or "mod"
                module_names[path] = re.sub(r"[^A-Za-z0-9_]", "_", f"{parent}_{base}")
        sidecar_names = getattr(self._context, "merged_module_names", None) or {}
        initializer_names: list[str] = []
        seen: set[str] = set()
        for filename in sources:
            module = (
                sidecar_names.get(filename)
                or module_names.get(filename)
                or os.path.splitext(os.path.basename(filename))[0]
            )
            name = self._initializer_function_name(module)
            if name in seen:
                continue
            seen.add(name)
            initializer_names.append(name)

        declarations = "\n".join(f"void {name}();" for name in initializer_names)
        calls = "\n".join(f"    {name}();" for name in initializer_names)
        return f"""

{declarations}

void Initializer() {{
    static bool initialized = false;
    if (initialized) {{
        return;
    }}
    initialized = true;
{calls}
}}
"""

    @staticmethod
    def _initializer_function_name(module: str) -> str:
        normalized = re.sub(r"[^A-Za-z0-9_]", "_", module).lower()
        return f"Initializer_{normalized or 'unknown'}"

    def produce_label_offsets(self):
        labeloffsets = """namespace m2c{
void   Initializer();
#ifndef M2C_CODE_EQUATE_begin
#define M2C_CODE_EQUATE_begin 1
static const dd kbegin = 0x1001;
#endif
"""
        i = 0x1001
        for k, v in list(self._context.symbols.get_globals().items()):
            if isinstance(v, (op.label, Proc)):
                if isinstance(v, Proc) and v.extern and self._is_public_code_offset_export(k):
                    continue
                k = self.sanitize_label_name(k)
                i += 1
                if v.real_offset or v.real_seg:
                    i = v.real_seg * 0x10000 + v.real_offset
                line = f"static const dd k{k} = 0x{i:x};\n"
                guard = self.code_equate_guard_name(k)
                if guard:
                    line = f"#ifndef {guard}\n#define {guard} 1\n{line}#endif\n"
                labeloffsets += line
        labeloffsets += "}\n"
        return labeloffsets

    def produce_structures(self, strucs: dict[str, "Struct"]):
        structures = "\n"
        if strucs:
            structures += """#pragma pack(push, 1)"""

        for name, v in strucs.items():
            struc_type = "struct" if v.gettype() == op.Struct.STRUCT else "union"
            structures += f"""
{struc_type} {name} {{
"""
            for member in v.getdata().values():
                array_suffix = f"[{member.elements}]" if member.elements > 1 else ""
                structures += f"  {member.data_type} {member.label}{array_suffix};\n"
            structures += """};
"""
        if strucs:
            structures += """
#pragma pack(pop)

"""
        structures += self._produce_old_struct_member_offsets()
        return structures

    def _produce_old_struct_member_offsets(self) -> str:
        offsets = getattr(self._context, "old_struct_member_offsets", {})
        if not offsets:
            return ""
        result = ""
        for member_name, (struct_name, _offset, _size) in offsets.items():
            const_name = self._old_struct_member_offset_constant_name(member_name)
            result += f"static const word {const_name} = {self._offsetof_decl(struct_name, member_name)};\n"
        return f"{result}\n"

    def _old_struct_member_offset_constant_name(self, member_name: str) -> str:
        member_name = str(member_name).lower()
        offsets = getattr(self._context, "old_struct_member_offsets", {})
        if member_name not in offsets:
            return member_name
        global_symbol = self._context.symbols.get_global(member_name)
        if (global_symbol is not None and not isinstance(global_symbol, op.Struct)) or self._data_label_exists(member_name):
            return f"__m2c_member_{member_name}"
        return member_name

    def _is_old_struct_member_offset_context(self, name: str) -> bool:
        if str(name).lower() not in getattr(self._context, "old_struct_member_offsets", {}):
            return False
        state = self._expr_state
        return state.indirection == IndirectionType.POINTER and not state.is_just_label

    def _remember_old_struct_member_size(self, name: str) -> None:
        member_info = getattr(self._context, "old_struct_member_offsets", {}).get(str(name).lower())
        if not member_info:
            return
        _struct_name, _offset, member_size = member_info
        self._expr_state.variable_size = member_size
        if self._middle_size == 0:
            self._middle_size = member_size

    def _data_label_exists(self, label: str) -> bool:
        label = str(label).lower()
        for segment in self._context.segments.values():
            for data in segment.getdata():
                if data.label.lower() == label:
                    return True
        return False

    def produce_data(self, hdata_bin):
        data_head = """
#pragma pack(push, 1)
namespace m2c{
struct Memory{
"""
        data_head += "".join(hdata_bin)
        data_head += """
#ifdef DOSBOX_CUSTOM
    db filll[1024*1024*16];
#endif
                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                """
        data_head += """};
}
#pragma pack(pop)
"""
        return data_head

    def produce_externals(self, context):
        data = "\n"
        external_proc_data_refs = getattr(context, "external_proc_data_refs", {})
        declared = set(getattr(self, "_merged_field_label_names", ()))
        for i in context.externals_vars:
            v = context.symbols.get_global(i)
            if v.used:
                if v.name.lower() in declared:
                    continue
                declared.add(v.name.lower())
                data += (
                    f"#ifndef {v.name}\n"
                    f"extern {self._cpp_external_type(v.original_type)}& {v.name};\n"
                    "#endif\n"
                )
        for name, original_type in sorted(external_proc_data_refs.items()):
            if name.lower() in declared:
                continue
            data += (
                f"#ifndef {name}\n"
                f"extern {self._cpp_external_type(original_type)}& {name};\n"
                "#endif\n"
            )
        return data

    def _cpp_external_type(self, data_ctype: str) -> str:
        aliases = {
            "byte": "db",
            "sbyte": "char",
            "word": "dw",
            "sword": "short",
            "dword": "dd",
            "sdword": "int",
            "qword": "dq",
        }
        return self._cpp_data_type(aliases.get(data_ctype.lower(), data_ctype))

    def _lea(self, dst: Expression, src: Expression) -> str:
        src_render = self._clone_expression_for_render(src)
        src_render.indirection = IndirectionType.OFFSET
        a, b = self.parse2(dst, src_render, lea=True)
        return f"{a} = {b}"

    def _movs(self, dst: Expression, src: Expression) -> str:
        size = self.calculate_size(dst)
        dstr, srcr = Token_.find_tokens(dst, REGISTER), Token_.find_tokens(src, REGISTER)
        if dstr and srcr:
            a, b = self.parse2(dst, src)
            return "MOVS(%s, %s, %s, %s, %d)" % (a, b, dstr[0], srcr[0], size)

        dreg, sreg = self._movs_index_registers(dst, src)
        a = self._string_op_indexed_operand(dst.segment_register or "es", dreg, size)
        b = self._string_op_indexed_operand(src.segment_register or "ds", sreg, size)
        return "MOVS(%s, %s, %s, %s, %d)" % (a, b, dreg, sreg, size)

    @staticmethod
    def _movs_index_registers(dst: Expression, src: Expression) -> tuple[str, str]:
        registers = set(getattr(dst, "registers", set())) | set(getattr(src, "registers", set()))
        if {"edi", "esi"}.intersection(registers):
            return "edi", "esi"
        return "di", "si"

    @staticmethod
    def _string_op_indexed_operand(segment: str, index_register: str, size: int) -> str:
        c_type = {1: "db", 2: "dw", 4: "dd", 8: "dq"}.get(size, "db")
        return f"*(({c_type}*)raddr({segment},{index_register}))"

    def _repe(self):
        self.prefix = "\tREPE "
        return ""

    def _repne(self):
        self.prefix = "\tREPNE "
        return ""

    def _lods(self, src: Expression) -> str:
        size = self.calculate_size(src)
        srcr = Token_.find_tokens(src, REGISTER)
        if srcr:
            a = self.render_instruction_argument(src)
            return "LODS(%s,%s,%d)" % (a, srcr[0], size)
        sreg = "esi" if "esi" in getattr(src, "registers", set()) else "si"
        a = self._string_op_indexed_operand(src.segment_register or "ds", sreg, size)
        return "LODS(%s,%s,%d)" % (a, sreg, size)

    def _leave(self) -> str:
        return "LEAVE"  # MOV(esp, ebp) POP(ebp)

    def _int(self, dst: Expression) -> str:
        a = self.render_instruction_argument(dst)
        return f"_INT({a})"

    def _instruction0(self, cmd: str) -> str:
        if cmd.upper() in {"QUEZ0"}:
            return ""
        return cmd.upper()

    def _instruction1(self, cmd: str, dst: Expression) -> str:
        default_size = 2 if cmd.lower() in {"push", "pop"} else 0
        a = self.render_instruction_argument(dst, def_size=default_size)
        return f"{cmd.upper()}({a})"

    def render_instruction_argument(self, expr: Expression, def_size: int = 0, destination: bool = False,
                                    lea: bool = False) -> str:
        result, _ = self.render_instruction_argument_with_state(
            expr,
            def_size,
            destination=destination,
            lea=lea,
        )
        return result

    @staticmethod
    def _clone_expression_for_render(expr: Expression) -> Expression:
        cloned = copy(expr)
        cloned.mods = set(expr.mods)
        cloned.registers = set(expr.registers)
        return cloned

    def _prepare_expression_for_render(
            self,
            expr: Expression,
            def_size: int = 0,
            *,
            destination: bool = False,
            lea: bool = False,
    ) -> tuple[Expression, int]:
        render_expr = self._clone_expression_for_render(expr)
        if destination:
            render_expr.mods.add("destination")
        if lea:
            render_expr.mods.add("lea")

        if def_size == 0 and render_expr.element_size == 0 and render_expr.indirection != IndirectionType.POINTER:
            from .parser import ExprSizeCalculator, Vector
            calc = ExprSizeCalculator(init=Vector(0, 0), context=self._context)
            def_size, _ = calc.visit(render_expr).values

        if render_expr.indirection == IndirectionType.POINTER and def_size and not render_expr.ptr_size:
            render_expr.ptr_size = def_size
        if def_size and render_expr.element_size == 0:
            render_expr.element_size = def_size
        return render_expr, def_size

    def render_instruction_argument_with_state(
            self,
            expr: Expression,
            def_size: int = 0,
            *,
            destination: bool = False,
            lea: bool = False,
    ) -> tuple[str, _ExprRenderState]:
        render_expr, def_size = self._prepare_expression_for_render(
            expr,
            def_size,
            destination=destination,
            lea=lea,
        )
        # Render expression with explicit rendering context instead of mutating shared fields.
        ir2cpp = IR2Cpp(
            self._context,
            lea=lea,
            indirection=render_expr.indirection,
            is_jump=self.itisjump,
            is_call=self.itiscall,
            assignments=self._assignments,
        )
        ir2cpp._namespace = self._namespace
        result = "".join(ir2cpp.visit(render_expr))
        rendered = result[1:-1] if self.check_parentesis(result) else result
        return rendered, ir2cpp._expr_state

    @staticmethod
    def _parenthesize_compound(rendered: str) -> str:
        """Wrap a rendered expression in parens when it has a top-level binary op.

        Equate/assignment values are substituted inline into enclosing
        expressions; ``A - (B - C)`` must not flatten into ``A - B - C``.
        """
        depth = 0
        for ch in rendered:
            if ch in "([":
                depth += 1
            elif ch in ")]":
                depth -= 1
            elif depth == 0 and ch in "+-*/%<>&|^":
                return f"({rendered})"
        return rendered

    def check_parentesis(self, string: str) -> bool:
        """Check if first ( matches the last one.

        >>> self.check_parentesis('(())')
        True
        >>> self.check_parentesis('()()')
        False
        """
        if not string or string[0] != "(" or string[-1] != ")":
            return False
        res = 0
        for c in string[1:-1]:
            if c == "(":
                res += 1
            elif c == ")":
                res -= 1
            if res < 0:
                return False
        return True

    def _jump(self, cmd: str, label_expr: Expression) -> str:
        if self.isrelativejump(label_expr):
            return "{;}"

        label, _ = self.jump_post(label_expr)
        condition = {
            "JZ": "GET_ZF()",
            "JE": "GET_ZF()",
            "JNZ": "!GET_ZF()",
            "JNE": "!GET_ZF()",
            "JBE": "GET_CF() || GET_ZF()",
            "JNA": "GET_CF() || GET_ZF()",
            "JA": "!GET_CF() && !GET_ZF()",
            "JNBE": "!GET_CF() && !GET_ZF()",
            "JC": "GET_CF()",
            "JB": "GET_CF()",
            "JNAE": "GET_CF()",
            "JNC": "!GET_CF()",
            "JNB": "!GET_CF()",
            "JAE": "!GET_CF()",
            "JP": "GET_PF()",
            "JPE": "GET_PF()",
            "JNP": "!GET_PF()",
            "JPO": "!GET_PF()",
        }.get(cmd.upper())
        if condition and (dispatch := self._conditional_cross_proc_dispatch(label, condition)):
            return dispatch
        assert self._context.args
        if self._context.args.get("mergeprocs") in {"persegment", "separate", "single"} and cmd.upper() == "JMP":
            if label in {"__dispatch_call", "__dispatch_call_ext"}:
                return f"return {label}(__disp, _state);"
            if g := self._context.symbols.get_global(label):
                target_proc_name = None
                if isinstance(g, op.label) and g.name in self.label_to_proc:
                    target_proc_name = self.label_to_proc[g.name]
                elif isinstance(g, Proc):
                    target_proc_name = g.name
                proc = getattr(self, "proc", None)
                current_proc = proc if isinstance(proc, str) else getattr(proc, "name", "")
                if target_proc_name and current_proc != target_proc_name:
                    if g.name == target_proc_name:
                        return f"return {self.mangle_label(g.name)}(0, _state);"
                    return f"return {self.mangle_label(target_proc_name)}(m2c::k{label}, _state);"

        if label == "main":
            label = self.mangle_label(label)
        return f"{cmd.upper()}({label})"

    def _instruction2(self, cmd: str, dst: Expression, src: Expression) -> str:
        a, b = self.parse2(dst, src)
        return f"{cmd.upper()}({a}, {b})"

    def _instruction3(self, cmd: str, dst: Expression, src: Expression, c: Expression) -> str:
        a, b = self.parse2(dst, src)
        c_rendered = self.render_instruction_argument(c)
        return f"{cmd.upper()}({a}, {b}, {c_rendered})"

    def _instruction4(self, cmd: str, a0: Expression, a1: Expression, a2: Expression, a3: Expression) -> str:
        a0_rendered = self.render_instruction_argument(a0)
        a1_rendered = self.render_instruction_argument(a1)
        a2_rendered = self.render_instruction_argument(a2)
        a3_rendered = self.render_instruction_argument(a3)
        return f"{cmd.upper()}({a0_rendered}, {a1_rendered}, {a2_rendered}, {a3_rendered})"

    def return_empty(self, _):
        return []

    def _assignment(self, stmt):
        dst, src = stmt
        if not isinstance(src, Expression):
            src = Asm2IR(self._context, "").transform(src)
        self._assignments[dst] = self._clone_expression_for_render(src)
        return ""

    def _equ(self, dst: str):
        assert isinstance(dst, str)
        symbol = self._context.symbols.get_global(dst)
        assert isinstance(symbol, op._equ)
        self._cmdlabel += self.render_equate_definition(dst, symbol)
        return ""

    def _equ_struct_size_name(self, src: Expression) -> str:
        if not isinstance(src, Expression) or len(src.children) != 1:
            return ""
        child = src.children[0]
        if not isinstance(child, lark.Token) or child.type != LABEL:
            return ""
        name = str(child)
        symbol = self._context.symbols.get_global(name)
        if isinstance(symbol, op.Struct):
            return symbol.name
        return ""

    def _runtime_linear_for_data(self, data: Data) -> int | None:
        linear = getattr(data, "runtime_linear_addr", None)
        if isinstance(linear, int):
            return linear
        real_seg, real_offset = data.getrealaddr()
        if real_seg is not None and real_offset is not None:
            return real_seg * 0x10 + real_offset
        return None

    @staticmethod
    def _runtime_data_element_size(data: Data, elements: int) -> int:
        if elements > 0:
            return max(1, data.getsize() // elements)
        return data.getsize()

    def _runtime_symbol_linear(self, symbol: Any) -> int | None:
        if isinstance(symbol, op.var):
            if symbol.external:
                return None
            segment = self._context.segments.get(symbol.segment)
            if segment is None:
                return None
            return segment.offset + symbol.offset
        if isinstance(symbol, (op.label, Proc)):
            real_seg = getattr(symbol, "real_seg", None)
            real_offset = getattr(symbol, "real_offset", None)
            if real_seg is not None and real_offset is not None:
                return real_seg * 0x10 + real_offset
        return None

    @staticmethod
    def _runtime_var_size(symbol: Any) -> int:
        if not isinstance(symbol, op.var):
            return 0
        element_size = int(getattr(symbol, "size", 0) or 0)
        elements = int(getattr(symbol, "elements", 1) or 1)
        if element_size <= 0:
            return 0
        return element_size * max(1, elements)

    def _runtime_symbol_tables(self) -> tuple[dict[int, tuple[str, Any]], list[tuple[int, int, str, Any]]]:
        if self._rt_symbol_exact_by_linear is not None and self._rt_var_ranges_by_linear is not None:
            return self._rt_symbol_exact_by_linear, self._rt_var_ranges_by_linear

        exact: dict[int, tuple[str, Any]] = {}
        ranges: list[tuple[int, int, str, Any]] = []
        for name, symbol in self._context.symbols.get_globals().items():
            linear = self._runtime_symbol_linear(symbol)
            if linear is None:
                continue
            if isinstance(symbol, op.var):
                exact[linear] = (name, symbol)
                total_size = self._runtime_var_size(symbol)
                if total_size > 0:
                    ranges.append((linear, linear + total_size, name, symbol))
            else:
                exact.setdefault(linear, (name, symbol))

        ranges.sort(key=lambda item: (item[1] - item[0], item[0]))
        self._rt_symbol_exact_by_linear = exact
        self._rt_var_ranges_by_linear = ranges
        return exact, ranges

    def _runtime_symbol_for_linear(self, linear: int) -> tuple[str, Any, int] | None:
        exact, ranges = self._runtime_symbol_tables()
        if linear in exact:
            name, symbol = exact[linear]
            return name, symbol, 0
        for start, end, name, symbol in ranges:
            if start < linear < end:
                return name, symbol, linear - start
        return None

    @staticmethod
    def _runtime_add_delta(expr: str, delta: int) -> str:
        if delta == 0:
            return expr
        return f"({expr} + 0x{delta:x})"

    def _runtime_symbol_reference(self, target_linear: int, value_size: int, flags: int) -> str | None:
        match = self._runtime_symbol_for_linear(target_linear)
        if match is None:
            return None
        _name, symbol, delta = match
        if isinstance(symbol, op.var):
            if flags & RT_FAR_POINTER or value_size >= 4:
                expr = f"far_offset({symbol.segment},{symbol.name})"
            elif value_size == 2:
                expr = f"offset({symbol.segment},{symbol.name})"
            else:
                return None
            return self._runtime_add_delta(expr, delta)
        if isinstance(symbol, (op.label, Proc)):
            expr = f"m2c::k{symbol.name.lower()}"
            if value_size <= 2:
                expr = f"({expr} & 0xffff)"
            return self._runtime_add_delta(expr, delta)
        return None

    @staticmethod
    def _runtime_value_matches(observed_value: int | None, source_value: int, value_size: int) -> bool:
        if observed_value is None:
            return True
        if value_size <= 0 or value_size >= 8:
            return observed_value == source_value
        mask = (1 << (value_size * 8)) - 1
        return (observed_value & mask) == (source_value & mask)

    def _runtime_pointer_expression_for_value(
            self,
            source_linear: int | None,
            source_value: Any,
            element_size: int,
    ) -> str | None:
        if source_linear is None or not isinstance(source_value, int):
            return None
        entries = getattr(self._context, "runtime_pointer_meta", {}).get(source_linear, [])
        if not entries:
            return None
        for entry in sorted(entries, key=lambda item: _parse_runtime_int(item.get("Count")) or 0, reverse=True):
            if not isinstance(entry, dict):
                continue
            value_size = _parse_runtime_int(entry.get("Size")) or element_size
            if value_size != element_size:
                continue
            observed_value = _parse_runtime_int(entry.get("Value"))
            if not self._runtime_value_matches(observed_value, source_value, value_size):
                continue
            target = _parse_runtime_int(entry.get("TargetAddr"))
            if target is None:
                continue
            flags = _parse_runtime_int(entry.get("Flags")) or 0
            expr = self._runtime_symbol_reference(target, value_size, flags)
            if expr is not None:
                return expr
        return None

    def produce_c_data_single_(self, data: Data) -> tuple[str, str, int]:
        """It takes an assembler data and returns a C++ object.

        :param data: The data to be converted
        :return: data value, declaration, size
        """
        # Real conversion
        internal_data_type = data.getinttype()
        state = self._expr_state
        prev_size = state.element_size
        prev_data_label_size = state.data_label_size
        binary_width = self._context.typetosize(data.data_type)
        state.element_size = data.getsize()
        state.data_label_size = binary_width
        try:
            logging.debug("current data type = %s", internal_data_type)
            rc, rh = self.__type_table[internal_data_type](data)
        finally:
            state.element_size = prev_size
            state.data_label_size = prev_data_label_size

        logging.debug(rc)
        logging.debug(rh)
        return rc, rh, data.getsize()

    def produce_c_data_number(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, size = data.getdata()
        r = self._flatten_data_values(r)
        source_linear = self._runtime_linear_for_data(data)
        element_size = self._runtime_data_element_size(data, elements)
        if len(r) == 1 and isinstance(r[0], int):
            rc = self._runtime_pointer_expression_for_value(source_linear, r[0], element_size) or str(r[0])
        elif len(r) == 1 and data_ctype in {"db", "char"} and isinstance(r[0], str) and len(r[0]) == 1:
            rc = self.convert_char(r[0])
        else:
            rc = "".join(str(i) if isinstance(i, int) else self._render_data_value_part(i, data_ctype) for i in r)
        rc = self._mask_arithmetic_data_element(self._replace_current_location_symbol(rc, data), data_ctype)
        rh = f"{data_ctype} {label}"
        return rc, rh

    @staticmethod
    def _replace_current_location_symbol(value: str, data: op.Data, element_index: int = 0, element_size: int = 0) -> str:
        if "$" not in value:
            return value
        current_offset = data.offset + element_index * element_size
        return value.replace("$", str(current_offset))

    def produce_c_data_array(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, _ = data.getdata()
        r = self._flatten_data_values(r)
        source_linear = self._runtime_linear_for_data(data)
        element_size = self._runtime_data_element_size(data, elements)
        if self._is_listing_source() and data_ctype == "char" and elements == 1:
            value = r[0] if r else 0
            if isinstance(value, lark.Tree):
                rc = "".join(self.visit(value))
            elif isinstance(value, op.Data):
                rc = self.produce_c_data_single_(value)[0]
            else:
                rc = self._runtime_pointer_expression_for_value(source_linear, value, element_size) or self.convert_char(value)
            rc = self._replace_current_location_symbol(rc, data)
            rh = f"{data_ctype} {label}"
            return rc, rh
        if not any(r):  # all zeros
            r = [0]
        if elements == 1:
            single = r[0]
            if isinstance(single, op.Data):
                rc = self.produce_c_data_single_(single)[0]
            elif isinstance(single, lark.Tree):
                rc = "".join(self.visit(single))
            elif isinstance(single, list):
                rc = self._render_data_value_part(single, data_ctype)
            else:
                rc = self._runtime_pointer_expression_for_value(source_linear, single, element_size) or str(single)
            rc = self._mask_arithmetic_data_element(self._replace_current_location_symbol(rc, data), data_ctype)
            rh = f"{data_ctype} {label}"
            return rc, rh
        rc = "{"
        for i, v in enumerate(r):
            if i != 0:
                rc += ","
            if isinstance(v, op.Data):
                c = self.produce_c_data_single_(v)[0]
                rc += c
            elif isinstance(v, lark.Tree):
                element_value = self._mask_arithmetic_data_element("".join(self.visit(v)), data_ctype)
                rc += self._replace_current_location_symbol(element_value, data, i, element_size)
            elif isinstance(v, list):
                element_value = self._mask_arithmetic_data_element(
                    self._render_data_value_part(v, data_ctype), data_ctype)
                rc += self._replace_current_location_symbol(element_value, data, i, element_size)
            else:
                element_linear = None if source_linear is None else source_linear + i * element_size
                element_value = (
                    self._runtime_pointer_expression_for_value(element_linear, v, element_size)
                    or (self.convert_char(v) if isinstance(v, str) or data_ctype == "char" else self._render_int_for_ctype(v, data_ctype))
                )
                element_value = self._mask_arithmetic_data_element(element_value, data_ctype)
                rc += self._replace_current_location_symbol(element_value, data, i, element_size)
        rc += "}"
        rh = f"{data_ctype} {label}[{elements}]"
        return rc, rh

    def _render_data_value_part(self, value: Any, data_ctype: str, *, convert_strings: bool = True) -> str:
        if isinstance(value, list):
            word_operator, operand_parts = self._split_list_word_operator(value)
            if word_operator:
                operator = word_operator
                rendered_value = "".join(
                    self._render_data_value_part(part, data_ctype, convert_strings=True)
                    for part in operand_parts
                )
                if operator == "low":
                    return f"({rendered_value} & 0xff)"
                if operator == "high":
                    return f"(({rendered_value} >> 8) & 0xff)"
                if operator == "lowword":
                    return f"({rendered_value} & 0xffff)"
                return f"(({rendered_value} >> 16) & 0xffff)"
            return "".join(
                self._render_data_value_part(part, data_ctype, convert_strings=False)
                for part in value
            )
        if isinstance(value, (lark.Tree, lark.Token)):
            return "".join(str(part) for part in self.visit(value))
        if convert_strings and (isinstance(value, str) or data_ctype == "char"):
            return self.convert_char(value)
        if isinstance(value, int):
            return self._render_int_for_ctype(value, data_ctype)
        return str(value)

    _CTYPE_RANGES = {
        "db": (0, 0xFF), "byte": (0, 0xFF), "char": (-0x80, 0x7F), "sbyte": (-0x80, 0x7F),
        "dw": (0, 0xFFFF), "word": (0, 0xFFFF), "sword": (-0x8000, 0x7FFF),
        "dd": (0, 0xFFFFFFFF), "dword": (0, 0xFFFFFFFF), "sdword": (-0x80000000, 0x7FFFFFFF),
        "dq": (0, 0xFFFFFFFFFFFFFFFF), "qword": (0, 0xFFFFFFFFFFFFFFFF),
    }

    @classmethod
    def _mask_arithmetic_data_element(cls, rendered: str, data_ctype: str) -> str:
        """Wrap a purely-arithmetic element render in a C cast when its constant
        value overflows the target type, so it truncates like MASM instead of
        tripping C++11 narrowing."""
        c_type = {
            "byte": "db", "char": "db", "sbyte": "db",
            "word": "dw", "sword": "dw", "near": "dw", "near16": "dw",
            "dword": "dd", "sdword": "dd", "far": "dd", "far16": "dd", "far32": "dd",
            "qword": "dq",
        }.get(data_ctype, data_ctype)
        if c_type not in {"db", "dw", "dd", "dq"}:
            return rendered
        if not re.fullmatch(r"[0-9a-fA-FxXhHdDoObB()+\-*/%&|^~<>\s]+", rendered) or not re.search(
            r"[()+\-*/%&|^~<>]", rendered
        ):
            return rendered
        bounds = cls._CTYPE_RANGES.get(data_ctype, cls._CTYPE_RANGES.get(c_type))
        try:
            value = eval(rendered, {"__builtins__": {}}, {})  # noqa: S307 - arithmetic-only charset above
        except Exception:
            value = None
        if bounds is not None and isinstance(value, (int, float)) and bounds[0] <= int(value) <= bounds[1]:
            return rendered
        return f"{c_type}({rendered})"

    @staticmethod
    def _render_int_for_ctype(value: int, data_ctype: str) -> str:
        if not isinstance(value, int):
            return str(value)
        ranges = {
            "db": (0, 0xFF), "byte": (0, 0xFF), "char": (-0x80, 0x7F), "sbyte": (-0x80, 0x7F),
            "dw": (0, 0xFFFF), "word": (0, 0xFFFF), "sword": (-0x8000, 0x7FFF),
            "dd": (0, 0xFFFFFFFF), "dword": (0, 0xFFFFFFFF), "sdword": (-0x80000000, 0x7FFFFFFF),
            "dq": (0, 0xFFFFFFFFFFFFFFFF), "qword": (0, 0xFFFFFFFFFFFFFFFF),
        }
        bounds = ranges.get(data_ctype)
        if bounds is not None and not (bounds[0] <= value <= bounds[1]):
            return f"{data_ctype}({value})"
        return str(value)

    @staticmethod
    def _split_list_word_operator(value: list[Any]) -> tuple[str, list[Any]]:
        operators = {"low", "high", "lowword", "highword"}
        if value and str(value[0]).lower() in operators:
            return str(value[0]).lower(), value[1:]

        prefix = ""
        idx = 0
        while idx < len(value) and isinstance(value[idx], str) and len(value[idx]) == 1 and value[idx].isalpha():
            prefix += value[idx]
            idx += 1
            lower = prefix.lower()
            if lower in operators:
                return lower, value[idx:]
            if not any(op.startswith(lower) for op in operators):
                break
        return "", value

    def produce_c_data_zero_string(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, size = data.getdata()
        r = flatten(r)
        size = max(size, len(r))
        if self._is_listing_source() and size == 1:
            rc = self.convert_char(r[0] if r else 0)
            rh = f"char {label}"
            return rc, rh
        rc = '"' + "".join(self.convert_str(i) for i in r[:-1]) + '"'
        rc = re.sub(r"(\\x[0-9a-f][0-9a-f])([0-9a-fA-F])", r'\g<1>" "\g<2>', rc)  # fix for stupid C hex escapes: \xaef
        rh = f"char {label}[{size}]"
        return rc, rh

    def produce_c_data_array_string(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, size = data.getdata()
        r = flatten(r)
        size = max(size, len(r))
        if self._is_listing_source() and size == 1:
            rc = self.convert_char(r[0] if r else 0)
            rh = f"char {label}"
            return rc, rh
        rc = "{" + ",".join([self.convert_char(i) for i in r]) + "}"
        rh = f"char {label}[{size}]"
        return rc, rh

    def produce_c_data_object(self, data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = []
        for i in data.getmembers():
            c, _, _ = self.produce_c_data_single_(i)
            if c == "":
                c = "0"
            rc += [c]
        rc_str = "{" + ",".join(rc) + "}"
        rh = f"{self._cpp_data_type(data_ctype)} {label}"
        return rc_str, rh

    def _cpp_data_type(self, data_ctype: str) -> str:
        if data_ctype in CPP_STRUCT_TAG_REQUIRED or (
            data_ctype in getattr(self._context, "structures", {}) and self._data_label_exists(data_ctype)
        ):
            return f"struct {data_ctype}"
        return data_ctype

    def convert_char(self, c: Union[int, str]) -> str:
        if isinstance(c, int):
            if c in [10, 13]:
                return f"'{self.convert_str(c)}'"
            if c < -128 or c > 127:
                return f"'\\x{c & 0xff:02x}'"
            return str(c)
        if not isinstance(c, str):
            return "0"
        if isinstance(c, str) and c in {"", "''", '""'}:
            return "0"
        if isinstance(c, str) and len(c) != 1:
            return c
        return f"'{self.convert_str(c)}'"

    def convert_str(self, c: Union[int, str]) -> str:
        vvv = ""
        if isinstance(c, int):
            if c == 13:
                vvv = r"\r"
            elif c == 10:
                vvv = r"\n"
            elif c == 0:
                vvv = r"\0"
            elif c < 32:
                vvv = f"\\x{c:02x}"
            else:
                vvv = chr(c)
        elif isinstance(c, str):
            # logging.debug "~~ " + r[i] + str(ord(r[i]))
            # for c in string:
            if len(c) != 1:
                return "".join(self.convert_str(char) for char in c)

            if c in ["'", '"', "\\"]:
                vvv = "\\" + c
            elif ord(c) > 127:
                vvv = f"\\x{c.encode('cp437', 'backslashreplace')[0]:02x}"
            elif c == "\0":
                vvv = "\\0"
            else:
                vvv = c
        return vvv

    def produce_global_jump_table(self, globals, itislst):
        # Produce call table
        if itislst:
            result = """
  static bool __dispatch_call(m2c::_offsets __i, struct m2c::_STATE* _state){
  X86_REGREF
     __disp=__i;
     switch (__i) {
"""
        else:
            result = """
  static bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state){
     switch (__disp) {
"""
        entries = OrderedDict()
        extern_entries = set()
        direct_extern_refs = getattr(self._context, "extern_code_refs", set())
        for k, v in globals:
            if isinstance(v, Proc) and v.used:
                if v.extern and k not in direct_extern_refs:
                    continue
                k = re.sub(r"[^A-Za-z0-9_]", "_", k)  # need to do it during mangling
                entries[k] = (self.mangle_label(k), "0")
                if v.extern:
                    extern_entries.add(k)
                labels = v.provided_labels

                entries.update({label: (v.name, "__disp") for label in set(labels) if label != v.name})
            elif isinstance(v, op.label) and v.used:
                # Add all used labels, not just those provided by procedures
                k = re.sub(r"[^A-Za-z0-9_]", "_", k)  # need to do it during mangling
                if k not in entries:  # Only add if not already added
                    # Find which procedure this label belongs to
                    proc_name = self.label_to_proc.get(k, k)
                    entries[k] = (proc_name, "__disp")

        # Ensure labels discovered during grouping/merging are globally dispatchable.
        # Some labels may not exist as standalone globals after merge, but are still
        # reachable by indirect jumps/calls through register/memory targets.
        for label_name, proc_name in self.label_to_proc.items():
            sanitized_label = re.sub(r"[^A-Za-z0-9_]", "_", label_name)
            if sanitized_label not in entries:
                entries[sanitized_label] = (proc_name, "__disp")

        # for name in procs:
        #    if not name.startswith('_group'):  # TODO remove dirty hack. properly check for group

        names = self.leave_unique_labels(entries.keys())
        # Multiple labels may share the same cs:ip (e.g. an IDA 'segNNN_YYY_proc'
        # alias for a proc entry). Emit only one case per offset value.
        label_offsets = self.export_defined_code_symbol_offsets()
        emitted_offsets: set[int] = set()
        for name in sorted(names):
            off = label_offsets.get(name)
            if off is not None:
                if off in emitted_offsets:
                    continue
                emitted_offsets.add(off)
            line = "        case m2c::k{}: \tif (!{}({}, _state)) return false; break;\n".format(
                name, *entries[name]
            )
            if name in extern_entries:
                line = f"#ifndef {self.code_equate_guard_name(name)}\n{line}#endif\n"
            result += line

        result += "        default: { bool handled = false; if (!m2c::dispatch_external_code(__disp, _state, &handled)) return false; if (handled) break; m2c::log_error(\"Don't know how to call to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(_state); abort(); }\n"
        result += "     };\n     return true;\n}\n"
        result += """
  static bool __dispatch_call_ext(m2c::_offsets __disp, struct m2c::_STATE* _state){
     // Indirect call/jump targets hold aggregate (linked) code offsets
     // (OFFSET emits m2c::kglobal_* and code tables store the same space),
     // so resolve them through the aggregate dispatcher before falling back
     // to this module's local offset switch.
     bool handled = false;
     bool ok = m2c::dispatch_external_code(__disp, _state, &handled);
     if (handled) return ok;
     return __dispatch_call(__disp, _state);
}
"""
        return result

    def _mov(self, dst: Expression, src: Expression) -> str:
        a, b = self.parse2(dst, src)
        if "m2c::near_offset_data(" in b:
            self._pending_data_offset_ds_restore = True
        mapped_memory_access = "raddr" in a or "raddr" in b
        if a in {"ds", "es", "ss"}:
            return f"m2c::set_segment_register({a}, {b});"
        if mapped_memory_access:
            return f"MOV({a}, {b})"
        return f"{a} = {b};"

    def produce_jump_table(self, offsets):
        """It takes a list of labels and produces a C++ switch statement that jumps to the corresponding label.

        :param offsets: a list of labels that we want to jump to
        :return: The result of the function.
        """
        # Produce jump table
        result = """
            assert(0);
            __dispatch_call_ext:
            { bool handled = false;
              bool ok = m2c::dispatch_external_code(__disp, _state, &handled);
              if (handled) return ok; }
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            switch (__disp) {
        """
        label_offsets = self.export_defined_code_symbol_offsets()
        emitted_offsets: set[int] = set()
        for name, label in offsets:
            logging.debug("%s, %s", name, label)
            off = label_offsets.get(name)
            if off is not None:
                if off in emitted_offsets:
                    continue
                emitted_offsets.add(off)
            result += f"        case m2c::k{name}: \tgoto {label};\n"
        if self.proc and self.proc.name in set(self.groups.values()):
            result += "        default: return __dispatch_call(__disp, _state);\n"
        else:
            result += "        default: { bool handled = false; if (!m2c::dispatch_external_code(__disp, _state, &handled)) return false; if (handled) break; m2c::log_error(\"Don't know how to jump to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(_state); abort(); }\n"
        result += "    };\n}\n"
        return result

    def mangle_label(self, name: str) -> str:
        name = mangle_asm_labels(name)
        return name.lower()

    def produce_number(self, expr: str, radix: int, sign: str, value: str) -> str:
        if radix == 10:
            return f"{sign}{value}"
        elif radix == 16:
            return f"{sign}0x{value}"
        elif radix == 2:
            return f"{sign}{hex(int(str(value), 2))}"
        elif radix == 8:
            return f"{sign}0{value}"
        else:
            return str(int(expr, radix))



    def INTEGER(self, t: Token) -> list[str]:
        assert t.start_pos and t.line is not None and t.value is not None
        radix, sign_int, value = t.start_pos, t.line, t.value
        sign = "" if sign_int == 1 else "-"
        return [self.produce_number("", radix, sign, value)]

    def STRING(self, token: Token) -> list[str]:
        result = token.value
        if len(token.value) == 4:  # m:
            ex = token
            result = "0x"
            for i in range(4):
                ss = hex(ord(ex[i]))
                result += ss[2:]
        else:
            result = result.replace("\\", "\\\\")  # escape c \ symbol
            result = f"'{result}'"
        return [result]


    def expr(self, tree: Expression) -> str:
        state = self._expr_state
        prev_data_label_size = state.data_label_size
        state.reset()
        state.data_label_size = prev_data_label_size
        previous_indirection = state.indirection
        state.indirection = self._effective_indirection_for_expr(tree)
        prev_work_segment = state.work_segment
        if tree.segment_register:
            state.work_segment = tree.segment_register
        prev_element_size = state.element_size
        state.element_size = tree.element_size
        try:
            self._initialize_expr_shape_flags(tree)
            result = "".join(self.visit(tree.children))
            return self._finalize_rendered_expr(tree, result)
        finally:
            state.indirection = previous_indirection
            state.element_size = prev_element_size
            state.work_segment = prev_work_segment

    def _effective_indirection_for_expr(self, tree: Expression) -> IndirectionType:
        effective_indirection = tree.indirection
        if self.itiscall and tree.mods & {"near", "far"}:
            return IndirectionType.VALUE
        return effective_indirection

    def _initialize_expr_shape_flags(self, tree: Expression) -> None:
        state = self._expr_state
        origexpr = tree.children[0]
        while isinstance(origexpr, list) and origexpr:
            origexpr = origexpr[0]
        single = len(tree.children) == 1
        state.is_just_label = self._check_for_just_label(origexpr, single)
        state.is_just_member = single and isinstance(origexpr, lark.Tree) and origexpr.data == MEMBERDIR

    def _effective_ptr_size_for_expr(self, tree: Expression) -> int:
        state = self._expr_state
        effective_ptr_size = tree.ptr_size
        if state.indirection == IndirectionType.POINTER and effective_ptr_size == 0 and state.variable_size:
            return state.variable_size
        return effective_ptr_size

    def _finalize_rendered_expr(self, tree: Expression, result: str) -> str:
        state = self._expr_state
        state.size_changed = state.size_changed or "size_changed" in tree.mods and self._middle_size != tree.size()
        effective_ptr_size = self._effective_ptr_size_for_expr(tree)

        if state.indirection == IndirectionType.POINTER and tree.registers.intersection({"bp", "ebp", "sp", "esp"}):
            state.work_segment = "ss"

        if state.need_pointer_to_member:
            result = result[:-1] if result[-1] == "+" else result
            result = result.replace("++", "+").replace("+-", "-")
            result = f"{result}+{state.need_pointer_to_member[0]}))->{'.'.join(state.need_pointer_to_member[1:])}"

        if state.indirection == IndirectionType.POINTER and not state.is_member and (
            not state.is_just_label or state.size_changed
        ) and ("lea" not in tree.mods or "destination" in tree.mods):
            result = self.convert_sqbr_reference(tree.segment_register, result, effective_ptr_size)
        if state.is_member:
            member_segment = tree.segment_register or state.work_segment
            result = f"(({state.struct_type}*)raddr({member_segment},{result}"
        if state.needs_dereference:
            state.needs_dereference = False
            result = f"*{result}" if result[0] == "(" and result[-1] == ")" else f"*({result})"
        return result

    def _check_for_just_label(self, origexpr, single: bool):
        return single and ((isinstance(origexpr, lark.Token) and origexpr.type == LABEL)
                           or (isinstance(origexpr, lark.Tree) and origexpr.data == SQEXPR
                               and isinstance(origexpr.children, lark.Token) and origexpr.children.type == LABEL)
                           or (isinstance(origexpr, lark.Tree) and origexpr.data == MEMBERDIR))

    def data(self, data: Data) -> tuple[str, str, int]:
        binary_width = self._context.typetosize(data.data_type)  # TODO pervertion
        prev_data_label_size = self._expr_state.data_label_size
        self._expr_state.data_label_size = binary_width
        # For unit test
        from masm2c.parser import Parser
        Parser.c_dummy_label[0] = 0
        try:
            c, h, size = self.produce_c_data_single_(data)
            c += f", // {data.getlabel()}" + "\n"
            h += ";\n"
        finally:
            self._expr_state.data_label_size = prev_data_label_size
        return c, h, size

    def LABEL(self, token: Token) -> list[Union[str, Token]]:
        if self._expr_state.data_label_size:
            size = self._expr_state.data_label_size
            return [self.convert_label_data(token, size=size)]
        return [self.convert_label_(token)]

    def convert_label_data(self, v: Token, size: int=0) -> Union[Token, str]:
        logging.debug("convert_label_data(%s)", v)
        size = 2 if size <= 0 else size
        if (g := self._context.symbols.get_global(v)) is None:
            return v
        if isinstance(g, op.var):
            if g.external and self._is_cross_module_code_export(str(v)):
                result = f"m2c::{self.global_code_offset_constant(str(v))}"
            elif g.issegment:
                result = f"seg_offset({g.name})"
            elif size == 2:
                result = f"offset({g.segment},{g.name})"
            elif size == 4:
                result = f"far_offset({g.segment},{g.name})"
            else:
                logging.error(f"Some unknown data size {size} for {g.name}")
                result = g.original_name
        elif isinstance(g, (op._equ, op._assignment)):
            result = g.original_name
        elif isinstance(g, (op.label, Proc)):
            name = self.sanitize_label_name(str(v))
            if self._is_cross_module_code_export(name) or name in self._data_referenced_code_symbol_names():
                result = f"m2c::{self.global_code_offset_constant(str(v))}"
            else:
                result = f"m2c::k{g.name.lower()}"
        elif not isinstance(g, op.Struct):
            result = g.offset
        logging.debug(result)
        return result

    def offsetdir(self, tree: Tree) -> list[Union[str, Token]]:  # TODO equ, assign support
        name = tree.children[0]

        if isinstance(name, lark.Tree) and name.data=="memberdir":
            label = name.children
            assert isinstance(label, list) and all(isinstance(lab, str) for lab in label)
            if (g := self._context.symbols.get_global(label[0])) is None:
                return label

            value_str = self.convert_member_offset(g, label)
            return [lark.Token("memberdir", value_str)]

        if isinstance(name, lark.Token) and name.type == "INTEGER":
            return ["".join(str(part) for part in self.visit(name))]
        if isinstance(name, list):
            return ["".join(str(part) for part in self.visit(name))]
        if isinstance(name, lark.Tree):
            previous_indirection = self._expr_state.indirection
            self._expr_state.indirection = IndirectionType.OFFSET
            try:
                return ["".join(str(part) for part in self.visit(name))]
            finally:
                self._expr_state.indirection = previous_indirection

        assert isinstance(name, str)
        if (g := self._context.symbols.get_global(name)) is None:
            if len(name) == 1:
                return [self.convert_char(name)]
            if self._is_cross_module_code_export(name):
                return [f"m2c::{self.global_code_offset_constant(name)}"]
            if self._is_continuation_module():
                if self._is_mangled_internal_code_label(name):
                    return [f"m2c::k{self.sanitize_label_name(name)}"]
                return [f"m2c::near_offset_external({self.sanitize_label_name(name)})"]
            return [name]
        if isinstance(g, op.var):
            logging.debug("it is var %s", g.size)
            if g.external and self._is_cross_module_code_export(name):
                return [f"m2c::{self.global_code_offset_constant(name)}"]
            offset_size = self._expr_state.element_size
            if offset_size not in {2, 4}:
                offset_size = 2
            if offset_size == 2:
                if g.external and not self._expr_state.data_label_size:
                    return [f"m2c::near_offset_external({g.name})"]
                return [self._near_data_offset_expr(g, g.name)]
            if g.external and not self._expr_state.data_label_size:
                return [f"m2c::far_offset_external({g.name})"]
            return [self._far_data_offset_expr(g, g.name)]
        elif isinstance(g, (Proc, op.label)):
            logging.debug("it is proc")
            if self._should_render_global_code_offset(name, g):
                return [f"m2c::{self.global_code_offset_constant(name)}"]
            return [f"m2c::k{g.name}"]
        elif isinstance(g, (op._equ, op._assignment)) and isinstance(g.value, Expression):
            if (symbolic_offset := self._render_single_base_offset_expression(g.value)) is not None:
                return [symbolic_offset]
            if (folded := self._fold_location_counter_expression(g)) is not None:
                return [folded]
            return [self._parenthesize_compound("".join(str(part) for part in self.visit(g.value)))]
        elif isinstance(g, (op._equ, op._assignment)):
            return [g.original_name]
        else:
            raise ValueError("Unknown type for offsetdir %s", type(g))

    def seg(self, tree: Tree) -> list[str]:
        name = tree.children[0]
        if isinstance(name, lark.Tree):
            rendered = "".join(str(part) for part in self.visit(name))
            return [f"seg_offset({rendered})"]
        label = str(name)
        symbol = self._context.symbols.get_and_mark_global(label)
        if isinstance(symbol, op.var):
            if symbol.external:
                return [f"m2c::segment_of_external({symbol.name})"]
            if self._should_emit_linked_data_offset(symbol):
                return [f"m2c::segment_of_external({symbol.name})"]
            return [f"seg_offset({symbol.segment or symbol.name})"]
        if isinstance(symbol, Proc):
            return [f"seg_offset({symbol.segment or label})"]
        if isinstance(symbol, op.label) and symbol.proc:
            if getattr(symbol, "segment", ""):
                return [f"seg_offset({symbol.segment})"]
            proc = self._context.symbols.get_global(symbol.proc)
            if isinstance(proc, Proc):
                return [f"seg_offset({proc.segment or label})"]
        return [f"seg_offset({label})"]

    # Approximate C++ precedence of rendered operator nodes (higher binds tighter).
    _EXPR_NODE_PRECEDENCE = {
        "memberdir": 95, "sqexpr2": 95, "braces": 95,
        "unadddir": 80, "notdir": 80, "wordopdir": 80,
        "offsetdir": 80, "seg": 80, "ptrdir": 80, "segoverride": 80,
        "muldir": 70,
        "adddir": 60,
        "shiftdir": 55,
        "reldir": 40,
        "anddir": 30,
        "xordir": 25,
        "ordir": 20,
    }

    @classmethod
    def _expression_operand_precedence(cls, child: Any) -> int | None:
        """Return the C++ precedence of a rendered operand node, if it is an operator."""
        node = child
        while True:
            if isinstance(node, Expression) and len(node.children) == 1:
                node = node.children[0]
            elif isinstance(node, list) and len(node) == 1:
                node = node[0]
            else:
                break
        if isinstance(node, lark.Tree):
            return cls._EXPR_NODE_PRECEDENCE.get(node.data)
        return None

    _NONASSOCIATIVE_OPERATOR_TOKENS = frozenset({
        "-", "/", "%", "MOD", "SHL", "SHR", "<<", ">>",
        "<", ">", "<=", ">=", "==", "!=",
        "EQ", "NE", "LT", "LE", "GT", "GE",
    })

    def _render_operator_children(self, children: list[Any], parent_data: str = "") -> list[str]:
        parent_precedence = self._EXPR_NODE_PRECEDENCE.get(parent_data, 0)
        operator_token = ""
        if len(children) > 1:
            middle = children[1]
            operator_token = str(middle).strip().upper() if isinstance(middle, (lark.Token, str)) else ""
        nonassociative = operator_token in self._NONASSOCIATIVE_OPERATOR_TOKENS
        rendered = []
        for index, child in enumerate(children):
            if isinstance(child, lark.Token):
                rendered_child = "".join(str(part) for part in self.visit(child))
            elif isinstance(child, str):
                rendered_child = child
            else:
                rendered_child = "".join(str(part) for part in self.visit(child))
            if index != 1 and parent_precedence:
                # Keep substituted expressions grouped: `A - (B - C)` must not
                # flatten into `A - B - C`. Wrap when the operand binds looser
                # than the parent operator, or when it sits on the right side
                # of a non-associative operator of the same precedence.
                child_precedence = self._expression_operand_precedence(child)
                if child_precedence is not None and (
                    child_precedence < parent_precedence
                    or (index > 1 and nonassociative and child_precedence <= parent_precedence)
                ):
                    rendered_child = f"({rendered_child})"
            rendered.append(rendered_child)
        return rendered

    def dollar(self, _tree: Tree) -> list[str]:
        return ["$"]

    def adddir(self, tree: Tree) -> list[str]:
        if self._count_known_offset_labels(tree) >= 2 and (
            rendered := self._render_known_offset_expression(tree)
        ):
            return [rendered]
        if self._should_fold_inline_int_expression(tree) and (
            folded := self._eval_asm_int_expression(tree, None)
        ) is not None:
            return [str(folded)]
        left, operator, right = self._render_operator_children(tree.children, "adddir")
        return [f"{left}{operator}{right}"]

    def muldir(self, tree: Tree) -> list[str]:
        if self._count_known_offset_labels(tree) >= 2 and (
            rendered := self._render_known_offset_expression(tree)
        ):
            return [rendered]
        if self._should_fold_inline_int_expression(tree) and (
            folded := self._eval_asm_int_expression(tree, None)
        ) is not None:
            return [str(folded)]
        left, operator, right = self._render_operator_children(tree.children, "muldir")
        return [f"{left}{operator}{right}"]

    def _should_fold_inline_int_expression(self, node: Any) -> bool:
        """Return true for inline MASM expressions that are absolute constants."""
        return self._contains_location_counter(node)

    def _render_known_offset_expression(self, node: Any) -> str | None:
        """Render known MASM label arithmetic with explicit offset expressions."""
        if isinstance(node, Expression):
            if len(node.children) != 1:
                return None
            return self._render_known_offset_expression(node.children[0])
        if isinstance(node, list):
            if len(node) != 1:
                return None
            return self._render_known_offset_expression(node[0])
        if isinstance(node, Tree):
            if node.data == "braces":
                inner_children = [
                    child
                    for child in node.children
                    if not (isinstance(child, Token) and child.type in {"LPAR", "RPAR"})
                ]
                if len(inner_children) != 1:
                    return None
                inner = self._render_known_offset_expression(inner_children[0])
                return f"({inner})" if inner is not None else None
            if node.data in {"adddir", "muldir"} and len(node.children) == 3:
                left = self._render_known_offset_expression(node.children[0])
                right = self._render_known_offset_expression(node.children[2])
                if left is None or right is None:
                    return None
                return f"{left}{node.children[1]}{right}"
            if node.data == "unadddir" and len(node.children) == 2:
                value = self._render_known_offset_expression(node.children[1])
                return None if value is None else f"{node.children[0]}{value}"
            if len(node.children) == 1:
                return self._render_known_offset_expression(node.children[0])
            return None
        if isinstance(node, Token):
            if node.type == "INTEGER":
                int_value = self._eval_asm_int_expression(node, None)
                return None if int_value is None else str(int_value)
            if node.type in {"LABEL", "COMMON"}:
                return self._known_symbol_offset_expression(str(node))
            return None
        return None

    def _render_single_base_offset_expression(self, node: Any) -> str | None:
        """Render a single-label address expression without folding its base."""
        if self._count_known_offset_labels(node) != 1:
            return None
        return self._render_known_offset_expression(node)

    def _known_symbol_offset_expression(self, name: str) -> str | None:
        """Return the generated C++ offset expression for a known symbol."""
        symbol = self._context.symbols.get_global(name)
        if isinstance(symbol, op.var):
            if symbol.external:
                return f"m2c::near_offset_external({symbol.name})"
            return f"offset({symbol.segment},{symbol.name})"
        if isinstance(symbol, op.Data):
            segment = getattr(symbol, "segment", "") or self._namespace or "default_seg"
            label = getattr(symbol, "label", name)
            return f"offset({segment},{label})"
        if isinstance(symbol, (Proc, op.label)):
            if self._should_render_global_code_offset(name, symbol):
                return f"m2c::{self.global_code_offset_constant(name)}"
            return f"m2c::k{self.sanitize_label_name(name)}"
        return None

    def _should_render_global_code_offset(self, name: str, symbol: Proc | op.label) -> bool:
        """Return true when a code OFFSET may be consumed outside this module."""
        if not self._linked_data_offsets_enabled():
            return False
        if name in self._instruction_offset_referenced_code_symbol_names():
            return True
        if isinstance(symbol, Proc) and symbol.extern:
            return self._is_cross_module_code_export(name)
        return self._is_cross_module_code_export(name) or self._is_public_code_offset_export(name)

    @classmethod
    def _contains_asm_address_term(cls, node: Any) -> bool:
        """Return true when an expression contains MASM address-relative terms."""
        if isinstance(node, Tree):
            if node.data == "dollar":
                return True
            return any(cls._contains_asm_address_term(child) for child in node.children)
        if isinstance(node, list):
            return any(cls._contains_asm_address_term(child) for child in node)
        return isinstance(node, Token) and node.type == "LABEL"

    @classmethod
    def _contains_location_counter(cls, node: Any) -> bool:
        """Return true when an expression references MASM's current offset."""
        if isinstance(node, Tree):
            if node.data == "dollar":
                return True
            return any(cls._contains_location_counter(child) for child in node.children)
        if isinstance(node, list):
            return any(cls._contains_location_counter(child) for child in node)
        return False

    def _count_known_offset_labels(self, node: Any) -> int:
        """Count labels whose assembler offsets are known in the current context."""
        if isinstance(node, Tree):
            return sum(self._count_known_offset_labels(child) for child in node.children)
        if isinstance(node, list):
            return sum(self._count_known_offset_labels(child) for child in node)
        if isinstance(node, Token) and node.type in {"LABEL", "COMMON"}:
            return 1 if self._known_symbol_offset(str(node)) is not None else 0
        return 0

    def _fold_location_counter_expression(self, symbol: Union[op._equ, op._assignment]) -> str | None:
        """Evaluate MASM absolute expressions that depend on known offsets."""
        value = getattr(symbol, "value", None)
        if not isinstance(value, Expression):
            return None
        if not self._contains_asm_address_term(value):
            return None
        current_offset = getattr(symbol, "offset", None)
        if current_offset is None and not Token_.find_tokens(value, "dollar"):
            current_offset = 0
        folded = self._eval_asm_int_expression(value, current_offset)
        return None if folded is None else str(folded)

    def _eval_asm_int_expression(self, node: Any, current_offset: int | None) -> int | None:
        """Evaluate the integer subset of MASM expressions used for constants."""
        if isinstance(node, Expression):
            if len(node.children) != 1:
                return None
            return self._eval_asm_int_expression(node.children[0], current_offset)
        if isinstance(node, list):
            if len(node) != 1:
                return None
            return self._eval_asm_int_expression(node[0], current_offset)
        if isinstance(node, Tree):
            if node.data == "dollar":
                return current_offset
            if node.data == "braces":
                inner_children = [
                    child
                    for child in node.children
                    if not (isinstance(child, Token) and child.type in {"LPAR", "RPAR"})
                ]
                if len(inner_children) == 1:
                    return self._eval_asm_int_expression(inner_children[0], current_offset)
                return None
            if node.data == "adddir" and len(node.children) == 3:
                left = self._eval_asm_int_expression(node.children[0], current_offset)
                right = self._eval_asm_int_expression(node.children[2], current_offset)
                if left is None or right is None:
                    return None
                return left + right if str(node.children[1]) == "+" else left - right
            if node.data == "muldir" and len(node.children) == 3:
                left = self._eval_asm_int_expression(node.children[0], current_offset)
                right = self._eval_asm_int_expression(node.children[2], current_offset)
                if left is None or right is None:
                    return None
                operator = str(node.children[1]).lower()
                if operator == "*":
                    return left * right
                if operator == "/" and right:
                    return left // right
                return None
            if node.data == "unadddir" and len(node.children) == 2:
                value = self._eval_asm_int_expression(node.children[1], current_offset)
                if value is None:
                    return None
                return value if str(node.children[0]) == "+" else -value
            if node.data in {
                "size", "sizeofdir", "offsetdir", "segdir", "memberdir",
                "sqexpr", "sqexpr2", "wordopdir", "typedefdir", "dollar2",
            }:
                return None
            if len(node.children) == 1:
                return self._eval_asm_int_expression(node.children[0], current_offset)
            return None
        if isinstance(node, Token):
            if node.type == "INTEGER":
                radix = int(getattr(node, "start_pos", 10) or 10)
                sign = int(getattr(node, "line", 1) or 1)
                return sign * int(str(node.value), radix)
            if node.type in {"LABEL", "COMMON"}:
                return self._known_symbol_offset(str(node))
            return None
        return None

    def _known_symbol_offset(self, name: str) -> int | None:
        """Return a known assembler offset for a symbol, if one is available."""
        symbol = self._context.symbols.get_global(name)
        if isinstance(symbol, op.var):
            return int(symbol.offset)
        if isinstance(symbol, op.Data):
            return int(symbol.offset)
        real_offset = getattr(symbol, "real_offset", None)
        if isinstance(real_offset, int):
            return real_offset
        return None

    def notdir(self, tree: Tree) -> list[Union[str, Token]]:
        return ["~", *self._render_operator_children(tree.children, "notdir")]

    def wordopdir(self, tree: Tree) -> list[str]:
        operator = str(tree.children[0]).lower()
        value = self._render_operator_children(tree.children[1:], "wordopdir")[0]
        if operator == "low":
            return [f"({value} & 0xff)"]
        if operator == "high":
            return [f"(({value} >> 8) & 0xff)"]
        if operator == "lowword":
            return [f"({value} & 0xffff)"]
        if operator == "highword":
            return [f"(({value} >> 16) & 0xffff)"]
        raise ValueError(f"Unknown word operator {operator}")

    def shiftdir(self, tree: Tree) -> list[str]:
        left, operator, right = self._render_operator_children(tree.children, "shiftdir")
        if str(operator).lower() == "shl":
            return [f"({left} << {right})"]
        return [f"({left} >> {right})"]

    def ordir(self, tree: Tree) -> list[Union[str, Token]]:
        left, right = self._render_operator_children(tree.children, "ordir")
        return [left, " | ", right]

    def xordir(self, tree):
        left, right = self._render_operator_children(tree.children, "xordir")
        return [left, " ^ ", right]

    def anddir(self, tree):
        left, right = self._render_operator_children(tree.children, "anddir")
        return [left, " & ", right]

    def _render_known_size_operator(self, target: Any, *, total: bool) -> str:
        if isinstance(target, Tree):
            rendered = "".join(str(part) for part in self.visit(target))
            return f"sizeof({rendered})"
        name = str(target).lower()
        symbol = self._context.symbols.get_global(name)
        if isinstance(symbol, op.var):
            return str(symbol.size * symbol.elements if total else symbol.size)
        if isinstance(symbol, op.Struct):
            return f"sizeof({name})" if total else str(symbol.size)
        return f"sizeof({target})"

    def sizearg(self, tree: Tree) -> list[str]:
        return [self._render_known_size_operator(tree.children[0], total=True)]

    def sizeofdir(self, tree: Tree) -> list[str]:
        return [self._render_known_size_operator(tree.children[0], total=False)]


class IR2Cpp(Cpp):
    def __init__(
        self,
        parser: "Parser",
        *,
        lea: bool = False,
        indirection: IndirectionType = IndirectionType.VALUE,
        is_jump: bool = False,
        is_call: bool = False,
        assignments: dict[str, Expression] | None = None,
    ) -> None:
        super().__init__(context=parser)
        self.lea = lea
        self._expr_state.indirection = indirection
        self.itisjump = is_jump
        self.itiscall = is_call
        if assignments is not None:
            self._assignments = assignments



if __name__ == "__main__":
    import doctest
    doctest.testmod()
