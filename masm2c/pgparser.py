import logging
import os
import re
from collections import OrderedDict
from copy import deepcopy, copy

from lark import Transformer, Lark

from . import op
from .Macro import Macro
from .Token import Token

macroses = OrderedDict()
macronamere = re.compile(r'([A-Za-z_@$?][A-Za-z0-9_@$?]*)')
commentid = re.compile(r'COMMENT\s+([^ ]).*?\1[^\r\n]*', flags=re.DOTALL)


class Tr(Transformer):

    def __init__(self, context):
        self.context = context
        
    def get_line_number(self, context):
        """
        It returns the line number of the current position in the input string
    
        :param context: the context object that is passed to the action function
        :return: The line number of the current position in the input string.
        """
        return context.input_str[: context.start_position].count('\n') + 1
    
    
    def get_raw(self, context):
        """
        It returns the raw text that was provided to parser
    
        :param context:
        :return: The raw string from the input string.
        """
        return context.input_str[context.start_position: context.end_position].strip()
    
    
    def get_raw_line(self, context):
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
    def build_ast(self, nodes, type=''):
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
    
    

    def expr(self, nodes):
        return nodes
    
    
    def dupdir(self, nodes, times, values):
        return nodes #Token('dupdir', [times, values])
    
    
    def segoverride(self, nodes):
        # global cur_segment
        if isinstance(nodes[0], list):
            # cur_segment = nodes[0][-1]
            return nodes[0][:-1] + [Token('segoverride', nodes[0][-1]), nodes[2]]
        # cur_segment = nodes[0] #!
        return [Token('segoverride', nodes[0]), nodes[2]]
    
    
    def ptrdir(self, nodes):
        if len(nodes) == 3:
            return [Token('ptrdir', nodes[0]), nodes[2]]
        else:
            return [Token('ptrdir', nodes[0]), nodes[1]]
    
    
    def integertok(self, nodes):
        from masm2c.cpp import Cpp
        return nodes #Token('INTEGER', Cpp(self.context.convert_asm_number_into_c(nodes, self.context.radix))  # TODO remove this
    
    
    def commentkw(self, head, s, pos):
        # multiline comment
        if s[pos:pos + 7] == 'COMMENT':
            if mtch := commentid.match(s[pos:]):
                return mtch.group(0)
        return None
    
    
    def macroname(self, s, pos):
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
    
    
    def macrodirhead(self, nodes, name, parms):
        # macro definition header
        param_names = []
        if parms:
            param_names = [i.lower() for i in Token.find_tokens(parms, 'LABEL')]
        self.context.current_macro = Macro(name.value.lower(), param_names)
        self.context.macro_names_stack.add(name.value.lower())
        logging.debug("macroname added ~~%s~~", name.value)
        return nodes
    
    
    def repeatbegin(self, nodes, value):
        # start of repeat macro
        self.context.current_macro = Macro("", [], value)
        self.context.macro_names_stack.add('')  # TODO
        logging.debug("repeatbegin")
        return nodes
    
    
    def endm(self, nodes):
        # macro definition end
        name = self.context.macro_names_stack.pop()
        logging.debug("endm %s", name)
        macroses[name] = self.context.current_macro
        self.context.current_macro = None
        return nodes
    
    
    class Getmacroargval:
    
        def __init__(self, params, args):
            self.argvaluedict = OrderedDict(zip(params, args))
    
        def __call__(self, token):
            return self.argvaluedict[token.value]
    
    
    def macrocall(self, nodes, name, args):
        # macro usage
        logging.debug("macrocall " + name + "~~")
        macros = macroses[name]
        instructions = deepcopy(macros.instructions)
        param_assigner = self.Getmacroargval(macros.getparameters(), args)
        for instruction in instructions:
            instruction.args = Token.find_and_replace_tokens(instruction.args, 'LABEL', param_assigner)
        self.context.proc.stmts += instructions
        return nodes
    
    
    def structname(self, s, pos):
        if self.context.structures:
            mtch = macronamere.match(s[pos:])
            if mtch:
                result = mtch.group().lower()
                # logging.debug ("matched ~^~" + result+"~^~")
                if result in self.context.structures.keys():
                    logging.debug(" ~^~" + result + "~^~ in structures")
                    return result
        return None
    
    
    def structdirhdr(self, nodes, name, type):
        # structure definition header
        self.context.current_struct = op.Struct(name.value.lower(), type)
        self.context.struct_names_stack.add(name.value.lower())
        logging.debug("structname added ~~" + name.value + "~~")
        return nodes
    
    
    def structinstdir(self, nodes, label, type, values):
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
        self.context.add_structinstance(name, type.lower(), args, raw=self.get_raw(self.context))
        return nodes
    
    
    def datadir(self, nodes, label, type, values):
        logging.debug("datadir " + str(nodes) + " ~~")
    
        if label:
            label = label.value
        else:
            label = ""
    
        return self.context.datadir_action(label, type.lower(), values, raw=self.get_raw(self.context),
                                            line_number=self.get_line_number(self.context))
    
    
    def includedir(self, nodes, name):
        # context.parser.input_str = context.input_str[:context.end_position] + '\n' + read_asm_file(name) \
        # + '\n' + context.input_str[context.end_position:]
        fullpath = os.path.join(os.path.dirname(os.path.realpath(self.context._current_file)), name)
        result = self.context.parse_include_file_lines(fullpath)
        return result
    
    
    def segdir(self, nodes, type):
        logging.debug("segdir " + str(nodes) + " ~~")
        self.context.action_simplesegment(type, '')  # TODO
        return nodes
    
    
    def segmentdir(self, nodes, name, options):
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
    
        self.context.create_segment(name.value, options=opts, segclass=segclass, raw=self.get_raw(self.context))
        return nodes
    
    
    def modeldir(self, nodes, model):
        logging.debug("modeldir " + str(nodes) + " ~~")
        return nodes
    
    
    def endsdir(self, nodes, name):
        logging.debug("ends " + str(nodes) + " ~~")
        self.context.action_ends()
        return nodes
    
    
    def procdir(self, nodes, name, type):
        logging.debug("procdir " + str(nodes) + " ~~")
        self.context.action_proc(name, type, line_number=self.get_line_number(self.context), raw=self.get_raw_line(self.context))
        return nodes
    
    
    def endpdir(self, nodes, name):
        logging.debug("endp " + str(name) + " ~~")
        self.context.action_endp()
        return nodes
    
    
    def equdir(self, nodes, name, value):
        logging.debug("equdir " + str(nodes) + " ~~")
        return self.context.action_equ(name.value, value, raw=self.get_raw(self.context), line_number=self.get_line_number(self.context))
    
    
    def assdir(self, nodes, name, value):
        logging.debug("assdir " + str(nodes) + " ~~")
        return self.context.action_assign(name.value, value, raw=self.get_raw(self.context), line_number=self.get_line_number(self.context))
    
    
    def labeldef(self, nodes, name, colon):
        logging.debug("labeldef " + str(nodes) + " ~~")
        return self.context.action_label(name.value, isproc=False, raw=self.get_raw_line(self.context),
                                          line_number=self.get_line_number(self.context),
                                          globl=(colon == '::'))
    
    
    def instrprefix(self, nodes):
        logging.debug("instrprefix " + str(nodes) + " ~~")
        instruction = nodes[0]
        self.context.action_instruction(instruction, [], raw=self.get_raw_line(self.context), line_number=self.get_line_number(self.context))
        return []
    
    
    def asminstruction(self, nodes, instruction, args):
        logging.debug("asminstruction " + str(nodes) + " ~~")
        # args = build_ast(args)
        if not instruction:
            return nodes
        if args is None:
            args = []
        return self.context.action_instruction(instruction, args, raw=self.get_raw_line(self.context),
                                                line_number=self.get_line_number(self.context))
    
    
    def enddir(self, nodes, label):
        logging.debug("end " + str(nodes) + " ~~")
        self.context.action_end(label)
        return nodes
    
    
    def notdir(self, nodes):
        nodes[0] = '~'  # should be in Cpp module
        return nodes
    
    
    def ordir(self, nodes):
        nodes[1] = '|'
        return nodes
    
    
    def xordir(self, nodes):
        nodes[1] = '^'
        return nodes
    
    
    def anddir(self, nodes):
        nodes[1] = ' & '
        return nodes
    
    
    def register(self, nodes):
        return nodes #Token('register', nodes[0].lower())
    
    
    def segmentregister(self, nodes):
        return nodes #Token('segmentregister', nodes[0].lower())
    
    
    def sqexpr(self, nodes):
        logging.debug("/~" + str(nodes) + "~\\")
        res = nodes[1]
        return nodes #Token('sqexpr', res)
    
    
    def offsetdir(self, nodes):
        logging.debug("offset /~" + str(nodes) + "~\\")
        return nodes #Token('offsetdir', nodes[1])
    
    
    def segmdir(self, nodes):
        logging.debug("segmdir /~" + str(nodes) + "~\\")
        # global indirection
        # indirection = -1
        return nodes #Token('segmdir', nodes[1])
    
    
    def labeltok(self, nodes):
        return nodes #Token('LABEL', nodes)
    
    
    def STRING(self, nodes):
        return nodes #Token('STRING', nodes)
    
    
    def structinstance(self, nodes, values):
        return nodes #Token('structinstance', values)
    
    
    def memberdir(self, nodes, variable, field):
        result = Token('memberdir', [variable, field])
        logging.debug(result)
        return result
    
    
    def radixdir(self, nodes, value):
        self.context.radix = int(value.value.value)
        return nodes
    
    
    def externdef(self, nodes, extrnname, type):
        logging.debug('externdef %s', nodes)
        self.context.add_extern(extrnname.value, type)
        return nodes
    
    
    def maked(self, nodes):
        # return nodes #Token(nodes[0].upper(), nodes[1].value)
        # TODO dirty workaround for now
        if nodes[0].lower() == 'size':
            return [f'sizeof({nodes[1].value.lower()})']
        else:
            return nodes
    
    
    def offsetdirtype(self, nodes, directive, value):
        from .parser import Parser
        logging.debug(f'offsetdirtype {directive} {str(value)}')
        directive = directive.lower()
        value = value.value.value if value else 2
        if directive == 'align':
            self.context.align(Parser.parse_int(value))
        elif directive == 'even':
            self.context.align(2)
        elif directive == 'org':
            self.context.org(Parser.parse_int(value))
        return nodes

'''
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
'''

class LarkParser:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(LarkParser, cls).__new__(cls)
            logging.debug("Allocated LarkParser instance")

            file_name = os.path.dirname(os.path.realpath(__file__)) + "/_masm61.lark"
            debug = False
            with open(file_name, 'rt') as gr:
                cls._inst.or_parser = Lark(gr, parser='lalr', propagate_positions=True, debug=debug)

            cls._inst.parser = copy(cls._inst.or_parser)

        return cls._inst


OFFSETDIR = 'offsetdir'
LABEL = 'LABEL'
PTRDIR = 'ptrdir'
REGISTER = 'register'
SEGMENTREGISTER = 'segmentregister'
SEGOVERRIDE = 'segoverride'
SQEXPR = 'sqexpr'
INTEGER = 'INTEGER'
MEMBERDIR = 'memberdir'
