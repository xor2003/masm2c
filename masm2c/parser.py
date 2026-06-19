""" Module to parse assembler source """
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
from masm2c.proc import Proc
from ast import literal_eval
import hashlib
import logging
import os
import re
import sys
from collections import OrderedDict
from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import Any, Optional, Final, cast
from collections.abc import Callable

import jsonpickle  # type: ignore[import-untyped]
from lark import UnexpectedToken, lark
from lark.lexer import Token
from lark.tree import Tree

from masm2c.op import Data, Struct, _assignment, _equ, baseop, label, var
from masm2c.Token import Token as Token_, Expression
from masm2c.gen import avoid_cpp_keyword
from .symbol_table import SymbolTable # Added import

from . import op
from .pgparser import (
    Asm2IR,
    AsmData2IR,
    BottomUpVisitor,
    ExprRemover,
    IncludeLoader,
    LarkParser,
    _is_token,
    _token_lower,
)
from .Macro import Macro
from .enumeration import IndirectionType

INTEGERCNST = "integer"
STRINGCNST = "STRING"

_REGEX_STRUCT_COMMENT = re.compile(
    r"^struct\s+(?P<name>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\b",
    flags=re.IGNORECASE,
)
_REGEX_STRUCT_HDR = re.compile(
    r"^(?P<name>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+(?:STRUC|STRUCT|UNION)\b",
    flags=re.IGNORECASE,
)
_REGEX_STRUCT_INSTANCE = re.compile(
    r"^(?P<label>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+"
    r"(?P<stype>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+"
    r"[A-Za-z0-9_@$?.]+\s+DUP\s*\(",
    flags=re.IGNORECASE,
)
_REGEX_STRUCT_INSTANCE_SIMPLE = re.compile(
    r"^(?P<label>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+"
    r"(?P<stype>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+<",
    flags=re.IGNORECASE,
)
_REGEX_STRUCT_INSTANCE_LINE = re.compile(
    r"^(?P<ws>\s*)(?P<name>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+(?P<rest><.+)$",
)
_REGEX_STRUCT_DUP_INSTANCE_LINE = re.compile(
    r"^(?P<ws>\s*)(?P<name>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+"
    r"(?P<rest>[A-Za-z0-9_@$?.]+\s+DUP\s*\(.+)$",
    flags=re.IGNORECASE,
)
_DATA_DECL_NAMES = {
    "db", "dw", "dd", "df", "dq", "dt",
    "byte", "sbyte", "word", "sword", "dword", "sdword",
    "fword", "qword", "tbyte", "real4", "real8", "real10",
}


@dataclass
class _PendingParseState:
    proc_options: list[str] = field(default_factory=list)
    mnemonic: str = ""
    source_comment: str = ""

    def reset(self) -> None:
        self.proc_options.clear()
        self.mnemonic = ""
        self.source_comment = ""


@dataclass
class _ConditionalFrame:
    parent_active: bool
    branch_taken: bool
    current_active: bool


@dataclass
class _TextMacro:
    parameters: list[str]
    body: list[str]


class Vector:
    """A 2D vector class with basic vector operations."""
    
    def __init__(self, arg1: int=0, arg2: int=0) -> None:
        """Initialize a new vector with x and y components.
        
        Args:
            arg1: x component (default: 0)
            arg2: y component (default: 0)
        """
        self.__value: list[int] = [arg1, arg2]

    def __add__(self, vec: Optional["Vector"]) -> "Vector":
        """Add another vector to this vector.
        
        Args:
            vec: The vector to add. If None, returns a copy of this vector.
            
        Returns:
            A new Vector instance with the sum of the vectors.
        """
        if vec is None:
            return Vector(self.__value[0], self.__value[1])
        return Vector(self.__value[0] + vec.values[0], self.__value[1] + vec.values[1])

    def __mul__(self, other: int) -> "Vector":
        """Multiply this vector by a scalar.
        
        Args:
            other: The scalar to multiply by.
            
        Returns:
            A new Vector instance with scaled components.
            
        Raises:
            TypeError: If other is not an integer.
        """
        if not isinstance(other, int):
            raise TypeError(f"Cannot multiply Vector by {type(other)}")
        return Vector(self.__value[0] * other, self.__value[1] * other)

    def __repr__(self) -> str:
        """Return a string representation of the vector."""
        return f"Vector({self.__value[0]}, {self.__value[1]})"

    @property
    def values(self) -> list[int]:
        """Return the vector components as a list."""
        return self.__value.copy()

class ExprSizeCalculator(BottomUpVisitor):

    def __init__(self, element_size: int=0, *, init: Vector, **kwargs) -> None:
        super().__init__(init=init, **kwargs)
        self.element_number = 0
        self.element_size = element_size
        self.kwargs = kwargs

    def expr(self, tree: Expression, size: Vector) -> Vector:
        if self.element_size:
            tree.element_size = self.element_size
        """

        self.element_number += tree.element_number
        size += tree.size()
        #self.size += size
        """
        return Vector(tree.size(), tree.element_number)

    def dupdir(self, tree: lark.Tree, size: Vector) -> Vector:
        #if not hasattr(tree, "repeat"):
        #    raise RuntimeError()
        return size * tree.meta.line

    def LABEL(self, token: Token) -> Vector | None:  # TODO very strange, to replace
        context = self.kwargs["context"]
        if not (g := context.symbols.get_and_mark_global(token)):
            return None
        if isinstance(g, op.var):
            if self.element_size < 1:
                self.element_size = g.size
            return Vector(self.element_size, 1)
        elif isinstance(g, (op._assignment, op._equ)) and isinstance(g.value, Expression):
            self.element_size = g.value.size()
            if self.element_size < 1:
                self.element_size = self.visit(g.value).values[0]
            return Vector(self.element_size, 1)
        return None

    def register(self, tree: Tree, size: Vector) -> Vector:
        context = self.kwargs["context"]
        self.element_size = context.register_size(tree.children[0])
        return Vector(self.element_size, 1)

    def segmentregister(self, tree: Tree, size: Vector) -> Vector:
        return self.register(tree, size)

    def memberdir(self, tree: Tree, size: Vector) -> Vector:
        label = tree.children
        context = self.kwargs["context"]
        g = context.symbols.get_and_mark_global(label[0])
        type = label[0] if isinstance(g, op.Struct) else g.original_type

        try:
            for member in label[1:]:
                if (g := context.symbols.get_and_mark_global(type)) is None:
                    raise KeyError(type)
                if isinstance(g, op.Struct):
                    g = g.getitem(str(member))
                    type = g.data  # type: ignore[union-attr]
                else:
                    return g._size
        except KeyError as ex:
            logging.debug("Didn't found for %s %s will try workaround", label, ex.args)
            # if members are global as with M510 or tasm try to find last member size
            g = context.symbols.get_and_mark_global(label[-1])

        self.element_size = g.size
        return Vector(self.element_size, 1)


def dump_object(value: Struct | label | Proc | var | _equ | _assignment) -> str:
    """Represents object as string.

    :param value: The object to dump
    :return: A string representation of the object.
    """
    if not hasattr(value, "__dict__"):
        return ""
    stuff = str(vars(value))
    replacements = (
        (r"\n", " "),
        (r"[{}]", ""),
        (r"'([A-Za-z_0-9]+)'\s*:\s*", r"\g<1>="),
    )
    for old, new in replacements:
        stuff = re.sub(old, new, stuff)
    stuff = f"{value.__class__.__name__}({stuff})"
    return stuff


class Parser:
    c_dummy_label: Final[list] = [0]
    _file_cache: dict[str, tuple[float, str]] = {}

    def __init__(self, args: Optional[dict] = None) -> None:
        """Assembler parser."""
        self.test_mode = False
        # self.__globals: OrderedDict[str, Struct | label | Proc | var | _equ | _assignment] = OrderedDict() # Removed
        self.symbols = SymbolTable() # Use SymbolTable
        self.symbols.test_mode = self.test_mode # Pass test_mode flag
        self.pass_number = 0

        self.__lex = LarkParser(context=self)

        self.externals_vars: set[str] = set()
        self.externals_procs: set[str] = set()
        self.macroses: OrderedDict[str, Any] = OrderedDict()
        self._text_macros: dict[str, _TextMacro] = {}
        self.itislst = False
        self.source_is_lst = False
        self.initial_procs_start: set[int] = set()
        self.procs_start: set[int] = set()
        self.runtime_code_meta: dict[int, dict[str, Any]] = {}
        self.runtime_abi_meta: dict[int, dict[str, Any]] = {}
        self.runtime_meta: dict[str, Any] = {}
        self.runtime_function_sampling_meta: dict[int, dict[str, Any]] = {}
        self.runtime_data_meta: dict[int, dict[str, Any]] = {}
        self.runtime_pointer_meta: dict[int, list[dict[str, Any]]] = {}
        self.runtime_access_site_meta: dict[int, list[dict[str, Any]]] = {}
        self.runtime_meta_anchor: int | None = None

        if not args:
            args = {"mergeprocs": "separate"}
        self.args = args
        self.arg_renderer_factory = None
        self.expr_int_evaluator = None
        self._include_loader = IncludeLoader(self)
        self._expr_remover = ExprRemover()
        self._asm2ir = Asm2IR(self)

        self.next_pass(Parser.c_dummy_label[0])

    def next_pass(self, counter: int) -> None:
        """Initializer for each pass.

        :param counter: Labels id counter
        :return:
        """
        self.pass_number += 1
        logging.info(f"     Pass number {self.pass_number}")
        self.symbols.set_pass_info(self.pass_number, self.test_mode) # Update SymbolTable
        Parser.c_dummy_label[0] = counter

        self.procs_start = self.initial_procs_start
        self.segments = OrderedDict()
        self.data_aliases: list[op.var] = []
        self.public_symbols: set[str] = set()
        self.flow_terminated = True
        self.need_label = True

        self.structures: OrderedDict[str, Struct] = OrderedDict()
        self.record_names: set[str] = set()
        self.record_defs: dict[str, list[int]] = {}
        self.macro_names_stack: list[str] = []
        self.proc_list: list[str] = []
        self.proc = None
        self.old_struct_fields = False
        self.old_struct_member_offsets: OrderedDict[str, tuple[str, int]] = OrderedDict()

        self.__offset_id = 0x1111
        self.entry_point = "mainproc_begin"
        self.main_file = False
        self.__proc_stack: list[Proc] = []

        self.__binary_data_size = 0
        self.__cur_seg_offset = 0
        self.__c_dummy_jump_label = 0
        self.__c_extra_dummy_jump_label = 0

        self.__segment_name = "default_seg"
        self.__segment = op.Segment(self.__segment_name, 0, comment="Artificial initial segment")
        self.segments[self.__segment_name] = self.__segment

        self.proc = self.add_proc("mainproc", "", 0, False)

        self.used = False

        self.radix = 10

        self.current_macro = None
        self.current_struct: Optional[Struct] = None
        self._pending = _PendingParseState()
        self._text_macro_expansion_id = 0
        self._text_equates: dict[str, str] = {}

        self.struct_names_stack: list[str] = []

        self._current_file = ""
        self.__current_file_hash = "0"

        self.data_merge_candidates = 0

        self.equs: set[str] = set()


    def replace_dollar_w_segoffst(self, v: str) -> str:
        logging.debug("$ = %d", self.__cur_seg_offset)
        return v.replace("$", str(self.__cur_seg_offset))

    @staticmethod
    def _parse_octal(v: str) -> int:
        """Parse octal number string (ending with O or Q)"""
        return int(v[:-1], 8)

    @staticmethod
    def _parse_hex(v: str) -> int:
        """Parse hexadecimal number string (ending with H)"""
        return int(v[:-1], 16)

    @staticmethod
    def _parse_binary(v: str) -> int:
        """Parse binary number string (ending with B)"""
        return int(v[:-1], 2)

    @staticmethod
    def _parse_decimal(v: str) -> int:
        """Parse decimal number or expression"""
        try:
            return Parser._eval_int_expression(v)
        except Exception:
            return int(v)

    @staticmethod
    def _eval_int_expression(rendered: str) -> int:
        return int(eval(rendered, {"__builtins__": {}}, {}))

    @staticmethod
    def parse_int(v: str) -> int:
        """Parse integer from string in various bases (hex, octal, binary, decimal)"""
        assert isinstance(v, str)
        v = v.strip()
        
        if re.match(r"^[+-]?[0-8]+[OoQq]$", v):
            return Parser._parse_octal(v)
        elif re.match(r"^[+-]?\d[0-9A-Fa-f]*[Hh]$", v):
            return Parser._parse_hex(v)
        elif re.match(r"^[01]+[Bb]$", v):
            return Parser._parse_binary(v)
        else:
            return Parser._parse_decimal(v)

    def identify_data_internal_type(self, data: Tree, elements_count: int, is_string_type: bool) -> op.DataType:
        if not is_string_type:
            return op.DataType.ARRAY if elements_count > 1 else op.DataType.NUMBER
        args = data.children
        last_value = None
        if args and isinstance(args[-1], Tree) and args[-1].children:
            last_value = args[-1].children[-1]
        return (
            op.DataType.ZERO_STRING
            if elements_count >= 2
               and not (isinstance(args[-1], Tree) and args[-1].data == "dupdir")
            and _is_token(last_value)
            and cast(Token, last_value).type == "INTEGER"
            and cast(Token, last_value).value == "0"
            else op.DataType.ARRAY_STRING
        )



    def action_label(self, name: str, far: bool=False, isproc: bool=False, raw: str="", globl: bool=True, line_number: int=0) -> None:
        """Create and register a new label in the current procedure
        
        Args:
            name: Original label name
            far: Whether the label has far addressing
            isproc: Whether the label represents a procedure
            raw: Raw line text for address extraction
            globl: Whether the label has global scope
            line_number: Source line number
        """
        logging.debug("Creating label: %s", name)
        
        # Handle special placeholder labels
        if name == "arbarb":  # Special case placeholder
            name = self.get_dummy_jumplabel()
            
        # Mangle label name for C compatibility
        mangled_name = self.mangle_label(name)
        
        self.need_label = False
        self.make_sure_proc_exists(line_number, raw)
        
        assert self.proc, "No current procedure for label"
        if mangled_name in self.public_symbols:
            globl = True

        # Create label object
        label_obj = op.label(
            mangled_name,
            proc=self.proc.name,
            isproc=isproc,
            line_number=self.__offset_id,
            far=far,
            globl=globl
        )
        
        # Extract real addresses from listing if available
        _, label_obj.real_offset, label_obj.real_seg = self.get_lst_offsets(raw)
        
        # Update procedure start tracking
        if label_obj.real_seg:
            self.procs_start.discard(label_obj.real_seg * 0x10 + label_obj.real_offset)
            
        # Register label with procedure and symbol table
        self.proc.add_label(mangled_name, label_obj)
        existing = self.symbols.get_global(mangled_name)
        if (
            existing is not None
            and self.pass_number == 1
            and not globl
            and isinstance(existing, op.label)
        ):
            self.symbols.reset_global(mangled_name, label_obj)
        else:
            self.symbols.set_global(mangled_name, label_obj)
        
        # Increment ID for next label
        self.__offset_id += 1
        self.__offset_id += 1

    def make_sure_proc_exists(self, line_number: int, raw: str) -> None:
        if self.proc:
            return
        _, real_offset, real_seg = self.get_lst_offsets(raw)
        offset = real_offset if real_seg else self.__cur_seg_offset
        pname = f"{self.__segment.name}_{offset:x}_proc"  # automatically generated proc name
        if pname in self.proc_list:
            self.proc = self.symbols.get_and_mark_global(pname)
        else:
            self.proc = self.add_proc(pname, raw, line_number, False)

    def align(self, align_bound=0x10):
        num = (align_bound - (self.__binary_data_size & (align_bound - 1))) if (
                self.__binary_data_size & (align_bound - 1)) else 0
        self.org(num)

    def org(self, num):
        if self.itislst:
            return
        if num == 0:
            return
        label = self.get_dummy_label()
        offset = self.__binary_data_size
        self.__binary_data_size += num
        self.data_merge_candidates = 0

        self.__segment.append(
            op.Data(label, "db", op.DataType.ARRAY, [0], num, num, comment="for alignment", align=True,
                    offset=offset))

    def move_offset(self, pointer, raw):
        if pointer > self.__binary_data_size:
            self.data_merge_candidates = 0
            label = self.get_dummy_label()

            num = pointer - self.__binary_data_size
            offset = self.__binary_data_size
            self.__binary_data_size += num

            self.__segment.append(
                op.Data(label, "db", op.DataType.ARRAY, [0], num, num, comment="move_offset", align=True,
                        offset=offset))
        elif pointer < self.__binary_data_size and not self.itislst:
            self.data_merge_candidates = 0
            logging.warning(f"Maybe wrong offset current:{self.__binary_data_size:x} should be:{pointer:x} ~{raw}~")

    def get_dummy_label(self, line_number: int = 0) -> str:
        if self.test_mode:
            return f"dummy{self.__current_file_hash[0]}_{hex(self.__binary_data_size)[2:]}"
        segment = re.sub(r"[^A-Za-z0-9_]", "_", getattr(self, "_Parser__segment_name", "") or "noseg")
        parts = [self.__current_file_hash[:8], segment, hex(self.__binary_data_size)[2:]]
        if line_number:
            parts.append(str(line_number))
        return "dummy" + "_".join(parts)

    def get_dummy_jumplabel(self):
        self.__c_dummy_jump_label += 1
        return f"dummylabel{self.__c_dummy_jump_label}"

    def get_extra_dummy_jumplabel(self):
        self.__c_extra_dummy_jump_label += 1
        return f"edummylabel{self.__c_extra_dummy_jump_label}"

    def parse_file(self, fname):
        logging.info(f" *** Parsing {fname} file")
        """
        num = 0x1000
        if num:
            self.__binary_data_size += num

            self.__c_dummy_label += 1
            label = "dummy" + str(self.__c_dummy_label)

            self.c_data.append("{0}, // padding\n")
            self.h_data.append(" db " + label + "[" + str(num) + "]; // protective\n")
        """

        self.parse_file_lines(fname)

        self.align()

        return self

    def parse_file_lines(self, file_name):
        previous_itislst = self.itislst
        self._switch_file_context(file_name)
        try:
            content = self._read_whole_file(file_name)
            if file_name.lower().endswith(".lst"):  # for .lst provided by IDA move address to comments after ;~
                # we want exact placement so program could work
                content = self.extract_addresses_from_lst(file_name, content)
            content = self._join_continued_lines(content)
            content = self._wrap_bare_data_table(content)
            content = self.apply_conditional_assembly(content)
            self._preload_text_macros(content, set())
            content = self._strip_text_macro_definitions(content)
            content = self._expand_repeat_blocks(content)
            content = self._expand_text_macros(content)
            content = self._expand_repeat_blocks(content)
            content = self._expand_text_equates(content)
            content = self._trim_trailing_lines_after_end(content)
            self._predeclare_included_structure_names(content, set())
            self._predeclare_structure_names(content)
            content = self._normalize_struct_instance_rows(content)
            result = self.parse_text(content, file_name=file_name)
            self.process_ast(content, result)
        finally:
            self.itislst = previous_itislst

    def _switch_file_context(self, file_name: str) -> tuple[str, str]:
        previous = (self._current_file, self.__current_file_hash)
        self._current_file = file_name
        self.__current_file_hash = hashlib.blake2s(os.path.basename(file_name).encode("utf8")).hexdigest()
        return previous

    def _read_whole_file(self, file_name: str) -> str:
        from . import utils

        try:
            mtime = os.path.getmtime(file_name)
        except OSError:
            return utils.read_whole_file(file_name)

        cache_entry = self.__class__._file_cache.get(file_name)
        if cache_entry and cache_entry[0] == mtime:
            return cache_entry[1]

        content = utils.read_whole_file(file_name)
        self.__class__._file_cache[file_name] = (mtime, content)
        return content

    def is_known_macro(self, name: str) -> bool:
        return name in self.macroses

    def declare_structure_name(self, name: str) -> None:
        key = name.lower()
        if key not in self.structures:
            self.structures[key] = Struct("", "")

    def declare_record_name(self, name: str) -> None:
        self.record_names.add(name.lower())

    def declare_record_definition(self, name: str, widths: list[int]) -> None:
        self.declare_record_name(name)
        self.record_defs[name.lower()] = widths

    def match_known_record_name(self, name: str) -> bool:
        return name.lower() in self.record_names

    def has_structure(self, name: str) -> bool:
        return name.lower() in self.structures

    def has_any_structures(self) -> bool:
        return bool(self.structures)

    def match_known_structure_name(self, name: str) -> str | None:
        candidate = name.lower()
        return candidate if self.has_structure(candidate) else None

    def struct_size_hint_for_label(self, label: str) -> int | None:
        structure_name = self.match_known_structure_name(label)
        if structure_name is None:
            return None
        return self.structures[structure_name].size

    def is_lst_mode(self) -> bool:
        return self.itislst

    def is_listing_source(self) -> bool:
        return self.source_is_lst or self.itislst

    def parse_numeric_value(self, value: str) -> int:
        return Parser.parse_int(value)

    def set_radix(self, radix: int) -> None:
        if 2 <= radix <= 16:
            self.radix = radix
        else:
            raise ValueError(f"Invalid radix {radix}; expected 2..16")

    def evaluate_repeat_count(self, repeat_expression: Expression) -> int:
        repeat = self._resolve_assignment_symbols(copy(repeat_expression), resolve_equ=True)
        repeat.indirection = IndirectionType.VALUE
        try:
            return self.eval_expression_to_int(repeat)
        except Exception:
            return 0

    def normalize_label(self, name: str | lark.Token) -> str:
        return Parser.mangle_label(name)

    def register_size(self, expr: lark.Token | str) -> int:
        return Parser.is_register(expr)

    def sizeof_type(self, value_in: str | Token_) -> int:
        return self.typetosize(value_in)

    def resolve_include_path(self, include_name: str) -> str:
        include_norm = include_name.strip().strip('"').strip("'").replace("\\", os.sep)
        drive_rooted = re.match(r"^[A-Za-z]:[/\\\\]", include_norm) is not None
        if drive_rooted:
            include_norm = re.sub(r"^[A-Za-z]:[/\\\\]", "", include_norm, count=1)
        current_dir = os.path.dirname(os.path.realpath(self._current_file))
        relative_tail = include_norm.lstrip("/\\")

        direct = os.path.normpath(
            os.path.join(
                current_dir,
                relative_tail if include_norm.startswith(("/", "\\")) or drive_rooted else include_norm,
            ),
        )
        if os.path.exists(direct):
            return direct

        probe_dir = current_dir
        while True:
            candidate = os.path.normpath(os.path.join(probe_dir, relative_tail))
            if os.path.exists(candidate):
                return candidate
            parent = os.path.dirname(probe_dir)
            if parent == probe_dir:
                break
            probe_dir = parent

        return direct

    def parse_include_directive(self, include_name: str):
        fullpath = self.resolve_include_path(include_name)
        return self.parse_include_file_lines(fullpath)

    def apply_offset_directive(self, directive: str, value: str) -> None:
        if directive == "align":
            self.align(self.parse_numeric_value(value))
        elif directive == "even":
            self.align(2)
        elif directive == "org":
            self.org(self.parse_numeric_value(value))

    def apply_option_directive(self, options: list[str]) -> None:
        for option in options:
            normalized = option.lower()
            if normalized in {"m510", "oldstructs", "noscoped"}:
                self.old_struct_fields = True
            elif normalized in {"nom510", "nooldstructs", "scoped"}:
                self.old_struct_fields = False

    def dispatch_instruction(self, instruction: str, args: list[Any], *, raw: str, line_number: int):
        comment = self.consume_pending_source_comment()
        if comment and comment not in raw:
            raw = f"{raw} {comment}" if comment.startswith(";") else f"{raw} ; {comment}"
        return self.action_instruction(instruction, args, raw=raw, line_number=line_number)

    def finish_program(self, entry_label: str) -> None:
        self.action_end(entry_label)

    def begin_procedure(self, name: str, proc_type: list[str], *, line_number: int, raw: str) -> None:
        self.action_proc(name, proc_type, line_number=line_number, raw=raw)

    def end_procedure(self) -> None:
        self.action_endp()

    def begin_simple_segment(self, segtype: str) -> None:
        self.action_simplesegment(segtype, None)

    def begin_named_segment(self, name: str, *, options: set[str], segclass: str | None, raw: str):
        return self.create_segment(name, options=options, segclass=segclass, raw=raw)

    def end_current_scope(self) -> None:
        self.action_ends()

    def define_label(self, name: str, *, raw: str, line_number: int, globl: bool=True) -> None:
        self.action_label(name, isproc=False, raw=raw, line_number=line_number, globl=globl)

    def declare_external_symbol(self, label: str, symbol_type: Token | str) -> None:
        self.add_extern(label, symbol_type)

    def declare_public_symbols(self, labels: list[str]) -> None:
        self.public_symbols.update(self.mangle_label(label) for label in labels)

    def define_equ(self, label: str, value: Expression | str, *, raw: str, line_number: int):
        return self.action_equ(label, value, raw=raw, line_number=line_number)

    def define_assignment(self, label: str, value: Expression, *, raw: str, line_number: int):
        return self.action_assign(label, value, raw=raw, line_number=line_number)

    def define_struct_instance(self, label: str, struct_type: str, args: list[Any], *, raw: str) -> None:
        self.add_structinstance(label.lower(), struct_type.lower(), args, raw=raw)

    def define_data(self, label: str, data_type: str, values: Tree, *, is_string: bool, raw: str, line_number: int):
        return self.datadir_action(label, data_type, values, is_string=is_string, raw=raw, line_number=line_number)

    def define_data_alias(self, label: str, data_type: str, *, raw: str, line_number: int) -> op.var:
        self.adjust_offset_to_real(raw, label)
        label = self.mangle_label(label)
        data_type = data_type.lower()
        alias = op.var(
            self.typetosize(data_type),
            self.__cur_seg_offset,
            name=label,
            segment=self.__segment_name,
            elements=1,
            original_type=data_type,
            filename=self._current_file,
            raw=raw,
            line_number=line_number,
        )
        self.symbols.set_global(label, alias)
        self.data_aliases.append(alias)
        return alias

    def set_pending_proc_options(self, options: list[str]) -> None:
        self._pending.proc_options = list(options)

    def consume_pending_proc_options(self) -> list[str]:
        options = self._pending.proc_options
        self._pending.proc_options = []
        return options

    # Backward-compatible alias for older call sites.
    def consume_proc_options(self) -> list[str]:
        return self.consume_pending_proc_options()

    def prepare_instruction_args(self, instruction: str, args: list[Any]) -> list[Any]:
        if len(args) >= 2 and isinstance(args[0], Expression):
            args[0].mods.add("destination")
        if instruction == "lea":
            for arg in args:
                if isinstance(arg, Expression):
                    arg.mods.add("lea")
        return args

    def set_pending_mnemonic(self, mnemonic: str) -> None:
        self._pending.mnemonic = mnemonic

    def consume_pending_mnemonic(self) -> str:
        mnemonic = self._pending.mnemonic
        self._pending.mnemonic = ""
        return mnemonic

    def resolve_label_for_expression(self, value_in: Token | str, expr: Expression) -> str:
        value = self.normalize_label(value_in)
        if g := self.lookup_global_symbol(value):
            from masm2c.proc import Proc
            from .enumeration import IndirectionType
            if isinstance(g, (op._equ, op._assignment)):
                if isinstance(g.value, Expression):
                    g.size = g.value.size()
                    if (
                        len(g.children) == 2
                        and isinstance(g.children[1], Expression)
                        and g.children[1].indirection == IndirectionType.POINTER
                    ):
                        expr.ptr_size = g.size
                    else:
                        expr.element_size = g.size
            elif isinstance(g, (Proc, op.label, op.var)):
                pass
            elif isinstance(g, op.Struct):
                expr.element_size = g.size
        elif self.has_structure(value):
            expr.element_size = self.structures[value].size
        return value

    def apply_register_reference(self, expr: Expression, register_name: str) -> None:
        reg = register_name.lower()
        expr.element_size = self.register_size(reg)
        expr.registers.add(reg)

    def apply_segment_register_reference(self, expr: Expression, register_name: str) -> None:
        reg = register_name.lower()
        expr.element_size = self.register_size(reg)
        expr.segment_register = reg

    def set_pending_source_comment(self, text: str) -> None:
        self._pending.source_comment = text.strip()

    def consume_pending_source_comment(self) -> str:
        text = self._pending.source_comment
        self._pending.source_comment = ""
        return text

    def flush_pending_source_comment(self, *, line_number: int=0) -> None:
        text = self.consume_pending_source_comment()
        if not text:
            return
        self.make_sure_proc_exists(line_number, text)
        assert self.proc
        o = op._instruction0([])
        o.cmd = ""
        o.filename = self._current_file
        o.raw_line = text
        o.line_number = line_number
        o.syntetic = True
        if self.current_macro:
            self.current_macro.instructions.append(o)
        else:
            self.proc.stmts.append(o)

    def lookup_global_symbol(self, name: str):
        return self.symbols.get_and_mark_global(name)

    def lookup_mangled_symbol(self, name: str):
        return self.lookup_global_symbol(self.mangle_label(name))

    def append_current_statement(self, statement: Any) -> None:
        assert self.proc is not None
        self.proc.stmts.append(statement)

    def append_current_statements(self, statements: list[Any]) -> None:
        assert self.proc is not None
        self.proc.stmts += statements

    def begin_structure_definition(self, name: str, type_name: str) -> None:
        key = name.lower()
        self.current_struct = op.Struct(key, type_name.lower())
        self.struct_names_stack.append(key)

    def begin_named_macro(self, name: str, parameters: list[str]) -> None:
        macro_name = name.lower()
        self.begin_macro_definition(macro_name, Macro(macro_name, parameters))

    def begin_repeat_macro(self, repeat: int) -> None:
        self.begin_macro_definition("", Macro("", [], repeat))

    def begin_macro_definition(self, name: str, macro: Any) -> None:
        self.current_macro = macro
        self.macro_names_stack.append(name)

    def end_macro_definition(self) -> str:
        name = self.macro_names_stack.pop()
        self.macroses[name] = self.current_macro
        self.current_macro = None
        return name

    def get_macro(self, name: str) -> Any:
        return self.macroses[name]

    def extract_addresses_from_lst(self, file_name, content):
        self.itislst = True
        self.source_is_lst = True
        segmap = self.read_segments_map(file_name)
        # MASM listings include banner/page headers that are not source code.
        # Keep them as comments so line numbering and later diagnostics stay stable.
        content = re.sub(
            r"(?m)^\s*(Microsoft \(R\) Macro Assembler[^\r\n]*)$",
            lambda m: f"; {m.group(1)}",
            content,
        )
        content = re.sub(
            r"(?m)^([^\t;\r\n].*Page\s+\d+\s*-\s*\d+)\s*$",
            lambda m: f"; {m.group(1)}",
            content,
        )
        # Remove MASM listing location/object columns.
        content = re.sub(r"(?m)^\s*=\s*[+-]?[0-9A-F]{1,8}\s+", "", content)
        content = re.sub(r"(?m)^\s*=\s*[A-Za-z_@$?.][A-Za-z0-9_@$?.]*\s+", "", content)
        content = re.sub(
            r"(?m)^\s*[0-9A-F]{4,8}(?:\s+(?!(?:DB|DW|DD|DQ|DT)\b)[0-9A-F]{2,8}/?)*(?:\s+[A-Za-z])?\s+",
            "",
            content,
        )
        content = re.sub(r"(?m)^\s*[0-9A-F]{2}:\s+(?:[0-9A-F]{2}\s+)+", "", content)
        content = re.sub(r"(?m)^\s*----(?:\s+[0-9A-F]{1,8})?(?:\s+[A-Za-z])?\s+", "", content)
        content = re.sub(r"(?m)^\s*[0-9A-F]{1,8}\s+[A-Za-z]\s+(?=[A-Za-z_@$?.]|@@)", "", content)
        content = re.sub(r"(?m)^\s*[\[\]]\s*$", "", content)
        content = re.sub(r"(?m)^\s*\[\s*(?=[A-Za-z_@$?.]|DB\b|DW\b|DD\b|DQ\b|DT\b)", "", content)
        content = re.sub(r"(?m)^\s*[0-9A-F]{2}(?:\s+[0-9A-F]{2})*\s*$", "", content)
        content = re.sub(r"(?m)^\s*[0-9A-F]{2}\s+(?=[a-z][A-Za-z0-9_@$?.]*\b)", "", content)
        content = re.sub(r"(?m)^\s*[0-9A-F]{2}\s+(?=[A-Za-z_@$?][A-Za-z0-9_@$?.]*:)", "", content)
        content = re.sub(
            r"(?m)^\s*\d+\s+(?=(?:@@|[A-Za-z_@$?.][A-Za-z0-9_@$?.]*:?))",
            "",
            content,
        )
        content = re.sub(r"(?m)^C\s+", "", content)
        content = re.sub(r"(?m)^\s*[A-Z]\s+(?=[A-Za-z_@$?.;])", "", content)
        content = re.sub(r"(?m)^C\s+(?=;)", "", content)
        if end_match := re.search(r"(?mi)^\s*END\b[^\r\n]*", content):
            end_pos = end_match.end()
            content = content[:end_pos] + "\n"
        # Remove structs addresses
        content = re.sub(r"(?m)^[0-9A-F]{8}(?=\s)\s?", "", content)
        # Move current CS:IP to the end of the string
        content = re.sub(r"^(?P<segment>[_0-9A-Za-z]+):(?P<offset>[0-9A-Fa-f]{4,8})(?P<remain>.*)",
                         lambda m: f'{m.group("remain")} ;~ {segmap.get(m.group("segment"))}:{m.group("offset")}',
                         content, flags=re.MULTILINE)
        content = re.sub(r"(?m)^C\s+(?=[A-Za-z_@$?.;])", "", content)
        content = re.sub(r"<([A-Za-z0-9_@$?.]+)>", r"<\1 >", content)
        return content

    def read_segments_map(self, file_name):
        """It reads a .map file and returns a dictionary of segments.

        :param file_name: The name of the .map file
        :return: A dictionary of segments and their values.
        """
        map_file = re.sub(r"\.lst$", ".map", file_name, flags=re.I)
        loadsegment = self.args.get("loadsegment", "0x1a2")
        if isinstance(loadsegment, int):
            DOSBOX_START_SEG = loadsegment
        elif loadsegment is None:
            DOSBOX_START_SEG = 0x1A2
        else:
            DOSBOX_START_SEG = int(loadsegment, 0)
        if not os.path.exists(map_file):
            logging.warning("Map file %s was not found; keeping lst offsets without segment remap", map_file)
            return OrderedDict()
        content = self._read_whole_file(map_file).splitlines()
        strgenerator = iter(content)
        segs = OrderedDict()
        for line in strgenerator:
            if line.strip() == "Start  Stop   Length Name               Class":  # IDA Pro .lst magic
                break
        # Reads text until the end of the block:
        for line in strgenerator:  # This keeps reading the file
            try:
                if line.strip() == "Address         Publics by Value":
                    break
                if line.strip():
                    m = re.match(
                        r"^\s+(?P<start>[0-9A-F]{5,10})H [0-9A-F]{5,10}H [0-9A-F]{5,10}H (?P<segment>[_0-9A-Za-z]+)\s+",
                        line)
                    segs[m["segment"]] = f"{int(m['start'], 16) // 16 + DOSBOX_START_SEG:04X}"
            except Exception as ex:
                print("read_segments_map Exception", ex, map_file, line)
                raise

        logging.debug("Results of loading .map file: %s", segs)
        return segs

    def parse_include_file_lines(self, file_name):
        def _parse() -> list[Any]:
            content = self._read_whole_file(file_name)
            return self.parse_file_inside(content, file_name=file_name)
        return self._run_with_file_context(file_name, _parse)

    def _run_with_file_context(self, file_name: str, action: Callable[[], Any]) -> Any:
        previous = self._switch_file_context(file_name)
        try:
            return action()
        finally:
            self._current_file, self.__current_file_hash = previous

    def _run_in_transient_test_parse_state(self, action: Callable[[], Any]) -> Any:
        previous_test_mode = self.test_mode
        previous_segments = self.segments
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            return action()
        finally:
            self.test_mode = previous_test_mode
            self.segments = previous_segments

    def action_assign(self, label: Token | str, value: Expression, raw: str="", line_number: int=0) -> _assignment:
        """This function is called when the parser encounters an assignment statement
        It creates an assignment operation, and then appends it to the list of statements.

        :param label: the name of the variable
        :param value: The value to assign to the label
        :param raw: the raw line of code
        :param line_number: The line number of the assignment statement, defaults to 0 (optional)
        :return: The assignment operation.
        """
        label = self.mangle_label(label)
        value = self._resolve_assignment_symbols(value)
        self._preserve_assignment_ptr_metadata(value, raw)

        # if self.has_global(label):
        assert self.proc
        o = self.proc.create_assignment_op(label, value, line_number=line_number)
        o.filename = self._current_file
        o.raw_line = raw.rstrip()
        self.symbols.reset_global(label, o)
        self.proc.stmts.append(o)
        self.equs.add(label)
        return o

    def _preserve_assignment_ptr_metadata(self, value: Expression, raw: str) -> None:
        if value.ptr_size or value.original_type:
            return
        match = re.search(r"\b(?P<type>[A-Za-z_][A-Za-z0-9_]*)\s+PTR\b", raw, flags=re.IGNORECASE)
        if not match:
            return
        pointer_type = self.mangle_label(match.group("type"))
        value.original_type = pointer_type
        value.indirection = IndirectionType.POINTER
        value.mods.add("size_changed")
        if pointer_type in self.structures:
            return
        try:
            value.ptr_size = self.typetosize(pointer_type)
        except Exception:
            value.ptr_size = 0

    def _resolve_assignment_symbols(self, value: Any, seen: set[str] | None = None, *, resolve_equ: bool = False) -> Any:
        seen = seen or set()
        if isinstance(value, Token) and value.type == "LABEL":
            name = self.mangle_label(value)
            if name in seen:
                return value
            symbol = self.symbols.get_global(name)
            if isinstance(symbol, op._assignment) or (
                resolve_equ and isinstance(symbol, op._equ) and isinstance(symbol.value, Expression)
            ):
                return self._resolve_assignment_symbols(deepcopy(symbol.value), seen | {name}, resolve_equ=resolve_equ)
            return value
        if isinstance(value, Tree):
            resolved = deepcopy(value)
            resolved.children = [
                self._resolve_assignment_symbols(child, seen, resolve_equ=resolve_equ) for child in resolved.children
            ]
            return resolved
        if isinstance(value, list):
            return [self._resolve_assignment_symbols(child, seen, resolve_equ=resolve_equ) for child in value]
        return value

    def action_assign_test(self, label: str="", value: str="", line_number: int=0) -> None:
        raw = value
        result = self.parse_text(value, start_rule="expr")
        value_tree = self.process_ast(value, result)
        assert isinstance(value_tree, Expression)
        o = self.action_assign(label, value_tree, raw, line_number)
        o.implemented = True

    def action_equ_test(self, label: str="", value: str="", raw: str="", line_number: int=0) -> None:
        result = self.parse_text(value, start_rule="equtype")
        value_tree = self.process_ast(value, result)
        assert isinstance(value_tree, Expression)
        o = self.action_equ(label, value_tree, raw, line_number)
        o.implemented = True

    def return_empty(self, _):
        return []

    def action_equ(self, label: str="", value: Expression | str="", raw: str="", line_number: int=0) -> _equ:
        from .enumeration import IndirectionType
        label = self.mangle_label(label)
        size = value.size() if isinstance(value, Expression) else 0

        o = Proc.create_equ_op(label, value, line_number=line_number)
        o.filename = self._current_file
        o.raw_line = raw.rstrip()
        o.element_size = size
        if isinstance(value, Expression) and value.indirection == IndirectionType.POINTER:
            o.original_type = value.original_type
        existing = self.symbols.get_global(label)
        if self.itislst and self.pass_number == 1 and existing is not None:
            self.symbols.reset_global(label, o)
        elif self.pass_number == 1 and isinstance(existing, op._equ):
            self.symbols.reset_global(label, o)
        else:
            self.symbols.set_global(label, o)
        self.equs.add(label)
        proc = self.symbols.get_and_mark_global("mainproc")
        proc.stmts.append(o)
        return o

    def create_segment(self, name, options=None, segclass=None, raw=""):
        logging.info("     Found segment %s", name)
        name = name.lower()
        self.data_merge_candidates = 0
        self.__segment_name = name
        if name in self.segments:
            self.__segment = self.segments[name]
        else:
            _, real_offset, real_seg = self.get_lst_offsets(raw)
            if real_seg:
                self.move_offset(real_seg * 0x10, raw)
            self.align()
            self.__cur_seg_offset = 0
            if real_offset:
                self.__cur_seg_offset = real_offset

            offset = real_seg * 16 if real_seg else self.__binary_data_size
            logging.debug("segment %s %x", name, offset)
            binary_width = 0

            self.__segment = op.Segment(name, offset, options=options, segclass=segclass)
            self.segments[name] = self.__segment

            self.symbols.set_global(name, op.var(binary_width, offset, name, issegment=True))
        return self.__segment

    def action_proc(self, name, type, line_number=0, raw=""):
        logging.info("      Found proc %s", name)
        self.action_endp()
        name = self.mangle_label(name)
        far = False
        for i in type:
            if i and i.lower() == "far":
                far = True
                break

        self.proc = self.add_proc(name, raw, line_number, far)

    def add_proc(self, name: str, raw: str, line_number: int, far: bool) -> Proc:
        if self.args.get("mergeprocs") == "separate":
            self.need_label = False
        # if self.__separate_proc:
        offset, real_offset, real_seg = self.get_lst_offsets(raw)
        if real_seg:
            self.procs_start.discard(real_seg * 0x10 + real_offset)
        proc = Proc(name, far=far, line_number=line_number, offset=offset,
                    real_offset=real_offset, real_seg=real_seg,
                    segment=self.__segment.name)
        self.proc_list.append(name)
        existing = self.symbols.get_global(name)
        if self.itislst and self.pass_number == 1 and isinstance(existing, op.label):
            # IDA listings commonly emit a public/global label immediately before
            # the real PROC header for the same symbol.
            self.symbols.reset_global(name, proc)
        else:
            self.symbols.set_global(name, proc)
        self.__proc_stack.append(proc)
        return proc

    def action_simplesegment(self, type, name):
        if name is None:
            name = ""
        else:
            type += "_"
        type = type[1:] + name
        self.create_segment(type)

    """
    def action_prefix(self, line):
        cmd = line.split()
        cmd0 = str(cmd[0])
        cmd0l = cmd0.lower()

        o = self.proc.action_instruction(cmd0l)
        o.line = cmd0l
        o.line_number = self.line_number
        self.proc.stmts.append(o)

        o = self.proc.action_instruction(" ".join(cmd[1:]))
        o.line = " ".join(cmd[1:])
        o.line_number = self.line_number
        self.proc.stmts.append(o)
    """

    def action_endseg(self):
        logging.debug("segment %s ends", self.__segment_name)
        self.__segment_name = "default_seg"

    def action_include(self, name):
        logging.info("including %s", name)
        self.parse_file(name)

    def action_endp(self):
        if self.proc and not self.test_mode:
            if self.__proc_stack:
                self.__proc_stack.pop()
            self.proc = None
        """ Support code outside procs
        if self.__proc_stack:
            self.proc = self.__proc_stack[-1]
        else:
            self.proc = None

    def action_endif(self):
        self.pop_if()

    def action_else(self):
        self.push_else()

    def action_if(self, line):
        cmd = line.split()
        self.push_if(cmd[1])
    """

    def action_code(self, line: str) -> baseop:
        previous_need_label = self.need_label
        self.need_label = False
        try:
            def _parse_instruction() -> baseop:
                self.test_pre_parse()
                result = self.parse_text(line + "\n", start_rule="instruction")
                result = self.process_ast(line, result)
                assert isinstance(result, baseop)
                return result
            try:
                return self._run_in_transient_test_parse_state(_parse_instruction)
            except Exception as e:
                print(e)
                logging.exception("Error1")
                raise
        finally:
            self.need_label = previous_need_label

    def test_size(self, line):
        def _parse_size() -> int:
            try:
                self.test_pre_parse()
                result = self.parse_text(line, start_rule="expr")
                expr = self.process_ast(line, result)
                assert isinstance(expr, Expression)
                return expr.size()
            except Exception as e:
                print(e)
                import traceback
                logging.exception(traceback.format_exc())
                raise
        return self._run_in_transient_test_parse_state(_parse_size)

    def action_data(self, line: str) -> Tree:
        """For tests only."""
        def _parse_data() -> Tree:
            try:
                self.test_pre_parse()
                result = self.parse_text(line + "\n", start_rule="insegdirlist")
                result = self.process_ast(line, result)
                assert isinstance(result, lark.Tree)
                return result
            except Exception as e:
                print(e)
                logging.exception("Error3")
                raise
        return self._run_in_transient_test_parse_state(_parse_data)

    def parse_arg(self, line: str, def_size: int=0, destination: bool=False) -> str:
        def _parse_arg() -> str:
            try:
                self.test_pre_parse()
                expr = self.parse_text(line, start_rule="expr")
                expr = self.process_ast(line, expr)
                assert isinstance(expr, Expression)
                return self.render_expression(expr, def_size=def_size, destination=destination)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                assert exc_tb
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(e, exc_type, fname, exc_tb.tb_lineno)
                import logging
                import traceback

                logging.exception(traceback.format_exc())
                raise
        return self._run_in_transient_test_parse_state(_parse_arg)

    def parse_include(self, line, file_name=None):
        return self.parse_text(line, file_name=file_name, start_rule="insegdirlist")

    def render_expression(self, expr: Expression, def_size: int=0, destination: bool=False) -> str:
        renderer_factory = self.arg_renderer_factory
        if renderer_factory is None:
            from .cpp import Cpp
            renderer_factory = Cpp
        return renderer_factory(self).render_instruction_argument(expr, def_size=def_size, destination=destination)

    def eval_expression_to_int(self, expr: Expression) -> int:
        evaluator = self.expr_int_evaluator
        if evaluator is not None:
            return int(evaluator(self, expr))
        rendered = self.render_expression(expr)
        try:
            return int(literal_eval(rendered))
        except (SyntaxError, ValueError):
            return Parser._eval_int_expression(rendered)



    def datadir_action(self, label: str, type: str, args: Tree, is_string: bool=False, raw: str="", line_number: int=0) -> Data | list:
        if self.__cur_seg_offset > 0xffff:
            return []
        if self.__cur_seg_offset & 0xff == 0:
            logging.info(f"      Current offset {self.__cur_seg_offset:x} line={line_number}")
        isstruct = len(self.struct_names_stack) != 0

        binary_width, size, elements = self._compute_data_layout(type, args)

        offset = self.__cur_seg_offset
        if not isstruct:
            self._prepare_nonstruct_data_context(raw, label, line_number, args)
            offset = self.__cur_seg_offset

        logging.debug("convert_data %s %d %s", label, binary_width, args)

        data_internal_type = self.identify_data_internal_type(args, elements, is_string)
        array = AsmData2IR().visit(args)
        array = self._resolve_assignment_symbols(array)
        if data_internal_type == op.DataType.ARRAY and not any(array) and not isstruct:  # all zeros
            array = [0]

        logging.debug("~size %d elements %d", binary_width, elements)
        self._register_data_symbol_if_needed(label, isstruct, binary_width, offset, type, elements, raw, line_number)

        dummy_label = False
        if not label:
            dummy_label = True
            label = self.get_dummy_label(line_number)

        if isstruct:
            data_type = "struct data"
        else:
            self.__binary_data_size += size
            self.__cur_seg_offset += size
            data_type = "usual data"
        data = op.Data(label, type, data_internal_type, array, elements, size, filename=self._current_file,
                       raw_line=raw,
                       line_number=line_number, comment=data_type, offset=offset)
        self._append_data_record(data, isstruct, raw, dummy_label, data_internal_type, binary_width)

        self.flow_terminated = True
        return data  # c, h, size

    def _compute_data_layout(self, data_type: str, args: Tree) -> tuple[int, int, int]:
        binary_width = self.typetosize(data_type)
        calc = ExprSizeCalculator(element_size=binary_width, init=Vector(0, 0), context=self)
        size, elements = calc.visit(args).values
        if size == 0:
            size = binary_width * elements
        return binary_width, size, elements

    def _prepare_nonstruct_data_context(self, raw: str, label: str, line_number: int, args: Tree) -> None:
        self.adjust_offset_to_real(raw, label)
        if not self.flow_terminated:
            logging.error(f"Flow wasn't terminated! line={line_number} offset={self.__cur_seg_offset}")
        logging.debug("args %s offset %d", args, self.__cur_seg_offset)

    def _register_data_symbol_if_needed(
            self,
            label: str,
            isstruct: bool,
            binary_width: int,
            offset: int,
            data_type: str,
            elements: int,
            raw: str,
            line_number: int,
    ) -> None:
        if not label or isstruct:
            return
        symbol = op.var(
            binary_width,
            offset,
            name=label,
            segment=self.__segment_name,
            elements=elements,
            original_type=data_type,
            filename=self._current_file,
            raw=raw,
            line_number=line_number,
        )
        existing = self.symbols.get_global(label)
        if self.itislst and self.pass_number == 1 and isinstance(existing, (op._assignment, op._equ)):
            self.symbols.reset_global(label, symbol)
            return
        self.symbols.set_global(label, symbol)

    def _append_data_record(
            self,
            data: Data,
            isstruct: bool,
            raw: str,
            dummy_label: bool,
            data_internal_type: op.DataType,
            binary_width: int,
    ) -> None:
        if isstruct:
            assert self.current_struct
            self._remember_old_struct_member_offset(data)
            self.current_struct.append(data)
            return
        _, data.real_offset, data.real_seg = self.get_lst_offsets(raw)
        self._attach_runtime_data_metadata(data)
        self.__segment.append(data)
        if dummy_label and data_internal_type == op.DataType.NUMBER and binary_width == 1:
            self.merge_data_bytes()
        else:
            self.data_merge_candidates = 0

    def _runtime_linear_for_data(self, data: Data) -> int | None:
        if data.real_seg is not None and data.real_offset is not None:
            return data.real_seg * 0x10 + data.real_offset
        if self.__segment is None:
            return None
        return self.__segment.offset + data.offset

    def _attach_runtime_data_metadata(self, data: Data) -> None:
        linear = self._runtime_linear_for_data(data)
        if linear is None:
            return
        data.runtime_linear_addr = linear  # type: ignore[attr-defined]
        data.runtime_data_meta = self.runtime_data_meta.get(linear)  # type: ignore[attr-defined]
        data.runtime_pointer_meta = self.runtime_pointer_meta.get(linear, [])  # type: ignore[attr-defined]

    def merge_data_bytes(self) -> None:
        self.data_merge_candidates += 1
        size = 32
        if self.data_merge_candidates != size:
            return

        if self.__segment.getdata()[-size].offset + size - 1 != self.__segment.getdata()[-1].offset:
            logging.debug(
                "Cannot merge %s - %s", self.__segment.getdata()[-size].label, self.__segment.getdata()[-1].label)
        else:
            logging.debug(
                "Merging data at %s - %s", self.__segment.getdata()[-size].label, self.__segment.getdata()[-1].label)
            array = [x.children[0] for x in self.__segment.getdata()[-size:]]
            if not any(array):  # all zeros
                array = [0]

            self.__segment.getdata()[-size].children = array
            self.__segment.getdata()[-size].elements = size
            self.__segment.getdata()[-size].data_internal_type = op.DataType.ARRAY
            self.__segment.getdata()[-size]._size = size
            self.__segment.setdata(self.__segment.getdata()[:-(size - 1)])

        self.data_merge_candidates = 0

    def _remember_old_struct_member_offset(self, data: Data) -> None:
        if not self.old_struct_fields or not data.label:
            return
        assert self.current_struct
        offset = 0 if self.current_struct.gettype() == op.Struct.UNION else self.current_struct.getsize()
        self.old_struct_member_offsets.setdefault(data.label.lower(), (self.current_struct.name, offset))

    def adjust_offset_to_real(self, raw: str, label: str) -> None:
        absolute_offset, real_offset, _ = self.get_lst_offsets(raw)
        if self.itislst and real_offset and real_offset > 0xffff:  # IDA issue
            return
        if absolute_offset == 0:
            return

        self.move_offset(absolute_offset, raw)
        if self.__cur_seg_offset > real_offset and not self.itislst:
            logging.warning(f"Current offset does not equal to required for {label}")
        if self.__cur_seg_offset != real_offset:
            self.data_merge_candidates = 0
        self.__cur_seg_offset = real_offset

    def get_lst_offsets(self, raw: str) -> tuple[int, int, int]:
        """Get required offsets from .LST file
        :param raw: raw string
        :return: offset from memory begging, offset starting from segment, segment in para.
        """
        real_offset = 0
        absolute_offset = 0
        real_seg = 0
        if self.itislst and (m := re.match(
            r".* ;~ (?P<segment>[0-9A-Fa-f]{4}):(?P<offset>[0-9A-Fa-f]{4})", raw,
        )):
            real_offset = int(m["offset"], 16)
            real_seg = int(m["segment"], 16)
            absolute_offset = real_seg * 0x10 + real_offset
        return absolute_offset, real_offset, real_seg


    def test_pre_parse(self) -> None:
        self.__binary_data_size = 0
        self.__c_dummy_jump_label = 0
        self.__c_extra_dummy_jump_label = 0

    def parse_file_inside(self, text, file_name=None):
        text = self._join_continued_lines(text)
        filtered = self.apply_conditional_assembly(text)
        self._collect_text_macros_from_content(filtered)
        self._preload_text_macros(filtered, set())
        filtered = self._strip_text_macro_definitions(filtered)
        filtered = self._expand_repeat_blocks(filtered)
        filtered = self._expand_text_macros(filtered)
        filtered = self._expand_repeat_blocks(filtered)
        filtered = self._expand_text_equates(filtered)
        filtered = self._trim_trailing_lines_after_end(filtered)
        self._predeclare_included_structure_names(filtered, set())
        self._predeclare_structure_names(filtered)
        filtered = self._normalize_struct_instance_rows(filtered)
        return self.parse_include(filtered, file_name)

    def _preload_text_macros(self, content: str, seen: set[str]) -> None:
        self._collect_text_macros_from_content(content)
        for line in content.splitlines():
            code = line.split(";", 1)[0].strip()
            match = re.match(r"^INCLUDE\s+(.+)$", code, re.IGNORECASE)
            if not match:
                continue
            include_path = self.resolve_include_path(match.group(1).strip())
            if include_path in seen or not os.path.exists(include_path):
                continue
            seen.add(include_path)
            include_content = self.apply_conditional_assembly(self._join_continued_lines(self._read_whole_file(include_path)))
            previous = self._switch_file_context(include_path)
            try:
                self._preload_text_macros(include_content, seen)
            finally:
                self._current_file, self.__current_file_hash = previous

    def _collect_text_macros_from_content(self, content: str) -> None:
        lines = content.splitlines(keepends=True)
        i = 0
        while i < len(lines):
            header = re.match(
                r"^\s*(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s+MACRO\b(?P<params>[^\r\n;]*)",
                lines[i],
                re.IGNORECASE,
            )
            if not header:
                i += 1
                continue
            body: list[str] = []
            i += 1
            depth = 1
            while i < len(lines):
                if self._starts_macro_like_block(lines[i]):
                    depth += 1
                if re.match(r"^\s*ENDM\b", lines[i], re.IGNORECASE):
                    depth -= 1
                    if depth == 0:
                        break
                body.append(lines[i])
                i += 1
            params = [
                param.strip().split(":", 1)[0].split("=", 1)[0].lower()
                for param in header.group("params").split(",")
                if param.strip()
            ]
            self._text_macros[header.group("name").lower()] = _TextMacro(params, body)
            i += 1

    @staticmethod
    def _starts_macro_like_block(line: str) -> bool:
        code = line.split(";", 1)[0].strip()
        return bool(
            re.match(r"^[A-Za-z_@$?][A-Za-z0-9_@$?]*\s+MACRO\b", code, re.IGNORECASE)
            or re.match(r"^(?:REPT|REPEAT|IRP|IRPC|WHILE)\b", code, re.IGNORECASE)
        )

    def _strip_text_macro_definitions(self, content: str) -> str:
        rows: list[str] = []
        lines = content.splitlines(keepends=True)
        i = 0
        while i < len(lines):
            if not re.match(r"^\s*[A-Za-z_@$?][A-Za-z0-9_@$?]*\s+MACRO\b", lines[i], re.IGNORECASE):
                rows.append(lines[i])
                i += 1
                continue
            i += 1
            depth = 1
            while i < len(lines) and depth:
                if self._starts_macro_like_block(lines[i]):
                    depth += 1
                if re.match(r"^\s*ENDM\b", lines[i], re.IGNORECASE):
                    depth -= 1
                i += 1
        return "".join(rows)

    def _expand_repeat_blocks(self, content: str, symbols: dict[str, int] | None = None) -> str:
        rows: list[str] = []
        lines = content.splitlines(keepends=True)
        i = 0
        symbols = symbols if symbols is not None else {}
        while i < len(lines):
            line = lines[i]
            code = line.split(";", 1)[0].strip()
            assignment = re.match(r"^(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s*=\s*(?P<expr>.+)$", code)
            if assignment:
                symbols[assignment.group("name").lower()] = self._eval_repeat_expression(
                    assignment.group("expr"),
                    symbols,
                )
                rows.append(line)
                i += 1
                continue

            repeat = re.match(r"^\s*(?:REPT|REPEAT)\s+(?P<count>[^;\r\n]+)", line, re.IGNORECASE)
            if not repeat:
                rows.append(line)
                i += 1
                continue

            count = max(0, self._eval_repeat_expression(repeat.group("count"), symbols))
            i += 1
            body: list[str] = []
            depth = 1
            while i < len(lines) and depth:
                if re.match(r"^\s*(?:REPT|REPEAT)\b", lines[i], re.IGNORECASE):
                    depth += 1
                if re.match(r"^\s*ENDM\b", lines[i], re.IGNORECASE):
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                if depth:
                    body.append(lines[i])
                i += 1
            for _ in range(count):
                rows.extend(self._expand_repeat_iteration(body, symbols))
        return "".join(rows)

    def _expand_repeat_iteration(self, body: list[str], symbols: dict[str, int]) -> list[str]:
        rows: list[str] = []
        for line in body:
            code = line.split(";", 1)[0].strip()
            assignment = re.match(r"^(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s*=\s*(?P<expr>.+)$", code)
            if assignment:
                symbols[assignment.group("name").lower()] = self._eval_repeat_expression(
                    assignment.group("expr"),
                    symbols,
                )
                continue
            rows.append(self._substitute_repeat_percent_expressions(line, symbols))
        return self._expand_repeat_blocks("".join(rows), symbols).splitlines(keepends=True)

    @staticmethod
    def _substitute_repeat_percent_expressions(line: str, symbols: dict[str, int]) -> str:
        def replace(match: re.Match[str]) -> str:
            return str(symbols.get(match.group("name").lower(), 0))

        return re.sub(r"%(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)", replace, line)

    @staticmethod
    def _eval_repeat_expression(expression: str, symbols: dict[str, int]) -> int:
        rendered = expression
        for name, value in sorted(symbols.items(), key=lambda item: len(item[0]), reverse=True):
            rendered = re.sub(rf"\b{re.escape(name)}\b", str(value), rendered, flags=re.IGNORECASE)
        rendered = rendered.replace("/", "//")
        try:
            return int(eval(rendered, {"__builtins__": {}}, {}))
        except Exception:
            return 0

    def _expand_text_equates(self, content: str) -> str:
        rows: list[str] = []
        for line in content.splitlines(keepends=True):
            body = line[:-1] if line.endswith("\n") else line
            newline = "\n" if line.endswith("\n") else ""
            if self._remember_text_equate_line(body):
                rows.append(line)
                continue

            code, sep, comment = body.partition(";")
            self._forget_shadowed_text_equate(code)
            rows.append(self._substitute_text_equates_in_code(code) + (sep + comment if sep else "") + newline)
        return "".join(rows)

    def _remember_text_equate_line(self, line: str) -> bool:
        match = re.match(
            r"^\s*(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s+EQU\s*<(?P<text>[^<>]*)>\s*(?:;.*)?$",
            line,
            re.IGNORECASE,
        )
        if not match:
            return False
        self._text_equates[match.group("name").lower()] = match.group("text")
        return True

    def _forget_shadowed_text_equate(self, code: str) -> None:
        match = re.match(
            r"^\s*(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s*(?:=\s*|\s+EQU\b)",
            code,
            re.IGNORECASE,
        )
        if match:
            self._text_equates.pop(match.group("name").lower(), None)

    def _substitute_text_equates_in_code(self, code: str) -> str:
        if not self._text_equates:
            return code

        result: list[str] = []
        i = 0
        while i < len(code):
            char = code[i]
            if char in {"'", '"'}:
                end = self._quoted_text_end(code, i)
                result.append(code[i:end])
                i = end
                continue
            match = re.match(r"[A-Za-z_@$?][A-Za-z0-9_@$?]*", code[i:])
            if match:
                token = match.group(0)
                result.append(self._text_equates.get(token.lower(), token))
                i += len(token)
                continue
            result.append(char)
            i += 1
        return "".join(result)

    @staticmethod
    def _quoted_text_end(code: str, start: int) -> int:
        quote = code[start]
        i = start + 1
        while i < len(code):
            if code[i] == quote:
                if i + 1 < len(code) and code[i + 1] == quote:
                    i += 2
                    continue
                return i + 1
            i += 1
        return len(code)

    def _expand_text_macros(self, content: str) -> str:
        expanded = content
        for _ in range(20):
            next_expanded, changed = self._expand_text_macros_once(expanded)
            expanded = next_expanded
            if not changed:
                return expanded
        return expanded

    def _expand_text_macros_once(self, content: str) -> tuple[str, bool]:
        changed = False
        rows: list[str] = []
        lines = content.splitlines(keepends=True)
        i = 0
        while i < len(lines):
            line = lines[i]
            if re.match(r"^\s*[A-Za-z_@$?][A-Za-z0-9_@$?]*\s+MACRO\b", line, re.IGNORECASE):
                rows.append(line)
                i += 1
                while i < len(lines):
                    rows.append(lines[i])
                    if re.match(r"^\s*ENDM\b", lines[i], re.IGNORECASE):
                        i += 1
                        break
                    i += 1
                continue
            code, sep, comment = line.partition(";")
            match = re.match(
                r"^(?P<ws>\s*)(?:(?P<label>(?:@@|[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s*:)\s*)?"
                r"(?P<name>[A-Za-z_@$?][A-Za-z0-9_@$?]*)(?P<args>\b[^\r\n]*)$",
                code,
            )
            if not match:
                rows.append(line)
                i += 1
                continue
            macro = self._text_macros.get(match.group("name").lower())
            if macro is None:
                rows.append(line)
                i += 1
                continue
            if split_lines := self._split_chained_macro_invocation(line, match):
                rows.extend(split_lines)
                changed = True
                i += 1
                continue
            changed = True
            args = self._split_macro_args(match.group("args").strip())
            replacements = dict(zip(macro.parameters, args))
            self._text_macro_expansion_id += 1
            local_replacements = self._local_macro_replacements(macro.body, self._text_macro_expansion_id)
            replacements.update(local_replacements)
            label = (match.group("label") or "").strip().rstrip(":")
            for body_line in macro.body:
                if re.match(r"^\s*LOCAL\b", body_line, re.IGNORECASE):
                    continue
                rendered = self._substitute_text_macro_args(body_line.lstrip(), replacements)
                if label:
                    rows.append(f"{match.group('ws')}{label}:\t{rendered}")
                    label = ""
                else:
                    rows.append(match.group("ws") + rendered)
            if sep and comment.strip():
                rows.append(f"{match.group('ws')};{comment}")
            i += 1
        return "".join(rows), changed

    def _split_chained_macro_invocation(self, line: str, match: re.Match[str]) -> list[str]:
        if not self._text_macros:
            return []
        names = "|".join(re.escape(name) for name in sorted(self._text_macros, key=len, reverse=True))
        split = re.search(rf"\s+\band\b\s+(?=(?:{names})\b)", match.group("args"), re.IGNORECASE)
        if split is None:
            return []
        first_args = match.group("args")[: split.start()].strip()
        rest = match.group("args")[split.end():].strip()
        line_end = "\n" if line.endswith("\n") else ""
        label = f"{match.group('label').strip().rstrip(':')}: " if match.group("label") else ""
        return [
            f"{match.group('ws')}{label}{match.group('name')} {first_args}{line_end}",
            f"{match.group('ws')}{rest}{line_end}",
        ]

    @staticmethod
    def _split_macro_args(text: str) -> list[str]:
        if not text:
            return []
        args: list[str] = []
        current: list[str] = []
        angle_depth = 0
        paren_depth = 0
        for char in text:
            if char == "<":
                angle_depth += 1
            elif char == ">" and angle_depth:
                angle_depth -= 1
            elif char == "(":
                paren_depth += 1
            elif char == ")" and paren_depth:
                paren_depth -= 1
            if char == "," and angle_depth == 0 and paren_depth == 0:
                args.append("".join(current).strip())
                current = []
            else:
                current.append(char)
        args.append("".join(current).strip())
        return args

    @staticmethod
    def _substitute_text_macro_args(line: str, replacements: dict[str, str]) -> str:
        result = line
        for name, value in replacements.items():
            result = re.sub(rf"&{re.escape(name)}\b", value, result, flags=re.IGNORECASE)
            result = re.sub(rf"\b{re.escape(name)}&", value, result, flags=re.IGNORECASE)
            result = re.sub(rf"\b{re.escape(name)}\b", value, result, flags=re.IGNORECASE)
        return result

    @staticmethod
    def _local_macro_replacements(body: list[str], expansion_id: int) -> dict[str, str]:
        replacements: dict[str, str] = {}
        for line in body:
            match = re.match(r"^\s*LOCAL\s+(?P<names>[^;\r\n]+)", line, re.IGNORECASE)
            if not match:
                continue
            for name in match.group("names").split(","):
                local_name = name.strip()
                if local_name:
                    replacements[local_name.lower()] = f"__m2c_macrolocal_{expansion_id}_{local_name.lstrip('_')}"
        return replacements

    def _join_continued_lines(self, content: str) -> str:
        rows: list[str] = []
        pending = ""
        for line in content.splitlines(keepends=True):
            body = line[:-1] if line.endswith("\n") else line
            newline = "\n" if line.endswith("\n") else ""
            code = body.split(";", 1)[0]
            stripped = code.rstrip()
            if stripped.endswith("\\"):
                backslash_index = body.find("\\", len(stripped) - 1)
                pending += body[:backslash_index].rstrip() + " "
                continue
            rows.append(pending + body + newline)
            pending = ""
        if pending:
            rows.append(pending)
        return "".join(rows)

    @staticmethod
    def _trim_trailing_lines_after_end(content: str) -> str:
        lines = content.splitlines(keepends=True)
        last_end_index: int | None = None
        for index, line in enumerate(lines):
            code = line.split(";", 1)[0].replace("\x1a", "").strip()
            if re.match(r"^END(?:\s+.+)?$", code, re.IGNORECASE):
                last_end_index = index
        if last_end_index is None:
            return content
        trailing = lines[last_end_index + 1:]
        if all(not line.split(";", 1)[0].replace("\x1a", "").strip() for line in trailing):
            return "".join(lines[:last_end_index + 1])
        return content

    def _wrap_bare_data_table(self, content: str) -> str:
        code_lines = []
        for line in content.splitlines():
            code = line.split(";", 1)[0].strip()
            if code:
                code_lines.append(code)
        if not code_lines:
            return content
        data_decl_pattern = "|".join(re.escape(name) for name in sorted(_DATA_DECL_NAMES, key=len, reverse=True))
        if not all(re.match(rf"^(?:{data_decl_pattern})\b", line, re.IGNORECASE) for line in code_lines):
            return content
        return f"_DATA segment para public 'DATA'\n{content.rstrip()}\n_DATA ends\nend\n"

    def _predeclare_structure_names(self, content: str) -> None:
        for line in content.splitlines():
            code = line.split(";", 1)[0].strip()
            comment = line.split(";", 1)[1].strip() if ";" in line else ""
            if not code:
                if comment:
                    lst_struct = _REGEX_STRUCT_COMMENT.match(comment)
                    if lst_struct:
                        self.declare_structure_name(lst_struct.group("name"))
                continue
            if hdr := _REGEX_STRUCT_HDR.match(code):
                self.declare_structure_name(hdr.group("name"))
            if record := re.match(
                r"^(?P<name>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+RECORD\b(?P<bits>.*)$",
                code,
                re.IGNORECASE,
            ):
                widths = [
                    int(width)
                    for width in re.findall(r":\s*([0-9]+)", record.group("bits"))
                ]
                self.declare_record_definition(record.group("name"), widths)
            mtch = _REGEX_STRUCT_INSTANCE.match(code)
            if mtch and mtch.group("stype").lower() not in _DATA_DECL_NAMES:
                self.declare_structure_name(mtch.group("stype"))
            simple_mtch = _REGEX_STRUCT_INSTANCE_SIMPLE.match(code)
            if simple_mtch and simple_mtch.group("stype").lower() not in _DATA_DECL_NAMES:
                self.declare_structure_name(simple_mtch.group("stype"))

    def _predeclare_included_structure_names(self, content: str, seen: set[str]) -> None:
        for line in content.splitlines():
            code = line.split(";", 1)[0].strip()
            match = re.match(r"^INCLUDE\s+(.+)$", code, re.IGNORECASE)
            if not match:
                continue
            include_path = self.resolve_include_path(match.group(1).strip())
            if include_path in seen or not os.path.exists(include_path):
                continue
            seen.add(include_path)
            include_content = self._join_continued_lines(self._read_whole_file(include_path))
            include_content = self.apply_conditional_assembly(include_content)
            self._predeclare_structure_names(include_content)
            previous = self._switch_file_context(include_path)
            try:
                self._predeclare_included_structure_names(include_content, seen)
            finally:
                self._current_file, self.__current_file_hash = previous

    def _normalize_struct_instance_rows(self, content: str) -> str:
        rows: list[str] = []
        for line_no, line in enumerate(content.splitlines(keepends=True), start=1):
            code = line.split(";", 1)[0]
            mtch = _REGEX_STRUCT_INSTANCE_LINE.match(code) or _REGEX_STRUCT_DUP_INSTANCE_LINE.match(code)
            if mtch and self.match_known_structure_name(mtch.group("name")):
                prefix = f'{mtch.group("ws")}__m2c_structrow_{self.__current_file_hash[:8]}_{line_no} '
                line = prefix + line[len(mtch.group("ws")):]
            elif record_line := self._rewrite_record_instance_line(line, line_no):
                line = record_line
            rows.append(line)
        return "".join(rows)

    def _rewrite_record_instance_line(self, line: str, line_no: int) -> str:
        code, sep, comment = line.partition(";")
        match = re.match(
            r"^(?P<ws>\s*)(?:(?P<label>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+)?"
            r"(?P<name>[A-Za-z_@$?.][A-Za-z0-9_@$?.]*)\s+(?P<value>.+?)\s*$",
            code,
            re.IGNORECASE,
        )
        if not match or not self.match_known_record_name(match.group("name")):
            return ""
        packed = self._pack_record_value(match.group("name"), match.group("value"))
        if not packed:
            return ""
        label = match.group("label") or f"__m2c_recordrow_{self.__current_file_hash[:8]}_{line_no}"
        suffix = f";{comment}" if sep else ""
        newline = "\n" if line.endswith("\n") else ""
        return f"{match.group('ws')}{label} DB {packed}{suffix}{newline}"

    def _pack_record_value(self, name: str, value: str) -> str:
        dup_match = re.match(r"(?P<count>.+?)\s+DUP\s*\(\s*<(?P<args>.*)>\s*\)\s*$", value, re.IGNORECASE)
        if dup_match:
            packed = self._pack_record_args(name, self._split_macro_args(dup_match.group("args")))
            return f"{dup_match.group('count').strip()} DUP({packed})" if packed else ""
        simple_match = re.match(r"<(?P<args>.*)>\s*$", value)
        if simple_match:
            return self._pack_record_args(name, self._split_macro_args(simple_match.group("args")))
        return ""

    def _pack_record_args(self, name: str, args: list[str]) -> str:
        widths = self.record_defs.get(name.lower())
        if not widths:
            return ""
        padded_args = [*args, *(["0"] * max(0, len(widths) - len(args)))]
        shift = sum(widths)
        parts: list[str] = []
        for width, arg in zip(widths, padded_args):
            shift -= width
            value = arg.strip() or "0"
            if shift:
                parts.append(f"(({value}) * {1 << shift})")
            else:
                parts.append(f"({value})")
        return " + ".join(parts)

    def apply_conditional_assembly(self, content: str) -> str:
        lines = content.splitlines(keepends=True)
        output: list[str] = []
        stack: list[_ConditionalFrame] = []

        for line in lines:
            directive = self._parse_conditional_directive(line)
            if directive is None:
                if all(frame.current_active for frame in stack):
                    output.append(line)
                continue

            keyword, payload = directive
            upper = keyword.upper()
            parent_active = all(frame.current_active for frame in stack)

            if upper in {"IF", "IFE", "IFB", "IFNB", "IFDEF", "IFNDEF", "IFDIF", "IFDIFI", "IFIDN", "IFIDNI", "IF1", "IF2"}:
                cond = self._evaluate_conditional(upper, payload)
                active = parent_active and cond
                stack.append(_ConditionalFrame(parent_active=parent_active, branch_taken=active, current_active=active))
                continue

            if upper.startswith("ELSEIF"):
                if not stack:
                    continue
                frame = stack[-1]
                if not frame.parent_active or frame.branch_taken:
                    frame.current_active = False
                else:
                    base = upper[4:]
                    cond = self._evaluate_conditional(base, payload)
                    frame.current_active = cond
                    frame.branch_taken = cond
                continue

            if upper == "ELSE":
                if not stack:
                    continue
                frame = stack[-1]
                frame.current_active = frame.parent_active and not frame.branch_taken
                frame.branch_taken = True
                continue

            if upper == "ENDIF":
                if stack:
                    stack.pop()
                continue

        return "".join(output)

    def _parse_conditional_directive(self, line: str) -> tuple[str, str] | None:
        code = line.split(";", 1)[0].strip()
        if not code:
            return None
        match = re.match(
            r"^(?:(?:@@|[A-Za-z_@$?][A-Za-z0-9_@$?]*)\s*:\s*)?"
            r"(IF(?:E|B|NB|DEF|NDEF|DIF|DIFI|IDN|IDNI|1|2)?|"
            r"ELSEIF(?:E|B|NB|DEF|NDEF|DIF|DIFI|IDN|IDNI|1|2)?|ELSE|ENDIF)\b(.*)$",
            code,
            re.IGNORECASE,
        )
        if not match:
            return None
        return match.group(1), match.group(2).strip()

    def _evaluate_conditional(self, keyword: str, payload: str) -> bool:
        key = keyword.upper()
        if key == "IF1":
            return self.pass_number == 1
        if key == "IF2":
            return self.pass_number >= 2
        if key in {"IF", "IFE"}:
            expr_val = self._evaluate_conditional_expression(payload)
            return (expr_val != 0) if key == "IF" else (expr_val == 0)
        if key in {"IFDEF", "IFNDEF"}:
            symbol = payload.split()[0] if payload else ""
            defined = bool(symbol) and self.symbols.get_global(symbol.lower()) is not None
            return defined if key == "IFDEF" else not defined
        if key in {"IFB", "IFNB"}:
            text = self._extract_text_item(payload)
            is_blank = text.strip() == ""
            return is_blank if key == "IFB" else not is_blank
        if key in {"IFIDN", "IFIDNI", "IFDIF", "IFDIFI"}:
            left, right = self._extract_text_pair(payload)
            if key in {"IFIDNI", "IFDIFI"}:
                same = left.lower() == right.lower()
            else:
                same = left == right
            return same if key in {"IFIDN", "IFIDNI"} else not same
        return False

    def _extract_text_item(self, payload: str) -> str:
        match = re.search(r"<(.*)>", payload)
        if match:
            return match.group(1).strip()
        return payload.strip()

    def _extract_text_pair(self, payload: str) -> tuple[str, str]:
        m = re.match(r"\s*<(.*?)>\s*,\s*<(.*?)>\s*$", payload)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        parts = [p.strip() for p in payload.split(",", 1)]
        if len(parts) == 2:
            return parts[0], parts[1]
        return payload.strip(), ""

    def _evaluate_conditional_expression(self, payload: str) -> int:
        expr = payload.strip()
        if not expr:
            return 0
        relops = {
            "EQ": "==",
            "NE": "!=",
            "LT": "<",
            "LE": "<=",
            "GT": ">",
            "GE": ">=",
        }
        for old, new in relops.items():
            expr = re.sub(rf"\b{old}\b", new, expr, flags=re.IGNORECASE)
        expr = re.sub(r"\b([01]+)b\b", lambda match: str(int(match.group(1), 2)), expr, flags=re.IGNORECASE)
        expr = re.sub(r"\b([0-9A-F]+)h\b", lambda match: str(int(match.group(1), 16)), expr, flags=re.IGNORECASE)
        expr = re.sub(r"\b[A-Za-z_@$?][A-Za-z0-9_@$?]*\b", "0", expr)
        try:
            return int(bool(eval(expr, {"__builtins__": {}}, {})))
        except Exception:
            return 0

    def parse_text(self, text: str, file_name: str="", start_rule: str="start") -> Tree:
        text = self._normalize_label_alias_directives(text)
        logging.debug("parsing: [%s]", text)
        parser = self._select_parser(start_rule)
        try:
            self.__lex.bind_context(self)
            result = parser.parse(text, start=start_rule)
        except (UnexpectedToken, KeyError, TypeError) as ex:
            if self.__lex.start_parser and parser is not self.__lex.start_parser[0]:
                try:
                    logging.debug("Primary parser failed (%s), retrying with post-lex fallback for start=%s", type(ex).__name__, start_rule)
                    return self.__lex.start_parser[0].parse(text, start=start_rule)
                except Exception as ex_fallback:
                    logging.debug("Post-lex fallback also failed (%s): %s", type(ex_fallback).__name__, ex_fallback)
            if isinstance(ex, UnexpectedToken):
                logging.exception("Parse failure: [%s] line=%s column=%s", ex.token, getattr(ex, "line", "?"), getattr(ex, "column", "?"))
            else:
                logging.exception("Parse failure: %s", ex)
            sys.exit(9)
        return result

    def _select_parser(self, start_rule: str):
        if start_rule == "start" and self.__lex.start_parser:
            return self.__lex.start_parser[0]
        parser_lookup = {
            "expr": self.__lex.expr_parser,
            "instruction": self.__lex.instruction_parser,
            "equtype": self.__lex.equtype_parser,
            "insegdirlist": self.__lex.insegdirlist_parser,
            "_directivelist": self.__lex.directivelist_parser,
        }
        selected = parser_lookup.get(start_rule, self.__lex.parser)
        if selected:
            return selected[0]
        return self.__lex.parser[0]

    @staticmethod
    def _normalize_label_alias_directives(text: str) -> str:
        label = r"[A-Za-z@_$?][A-Za-z@_$?0-9]*"
        pattern = re.compile(
            rf"^(?P<indent>[ \t]*)(?P<name>{label})[ \t]+LABEL[ \t]+(?P<type>[^;\r\n]+?)(?P<comment>[ \t]*;[^\r\n]*)?$",
            re.IGNORECASE | re.MULTILINE,
        )

        def repl(match: re.Match[str]) -> str:
            data_type = match.group("type").strip()
            comment = match.group("comment") or ""
            return f"{match.group('indent')}__MASM2C_LABEL_ALIAS {match.group('name')} {data_type}{comment}"

        return pattern.sub(repl, text)

    def process_ast(self, text: str, result: Tree) -> baseop | Expression | lark.Tree:
        self._include_loader.context = self
        self._asm2ir.context = self
        self._asm2ir.input_str = text
        self._asm2ir._clear_expression()
        result = self._include_loader.transform(result)
        result = self._expr_remover.transform(result)
        """
        for e in self.equs:
            g = self.get_and_mark_global(e)
            if not isinstance(g.value, Expression):
                g.value = self._asm2ir.transform(g.value)
        """
        result = self._asm2ir.transform(result)
        return result

    @staticmethod
    def mangle_label(name: str | lark.Token) -> str:
        name = _token_lower(name)  # ([A-Za-z@_\$\?][A-Za-z0-9@_\$\?]*)
        return avoid_cpp_keyword(name.replace("@", "arb").replace("?", "que").replace("$", "dol"))

    @staticmethod
    def is_register(expr: lark.Token | str) -> int:
        expr = _token_lower(expr)
        size = 0
        if expr in {"al", "bl", "cl", "dl", "ah", "bh", "ch", "dh"}:
            logging.debug("is reg res 1")
            size = 1
        elif expr in {"ax", "bx", "cx", "dx", "si", "di", "sp", "bp", "ds", "cs", "es", "fs", "gs", "ss"}:
            logging.debug("is reg res 2")
            size = 2
        elif expr in {"eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp"}:
            logging.debug("is reg res 4")
            size = 4
        return size

    def typetosize(self, value_in: str | Token_) -> int:
        value = value_in.children if isinstance(value_in, Token_) else value_in
        if not isinstance(value, str):
            logging.error(f"Type is not a string TODO {value!s}")
            return 0
        value = value.lower()
        if value in self.structures and isinstance(self.structures[value], Struct):
            return self.structures[value].getsize()
        try:
            size = {"db": 1, "byte": 1, "sbyte": 1,
                    "dw": 2, "word": 2, "sword": 2, "small": 2, "near": 2,
                    "dd": 4, "dword": 4, "sdword": 4, "large": 4, "far": 4, "real4": 4,
                    "df": 6, "fword": 6,
                    "dq": 8, "qword": 8, "real8": 8,
                    "dt": 10, "tbyte": 10, "real10": 10}[value]
        except KeyError:
            logging.exception("Cannot find size for %s", value)
            size = 0
        return size

    def convert_members(self, data: Data, values: Tree | list[Tree]) -> list[list[int] | Any | int]:
        if data.isobject():
            if isinstance(values, lark.Tree):
                values = values.children
            return [self.convert_members(m, v) for m, v in zip(data.getmembers(), values)]
        """
        type = data.gettype()
        binary_width = self.typetosize(type)
        _, _, array = self.process_data_tokens(values, binary_width)
        """
        return AsmData2IR().visit(values)

    def add_structinstance(self, label: str, type: str, args: list[Any | Tree], raw: str="") -> None:

        if not label:
            label = self.get_dummy_label()

        self.data_merge_candidates = 0
        self.adjust_offset_to_real(raw, label)
        offset = self.__cur_seg_offset

        s = self.structures[type]
        number = 1
        if isinstance(args, list) and len(args) > 2 and isinstance(args[1], str) and args[1] == "dup":
            expr = Token_.find_tokens(args[0],"expr")
            assert isinstance(expr, Expression)
            number = self.eval_expression_to_int(expr)
            args = args[3]
        args = Token_.remove_tokens(args, ["structinstance"])

        d = op.Data(label, type, op.DataType.OBJECT, args, 1, s.getsize(), comment="struct instance", offset=offset)
        members = [deepcopy(i) for i in s.getdata().values()]
        d.setmembers(members)
        args = self.convert_members(d, args)
        d.setvalue(args)

        if number > 1:
            d = op.Data(label, type, op.DataType.ARRAY, number * [d], number, number * s.getsize(),
                        comment="object array",
                        offset=offset)

        isstruct = len(self.struct_names_stack) != 0
        if isstruct:
            assert self.current_struct
            self.current_struct.append(d)
        else:
            self.adjust_offset_to_real(raw, label)
            if label:
                self.symbols.set_global(label,
                                op.var(number * s.getsize(), self.__cur_seg_offset, label, segment=self.__segment_name, \
                                       original_type=type))
            self.__segment.append(d)
            self.__cur_seg_offset += number * s.getsize()
            self.__binary_data_size += number * s.getsize()

    def add_extern(self, label: str, type: Token | str) -> None:
        strtype = self.mangle_label(type)
        if isinstance(type, Token_):
            strtype = str(type.children)
        label = self.mangle_label(label)
        if strtype in {"near", "near16", "near32", "far", "far16", "far32"}:
            far = strtype.startswith("far")
            strtype = "proc"
        else:
            far = False
        if strtype == "abs":
            # MASM ABS externs are absolute symbols, commonly public EQU values
            # from another module. They are not storage and must not link as vars.
            return
        if strtype not in ["proc"]:
            binary_width = self.typetosize(type)
            self.symbols.reset_global(label, op.var(binary_width, 0, name=label, segment=self.__segment_name,
                                            elements=1, external=True, original_type=strtype))
            self.externals_vars.add(label)
        else:  # Proc
            # if self.__separate_proc:
            self.externals_procs.add(label)
            proc = Proc(label, extern=True, far=far)
            logging.debug("procedure %s, extern", label)
            self.symbols.reset_global(label, proc)

    def add_call_to_entrypoint(self):
        """It adds a call to the entry point of the program to the service mainproc."""
        # if self.__separate_proc:
        proc = self.symbols.get_and_mark_global("mainproc")
        result = self.parse_text(self.entry_point, start_rule="expr")
        expr = self.process_ast("", result)

        o = proc.create_instruction_object("call", [expr])
        o.filename = self._current_file
        o.raw_line = ""
        o.line_number = 0
        proc.stmts.append(o)
        o = proc.create_instruction_object("ret")
        o.filename = self._current_file
        o.raw_line = ""
        o.line_number = 0
        proc.stmts.append(o)

    def action_instruction(self, instruction: str, args: list[Expression | Any], raw: str="", line_number: int=0) -> baseop | None:
        self.handle_local_asm_jumps(instruction, args)
        self.make_sure_proc_exists(line_number, raw)
        op = self._build_instruction_op(instruction, args, raw, line_number)
        if op is None:
            return None
        self._update_runtime_label_state(op, raw, line_number)
        self._append_helping_label_if_needed(op, raw)
        self._finalize_instruction_state(op)
        return op

    def _build_instruction_op(
            self,
            instruction: str,
            args: list[Expression | Any],
            raw: str,
            line_number: int,
    ) -> baseop | None:
        assert self.proc
        o = self.proc.create_instruction_object(instruction, args)
        o.filename = self._current_file
        o.raw_line = raw
        o.line_number = line_number

        if self.current_macro:
            self.current_macro.instructions.append(o)
            return None
        return o

    def _update_runtime_label_state(self, o: baseop, raw: str, line_number: int) -> None:
        assert self.proc
        _, o.real_offset, o.real_seg = self.get_lst_offsets(raw)
        self._append_runtime_metadata_comment(o)
        if (
            not self.need_label
            and o.real_seg
            and self.procs_start
            and (o.real_seg * 0x10 + o.real_offset) in self.procs_start
        ):
            logging.warning(
                f"Add a label since run-time info contain flow enter at this address {o.real_seg:x}:{o.real_offset:x} line={line_number}")
            self.need_label = True
        if self.need_label and self.flow_terminated:
            logging.warning(f"Flow terminated and it was no label yet line={line_number}")
            if o.real_seg:
                logging.warning(f"at {o.real_seg:x}:{o.real_offset:x}")

    def _append_runtime_metadata_comment(self, o: baseop) -> None:
        """Attach compact runtime metadata/ABI hints to raw instruction comment."""
        if o.real_seg is None:
            return
        if o.real_offset is None:
            return
        linear = o.real_seg * 0x10 + o.real_offset
        parts: list[str] = []

        code = self.runtime_code_meta.get(linear)
        if code:
            if code.get("Self"):
                parts.append("rt-selfmod")
            accdat = code.get("Accdat", [])
            if isinstance(accdat, list) and accdat:
                parts.append(f"rt-accdat={len(accdat)}")
            size = code.get("Size")
            if size is not None:
                parts.append(f"rt-size={size}")
            modsize = code.get("Modsize")
            if modsize not in (None, 0):
                parts.append(f"rt-mod={modsize}")
            selfvar = code.get("SelfVar", [])
            if selfvar:
                parts.append(f"rt-selfvar={len(selfvar)}")
            edges = code.get("Edges", {})
            if isinstance(edges, dict) and edges:
                edge_kinds = code.get("EdgeKinds", {})
                parts.append(f"rt-edgecnt={len(edges)}")
                edge_samples = []
                for dst, count in sorted(edges.items(), key=lambda item: int(item[1]), reverse=True)[:6]:
                    try:
                        dst_i = self._parse_rt_addr(dst)
                        if dst_i is None:
                            continue
                        count_i = int(count)
                        kinds = edge_kinds.get(dst)
                        if kinds is None and isinstance(edge_kinds, dict):
                            for edge_key, edge_value in edge_kinds.items():
                                edge_key_int = self._parse_rt_addr(edge_key)
                                if edge_key_int == dst_i:
                                    kinds = edge_value
                                    break
                        kinds = self._edge_kind_text(kinds)
                        edge_samples.append(f"{hex(dst_i)}#{count_i}:{kinds}")
                    except Exception:
                        continue
                if edge_samples:
                    parts.append("rt-edges=" + ",".join(edge_samples))

        abi = self.runtime_abi_meta.get(linear)
        if abi and isinstance(abi, dict):
            if abi.get("CallConv"):
                parts.append(f"abi-cc={abi.get('CallConv')}")
            if abi.get("InRegs"):
                parts.append(f"abi-in={abi.get('InRegs')}")
            if abi.get("OutRegs"):
                parts.append(f"abi-out={abi.get('OutRegs')}")
            if abi.get("ArgStack"):
                parts.append(f"abi-args={abi.get('ArgStack')}")
            if abi.get("RetRegs"):
                parts.append(f"abi-ret={abi.get('RetRegs')}")
            if abi.get("Confidence") is not None:
                parts.append(f"abi-conf={abi.get('Confidence')}")
            if abi.get("Calls") is not None:
                parts.append(f"abi-calls={abi.get('Calls')}")
            if abi.get("StackCleanup") not in (None, 0):
                parts.append(f"abi-stackcleanup={abi.get('StackCleanup')}")
            if abi.get("Clobbers"):
                parts.append(f"abi-clob={abi.get('Clobbers')}")
            if abi.get("Preserved"):
                parts.append(f"abi-pres={abi.get('Preserved')}")
            if abi.get("ArgStack") is not None:
                parts.append(f"abi-argstack={abi.get('ArgStack')}")

        sampling = self.runtime_function_sampling_meta.get(linear)
        if sampling and isinstance(sampling, dict):
            calls = sampling.get("Calls")
            sampled = sampling.get("SampledCalls")
            if calls is not None:
                parts.append(f"rt-func-calls={calls}")
            if sampled is not None:
                parts.append(f"rt-func-sampled={sampled}")
            if calls not in (None, 0) and sampled is not None:
                try:
                    parts.append(f"rt-func-ratio={sampled / calls:.4f}")
                except Exception:
                    pass

        if self.runtime_meta_anchor is not None and linear == self.runtime_meta_anchor:
            load_seg = self.runtime_meta.get("DosboxLoadSeg")
            img_size = self.runtime_meta.get("ImageSizeBytes")
            if load_seg is not None:
                parts.append(f"rt-loadseg={load_seg}")
            if img_size is not None:
                parts.append(f"rt-imagesize={img_size}")

        if parts:
            extra = " ;~ " + " ".join(str(p) for p in parts)
            if extra not in o.raw_line:
                o.raw_line = (o.raw_line or "") + extra

    @staticmethod
    def _edge_kind_text(value: Any) -> str:
        try:
            mask = int(value or 0)
        except Exception:
            return "FLOW"
        tags: list[str] = []
        if mask & 1:
            tags.append("JMP")
        if mask & 2:
            tags.append("CALL")
        if mask & 4:
            tags.append("RET")
        if mask & 8:
            tags.append("JCC")
        return "/".join(tags) if tags else "FLOW"

    @staticmethod
    def _parse_rt_addr(value: Any) -> int | None:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value, 0)
            except Exception:
                pass
            try:
                if re.search(r"[a-fA-F]", value):
                    return int(value, 16)
                return int(value)
            except Exception:
                return None
        return None

    def _append_helping_label_if_needed(self, o: baseop, raw: str) -> None:
        assert self.proc
        if self.need_label and self.proc.stmts:
            label_name = f"ret_{o.real_seg:x}_{o.real_offset:x}" if o.real_seg else self.get_extra_dummy_jumplabel()
            logging.warning(f"Adding helping label {label_name}")
            self.action_label(label_name, raw=raw, globl=False)

    def _finalize_instruction_state(self, o: baseop) -> None:
        assert self.proc
        self.proc.stmts.append(o)
        if self.args.get("mergeprocs") == "single":
            self.need_label |= self.proc.is_return_point(o)
        self.flow_terminated = self.proc.is_flow_terminating_stmt(o)
        self.need_label |= self.flow_terminated

        self.collect_labels(self.proc.used_labels, o)

    def handle_local_asm_jumps(self, instruction: str | Token, args: list[Expression | Any]) -> None:
        if (
            (_token_lower(instruction).startswith("j") or _token_lower(instruction).startswith("loop"))
            and len(args) == 1
            and isinstance(args[0], lark.Tree)
            and isinstance(args[0].children, list)
            and _is_token(args[0].children[0])
            and args[0].children[0].type == "LABEL"
        ):
            if _token_lower(args[0].children[0]) == "arbf":  # @f
                args[0].children[0] = f"dummylabel{self.__c_dummy_jump_label + 1!s}"
            elif _token_lower(args[0].children[0]) == "arbb":  # @b
                args[0].children[0] = f"dummylabel{self.__c_dummy_jump_label!s}"

    def collect_labels(self, target: set[str], operation: baseop) -> None:
        for arg in operation.children:
            offset = Token_.find_tokens(arg, "offsetdir") or []
            if offset and not isinstance(offset[0], str):
                offset = []
            labels = (Token_.find_tokens(arg, "LABEL") or []) + offset
            # TODO replace with AST traversing
            #  If it is call to a proc then does not take it into account
            #  TODO: check for calls into middle of proc
            if labels and not operation.cmd.startswith("call") and not (
                    self.args.get("mergeprocs") == "separate" and operation.cmd == "jmp"):
                label = labels[0]
                if label == "dol":
                    continue
                assert isinstance(label, str)
                target.add(self.mangle_label(label))

    def action_ends(self) -> None:
        if len(self.struct_names_stack):  # if it is not a structure then it is end of segment
            name = self.struct_names_stack.pop()
            logging.debug("endstruct %s", name)
            assert self.current_struct
            self.structures[name] = self.current_struct
            existing = self.symbols.get_global(name)
            if self.itislst and self.pass_number == 1 and isinstance(existing, op.Struct):
                self.symbols.reset_global(name, self.current_struct)
            else:
                self.symbols.set_global(name, self.current_struct)
            self.current_struct = None
        else:
            self.action_endp()
            self.action_endseg()

    def action_end(self, label):
        if label:
            self.main_file = True
            self.entry_point = str(label)
            self.add_call_to_entrypoint()

    def parse_rt_info(self, name):
        try:
            with open(f"{name}.json") as infile:
                logging.info(f" *** Loading {name}.json")
                j = jsonpickle.decode(infile.read())
                self.runtime_code_meta = {}
                self.runtime_abi_meta = {}
                self.runtime_function_sampling_meta = {}
                self.runtime_data_meta = {}
                self.runtime_pointer_meta = {}
                self.runtime_access_site_meta = {}
                self.runtime_meta = j.get("Meta", {}) if isinstance(j, dict) else {}
                self.runtime_meta_anchor = None

                # Keep segment mapping aligned with runtime metadata when the
                # caller did not provide a fixed --loadsegment override.
                if not self.args.get("loadsegment"):
                    try:
                        rt_seg = self.runtime_meta.get("DosboxLoadSeg")
                        if rt_seg is not None:
                            self.args["loadsegment"] = hex(int(rt_seg))
                    except Exception:
                        pass

                proc_starts = set()
                for jump in j.get("Jumps", []):
                    jump_addr = self._parse_rt_addr(jump)
                    if jump_addr is not None:
                        proc_starts.add(jump_addr)
                for src_addr, code in j.get("Code", {}).items():
                    src = self._parse_rt_addr(src_addr)
                    if src is None:
                        continue
                    if isinstance(code, dict):
                        self.runtime_code_meta[src] = code
                    edges = code.get("Edges", {})
                    edge_kinds = code.get("EdgeKinds", {})
                    for dst_addr, _count in edges.items():
                        dst = self._parse_rt_addr(dst_addr)
                        if dst is None:
                            continue
                        mask = int(edge_kinds.get(dst_addr, 0))
                        # bit1 (Call) and bit0 (Jump) are useful function-entry hints
                        if mask & ((1 << 1) | (1 << 0)):
                            proc_starts.add(dst)

                for data_addr, data_meta in j.get("Data", {}).items():
                    addr = self._parse_rt_addr(data_addr)
                    if addr is None or not isinstance(data_meta, dict):
                        continue
                    self.runtime_data_meta[addr] = data_meta

                for pointer_meta in j.get("PointerEvidence", {}).values():
                    if not isinstance(pointer_meta, dict):
                        continue
                    source = self._parse_rt_addr(pointer_meta.get("SourceAddr"))
                    if source is None:
                        continue
                    self.runtime_pointer_meta.setdefault(source, []).append(pointer_meta)

                for access_meta in j.get("AccessSites", {}).values():
                    if not isinstance(access_meta, dict):
                        continue
                    csip = self._parse_rt_addr(access_meta.get("Csip"))
                    if csip is None:
                        continue
                    self.runtime_access_site_meta.setdefault(csip, []).append(access_meta)

                for sample_addr, sample_state in j.get("FunctionSampling", {}).items():
                    addr = self._parse_rt_addr(sample_addr)
                    if addr is None:
                        continue
                    if not isinstance(sample_state, dict):
                        continue
                    self.runtime_function_sampling_meta[addr] = sample_state
                    proc_starts.add(addr)

                for abi_addr, abi in j.get("Abi", {}).items():
                    addr = self._parse_rt_addr(abi_addr)
                    if addr is None:
                        continue
                    if isinstance(abi, dict):
                        self.runtime_abi_meta[addr] = abi
                        # ABI entries should also be considered function starts.
                        proc_starts.add(addr)
                        if addr in self.runtime_function_sampling_meta:
                            self.runtime_function_sampling_meta[addr].setdefault("FromAbi", True)
                        else:
                            self.runtime_function_sampling_meta[addr] = {"FromAbi": True}

                self.initial_procs_start = self.procs_start = proc_starts
                all_starts = set(proc_starts)
                if not all_starts:
                    all_starts = set(j.get("Jumps", []))
                all_starts |= set(self.runtime_code_meta.keys())
                if all_starts:
                    try:
                        self.runtime_meta_anchor = min(all_starts)
                    except Exception:
                        self.runtime_meta_anchor = None
        except FileNotFoundError:
            pass


def parse_asm_number(expr: Token | str, radix: int) -> tuple[int, str, str]:
    if expr == "?":
        radix, sign, value = 10, "", "0"
        return radix, sign, value

    if m := re.match(r"^(?P<sign>[+-]?)(?P<value>[0-8]+)[OoQq]$", expr):
        radix = 8
    elif m := re.match(r"^(?P<sign>[+-]?)(?P<value>[0-9][0-9A-Fa-f]*)[Hh]$", expr):
        radix = 16
    elif m := re.match(r"^(?P<sign>[+-]?)(?P<value>[0-9]+)[Dd]$", expr):
        radix = 10
    elif m := re.match(r"^(?P<sign>[+-]?)(?P<value>[0-1]+)[Bb]$", expr):
        radix = 2
    elif m := re.match(r"^(?P<sign>[+-]?)(?P<value>[0-9]+)$", expr):
        pass
    elif m := re.match(r"^(?P<sign>[+-]?)(?P<value>[0-9][0-9A-Fa-f]*)$", expr):
        radix = 16
    else:
        raise ValueError(expr)
    sign = m["sign"] or ""
    value = m["value"]
    return radix, sign, value
