from __future__ import absolute_import
from __future__ import print_function

import logging
import re
from builtins import object
from builtins import range
from builtins import str

from masm2c.Token import Token
from masm2c import op

# label_re = re.compile(r'^([\S@]+)::?(.*)$')  # speed
PTRDIR = 'ptrdir'


class Proc(object):
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
        self.provided_labels = set([name])
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
        self.stmts.append(label)
        self.provided_labels.add(name)

    def optimize(self, keep_labels=[]):
        logging.info("optimizing...")
        # trivial simplifications

    '''
    def action_instruction(self, stmt):
        # print stmt
        # comment = stmt.find(';')
        # comments = ""
        # if comment >= 0:
        #       comments = stmt[comment:]
        stmt = stmt.strip()
        #line = stmt

        stmt = self.parse_extract_label(stmt)

        if len(stmt) == 0:
            return

        o = self.split_create_instruction(stmt)
        # o.line = line
        # o.line_number = line_number
        # self.stmts.append(o)
        return o

    def parse_extract_label(self, stmt):
        r = label_re.search(stmt)
        if r:
            logging.info("add label %s" % r.group(1))
            # label
            self.add_label(r.group(1).lower(), self)
            # print "remains: %s" %r.group(2)
            stmt = r.group(2).strip()
        return stmt
    '''

    def split_create_instruction(self, stmt):
        # s = [stmt.replace("\x00", " ") for stmt in
        #     re.sub('["\'].+?["\']', lambda m: m.group(0).replace(" ", "\x00"), stmt).split()]
        s = stmt.split()
        o = self.create_instruction_object(s[0], s[1:])
        return o

    def create_instruction_object(self, instruction, args=[]):
        cl = self.find_op_class(instruction, args)
        # print "args %s" %s[1:]
        # arg = " ".join(args) if len(args) > 0 else ""
        o = cl(args)
        # o.comments = comments
        o.cmd = instruction.lower()
        # logging.info("~1~2~ " + o.command + " ~ " + o.cmd)
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
        except:
            raise Exception("unknown command: " + cmd.lower())
        return cl

    def add_equ(self, label, value, line_number=0):  # only for tests. to remove
        o = Proc.create_equ_op(label, value, line_number)
        self.stmts.append(o)

    @staticmethod
    def create_equ_op(label, value, line_number):  # TODO Move it to parser
        logging.debug(label + " " + str(value))
        o = op._equ([label, value])
        # value = cpp.convert_number_to_c(value)
        ptrdir = Token.find_tokens(value, PTRDIR)
        if ptrdir:
            if isinstance(ptrdir[0], Token):
                o.original_type = ptrdir[0].value.lower()
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
        ptrdir = Token.find_tokens(value, PTRDIR)
        if ptrdir:
            if isinstance(ptrdir[0], Token):
                o.original_type = ptrdir[0].value.lower()
            elif isinstance(ptrdir[0], str):
                o.original_type = ptrdir[0].lower()

        o.raw_line = str(line_number) + " " + label + " = " + str(value)
        o.line_number = line_number
        o.cmd = o.raw_line
        o.value = value

        #               logging.info "~~~" + o.command + o.comments
        return o

    def __str__(self):
        r = []
        for i in self.stmts:
            r.append(i.__str__())
        return "\n".join(r)

    def enrich_command(self, stmt, full_command):
        def expr_is_register(e):
            return isinstance(e, Token) and isinstance(e.value, Token) and e.value.type in ['register',
                                                                                            'segmentregister']

        def cmd_wo_args(stmt):
            return len(stmt.args) == 0

        def cmd_impacting_only_registers(stmt):
            return (cmd_wo_args(stmt) or \
                stmt.cmd in ['cmp', 'test'] or \
                (stmt.cmd != 'xchg' and len(stmt.args) >= 1 and expr_is_register(stmt.args[0]) or \
                (stmt.cmd == 'xchg' and expr_is_register(stmt.args[0]) and expr_is_register(stmt.args[1])))) and \
                not stmt.cmd.startswith('push') and not stmt.cmd.startswith('pop') and not stmt.cmd.startswith('stos') and \
                not stmt.cmd.startswith('movs')

        def expr_is_mov_ss(e):
            return stmt.cmd in ['mov', 'pop'] and \
                   isinstance(e, Token) and isinstance(e.value, Token) and e.value.type == 'segmentregister' and \
                   e.value.type == 'ss'

        if self.is_flow_change_stmt(stmt) or stmt.cmd in ['out', 'in'] or expr_is_mov_ss(stmt):
            trace_mode = 'R'  # trace only. external impact or execution point change
        elif cmd_impacting_only_registers(stmt):
            trace_mode = 'T'  # compare execution with dosbox. registers only impact
        else:
            trace_mode = 'X'  # compare execution with dosbox. memory impact

        result = "\t" + trace_mode + "(" + full_command + ");"
        return result

    def visit(self, visitor, skip=0):
        for i in range(skip, len(self.stmts)):
            stmt = self.stmts[i]
            from masm2c.cpp import InjectCode, SkipCode
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
        visitor.label = ''
        visitor.dispatch = ''
        visitor.prefix = ''
        command = self.generate_c_cmd(visitor, stmt)
        if command and stmt.real_seg:  # and (self.is_flow_change_stmt(stmt) or 'cs' in command or 'cs' in visitor.before):
            visitor.body += f'cs={stmt.real_seg:#04x};eip={stmt.real_offset:#08x}; '
        full_command = prefix + command
        if full_command:
            full_command = self.enrich_command(stmt, full_command)
        full_line = visitor.label + visitor.dispatch + full_command
        return full_line

    def generate_c_cmd(self, visitor, stmt):
        s = stmt.visit(visitor)
        return s

    def if_terminated_proc(self):
        '''Check if proc was terminated with jump or ret to know if execution flow contiues across function end'''
        if self.stmts:
            last_stmt = self.stmts[-1]
            return self.is_flow_terminating_stmt(last_stmt)
        return True

    def is_flow_terminating_stmt(self, last_stmt):
        return last_stmt.cmd.startswith('jmp') or last_stmt.cmd.startswith('ret') or last_stmt.cmd == 'iret'

    def is_return_point(self, stmt):
        return stmt.cmd.startswith('call')

    def is_flow_change_stmt(self, stmt):
        return stmt.cmd.startswith('j') or stmt.cmd.startswith('int') or stmt.cmd == 'iret' \
               or stmt.cmd.startswith('ret') or stmt.cmd.startswith('call') or stmt.cmd.startswith('loop')
