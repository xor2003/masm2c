from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import re
import sys
from builtins import chr
from builtins import hex
from builtins import object
from builtins import range
from builtins import str
from copy import copy

import parglare
from parglare import Grammar, Parser as PGParser

from masm2c import cpp
from masm2c.proc import Proc
from masm2c import proc
from masm2c import op
from masm2c.Token import Token

# from parglare.parser import Context as PGContext
# action = get_collector()
# ScummVM - Graphic Adventure Engine
#
# ScummVM is the legal property of its developers, whose names
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
INTEGERCNST = 'INTEGER'
STRINGCNST = 'STRING'


def escape(s):
    if isinstance(s, list):
        return [escape(i) for i in s]
    elif isinstance(s, Token):
        return escape(s.value)
    else:
        return s.translate(s.maketrans({"\\": r"\\"})).replace("''", "'").replace('""', '"')


def read_asm_file(file_name):
    logging.info("opening file %s..." % file_name)
    if sys.version_info >= (3, 0):
        fd = open(file_name, 'rt', encoding="cp437")
    else:
        fd = open(file_name, 'rt')
    content = fd.read()
    fd.close()
    return content


macroids = []
structtags = []
macroidre = re.compile(r'([A-Za-z@_\$\?][A-Za-z0-9@_\$\?]*)')


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
    return context.input_str[context.start_position: context.end_position]


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


def INTEGER(context, nodes):
    return Token('INTEGER', cpp.convert_number_to_c(nodes))


def macroid(head, s, pos):
    mtch = macroidre.match(s[pos:])
    if mtch:
        result = mtch.group().lower()
        # logging.debug ("matched ~^~" + result+"~^~")
        if result in macroids:
            logging.debug(" ~^~" + result + "~^~ in macroids")
            return result
        else:
            return None
    else:
        return None

def macrodir(_, nodes, name):
    macroids.insert(0, name.value.lower())
    logging.debug("macroid added ~~" + name.value + "~~")

def structtag(head, s, pos):
    mtch = macroidre.match(s[pos:])
    if mtch:
        result = mtch.group().lower()
        # logging.debug ("matched ~^~" + result+"~^~")
        if result in structtags:
            logging.debug(" ~^~" + result + "~^~ in structtags")
            return result
        else:
            return None
    else:
        return None

def structdir(context, nodes, name, item):
    logging.debug("structdir", str(nodes))
    structtags.insert(0, name.value.lower())
    logging.debug("structtag added ~~" + name.value + "~~")
    return []  # Token('structdir', nodes) TODO ignore by now

def structinstdir(context, nodes, label, type, values):
    logging.debug("structinstdir" + str(label) + str(type) + str(values))
    return nodes  # Token('structdir', nodes) TODO ignore by now

def calculate_data_size_new(size, values):
    if isinstance(values, list):
        return sum(calculate_data_size_new(size, x) for x in values)
    elif isinstance(values, Token):
        if values.type == 'expr':
            if isinstance(values.value, Token) and values.value.type == STRINGCNST:
                return calculate_data_size_new(size, values.value)
            else:
                return size
        elif values.type == STRINGCNST:
            return Parser.calculate_STRING_size(values.value)
        elif values.type == 'dupdir':
            return Parser.parse_int(escape(values.value[0])) * calculate_data_size_new(size, values.value[1])
        else:
            return size
    elif isinstance(values, str):
        if values == '?':
            return size
        return len(values)
    else:
        raise Exception('Unknown Token: ' + str(values))


def remove_dupdir(values):
    if isinstance(values, list):
        return [remove_dupdir(x) for x in values]
    elif isinstance(values, Token) and values.type == 'dupdir':
        return Parser.parse_int(escape(values.value[0])) * remove_dupdir(values.value[1])
    elif isinstance(values, str) and values == '?':
        return 0
    return values


def datadir(context, nodes, label, type, values):
    logging.debug("datadir " + str(nodes) + " ~~")
    if label:
        label = label.value
    else:
        label = ""
    label = context.extra.mangle_label(label)

    if Token.find_and_call_tokens(nodes, 'structinstance'):
        return []

    binary_width = calculate_type_size(type)
    size = calculate_data_size_new(binary_width, values)

    #values = Token.remove_tokens(values, ['expr'])
    '''
    values = remove_dupdir(values) # temporary fix unittests

    if isinstance(values, list):
        s = []
        for x in values:
            if isinstance(x, Token):
                s = s + [x.value]
            else:
                s = s + [x]
        values = s
    elif isinstance(values, Token):
        if values.type=='dupdir':
            values = Parser.parse_int(escape(values.value[0])) * [values.value[1]]
        else:
            values = values.value

    values = escape(values)
    '''

    return context.extra.datadir_action(label.lower(), type, values, size)


def includedir(context, nodes, name):
    # context.parser.input_str = context.input_str[:context.end_position] + '\n' + read_asm_file(name) \
    # + '\n' + context.input_str[context.end_position:]
    result = context.extra.parse_include_file_lines(name)
    return result


def segdir(context, nodes, type):
    logging.debug("segdir " + str(nodes) + " ~~")
    context.extra.action_simplesegment(type, '')  #TODO
    return nodes


def segmentdir(context, nodes, name):
    logging.debug("segmentdir " + str(nodes) + " ~~")
    context.extra.action_segment(name.value)
    return nodes


def endsdir(context, nodes, name):
    logging.debug("ends " + str(nodes) + " ~~")
    context.extra.action_endseg()
    return nodes


def procdir(context, nodes, name, type):
    logging.debug("procdir " + str(nodes) + " ~~")
    context.extra.action_proc(name, type)
    return nodes


def endpdir(context, nodes, name):
    logging.debug("endp " + str(name) + " ~~")
    context.extra.action_endp()
    return nodes


def equdir(context, nodes, name, value):
    logging.debug("equdir " + str(nodes) + " ~~")
    return context.extra.action_equ(name, value)


def assdir(context, nodes, name, value):
    logging.debug("assdir " + str(nodes) + " ~~")
    return context.extra.action_assign(name, value)


def labeldef(context, nodes, name):
    logging.debug("labeldef " + str(nodes) + " ~~")
    return context.extra.action_label(name.value)


def instrprefix(context, nodes):
    logging.debug("instrprefix " + str(nodes) + " ~~")
    instruction = nodes[0]
    o = context.extra.proc.create_instruction_object(instruction)
    o.line = get_raw(context)
    o.line_number = get_line_number(context)
    context.extra.proc.stmts.append(o)
    return []


def asminstruction(context, nodes, instruction, args):
    logging.debug("instruction " + str(nodes) + " ~~")
    # if args:
    #    args = [listtostring(i) for i in args] # TODO temporary workaround
    # args = build_ast(args)
    if not instruction:
        return nodes
    if args is None:
        args = []
    o = context.extra.proc.create_instruction_object(instruction, args)
    o.line = get_raw(context)
    o.line_number = get_line_number(context)
    context.extra.proc.stmts.append(o)
    return o


def enddir(context, nodes, label):
    logging.debug("end " + str(nodes) + " ~~")
    if label:
        context.extra.entry_point = Token.find_and_call_tokens(label, 'LABEL')[0].lower()
    return nodes


def notdir(context, nodes):
    nodes[0] = '~'
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
    logging.debug("offset /~" + str(nodes) + "~\\")
    # global indirection
    # indirection = -1
    return Token('segmdir', nodes[1])


def LABEL(context, nodes):
    return Token('LABEL', nodes)


def STRING(context, nodes):
    return Token('STRING', nodes)

def memberdir(context, nodes, variable, field):
    result = Token('memberdir', [variable, field])
    logging.debug(result)
    return result

actions = {
    "field": make_token,
    "memberdir": memberdir,
    "structinstdir": structinstdir,
    "dupdir": dupdir,
    "structinstance": make_token,
    "structdir": structdir,
    "includedir": includedir,
    "instrprefix": instrprefix,
    "INTEGER": INTEGER,
    "LABEL": LABEL,
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
    "macrodir": macrodir,
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
    'macroid': macroid,
    "structtag": structtag
}


class ParglareParser(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ParglareParser, cls).__new__(cls)
            logging.debug("Allocated ParglareParser instance")

            file_name = os.path.dirname(os.path.realpath(__file__)) + "/_masm61.pg"
            cls._inst.or_grammar = Grammar.from_file(file_name, ignore_case=True, recognizers=recognizers)
            ## cls._inst.parser = PGParser(grammar, debug=True, debug_trace=True, actions=action.all)
            ## cls._inst.parser = PGParser(grammar, debug=True, actions=action.all)
            cls._inst.or_parser = PGParser(cls._inst.or_grammar,
                                           actions=actions)  # , build_tree = True, call_actions_during_tree_build = True)

            cls._inst.grammar = cls._inst.or_grammar
            cls._inst.parser = copy(cls._inst.or_parser)
            cls._inst.parser.grammar = cls._inst.grammar

        return cls._inst


def dump_object(value):
    stuff = str(value.__dict__)
    replacements = [
        (r'\n', ' '),
        (r'[{}]', ''),
        (r"'([A-Za-z_0-9]+)'\s*:\s*", '\g<1>=')
    ]
    for old, new in replacements:
        stuff = re.sub(old, new, stuff)
    stuff = value.__class__.__name__ + "(" + stuff + ")"
    return stuff


def calculate_type_size(type):
    return Parser.typetosize(type)


class Parser:
    def __init__(self, skip_binary_data=[]):
        self.__skip_binary_data = skip_binary_data
        self.strip_path = 0
        self.__globals = {}
        self.__offsets = {}
        self.__offset_id = 0x1111
        self.__stack = []
        self.proc_list = []

        self.entry_point = ""

        # self.proc = None
        nname = "mainproc"
        self.proc = Proc(nname)
        self.proc_list.append(nname)
        self.set_global(nname, self.proc)

        self.__binary_data_size = 0
        self.c_data = []
        self.h_data = []
        self.__cur_seg_offset = 0
        self.__dummy_enum = 0
        self.__segment = "default_seg"

        # self.__symbols = []
        self.__link_later = []
        # self.data_started = False
        # self.prev_data_type = 0
        # self.prev_data_ctype = 0
        self.line_number = 0
        self.__lex = ParglareParser()
        self.used = False
        # self.__pgcontext = PGContext(extra = self)

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

    def set_global(self, name, value):
        if len(name) == 0:
            raise Exception("empty name is not allowed")
        value.original_name = name
        name = name.lower()

        stuff = dump_object(value)
        logging.debug("set_global(name='%s',value=%s)" % (name, stuff))
        if name in self.__globals:
            raise Exception("global %s was already defined", name)
        value.used = False
        self.__globals[name] = value

    '''
    def reset_global(self, name, value):
            if len(name) == 0:
                    raise Exception("empty name is not allowed")
            name = name.lower()
            logging.debug("adding global %s -> %s" %(name, value))
            self.__globals[name] = value
    '''

    def get_global(self, name):
        name = name.lower()
        logging.debug("get_global(%s)" % name)
        try:
            g = self.__globals[name]
            logging.debug(g)
        except KeyError:
            logging.debug("get_global KeyError %s" % name)
            raise
        g.used = True
        assert self.__globals[name].used
        return g

    def get_globals(self):
        return self.__globals

    def has_global(self, name):
        name = name.lower()
        return name in self.__globals

    def set_offset(self, name, value):
        if len(name) == 0:
            raise Exception("empty name is not allowed")
        name = name.lower()
        logging.debug("adding offset %s -> %s" % (name, value))
        if name in self.__offsets:
            raise Exception("offset %s was already defined", name)
        self.__offsets[name] = value

    def get_offset(self, name):
        return self.__offsets[name.lower()]

    def evall(self, stmt):
        try:
            return Parser.parse_int(stmt)
        except:
            pass
        value = self.__globals[stmt.lower()].value
        return int(value)

    def expr_callback(self, match):
        name = match.group(1).lower()
        g = self.get_global(name)
        if isinstance(g, op.equ) or isinstance(g, op.assignment):
            return g.value
        else:
            return "0x%04x" % g.offset

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
                except:
                    pass
                vv += str(i)
            v = vv
        v = v.strip()
        # logging.debug "~2~ %s" %v
        if re.match(r'^[+-]?[0-9][0-9A-Fa-f]*[Hh]$', v):
            v = int(v[:-1], 16)
            # logging.debug "~3~ %i" %v
        elif re.match(r'^[01]+[Bb]$', v):
            v = int(v[:-1], 2)
            # logging.debug "~2~ %i" %v

        try:
            vv = eval(v)
            v = vv
        except:
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

    @staticmethod
    def calculate_STRING_size(v):
        v = v.replace("\'\'", "'").replace('\"\"', '"')
        return len(v) - 2

    def get_global_value(self, v, base):
        logging.debug("get_global_value(%s)" % v)
        v = self.mangle_label(v)
        g = self.get_global(v)
        logging.debug(g)
        if isinstance(g, op._equ) or isinstance(g, op._assignment):
            v = g.original_name
        elif isinstance(g, op.var):
            v = "offset(%s,%s)" % (g.segment, g.name)
        elif isinstance(g, op.label):
            v = "k%s" % (g.name.lower())
        else:
            v = g.offset
        logging.debug(v)
        return v

    def convert_data_to_c(self, label, width, data):
        """ Generate C formated data """
        logging.debug("convert_data_to_c %s %d %s" % (label, width, data))
        # original_label = label
        label = label.lower()



        elements, is_string, r = self.process_data_tokens(data, width)

        base = 1 << (8 * width)
        data_ctype = {1: 'db', 2: 'dw', 4: 'dd', 8: 'dq', 10: 'dt'}[width]
        rh = []
        # cur_data_type = 0
        if is_string:
            if len(r) >= 2 and r[-1] == 0:
                cur_data_type = 1  # 0 terminated string
            else:
                cur_data_type = 2  # array string

        else:
            cur_data_type = 3  # number
            if elements > 1:
                cur_data_type = 4  # array of numbers

        logging.debug("current data type = %d current data c type = %s" % (cur_data_type, data_ctype))

        if len(label) == 0:
            self.__dummy_enum += 1
            label = "dummy" + str(self.__dummy_enum)

        vh = ""
        vc = ""

        if cur_data_type == 1:  # 0 terminated string
            vh = "char " + label + "[" + str(len(r)) + "]"

        elif cur_data_type == 2:  # array string
            vh = "char " + label + "[" + str(len(r)) + "]"
            vc = "{"

        elif cur_data_type == 3:  # number
            vh = data_ctype + " " + label

        elif cur_data_type == 4:  # array
            vh = data_ctype + " " + label + "[" + str(elements) + "]"
            vc = "{"

        if cur_data_type == 1:  # string
            vv = "\""
            for i in range(0, len(r) - 1):
                vv += self.convert_str(r[i])
            vv += "\""
            r = ["", vv]

        elif cur_data_type == 2:  # array of char
            vv = ""
            logging.debug(r)
            for i in range(0, len(r)):
                vv += self.convert_char(r[i])
                if i != len(r) - 1:
                    vv += ","
            r = ["", vv]

        elif cur_data_type == 3:  # number
            r[0] = str(r[0])

        elif cur_data_type == 4:  # array of numbers
            # vv = ""
            for i in range(0, len(r)):
                r[i] = str(r[i])
                if i != len(r) - 1 :
                    r[i] += ","

        r.insert(0, vc)
        rh.insert(0, vh)
        # if it was array of numbers or array string
        if cur_data_type == 4 or cur_data_type == 2:
            r.append("}")

        r.append(", // " + label + "\n")  # TODO can put original_label
        rh.append(";\n")

        logging.debug(r)
        logging.debug(rh)
        logging.debug("returning")

        r = "".join(r)
        rh = "".join(rh)
        return r, rh, elements

    def convert_char(self, c):
        if isinstance(c, int) and c not in [10, 13]:
            return str(c)
        return "'" + self.convert_str(c) + "'"

    def convert_str(self, c):
        vvv = ""
        if isinstance(c, int):
            if c == 13:
                vvv = r"\r"
            elif c == 10:
                vvv = r"\n"
            elif c < 10:
                vvv = "\\{:01x}".format(c)
            elif c < 32:
                vvv = "\\x{:02x}".format(c)
            else:
                vvv = chr(c)
        elif isinstance(c, str):
            # logging.debug "~~ " + r[i] + str(ord(r[i]))
            if c in ["\'", '\"', '\\']:
                vvv = "\\" + c
            elif ord(c) > 127:
                vvv = '\\' + hex(ord(c.encode('cp437', 'backslashreplace')))[1:]
                #vvv = c
            elif c == '\0':
                vvv = '\\0'
            else:
                vvv = c
            #vvv = "'" + vvv + "'"
        return vvv

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
                v = v.replace("\'\'", "'").replace('\"\"', '"')
                res = []
                for i in range(1, len(v) - 1):
                    res.append(v[i])
                reslist = res
                elements = len(v) - 2
                is_string = True

            # check if dup
            elif v.type == 'dupdir':
                # we should parse that
                repeat = Parser.parse_int(escape(v.value[0]))
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

                except:
                    # global name
                    # traceback.print_stack(file=sys.stdout)
                    # logging.debug "global/expr: ~%s~" %v
                    try:
                        v = self.get_global_value(v, base)
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
                    v = self.get_global_value(v, base)
                except KeyError:
                    logging.warning("unknown address %s" % v)
                    logging.warning(self.c_data)
                    # logging.warning(r)
                    # logging.warning(len(self.c_data) + len(r))
                    # self.__link_later.append((len(self.c_data) + len(r), v))
                    #v = 0
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
                '''
                else:
                    try:
                        value = Parser.parse_int(str(value))
                    except:
                        value = str(value)
                '''
            # logging.debug "n = %d value = %d" %(n, value)

            res.append(value)
        return n * len(values), res

    def action_label_(self, line, far=False, isproc=False):
        # logging.info(line)
        m = re.match('([@\w]+)\s*::?', line)
        name = m.group(1).strip()
        logging.debug(name)
        self.action_label(name=name, far=far, isproc=isproc)

    def action_label(self, name, far=False, isproc=False):
        # if self.visible():
        # name = m.group(1)
        # logging.debug "~name: %s" %name
        name = self.mangle_label(name)
        # logging.debug "~~name: %s" %name
        if not (name in self.__skip_binary_data):
            logging.debug("offset %s -> %s" % (name, "&m." + name.lower() + " - &m." + self.__segment))
            '''
            if self.proc is None:
                    nname = "mainproc"
                    self.proc = proc(nname)
                    #logging.debug "procedure %s, #%d" %(name, len(self.proc_list))
                    self.proc_list.append(nname)
                    self.set_global(nname, self.proc)
            '''
            if self.proc:
                self.proc.add_label(name, isproc)
                # self.set_offset(name, ("&m." + name.lower() + " - &m." + self.segment, self.proc, len(self.proc.stmts)))
                self.set_offset(name, ("&m." + name.lower() + " - &m." + self.__segment, self.proc, self.__offset_id))
                self.set_global(name, op.label(name, proc.Proc, line_number=self.__offset_id, far=far))
                self.__offset_id += 1
            else:
                logging.error("!!! Label %s is outside the procedure" % name)
        else:
            logging.info("skipping binary data for %s" % (name,))

    def create_segment(self, name):
        binary_width = 1
        offset = self.__binary_data_size // 16
        logging.debug("segment %s %x" % (name, offset))
        self.__cur_seg_offset = 16

        num = (0x10 - (self.__binary_data_size & 0xf)) & 0xf
        if num:
            l = ['0'] * num
            self.__binary_data_size += num

            self.__dummy_enum += 1
            labell = "dummy" + str(self.__dummy_enum)

            self.c_data.append("{" + ",".join(l) + "}, // padding\n")
            self.h_data.append(" db " + labell + "[" + str(num) + "]; // padding\n")

        num = 0x10
        l = ['0'] * num
        self.__binary_data_size += num

        self.c_data.append("{" + ",".join(l) + "}, // segment " + name + "\n")
        self.h_data.append(" db " + name + "[" + str(num) + "]; // segment " + name + "\n")

        self.set_global(name, op.var(binary_width, offset, name, issegment=True))
        '''
        if self.proc == None:
                name = "mainproc"
                self.proc = proc(name)
                #logging.debug "procedure %s, #%d" %(name, len(self.proc_list))
                self.proc_list.append(name)
                self.set_global(name, self.proc)
        '''

    def parse_file(self, fname):
        self.line_number = 0
        skipping_binary_data = False
        num = 0x1000
        if num:
            self.__binary_data_size += num

            self.__dummy_enum += 1
            labell = "dummy" + str(self.__dummy_enum)

            self.c_data.append("{0}, // padding\n")
            self.h_data.append(" db " + labell + "[" + str(num) + "]; // protective\n")
        self.parse_file_lines(fname, skipping_binary_data)
        num = (0x10 - (self.__binary_data_size & 0xf)) & 0xf
        if num:
            l = num * ['0']
            self.__binary_data_size += num

            self.__dummy_enum += 1
            labell = "dummy" + str(self.__dummy_enum)

            self.c_data.append("{" + ",".join(l) + "}, // padding\n")
            self.h_data.append(" db " + labell + "[" + str(num) + "]; // padding\n")
        return self

    def parse_file_lines(self, file_name, skipping_binary_data):
        content = read_asm_file(file_name)
        self.parse_args_new_data(content, file_name=file_name)

    def parse_include_file_lines(self, file_name):
        content = read_asm_file(file_name)
        return self.parse_file_inside(content, file_name=file_name)

    def tokenstostring(self, l):  # TODO remove
        if isinstance(l, str):
            return l
        elif isinstance(l, list):
            return " ".join([self.tokenstostring(i) for i in l])
        elif isinstance(l, Token):
            return l.value

    def action_assign(self, name, value):
        name = name.value
        value = Token.remove_tokens(value,'expr')
        #value = self.tokenstostring(value)
        #value = self.get_equ_value(value)
        has_global = False
        if self.has_global(name):
            has_global = True
            name = self.get_global(name).original_name
        o = self.proc.add_assignment(name, value, line_number=self.line_number)
        if not has_global:
            self.set_global(name, o)
        self.proc.stmts.append(o)
        return o

    def action_equ(self, name, value):
        name = name.value
        value = Token.remove_tokens(value,'expr')
        #value = self.tokenstostring(value)
        #vv = self.get_equ_value(value)
        proc = self.get_global("mainproc")
        o = proc.add_equ_(name, value, line_number=self.line_number)
        self.set_global(name, o)
        proc.stmts.insert(0, o)
        return o

    def action_segment(self, name):
        name = name.lower()
        self.__segment = name
        self.create_segment(name)

    def action_proc(self, name, type):
        logging.info("procedure name %s" % name.value)
        name = name.value.lower()
        far = ''
        for i in type:
            if i and i.lower() == 'far':
                far = True
        '''
                                        name = cmd0l
                                        self.proc = proc(name)
                                        logging.debug "procedure %s, #%d" %(name, len(self.proc_list))
                                        self.proc_list.append(name)
                                        self.set_global(name, self.proc)
        '''

        self.action_label(name, far=far, isproc=True)

    def action_simplesegment(self, type, name):
        if name is None:
            name = ""
        else:
            type = type + "_"
        type = type[1:] + name
        self.action_segment(type)

    def action_end(self, line):
        cmd = line.split()
        if len(cmd) >= 2:
            self.entry_point = cmd[1].lower()

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

    def action_endseg(self):
        logging.debug("segment %s ends" % self.__segment)
        self.__segment = "default_seg"

    def action_include(self, name):
        logging.info("including %s" % name)
        self.parse_file(name)

    def action_endp(self):
        self.proc = self.get_global('mainproc')

    def action_endif(self):
        self.pop_if()

    def action_else(self):
        self.push_else()

    def action_if(self, line):
        cmd = line.split()
        self.push_if(cmd[1])

    def action_code(self, line):
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
        del self.__globals['default_seg']
        return result

    def test_size(self, line):
        try:
            result = self.parse_args_new_data_('''.model tiny
        default_seg segment
        mov ax, ''' + line + '''
        default_seg ends
            end start
            ''').asminstruction.src
        except Exception as e:
            print(e)
            logging.error("Error2")
            result = [str(e)]
        del self.__globals['default_seg']
        return result

    def action_data(self, line):
        try:
            result = self.parse_args_new_data_('''.model tiny
    default_seg segment
    ''' + line + '''
    default_seg ends
    end startd
    ''')
        except Exception as e:
            print(str(e))
            logging.error("Error3")
            result = [str(e)]
        del self.__globals['default_seg']
        return result

    def parse_arg(self, line):
        try:
            result = self.parse_args_new_data_('''.model tiny
        default_seg segment
        mov ax, ''' + line + '''
        default_seg ends
        end start
        ''').asminstruction.src
        except Exception as e:
            print(e)
            logging.error("Error4")
            result = [str(e)]
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
            result = parser.parse('''.model tiny
            some_seg segment
            ''' + line + '''
            some_seg ends
            end
            ''', file_name=file_name, extra=self)  # context = self.__pgcontext)
            del self.__globals['some_seg']

        return result

    def datadir_action(self, name, type, args, size):
        s = size
        binary_width = calculate_type_size(type)
        offset = self.__cur_seg_offset
        logging.debug("data value %s offset %d" % (str(args), offset))
        self.__binary_data_size += s
        self.__cur_seg_offset += s
        c, h, elements = self.convert_data_to_c(name, binary_width,
                                                args)
        self.c_data += c
        self.h_data += h
        logging.debug("~size %d elements %d" % (binary_width, elements))
        if name:
            self.set_global(name.lower(), op.var(binary_width, offset, name=name,
                                                 segment=self.__segment, elements=elements))
        # logging.debug("~~        self.assertEqual(parser_instance.parse_data_line_whole(line='"+str(line)+"'),"+str(("".join(c), "".join(h), offset2 - offset))+")")
        return c, h, s

    def get_equ_value(self, v):
        logging.debug("%s" % v)
        vv = self.replace_dollar_w_segoffst(v)
        # ? vv = " ".join(self.parse_args(vv))
        vv = vv.strip()
        logging.debug("%s" % vv)
        m = re.match(r'\bbyte\s+(?:ptr)?\s*(.*)', vv)
        if m is not None:
            vv = m.group(1).strip()
        m = re.match(r'\bdword\s+(?:ptr)?\s*(.*)', vv)
        if m is not None:
            vv = m.group(1).strip()
        m = re.match(r'\bqword\s+(?:ptr)?\s*(.*)', vv)
        if m is not None:
            vv = m.group(1).strip()
        m = re.match(r'\btword\s+(?:ptr)?\s*(.*)', vv)
        if m is not None:
            vv = m.group(1).strip()
        m = re.match(r'\bword\s+(?:ptr)?\s*(.*)', vv)
        if m is not None:
            vv = m.group(1).strip()
        #vv = cpp.convert_number_to_c(vv)
        return vv

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
        # logging.debug self.c_data

    def parse_args_new_data_(self, text):
        # self.__pgcontext = PGContext(extra = self)
        self.__binary_data_size = 0
        self.__dummy_enum = 0  # one dummy number is used for "default_seg" creation
        return self.parse_file_insideseg(text)

    def parse_file_insideseg(self, text):
        return self.parse_args_new_data(text)[0][1][1][0].insegmentdir

    def parse_file_inside(self, text, file_name=None):
        return self.parse_include(text, file_name)

    def parse_args_new_data(self, text, file_name=None):
        logging.debug("parsing: [%s]" % text)

        result = self.__lex.parser.parse(text, file_name=file_name, extra=self)  # context = self.__pgcontext)
        # result = self.__lex.parser.call_actions(tree)
        logging.debug(str(result))
        return result

    @staticmethod
    def mangle_label(name):
        name = name.lower()
        return name.replace('@', "arb")

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

    @staticmethod
    def typetosize(value):
        if not isinstance(value, str):
            logging.error("Type is not a string TODO "+str(value)) # TODO add structures
            return 0
        value = value.lower()
        #DB | DW | DD | DF | DQ | DT | BYTE | SBYTE | WORD | SWORD | DWORD | SDWORD | FWORD | QWORD | TBYTE | REAL4 | REAL8 | REAL10
        try:
            size = {'db': 1, 'byte': 1, 'sbyte': 1,
                    'dw': 2, 'word': 2, 'sword': 2, 'small': 2,
                    'dd': 4, 'dword': 4, 'sdword': 4, 'large': 4, 'real4': 4,
                    'df': 6, 'fword': 6,
                    'dq': 8, 'qword': 8, 'real8': 8,
                    'dt': 10, 'tbyte': 10, 'real10': 10}[value]
        except KeyError:
            logging.debug("Cannot find size for %s" % value)
            size = 0
        return size
