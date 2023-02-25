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
import re
from builtins import range, str

from . import op
from .Token import Token

# label_re = re.compile(r'^([\S@]+)::?(.*)$')  # speed

PTRDIR = 'ptrdir'


class Proc:
    last_addr = 0xc000
    elements = 1  # how many

    def __init__(self, name: str, far: bool = False, line_number: int = 0, extern: bool = False, offset=0,
                 real_offset=0,
                 real_seg=0, segment=''):
        '''
        Represent asm procedure

        :param name: Name
        :param far: is Far proc?
        :param line_number: Original line number
        :param extern: is Extern proc?
        '''
        self.name = name
        self.original_name = name

        self.stmts = []
        self.provided_labels = {name,}
        self.line_number = line_number
        self.far = far
        self.used = False
        self.extern = extern
        self.used_labels = set()
        self.group = None
        self.segment = segment

        if offset:
            self.offset = offset
        else:
            self.offset = Proc.last_addr
        Proc.last_addr += 4
        self.real_offset, self.real_seg = real_offset, real_seg
        # self.retlabels = set()

    def merge_two_procs(self, newname, other):
        self.name, self.original_name = newname, newname
        self.stmts += other.stmts
        self.provided_labels |= other.provided_labels
        self.used_labels |= other.used_labels
        self.extern = other.extern
        # self.group = None
        del other

    def add_label(self, name, label):
        logging.debug(f"Label {name} is provided by {self.name} proc")
        self.stmts.append(label)
        self.provided_labels.add(name)

    def optimize(self, keep_labels=None):
        logging.info("optimizing...")
        # trivial simplifications


    def create_instruction_object(self, instruction, args=None):
        """
        :param instruction: the instruction name
        :param args: a list of strings, each string is an argument to the instruction
        :return: An object of type cl, which is a subclass of Instruction.
        """
        if args is None:
            args = []
        cl = self.find_op_class(instruction, args)
        o = cl(args)
        o.cmd = instruction.lower()
        o.syntetic = False
        return o

    def find_op_class(self, cmd, args):
        try:
            cl = getattr(op, '_' + cmd.lower())
        except AttributeError:
            cl = self.find_op_common_class(cmd, args)
        return cl

    def find_op_common_class(self, cmd, args):
        logging.debug(cmd)
        try:
            if re.match(r"^(j[a-z]+|loop[a-z]*)$", cmd.lower()):
                cl = getattr(op, '_jump')
            else:
                cl = getattr(op, '_instruction' + str(len(args)))
        except AttributeError:
            raise Exception("Unknown instruction: " + cmd.lower())
        return cl

    def add_equ(self, label, value, line_number=0):  # only for tests. to remove
        o = Proc.create_equ_op(label, value, line_number)
        self.stmts.append(o)

    @staticmethod
    def create_equ_op(label, value, line_number):  # TODO Move it to parser
        logging.debug(label + " " + str(value))
        o = op._equ([label, value])
        # value = cpp.convert_number_to_c(value)
        if ptrdir := Token.find_tokens(value, PTRDIR):
            if isinstance(ptrdir[0], Token):
                o.original_type = ptrdir[0].children.lower()
            elif isinstance(ptrdir[0], str):
                o.original_type = ptrdir[0].lower()

        o.raw_line = str(line_number) + " " + label + " equ " + str(value)
        o.line_number = line_number
        o.cmd = o.raw_line
        o.value = value
        #               logging.info "~~~" + o.command + o.comments
        return o

    def create_assignment_op(self, label, value, line_number=0):
        logging.debug(label + " " + str(value))
        # value = cpp.convert_number_to_c(value)
        o = op._assignment([label, value])
        if hasattr(value, 'original_type'):  # TODO cannot get original type anymore. not required here
            o.original_type = value.original_type

        o.raw_line = str(line_number) + " " + label + " = " + str(value)
        o.line_number = line_number
        o.cmd = o.raw_line
        o.value = value

        #               logging.info "~~~" + o.command + o.comments
        return o

    def __str__(self):
        return "\n".join((i.__str__() for i in self.stmts))

    def set_instruction_compare_subclass(self, stmt, full_command, itislst):
        """Sets libdosbox's emulator the instruction subclass
        to perform comparison of instruction side effects at run-time with the emulated"""

        def expr_is_register(e):
            return isinstance(e, Token) and isinstance(e.children, Token) and e.children.data in {'register',
                                                                                            'segmentregister'}

        def cmd_wo_args(stmt):
            return len(stmt.children) == 0

        def cmd_impacting_only_registers(stmt):
            return (cmd_wo_args(stmt) or \
                    stmt.cmd in {'cmp', 'test'} or \
                    (stmt.cmd != 'xchg' and len(stmt.children) >= 1 and expr_is_register(stmt.children[0]) or \
                     (stmt.cmd == 'xchg' and expr_is_register(stmt.children[0]) and expr_is_register(stmt.children[1])))) and \
                not stmt.cmd.startswith('push') and not stmt.cmd.startswith('pop') and not stmt.cmd.startswith('stos') and \
                not stmt.cmd.startswith('movs')

        def expr_is_mov_ss(e):
            return e.cmd == 'mov' and \
                   isinstance(e.children[0], Token) and isinstance(e.children[0].children, Token) and e.children[0].children.data == 'segmentregister' and \
                   e.children[0].children.children == 'ss'

        if self.is_flow_change_stmt(stmt) and not stmt.syntetic:
            trace_mode = 'J'  # check for proper jump
        elif not itislst or stmt.syntetic:
            trace_mode = 'R'  # trace only
        elif stmt.cmd.startswith('int') or stmt.cmd in {'out', 'in'} or expr_is_mov_ss(stmt):
            trace_mode = 'S'  # check for self-modification
        elif cmd_impacting_only_registers(stmt):
            trace_mode = 'T'  # compare execution with dosbox. registers only impact
        else:
            trace_mode = 'X'  # compare execution with dosbox. memory impact

        result = "\t" + trace_mode + "(" + full_command + ");"
        return result

    def visit(self, visitor, skip=0):
        for i in range(skip, len(self.stmts)):
            stmt = self.stmts[i]
            from .gen import InjectCode
            from .gen import SkipCode
            try:
                full_line = self.generate_full_cmd_line(visitor, stmt)
                visitor.body += full_line
            except InjectCode as ex:
                logging.debug(f'Injecting code {ex.cmd} before {stmt}')
                s = self.generate_full_cmd_line(visitor, ex.cmd)
                visitor.body += s
                s = self.generate_full_cmd_line(visitor, stmt)
                visitor.body += s
            except SkipCode:
                logging.debug(f'Skipping code {stmt}')
            except Exception as ex:
                logging.error(f'Exception {ex.args}')
                logging.error(f' in {stmt.filename}:{stmt.line_number} {stmt.raw_line}')
                raise

            try:  # trying to add command and comment
                if stmt.raw_line or stmt.line_number != 0:
                    visitor.body += "\t// " + str(stmt.line_number) \
                                   + " " + stmt.raw_line + "\n"
            except AttributeError:
                logging.warning(f"Some attributes missing while setting comment for {stmt}")

    def generate_full_cmd_line(self, visitor, stmt):
        prefix = visitor.prefix
        visitor._cmdlabel = ''
        visitor.dispatch = ''
        visitor.prefix = ''
        if stmt:= tuple(visitor.visit(stmt)):
            command = stmt.accept(visitor)
        else:
            command = ''
        if command and stmt.real_seg:  # and (self.is_flow_change_stmt(stmt) or 'cs' in command or 'cs' in visitor.before):
            visitor.body += f'cs={stmt.real_seg:#04x};eip={stmt.real_offset:#08x}; '

        full_command = prefix + command

        if full_command:
            full_command = self.set_instruction_compare_subclass(stmt, full_command, visitor._context.itislst)

        full_line = visitor._cmdlabel + visitor.dispatch + full_command
        return full_line

    def generate_c_cmd(self, visitor, stmt):
        return stmt.accept(visitor)

    def if_terminated_proc(self):
        '''Check if proc was terminated with jump or ret to know if execution flow continues across function end'''
        if self.stmts:
            last_stmt = self.stmts[-1]
            return self.is_flow_terminating_stmt(last_stmt)
        return True

    def is_flow_terminating_stmt(self, stmt):
        from masm2c.cpp import Cpp
        return (stmt.cmd.startswith('jmp') and not Cpp.isrelativejump(stmt.raw_line)) \
               or stmt.cmd.startswith('ret') or stmt.cmd == 'iret'

    def is_return_point(self, stmt):
        return stmt.cmd.startswith('call')

    def is_flow_change_stmt(self, stmt):
        return stmt.cmd.startswith('j') or self.is_flow_terminating_stmt(stmt) \
               or stmt.cmd.startswith('call') or stmt.cmd.startswith('loop')
