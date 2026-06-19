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
        for p in sorted(procs):  # TODO only if used or public
            result += "%sbool %s(m2c::_offsets, struct m2c::_STATE*);\n" % (
                self.renderer.function_linkage(p),
                self.renderer.mangle_label(p),
            )

        for i in sorted(context.externals_procs):
            v = context.symbols.get_global(i)
            if v.used:
                result += f"extern bool {v.name}(m2c::_offsets, struct m2c::_STATE*);\n"

        result += """
static bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state);
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
        self._assignments: dict[str, Expression] = {}
        self._expr_state.is_member = False

        self.far = False
        self._expr_state.reset()

        self.itisjump = False
        self.itiscall = False
        self.__type_table = {op.DataType.NUMBER: self.produce_c_data_number,
                             op.DataType.ARRAY: self.produce_c_data_array,
                             op.DataType.ZERO_STRING: self.produce_c_data_zero_string,
                             op.DataType.ARRAY_STRING: self.produce_c_data_array_string,
                             op.DataType.OBJECT: self.produce_c_data_object,
                             }

    def function_linkage(self, name: str) -> str:
        return "" if name in getattr(self._context, "public_symbols", set()) else "static "

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
            return self._old_struct_member_offset_constant_name(name)
        if name in self._assignments:
            return self.render_instruction_argument(self._assignments[name])
        if (g := self._context.symbols.get_and_mark_global(name)) is None:
            return name

        state = self._expr_state
        state.is_label = True

        if isinstance(g, op.var):
            return self.convert_label_var(g, name, original_name)
        elif isinstance(g, op.label):
            return f"m2c::k{name}" if self._expr_state.data_label_size or not self.itisjump else name
        elif isinstance(g, op._assignment):
            if self._context.test_mode:
                self._apply_assignment_symbol_state(g)
                return name
            return self.render_instruction_argument(g.value)
        return name

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

            if not self.lea:
                self._expr_state.indirection = IndirectionType.POINTER

        #print("\ng.elements == 1 %s, self._expr_state.is_just_label=%s, not self.lea=%s, g.size == self.element_size %s" %(
        #      g.elements == 1, self._expr_state.is_just_label, not self.lea, g.size == self.element_size))
        simple_argument = (
            g.elements == 1
            and state.is_just_label
            and not self.lea
            and g.size == state.element_size
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
            result = f"offset({g.segment},{g.name})"
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
            for segment in segments.values():
                segment_data_cpp, segment_hpp = self._emit_segment_binding_declarations(segment)
                data_cpp_file += segment_data_cpp
                hpp_file += segment_hpp

                for data in segment.getdata():
                    rendered = self._render_data_declaration(data)
                    cpp_file += rendered["cpp_init"]
                    data_hpp_file += rendered["data_hpp_decl"]
                    data_cpp_file += rendered["data_cpp_ref"]
                    hpp_file += rendered["extern_hpp_decl"]
                for alias in self._iter_data_aliases_for_segment(segment):
                    data_cpp_file += self._render_data_alias_reference(alias)
                    hpp_file += self._render_data_alias_extern(alias)
            return cpp_file, data_hpp_file, data_cpp_file, hpp_file
        finally:
            self._expr_state.data_label_size = prev_data_label_size

    def _iter_data_aliases_for_segment(self, segment: Any):
        segment_names = set(getattr(segment, "segment_aliases", {segment.name: 0}))
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

    def _emit_segment_binding_declarations(self, segment: Any) -> tuple[str, str]:
        data_cpp = ""
        hpp = ""
        aliases = getattr(segment, "segment_aliases", {segment.name: 0})
        for name, relative_offset in aliases.items():
            data_cpp += f"db& {name}=*((db*)&m2c::m+0x{segment.offset + relative_offset:x});\n"
            hpp += f"extern db& {name};\n"
        return data_cpp, hpp

    def _render_data_declaration(self, data: Data) -> dict[str, str]:
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
            ) = self._render_data_assignment_and_refs(data, value, type_and_name)

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
        data_cpp_ref = self._generate_dataref_from_declaration_c(type_and_name)
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

    def _generate_dataref_from_declaration_c(self, _hpp):
        """It takes a C++ declaration and returns a reference to the same variable.

        :param _hpp: declaration string
        :return: The reference to the same data
        """
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
            value = f'offsetof({label[0]},{".".join(label[1:])})'

        if self._expr_state.indirection == IndirectionType.POINTER and state.needs_dereference and state.struct_type:
            state.is_member = True
            state.needs_dereference = False

        return value

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
                value = f'offset({g.segment},{".".join(label)})'
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
            value = f'offset({g.segment},{".".join(label)})'
        elif isinstance(g, op.Struct):
            value = f'offsetof({label[0]},{".".join(label[1:])})'
        elif isinstance(g, (op._equ, op._assignment)):
            value = f'({label[0]})+offsetof({g.original_type},{".".join(label[1:])})'
        else:
            raise Exception(f"Not handled type {type(g)!s}")

        self._expr_state.indirection = IndirectionType.VALUE
        return value

    def convert_sqbr_reference(self, segment: str, expr: str, size: int) -> str:
        state = self._expr_state
        if not state.is_label or not state.is_variable:
            state.needs_dereference = True
            state.is_pointer = True
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
            self.dispatch += f"__disp={name};\n"
            name = "__dispatch_call"

        return name, far

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
                proc_name = "__dispatch_call"

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
            proc_name, label_ip = "__dispatch_call", proc_name

        proc_name = self.mangle_label(proc_name)

        if far:
            ret += f"CALLF({proc_name},{label_ip})"
        else:
            ret += f"CALL({proc_name},{label_ip})"
        return ret

    def _render_with_flags(self, expr: Expression, *, is_jump: bool = False, is_call: bool = False) -> str:
        prev_jump, prev_call = self.itisjump, self.itiscall
        self.itisjump, self.itiscall = is_jump, is_call
        try:
            return self.render_instruction_argument(expr, 0)
        finally:
            self.itisjump, self.itiscall = prev_jump, prev_call

    def _ret(self, src: list[Union[Expression, Any]]) -> str:
        arg = self.render_instruction_argument(src[0]) if src else "0"
        return f"RETN({arg})"

    def _retf(self, src: list[Union[Expression, Any]]) -> str:
        arg = self.render_instruction_argument(src[0]) if src else "0"
        return f"RETF({arg})"

    def _xlat(self, src: list[Union[Expression, Any]]) -> str:
        if not src:
            return "XLAT"
        arg = self.render_instruction_argument(src[0])[2:-1]
        return f"XLATP({arg})"

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
        label_str, _ = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "!GET_ZF()"):
            return dispatch
        return f"JNZ({label_str})"

    def _jbe(self, label: Expression) -> str:
        label_str, _ = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "GET_CF() || GET_ZF()"):
            return dispatch
        return f"JBE({label_str})"

    def _ja(self, label: Expression) -> str:
        label_str, far = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "!GET_CF() && !GET_ZF()"):
            return dispatch
        return f"JA({label_str})"

    def _jc(self, label: Expression) -> str:
        label_str, far = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "GET_CF()"):
            return dispatch
        return f"JC({label_str})"

    def _jnc(self, label: Expression) -> str:
        label_str, far = self.jump_post(label)
        if dispatch := self._conditional_cross_proc_dispatch(label_str, "!GET_CF()"):
            return dispatch
        return f"JNC({label_str})"

    def _conditional_cross_proc_dispatch(self, label: str, condition: str) -> str:
        if not self._context.args or self._context.args.get("mergeprocs") != "separate":
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
        return "CMPSB"

    def _lodsb(self) -> str:
        return "LODSB"

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

        with open(cpp_fname, "w", encoding=self.__codeset) as cpp_file:
            hpp_file = open(header_fname, "w", encoding=self.__codeset)

            cpp_file.write(f"""{banner}
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

         namespace m2c {{
          void   Initializer()
        #else
         #define MYCOPY(x) memcpy(&x,&tmp999,sizeof(tmp999));
         namespace {{
          struct Initializer {{
           Initializer()
        #endif
        {{
        {cpp_assigns}
        }}
        #ifndef DOSBOX_CUSTOM
          }};
         static const Initializer i;
        #endif
        }}
        """)
        hpp_file.write(f"""{banner}
#ifndef {header_id}
#define {header_id}

#include "asm.h"

{self.produce_structures(self._context.structures)}
{equates}
{cpp_extern}
#if __has_include("_equates.h")
#include "_equates.h"
#endif
{self.produce_label_offsets()}
{self.proc_strategy.write_declarations(self._procs + list(self.grouped), self._context)}
{self.produce_externals(self._context)}
#endif
""")

        hpp_file.close()

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
        )

    def write_procedures(self, banner, header_fname):
        cpp_file_text = ""
        split_segment_includes: list[str] = []
        last_segment = None
        cpp_segment_file = None
        self.generate_label_to_proc_map()
        for name in self._procs:
            proc_text, segment = self._render_procedure(name)
            if self._is_listing_source() and segment != last_segment:  # If .lst write to separate segments. Open new if changed
                last_segment = segment
                if cpp_segment_file:
                    cpp_segment_file.close()

                cpp_segment_fname = f"{self._namespace.lower()}_{segment}.cpp"
                split_segment_includes.append(cpp_segment_fname)
                logging.info(f" *** Generating output file in C++ {cpp_segment_fname}")
                cpp_segment_file = open(cpp_segment_fname, "w", encoding=self.__codeset)
                cpp_segment_file.write(f"""{banner}
#include "{header_fname}"

                """)

            if cpp_segment_file:
                cpp_segment_file.write(f"{proc_text}\n")
            else:
                cpp_file_text += f"{proc_text}\n"
            self.__proc_done.append(name)
            self.__methods.append(name)
        if cpp_segment_file:
            cpp_segment_file.close()

        if split_segment_includes:
            cpp_file_text += "\n".join(f'#include "{name}"' for name in split_segment_includes)
            cpp_file_text += "\n"

        return cpp_file_text

    def produce_equates(self) -> str:
        result = ""
        for symbol in self._context.symbols.get_globals().values():
            if not isinstance(symbol, op._equ) or symbol.implemented:
                continue
            result += self.render_equate_definition(symbol.name, symbol)
            symbol.implemented = True
        self._cmdlabel = ""
        return result

    def export_equates(self) -> list[tuple[str, str]]:
        equates: list[tuple[str, str]] = []
        public_symbols: set[str] = getattr(self._context, "public_symbols", set())
        for symbol in self._context.symbols.get_globals().values():
            if not isinstance(symbol, op._equ) or not isinstance(symbol.value, Expression):
                continue
            if symbol.name not in public_symbols:
                continue
            rendered = self.render_equate_value(symbol)
            if rendered and not self._is_module_local_equate_value(rendered):
                equates.append((symbol.name, rendered))
        return equates

    @staticmethod
    def _is_module_local_equate_value(rendered: str) -> bool:
        return any(token in rendered for token in ("sizeof(", "offset(", "far_offset(", "seg_offset("))

    def render_equate_definition(self, name: str, symbol: op._equ) -> str:
        if isinstance(symbol.value, str):
            return f"#define {name} {symbol.value}\n"
        rendered = self.render_equate_value(symbol)
        if not rendered:
            return ""
        if rendered.startswith("sizeof("):
            return f"static const int {name} = (int){rendered};\n"
        if not re.search(r"[A-Za-z_]", rendered):
            return f"static const int {name} = {rendered};\n"
        return f"#define {name} ({rendered})\n"

    def render_equate_value(self, symbol: op._equ) -> str:
        src = symbol.value
        if not isinstance(src, Expression):
            return ""
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
            f"""
 {self.function_linkage(p)}bool {self.renderer.mangle_label(p)}(m2c::_offsets, struct m2c::_STATE* _state){{return {self.groups[p]}(m2c::k{p}, _state);}}
"""
            for p in sorted(self.grouped)
        )
        label_wrappers = "".join(
            f"""
 bool {self.renderer.mangle_label(name)}(m2c::_offsets, struct m2c::_STATE* _state){{return {owner}(m2c::k{name}, _state);}}
"""
            for name, owner in sorted(self._public_label_wrapper_targets().items())
        )
        return grouped_wrappers + label_wrappers

    def _public_label_wrapper_targets(self) -> dict[str, str]:
        targets: dict[str, str] = {}
        for name, symbol in self._context.symbols.get_globals().items():
            if not isinstance(symbol, op.label) or not symbol.globl:
                continue
            owner = self.label_to_proc.get(symbol.name)
            if not owner or owner == name or name in self._procs or name in self.grouped:
                continue
            targets[name] = owner
        return targets

    def convert_segment_files_into_datacpp(self, asm_files):
        """It reads .seg files, and writes the data segments to _data.cpp/h file.

        :param asm_files: A list of the assembly files
        """
        self.write_data_segments_cpp(*self.read_segment_files(asm_files))

    def write_data_segments_cpp(self, segments, structures):
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
            _, data_h, data_cpp_reference, _ = self.render_data_c(segments)
        finally:
            self._context.segments = previous_segments
            self._context.structures = previous_structures
        self._write_equates_header(getattr(self._context, "exported_equates", []))
        fname = "_data.cpp"
        header = "_data.h"
        with open(fname, "w", encoding=self.__codeset) as fd:
            fd.write(f"""#include "_data.h"
namespace m2c{{

struct Memory m;

struct Memory types;

db(& stack)[STACK_SIZE]=m.stack;
db(& heap)[HEAP_SIZE]=m.heap;
}}
{data_cpp_reference}

""")

        with open(header, "w", encoding=self.__codeset) as hd:
            hd.write("""
#ifndef ___DATA_H__
#define ___DATA_H__
#include "asm.h"
""" + self.produce_structures(structures) + self.produce_data(data_h) + """
#endif
""")

    def _write_equates_header(self, equates: list[tuple[str, str]]) -> None:
        with open("_equates.h", "w", encoding=self.__codeset) as f:
            f.write("#ifndef __M2C_EQUATES_H__\n#define __M2C_EQUATES_H__\n\n")
            for name, value in equates:
                f.write(f"#ifndef {name}\n#define {name} ({value})\n#endif\n")
            f.write("\n#endif\n")

    def _deduplicate_memory_field_labels(self, segments: OrderedDict) -> OrderedDict:
        result = deepcopy(segments)
        seen: set[str] = set()
        for segment in result.values():
            for data in segment.getdata():
                if not data.label:
                    continue
                label = data.label.lower()
                if label not in seen:
                    seen.add(label)
                    continue
                data.label = self._unique_memory_field_label(data, seen)
                seen.add(data.label.lower())
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

    def produce_label_offsets(self):
        labeloffsets = """namespace m2c{
void   Initializer();
static const dd kbegin = 0x1001;
"""
        i = 0x1001
        for k, v in list(self._context.symbols.get_globals().items()):
            if isinstance(v, (op.label, Proc)):
                k = re.sub(r"[^A-Za-z0-9_]", "_", k).lower()
                i += 1
                if v.real_offset or v.real_seg:
                    i = v.real_seg * 0x10000 + v.real_offset
                labeloffsets += f"static const dd k{k} = 0x{i:x};\n"
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
        for member_name, (struct_name, _offset) in offsets.items():
            const_name = self._old_struct_member_offset_constant_name(member_name)
            result += f"static const word {const_name} = offsetof({struct_name}, {member_name});\n"
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
        for i in context.externals_vars:
            v = context.symbols.get_global(i)
            if v.used:
                data += f"extern {self._cpp_external_type(v.original_type)}& {v.name};\n"
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
        a, b = self.parse2(dst, src)
        assert dstr and srcr
        return "MOVS(%s, %s, %s, %s, %d)" % (a, b, dstr[0], srcr[0], size)

    def _repe(self):
        self.prefix = "\tREPE "
        return ""

    def _repne(self):
        self.prefix = "\tREPNE "
        return ""

    def _lods(self, src: Expression) -> str:
        a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        srcr = Token_.find_tokens(src, REGISTER)
        assert srcr
        return "LODS(%s,%s,%d)" % (a, srcr[0], size)

    def _leave(self) -> str:
        return "LEAVE"  # MOV(esp, ebp) POP(ebp)

    def _int(self, dst: Expression) -> str:
        a = self.render_instruction_argument(dst)
        return f"_INT({a})"

    def _instruction0(self, cmd: str) -> str:
        return cmd.upper()

    def _instruction1(self, cmd: str, dst: Expression) -> str:
        a = self.render_instruction_argument(dst)
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
        result = "".join(ir2cpp.visit(render_expr))
        rendered = result[1:-1] if self.check_parentesis(result) else result
        return rendered, ir2cpp._expr_state

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
        }.get(cmd.upper())
        if condition and (dispatch := self._conditional_cross_proc_dispatch(label, condition)):
            return dispatch
        assert self._context.args
        if self._context.args.get("mergeprocs") == "separate" and cmd.upper() == "JMP":
            if label == "__dispatch_call":
                return "return __dispatch_call(__disp, _state);"
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
                        return f"return {g.name}(0, _state);"
                    return f"return {target_proc_name}(m2c::k{label}, _state);"

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
        state.element_size = data.getsize()
        try:
            logging.debug("current data type = %s", internal_data_type)
            rc, rh = self.__type_table[internal_data_type](data)
        finally:
            state.element_size = prev_size

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
            rc = "".join(str(i) if isinstance(i, int) else "".join(str(x) for x in self.visit(i)) for i in r)
        rc = self._replace_current_location_symbol(rc, data)
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
                rc = ",".join(
                    self.convert_char(i) if isinstance(i, str) or data_ctype == "char" else str(i)
                    for i in single
                )
            else:
                rc = self._runtime_pointer_expression_for_value(source_linear, single, element_size) or str(single)
            rc = self._replace_current_location_symbol(rc, data)
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
                element_value = "".join(self.visit(v))
                rc += self._replace_current_location_symbol(element_value, data, i, element_size)
            elif isinstance(v, list):
                values = [str(i) for i in v]
                element_value = "".join(values)
                rc += self._replace_current_location_symbol(element_value, data, i, element_size)
            else:
                element_linear = None if source_linear is None else source_linear + i * element_size
                element_value = (
                    self._runtime_pointer_expression_for_value(element_linear, v, element_size)
                    or (self.convert_char(v) if isinstance(v, str) or data_ctype == "char" else str(v))
                )
                rc += self._replace_current_location_symbol(element_value, data, i, element_size)
        rc += "}"
        rh = f"{data_ctype} {label}[{elements}]"
        return rc, rh

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
        if isinstance(c, int) and c not in [10, 13]:
            return str(c)
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
     if ((__i>>16) == 0) {__i |= ((dd)cs) << 16;}
     __disp=__i;
     switch (__i) {
"""
        else:
            result = """
  static bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state){
     switch (__disp) {
"""
        entries = OrderedDict()
        for k, v in globals:
            if isinstance(v, Proc) and v.used:
                k = re.sub(r"[^A-Za-z0-9_]", "_", k)  # need to do it during mangling
                entries[k] = (self.mangle_label(k), "0")
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
        for name in sorted(names):
            result += "        case m2c::k{}: \t{}({}, _state); break;\n".format(name, *entries[name])

        result += "        default: m2c::log_error(\"Don't know how to call to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(); abort();\n"
        result += "     };\n     return true;\n}\n"
        return result

    def _mov(self, dst: Expression, src: Expression) -> str:
        a, b = self.parse2(dst, src)
        mapped_memory_access = "raddr" in a or "raddr" in b
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
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
        """
        for name, label in offsets:
            logging.debug("%s, %s", name, label)
            result += f"        case m2c::k{name}: \tgoto {label};\n"
        result += "        default: m2c::log_error(\"Don't know how to jump to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(); abort();\n"
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
        state.reset()
        previous_indirection = state.indirection
        state.indirection = self._effective_indirection_for_expr(tree)
        prev_element_size = state.element_size
        state.element_size = tree.element_size
        try:
            self._initialize_expr_shape_flags(tree)
            result = "".join(self.visit(tree.children))
            return self._finalize_rendered_expr(tree, result)
        finally:
            state.indirection = previous_indirection
            state.element_size = prev_element_size

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
            result = f"(({state.struct_type}*)raddr({state.work_segment},{result}"
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
            if g.issegment:
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

        if isinstance(name, list):
            return ["".join(str(part) for part in self.visit(name))]
        if isinstance(name, lark.Tree):
            return ["".join(str(part) for part in self.visit(name))]

        assert isinstance(name, str)
        if (g := self._context.symbols.get_global(name)) is None:
            return [name]
        if isinstance(g, op.var):
            logging.debug("it is var %s", g.size)
            offset_size = self._expr_state.element_size
            if offset_size not in {2, 4}:
                offset_size = 2
            if offset_size == 2:
                return [f"offset({g.segment},{g.name})"]
            return [f"far_offset({g.segment},{g.name})"]
        elif isinstance(g, (Proc, op.label)):
            logging.debug("it is proc")
            return [f"m2c::k{g.name}"]
        elif isinstance(g, (op._equ, op._assignment)) and isinstance(g.value, Expression):
            return ["".join(str(part) for part in self.visit(g.value))]
        elif isinstance(g, (op._equ, op._assignment)):
            return [g.original_name]
        else:
            raise ValueError("Unknown type for offsetdir %s", type(g))

    def _render_operator_children(self, children: list[Any]) -> list[str]:
        rendered = []
        for child in children:
            if isinstance(child, lark.Token):
                rendered.append("".join(str(part) for part in self.visit(child)))
            elif isinstance(child, str):
                rendered.append(child)
            else:
                rendered.append("".join(str(part) for part in self.visit(child)))
        return rendered

    def notdir(self, tree: Tree) -> list[Union[str, Token]]:
        return ["~", *self._render_operator_children(tree.children)]

    def wordopdir(self, tree: Tree) -> list[str]:
        operator = str(tree.children[0]).lower()
        value = self._render_operator_children(tree.children[1:])[0]
        if operator == "low":
            return [f"({value} & 0xff)"]
        if operator == "high":
            return [f"(({value} >> 8) & 0xff)"]
        if operator == "lowword":
            return [f"({value} & 0xffff)"]
        if operator == "highword":
            return [f"(({value} >> 16) & 0xffff)"]
        raise ValueError(f"Unknown word operator {operator}")

    def ordir(self, tree: Tree) -> list[Union[str, Token]]:
        left, right = self._render_operator_children(tree.children)
        return [left, " | ", right]

    def xordir(self, tree):
        left, right = self._render_operator_children(tree.children)
        return [left, " ^ ", right]

    def anddir(self, tree):
        left, right = self._render_operator_children(tree.children)
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
