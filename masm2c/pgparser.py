import logging
import os
import re
from collections import OrderedDict
from copy import deepcopy, copy

from parglare import Grammar
from parglare import Parser as PGParser

from . import op
from .Macro import Macro
from .Token import Token

from . import cpp as cpp_module

macroses = OrderedDict()
macronamere = re.compile(r'([A-Za-z_@$?][A-Za-z0-9_@$?]*)')
commentid = re.compile(r'COMMENT\s+([^ ]).*?\1[^\r\n]*', flags=re.DOTALL)


def get_line_number(context):
    """
    It returns the line number of the current position in the input string

    :param context: the context object that is passed to the action function
    :return: The line number of the current position in the input string.
    """
    return context.input_str[: context.start_position].count('\n') + 1


def get_raw(context):
    """
    It returns the raw text that was provided to parser

    :param context:
    :return: The raw string from the input string.
    """
    return context.input_str[context.start_position: context.end_position].strip()


def get_raw_line(context):
    """
    It returns the raw line of text that the cursor is currently on

    :param context: The context object that contains the current position in the input string, the start and end positions
    of the current match, and the input string itself
    :return: The line of text from the input string.
    """
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
    return Token('INTEGER', cpp_module.convert_asm_number_into_c(nodes, context.extra.radix))


def commentkw(head, s, pos):
    # multiline comment
    if s[pos:pos + 7] == 'COMMENT':
        if mtch := commentid.match(s[pos:]):
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
    context.extra.current_struct = op.Struct(name.value.lower(), type)
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
    fullpath = os.path.join(os.path.dirname(os.path.realpath(context.extra._current_file)), name)
    result = context.extra.parse_include_file_lines(fullpath)
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
    from .parser import Parser
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
            debug = False
            cls._inst.or_parser = PGParser(cls._inst.or_grammar, debug=debug, actions=actions, build_tree = False)
            ##cls._inst.or_parser = GLRParser(cls._inst.or_grammar, debug=debug, actions=actions, prefer_shifts=True)

            # , build_tree = True, call_actions_during_tree_build = True)

            cls._inst.grammar = cls._inst.or_grammar
            cls._inst.parser = copy(cls._inst.or_parser)
            cls._inst.parser.grammar = cls._inst.grammar

        return cls._inst
