from ast import literal_eval
''' Module to parse assembler source '''
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
from builtins import range, str
from collections import OrderedDict
from copy import deepcopy


import jsonpickle
from lark import lark

from . import cpp as cpp_module
from . import op
from .pgparser import LarkParser, Asm2IR, ExprRemover, AsmData2IR, BottomUpVisitor, \
    IncludeLoader
from .proc import Proc

from .Token import Token, Expression

INTEGERCNST = 'integer'
STRINGCNST = 'STRING'

class Vector:

    def __init__(self, *args):
        self.__value = args

    def __add__(self, vec):
        if vec is not None:
            self.__value = [a + b for a, b in zip(self.__value, vec)]
        return self

    def __mul__(self, other):
        self.__value = list(a * other for a in self)
        return self

    #@property
    #def value(self):
    #    return self.__value

    def __getitem__(self, item):
        return self.__value[item]

    def __repr__(self):
        return f"{self.__value}"

class ExprSizeCalculator(BottomUpVisitor):

    def __init__(self, element_size=0, **kwargs):
        super().__init__(**kwargs)
        #self.size = 0
        self.element_number = 0
        self.element_size = element_size
        self.kwargs = kwargs

    def expr(self, tree, size):
        if self.element_size:
            tree.element_size = self.element_size
        '''
        
        self.element_number += tree.element_number
        size += tree.size()
        #self.size += size
        '''
        ##return size + (tree.size(), tree.element_number)
        #return size + (self.element_size, tree.element_number)
        return Vector(tree.size(), tree.element_number)

    def dupdir(self, tree, size):
        #self.element_number += tree.repeat
        return size * tree.repeat

    def LABEL(self, token):  # TODO very strange, to replace
        context = self.kwargs['context']
        if context.has_global(token):
            g = context.get_global(token)
            if isinstance(g, (op._assignment, op._equ)):
                self.element_size = g.value.size()
                return Vector(self.element_size, 1)

    def memberdir(self, tree, size):
        label = tree.children
        context = self.kwargs['context']
        g = context.get_global(label[0])
        if isinstance(g, op.Struct):
            type = label[0]
        else:
            type = g.original_type

        try:
            for member in label[1:]:
                g = context.get_global(type)
                if isinstance(g, op.Struct):
                    g = g.getitem(member)
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
    """
    It reads the whole file and returns it as a string

    :param file_name: The name of the file to read
    :return: The content of the file.
    """
    logging.info("     Reading file %s...", file_name)
    with open(file_name, 'rt', encoding="cp437") as file:
        content = file.read()
    return content


def dump_object(value):
    """
    Represents object as string

    :param value: The object to dump
    :return: A string representation of the object.
    """
    stuff = str(value.__dict__)
    replacements = (
        (r'\n', ' '),
        (r'[{}]', ''),
        (r"'([A-Za-z_0-9]+)'\s*:\s*", r'\g<1>=')
    )
    for old, new in replacements:
        stuff = re.sub(old, new, stuff)
    stuff = value.__class__.__name__ + "(" + stuff + ")"
    return stuff


class Parser:
    c_dummy_label = 0

    def __init__(self, args=None, skip_binary_data: list = None):
        '''
        Assembler parser
        '''
        self.test_mode = False
        self.__globals = OrderedDict()
        # self.__offsets = OrderedDict()
        self.pass_number = 0

        self.__lex = LarkParser(context=self)

        # self.segments = OrderedDict()
        self.externals_vars = set()
        self.externals_procs = set()
        self.__files = set()
        self.itislst = False
        self.initial_procs_start = set()
        self.procs_start = set()

        if not args:
            class MyDummyObj: pass

            args = MyDummyObj()
            args.mergeprocs = 'separate'
        self.args = args

        self.next_pass(Parser.c_dummy_label)

    def next_pass(self, counter):
        '''
        Initializer for each pass

        :param counter: Labels id counter
        :return:
        '''
        self.pass_number += 1
        logging.info(f"     Pass number {self.pass_number}")
        Parser.c_dummy_label = counter

        self.procs_start = self.initial_procs_start
        self.segments = OrderedDict()
        self.flow_terminated = True
        self.need_label = True

        self.structures = OrderedDict()
        self.macro_names_stack = set()
        self.proc_list = []
        self.proc = None

        # self.__label_to_skip = skip_binary_data
        self.__offset_id = 0x1111
        self.__stack = []
        self.entry_point = "mainproc_begin"
        self.main_file = False
        self.__proc_stack = []

        self.__binary_data_size = 0
        self.__cur_seg_offset = 0
        self.__c_dummy_jump_label = 0
        self.__c_extra_dummy_jump_label = 0

        self.__segment_name = "default_seg"
        self.__segment = op.Segment(self.__segment_name, 0, comment="Artificial initial segment")
        self.segments[self.__segment_name] = self.__segment

        self.proc = self.add_proc("mainproc", '', 0, False)

        self.used = False

        self.radix = 10

        self.current_macro = None
        self.current_struct = None

        self.struct_names_stack = list()

        self._current_file = ''
        self.__current_file_hash = '0'

        self.data_merge_candidats = 0

        self.equs = set()

    '''
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
    '''

    def set_global(self, name, value):
        if len(name) == 0:
            raise NameError("empty name is not allowed")
        value.original_name = name
        name = name.lower()

        logging.debug("set_global(name='%s',value=%s)", name, dump_object(value))
        if name in self.__globals and self.pass_number == 1 and not self.test_mode:
            raise LookupError("global %s was already defined" % name)
        value.used = False
        self.__globals[name] = value

    def reset_global(self, name, value):
        if len(name) == 0:
            raise NameError("empty name is not allowed")
        value.original_name = name
        name = name.lower()
        logging.debug(f"reset global {name} -> {value}")
        self.__globals[name] = value

    def get_global(self, name):
        name = name.lower()
        logging.debug(f"get_global({name})")
        try:
            g = self.__globals[name]
            logging.debug(type(g))
        except KeyError:
            logging.debug(f"get_global KeyError {name}")
            raise
        g.used = True
        # assert self.__globals[name].used
        return g

    def get_globals(self):
        return self.__globals

    def has_global(self, name):
        name = name.lower()
        return name in self.__globals

    '''
    def set_offset(self, name, value):
        if len(name) == 0:
            raise NameError("empty name is not allowed")
        logging.debug("adding offset %s -> %s" % (name, value))
        if name in self.__offsets and self.pass_number == 1:
            raise LookupError("offset %s was already defined", name)
        self.__offsets[name] = value

    def get_offset(self, name):
        return self.__offsets[name.lower()]
    '''

    def replace_dollar_w_segoffst(self, v):
        logging.debug("$ = %d", self.__cur_seg_offset)
        return v.replace('$', str(self.__cur_seg_offset))

    @staticmethod
    def parse_int(v):
        # logging.debug "~1~ %s" %v
        if isinstance(v, list):
            vv = ""
            for i in v:
                try:
                    i = Parser.parse_int(i)
                except Exception:
                    pass
                vv += str(i)
            v = vv
        v = v.strip()
        # logging.debug "~2~ %s" %v
        if re.match(r'^[+-]?[0-8]+[OoQq]$', v):
            v = int(v[:-1], 8)
        # elif re.match(r'^[+-]?[0-9]+[Dd]?$', v):
        #    v = int(v[:-1], 10)
        elif re.match(r'^[+-]?[0-9][0-9A-Fa-f]*[Hh]$', v):
            v = int(v[:-1], 16)
        elif re.match(r'^[01]+[Bb]$', v):
            v = int(v[:-1], 2)
        # v = int(cpp.convert_number_to_c(v))

        try:
            vv = eval(v)
            v = vv
        except Exception:
            pass

        # logging.debug "~4~ %s" %v
        return int(v)

    def calculate_STRING_size(self, v):
        if not self.itislst:
            v = v.replace("\'\'", "'").replace('\"\"', '"')
        return len(v) - 2

    def get_global_value(self, v, size=2):  # TODO it is C++ specific. see convert_label()
        logging.debug("get_global_value(%s)", v)
        v = self.mangle_label(v)
        if not self.has_global(v):
            return v
        g = self.get_global(v)
        #logging.debug(g)
        if isinstance(g, (op._equ, op._assignment)):
            v = g.original_name
        elif isinstance(g, op.var):
            #size = g.size ## ?
            if g.issegment:
                v = f"seg_offset({g.name})"
            else:
                if size == 2:
                    v = f"offset({g.segment},{g.name})"
                elif size == 4:
                    v = f"far_offset({g.segment},{g.name})"
                else:
                    logging.error(f'Some unknown data size {size} for {g.name}')
        elif isinstance(g, (op.label, Proc)):
            v = f"m2c::k{g.name.lower()}"
        elif isinstance(g, op.Struct):
            pass
        else:
            v = g.offset
        logging.debug(v)
        return v

    def identify_data_internal_type(self, data, elements, is_string) -> op.DataType:
        args = data.children
        if is_string:

            if elements >= 2 and isinstance(args[-1].children[-1], lark.Token) \
                    and args[-1].children[-1].type == 'INTEGER' and args[-1].children[-1].value == '0':
                cur_data_type = op.DataType.ZERO_STRING  # 0 terminated string
            else:
                cur_data_type = op.DataType.ARRAY_STRING  # array string
        else:
            cur_data_type = op.DataType.NUMBER  # number
            if elements > 1:
                cur_data_type = op.DataType.ARRAY  # array
        return cur_data_type

    def process_data_tokens(self, value, width):
        elements = 0
        reslist = []
        is_string = False
        base = 1 << (8 * width)

        if isinstance(value, list):
            for subvalue in value:
                ele, is_string2, rr2 = self.process_data_tokens(subvalue, width)
                elements += ele
                is_string |= is_string2
                reslist += rr2
        elif isinstance(value, Token):
            if value.data in ['offsetdir', 'segmdir']:
                if isinstance(value.children, list):  # hack when '+' is glued to integer
                    value.children = Token.remove_tokens(value.children, ['expr'])
                    lst = [value.children[0]]
                    for val in value.children[1:]:
                        if isinstance(val, Token) and val.data == 'INTEGER':
                            lst += ['+']
                        lst += [val]
                    value.children = lst
                elements, is_string, reslist = self.process_data_tokens(value.children, width)
            elif value.data == 'expr':
                el, is_string, res = self.process_data_tokens(value.children, width)
                if not is_string and len(res) != 1:
                    reslist = ["".join(str(x) for x in res)]
                    elements = 1
                else:
                    reslist = res
                    elements = el
            elif value.data == 'STRING':
                value = value.children
                assert isinstance(value, str)
                if not self.itislst:  # not for IDA .lst
                    value = value.replace("\'\'", "'").replace('\"\"', '"')  # masm behaviour
                reslist = list(value[1:-1])
                elements = len(reslist)
                is_string = True

            # check if dup
            elif value.data == 'dupdir':
                # we should parse that
                repeat = Parser.parse_int(self.escape(value.children[0]))
                values = self.process_data_tokens(value.children[1], width)[2]
                elements, reslist = self.action_dup(repeat, values)

            elif value.data == 'INTEGER':
                elements += 1
                try:  # just number or many
                    value = value.children
                    # if v == '?':
                    #    v = '0'
                    value = Parser.parse_int(value)

                    if value < 0:  # negative values
                        value += base

                except Exception:
                    # global name
                    # traceback.print_stack(file=sys.stdout)
                    # logging.debug "global/expr: ~%s~" %v
                    try:
                        value = self.get_global_value(value, width)
                    except KeyError:
                        value = 0
                reslist = [value]

            # logging.debug("global/expr: ~%s~" % v)
            elif value.data == 'LABEL':
                elements = 1
                try:
                    value = value.children
                    # width = 2  # TODO for 16 bit only
                    value = self.mangle_label(value)
                    value = self.get_global_value(value, width)
                except KeyError:
                    if self.pass_number != 1:
                        logging.error("unknown address %s", value)
                    # logging.warning(self.c_data)
                    # logging.warning(r)
                    # logging.warning(len(self.c_data) + len(r))
                    # self.__link_later.append((len(self.c_data) + len(r), v))
                    # v = 0
                reslist = [value]
        elif value == '?':
            elements = 1
            reslist = [0]
        else:
            elements = 1
            reslist = [value]
        return elements, is_string, reslist

    def action_dup(self, n, values):
        res = []
        for i in range(0, n):
            for value in values:
                if value == '?':
                    value = 0
                else:
                    if isinstance(value, list):
                        val = ""
                        for v in value:
                            try:
                                v = Parser.parse_int(v)
                            except ValueError:
                                pass
                            val += str(v)
                        value = val
                # logging.debug "n = %d value = %d" %(n, value)

                res.append(value)
        return n * len(values), res

    def action_label(self, name, far=False, isproc=False, raw='', globl=True, line_number=0):
        logging.debug("label name: %s", name)
        if name == 'arbarb': # @@
            name = self.get_dummy_jumplabel()
        name = self.mangle_label(name)  # for tests only

        # logging.debug("offset %s -> %s" % (name, "&m." + name.lower() + " - &m." + self.__segment_name))

        self.need_label = False
        self.make_sure_proc_exists(line_number, raw)

        # if self.proc:
        l = op.label(name, proc=self.proc.name, isproc=isproc, line_number=self.__offset_id, far=far, globl=globl)
        _, l.real_offset, l.real_seg = self.get_lst_offsets(raw)

        if l.real_seg:
            self.procs_start.discard(l.real_seg * 0x10 + l.real_offset)
        self.proc.add_label(name, l)
        # self.set_offset(name,
        #                ("&m." + name.lower() + " - &m." + self.__segment_name, self.proc, self.__offset_id))
        self.set_global(name, l)
        self.__offset_id += 1
        # else:
        #    logging.error("!!! Label %s is outside the procedure" % name)

    def make_sure_proc_exists(self, line_number, raw):
        if not self.proc:
            _, real_offset, real_seg = self.get_lst_offsets(raw)
            if real_seg:
                offset = real_offset
            else:
                offset = self.__cur_seg_offset
            pname = f'{self.__segment.name}_{offset:x}_proc'  # automatically generated proc name
            # pname = f'{self.__segment.name}_proc'
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
                op.Data(label, 'db', op.DataType.ARRAY, [0], num, num, comment='for alignment', align=True,
                        offset=offset))

    def move_offset(self, pointer, raw):
        if pointer > self.__binary_data_size:
            self.data_merge_candidats = 0
            label = self.get_dummy_label()

            num = pointer - self.__binary_data_size
            offset = self.__binary_data_size
            self.__binary_data_size += num

            self.__segment.append(
                op.Data(label, 'db', op.DataType.ARRAY, [0], num, num, comment='move_offset', align=True,
                        offset=offset))
        elif pointer < self.__binary_data_size and not self.itislst:
            self.data_merge_candidats = 0
            logging.warning(f'Maybe wrong offset current:{self.__binary_data_size:x} should be:{pointer:x} ~{raw}~')

    def get_dummy_label(self):
        # Parser.c_dummy_label += 1
        label = "dummy" + self.__current_file_hash[0] + '_' + str(hex(self.__binary_data_size))[2:]
        return label

    def get_dummy_jumplabel(self):
        self.__c_dummy_jump_label += 1
        label = "dummylabel" + str(self.__c_dummy_jump_label)
        return label

    def get_extra_dummy_jumplabel(self):
        self.__c_extra_dummy_jump_label += 1
        label = "edummylabel" + str(self.__c_extra_dummy_jump_label)
        return label

    def parse_file(self, fname):
        logging.info(f' *** Parsing {fname} file')
        '''
        num = 0x1000
        if num:
            self.__binary_data_size += num

            self.__c_dummy_label += 1
            label = "dummy" + str(self.__c_dummy_label)

            self.c_data.append("{0}, // padding\n")
            self.h_data.append(" db " + label + "[" + str(num) + "]; // protective\n")
        '''

        self.parse_file_lines(fname)

        self.align()

        return self

    def parse_file_lines(self, file_name):
        self._current_file = file_name
        self.__current_file_hash = hashlib.blake2s(self._current_file.encode('utf8')).hexdigest()
        content = read_whole_file(file_name)
        if file_name.lower().endswith('.lst'):  # for .lst provided by IDA move address to comments after ;~
            # we want exact placement so program could work
            content = self.extract_addresses_from_lst(file_name, content)
        result = self.parse_text(content, file_name=file_name)
        result = self.process_ast(content, result)
        #result = "".join(IR2Cpp(self).visit(result))

    def extract_addresses_from_lst(self, file_name, content):
        self.itislst = True
        segmap = self.read_segments_map(file_name)
        content = re.sub(r'^(?P<segment>[_0-9A-Za-z]+):(?P<offset>[0-9A-Fa-f]{4,8})(?P<remain>.*)',
                         lambda m: f'{m.group("remain")} ;~ {segmap.get(m.group("segment"))}:{m.group("offset")}',
                         content, flags=re.MULTILINE)
        return content

    def read_segments_map(self, file_name):
        """
        It reads a .map file and returns a dictionary of segments

        :param file_name: The name of the .map file
        :return: A dictionary of segments and their values.
        """
        content = read_whole_file(re.sub(r'\.lst$', '.map', file_name, flags=re.I)).splitlines()
        DOSBOX_START_SEG = int(self.args.loadsegment, 0)
        strgenerator = (x for x in content)
        segs = OrderedDict()
        for line in strgenerator:
            if line.strip() == 'Start  Stop   Length Name               Class':  # IDA Pro .lst magic
                break
        # Reads text until the end of the block:
        for line in strgenerator:  # This keeps reading the file
            if line.strip() == 'Address         Publics by Value':
                break
            else:
                if line.strip():
                    # print(line)
                    m = re.match(
                        r'^\s+(?P<start>[0-9A-F]{5,10})H [0-9A-F]{5,10}H [0-9A-F]{5,10}H (?P<segment>[_0-9A-Za-z]+)\s+[A-Z]+',
                        line)
                    segs[m.group('segment')] = f"{(int(m.group('start'), 16) // 16 + DOSBOX_START_SEG):04X}"
                    # print(segs)
        logging.debug(f'Results of loading .map file: {segs}')
        return segs

    def parse_include_file_lines(self, file_name):
        self.__files.add(self._current_file)
        self._current_file = file_name
        content = read_whole_file(file_name)
        result = self.parse_file_inside(content, file_name=file_name)
        self._current_file = self.__files.pop()
        return result

    def action_assign(self, label, value, raw='', line_number=0):
        """
        This function is called when the parser encounters an assignment statement
        It creates an assignment operation, and then appends it to the list of statements

        :param label: the name of the variable
        :param value: The value to assign to the label
        :param raw: the raw line of code
        :param line_number: The line number of the assignment statement, defaults to 0 (optional)
        :return: The assignment operation.
        """
        label = self.mangle_label(label)

        # if self.has_global(label):
        #    label = self.get_global(label).original_name
        o = self.proc.create_assignment_op(label, value, line_number=line_number)
        o.filename = self._current_file
        o.raw_line = raw.rstrip()
        self.reset_global(label, o)
        self.proc.stmts.append(o)
        self.equs.add(label)
        return o

    def action_assign_test(self, label="", value="", line_number=0):
        raw = value
        #result = self.parse_text(value, start_rule='expr')
        #value = self.process_ast(value, result)
        result = self.parse_text(value, start_rule='expr')
        value = self.process_ast(value, result)
        o = self.action_assign(label, value, raw, line_number)
        o.implemented = True

    def action_equ_test(self, label="", value="", raw='', line_number=0):
        result = self.parse_text(value, start_rule='equtype')
        value = self.process_ast(value, result)

        o = self.action_equ(label, value, raw, line_number)
        o.implemented = True

    def return_empty(self, _):
        return []

    def action_equ(self, label="", value="", raw='', line_number=0):
        from .enum import IndirectionType
        label = self.mangle_label(label)
        #value = Token.remove_tokens(value, ['expr'])
        size = value.size() if isinstance(value, Expression) else 0
        #calc = ExprSizeCalculator(init=Vector(0, 0))
        #size = calc.visit(value)[0]

        #size = cpp_module.Cpp(self).calculate_size(value)
        #ptrdir = Token.find_tokens(value, 'ptrdir')
            #value = Token.find_and_replace_tokens(value, 'ptrdir', self.return_empty)
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

    def create_segment(self, name, options=None, segclass=None, raw=''):
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

            if real_seg:
                offset = real_seg * 0x10
            else:
                offset = self.__binary_data_size
            logging.debug("segment %s %x", name, offset)
            binary_width = 0

            self.__segment = op.Segment(name, offset, options=options, segclass=segclass)
            self.segments[name] = self.__segment
            # self.__segment.append(op.Data(name, 'db', DataType.ARRAY, [], 0, 0, comment='segment start zero label'))

            self.set_global(name, op.var(binary_width, offset, name, issegment=True))
        return self.__segment

    def action_proc(self, name, type, line_number=0, raw=''):
        logging.info("      Found proc %s", name)
        self.action_endp()
        name = self.mangle_label(name)
        far = False
        for i in type:
            if i and i.lower() == 'far':
                far = True

        self.proc = self.add_proc(name, raw, line_number, far)
        # else:
        #    self.action_label(name, far=far, isproc=True)

    def add_proc(self, name, raw, line_number, far):
        if self.args.mergeprocs == 'separate':
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
            type = type + "_"
        type = type[1:] + name
        self.create_segment(type)

    '''
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
    '''

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
        ''' Support code outside procs
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
    '''

    def action_code(self, line):
        #from .cpp import IR2Cpp
        self.test_mode = True
        self.need_label = False
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            result = self.parse_text(line + "\n", start_rule='instruction')
            #result = result.children[2].children[1].children[1]
            result = self.process_ast(line, result)
            #result = "".join(IR2Cpp(self).visit(result))
        except Exception as e:
            print(e)
            logging.error("Error1")
            result = [str(e)]
            raise
        #del self.__globals['default_seg']
        return result

    def test_size(self, line):
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            result = self.parse_text(line, start_rule='expr')
            #result = result.children[2].children[1].children[1]
            expr = self.process_ast(line, result)
            result = expr.size()
        except Exception as e:
            print(e)
            import traceback
            logging.error(traceback.format_exc())
            result = [str(e)]
            raise
        #del self.__globals['default_seg']
        return result

    def action_data(self, line):
        ''' For tests only '''
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            result = self.parse_text(line + "\n", start_rule='insegdirlist')
            result = self.process_ast(line, result)
            #result = tuple(self.cpp.visit(result))
        except Exception as e:
            print(e)
            logging.error("Error3")
            result = [str(e)]
            raise
        #del self.__globals['default_seg']
        return result

    def parse_arg(self, line, def_size=0, destination=False):
        from .cpp import Cpp
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            self.test_pre_parse()
            expr = self.parse_text(line, start_rule='expr')
            #expr = result.children[2].children[1].children[1]
            expr = self.process_ast(line, expr)
            #if destination:
            #    expr.mods.add("destination")
            #if def_size and expr.element_size == 0:
            #    expr.element_size = def_size
            #result = "".join(IR2Cpp(self).visit(expr))
            result = Cpp(self).render_instruction_argument(expr, def_size=def_size, destination=destination)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            import traceback, logging

            logging.error(traceback.format_exc())
            # result = [f'{e} {exc_type} {fname} {exc_tb.tb_lineno}']
            raise
        ### del self.__globals['default_seg']
        return result

    def parse_include(self, line, file_name=None):
        result = self.parse_text(line, file_name=file_name, start_rule='insegdirlist')
        return result

    def escape(self, s):
        if isinstance(s, list):
            return [self.escape(i) for i in s]
        elif isinstance(s, Token):
            return self.escape(s.children)
        else:
            s = s.translate(s.maketrans({"\\": r"\\"}))
            # if not self.itislst:
            s = s.replace("''", "'").replace('""', '"')
            return s

    def calculate_data_size_new(self, size, values):
        if isinstance(values, list):
            return sum(self.calculate_data_size_new(size, x) for x in values)
        elif isinstance(values, Token):
            if values.data == 'expr':
                if isinstance(values.children, Token) and values.children.data == STRINGCNST:
                    return self.calculate_data_size_new(size, values.children)
                else:
                    return size
            elif values.data == STRINGCNST:
                return self.calculate_STRING_size(values.children)
            elif values.data == 'dupdir':
                return Parser.parse_int(self.escape(values.children[0])) * self.calculate_data_size_new(size,
                                                                                                        values.children[
                                                                                                            1])
            else:
                return size
        elif isinstance(values, str):
            if values == '?':
                return size
            return len(values)
        else:
            raise NotImplementedError('Unknown Token: ' + str(values))

    def datadir_action(self, label, type, args, is_string=False, raw='', line_number=0):
        if self.__cur_seg_offset > 0xffff:
            return []
        if self.__cur_seg_offset & 0xff == 0:
            logging.info(f"      Current offset {self.__cur_seg_offset:x} line={line_number}")
        isstruct = len(self.struct_names_stack) != 0

        #label = self.mangle_label(label)
        binary_width = self.typetosize(type)
        #for ex in args:
        #    ex.element_size = binary_width

        calc = ExprSizeCalculator(element_size=binary_width, init=Vector(0, 0), context=self)
        size, elements = calc.visit(args) #, result=0)
        if size == 0:
            size = binary_width * elements
        #size = calc.size
        ##size = sum(map(Expression.size, args))  #self.calculate_data_size_new(binary_width, args)
        ##elements = sum(arg.element_number for arg in args)
        #elements = calc.element_number

        offset = self.__cur_seg_offset
        if not isstruct:

            self.adjust_offset_to_real(raw, label)

            offset = self.__cur_seg_offset
            if not self.flow_terminated:
                logging.error(f"Flow wasn't terminated! line={line_number} offset={self.__cur_seg_offset}")

            logging.debug("args %s offset %d", args, offset)

        logging.debug("convert_data %s %d %s", label, binary_width, args)
        # original_label = label

        data_internal_type = self.identify_data_internal_type(args, elements, is_string)
        #elements, is_string, array = self.process_data_tokens(args, binary_width)
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
            data_type = 'struct data'
        else:
            self.__binary_data_size += size
            self.__cur_seg_offset += size
            data_type = 'usual data'
        data = op.Data(label, type, data_internal_type, array, elements, size, filename=self._current_file,
                       raw_line=raw,
                       line_number=line_number, comment=data_type, offset=offset)
        if isstruct:
            self.current_struct.append(data)
        else:
            _, data.real_offset, data.real_seg = self.get_lst_offsets(raw)
            self.__segment.append(data)
            if dummy_label and data_internal_type == op.DataType.NUMBER and binary_width == 1:
                self.merge_data_bytes()
            else:
                self.data_merge_candidats = 0

        # c, h, size = cpp.Cpp.produce_c_data(data) # TO REMOVE
        # self.c_data += c
        # self.h_data += h

        # logging.debug("~~        self.assertEqual(parser_instance.parse_data_line_whole(line='"+str(line)+"'),"+str(("".join(c), "".join(h), offset2 - offset))+")")
        self.flow_terminated = True
        return data  # c, h, size

    def merge_data_bytes(self):
        self.data_merge_candidats += 1
        size = 32
        if self.data_merge_candidats == size:
            if self.__segment.getdata()[-size].offset + size - 1 != self.__segment.getdata()[-1].offset:
                logging.debug(
                    f'Cannot merge {self.__segment.getdata()[-size].__label} - {self.__segment.getdata()[-1].__label}')
                self.data_merge_candidats = 0
            else:
                logging.debug(
                    f'Merging data at {self.__segment.getdata()[-size].__label} - {self.__segment.getdata()[-1].__label}')
                array = [x.children[0] for x in self.__segment.getdata()[-size:]]
                if not any(array):  # all zeros
                    array = [0]

                self.__segment.getdata()[-size].children = array
                self.__segment.getdata()[-size].elements = size
                self.__segment.getdata()[-size].data_internal_type = op.DataType.ARRAY
                self.__segment.getdata()[-size]._size = size
                self.__segment.setdata(self.__segment.getdata()[:-(size - 1)])
                self.data_merge_candidats = 0

    def adjust_offset_to_real(self, raw, label):
        absolute_offset, real_offset, _ = self.get_lst_offsets(raw)
        if self.itislst and real_offset and real_offset > 0xffff:  # IDA issue
            return
        if absolute_offset:
            self.move_offset(absolute_offset, raw)
            if self.__cur_seg_offset > real_offset:
                if not self.itislst:
                    logging.warning(f'Current offset does not equal to required for {label}')
            if self.__cur_seg_offset != real_offset:
                self.data_merge_candidats = 0
            self.__cur_seg_offset = real_offset

    def get_lst_offsets(self, raw):
        '''
        Get required offsets from .LST file
        :param raw: raw string
        :return: offset from memory begging, offset starting from segment, segment in para
        '''
        real_offset = None
        absolute_offset = None
        real_seg = None
        if self.itislst:
            m = re.match(r'.* ;~ (?P<segment>[0-9A-Fa-f]{4}):(?P<offset>[0-9A-Fa-f]{4})', raw)
            if m:
                real_offset = int(m.group('offset'), 16)
                real_seg = int(m.group('segment'), 16)
                absolute_offset = real_seg * 0x10 + real_offset
        return absolute_offset, real_offset, real_seg

    '''
    def link(self):
        logging.debug("link()")
        # logging.debug self.c_data
        for addr, expr in self.__link_later:
            logging.debug("addr %s expr %s" % (addr, expr))
            try:
                # v = self.eval_expr(expr)
                v = expr
                # if self.has_global('k' + v):
                #               v = 'k' + v
                v = self.get_global_value(v, 0x10000)

                logging.debug("link: patching %04x -> %s" % (addr, v))
            except:
                logging.warning("link: Exception %s" % expr)
                continue
            logging.debug("link: addr %s v %s" % (addr, v))
            self.c_data[addr] = str(v)
    '''

    def test_pre_parse(self):
        self.__binary_data_size = 0
        self.__c_dummy_jump_label = 0
        self.__c_extra_dummy_jump_label = 0

    def parse_file_inside(self, text, file_name=None):
        return self.parse_include(text, file_name)

    def parse_text(self, text, file_name=None, start_rule='start'):
        logging.debug("parsing: [%s]", text)

        result = self.__lex.parser.parse(text, start=start_rule)  # , file_name=file_name, extra=self)
        return result

    def process_ast(self, text, result):
        result = IncludeLoader(self).transform(result)
        result = ExprRemover().transform(result)
        #result = EquCollector(self).transform(result)
        asm2ir = Asm2IR(self, text)
        '''
        for e in self.equs:
            g = self.get_global(e)
            if not isinstance(g.value, Expression):
                g.value = asm2ir.transform(g.value)
        '''
        result = asm2ir.transform(result)
        return result

    @staticmethod
    def mangle_label(name):
        name = name.lower()  # ([A-Za-z@_\$\?][A-Za-z0-9@_\$\?]*)
        return name.replace('@', "arb").replace('?', "que").replace('$', "dol")

    @staticmethod
    def is_register(expr):
        expr = expr.lower()
        size = 0
        if expr in {'al', 'bl', 'cl', 'dl', 'ah', 'bh', 'ch', 'dh'}:
            logging.debug('is reg res 1')
            size = 1
        elif expr in {'ax', 'bx', 'cx', 'dx', 'si', 'di', 'sp', 'bp', 'ds', 'cs', 'es', 'fs', 'gs', 'ss'}:
            logging.debug('is reg res 2')
            size = 2
        elif expr in {'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp'}:
            logging.debug('is reg res 4')
            size = 4
        return size

    def typetosize(self, value):
        if isinstance(value, Token):
            value = value.children
        if not isinstance(value, str):
            logging.error("Type is not a string TODO " + str(value))
            return 0
        value = value.lower()
        if value in self.structures.keys() and self.structures[value] != True:
            return self.structures[value].getsize()
        try:
            size = {'db': 1, 'byte': 1, 'sbyte': 1,
                    'dw': 2, 'word': 2, 'sword': 2, 'small': 2, 'near': 2,
                    'dd': 4, 'dword': 4, 'sdword': 4, 'large': 4, 'far': 4, 'real4': 4,
                    'df': 6, 'fword': 6,
                    'dq': 8, 'qword': 8, 'real8': 8,
                    'dt': 10, 'tbyte': 10, 'real10': 10}[value]
        except KeyError:
            logging.error("Cannot find size for %s", value)
            size = 0
        return size

    def convert_members(self, data, values):
        if data.isobject():
            if isinstance(values, lark.Tree):
                values = values.children
            return [self.convert_members(m, v) for m, v in zip(data.getmembers(), values)]
        else:
            '''
            type = data.gettype()
            binary_width = self.typetosize(type)
            _, _, array = self.process_data_tokens(values, binary_width)
            '''
            array = AsmData2IR().visit(values)
            return array

    def add_structinstance(self, label, type, args, raw=''):

        if not label:
            label = self.get_dummy_label()

        self.data_merge_candidats = 0
        self.adjust_offset_to_real(raw, label)
        offset = self.__cur_seg_offset

        s = self.structures[type]
        number = 1
        if isinstance(args, list) and len(args) > 2 and isinstance(args[1], str) and args[1] == 'dup':
            cpp = cpp_module.Cpp(self)
            number = literal_eval(cpp.render_instruction_argument(Token.find_tokens(args[0],'expr')))
            args = args[3]
        args = Token.remove_tokens(args, ['structinstance'])

        d = op.Data(label, type, op.DataType.OBJECT, args, 1, s.getsize(), comment='struct instance', offset=offset)
        members = [deepcopy(i) for i in s.getdata().values()]
        d.setmembers(members)
        args = self.convert_members(d, args)
        d.setvalue(args)

        if number > 1:
            d = op.Data(label, type, op.DataType.ARRAY, number * [d], number, number * s.getsize(),
                        comment='object array',
                        offset=offset)

        isstruct = len(self.struct_names_stack) != 0
        if isstruct:
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

    def add_extern(self, label, type):
        strtype = self.mangle_label(type)
        if isinstance(type, Token):
            strtype = type.children
        label = self.mangle_label(label)
        if strtype not in ['proc']:
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
            # else:
            #    self.reset_global(label, op.label(label, proc=self.proc.name, isproc=True))

    def add_call_to_entrypoint(self):
        """
        It adds a call to the entry point of the program to the service mainproc
        """
        # if self.__separate_proc:
        proc = self.get_global('mainproc')
        result = self.parse_text(self.entry_point, start_rule='expr')
        expr = self.process_ast('', result)

        o = proc.create_instruction_object('call', [expr])
        o.filename = self._current_file
        o.raw_line = ''
        o.line_number = 0
        proc.stmts.append(o)
        o = proc.create_instruction_object('ret')
        o.filename = self._current_file
        o.raw_line = ''
        o.line_number = 0
        proc.stmts.append(o)

    def action_instruction(self, instruction, args, raw='', line_number=0):
        self.handle_local_asm_jumps(instruction, args)

        self.make_sure_proc_exists(line_number, raw)

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
                if o.real_seg:
                    label_name = f'ret_{o.real_seg:x}_{o.real_offset:x}'
                else:
                    label_name = self.get_extra_dummy_jumplabel()
                logging.warning(f"Adding helping label {label_name}")
                self.action_label(label_name, raw=raw)
            self.proc.stmts.append(o)
            if self.args.mergeprocs == 'single':
                self.need_label |= self.proc.is_return_point(o)
            self.flow_terminated = self.proc.is_flow_terminating_stmt(o)
            self.need_label |= self.flow_terminated

            self.collect_labels(self.proc.used_labels, o)
            return o
        else:
            self.current_macro.instructions.append(o)
            return None

    def handle_local_asm_jumps(self, instruction, args):
        if (instruction[0].lower() == 'j' or instruction[0].lower() == 'loop') and \
                len(args) == 1 and isinstance(args[0], lark.Tree) and \
                isinstance(args[0].children, list) and isinstance(args[0].children[0], lark.Token) and \
                args[0].children[0].type == 'LABEL':
            if args[0].children[0].lower() == 'arbf':  # @f
                args[0].children[0] = "dummylabel" + str(self.__c_dummy_jump_label + 1)
            elif args[0].children[0].lower() == 'arbb':  # @b
                args[0].children[0] = "dummylabel" + str(self.__c_dummy_jump_label)

    def collect_labels(self, target, operation):
        for arg in operation.children:
            labels = Token.find_tokens(arg, 'LABEL')  # TODO replace with AST traversing
            #  If it is call to a proc then does not take it into account
            #  TODO: check for calls into middle of proc
            if labels and not operation.cmd.startswith('call') and not (
                    self.args.mergeprocs == 'separate' and operation.cmd == 'jmp'):
                label = labels[0]
                target.add(self.mangle_label(label))

    def action_ends(self):
        if len(self.struct_names_stack):  # if it is not a structure then it is end of segment
            name = self.struct_names_stack.pop()
            logging.debug("endstruct " + name)
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
        # dbx_img_offset = int(self.args.loadsegment, 0)  # para
        # ida_load = 0x1000

        try:
            with open(name + ".json") as infile:
                logging.info(f' *** Loading {name}.json')
                j = jsonpickle.decode(infile.read())
                self.initial_procs_start = self.procs_start = set(j['Jumps'])
        except FileNotFoundError:
            pass


def parse_asm_number(expr, radix):
    if expr == '?':
        radix, sign, value = 10, '', '0'
    else:
        if m := re.match(r'^(?P<sign>[+-]?)(?P<value>[0-8]+)[OoQq]$', expr):
            radix = 8
        elif m := re.match(r'^(?P<sign>[+-]?)(?P<value>[0-9][0-9A-Fa-f]*)[Hh]$', expr):
            radix = 16
        elif m := re.match(r'^(?P<sign>[+-]?)(?P<value>[0-9]+)[Dd]$', expr):
            radix = 10
        elif m := re.match(r'^(?P<sign>[+-]?)(?P<value>[0-1]+)[Bb]$', expr):
            radix = 2
        elif m := re.match(r'^(?P<sign>[+-]?)(?P<value>[0-9]+)$', expr):
            pass
        elif m := re.match(r'^(?P<sign>[+-]?)(?P<value>[0-9][0-9A-Fa-f]*)$', expr):
            radix = 16
        else:
            raise ValueError(expr)
        sign = m['sign'] if m['sign'] else ''
        value = m['value']
        #value = int(value, radix)
        #if sign == '-':
        #    value *= -1
    return radix, sign, value
