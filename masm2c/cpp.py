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
from typing import TYPE_CHECKING, Any, Optional, Union

from lark.lexer import Token
from lark.tree import Tree
from masm2c.op import Data
from masm2c.Token import Expression

if TYPE_CHECKING:
    from masm2c.parser import Parser

import os
import re
from collections import OrderedDict

from lark import lark

from . import op, proc
from . import proc as proc_module
from .enumeration import IndirectionType
from .gen import Gen, InjectCode, mangle_asm_labels
from .pgparser import LABEL, MEMBERDIR, REGISTER, SQEXPR, Asm2IR, TopDownVisitor
from .Token import Expression, Token


def flatten(s: list) -> list:
    if not s:
        return s
    if isinstance(s[0], list):
        return flatten(s[0]) + flatten(s[1:])
    return s[:1] + flatten(s[1:])


class SeparateProcStrategy:

    def __init__(self, renderer: "Cpp") -> None:
        self.renderer = renderer

    def produce_proc_start(self, name):
        return f" // Procedure {name}() start\n{self.renderer.cpp_mangle_label(name)}()\n{{\n"

    def function_header(self, name, entry_point=""):
        header = """

 bool %s(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;
""" % self.renderer.cpp_mangle_label(name)

        if entry_point != "":
            header += """
    if (__disp == kbegin) goto %s;
""" % entry_point

        header += """
    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    %s:
    _begin:
""" % self.renderer.cpp_mangle_label(name)
        return header

    def write_declarations(self, procs, context):
        result = ""
        for p in sorted(procs):  # TODO only if used or public
            if p == "mainproc" and not context.itislst:  # and not context.main_file:
                result += "static "
            result += "bool %s(m2c::_offsets, struct m2c::_STATE*);\n" % self.renderer.cpp_mangle_label(p)

        for i in sorted(context.externals_procs):
            v = context.get_global(i)
            if v.used:
                result += f"extern bool {v.name}(m2c::_offsets, struct m2c::_STATE*);\n"

        result += """
bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state);
"""
        return result


class Cpp(Gen, TopDownVisitor):
    """Visitor which can produce C++ equivalents for asm instructions."""

    def __init__(self, context: Optional["Parser"]=None, outfile: str="", skip_output: None=None,
                 merge_data_segments: bool=True) -> None:
        # proc_strategy = SingleProcStrategy()):
        """:param context: pointer to Parser data
        :param outfile: Output filename
        :param skip_output: List of functions to skip at output
        """
        super().__init__(context, outfile=outfile, skip_output=skip_output, merge_data_segments=merge_data_segments)
        self.proc_strategy = SeparateProcStrategy(self)
        self.renderer = self
        self._namespace = os.path.basename(outfile)
        self.__codeset = "cp437"
        self._context = context

        self._indirection: IndirectionType = IndirectionType.VALUE

        #
        self.__proc_done = []
        self.__failed = []
        self._proc_addr = []
        self.__used_data_offsets = set()
        self.__methods = []
        self.__pushpop_count = 0

        self.far = False
        self.size_changed = False
        self.needs_dereference = False
        self.itispointer = False

        self.struct_type = None

        self.dispatch = ""
        self.prefix = ""
        self._cmdlabel = ""

        self.isvariable = False
        self.islabel = False

        self.itisjump = False
        self.itiscall = False
        self.is_data = False

        self.__type_table = {op.DataType.NUMBER: self.produce_c_data_number,
                             op.DataType.ARRAY: self.produce_c_data_array,
                             op.DataType.ZERO_STRING: self.produce_c_data_zero_string,
                             op.DataType.ARRAY_STRING: self.produce_c_data_array_string,
                             op.DataType.OBJECT: self.produce_c_data_object,
                             }

        self.element_size = -1


    def convert_label_(self, original_name: Token) -> str:
        """
        Converts a label to its corresponding value.

        :param original_name: The original label name.
        :type original_name: Token
        :return: The corresponding value of the label.
        :rtype: str
        """
        name = str(original_name)
        if (g := self._context.get_global(name)) is None:
            return name

        self.islabel = True

        if isinstance(g, op.var):
            return self.convert_label_var(g, name, original_name)
        elif isinstance(g, op.label):
            return f"m2c::k{name}" if self.is_data or not self.itisjump else name
        else:
            return name

    def convert_label_var(self, g, name, original_name) -> str:
        logging.debug("Variable detected. Size: %s", g.size)
        self.variable_size = source_var_size = g.size

        if source_var_size == 0 and not g.issegment:
            raise Exception("Invalid variable '%s' size %u" % (name, source_var_size))

        if source_var_size:
            self.isvariable = True
        if self._middle_size == 0:  # TODO check
            self._middle_size = source_var_size

        if g.issegment:
            self._indirection = IndirectionType.VALUE
            return f"seg_offset({original_name.lower()})"
        return self._convert_label_var_non_segment(g, name)

    def _convert_label_var_non_segment(self, g, name):
        self.needs_dereference = False
        self.itispointer = False
        if g.elements != 1:  # array
            self.needs_dereference = True
            self.itispointer = True

            if not self.lea:
                self._indirection = IndirectionType.POINTER

        if g.elements == 1 and self._isjustlabel and not self.lea and g.size == self.element_size:
            result = g.name
            self._indirection = IndirectionType.VALUE
        else:
            result = self._convert_label_var_non_segment_complex(g, name)
        return result

    def _convert_label_var_non_segment_complex(self, g, name):
        if not self._isjustlabel and not self.lea and self._indirection == IndirectionType.VALUE:
            self._indirection = IndirectionType.POINTER
        if self._indirection == IndirectionType.POINTER:  # and self.isvariable:
            result = g.name
            if not self._isjustlabel:  # if not just single label: [a+3] address arithmetics
                self.needs_dereference = True
                self.itispointer = True
                if g.elements == 1:  # array generates pointer himself
                    result = f"&{result}"

                if g.getsize() == 1:  # it is already a byte
                    result = f"({result})"
                else:
                    result = f"((db*){result})"
                    self.size_changed = True
                    self._middle_size = 1
        elif self._indirection == IndirectionType.OFFSET:
            result = f"offset({g.segment},{g.name})"
            self.needs_dereference = False
            self.itispointer = False
        else:
            result = name
        if self._work_segment == "cs":
            self.body += "\tcs=seg_offset(" + g.segment + ");\n"
        return result

    def render_data_c(self, segments):
        """It takes a list of DOS segments, and for each segment, it takes a list of data items, and for each data item, it
        produces a C++ assignment statement, a C++ extern statement, and a C++ reference statement.

        :param segments: a dictionary of segments, where the key is the segment name and the value is the segment object
        :return: cpp_file, data_hpp_file, data_cpp_file, hpp_file
        """
        self.is_data = True

        cpp_file = ""
        data_hpp_file = ""
        data_cpp_file = ""
        hpp_file = ""
        for segment in segments.values():
            #  Add segment address
            data_cpp_file += f"db& {segment.name}=*((db*)&m2c::m+0x{segment.offset:x});\n"
            hpp_file += f"extern db& {segment.name};\n"

            for data in segment.getdata():
                value, type_and_name, _ = self.produce_c_data_single_(data)

                type_and_name += ";\n"

                if not data.is_align():  # if align do not assign it
                    m = re.match(r"^(\w+)\s+(\w+)(\[\d+\])?;\n", type_and_name)
                    if not m:
                        logging.error(f"Failed to parse {value} {type_and_name}")
                    name = m[2]

                    type_and_size = re.sub(r"^(?P<type>\w+)\s+\w+(\[\d+\])?;\n", r"\g<type> tmp999\g<2>", type_and_name)

                    if name.startswith("dummy") and value == "0":
                        value = ""
                    elif m[2]:  # if array
                        value = "" if value == "{}" else f"    {{{type_and_size}={value};MYCOPY({name})}}"
                    else:
                        value = f"    {{{type_and_size}={value};MYCOPY({name})}}"

                    # char (& bb)[5] = group.bb;
                    # references
                    _reference_in_data_cpp = self._generate_dataref_from_declaration_c(type_and_name)
                    # externs
                    _extern_in_hpp = self._generate_extern_from_declaration_c(type_and_name)

                    if value:
                        real_seg, real_offset = data.getrealaddr()
                        if real_seg:
                            value += f" // {real_seg:04x}:{real_offset:04x}"
                            type_and_name = f"{type_and_name[:-1]} // {real_seg:04x}:{real_offset:04x}\n"
                        value += "\n"

                    cpp_file += value  # cpp source - assigning
                    hpp_file += _extern_in_hpp  # extern for header

                    data_cpp_file += _reference_in_data_cpp  # reference in _data.cpp
                data_hpp_file += type_and_name  # headers in _data.h

        self.is_data = False
        return cpp_file, data_hpp_file, data_cpp_file, hpp_file

    def _generate_extern_from_declaration_c(self, _hpp):
        """It takes a C++ declaration and returns a extern declaration to the same.

        :param _hpp: The C++ header file
        :return: The extern declaration of the function or variable.
        """
        _extern = re.sub(r"^(\w+)\s+([\w\[\]]+)(\[\d+\]);", r"extern \g<1> (& \g<2>)\g<3>;", _hpp)
        _extern = re.sub(r"^(\w+)\s+([\w\[\]]+);", r"extern \g<1>& \g<2>;", _extern)
        return _extern

    def _generate_dataref_from_declaration_c(self, _hpp):
        """It takes a C++ declaration and returns a reference to the same variable.

        :param _hpp: declaration string
        :return: The reference to the same data
        """
        _reference = re.sub(r"^(\w+)\s+([\w\[\]]+)(\[\d+\]);",
                            r"\g<1> (& \g<2>)\g<3> = m2c::m.\g<2>;", _hpp)
        _reference = re.sub(r"^(\w+)\s+([\w\[\]]+);", r"\g<1>& \g<2> = m2c::m.\g<2>;", _reference)
        return _reference

    def memberdir(self, tree: Tree) -> list[str]:
        return [self.convert_member_(tree.children)]


    def convert_member_(self, label: list[str]) -> str:
        self.struct_type = None
        value = ".".join(label)

        if self._indirection == IndirectionType.OFFSET and (g := self._context.get_global(label[0])):
            return self.convert_member_offset(g, label)

        if (g := self._context.get_global(label[0])) is None:
            logging.error("global '%s' is missing", label)
            return ".".join(label)

        if isinstance(g, (op._equ, op._assignment)):
            value = self._convert_member_equ(g, label)
        elif isinstance(g, op.var):

            value = self._convert_member_var(g, label)
        elif isinstance(g, op.Struct):
            #if self._isjustmember:
            value = f'offsetof({label[0]},{".".join(label[1:])})'

        if self._indirection == IndirectionType.POINTER and self.needs_dereference and self.struct_type:

            self._ismember = True

            self.needs_dereference = False

        #if size == 0:
        return value

    def _convert_member_var(self, g, label):
        source_var_size = self.calculate_member_size(label)
        if source_var_size == 0:
            raise Exception(f"invalid var {label} size {source_var_size}")

        self.variable_size = source_var_size
        logging.debug("it is var %s", source_var_size)
        if self._middle_size == 0:
            self._middle_size = source_var_size
        self.isvariable = True
        self.islabel = True
        if g.elements == 1 and self._isjustlabel and not self.lea and source_var_size == self._middle_size:
            self.needs_dereference = False
            self.itispointer = False
            value = ".".join(label)
            self._indirection = IndirectionType.VALUE
        else:
            self.needs_dereference = True
            self.itispointer = True
            if self._indirection == IndirectionType.POINTER:
                value = ".".join(label)
                if not self._isjustlabel:  # if not just single label
                    if g.elements == 1:  # array generates pointer himself
                        value = f"&{value}"

                    if g.getsize() == 1:  # it is already a byte
                        value = f"({value})"
                    else:
                        value = f"((db*){value})"
                        self.size_changed = True
            elif self._indirection == IndirectionType.OFFSET:
                value = f'offset({g.segment},{".".join(label)})'
            if self._work_segment == "cs":
                self.body += "\tcs=seg_offset(" + g.segment + ");\n"
        return value

    def _convert_member_equ(self, g, label):
        logging.debug("%s", g)
        if not g.implemented:
            raise InjectCode(g)
        if self._isjustlabel:
            value = ".".join(label)
        else:
            self.struct_type = g.value.original_type
            self.needs_dereference = True
            self.itispointer = False
            self._need_pointer_to_member = label
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
            raise Exception(f"Not handled type {str(type(g))}")
        self._indirection = IndirectionType.VALUE
        return value

    def convert_sqbr_reference(self, segment: str, expr: str, destination: bool, size: int, islabel: bool,
                               lea: bool = False) -> str:
        if not lea or destination:
            if not self.islabel or not self.isvariable:
                self.needs_dereference = True
                self.itispointer = True
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
            elif self.size_changed:  # or not self._isjustlabel:
                    expr = Cpp.render_new_pointer_size(self.itispointer, expr, size)
                    self.size_changed = False

            logging.debug(f"expr: {expr}")
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
        self.itisjump = True
        result = self.render_instruction_argument(expr, 0)  # TODO why need something else?
        self.itisjump = False
        name = result
        far = self.get_global_far(name)
        if "far" in expr.mods:
            far = True
        elif "near" in expr.mods:
            far = False

        if isinstance(name, str) and ((g := self._context.get_global(name)) is None or isinstance(g, op.var)):
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
        if isinstance(name, str) and (g := self._context.get_global(name)) and isinstance(g, proc_module.Proc | op.label):
            far = g.far  # make far calls to far procs
        return far

    def _label(self, name, isproc):
        if isproc:
            raise RuntimeError("Dead code?")
        else:
            self._cmdlabel = "%s:\n" % self.cpp_mangle_label(name)
        return ""

    def _call(self, expr: Expression) -> str:
        logging.debug("cpp._call(%s)", expr)
        ret = ""
        if expr.ptr_size == 0:
            expr.ptr_size = 2
        size = self.calculate_size(expr)
        self.itisjump = True
        self.itiscall = True
        proc_name = self.render_instruction_argument(expr, 0)  # TODO why need something else?
        self.itiscall = False
        self.itisjump = False
        far = self.get_global_far(proc_name)
        if size == 4 or "far" in expr.mods:
            far = True
        elif "near" in expr.mods:
            far = False

        label_ip = "0"
        if isinstance(proc_name, str) and (g := self._context.get_global(proc_name)):
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

        proc_name = self.cpp_mangle_label(proc_name)

        if far:
            ret += f"CALLF({proc_name},{label_ip})"
        else:
            ret += f"CALL({proc_name},{label_ip})"
        return ret

    def _ret(self, src: list[Union[Expression, Any]]) -> str:
        self.a = self.render_instruction_argument(src[0]) if src else "0"
        return f"RETN({self.a})"

    def _retf(self, src: list[Union[Expression, Any]]) -> str:
        self.a = self.render_instruction_argument(src[0]) if src else "0"
        return f"RETF({self.a})"

    def _xlat(self, src: list[Union[Expression, Any]]) -> str:
        if not src:
            return "XLAT"
        self.a = self.render_instruction_argument(src[0])[2:-1]
        return f"XLATP({self.a})"

    def parse2(self, dst: Expression, src: Expression) -> tuple[str, str]:
        dst_size, src_size = self.calculate_size(dst), self.calculate_size(src)
        if dst_size == 0:
            if src_size == 0:
                logging.debug("parse2: %s %s both sizes are 0", dst, src)
            dst_size = src_size
        if src_size == 0:
            src_size = dst_size

        if src.indirection == IndirectionType.POINTER and src.element_size == 0 and dst_size and not src.ptr_size:
            src.ptr_size = dst_size
        if dst.indirection == IndirectionType.POINTER and dst.element_size == 0 and src_size and not dst.ptr_size:
            dst.ptr_size = src_size
        dst = self.render_instruction_argument(dst, dst_size, destination=True)
        src = self.render_instruction_argument(src, src_size)
        return dst, src

    def _add(self, dst: Expression, src: Expression) -> str:
        self.a, self.b = self.parse2(dst, src)
        # if self.d in ['sp', 'esp'] and check_int(self.s):
        return f"ADD({self.a}, {self.b})"

    def _mul(self, src: list[Expression]) -> str:
        size = 0
        res = [self.render_instruction_argument(i, size) for i in src]
        for i in src:
            if size == 0:
                size = self.calculate_size(i)
            else:
                break
        if size == 0:
            size = self._middle_size
        return "MUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _imul(self, src: list[Expression]) -> str:
        size = 0
        for i in src:
            if size == 0:
                size = self.calculate_size(i)
            else:
                break
        res = [self.render_instruction_argument(i, size) for i in src]
        if size == 0:
            size = self._middle_size
        return "IMUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _div(self, src: Expression) -> str:
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        return "DIV%d(%s)" % (size, self.a)

    def _idiv(self, src: Expression) -> str:
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        return "IDIV%d(%s)" % (size, self.a)

    def _jz(self, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"
        label, _ = self.jump_post(label)  # TODO
        return f"JZ({label})"

    def _jnz(self, label: Expression) -> str:
        label, _ = self.jump_post(label)
        return f"JNZ({label})"

    def _jbe(self, label: Expression) -> str:
        label, _ = self.jump_post(label)
        return f"JBE({label})"

    def _ja(self, label: Expression) -> str:
        label, far = self.jump_post(label)
        return f"JA({label})"

    def _jc(self, label: Expression) -> str:
        label, far = self.jump_post(label)
        return f"JC({label})"

    def _jnc(self, label: Expression) -> str:
        label, far = self.jump_post(label)
        return f"JNC({label})"

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
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        srcr = Token.find_tokens(src, REGISTER)
        return "SCAS(%s,%s,%d)" % (self.a, srcr[0], size)

    def process(self):
        self.merge_procs()
        self._remove_hacks()

    def _remove_hacks(self):
        for proc_name in self._procs:
            proc = self._context.get_global(proc_name)
            i = 0
            while i < len(proc.stmts):
                self._remove_hacks_popf(i, proc)
                i += 1

    def _remove_hacks_popf(self, i, proc):
        # replace popf hack: or bh, 0; push cs; call loc+1
        if len(proc.stmts) - i >= 5 and \
                proc.stmts[i].cmd == '' and proc.stmts[i].data == 'label' and \
                proc.stmts[i + 1].cmd == 'or' and proc.stmts[i + 1].children == \
                [lark.Tree('expr', [lark.Tree('register', ['bh'])]),
                 lark.Tree('expr', [lark.Token('INTEGER', '0')])] and \
                proc.stmts[i + 2].cmd == '' and proc.stmts[i + 2].data == 'label' and \
                proc.stmts[i + 3].cmd == 'push' and proc.stmts[i + 3].children == \
                [lark.Tree('expr', [lark.Tree('segmentregister', ['cs'])])] and \
                proc.stmts[i + 4].cmd == 'call' and proc.stmts[i + 4].children[0].data == 'expr' and \
                proc.stmts[i + 4].children[0].children[0].data == 'adddir':
            logging.info("Patching popf hack")
            del proc.stmts[i + 4]
            del proc.stmts[i + 3]
            o = proc.create_instruction_object("popf", [])
            o.filename = ""
            o.line_number = 0
            o.raw_line = ""
            o.syntetic = True
            proc.stmts[i + 1] = o
        elif len(proc.stmts) - i >= 4 and \
                proc.stmts[i].cmd == '' and proc.stmts[i].data == 'label' and \
                proc.stmts[i + 1].cmd == 'or' and proc.stmts[i + 1].children == \
                [lark.Tree('expr', [lark.Tree('register', ['bh'])]),
                 lark.Tree('expr', [lark.Token('INTEGER', '0')])] and \
                proc.stmts[i + 2].cmd == 'push' and proc.stmts[i + 2].children == \
                [lark.Tree('expr', [lark.Tree('segmentregister', ['cs'])])] and \
                proc.stmts[i + 3].cmd == 'call' and proc.stmts[i + 3].children[0].data == 'expr' and \
                proc.stmts[i + 3].children[0].children[0].data == 'adddir':
            logging.info("Patching popf hack")
            del proc.stmts[i + 3]
            del proc.stmts[i + 2]
            o = proc.create_instruction_object("popf", [])
            o.filename = ""
            o.line_number = 0
            o.raw_line = ""
            o.syntetic = True
            proc.stmts[i + 1] = o

    def save_cpp_files(self, fname):
        cpp_assigns, _, _, cpp_extern = self.render_data_c(self._context.segments)

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
{self.produce_global_jump_table(list(self._context.get_globals().items()), self._context.itislst)}

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
{cpp_extern}
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

        self.write_segment_file(self._context.segments, self._context.structures, fname)

    def write_procedures(self, banner, header_fname):
        cpp_file_text = ""
        last_segment = None
        cpp_segment_file = None
        for name in self._procs:
            proc_text, segment = self._render_procedure(name)
            if self._context.itislst and segment != last_segment:  # If .lst write to separate segments. Open new if changed
                last_segment = segment
                if cpp_segment_file:
                    cpp_segment_file.close()

                cpp_segment_fname = f"{self._namespace.lower()}_{segment}.cpp"
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

        return cpp_file_text

    def render_entrypoint_c(self):
        entry_point_text = ""
        if self._context.main_file:
            g = self._context.get_global(self._context.entry_point)
            if isinstance(g, op.label) and self._context.entry_point not in self.grouped:
                entry_point_text = f"""
                 bool {self._context.entry_point}(m2c::_offsets, struct m2c::_STATE* _state){{return {self.label_to_proc[g.name]}(m2c::k{self._context.entry_point}, _state);}}
                """

            entry_point_text += f"""namespace m2c{{ m2cf* _ENTRY_POINT_ = &{self.cpp_mangle_label(self._context.entry_point)};}}
        """
        return entry_point_text

    def render_function_wrappers_c(self):
        return "".join(
            f"""
 bool {p}(m2c::_offsets, struct m2c::_STATE* _state){{return {self.groups[p]}(m2c::k{p}, _state);}}
"""
            for p in sorted(self.grouped)
        )

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
        _, data_h, data_cpp_reference, _ = self.render_data_c(segments)
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

    def produce_label_offsets(self):
        labeloffsets = """namespace m2c{
void   Initializer();
static const dd kbegin = 0x1001;
"""
        i = 0x1001
        for k, v in list(self._context.get_globals().items()):
            # if isinstance(v, (op.label, proc_module.Proc)) and v.used:
            if isinstance(v, (op.label, proc_module.Proc)):
                k = re.sub(r"[^A-Za-z0-9_]", "_", k).lower()
                i += 1
                if v.real_offset or v.real_seg:
                    i = v.real_seg * 0x10000 + v.real_offset
                labeloffsets += f"static const dd k{k} = 0x{i:x};\n"
        labeloffsets += "}\n"
        return labeloffsets

    def produce_structures(self, strucs):
        structures = "\n"
        if len(strucs):
            structures += """#pragma pack(push, 1)"""
        for name, v in strucs.items():
            struc_type = "struct" if v.gettype() == op.Struct.Type.STRUCT else "union"
            structures += f"""
{struc_type} {name} {{
"""
            for member in v.getdata().values():
                structures += f"  {member.data_type} {member.label};\n"
            structures += """};
"""
        if len(strucs):
            structures += """
#pragma pack(pop)

"""
        return structures

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
            v = context.get_global(i)
            if v.used:
                data += f"extern {v.original_type} {v.name};\n"
        return data

    def _lea(self, dst: Expression, src: Expression) -> str:
        src.indirection = IndirectionType.OFFSET
        src.mods.add("lea")
        dst.mods.add("lea")
        self.lea = True
        self.a, self.b = self.parse2(dst, src)
        self.lea = False
        return f"{self.a} = {self.b}"

    def _movs(self, dst: Expression, src: Expression) -> str:
        size = self.calculate_size(dst)
        dstr, srcr = Token.find_tokens(dst, REGISTER), Token.find_tokens(src, REGISTER)
        self.a, self.b = self.parse2(dst, src)
        return "MOVS(%s, %s, %s, %s, %d)" % (self.a, self.b, dstr[0], srcr[0], size)

    def _repe(self):
        self.prefix = "\tREPE "
        return ""

    def _repne(self):
        self.prefix = "\tREPNE "
        return ""

    def _lods(self, src: Expression) -> str:
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        srcr = Token.find_tokens(src, REGISTER)
        return "LODS(%s,%s,%d)" % (self.a, srcr[0], size)

    def _leave(self) -> str:
        return "LEAVE"  # MOV(esp, ebp) POP(ebp)

    def _int(self, dst: Expression) -> str:
        self.a = self.render_instruction_argument(dst)
        return f"_INT({self.a})"

    def _instruction0(self, cmd: str) -> str:
        return cmd.upper()

    def _instruction1(self, cmd: str, dst: Expression) -> str:
        self.a = self.render_instruction_argument(dst)
        return f"{cmd.upper()}({self.a})"

    def render_instruction_argument(self, expr: Expression, def_size: int = 0, destination: bool = False, lea: bool = False) -> str:
        if destination:
            expr.mods.add("destination")
        if lea:
            expr.mods.add("lea")
        if def_size == 0 and expr.element_size == 0 and expr.indirection != IndirectionType.POINTER:
            from .parser import ExprSizeCalculator, Vector
            calc = ExprSizeCalculator(init=Vector(0, 0), context=self._context)
            def_size, _ = calc.visit(expr)  # , result=0)

        if def_size and expr.element_size == 0:
            expr.element_size = def_size
        ir2cpp = IR2Cpp(self._context)
        ir2cpp.lea = self.lea
        ir2cpp._indirection = expr.indirection
        ir2cpp.itisjump = self.itisjump
        ir2cpp.itiscall = self.itiscall
        result = "".join(ir2cpp.visit(expr))
        self.size_changed = ir2cpp.size_changed
        return result[1:-1] if self.check_parentesis(result) else result

    def check_parentesis(self, string: str) -> bool:
        """Check if first ( matches the last one.

        >>> self.check_parentesis('(())')
        True
        >>> self.check_parentesis('()()')
        False
        """
        if not string or string[0] != "(" or string[-1] != ")": return False
        res = 0
        for c in string[1:-1]:
            if c == "(": res += 1
            elif c == ")": res -= 1
            if res < 0: return False
        return True

    def _jump(self, cmd: str, label: Expression) -> str:
        if self.isrelativejump(label):
            return "{;}"

        label, _ = self.jump_post(label)
        if self._context.args.mergeprocs == "separate" and cmd.upper() == "JMP":
            if label == "__dispatch_call":
                return "return __dispatch_call(__disp, _state);"
            if g := self._context.get_global(label):
                target_proc_name = None
                if isinstance(g, op.label) and g.name in self.label_to_proc:
                    target_proc_name = self.label_to_proc[g.name]
                elif isinstance(g, proc_module.Proc):
                    target_proc_name = g.name
                if target_proc_name and self.proc.name != target_proc_name:
                    if g.name == target_proc_name:
                        return f"return {g.name}(0, _state);"
                    return f"return {target_proc_name}(m2c::k{label}, _state);"

        return f"{cmd.upper()}({label})"

    def _instruction2(self, cmd: str, dst: Expression, src: Expression) -> str:
        self.a, self.b = self.parse2(dst, src)
        return f"{cmd.upper()}({self.a}, {self.b})"

    def _instruction3(self, cmd: str, dst: Expression, src: Expression, c: Expression) -> str:
        self.a, self.b = self.parse2(dst, src)
        self.c = self.render_instruction_argument(c)
        return f"{cmd.upper()}({self.a}, {self.b}, {self.c})"

    def return_empty(self, _):
        return []

    def _assignment(self, stmt):
        dst, src = stmt
        asm2ir = Asm2IR(self._context, "")
        if not isinstance(src, Expression):
            src = asm2ir.transform(src)

        src.indirection = IndirectionType.VALUE
        self._cmdlabel += f"#undef {dst}\n#define {dst} {self.render_instruction_argument(src)}\n"
        return ""

    def _equ(self, dst):
        src = self._context.get_global(dst).value
        src.indirection = IndirectionType.VALUE
        self._cmdlabel += f"#define {dst} {self.render_instruction_argument(src)}\n"
        return ""

    def produce_c_data_single_(self, data: Data) -> tuple[str, str, int]:
        """It takes an assembler data and returns a C++ object.

        :param data: The data to be converted
        :return: data value, declaration, size
        """
        # Real conversion
        internal_data_type = data.getinttype()
        self.element_size = data.getsize()

        logging.debug(f"current data type = {internal_data_type}")
        rc, rh = self.__type_table[internal_data_type](data)

        logging.debug(rc)
        logging.debug(rh)
        return rc, rh, data.getsize()

    def produce_c_data_number(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = "".join(str(i) if isinstance(i, int) else "".join(str(x) for x in self.visit(i)) for i in r)
        rh = f"{data_ctype} {label}"
        return rc, rh

    def produce_c_data_array(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, _ = data.getdata()
        if not any(r):  # all zeros
            r = [0]
        rc = "{"
        for i, v in enumerate(r):
            if i != 0:
                rc += ","
            if isinstance(v, op.Data):
                c = self.produce_c_data_single_(v)[0]
                rc += c
            elif isinstance(v, lark.Tree):
                rc += "".join(self.visit(v))
            elif isinstance(v, list):
                l = [str(i) for i in v]
                rc += "".join(l)
            else:
                rc += str(v)
        rc += "}"
        rh = f"{data_ctype} {label}[{elements}]"
        return rc, rh

    def produce_c_data_zero_string(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, size = data.getdata()
        r = flatten(r)
        rc = '"' + "".join(self.convert_str(i) for i in r[:-1]) + '"'
        rc = re.sub(r"(\\x[0-9a-f][0-9a-f])([0-9a-fA-F])", r'\g<1>" "\g<2>', rc)  # fix for stupid C hex escapes: \xaef
        rh = f"char {label}[{size}]"
        return rc, rh

    def produce_c_data_array_string(self, data: op.Data) -> tuple[str, str]:
        label, data_ctype, _, r, elements, size = data.getdata()
        r = flatten(r)
        rc = "{" + ",".join([self.convert_char(i) for i in r]) + "}"
        rh = f"char {label}[{size}]"
        return rc, rh

    def produce_c_data_object(self, data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = []
        for i in data.getmembers():
            c, _, _ = self.produce_c_data_single_(i)
            rc += [c]
        rc = "{" + ",".join(rc) + "}"
        rh = f"{data_ctype} {label}"
        return rc, rh

    def convert_char(self, c: Union[int, str]) -> str:
        if isinstance(c, int) and c not in [10, 13]:
            return str(c)
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

            if c in ["\'", '\"', "\\"]:
                vvv = "\\" + c
            elif ord(c) > 127:
                t = c.encode("cp437", "backslashreplace")
                vvv = "\\" + hex(ord(t))[1:]
            elif c == "\0":
                vvv = "\\0"
            else:
                vvv = c
        return vvv

    def produce_global_jump_table(self, globals, itislst):
        # Produce call table
        if itislst:
            result = """
 bool __dispatch_call(m2c::_offsets __i, struct m2c::_STATE* _state){
    X86_REGREF
    if ((__i>>16) == 0) {__i |= ((dd)cs) << 16;}
    __disp=__i;
    switch (__i) {
"""
        else:
            result = """
 bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state){
    switch (__disp) {
"""
        entries = OrderedDict()
        for k, v in globals:
            if isinstance(v, proc_module.Proc) and v.used:
                k = re.sub(r"[^A-Za-z0-9_]", "_", k)  # need to do it during mangling
                entries[k] = (self.cpp_mangle_label(k), "0")
                labels = v.provided_labels

                entries.update({label: (v.name, "__disp") for label in set(labels) if label != v.name})

        # for name in procs:
        #    if not name.startswith('_group'):  # TODO remove dirty hack. properly check for group

        names = self.leave_unique_labels(entries.keys())
        for name in sorted(names):
            result += "        case m2c::k{}: \t{}({}, _state); break;\n".format(name, *entries[name])

        result += "        default: m2c::log_error(\"Don't know how to call to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(); abort();\n"
        result += "     };\n     return true;\n}\n"
        return result

    def _mov(self, dst: Expression, src: Expression) -> str:
        self.a, self.b = self.parse2(dst, src)
        mapped_memory_access = "raddr" in self.a or "raddr" in self.b
        if mapped_memory_access:
            return f"MOV({self.a}, {self.b})"
        return f"{self.a} = {self.b};"

    def produce_jump_table_c(self, offsets):
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

    def cpp_mangle_label(self, name: str) -> str:
        name = mangle_asm_labels(name)
        return name.lower()

    def produce_number_c(self, expr: str, radix: int, sign: str, value: str) -> str:
        if radix == 10:
            return f"{sign}{value}"
        elif radix == 16:
            return f"{sign}0x{value}"
        elif radix == 2:
            return f"{sign}{hex(int(value, 2))}"
        elif radix == 8:
            return f"{sign}0{value}"
        else:
            return str(int(expr, radix))



    def INTEGER(self, t: Token) -> list[str]:
        return [self.produce_number_c("", t.start_pos, t.line, t.column)]

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
        self._indirection = tree.indirection

        origexpr = tree.children[0]
        while isinstance(origexpr, list) and origexpr:
            origexpr = origexpr[0]

        single = len(tree.children) == 1
        self._isjustlabel = self._check_for_just_label(origexpr, single)
        self._isjustmember = single and isinstance(origexpr, lark.Tree) and origexpr.data == MEMBERDIR

        if self.itiscall and tree.mods & {"near", "far"}: # and self._isjustlabel:
            tree.indirection = self._indirection = IndirectionType.VALUE

        self.element_size = tree.element_size
        self._ismember = False
        self._need_pointer_to_member = False
        result = "".join(self.visit(tree.children))
        tree.indirection = self._indirection

        if tree.indirection == IndirectionType.POINTER and tree.ptr_size == 0 and hasattr(self,"variable_size"):  # [ var ]
            tree.ptr_size = self.variable_size  # Set destination size based on variable size
        self.size_changed = self.size_changed or "size_changed" in tree.mods and self._middle_size != tree.size()

        if tree.indirection == IndirectionType.POINTER and tree.registers.intersection({"bp", "ebp", "sp", "esp"}):
            self._work_segment = "ss"  # and segment is not overriden means base is "ss:"

        if self._need_pointer_to_member:
            result = result[:-1] if result[-1] == "+" else result
            result = result.replace("++", "+").replace("+-", "-")
            result = f"{result}+{self._need_pointer_to_member[0]}))->{'.'.join(self._need_pointer_to_member[1:])}"

        if tree.indirection == IndirectionType.POINTER and not self._ismember and (
                not self._isjustlabel or self.size_changed):
            result = self.convert_sqbr_reference(tree.segment_register, result, "destination" in tree.mods,
                                                 tree.ptr_size, False, lea="lea" in tree.mods)
        if self._ismember:
            result = f"(({self.struct_type}*)raddr({self._work_segment},{result}"
        if self.needs_dereference:
            self.needs_dereference = False
            result = (
                f"*{result}"
                if result[0] == "(" and result[-1] == ")"
                else f"*({result})"
            )
        return result

    def _check_for_just_label(self, origexpr, single):
        return single and ((isinstance(origexpr, lark.Token) and origexpr.type == LABEL)
                           or (isinstance(origexpr, lark.Token) and origexpr.type == SQEXPR
                               and isinstance(origexpr.children,
                                              lark.Token) and origexpr.children.type == LABEL)
                           or (isinstance(origexpr, lark.Tree) and origexpr.data == MEMBERDIR))

    def data(self, data: Data) -> tuple[str, str, int]:
        binary_width = self._context.typetosize(data.data_type)  # TODO pervertion
        self.is_data = binary_width
        # For unit test
        from masm2c.parser import Parser
        Parser.c_dummy_label = 0
        c, h, size = self.produce_c_data_single_(data)
        c += f", // {data.getlabel()}" + "\n"
        h += ";\n"
        self.is_data = False
        return c, h, size

    def LABEL(self, token: Token) -> list[Union[str, Token]]:
        if self.is_data:
            size = self.is_data if type(self.is_data) == int else 0
            return [self.convert_label_data(token, size=size)]
        return [self.convert_label_(token)]

    def convert_label_data(self, v: Token, size: int=0) -> Union[Token, str]:
        logging.debug("convert_label_data(%s)", v)
        size = size or 2
        if (g := self._context.get_global(v)) is None:
            return v
        if isinstance(g, op.var):
            if g.issegment:
                v = f"seg_offset({g.name})"
            elif size == 2:
                v = f"offset({g.segment},{g.name})"
            elif size == 4:
                v = f"far_offset({g.segment},{g.name})"
            else:
                logging.error(f"Some unknown data size {size} for {g.name}")
        elif isinstance(g, (op._equ, op._assignment)):
            v = g.original_name
        elif isinstance(g, (op.label, proc.Proc)):
            v = f"m2c::k{g.name.lower()}"
        elif not isinstance(g, op.Struct):
            v = g.offset
        logging.debug(v)
        return v

    def offsetdir(self, tree: Tree) -> list[Union[str, Token]]:  # TODO equ, assign support
        name = tree.children[0]

        if isinstance(name, lark.Tree) and name.data=="memberdir":
            label = name.children
            if (g := self._context.get_global(label[0])) is None:
                return label

            value = self.convert_member_offset(g, label)
            return [lark.Token("memberdir", value)]

        if (g := self._context.get_global(name)) is None:
            return [name]
        if isinstance(g, op.var):
            logging.debug("it is var %s", g.size)
            if self.element_size == 2:
                return [f"offset({g.segment},{g.name})"]
            elif self.element_size == 4:
                return [f"far_offset({g.segment},{g.name})"]
            else:
                raise ValueError("Unknown offset size %s", self.element_size)
        elif isinstance(g, (proc_module.Proc, op.label)):
            logging.debug("it is proc")
            return [f"m2c::k{g.name}"]
        else:
            raise ValueError("Unknown type for offsetdir %s", type(g))

    def notdir(self, tree: Tree) -> list[Union[str, Token]]:
        return ["~", *tree.children]

    def ordir(self, tree: Tree) -> list[Union[str, Token]]:
        return [tree.children[0], " | ", tree.children[1]]

    def xordir(self, tree):
        return [tree.children[0], " ^ ", tree.children[1]]

    def anddir(self, tree):
        return [tree.children[0], " & ", tree.children[1]]

    def sizearg(self, tree: Tree) -> list[str]:
        return [f"sizeof({tree.children[0]})"]


IR2Cpp = Cpp
"""
class IR2Cpp(TopDownVisitor, Cpp):

    def __init__(self, parser):
        super(IR2Cpp, self).__init__(context=parser)
"""


if __name__ == "__main__":
    import doctest
    doctest.testmod()
