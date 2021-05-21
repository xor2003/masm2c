from __future__ import print_function

import logging
import os
import re
import sys
# from builtins import chr
# from builtins import hex
from builtins import object
from builtins import range
from builtins import str
from copy import copy, deepcopy
import traceback

import parglare
from parglare import Grammar, Parser as PGParser

from masm2c import cpp
from masm2c.cpp import Cpp
from masm2c.op import Segment, Struct, DataType
from masm2c.proc import Proc
from masm2c import proc
from masm2c import op
from masm2c.Token import Token
from masm2c.Macro import Macro

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


macroses = dict()
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


def integertok(context, nodes):
    return Token('INTEGER', cpp.convert_number_to_c(nodes, context.extra.radix))


def commentkw(head, s, pos):
    # multiline comment
    mtch = commentid.match(s[pos:])
    if mtch:
        return mtch.group(0)
    else:
        return None


def macroname(context, s, pos):
    # macro usage identifier
    mtch = macronamere.match(s[pos:])
    if mtch:
        result = mtch.group().lower()
        # logging.debug ("matched ~^~" + result+"~^~")
        if result in macroses.keys():
            logging.debug(" ~^~" + result + "~^~ in macronames")
            return result
        else:
            return None
    else:
        return None


def macrodirhead(context, nodes, name, parms):
    # macro definition header
    param_names = []
    if parms:
        param_names = [i.lower() for i in Token.find_tokens(parms, 'LABEL')]
    context.extra.current_macro = Macro(name.value.lower(), param_names)
    context.extra.macro_name.append(name.value.lower())
    logging.debug("macroname added ~~" + name.value + "~~")
    return nodes


def repeatbegin(context, nodes, value):
    # start of repeat macro
    context.extra.current_macro = Macro("", [], value)
    context.extra.macro_name.append('')  # TODO
    logging.debug("repeatbegin")
    return nodes


def endm(context, nodes):
    # macro definition end
    name = context.extra.macro_name.pop()
    logging.debug("endm " + name)
    macroses[name] = context.extra.current_macro
    context.extra.current_macro = None
    return nodes


class Getmacroargval:

    def __init__(self, params, args):
        self.argvaluedict = dict(zip(params, args))

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
    mtch = macronamere.match(s[pos:])
    if mtch:
        result = mtch.group().lower()
        # logging.debug ("matched ~^~" + result+"~^~")
        if result in context.extra.structures.keys():
            logging.debug(" ~^~" + result + "~^~ in structures")
            return result
        else:
            return None
    else:
        return None


def structdirhdr(context, nodes, name, type):
    # structure definition header
    context.extra.current_struct = Struct(name.value.lower(), type)
    context.extra.struct_name.append(name.value.lower())
    logging.debug("structname added ~~" + name.value + "~~")
    return nodes


def remove_str(text):
    if isinstance(text, str):
        # if re.match(r'\d+|\?', text):
        return text
        # else:
        #    return None
    elif isinstance(text, list):
        found = True
        while found:
            found = False
            while len(text) == 1 and isinstance(text[0], list):
                found = True
                text = text[0]
            if len(text) >= 3 and text[0] in ['<', '{'] and text[-1] in ['>', '}']:
                found = True
                text = text[1:-1]
            if len(text) and isinstance(text[-1], str) and re.match(r'\n+\s*', text[-1]):
                found = True
                text = text[:-1]

        l = list()
        for i in text:
            r = remove_str(i)
            if r:
                l += [r]
        return l
    else:
        return text


def structinstdir(context, nodes, label, type, values):
    logging.debug(f"structinstdir {label} {type} {values}")
    # args = remove_str(Token.remove_tokens(remove_str(values), 'expr'))
    args = values[0].value
    # args = Token.remove_tokens(remove_str(values), 'expr')
    if args == None:
        args = []
    # args = Token.remove(args, 'INTEGER')
    context.extra.add_structinstance(label.value, type, args)
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


def segmentdir(context, nodes, name):
    logging.debug("segmentdir " + str(nodes) + " ~~")
    context.extra.action_segment(name.value)
    return nodes


def endsdir(context, nodes, name):
    logging.debug("ends " + str(nodes) + " ~~")
    context.extra.action_ends()
    return nodes


def procdir(context, nodes, name, type):
    logging.debug("procdir " + str(nodes) + " ~~")
    context.extra.action_proc(name, type, line_number=get_line_number(context))
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


def labeldef(context, nodes, name):
    logging.debug("labeldef " + str(nodes) + " ~~")
    return context.extra.action_label(name.value)


def instrprefix(context, nodes):
    logging.debug("instrprefix " + str(nodes) + " ~~")
    instruction = nodes[0]
    # o = context.extra.proc.create_instruction_object(instruction)
    # o.line = get_raw(context)
    # o.line_number = get_line_number(context)
    # context.extra.proc.stmts.append(o)
    context.extra.action_instruction(instruction, [], raw=get_raw(context), line_number=get_line_number(context))
    return []


def asminstruction(context, nodes, instruction, args):
    logging.debug("instruction " + str(nodes) + " ~~")
    # args = build_ast(args)
    if not instruction:
        return nodes
    if args is None:
        args = []
    return context.extra.action_instruction(instruction, args, raw=get_raw(context),
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
    logging.debug("offset /~" + str(nodes) + "~\\")
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
    context.extra.radix = value
    return nodes


def externdef(context, nodes, extrnname, type):
    logging.debug('externdef %s' % str(nodes))
    context.extra.add_extern(extrnname.value, type)
    return nodes

def maked(context, nodes):
    #return Token(nodes[0].upper(), nodes[1].value)
    # TODO dirty workaround for now
    if nodes[0].lower() == 'size':
        return [f'sizeof({nodes[1].value.lower()})']
    else:
        return nodes

actions = {
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


class Parser:
    def __init__(self, skip_binary_data=[]):
        self.separate_proc = True
        # self.__label_to_skip = skip_binary_data

        self.__globals = {}
        self.__offsets = {}
        self.__offset_id = 0x1111
        self.__stack = []

        self.entry_point = "mainproc_begin"
        self.main_file = False

        self.proc_list = []
        self.proc_stack = []

        # self.proc = None
        nname = "mainproc"
        self.proc = Proc(nname)
        self.proc_list.append(nname)
        self.proc_stack.append(self.proc)
        self.set_global(nname, self.proc)

        self.__binary_data_size = 0
        self.c_data = []
        self.h_data = []
        self.__cur_seg_offset = 0
        self.__c_dummy_label = 0
        self.__c_dummy_jump_label = 0

        self.segments = dict()
        self.__segment_name = "default_seg"
        self.segment = Segment(self.__segment_name, 0)
        self.segments[self.__segment_name] = self.segment

        self.__lex = ParglareParser()
        self.used = False
        # self.__pgcontext = PGContext(extra = self)
        self.radix = 10

        self.current_macro = None
        self.macro_name = []

        self.current_struct = None
        self.struct_name = []
        self.structures = dict()
        self.externals_vars = set()
        self.externals_procs = set()

        self.current_file = ''
        self.files = []

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

        logging.debug("set_global(name='%s',value=%s)" % (name, dump_object(value)))
        if name in self.__globals:
            raise Exception("global %s was already defined", name)
        value.used = False
        self.__globals[name] = value

    def reset_global(self, name, value):
        if len(name) == 0:
            raise Exception("empty name is not allowed")
        value.original_name = name
        name = name.lower()
        logging.debug("reset global %s -> %s" % (name, value))
        self.__globals[name] = value

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
        # assert self.__globals[name].used
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
        elif re.match(r'^[01]+[Bb]$', v):
            v = int(v[:-1], 2)
        # v = int(cpp.convert_number_to_c(v))

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

    def get_global_value(self, v):
        logging.debug("get_global_value(%s)" % v)
        v = self.mangle_label(v)
        g = self.get_global(v)
        logging.debug(g)
        if isinstance(g, op._equ) or isinstance(g, op._assignment):
            v = g.original_name
        elif isinstance(g, op.var):
            v = "offset(%s,%s)" % (g.segment, g.name)
        elif isinstance(g, (op.label, proc.Proc)):
            v = "k%s" % (g.name.lower())
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
                cur_data_type = DataType.ARRAY_NUMBER  # array of numbers
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
                        v = self.get_global_value(v)
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
                    v = self.get_global_value(v)
                except KeyError:
                    logging.warning("unknown address %s" % v)
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

    def action_label(self, name, far=False, isproc=False):
        logging.debug("~name: %s" % name)
        if name == '@@':
            name = self.get_dummy_jumplabel()
        name = self.mangle_label(name)
        if True:  # not (name in self.__label_to_skip):
            logging.debug("offset %s -> %s" % (name, "&m." + name.lower() + " - &m." + self.__segment_name))
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
                self.set_offset(name,
                                ("&m." + name.lower() + " - &m." + self.__segment_name, self.proc, self.__offset_id))
                self.set_global(name, op.label(name, self.proc, line_number=self.__offset_id, far=far))
                self.__offset_id += 1
            else:
                logging.error("!!! Label %s is outside the procedure" % name)
        else:
            logging.info("skipping binary data for %s" % (name,))

    def create_segment(self, name):
        self.align()

        offset = self.__binary_data_size // 16
        logging.debug("segment %s %x" % (name, offset))

        binary_width = 0
        # num = 0
        # elf.c_data.append("{}, // segment " + name + "\n")
        # self.h_data.append(" db " + name + "[" + str(num) + "]; // segment " + name + "\n")

        self.segment = Segment(name, offset)
        self.segments[name] = self.segment

        self.segment.append(op.Data(name, 'db', DataType.ARRAY_NUMBER, [], 0, 0))
        # c, h = self.produce_c_data(name, 'db', 4, [], 0)
        # self.c_data += c
        # self.h_data += h

        # self.__binary_data_size += num
        self.__cur_seg_offset = 0

        self.set_global(name, op.var(binary_width, offset, name, issegment=True))

    def align(self, align_bound=0x10):
        num = (align_bound - (self.__binary_data_size & (align_bound - 1))) if (
                self.__binary_data_size & (align_bound - 1)) else 0
        if num:
            self.__binary_data_size += num

            label = self.get_dummy_label()

            self.segment.append(op.Data(label, 'db', DataType.ARRAY_NUMBER, num * [0], num, num))

    def get_dummy_label(self):
        self.__c_dummy_label += 1
        label = "dummy" + str(self.__c_dummy_label)
        return label

    def get_dummy_jumplabel(self):
        self.__c_dummy_jump_label += 1
        label = "dummylabel" + str(self.__c_dummy_jump_label)
        return label

    def parse_file(self, fname):
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
        self.current_file = file_name
        content = read_asm_file(file_name)
        self.parse_args_new_data(content, file_name=file_name)

    def parse_include_file_lines(self, file_name):
        self.files.append(self.current_file)
        self.current_file = file_name
        content = read_asm_file(file_name)
        result = self.parse_file_inside(content, file_name=file_name)
        self.current_file = self.files.pop()
        return result

    def action_assign(self, label, value, raw='', line_number=0):
        label = self.mangle_label(label)

        # if self.has_global(label):
        #    label = self.get_global(label).original_name
        o = self.proc.create_assignment_op(label, value, line_number=line_number)
        o.filename = self.current_file
        o.line = raw.rstrip()
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
        value = Token.remove_tokens(value, 'expr')
        size = Cpp(self).get_size(value)
        ptrdir = Token.find_tokens(value, 'ptrdir')
        if ptrdir:
            type = ptrdir[0]
            if isinstance(type, Token):
                type = type.value
            type = type.lower()
            value = Token.find_and_replace_tokens(value, 'ptrdir', self.return_empty)
        o = Proc.create_equ_op(label, value, line_number=line_number)
        o.filename = self.current_file
        o.line = raw.rstrip()
        o.size = size
        if ptrdir:
            o.original_type = type
        self.set_global(label, o)
        proc = self.get_global("mainproc")
        proc.stmts.append(o)
        return o

    def action_segment(self, name):
        name = name.lower()
        self.__segment_name = name
        self.create_segment(name)

    def action_proc(self, name, type, line_number=0):
        logging.info("procedure name %s" % name.value)
        name = self.mangle_label(name.value)
        far = False
        for i in type:
            if i and i.lower() == 'far':
                far = True

        if self.separate_proc:
            self.proc = Proc(name, far=far, line_number=line_number)
            logging.debug("procedure %s, #%d" % (name, len(self.proc_list)))
            self.proc_list.append(name)
            self.proc_stack.append(self.proc)
            self.set_global(name, self.proc)
        else:
            self.action_label(name, far=far, isproc=True)

    def action_simplesegment(self, type, name):
        if name is None:
            name = ""
        else:
            type = type + "_"
        type = type[1:] + name
        self.action_segment(type)

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
        self.proc_stack.pop()
        if self.proc_stack:
            self.proc = self.proc_stack[-1]
        else:
            self.proc = None

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
            ''').asminstruction.args[1]
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
        ''').asminstruction.args[1]
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

    def datadir_action(self, label, type, args, raw='', line_number=0):
        isstruct = len(self.struct_name) != 0

        label = self.mangle_label(label)
        binary_width = self.typetosize(type)
        size = calculate_data_size_new(binary_width, args)

        offset = self.__cur_seg_offset
        logging.debug("args %s offset %d" % (str(args), offset))

        self.__binary_data_size += size
        self.__cur_seg_offset += size
        logging.debug("convert_data %s %d %s" % (label, binary_width, args))
        # original_label = label

        elements, is_string, array = self.process_data_tokens(args, binary_width)
        data_internal_type = self.identify_data_internal_type(array, elements, is_string)

        logging.debug("~size %d elements %d" % (binary_width, elements))
        if label:
            self.set_global(label, op.var(binary_width, offset, name=label,
                                          segment=self.__segment_name, elements=elements, original_type=type,
                                          filename=self.current_file, raw=raw, line_number=line_number))

        if len(label) == 0:
            label = self.get_dummy_label()
        data = op.Data(label, type, data_internal_type, array, elements, size, filename=self.current_file, raw=raw,
                       line_number=line_number)
        if isstruct:
            self.current_struct.append(data)
        else:
            self.segment.append(data)

        # c, h, size = cpp.Cpp.produce_c_data(data) # TO REMOVE
        # self.c_data += c
        # self.h_data += h

        # logging.debug("~~        self.assertEqual(parser_instance.parse_data_line_whole(line='"+str(line)+"'),"+str(("".join(c), "".join(h), offset2 - offset))+")")
        return data  # c, h, size

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
        self.__c_dummy_label = 0  # one dummy number is used for "default_seg" creation
        self.__c_dummy_jump_label = 0
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

    def typetosize(self, value):
        if isinstance(value, Token) and value.value.lower() in self.structures.keys():
            return self.structures[value.value.lower()].getsize()
        elif not isinstance(value, str):
            logging.error("Type is not a string TODO " + str(value))
            return 0
        value = value.lower()
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

    def add_structinstance(self, label, type, args):
        s = self.structures[type]
        # cpp = Cpp(self)
        # args = Token.find_and_replace_tokens(args, 'structinstance', cpp.expand)
        args = Token.remove_tokens(args, 'structinstance')
        # args = [cpp.expand(i) for i in args]
        # elements, is_string, array = self.process_data_tokens(args, binary_width)
        d = op.Data(label, type, DataType.OBJECT, args, 1, s.getsize())
        members = [deepcopy(i) for i in s.getdata().values()]
        d.setmembers(members)
        args = self.convert_members(d, args)
        d.setvalue(args)

        isstruct = len(self.struct_name) != 0
        if isstruct:
            self.current_struct.append(d)
        else:
            self.segment.append(d)
            self.set_global(label, op.var(s.getsize(), self.__cur_seg_offset, label, segment=self.__segment_name, \
                                          original_type=type))
            self.__cur_seg_offset += s.getsize()

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
            if self.separate_proc:
                self.externals_procs.add(label)
                proc = Proc(label, extern=True)
                logging.debug("procedure %s, extern" % label)
                self.reset_global(label, proc)
            else:
                self.reset_global(label, op.label(label, self.proc))

    def add_call_to_entrypoint(self):
        if self.separate_proc:
            proc = self.get_global('mainproc')
            o = proc.create_instruction_object('call', [self.entry_point])
            o.line = ''
            o.line_number = 0
            proc.stmts.append(o)

    def action_instruction(self, instruction, args, raw='', line_number=0):
        if instruction[0].lower() == 'j' and len(args) == 1 and isinstance(args[0], Token) and \
                isinstance(args[0].value, Token) and args[0].value.type == 'LABEL':
            if args[0].value.value.lower() == '@f':
                args[0].value.value = "dummylabel" + str(self.__c_dummy_jump_label + 1)
            elif args[0].value.value.lower() == '@b':
                args[0].value.value = "dummylabel" + str(self.__c_dummy_jump_label)

        o = self.proc.create_instruction_object(instruction, args)
        o.filename = self.current_file
        o.line = raw
        o.line_number = line_number
        if self.current_macro == None:
            self.proc.stmts.append(o)
        else:
            self.current_macro.instructions.append(o)
        return o

    def action_ends(self):
        if len(self.struct_name):  # if it is not a structure then it is end of segment
            name = self.struct_name.pop()
            logging.debug("endstruct " + name)
            self.structures[name] = self.current_struct
            self.set_global(name, self.current_struct)
            self.current_struct = None
        else:
            self.action_endseg()

    def action_end(self, label):
        if label:
            self.main_file = True
            self.entry_point = Token.find_tokens(label, 'LABEL')[0].lower()
            self.add_call_to_entrypoint()
