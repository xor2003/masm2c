from __future__ import absolute_import
from __future__ import print_function

import logging
import re
from builtins import object
from builtins import range
from builtins import str

from masm2c.Token import Token
from masm2c import op

label_re = re.compile(r'^([\S@]+)::?(.*)$')  # speed
PTRDIR = 'ptrdir'


class Proc(object):
    last_addr = 0xc000
    elements = 1  # how many

    def __init__(self, name, far=False, line_number=0, extern=False, id=0):
        self.name = name
        self.original_name = name
        #self.__calls = []
        self.stmts = []
        self.labels = set()
        self.retlabels = set()
        self.offset = Proc.last_addr
        Proc.last_addr += 4
        self.line_number = line_number
        self.far = far
        self.used = False
        self.extern = extern

    def add_label(self, label, proc, line_number=0):
        self.stmts.append(op.label(label, proc=proc, line_number=line_number))
        self.labels.add(label)



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
    '''

    def parse_extract_label(self, stmt):
        r = label_re.search(stmt)
        if r:
            logging.info("add label %s" % r.group(1))
            # label
            self.add_label(r.group(1).lower(), self)
            # print "remains: %s" %r.group(2)
            stmt = r.group(2).strip()
        return stmt

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
                cl = getattr(op, '_instruction'+str(len(args)))
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
        #value = cpp.convert_number_to_c(value)
        ptrdir = Token.find_tokens(value, PTRDIR)
        if ptrdir:
            o.original_type = ptrdir[0].value.lower()

        o.raw_line = str(line_number) + " " + label + " equ " + str(value)
        o.line_number = line_number
        o.cmd = o.raw_line
        o.value = value
        #               logging.info "~~~" + o.command + o.comments
        return o

    def create_assignment_op(self, label, value, line_number=0):
        logging.debug(label + " " + str(value))
        #value = cpp.convert_number_to_c(value)
        o = op._assignment([label, value])
        ptrdir = Token.find_tokens(value, PTRDIR)
        if ptrdir:
            o.original_type = ptrdir[0].value.lower()

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

    def visit(self, visitor, skip=0):
        for i in range(skip, len(self.stmts)):
            stmt = self.stmts[i]
            from masm2c.cpp import InjectCode, SkipCode
            try:
                s = self.generate_c_cmd(visitor, stmt)
                visitor.body += s
            except InjectCode as ex:
                logging.debug(f'Injecting code {ex.cmd} before {stmt}')
                s = self.generate_c_cmd(visitor, ex.cmd)
                visitor.body += s
                s = self.generate_c_cmd(visitor, stmt)
                visitor.body += s
            except SkipCode:
                logging.debug(f'Skipping code {stmt}')
            except Exception as ex:
                logging.error(f'Exception in {stmt.filename}:{stmt.line_number} {stmt.raw_line}\n {ex.args}')
                raise


            try:  # trying to add command and comment
                if stmt.raw_line or stmt.line_number != 0:
                    visitor.body = visitor.body[:-1] + "\t// " + str(stmt.line_number) \
                                   + " " + stmt.raw_line + "\n"
            except AttributeError:
                logging.warning(f"Some attributes missing while setting comment for {stmt}")

    def generate_c_cmd(self, visitor, stmt):
        s = stmt.visit(visitor)
        return s
