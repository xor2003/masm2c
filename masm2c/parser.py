from __future__ import annotations

from argparse import Namespace
from ast import literal_eval

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
import hashlib
import logging
import os
import re
import sys
from collections import OrderedDict
from copy import deepcopy
from typing import Any, Optional, Never

import jsonpickle
from lark import UnexpectedToken, lark
from lark.lexer import Token
from lark.tree import Tree

from masm2c.op import Data, Struct, _assignment, _equ, baseop, label, var
from masm2c.proc import Proc
from masm2c.Token import Token as Token_, Expression

from . import cpp as cpp_module
from . import op
from .pgparser import (
    Asm2IR,
    AsmData2IR,
    BottomUpVisitor,
    ExprRemover,
    IncludeLoader,
    LarkParser,
)

INTEGERCNST = "integer"
STRINGCNST = "STRING"

class Vector:

    def __init__(self, arg1, arg2) -> None:
        self.__value: list[int] = [arg1, arg2]

    def __add__(self, vec: Optional[Vector]) -> Vector:
        if vec is not None:
            self.__value = [self.__value[0] + vec.values[0], self.__value[1] + vec.values[1]]
        return self

    def __mul__(self, other: int) -> Vector:
        self.__value = [self.__value[0] * other, self.__value[1] * other]
        return self

    @property
    def values(self):
        return self.__value

    #def __getitem__(self, item: int) -> int:
    #    return self.__value[item]

    def __repr__(self) -> str:
        return f"{self.__value}"

class ExprSizeCalculator(BottomUpVisitor):

    def __init__(self, element_size: int=0, **kwargs) -> None:
        super().__init__(**kwargs)
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
        if g := context.get_global(token):
            if isinstance(g, op.var):
                if self.element_size < 1:
                    self.element_size = g.size
                return Vector(self.element_size, 1)
            elif isinstance(g, (op._assignment, op._equ)):
                self.element_size = g.value.size()
                return Vector(self.element_size, 1)
            return None
        return None

    def memberdir(self, tree: Tree, size: Vector) -> Vector:
        label = tree.children
        context = self.kwargs["context"]
        g = context.get_global(label[0])
        type = label[0] if isinstance(g, op.Struct) else g.original_type

        try:
            for member in label[1:]:
                if (g := context.get_global(type)) is None:
                    raise KeyError(type)
                if isinstance(g, op.Struct):
                    g = g.getitem(str(member))
                    type = g.data
                else:
                    return g._size
        except KeyError as ex:
            logging.debug(f"Didn't found for {label} {ex.args} will try workaround")
            # if members are global as with M510 or tasm try to find last member size
            g = context.get_global(label[-1])

        self.element_size = g.size
        return Vector(self.element_size, 1)


def read_whole_file(file_name):
    """It reads the whole file and returns it as a string.

    :param file_name: The name of the file to read
    :return: The content of the file.
    """
    logging.info("     Reading file %s...", file_name)
    with open(file_name, encoding="cp437") as file:
        content = file.read()
    return content


def dump_object(value: Struct | label | Proc | var | _equ | _assignment) -> str:
    """Represents object as string.

    :param value: The object to dump
    :return: A string representation of the object.
    """
    stuff = str(value.__dict__)
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
    c_dummy_label = 0

    def __init__(self, args: Optional[Namespace] = None) -> None:
        """Assembler parser."""
        self.test_mode = False
        self.__globals: OrderedDict[str, Struct | label | Proc | var | _equ | _assignment] = OrderedDict()
        self.pass_number = 0

        self.__lex = LarkParser(context=self)

        self.externals_vars: set[str] = set()
        self.externals_procs: set[str] = set()
        self.__files: set[str] = set()
        self.itislst = False
        self.initial_procs_start: set[int] = set()
        self.procs_start: set[int] = set()

        if not args:
            class MyDummyObj(Namespace): pass

            args = MyDummyObj()
            args.mergeprocs = "separate"
        self.args = args

        self.next_pass(Parser.c_dummy_label)

    def next_pass(self, counter: int) -> None:
        """Initializer for each pass.

        :param counter: Labels id counter
        :return:
        """
        self.pass_number += 1
        logging.info(f"     Pass number {self.pass_number}")
        Parser.c_dummy_label = counter

        self.procs_start = self.initial_procs_start
        self.segments = OrderedDict()
        self.flow_terminated = True
        self.need_label = True

        self.structures: OrderedDict[str, Optional[Struct]] = OrderedDict()
        self.macro_names_stack: set[str] = set()
        self.proc_list: list[str] = []
        self.proc = None

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

        self.struct_names_stack: list[str] = []

        self._current_file = ""
        self.__current_file_hash = "0"

        self.data_merge_candidats = 0

        self.equs: set[str] = set()

    """
    def visible(self):
        for i in self.__stack:
            if not i or i == 0:
                return False
        return True

    def push_if(self, text):
        value = self.evall(text)
        # logging.debug "if %s -> %s" %(text, value)
        self.__stack.append(value)

    def push_else(self):
        # logging.debug "else"
        self.__stack[-1] = not self.__stack[-1]

    def pop_if(self):
        # logging.debug "endif"
        return self.__stack.pop()
    """

    def set_global(self, name: str, value: Struct | label | Proc | var | _equ | _assignment) -> None:
        if not name:
            raise NameError("empty name is not allowed")
        value.original_name = name
        name = name.lower()

        logging.debug("set_global(name='%s',value=%s)", name, dump_object(value))
        if name in self.__globals and self.pass_number == 1 and not self.test_mode:
            raise LookupError(f"global {name} was already defined")
        value.used = False
        self.__globals[name] = value

    def reset_global(self, name: str, value: Struct | label | Proc | var | _equ | _assignment) -> None:
        if not name:
            raise NameError("empty name is not allowed")
        value.original_name = name
        name = name.lower()
        logging.debug(f"reset global {name} -> {value}")
        self.__globals[name] = value

    def get_global(self, name: Token | str) -> Any:
        name = name.lower()
        logging.debug("get_global(%s)",name)
        g = self.__globals.get(name)
        logging.debug("%s", type(g))
        if g is None:
            logging.debug("get_global KeyError %s", name)
            return None
        g.used = True
        return g

    def get_globals(self):
        return self.__globals

    """
    def has_global(self, name):
        name = name.lower()
        return name in self.__globals


    def set_offset(self, name, value):
        if len(name) == 0:
            raise NameError("empty name is not allowed")
        logging.debug("adding offset %s -> %s" % (name, value))
        if name in self.__offsets and self.pass_number == 1:
            raise LookupError("offset %s was already defined", name)
        self.__offsets[name] = value

    def get_offset(self, name):
        return self.__offsets[name.lower()]
    """

    def replace_dollar_w_segoffst(self, v: str) -> str:
        logging.debug("$ = %d", self.__cur_seg_offset)
        return v.replace("$", str(self.__cur_seg_offset))

    @staticmethod
    def parse_int(v: str) -> int:
        # logging.debug "~1~ %s" %v
        assert isinstance(v, str)
        v = v.strip()
        # logging.debug "~2~ %s" %v
        result: str
        if re.match(r"^[+-]?[0-8]+[OoQq]$", v):
            result = str(int(v[:-1], 8))
        elif re.match(r"^[+-]?\d[0-9A-Fa-f]*[Hh]$", v):
            result = str(int(v[:-1], 16))
        elif re.match(r"^[01]+[Bb]$", v):
            result = str(int(v[:-1], 2))
        else:
            result = v

        try:
            vv: int = int(eval(result))
            return vv
        except Exception:
            pass

        # logging.debug "~4~ %s" %v
        return int(result)

    def identify_data_internal_type(self, data: Tree, elements_count: int, is_string_type: bool) -> op.DataType:
        if not is_string_type:
            return op.DataType.ARRAY if elements_count > 1 else op.DataType.NUMBER
        args = data.children
        return (
            op.DataType.ZERO_STRING
            if elements_count >= 2
               and not (isinstance(args[-1], Tree) and args[-1].data == "dupdir")
               and isinstance(args[-1].children[-1], lark.Token)
               and args[-1].children[-1].type == "INTEGER"
               and args[-1].children[-1].value == "0"
            else op.DataType.ARRAY_STRING
        )



    def action_label(self, name: str, far: bool=False, isproc: bool=False, raw: str="", globl: bool=True, line_number: int=0) -> None:
        logging.debug("label name: %s", name)
        if name == "arbarb": # @@
            name = self.get_dummy_jumplabel()
        name = self.mangle_label(name)  # for tests only


        self.need_label = False
        self.make_sure_proc_exists(line_number, raw)

        # if self.proc:
        assert self.proc
        l = op.label(name, proc=self.proc.name, isproc=isproc, line_number=self.__offset_id, far=far, globl=globl)
        _, l.real_offset, l.real_seg = self.get_lst_offsets(raw)

        if l.real_seg:
            self.procs_start.discard(l.real_seg * 0x10 + l.real_offset)
        self.proc.add_label(name, l)
        # self.set_offset(name,
        #                ("&m." + name.lower() + " - &m." + self.__segment_name, self.proc, self.__offset_id))
        self.set_global(name, l)
        self.__offset_id += 1

    def make_sure_proc_exists(self, line_number: int, raw: str) -> None:
        if not self.proc:
            _, real_offset, real_seg = self.get_lst_offsets(raw)
            offset = real_offset if real_seg else self.__cur_seg_offset
            pname = f"{self.__segment.name}_{offset:x}_proc"  # automatically generated proc name
            if pname in self.proc_list:
                self.proc = self.get_global(pname)
            else:
                self.proc = self.add_proc(pname, raw, line_number, False)

    def align(self, align_bound=0x10):
        num = (align_bound - (self.__binary_data_size & (align_bound - 1))) if (
                self.__binary_data_size & (align_bound - 1)) else 0
        self.org(num)

    def org(self, num):
        if self.itislst:
            return
        if num:
            label = self.get_dummy_label()
            offset = self.__binary_data_size
            self.__binary_data_size += num
            self.data_merge_candidats = 0

            self.__segment.append(
                op.Data(label, "db", op.DataType.ARRAY, [0], num, num, comment="for alignment", align=True,
                        offset=offset))

    def move_offset(self, pointer, raw):
        if pointer > self.__binary_data_size:
            self.data_merge_candidats = 0
            label = self.get_dummy_label()

            num = pointer - self.__binary_data_size
            offset = self.__binary_data_size
            self.__binary_data_size += num

            self.__segment.append(
                op.Data(label, "db", op.DataType.ARRAY, [0], num, num, comment="move_offset", align=True,
                        offset=offset))
        elif pointer < self.__binary_data_size and not self.itislst:
            self.data_merge_candidats = 0
            logging.warning(f"Maybe wrong offset current:{self.__binary_data_size:x} should be:{pointer:x} ~{raw}~")

    def get_dummy_label(self) -> str:
        return f"dummy{self.__current_file_hash[0]}_{hex(self.__binary_data_size)[2:]}"

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
        self._current_file = file_name
        self.__current_file_hash = hashlib.blake2s(os.path.basename(self._current_file).encode("utf8")).hexdigest()
        content = read_whole_file(file_name)
        if file_name.lower().endswith(".lst"):  # for .lst provided by IDA move address to comments after ;~
            # we want exact placement so program could work
            content = self.extract_addresses_from_lst(file_name, content)
        result = self.parse_text(content, file_name=file_name)
        result = self.process_ast(content, result)

    def extract_addresses_from_lst(self, file_name, content):
        self.itislst = True
        segmap = self.read_segments_map(file_name)
        # Remove structs addresses
        content = re.sub(r"^[0-9A-F]{8} ?", lambda m: "", content, flags=re.MULTILINE)
        # Move current CS:IP to the end of the string
        content = re.sub(r"^(?P<segment>[_0-9A-Za-z]+):(?P<offset>[0-9A-Fa-f]{4,8})(?P<remain>.*)",
                         lambda m: f'{m.group("remain")} ;~ {segmap.get(m.group("segment"))}:{m.group("offset")}',
                         content, flags=re.MULTILINE)
        return content

    def read_segments_map(self, file_name):
        """It reads a .map file and returns a dictionary of segments.

        :param file_name: The name of the .map file
        :return: A dictionary of segments and their values.
        """
        content = read_whole_file(re.sub(r"\.lst$", ".map", file_name, flags=re.I)).splitlines()
        DOSBOX_START_SEG = int(self.args.loadsegment, 0)
        strgenerator = iter(content)
        segs = OrderedDict()
        for line in strgenerator:
            if line.strip() == "Start  Stop   Length Name               Class":  # IDA Pro .lst magic
                break
        # Reads text until the end of the block:
        for line in strgenerator:  # This keeps reading the file
            if line.strip() == "Address         Publics by Value":
                break
            if line.strip():
                m = re.match(
                    r"^\s+(?P<start>[0-9A-F]{5,10})H [0-9A-F]{5,10}H [0-9A-F]{5,10}H (?P<segment>[_0-9A-Za-z]+)\s+[A-Z]+",
                    line)
                segs[m["segment"]] = f"{int(m['start'], 16) // 16 + DOSBOX_START_SEG:04X}"
        logging.debug(f"Results of loading .map file: {segs}")
        return segs

    def parse_include_file_lines(self, file_name):
        self.__files.add(self._current_file)
        self._current_file = file_name
        content = read_whole_file(file_name)
        result = self.parse_file_inside(content, file_name=file_name)
        self._current_file = self.__files.pop()
        return result

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

        # if self.has_global(label):
        assert self.proc
        o = self.proc.create_assignment_op(label, value, line_number=line_number)
        o.filename = self._current_file
        o.raw_line = raw.rstrip()
        self.reset_global(label, o)
        self.proc.stmts.append(o)
        self.equs.add(label)
        return o

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

        assert isinstance(value, Expression)
        o = Proc.create_equ_op(label, value, line_number=line_number)
        o.filename = self._current_file
        o.raw_line = raw.rstrip()
        o.element_size = size
        if isinstance(value, Expression) and value.indirection == IndirectionType.POINTER:
            o.original_type = value.original_type
        self.set_global(label, o)
        self.equs.add(label)
        proc = self.get_global("mainproc")
        proc.stmts.append(o)
        return o

    def create_segment(self, name, options=None, segclass=None, raw=""):
        logging.info("     Found segment %s", name)
        name = name.lower()
        self.data_merge_candidats = 0
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

            self.set_global(name, op.var(binary_width, offset, name, issegment=True))
        return self.__segment

    def action_proc(self, name, type, line_number=0, raw=""):
        logging.info("      Found proc %s", name)
        self.action_endp()
        name = self.mangle_label(name)
        far = False
        for i in type:
            if i and i.lower() == "far":
                far = True

        self.proc = self.add_proc(name, raw, line_number, far)

    def add_proc(self, name: str, raw: str, line_number: int, far: bool) -> Proc:
        if self.args.mergeprocs == "separate":
            self.need_label = False
        # if self.__separate_proc:
        offset, real_offset, real_seg = self.get_lst_offsets(raw)
        if real_seg:
            self.procs_start.discard(real_seg * 0x10 + real_offset)
        proc = Proc(name, far=far, line_number=line_number, offset=offset,
                    real_offset=real_offset, real_seg=real_seg,
                    segment=self.__segment.name)
        self.proc_list.append(name)
        self.set_global(name, proc)
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
        self.test_mode = True
        self.need_label = False
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            result = self.parse_text(line + "\n", start_rule="instruction")
            result = self.process_ast(line, result)
            assert isinstance(result, baseop)
        except Exception as e:
            print(e)
            logging.exception("Error1")
            #result = [str(e)]
            raise
        return result

    def test_size(self, line):
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            result = self.parse_text(line, start_rule="expr")
            expr = self.process_ast(line, result)
            result = expr.size()
        except Exception as e:
            print(e)
            import traceback
            logging.exception(traceback.format_exc())
            result = [str(e)]
            raise
        return result

    def action_data(self, line: str) -> Tree:
        """For tests only."""
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            result = self.parse_text(line + "\n", start_rule="insegdirlist")
            result = self.process_ast(line, result)
            assert isinstance(result, lark.Tree)
        except Exception as e:
            print(e)
            logging.exception("Error3")
            #result = [str(e)]
            raise
        return result

    def parse_arg(self, line: str, def_size: int=0, destination: bool=False) -> str:
        from .cpp import Cpp
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            expr = self.parse_text(line, start_rule="expr")
            expr = self.process_ast(line, expr)
            assert isinstance(expr, Expression)
            #if destination:
            #if def_size and expr.element_size == 0:
            result = Cpp(self).render_instruction_argument(expr, def_size=def_size, destination=destination)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            assert exc_tb
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            import logging
            import traceback

            logging.exception(traceback.format_exc())
            raise
        return result

    def parse_include(self, line, file_name=None):
        return self.parse_text(line, file_name=file_name, start_rule="insegdirlist")



    def datadir_action(self, label: str, type: str, args: Tree, is_string: bool=False, raw: str="", line_number: int=0) -> Data | list[Never]:
        if self.__cur_seg_offset > 0xffff:
            return []
        if self.__cur_seg_offset & 0xff == 0:
            logging.info(f"      Current offset {self.__cur_seg_offset:x} line={line_number}")
        isstruct = len(self.struct_names_stack) != 0

        binary_width = self.typetosize(type)
        #for ex in args:

        calc = ExprSizeCalculator(element_size=binary_width, init=Vector(0, 0), context=self)
        size, elements = calc.visit(args).values
        if size == 0:
            size = binary_width * elements

        offset = self.__cur_seg_offset
        if not isstruct:

            self.adjust_offset_to_real(raw, label)

            offset = self.__cur_seg_offset
            if not self.flow_terminated:
                logging.error(f"Flow wasn't terminated! line={line_number} offset={self.__cur_seg_offset}")

            logging.debug("args %s offset %d", args, offset)

        logging.debug("convert_data %s %d %s", label, binary_width, args)

        data_internal_type = self.identify_data_internal_type(args, elements, is_string)
        array = AsmData2IR().visit(args)
        if data_internal_type == op.DataType.ARRAY and not any(array) and not isstruct:  # all zeros
            array = [0]

        logging.debug("~size %d elements %d", binary_width, elements)
        if label and not isstruct:
            self.set_global(label, op.var(binary_width, offset, name=label,
                                          segment=self.__segment_name, elements=elements, original_type=type,
                                          filename=self._current_file, raw=raw, line_number=line_number))

        dummy_label = False
        if not label:
            dummy_label = True
            label = self.get_dummy_label()

        if isstruct:
            data_type = "struct data"
        else:
            self.__binary_data_size += size
            self.__cur_seg_offset += size
            data_type = "usual data"
        data = op.Data(label, type, data_internal_type, array, elements, size, filename=self._current_file,
                       raw_line=raw,
                       line_number=line_number, comment=data_type, offset=offset)
        if isstruct:
            assert self.current_struct
            self.current_struct.append(data)
        else:
            _, data.real_offset, data.real_seg = self.get_lst_offsets(raw)
            self.__segment.append(data)
            if dummy_label and data_internal_type == op.DataType.NUMBER and binary_width == 1:
                self.merge_data_bytes()
            else:
                self.data_merge_candidats = 0


        self.flow_terminated = True
        return data  # c, h, size

    def merge_data_bytes(self) -> None:
        self.data_merge_candidats += 1
        size = 32
        if self.data_merge_candidats == size:
            if self.__segment.getdata()[-size].offset + size - 1 != self.__segment.getdata()[-1].offset:
                logging.debug(
                    f"Cannot merge {self.__segment.getdata()[-size].label} - {self.__segment.getdata()[-1].label}")
            else:
                logging.debug(
                    f"Merging data at {self.__segment.getdata()[-size].label} - {self.__segment.getdata()[-1].label}")
                array = [x.children[0] for x in self.__segment.getdata()[-size:]]
                if not any(array):  # all zeros
                    array = [0]

                self.__segment.getdata()[-size].children = array
                self.__segment.getdata()[-size].elements = size
                self.__segment.getdata()[-size].data_internal_type = op.DataType.ARRAY
                self.__segment.getdata()[-size]._size = size
                self.__segment.setdata(self.__segment.getdata()[:-(size - 1)])

            self.data_merge_candidats = 0

    def adjust_offset_to_real(self, raw: str, label: str) -> None:
        absolute_offset, real_offset, _ = self.get_lst_offsets(raw)
        if self.itislst and real_offset and real_offset > 0xffff:  # IDA issue
            return
        if absolute_offset:
            self.move_offset(absolute_offset, raw)
            if self.__cur_seg_offset > real_offset and not self.itislst:
                logging.warning(f"Current offset does not equal to required for {label}")
            if self.__cur_seg_offset != real_offset:
                self.data_merge_candidats = 0
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
        return self.parse_include(text, file_name)

    def parse_text(self, text: str, file_name: None=None, start_rule: str="start") -> Tree:
        logging.debug("parsing: [%s]", text)
        try:
            assert hasattr(self.__lex, "parser")
            result = self.__lex.parser.parse(text, start=start_rule)
        except UnexpectedToken as ex:
            logging.exception("UnexpectedToken: [%s] line=%s column=%s", ex.token, ex.line, ex.column)
            sys.exit(9)
        return result

    def process_ast(self, text: str, result: Tree) -> baseop | Expression | lark.Tree:
        result = IncludeLoader(self).transform(result)
        result = ExprRemover().transform(result)
        asm2ir = Asm2IR(self, text)
        """
        for e in self.equs:
            g = self.get_global(e)
            if not isinstance(g.value, Expression):
                g.value = asm2ir.transform(g.value)
        """
        result = asm2ir.transform(result)
        return result

    @staticmethod
    def mangle_label(name: str | lark.Token) -> str:
        name = name.lower()  # ([A-Za-z@_\$\?][A-Za-z0-9@_\$\?]*)
        return name.replace("@", "arb").replace("?", "que").replace("$", "dol")

    @staticmethod
    def is_register(expr: lark.Token | str) -> int:
        expr = expr.lower()
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
        else:
            """
            type = data.gettype()
            binary_width = self.typetosize(type)
            _, _, array = self.process_data_tokens(values, binary_width)
            """
            return AsmData2IR().visit(values)

    def add_structinstance(self, label: str, type: str, args: list[Any | Tree], raw: str="") -> None:

        if not label:
            label = self.get_dummy_label()

        self.data_merge_candidats = 0
        self.adjust_offset_to_real(raw, label)
        offset = self.__cur_seg_offset

        s = self.structures[type]
        number = 1
        if isinstance(args, list) and len(args) > 2 and isinstance(args[1], str) and args[1] == "dup":
            cpp = cpp_module.Cpp(self)
            expr = Token_.find_tokens(args[0],"expr")
            number = literal_eval(cpp.render_instruction_argument(expr))
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
                self.set_global(label,
                                op.var(number * s.getsize(), self.__cur_seg_offset, label, segment=self.__segment_name, \
                                       original_type=type))
            self.__segment.append(d)
            self.__cur_seg_offset += number * s.getsize()
            self.__binary_data_size += number * s.getsize()

    def add_extern(self, label: str, type: Token) -> None:
        strtype = self.mangle_label(type)
        if isinstance(type, Token_):
            strtype = type.children
        label = self.mangle_label(label)
        if strtype not in ["proc"]:
            binary_width = self.typetosize(type)
            self.reset_global(label, op.var(binary_width, 0, name=label, segment=self.__segment_name,
                                            elements=1, external=True, original_type=strtype))
            self.externals_vars.add(label)
        else:  # Proc
            # if self.__separate_proc:
            self.externals_procs.add(label)
            proc = Proc(label, extern=True)
            logging.debug("procedure %s, extern", label)
            self.reset_global(label, proc)

    def add_call_to_entrypoint(self):
        """It adds a call to the entry point of the program to the service mainproc."""
        # if self.__separate_proc:
        proc = self.get_global("mainproc")
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

    def action_instruction(self, instruction: Token, args: list[Expression | Any], raw: str="", line_number: int=0) -> baseop | None:
        self.handle_local_asm_jumps(instruction, args)

        self.make_sure_proc_exists(line_number, raw)

        assert self.proc
        o = self.proc.create_instruction_object(instruction, args)
        o.filename = self._current_file
        o.raw_line = raw
        o.line_number = line_number
        if self.current_macro is None:
            _, o.real_offset, o.real_seg = self.get_lst_offsets(raw)
            if not self.need_label and o.real_seg and len(self.procs_start) \
                    and (o.real_seg * 0x10 + o.real_offset) in self.procs_start:
                logging.warning(
                    f"Add a label since run-time info contain flow enter at this address {o.real_seg:x}:{o.real_offset:x} line={line_number}")
                self.need_label = True
            if self.need_label and self.flow_terminated:
                logging.warning(f"Flow terminated and it was no label yet line={line_number}")
                if o.real_seg:
                    logging.warning(f"at {o.real_seg:x}:{o.real_offset:x}")
            if self.need_label and self.proc.stmts:  # skip first instruction
                label_name = f"ret_{o.real_seg:x}_{o.real_offset:x}" if o.real_seg else self.get_extra_dummy_jumplabel()
                logging.warning(f"Adding helping label {label_name}")
                self.action_label(label_name, raw=raw)
            self.proc.stmts.append(o)
            if self.args.mergeprocs == "single":
                self.need_label |= self.proc.is_return_point(o)
            self.flow_terminated = self.proc.is_flow_terminating_stmt(o)
            self.need_label |= self.flow_terminated

            self.collect_labels(self.proc.used_labels, o)
            return o
        else:
            self.current_macro.instructions.append(o)
            return

    def handle_local_asm_jumps(self, instruction: Token, args: list[Expression | Any]) -> None:
        if (
            instruction[0].lower() in ["j", "loop"]
            and len(args) == 1
            and isinstance(args[0], lark.Tree)
            and isinstance(args[0].children, list)
            and isinstance(args[0].children[0], lark.Token)
            and args[0].children[0].type == "LABEL"
        ):
            if args[0].children[0].lower() == "arbf":  # @f
                args[0].children[0] = f"dummylabel{self.__c_dummy_jump_label + 1!s}"
            elif args[0].children[0].lower() == "arbb":  # @b
                args[0].children[0] = f"dummylabel{self.__c_dummy_jump_label!s}"

    def collect_labels(self, target: set[str], operation: baseop) -> None:
        for arg in operation.children:
            offset = Token_.find_tokens(arg, "offsetdir") or []
            if offset and not isinstance(offset[0], str): offset = []
            labels = (Token_.find_tokens(arg, "LABEL") or []) + offset
            # TODO replace with AST traversing
            #  If it is call to a proc then does not take it into account
            #  TODO: check for calls into middle of proc
            if labels and not operation.cmd.startswith("call") and not (
                    self.args.mergeprocs == "separate" and operation.cmd == "jmp"):
                label = labels[0]
                if label == "dol":
                    continue
                assert isinstance(label, str)
                target.add(self.mangle_label(label))

    def action_ends(self) -> None:
        if len(self.struct_names_stack):  # if it is not a structure then it is end of segment
            name = self.struct_names_stack.pop()
            logging.debug(f"endstruct {name}")
            assert self.current_struct
            self.structures[name] = self.current_struct
            self.set_global(name, self.current_struct)
            self.current_struct = None
        else:
            self.action_endp()
            self.action_endseg()

    def action_end(self, label):
        if label:
            self.main_file = True
            self.entry_point = label
            self.add_call_to_entrypoint()

    def parse_rt_info(self, name):

        try:
            with open(f"{name}.json") as infile:
                logging.info(f" *** Loading {name}.json")
                j = jsonpickle.decode(infile.read())
                self.initial_procs_start = self.procs_start = set(j["Jumps"])
        except FileNotFoundError:
            pass


def parse_asm_number(expr: Token | str, radix: int) -> tuple[int, str, str]:
    if expr == "?":
        radix, sign, value = 10, "", "0"
    else:
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
        #if sign == '-':
    return radix, sign, value
