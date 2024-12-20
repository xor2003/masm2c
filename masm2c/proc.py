"""
Deals with procedures (functions) in assembly code.
"""
# Masm2c S2S translator (initially based on SCUMMVM tasmrecover))
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
from __future__ import annotations

import logging
import re
from typing import Any, TYPE_CHECKING, ClassVar, Optional

from lark import lark

from masm2c.op import _assignment, _equ, baseop, label
from masm2c.Token import Expression

from . import op
from .Token import Token

if TYPE_CHECKING:
    from .cpp import Cpp

PTRDIR = "ptrdir"


class Proc:
    """The Proc class stores information about each procedure, such as its name, arguments, and the instructions it contains."""

    last_addr: ClassVar = 0xc000

    def __init__(self, name: str, far: bool = False, line_number: int = 0, extern: bool = False, offset: int | None=0,
                 real_offset: int | None=0,
                 real_seg: int | None=0, segment: str="") -> None:
        """Represent asm procedure.

        :param name: Name
        :param far: is Far proc?
        :param line_number: Original line number
        :param extern: is Extern proc?
        """
        self.name = name
        self.original_name = name

        self.stmts: list[baseop] = []
        self.provided_labels = {name}
        self.line_number = line_number
        self.far = far
        self.used = False
        self.extern = extern
        self.used_labels: set[str] = set()
        self.group = None
        self.segment = segment
        self.to_group_with: set[str] = set()

        self.offset = offset or Proc.last_addr
        Proc.last_addr += 4
        self.real_offset, self.real_seg = real_offset, real_seg

    def merge_two_procs(self, newname: str, other: Proc):
        self.name, self.original_name = newname, newname
        self.stmts += other.stmts
        self.provided_labels |= other.provided_labels
        self.used_labels |= other.used_labels
        self.extern = other.extern
        del other

    def add_label(self, name: str, label: label) -> None:
        logging.debug("Label %s is provided by %s proc", name, self.name)
        self.stmts.append(label)
        self.provided_labels.add(name)

    def optimize(self, keep_labels=None):
        logging.info("optimizing...")
        # trivial simplifications


    def create_instruction_object(self, instruction: str, args: Optional[list[Expression]] = None) -> baseop:
        """:param instruction: the instruction name
        :param args: a list of strings, each string is an argument to the instruction
        :return: An object of type cl, which is a subclass of Instruction.
        """
        if args is None:
            args = []
        assert all(isinstance(arg, Expression) for arg in args)
        cl = self.find_op_class(instruction, args)
        o = cl(args)
        o.cmd = instruction.lower()
        o.syntetic = False
        return o

    def find_op_class(self, cmd: lark.Token, args: list[Expression]) -> Any:
        if hasattr(op, f"_{cmd.lower()}"):
            cl = getattr(op, f"_{cmd.lower()}")
        else:
            cl = self.find_op_common_class(cmd, args)
        return cl

    def find_op_common_class(self, cmd: str, args: list[Expression]) -> type[baseop]:
        logging.debug(cmd)
        try:
            cl = (
                op._jump
                if re.match("^(j[a-z]+|loop[a-z]*)$", cmd.lower())
                else getattr(op, f"_instruction{len(args)}")
            )
        except AttributeError as e:
            raise Exception(f"Unknown instruction: {cmd.lower()}") from e
        return cl

    def add_equ(self, label, value, line_number=0):  # only for tests. to remove
        o = Proc.create_equ_op(label, value, line_number)
        self.stmts.append(o)

    @staticmethod
    def create_equ_op(label: str, value: Expression, line_number: int) -> _equ:  # TODO Move it to parser
        logging.debug("%s %s", label, value)
        o = op._equ(label)
        if ptrdir := Token.find_tokens(value, PTRDIR):
            if isinstance(ptrdir[0], Token):
                assert isinstance(ptrdir[0].children, str)
                o.original_type = ptrdir[0].children.lower()
            elif isinstance(ptrdir[0], str):
                o.original_type = ptrdir[0].lower()

        o.raw_line = f"{line_number} {label} equ {value!s}"
        o.line_number = line_number
        o.cmd = o.raw_line
        o.value = value
        #               logging.info "~~~" + o.command + o.comments
        return o

    def create_assignment_op(self, label: str, value: Expression, line_number: int=0) -> _assignment:
        logging.debug("%s %s", label, value)
        o = op._assignment([label, value])
        if hasattr(value, "original_type"):  # TODO cannot get original type anymore. not required here
            o.original_type = value.original_type

        o.raw_line = f"{line_number} {label} = {value!s}"
        o.line_number = line_number
        o.cmd = o.raw_line
        o.value = value

        #               logging.info "~~~" + o.command + o.comments
        return o

    def __str__(self) -> str:
        return "\n".join(i.__str__() for i in self.stmts)

    def set_instruction_compare_subclass(self, stmt: baseop, full_command: str, itislst: bool) -> str:
        """Sets libdosbox's emulator the instruction subclass
        to perform comparison of instruction side effects at run-time with the emulated.
        """

        def expr_is_register(e):
            return isinstance(e, lark.Tree) and isinstance(e.children, list) and len(e.children) == 1 and \
                isinstance(e.children[0], lark.Tree) and e.children[0].data in {"register", "segmentregister"}

        def cmd_wo_args(stmt):
            return len(stmt.children) == 0

        def cmd_impacting_only_registers(stmt):
            return (cmd_wo_args(stmt) or \
                    stmt.cmd in {"cmp", "test"} or \
                    (stmt.cmd != "xchg" and len(stmt.children) >= 1 and expr_is_register(stmt.children[0]) or \
                     (stmt.cmd == "xchg" and expr_is_register(stmt.children[0]) and expr_is_register(stmt.children[1])))) and \
                not stmt.cmd.startswith("push") and not stmt.cmd.startswith("pop") and not stmt.cmd.startswith("stos") and \
                not stmt.cmd.startswith("movs")

        def expr_is_mov_ss(e):
            return e.cmd == "mov" and \
                   isinstance(e.children[0], lark.Tree) and isinstance(e.children[0].children[0], lark.Tree) and \
                e.children[0].children[0].data == "segmentregister" and \
                   e.children[0].children[0].children[0] == "ss"

        if self.is_flow_change_stmt(stmt) and not stmt.syntetic:
            trace_mode = "J"  # check for proper jump
        elif not itislst or stmt.syntetic:
            trace_mode = "R"  # trace only
        elif stmt.cmd.startswith("int") or stmt.cmd in {"out", "in"} or expr_is_mov_ss(stmt):
            trace_mode = "S"  # check for self-modification
        elif cmd_impacting_only_registers(stmt):
            trace_mode = "T"  # compare execution with dosbox. registers only impact
        else:
            trace_mode = "X"  # compare execution with dosbox. memory impact

        result = "\t" + trace_mode + "(" + full_command + ");"
        return result

    def visit(self, visitor: Cpp, skip=0):
        for i in range(skip, len(self.stmts)):
            stmt = self.stmts[i]
            from .gen import InjectCode, SkipCode
            try:
                full_line = self.generate_full_cmd_line(visitor, stmt)
                visitor.body += full_line
            except InjectCode as ex:
                logging.debug("Injecting code %s before %s", ex.cmd, stmt)
                s = self.generate_full_cmd_line(visitor, ex.cmd)
                visitor.body += s
                s = self.generate_full_cmd_line(visitor, stmt)
                visitor.body += s
            except SkipCode:
                logging.debug("Skipping code %s", stmt)
            except Exception as ex:
                logging.exception(f"Exception {ex.args}")
                logging.exception(f" in {stmt.filename}:{stmt.line_number} {stmt.raw_line}")
                raise

            try:  # trying to add command and comment
                if stmt.raw_line or stmt.line_number != 0:
                    visitor.body += "\t// " + str(stmt.line_number) \
                                   + " " + stmt.raw_line + "\n"
            except AttributeError:
                logging.warning(f"Some attributes missing while setting comment for {stmt}")

    def generate_full_cmd_line(self, visitor: Cpp, stmt: baseop) -> str:
        prefix = visitor.prefix
        visitor._cmdlabel = ""
        visitor.dispatch = ""
        visitor.prefix = ""
        #if stmt:= tuple(visitor.visit(stmt)):
        command = stmt.accept(visitor)
        if command and stmt.real_seg:  # and (self.is_flow_change_stmt(stmt) or 'cs' in command or 'cs' in visitor.before):
            visitor.body += f"cs={stmt.real_seg:#04x};eip={stmt.real_offset:#08x}; "

        full_command = prefix + command

        if full_command:
            full_command = self.set_instruction_compare_subclass(stmt, full_command, visitor._context.itislst)

        return visitor._cmdlabel + visitor.dispatch + full_command

    def generate_c_cmd(self, visitor: Cpp, stmt: baseop) -> str:
        return stmt.accept(visitor)

    def if_terminated_proc(self):
        """Check if proc was terminated with jump or ret to know if execution flow continues across function end."""
        if self.stmts:
            last_stmt = self.stmts[-1]
            return self.is_flow_terminating_stmt(last_stmt)
        return True

    def is_flow_terminating_stmt(self, stmt: baseop) -> bool:
        return (stmt.cmd.startswith("jmp") and "$" not in stmt.raw_line) \
               or stmt.cmd.startswith("ret") or stmt.cmd == "iret"

    def is_return_point(self, stmt):
        return stmt.cmd.startswith("call")

    def is_flow_change_stmt(self, stmt: baseop) -> bool:
        return stmt.cmd.startswith("j") or self.is_flow_terminating_stmt(stmt) \
               or stmt.cmd.startswith("call") or stmt.cmd.startswith("loop")
