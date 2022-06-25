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
from __future__ import print_function

import hashlib
import logging
import os
import re
import sys
from builtins import range, str
from collections import OrderedDict
from copy import copy, deepcopy

import jsonpickle
import parglare
from parglare import Grammar
from parglare import Parser as PGParser

from masm2c import cpp, op, proc
from masm2c.cpp import Cpp
from masm2c.Macro import Macro
from masm2c.op import DataType, Segment, Struct
from masm2c.proc import Proc
from masm2c.Token import Token

INTEGERCNST = 'INTEGER'
STRINGCNST = 'STRING'


class MyDummyObj: pass


def read_whole_file(file_name):
    logging.info("     Reading file %s...", file_name)
    if sys.version_info >= (3, 0):
        fd = open(file_name, 'rt', encoding="cp437")
    else:
        fd = open(file_name, 'rt')
    content = fd.read()
    fd.close()
    return content


macroses = OrderedDict()
macronamere = re.compile(r'([A-Za-z@_\$\?][A-Za-z0-9@_\$\?]*)')
commentid = re.compile(r'COMMENT\s+([^ ]).*?\1[^\r\n]*', flags=re.DOTALL)


def get_line_number(context):
    # old_line, old_col = parglare.pos_to_line_col(context.input_str, context.start_position)
    new_line = context.input_str[: context.start_position].count('\n') + 1
    # line_start_pos = context.input_str.rfind('\n', 0, context.start_position)
    # if line_start_pos == -1:
    #    line_start_pos = 0
    # new_col = context.start_position - line_start_pos - 1
    # assert(old_line == new_line and old_col == new_col)
    return new_line


def get_raw(context):
    return context.input_str[context.start_position: context.end_position].strip()


def get_raw_line(context):
    line_eol_pos = context.input_str.find('\n', context.end_position)
    if line_eol_pos == -1:
        line_eol_pos = context.end_position
    return context.input_str[context.start_position: line_eol_pos]


'''
def build_ast(nodes, type=''):
    if isinstance(nodes, parglare.parser.NodeNonTerm) and nodes.children:
        if len(nodes.children) == 1:
            return build_ast(nodes.children[0], nodes.symbol.name)
        else:
            l = []
            for n in nodes.children:
                if not n.symbol.name in ['COMMA']:
                    l.append(build_ast(n, nodes.symbol.name))
            return l
    else:
        return Node(name=nodes.symbol.name, type=type, keyword=nodes.symbol.keyword, value=nodes.value)
'''


def make_token(context, nodes):
    if len(nodes) == 1 and context.production.rhs[0].name not in (
            'type', 'e01', 'e02', 'e03', 'e04', 'e05', 'e06', 'e07', 'e08', 'e09', 'e10', 'e11'):
        nodes = Token(context.production.rhs[0].name, nodes[0])
    if context.production.rhs[0].name in (
            'type', 'e01', 'e02', 'e03', 'e04', 'e05', 'e06', 'e07', 'e08', 'e09', 'e10', 'e11'):
        nodes = nodes[0]
    return nodes


def expr(context, nodes):
    return Token('expr', make_token(context, nodes))


def dupdir(context, nodes, times, values):
    return Token('dupdir', [times, values])


def segoverride(context, nodes):
    # global cur_segment
    if isinstance(nodes[0], list):
        # cur_segment = nodes[0][-1]
        return nodes[0][:-1] + [Token('segoverride', nodes[0][-1]), nodes[2]]
    # cur_segment = nodes[0] #!
    return [Token('segoverride', nodes[0]), nodes[2]]


def ptrdir(context, nodes):
    if len(nodes) == 3:
        return [Token('ptrdir', nodes[0]), nodes[2]]
    else:
        return [Token('ptrdir', nodes[0]), nodes[1]]


def integertok(context, nodes):
    return Token('INTEGER', cpp.convert_number_to_c(nodes, context.extra.radix))


def commentkw(head, s, pos):
    # multiline comment
    if s[pos:pos + 7] == 'COMMENT':
        mtch = commentid.match(s[pos:])
        if mtch:
            return mtch.group(0)
    return None


def macroname(context, s, pos):
    if macroses:
        # macro usage identifier
        mtch = macronamere.match(s[pos:])
        if mtch:
            result = mtch.group().lower()
            # logging.debug ("matched ~^~" + result+"~^~")
            if result in macroses.keys():
                logging.debug(" ~^~" + result + "~^~ in macronames")
                return result
    return None


def macrodirhead(context, nodes, name, parms):
    # macro definition header
    param_names = []
    if parms:
        param_names = [i.lower() for i in Token.find_tokens(parms, 'LABEL')]
    context.extra.current_macro = Macro(name.value.lower(), param_names)
    context.extra.macro_names_stack.add(name.value.lower())
    logging.debug("macroname added ~~%s~~", name.value)
    return nodes


def repeatbegin(context, nodes, value):
    # start of repeat macro
    context.extra.current_macro = Macro("", [], value)
    context.extra.macro_names_stack.add('')  # TODO
    logging.debug("repeatbegin")
    return nodes


def endm(context, nodes):
    # macro definition end
    name = context.extra.macro_names_stack.pop()
    logging.debug("endm %s", name)
    macroses[name] = context.extra.current_macro
    context.extra.current_macro = None
    return nodes


class Getmacroargval:

    def __init__(self, params, args):
        self.argvaluedict = OrderedDict(zip(params, args))

    def __call__(self, token):
        return self.argvaluedict[token.value]


def macrocall(context, nodes, name, args):
    # macro usage
    logging.debug("macrocall " + name + "~~")
    macros = macroses[name]
    instructions = deepcopy(macros.instructions)
    param_assigner = Getmacroargval(macros.getparameters(), args)
    for instruction in instructions:
        instruction.args = Token.find_and_replace_tokens(instruction.args, 'LABEL', param_assigner)
    context.extra.proc.stmts += instructions
    return nodes


def structname(context, s, pos):
    if context.extra.structures:
        mtch = macronamere.match(s[pos:])
        if mtch:
            result = mtch.group().lower()
            # logging.debug ("matched ~^~" + result+"~^~")
            if result in context.extra.structures.keys():
                logging.debug(" ~^~" + result + "~^~ in structures")
                return result
    return None


def structdirhdr(context, nodes, name, type):
    # structure definition header
    context.extra.current_struct = Struct(name.value.lower(), type)
    context.extra.struct_names_stack.add(name.value.lower())
    logging.debug("structname added ~~" + name.value + "~~")
    return nodes


def structinstdir(context, nodes, label, type, values):
    logging.debug(f"structinstdir {label} {type} {values}")
    # args = remove_str(Token.remove_tokens(remove_str(values), 'expr'))
    args = values[0].value
    # args = Token.remove_tokens(remove_str(values), 'expr')
    if args is None:
        args = []
    # args = Token.remove(args, 'INTEGER')
    if label:
        name = label.value.lower()
    else:
        name = ''
    context.extra.add_structinstance(name, type.lower(), args, raw=get_raw(context))
    return nodes


def datadir(context, nodes, label, type, values):
    logging.debug("datadir " + str(nodes) + " ~~")

    if label:
        label = label.value
    else:
        label = ""

    return context.extra.datadir_action(label, type.lower(), values, raw=get_raw(context),
                                        line_number=get_line_number(context))


def includedir(context, nodes, name):
    # context.parser.input_str = context.input_str[:context.end_position] + '\n' + read_asm_file(name) \
    # + '\n' + context.input_str[context.end_position:]
    result = context.extra.parse_include_file_lines(name)
    return result


def segdir(context, nodes, type):
    logging.debug("segdir " + str(nodes) + " ~~")
    context.extra.action_simplesegment(type, '')  # TODO
    return nodes


def segmentdir(context, nodes, name, options):
    logging.debug("segmentdir " + str(nodes) + " ~~")

    opts = set()
    segclass = None
    if options:
        for o in options:
            if isinstance(o, str):
                opts.add(o.lower())
            elif isinstance(o, Token) and o.type == 'STRING':
                segclass = o.value.lower()
                if segclass[0] in ['"', "'"] and segclass[0] == segclass[-1]:
                    segclass = segclass[1:-1]
            else:
                logging.warning('Unknown segment option')

    context.extra.create_segment(name.value, options=opts, segclass=segclass, raw=get_raw(context))
    return nodes


def modeldir(context, nodes, model):
    logging.debug("modeldir " + str(nodes) + " ~~")
    return nodes


def endsdir(context, nodes, name):
    logging.debug("ends " + str(nodes) + " ~~")
    context.extra.action_ends()
    return nodes


def procdir(context, nodes, name, type):
    logging.debug("procdir " + str(nodes) + " ~~")
    context.extra.action_proc(name, type, line_number=get_line_number(context), raw=get_raw_line(context))
    return nodes


def endpdir(context, nodes, name):
    logging.debug("endp " + str(name) + " ~~")
    context.extra.action_endp()
    return nodes


def equdir(context, nodes, name, value):
    logging.debug("equdir " + str(nodes) + " ~~")
    return context.extra.action_equ(name.value, value, raw=get_raw(context), line_number=get_line_number(context))


def assdir(context, nodes, name, value):
    logging.debug("assdir " + str(nodes) + " ~~")
    return context.extra.action_assign(name.value, value, raw=get_raw(context), line_number=get_line_number(context))


def labeldef(context, nodes, name, colon):
    logging.debug("labeldef " + str(nodes) + " ~~")
    return context.extra.action_label(name.value, isproc=False, raw=get_raw_line(context),
                                      line_number=get_line_number(context),
                                      globl=(colon == '::'))


def instrprefix(context, nodes):
    logging.debug("instrprefix " + str(nodes) + " ~~")
    instruction = nodes[0]
    context.extra.action_instruction(instruction, [], raw=get_raw_line(context), line_number=get_line_number(context))
    return []


def asminstruction(context, nodes, instruction, args):
    logging.debug("asminstruction " + str(nodes) + " ~~")
    # args = build_ast(args)
    if not instruction:
        return nodes
    if args is None:
        args = []
    return context.extra.action_instruction(instruction, args, raw=get_raw_line(context),
                                            line_number=get_line_number(context))


def enddir(context, nodes, label):
    logging.debug("end " + str(nodes) + " ~~")
    context.extra.action_end(label)
    return nodes


def notdir(context, nodes):
    nodes[0] = '~'  # should be in Cpp module
    return nodes


def ordir(context, nodes):
    nodes[1] = '|'
    return nodes


def xordir(context, nodes):
    nodes[1] = '^'
    return nodes


def anddir(context, nodes):
    nodes[1] = ' & '
    return nodes


def register(context, nodes):
    return Token('register', nodes[0].lower())


def segmentregister(context, nodes):
    return Token('segmentregister', nodes[0].lower())


def sqexpr(context, nodes):
    logging.debug("/~" + str(nodes) + "~\\")
    res = nodes[1]
    return Token('sqexpr', res)


def offsetdir(context, nodes):
    logging.debug("offset /~" + str(nodes) + "~\\")
    return Token('offsetdir', nodes[1])


def segmdir(context, nodes):
    logging.debug("segmdir /~" + str(nodes) + "~\\")
    # global indirection
    # indirection = -1
    return Token('segmdir', nodes[1])


def labeltok(context, nodes):
    return Token('LABEL', nodes)


def STRING(context, nodes):
    return Token('STRING', nodes)


def structinstance(context, nodes, values):
    return Token('structinstance', values)


def memberdir(context, nodes, variable, field):
    result = Token('memberdir', [variable, field])
    logging.debug(result)
    return result


def radixdir(context, nodes, value):
    context.extra.radix = int(value.value.value)
    return nodes


def externdef(context, nodes, extrnname, type):
    logging.debug('externdef %s' % str(nodes))
    context.extra.add_extern(extrnname.value, type)
    return nodes


def maked(context, nodes):
    # return Token(nodes[0].upper(), nodes[1].value)
    # TODO dirty workaround for now
    if nodes[0].lower() == 'size':
        return [f'sizeof({nodes[1].value.lower()})']
    else:
        return nodes


def offsetdirtype(context, nodes, directive, value):
    logging.debug(f'offsetdirtype {directive} {str(value)}')
    directive = directive.lower()
    value = value.value.value if value else 2
    if directive == 'align':
        context.extra.align(Parser.parse_int(value))
    elif directive == 'even':
        context.extra.align(2)
    elif directive == 'org':
        context.extra.org(Parser.parse_int(value))
    return nodes


actions = {
    "offsetdirtype": offsetdirtype,
    "modeldir": modeldir,
    "dir3": maked,
    "externdef": externdef,
    "macrocall": macrocall,
    "repeatbegin": repeatbegin,
    "ENDM": endm,
    "radixdir": radixdir,
    "field": make_token,
    "memberdir": memberdir,
    "structinstdir": structinstdir,
    "dupdir": dupdir,
    "structinstance": structinstance,
    "structdirhdr": structdirhdr,
    "includedir": includedir,
    "instrprefix": instrprefix,
    "INTEGER": integertok,
    "LABEL": labeltok,
    "STRING": STRING,
    "anddir": anddir,
    "asminstruction": asminstruction,
    "assdir": assdir,
    "datadir": datadir,
    "enddir": enddir,
    "endpdir": endpdir,
    "endsdir": endsdir,
    "equdir": equdir,
    "labeldef": labeldef,
    "macrodirhead": macrodirhead,
    "notdir": notdir,
    "offsetdir": offsetdir,
    "ordir": ordir,
    "procdir": procdir,
    "ptrdir": ptrdir,
    "register": register,
    "segdir": segdir,
    "segmdir": segmdir,
    "segmentdir": segmentdir,
    "segmentregister": segmentregister,
    "segoverride": segoverride,
    "sqexpr": sqexpr,
    "xordir": xordir,
    "expr": expr,
    "aexpr": make_token,
    "cexpr": make_token,
    "cxzexpr": make_token,
    "flagname": make_token,
    "primary": make_token,
    "recordconst": make_token,
    "simpleexpr": make_token,
    "sizearg": make_token,
    "term": make_token
}

recognizers = {
    'macroname': macroname,
    "structname": structname,
    "COMMENTKW": commentkw
}


class ParglareParser:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ParglareParser, cls).__new__(cls)
            logging.debug("Allocated ParglareParser instance")

            file_name = os.path.dirname(os.path.realpath(__file__)) + "/_masm61.pg"
            cls._inst.or_grammar = Grammar.from_file(file_name, ignore_case=True, recognizers=recognizers)
            ## cls._inst.parser = PGParser(grammar, debug=True, debug_trace=True, actions=action.all)
            debug = False
            cls._inst.or_parser = PGParser(cls._inst.or_grammar, debug=debug, actions=actions)
            # , build_tree = True, call_actions_during_tree_build = True)

            cls._inst.grammar = cls._inst.or_grammar
            cls._inst.parser = copy(cls._inst.or_parser)
            cls._inst.parser.grammar = cls._inst.grammar

        return cls._inst


def dump_object(value):
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

    def __init__(self, args=None, skip_binary_data:list=None):
        '''
        Assembler parser
        '''
        self.test_mode = False
        self.__globals = OrderedDict()
        # self.__offsets = OrderedDict()
        self.pass_number = 0
        self.__lex = ParglareParser()
        #self.segments = OrderedDict()
        self.externals_vars = set()
        self.externals_procs = set()
        self.__files = set()
        self.itislst = False
        self.initial_procs_start = set()
        self.procs_start = set()

        if not args:
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
        self.__segment = Segment(self.__segment_name, 0, comment="Artificial initial segment")
        self.segments[self.__segment_name] = self.__segment

        self.proc = self.add_proc("mainproc", '', 0, False)

        self.used = False

        self.radix = 10

        self.current_macro = None
        self.current_struct = None

        self.struct_names_stack = set()

        self.__current_file = ''
        self.__current_file_hash = '0'

        self.data_merge_candidats = 0

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

        logging.debug("set_global(name='%s',value=%s)" % (name, dump_object(value)))
        if name in self.__globals and self.pass_number == 1 and not self.test_mode:
            raise LookupError("global %s was already defined" % name)
        value.used = False
        self.__globals[name] = value

    def reset_global(self, name, value):
        if len(name) == 0:
            raise NameError("empty name is not allowed")
        value.original_name = name
        name = name.lower()
        logging.debug("reset global %s -> %s" % (name, value))
        self.__globals[name] = value

    def get_global(self, name):
        name = name.lower()
        logging.debug("get_global(%s)" % name)
        try:
            g = self.__globals[name]
            logging.debug(type(g))
        except KeyError:
            logging.debug("get_global KeyError %s" % name)
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
        logging.debug("$ = %d" % self.__cur_seg_offset)
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
        if re.match(r'^[+-]?[0-9][0-9A-Fa-f]*[Hh]$', v):
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

    def calculate_data_binary_size(self, width, data):
        logging.debug("calculate_data_binary_size %d %s" % (width, data))
        s = 0
        for v in data:
            # v = v.strip()
            if isinstance(v, str) and width == 1 and len(v) >= 2 and (v[0] in ["'", '"']) and v[-1] == v[0]:
                s += self.calculate_STRING_size(v)
                continue

            if isinstance(v, list) and len(v) == 5 and v[1].lower() == 'dup':
                # logging.error(v)
                # we should parse that
                n = Parser.parse_int(v[0])
                '''
                value = m.group(2)
                value = value.strip()
                if value == '?':
                    value = 0
                else:
                    value = Parser.parse_int(value)
                '''
                s += n * width
                continue
            s += width
        return s

    def calculate_STRING_size(self, v):
        if not self.itislst:
            v = v.replace("\'\'", "'").replace('\"\"', '"')
        return len(v) - 2

    def get_global_value(self, v, size=2):
        logging.debug("get_global_value(%s)" % v)
        v = self.mangle_label(v)
        g = self.get_global(v)
        logging.debug(g)
        if isinstance(g, (op._equ, op._assignment)):
            v = g.original_name
        elif isinstance(g, op.var):
            if g.issegment:
                v = "seg_offset(%s)" % g.name
            else:
                if size == 2:
                    v = "offset(%s,%s)" % (g.segment, g.name)
                elif size == 4:
                    v = "far_offset(%s,%s)" % (g.segment, g.name)
                else:
                    logging.error(f'Some unknown data size {size} for {g.name}')
        elif isinstance(g, (op.label, proc.Proc)):
            v = "m2c::k%s" % (g.name.lower())
        else:
            v = g.offset
        logging.debug(v)
        return v

    def identify_data_internal_type(self, r, elements, is_string) -> DataType:
        if is_string:
            if len(r) >= 2 and r[-1] == 0:
                cur_data_type = DataType.ZERO_STRING  # 0 terminated string
            else:
                cur_data_type = DataType.ARRAY_STRING  # array string
        else:
            cur_data_type = DataType.NUMBER  # number
            if elements > 1:
                cur_data_type = DataType.ARRAY  # array
        return cur_data_type

    def process_data_tokens(self, v, width):
        elements = 0
        reslist = []
        is_string = False
        base = 1 << (8 * width)

        if isinstance(v, list):
            for vv in v:
                ele, is_string2, rr2 = self.process_data_tokens(vv, width)
                elements += ele
                is_string |= is_string2
                reslist += rr2
        elif isinstance(v, Token):
            if v.type in ['offsetdir', 'segmdir']:
                if isinstance(v.value, list):  # hack when '+' is glued to integer
                    v.value = Token.remove_tokens(v.value, ['expr'])
                    lst = [v.value[0]]
                    for val in v.value[1:]:
                        if isinstance(val, Token) and val.type == 'INTEGER':
                            lst += ['+']
                        lst += [val]
                    v.value = lst
                elements, is_string, reslist = self.process_data_tokens(v.value, width)
            elif v.type == 'expr':
                el, is_string, res = self.process_data_tokens(v.value, width)
                if not is_string and len(res) != 1:
                    reslist = ["".join(str(x) for x in res)]
                    elements = 1
                else:
                    reslist = res
                    elements = el
            elif v.type == 'STRING':
                v = v.value
                assert isinstance(v, str)
                if not self.itislst:  # but not for IDA .lst
                    v = v.replace("\'\'", "'").replace('\"\"', '"')  # masm behaviour
                reslist = list(v[1:-1])
                elements = len(reslist)
                is_string = True

            # check if dup
            elif v.type == 'dupdir':
                # we should parse that
                repeat = Parser.parse_int(self.escape(v.value[0]))
                values = self.process_data_tokens(v.value[1], width)[2]
                elements, reslist = self.action_dup(repeat, values)

            elif v.type == 'INTEGER':
                elements += 1
                try:  # just number or many
                    v = v.value
                    # if v == '?':
                    #    v = '0'
                    v = Parser.parse_int(v)

                    if v < 0:  # negative values
                        v += base

                except Exception:
                    # global name
                    # traceback.print_stack(file=sys.stdout)
                    # logging.debug "global/expr: ~%s~" %v
                    try:
                        v = self.get_global_value(v, width)
                    except KeyError:
                        v = 0
                reslist = [v]

            # logging.debug("global/expr: ~%s~" % v)
            elif v.type == 'LABEL':
                elements = 1
                try:
                    v = v.value
                    # width = 2  # TODO for 16 bit only
                    v = self.mangle_label(v)
                    v = self.get_global_value(v, width)
                except KeyError:
                    if self.pass_number != 1:
                        logging.error("unknown address %s" % v)
                    # logging.warning(self.c_data)
                    # logging.warning(r)
                    # logging.warning(len(self.c_data) + len(r))
                    # self.__link_later.append((len(self.c_data) + len(r), v))
                    # v = 0
                reslist = [v]
        elif v == '?':
            elements = 1
            reslist = [0]
        else:
            elements = 1
            reslist = [v]
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
        logging.debug("label name: %s" % name)
        if name == '@@':
            name = self.get_dummy_jumplabel()
        name = self.mangle_label(name)

        # logging.debug("offset %s -> %s" % (name, "&m." + name.lower() + " - &m." + self.__segment_name))

        self.need_label = False
        self.make_sure_proc_exists(line_number, raw)

        # if self.proc:
        l = op.label(name, proc=self.proc.name, isproc=isproc, line_number=self.__offset_id, far=far, globl=globl)
        _, l.real_offset, l.real_seg = self.get_lst_offsets(raw)

        if l.real_seg:
            self.procs_start.discard(l.real_seg*0x10 + l.real_offset)
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
            #pname = f'{self.__segment.name}_proc'
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
                op.Data(label, 'db', DataType.ARRAY, [0], num, num, comment='for alignment', align=True, offset=offset))

    def move_offset(self, pointer, raw):
        if pointer > self.__binary_data_size:
            self.data_merge_candidats = 0
            label = self.get_dummy_label()

            num = pointer - self.__binary_data_size
            offset = self.__binary_data_size
            self.__binary_data_size += num

            self.__segment.append(
                op.Data(label, 'db', DataType.ARRAY, [0], num, num, comment='move_offset', align=True, offset=offset))
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
        self.__current_file = file_name
        self.__current_file_hash = hashlib.blake2s(self.__current_file.encode('utf8')).hexdigest()
        content = read_whole_file(file_name)
        if file_name.lower().endswith('.lst'):  # for .lst provided by IDA move address to comments after ;~
            # we want exact placement so program could work
            self.itislst = True
            segmap = self.read_segments_map(file_name)
            content = re.sub(r'^(?P<segment>[_0-9A-Za-z]+):(?P<offset>[0-9A-Fa-f]{4,8})(?P<remain>.*)',
                             lambda m: f'{m.group("remain")} ;~ {segmap.get(m.group("segment"))}:{m.group("offset")}',
                             content, flags=re.MULTILINE)
        self.parse_args_new_data(content, file_name=file_name)

    def read_segments_map(self, file_name):
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
        self.__files.add(self.__current_file)
        self.__current_file = file_name
        content = read_whole_file(file_name)
        result = self.parse_file_inside(content, file_name=file_name)
        self.__current_file = self.__files.pop()
        return result

    def action_assign(self, label, value, raw='', line_number=0):
        label = self.mangle_label(label)

        # if self.has_global(label):
        #    label = self.get_global(label).original_name
        o = self.proc.create_assignment_op(label, value, line_number=line_number)
        o.filename = self.__current_file
        o.raw_line = raw.rstrip()
        self.reset_global(label, o)
        self.proc.stmts.append(o)
        return o

    def action_assign_test(self, label="", value="", raw='', line_number=0):
        o = self.action_assign(label, value, raw, line_number)
        o.implemented = True

    def action_equ_test(self, label="", value="", raw='', line_number=0):
        o = self.action_equ(label, value, raw, line_number)
        o.implemented = True

    def return_empty(self, _):
        return []

    def action_equ(self, label="", value="", raw='', line_number=0):
        label = self.mangle_label(label)
        value = Token.remove_tokens(value, ['expr'])
        size = Cpp(self).get_size(value)
        ptrdir = Token.find_tokens(value, 'ptrdir')
        if ptrdir:
            type = ptrdir[0]
            if isinstance(type, Token):
                type = type.value
            type = type.lower()
            value = Token.find_and_replace_tokens(value, 'ptrdir', self.return_empty)
        o = Proc.create_equ_op(label, value, line_number=line_number)
        o.filename = self.__current_file
        o.raw_line = raw.rstrip()
        o.size = size
        if ptrdir:
            o.original_type = type
        self.set_global(label, o)
        proc = self.get_global("mainproc")
        proc.stmts.append(o)
        return o

    def create_segment(self, name, options=None, segclass=None, raw=''):
        logging.info("     Found segment %s" % name)
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
            logging.debug("segment %s %x" % (name, offset))
            binary_width = 0

            self.__segment = Segment(name, offset, options=options, segclass=segclass)
            self.segments[name] = self.__segment
            # self.__segment.append(op.Data(name, 'db', DataType.ARRAY, [], 0, 0, comment='segment start zero label'))

            self.set_global(name, op.var(binary_width, offset, name, issegment=True))

    def action_proc(self, name, type, line_number=0, raw=''):
        logging.info("      Found proc %s" % name.value)
        self.action_endp()
        name = self.mangle_label(name.value)
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
            self.procs_start.discard(real_seg*0x10 + real_offset)
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
        logging.debug("segment %s ends" % self.__segment_name)
        self.__segment_name = "default_seg"

    def action_include(self, name):
        logging.info("including %s" % name)
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
        self.test_mode = True
        self.need_label = False
        self.segments = OrderedDict()
        try:
            result = self.parse_args_new_data_('''.model tiny
    default_seg segment
        ''' + line + '''
    default_seg ends
        end start
        ''').asminstruction
        except Exception as e:
            print(e)
            logging.error("Error1")
            result = [str(e)]
            raise
        del self.__globals['default_seg']
        return result

    def test_size(self, line):
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            result = self.parse_args_new_data_('''.model tiny
        default_seg segment
        mov ax, ''' + line + '''
        default_seg ends
            end start
            ''').asminstruction.args[1]
        except Exception as e:
            print(e)
            logging.error("Error2")
            result = [str(e)]
            raise
        del self.__globals['default_seg']
        return result

    def action_data(self, line):
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            result = self.parse_args_new_data_('''.model tiny
    default_seg segment
    ''' + line + '''
    default_seg ends
    end start
    ''')
        except Exception as e:
            print(str(e))
            logging.error("Error3")
            result = [str(e)]
            raise
        del self.__globals['default_seg']
        return result

    def parse_arg(self, line):
        self.test_mode = True
        self.segments = OrderedDict()
        try:
            result = self.parse_args_new_data_('''.model tiny
        default_seg segment
        mov ax, ''' + line + '''
        default_seg ends
        end start
        ''').asminstruction.args[1]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e,exc_type, fname, exc_tb.tb_lineno)
            logging.error("Error4")
            #result = [f'{e} {exc_type} {fname} {exc_tb.tb_lineno}']
            raise
        del self.__globals['default_seg']
        return result

    def parse_include(self, line, file_name=None):
        # parser = PGParser(self.__lex.grammar,
        #                            actions=actions)
        grammar = self.__lex.or_grammar
        parser = copy(self.__lex.or_parser)
        parser.grammar = grammar
        try:
            result = parser.parse('''.model tiny
            ''' + line + '''
            end
            ''', file_name=file_name, extra=self)  # context = self.__pgcontext)
        except parglare.exceptions.ParseError:
            result = parser.parse(f'''.model tiny
            {self.__segment.name} segment
            {line}
            {self.__segment.name} ends
            end
            ''', file_name=file_name, extra=self)  # context = self.__pgcontext)
            # del self.__globals['some_seg']

        return result

    def escape(self, s):
        if isinstance(s, list):
            return [self.escape(i) for i in s]
        elif isinstance(s, Token):
            return self.escape(s.value)
        else:
            s = s.translate(s.maketrans({"\\": r"\\"}))
            # if not self.itislst:
            s = s.replace("''", "'").replace('""', '"')
            return s

    def calculate_data_size_new(self, size, values):
        if isinstance(values, list):
            return sum(self.calculate_data_size_new(size, x) for x in values)
        elif isinstance(values, Token):
            if values.type == 'expr':
                if isinstance(values.value, Token) and values.value.type == STRINGCNST:
                    return self.calculate_data_size_new(size, values.value)
                else:
                    return size
            elif values.type == STRINGCNST:
                return self.calculate_STRING_size(values.value)
            elif values.type == 'dupdir':
                return Parser.parse_int(self.escape(values.value[0])) * self.calculate_data_size_new(size,
                                                                                                     values.value[1])
            else:
                return size
        elif isinstance(values, str):
            if values == '?':
                return size
            return len(values)
        else:
            raise NotImplementedError('Unknown Token: ' + str(values))

    def datadir_action(self, label, type, args, raw='', line_number=0):
        if self.__cur_seg_offset > 0xffff:
            return []
        if self.__cur_seg_offset & 0xff == 0:
            logging.info(f"      Current offset {self.__cur_seg_offset:x} line={line_number}")
        isstruct = len(self.struct_names_stack) != 0

        label = self.mangle_label(label)
        binary_width = self.typetosize(type)
        size = self.calculate_data_size_new(binary_width, args)

        offset = self.__cur_seg_offset
        if not isstruct:

            self.adjust_offset_to_real(raw, label)

            offset = self.__cur_seg_offset
            if not self.flow_terminated:
                logging.error(f"Flow wasn't terminated! line={line_number} offset={self.__cur_seg_offset}")

            logging.debug("args %s offset %d" % (str(args), offset))

        logging.debug("convert_data %s %d %s" % (label, binary_width, args))
        # original_label = label

        elements, is_string, array = self.process_data_tokens(args, binary_width)
        data_internal_type = self.identify_data_internal_type(array, elements, is_string)
        if data_internal_type == DataType.ARRAY and not any(array) and not isstruct:  # all zeros
            array = [0]

        logging.debug("~size %d elements %d" % (binary_width, elements))
        if label and not isstruct:
            self.set_global(label, op.var(binary_width, offset, name=label,
                                          segment=self.__segment_name, elements=elements, original_type=type,
                                          filename=self.__current_file, raw=raw, line_number=line_number))

        dummy_label = False
        if len(label) == 0:
            dummy_label = True
            label = self.get_dummy_label()

        if isstruct:
            data_type = 'struct data'
        else:
            self.__binary_data_size += size
            self.__cur_seg_offset += size
            data_type = 'usual data'
        data = op.Data(label, type, data_internal_type, array, elements, size, filename=self.__current_file,
                       raw_line=raw,
                       line_number=line_number, comment=data_type, offset=offset)
        if isstruct:
            self.current_struct.append(data)
        else:
            _, data.real_offset, data.real_seg = self.get_lst_offsets(raw)
            self.__segment.append(data)
            if dummy_label and data_internal_type == DataType.NUMBER and binary_width == 1:
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
                    f'Cannot merge {self.__segment.getdata()[-size].label} - {self.__segment.getdata()[-1].label}')
                self.data_merge_candidats = 0
            else:
                logging.debug(
                    f'Merging data at {self.__segment.getdata()[-size].label} - {self.__segment.getdata()[-1].label}')
                array = [x.array[0] for x in self.__segment.getdata()[-size:]]
                if not any(array):  # all zeros
                    array = [0]

                self.__segment.getdata()[-size].array = array
                self.__segment.getdata()[-size].elements = size
                self.__segment.getdata()[-size].data_internal_type = DataType.ARRAY
                self.__segment.getdata()[-size].size = size
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

    def parse_args_new_data_(self, text):
        # self.__pgcontext = PGContext(extra = self)
        self.__binary_data_size = 0
        # TODO check if required self.__c_dummy_label = 0  # one dummy number is used for "default_seg" creation
        self.__c_dummy_jump_label = 0
        self.__c_extra_dummy_jump_label = 0
        return self.parse_file_insideseg(text)

    def parse_file_insideseg(self, text):
        return self.parse_args_new_data(text)[0][1][1][0].insegmentdir

    def parse_file_inside(self, text, file_name=None):
        return self.parse_include(text, file_name)

    def parse_args_new_data(self, text, file_name=None):
        logging.debug("parsing: [%s]" % text)

        result = self.__lex.parser.parse(text, file_name=file_name, extra=self)

        logging.debug(str(result))
        return result

    @staticmethod
    def mangle_label(name):
        name = name.lower()  # ([A-Za-z@_\$\?][A-Za-z0-9@_\$\?]*)
        return name.replace('@', "arb").replace('?', "que").replace('$', "dol")

    @staticmethod
    def is_register(expr):
        expr = expr.lower()
        size = 0
        if len(expr) == 2 and expr[0] in ['a', 'b', 'c', 'd'] and expr[1] in ['h', 'l']:
            logging.debug('is reg res 1')
            size = 1
        elif expr in ['ax', 'bx', 'cx', 'dx', 'si', 'di', 'sp', 'bp', 'ds', 'cs', 'es', 'fs', 'gs', 'ss']:
            logging.debug('is reg res 2')
            size = 2
        elif expr in ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp']:
            logging.debug('is reg res 4')
            size = 4
        return size

    def typetosize(self, value):
        if isinstance(value, Token):
            value = value.value
        if not isinstance(value, str):
            logging.error("Type is not a string TODO " + str(value))
            return 0
        value = value.lower()
        if value in self.structures.keys():
            return self.structures[value].getsize()
        try:
            size = {'db': 1, 'byte': 1, 'sbyte': 1,
                    'dw': 2, 'word': 2, 'sword': 2, 'small': 2, 'near': 2,
                    'dd': 4, 'dword': 4, 'sdword': 4, 'large': 4, 'far': 4, 'real4': 4,
                    'df': 6, 'fword': 6,
                    'dq': 8, 'qword': 8, 'real8': 8,
                    'dt': 10, 'tbyte': 10, 'real10': 10}[value]
        except KeyError:
            logging.error("Cannot find size for %s" % value)
            size = 0
        return size

    def convert_members(self, data, values):
        if data.isobject():
            return [self.convert_members(m, v) for m, v in zip(data.getmembers(), values)]
        else:
            type = data.gettype()
            binary_width = self.typetosize(type)
            _, _, array = self.process_data_tokens(values, binary_width)
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
            cpp = Cpp(self)
            number = eval(cpp.expand(Token.find_tokens(args[0], 'expr')))
            args = args[3]
        args = Token.remove_tokens(args, ['structinstance'])

        d = op.Data(label, type, DataType.OBJECT, args, 1, s.getsize(), comment='struct instance', offset=offset)
        members = [deepcopy(i) for i in s.getdata().values()]
        d.setmembers(members)
        args = self.convert_members(d, args)
        d.setvalue(args)

        if number > 1:
            d = op.Data(label, type, DataType.ARRAY, number * [d], number, number * s.getsize(), comment='object array',
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
        strtype = type
        if isinstance(type, Token):
            strtype = type.value
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
            logging.debug("procedure %s, extern" % label)
            self.reset_global(label, proc)
            # else:
            #    self.reset_global(label, op.label(label, proc=self.proc.name, isproc=True))

    def add_call_to_entrypoint(self):
        # if self.__separate_proc:
        proc = self.get_global('mainproc')
        o = proc.create_instruction_object('call', [self.entry_point])
        o.filename = self.__current_file
        o.raw_line = ''
        o.line_number = 0
        proc.stmts.append(o)
        o = proc.create_instruction_object('ret')
        o.filename = self.__current_file
        o.raw_line = ''
        o.line_number = 0
        proc.stmts.append(o)

    def action_instruction(self, instruction, args, raw='', line_number=0):
        self.handle_local_asm_jumps(instruction, args)

        self.make_sure_proc_exists(line_number, raw)

        o = self.proc.create_instruction_object(instruction, args)
        o.filename = self.__current_file
        o.raw_line = raw
        o.line_number = line_number
        if self.current_macro == None:
            _, o.real_offset, o.real_seg = self.get_lst_offsets(raw)
            if not self.need_label and o.real_seg and len(self.procs_start) \
                    and (o.real_seg*0x10+o.real_offset) in self.procs_start:
                logging.warning(f"Add a label since run-time info contain flow enter at this address {o.real_seg:x}:{o.real_offset:x} line={line_number}")
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
        else:
            self.current_macro.instructions.append(o)
        return o

    def handle_local_asm_jumps(self, instruction, args):
        if (instruction[0].lower() == 'j' or instruction[0].lower() == 'loop') and \
                len(args) == 1 and isinstance(args[0], Token) and \
                isinstance(args[0].value, Token) and args[0].value.type == 'LABEL':
            if args[0].value.value.lower() == '@f':
                args[0].value.value = "dummylabel" + str(self.__c_dummy_jump_label + 1)
            elif args[0].value.value.lower() == '@b':
                args[0].value.value = "dummylabel" + str(self.__c_dummy_jump_label)

    def collect_labels(self, target, operation):
        for arg in operation.args:
            labels = Token.find_tokens(arg, 'LABEL')
            #  If it is call to a proc then does not take it into account
            #  TODO: check for calls into middle of proc
            if labels and not operation.cmd.startswith('call') and not (self.args.mergeprocs == 'separate' and operation.cmd == 'jmp'):
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
            self.entry_point = Token.find_tokens(label, 'LABEL')[0].lower()
            self.add_call_to_entrypoint()

    def get_segments(self):
        return self.segments

    def parse_rt_info(self, name):
        #dbx_img_offset = int(self.args.loadsegment, 0)  # para
        #ida_load = 0x1000

        try:
            with open(name+".json") as infile:
                logging.info(f' *** Loading {name}.json')
                j = jsonpickle.decode(infile.read())
                self.initial_procs_start = self.procs_start = set(j['Jumps'])
        except FileNotFoundError:
            pass
