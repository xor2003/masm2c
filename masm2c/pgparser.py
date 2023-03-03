from ast import literal_eval
import logging
import os
import re
import sys
from collections import OrderedDict
from copy import deepcopy, copy
from typing import Iterator

from lark import Transformer, Lark, v_args, Discard, Tree, Visitor, lark

from . import op
from .Macro import Macro
from .Token import Token, Expression

from .enum import IndirectionType

macroses = OrderedDict()
macronamere = re.compile(r'([A-Za-z_@$?][A-Za-z0-9_@$?]*)')
commentid = re.compile(r'COMMENT\s+([^ ]).*?\1[^\r\n]*', flags=re.DOTALL)

class MatchTag:
    always_accept = "LABEL", "structinstdir", "STRUCTNAME"

    def __init__(self, context):
        self.context = context
        self.last_type = None
        self.last = None

    def process(self, stream: Iterator[lark.Token]) -> Iterator[lark.Token]:
        for t in stream:
            if self.last_type == 'LABEL' and t.type == "LABEL" and t.value.lower() in {'struc','struct','union'}:  # HACK workaround
                # print(1, self.last_type, self.last, t)
                t.type = "STRUCTHDR"
            if t.type == "LABEL" and t.value.lower() in ['ends']:  # HACK workaround
                print(self.last_type, self.last)
                t.type = "endsdir"

            #if t.type == "LABEL" and t.value == 'VECTOR':
            #    print(t)

            if self.last_type == 'LABEL' and t.type == "STRUCTHDR":
                self.context.structures[self.last.lower()] = True
                # print(1, self.last_type, self.last, t)

            # if t.type == "STRUCTHDR":
            #    print(2, t)
            #    print(self.last)
            if self.context.structures and self.last_type == 'LABEL' \
                    and t.type == "LABEL" and t.value.lower() in self.context.structures:
                # print(3, t)
                t.type = "STRUCTNAME"
            self.last_type = t.type
            self.last = t.value
            yield t

def get_line_number(meta):
    """
    It returns the line number of the current position in the input string

    :param context: the context object that is passed to the action function
    :return: The line number of the current position in the input string.
    """
    return meta.line


def get_raw(input_str, meta):
    """
    It returns the raw text that was provided to parser

    :param context:
    :return: The raw string from the input string.
    """
    return input_str[meta.start_pos: meta.end_pos].strip()


def get_raw_line(input_str, meta):
    """
    It returns the raw line of text that the cursor is currently on

    :return: The line of text from the input string.
    """
    try:
        line_strt_pos = input_str.rfind('\n', 0, meta.start_pos) + 1

        line_eol_pos = input_str.find('\n', meta.start_pos)
        if line_eol_pos == -1:
            line_eol_pos = len(input_str)
    except Exception as ex:
        print(ex)
    return input_str[line_strt_pos: line_eol_pos]


class CommonCollector(Transformer):

    def __init__(self, context, input_str=''):
        self.context = context
        self._expression = None
        self.input_str = input_str

'''
class EquCollector(CommonCollector):

    def __init__(self, context, input_str=''):
        super().__init__(context, input_str)


'''

class Asm2IR(CommonCollector):

    def __init__(self, context, input_str=''):
        super().__init__(context, input_str)
        #self.context = context
        #self.input_str = input_str
        self._radix = 10
        #self._expression = None
        self._element_type = None

        self._size = 0
        self._poptions = []

    def externdef(self, nodes):
        label, type = nodes
        type = type.children[0].children[0]
        logging.debug('externdef %s', nodes)
        self.context.add_extern(label, type)
        return nodes

    @v_args(meta=True)
    def equdir(self, meta, nodes):
        name, value = nodes[0], nodes[1]
        logging.debug("equdir %s ~~", nodes)

        return self.context.action_equ(name, value, raw=get_raw(self.input_str, meta),
                                       line_number=get_line_number(meta))

    @v_args(meta=True)
    def assdir(self, meta, nodes):
        name, value = nodes[0], nodes[1]
        logging.debug("assdir %s ~~", nodes)
        return self.context.action_assign(name, value, raw=get_raw(self.input_str, meta),
                                          line_number=get_line_number(meta))

    @v_args(meta=True)
    def labeldef(self, meta, children):
        logging.debug("labeldef %s ~~", children)
        name, colon = children  # TODO
        return self.context.action_label(name, isproc=False, raw=get_raw_line(self.input_str, meta),
                                         line_number=get_line_number(meta),
                                         globl=(colon == '::'))


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

    def expr(self, children):
        # self.expression = self.expression or Expression()
        # while isinstance(children, list) and len(children) == 1:
        #    children = children[0]
        self.expression.children = children  # [0]
        result:Expression = self._expression
        if not self.expression.segment_overriden and result.indirection == IndirectionType.POINTER and \
                result.registers.intersection({'bp', 'ebp', 'sp', 'esp'}):
            result.segment_register = 'ss'
        #if result.indirection == IndirectionType.POINTER:
        #    self.expression.original_type = self._element_type
        self._expression = None
        return result

    def initvalue(self, expr):
        return lark.Tree(data='exprlist', children=[self.expr(expr)])

    def dupdir(self, children):
        from masm2c.cpp import IR2Cpp
        from masm2c.parser import Parser
        repeat = copy(children[0])
        repeat.indirection = IndirectionType.VALUE
        repeat = "".join(IR2Cpp(self.context).visit(repeat))
        repeat = eval(repeat)
        value = children[1]
        #self.expression.element_number *= repeat
        result = lark.Tree(data='dupdir', children=value)
        result.repeat = repeat
        return result  # Token('dupdir', [times, values])

    def segoverride(self, nodes):
        seg = nodes[0]
        if isinstance(seg, list):
            seg = seg[0]
        #self.__work_segment = seg.lower()
        self.expression.indirection = IndirectionType.POINTER
        self.expression.element_size = 0
        self.expression.segment_overriden = True
        return nodes[1:]

    def distance(self, children):
        self.expression.mods.add(children[0].lower())
        #self.expression.indirection = IndirectionType.OFFSET  #
        self._size = self.context.typetosize(children[0])
        return str(children[0]).lower()

    def ptrdir(self, children):
        if self.expression.indirection == IndirectionType.VALUE:  # set above
            self.expression.indirection = IndirectionType.POINTER
        type = children[0].lower()
        #if self._size: # TODO why need another variable?
        self.expression.ptr_size = self.context.typetosize(type)
        if type not in {'far', 'near'}:
            self.expression.mods.add('size_changed')
        self._element_type = self.expression.original_type = type
        children = children[1:]
        self.expression.element_size = 0
        return children

    def ptrdir2(self, children):  # tasm?
        self.expression.indirection = IndirectionType.POINTER
        #self.__work_segment = children[1].lower()
        self.expression.segment_overriden = True
        self.expression.ptr_size = self.context.typetosize(children[0])
        self.expression.mods.add('size_changed')
        self._element_type = self.expression.original_type = children[0].lower()
        return children[3:]

    def datadecl(self, children):
        # self.expression = self.expression or Expression()
        self._size = self.context.typetosize(children[0])
        self._element_type = children[0].lower()
        return str(children[0]).lower()

    def ANYTHING(self, value):
        return self.INTEGER('0')

    def INTEGER(self, value):
        from .parser import parse_asm_number
        from .gen import guess_int_size

        radix, sign, value = parse_asm_number(value, self._radix)

        val = int(value, radix)
        if sign == '-':
            val *= -1
        self.expression.element_size_guess = guess_int_size(val)
        # self.expression.element_size = max(guess_int_size(val), self.expression.element_size)

        t = lark.Token(type='INTEGER', value=sign + value)
        t.start_pos, t.line, t.column = radix, sign, value
        return t  # Token('INTEGER', Cpp(self.context.convert_asm_number_into_c(nodes, self.context.radix))  # TODO remove this

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
        self.context.current_macro = Macro(name.children.lower(), param_names)
        self.context.macro_names_stack.add(name.children.lower())
        logging.debug("macroname added ~~%s~~", name.children)
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
            return self.argvaluedict[token.children]

    def macrocall(self, nodes, name, args):
        # macro usage
        logging.debug("macrocall " + name + "~~")
        macros = macroses[name]
        instructions = deepcopy(macros.instructions)
        param_assigner = self.Getmacroargval(macros.getparameters(), args)
        for instruction in instructions:
            instruction.children = Token.find_and_replace_tokens(instruction.children, 'LABEL', param_assigner)
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

    def structdirhdr(self, nodes):
        name, type = nodes
        # structure definition header
        self.context.current_struct = op.Struct(name.lower(), type.lower())
        self.context.struct_names_stack.append(name.lower())
        logging.debug("structname added ~~" + name + "~~")
        return nodes

    @v_args(meta=True)
    def structinstdir(self, meta, nodes):
        label, type, values = nodes
        logging.debug(f"structinstdir {label} {type} {values}")
        # args = remove_str(Token.remove_tokens(remove_str(values), 'expr'))
        args = values.children[0]
        # args = Token.remove_tokens(remove_str(values), 'expr')
        if args is None:
            args = []
        # args = Token.remove(args, 'INTEGER')
        if label:
            name = label.lower()
        else:
            name = ''
        self.context.add_structinstance(name, type.lower(), args, raw=get_raw(self.input_str, meta))
        return nodes

    def insegdir(self, children: list):
        self._expression = None
        self._element_type = None
        self._size = 0
        return children

    @v_args(meta=True)
    def datadir(self, meta, children: list):
        logging.debug("datadir %s ~~", children)
        if len(children)==1: # TODO why?
            children = children[0]
        if isinstance(children[0], lark.Token) and children[0].type == 'LABEL':
            label = self.context.mangle_label(children.pop(0))
        else:
            label = ''
        type = children.pop(0).lower()
        if isinstance(children[0], (lark.Token, lark.Tree)):  # Data
            values = lark.Tree(data='data', children=children[0].children)
            #type = self._element_type
        else:
            #type = children[0][1].lower()  # Structs
            values = children[0][2:3][0]

        is_string = any('string' in expr.mods for expr in values.children if isinstance(expr, lark.Tree) and expr.data == 'expr')

        self._expression = None
        return self.context.datadir_action(label, type, values, is_string=is_string, raw=get_raw(self.input_str, meta),
                                           line_number=get_line_number(meta))


    def segdir(self, nodes, type):
        logging.debug("segdir " + str(nodes) + " ~~")
        self.context.action_simplesegment(type, '')  # TODO
        self._expression = None
        return nodes


    def LABEL(self, value):
        value = self.context.mangle_label(value)
        self.name = value

        logging.debug('name = %s', self.name)
        l = lark.Token(type='LABEL', value=value)
        if self.context.has_global(self.name):
            g = self.context.get_global(self.name)
            from masm2c.proc import Proc
            if isinstance(g, (op._equ, op._assignment)):
                #if not isinstance(g.value, Expression):
                #    g.value = Asm2IR(self.context, g.raw_line).transform(g.value)
                #    self.context.reset_global(self.name, g) #??
                if isinstance(g.value, Expression):
                    self.expression.element_size = g.size = g.value.size()
            elif isinstance(g, (op.label, Proc)):
                pass
                #self.expression.indirection = IndirectionType.OFFSET  # direct using number
            elif isinstance(g, op.var):
                pass
                #self.expression.indirection = IndirectionType.POINTER  # []
            elif isinstance(g, op.Struct):
                logging.debug('get_size res %d', g.size)
                l = lark.Token(type='LABEL', value=value)
                self._size = l.size = self.expression.element_size = g.size  # TODO too much?
            else:
                logging.debug('get_size res %d', g._size)
                self.expression.element_size = g._size
                l.size = g._size

        return l


    @v_args(meta=True)
    def segmentdir(self, meta, nodes):
        logging.debug("segmentdir " + str(nodes) + " ~~")

        name = self.name = self.context.mangle_label(nodes[0])
        options = nodes
        opts = set()
        segclass = None
        '''
        if options:
            for o in options:
                if isinstance(o, str):
                    opts.add(o.lower())
                elif isinstance(o, lark.Tree) and o.data == 'label':
                    segclass = o.children[0].lower()
                    if segclass[0] in ['"', "'"] and segclass[0] == segclass[-1]:
                        segclass = segclass[1:-1]
                else:
                    logging.warning('Unknown segment option')
        '''
        self.context.create_segment(name, options=opts, segclass=segclass, raw=get_raw(self.input_str, meta))
        self._expression = None
        return nodes

    def endsdir(self, nodes):
        logging.debug("ends " + str(nodes) + " ~~")
        self.context.action_ends()
        self._expression = None
        return nodes

    def poptions(self, options):
        self._poptions = options
        return Discard

    @v_args(meta=True)
    def procdir(self, meta, nodes):
        name, type = nodes[0], self._poptions
        self._poptions = []
        logging.debug("procdir " + str(nodes) + " ~~")
        self.context.action_proc(name, type, line_number=get_line_number(meta),
                                 raw=get_raw_line(self.input_str, meta))
        return nodes

    def endpdir(self, nodes):
        name = nodes[0]
        logging.debug("endp " + str(name) + " ~~")
        self.context.action_endp()
        return nodes


    @v_args(meta=True)
    def instrprefix(self, meta, nodes):
        logging.debug("instrprefix " + str(nodes) + " ~~")
        instruction = nodes[0]
        self.context.action_instruction(instruction, [], raw=get_raw_line(self.input_str, meta),
                                        line_number=get_line_number(meta))
        return Discard

    def mnemonic(self, name):
        self.instruction_name = name[0]
        return Discard

    def comment(self, children):
        self._comment = children
        return Discard

    @v_args(meta=True)
    def instruction(self, meta, nodes):
        logging.debug("asminstruction %s ~~", nodes)
        # args = build_ast(args)

        # self.expression = self.expression or Expression()
        instruction = self.instruction_name
        args = nodes[0].children if len(nodes) else []
        if len(args) >= 2:
            args[0].mods.add('destination')
        if instruction == 'lea':
            # self.expression.indirection = IndirectionType.OFFSET
            for arg in args:
                arg.mods.add('lea')
        '''
        if not instruction:
            return nodes
        if args is None:
            args = []
        '''
        # indirection: IndirectionType = IndirectionType.VALUE
        #return Tree(instruction, args, meta)
        self._expression = None
        return self.context.action_instruction(instruction, args, raw=get_raw_line(self.input_str, meta),
                                               line_number=get_line_number(meta)) or Discard

    def enddir(self, children):
        logging.debug("end %s ~~", children)
        self.context.action_end(children[0].children[0] if children else "")
        return children


    @property
    def expression(self):
        self._expression = self._expression or Expression()
        return self._expression

    def register(self, children):
        self.expression.element_size = self.context.is_register(children[0])
        self.expression.registers.add(children[0].lower())
        return Tree(data='register', children=[children[0].lower()])  # Token('segmentregister', nodes[0].lower())

    def segmentregister(self, children):
        self.expression.element_size = self.context.is_register(children[0])
        self.expression.segment_register = children[0].lower()
        return Tree(data='segmentregister', children=[children[0].lower()])  # Token('segmentregister', nodes[0].lower())

    def sqexpr(self, nodes):
        logging.debug("/~%s~\\", nodes)
        # res = nodes[1]
        # self.expression = self.expression or Expression()
        # self.expression.indirection = IndirectionType.POINTER
        self.expression.indirection = IndirectionType.POINTER
        self.expression.element_size = 0
        return nodes  # lark.Tree(data='sqexpr', children=nodes)

    def sqexpr2(self, nodes):
        logging.debug("/~%s~\\", nodes)
        # res = nodes[1]
        # self.expression = self.expression or Expression()
        # self.expression.indirection = IndirectionType.POINTER
        self.expression.indirection = IndirectionType.POINTER
        self.expression.element_size = 0
        nodes.insert(1, lark.Token(type='PLUS', value='+'))
        nodes = [lark.Tree(data='adddir', children=nodes)]
        return nodes  # lark.Tree(data='sqexpr', children=nodes)

    def offsetdir(self, nodes):
        logging.debug("offset /~%s~\\", nodes)
        # self.expression = self.expression or Expression()
        self.expression.indirection = IndirectionType.OFFSET
        #self.expression.mods.add('offset')
        self.expression.element_size = 2
        return lark.Tree('offsetdir', nodes)

    '''
    def seg(self, nodes):
        logging.debug("segmdir /~" + str(nodes) + "~\\")
        # global indirection
        # indirection = -1
        return nodes  # Token('segmdir', nodes[1])
    '''

    def labeltok(self, nodes):
        return nodes  # Token('LABEL', nodes)

    def STRING(self, nodes):
        m = re.match(r'[\'"](.+)[\'"]$', nodes)  # char constants
        if m:
            string = m.group(1)
            if not self.context.itislst:  # not for IDA .lst
                string = string.replace("\'\'", "'").replace('\"\"', '"')  # masm behaviour
            self.expression.element_number = len(string)
            self.expression.element_size = 1
            self.expression.mods.add('string')
            nodes = lark.Token(type='STRING', value=string)
        return nodes  # Token('STRING', nodes)

    def structinstance(self, nodes): #, values):
        return nodes  # Token('structinstance', values)

    def memberdir(self, nodes):
        return lark.Tree('memberdir', [self.context.mangle_label(str(node)) for node in nodes])

    def radixdir(self, children):
        self._radix = int(children[0])
        return children


    def maked(self, nodes):
        # return nodes #Token(nodes[0].upper(), nodes[1].value)
        # TODO dirty workaround for now
        if nodes[0].lower() == 'size':
            return [f'sizeof({nodes[1].children.lower()})']
        else:
            return nodes

    def offsetdirtype(self, nodes):
        directive = nodes[0].lower()
        from .parser import Parser
        logging.debug('offsetdirtype %s', nodes)
        value = nodes[1].children[0] if len(nodes)==2 else 2
        if directive == 'align':
            self.context.align(Parser.parse_int(value))
        elif directive == 'even':
            self.context.align(2)
        elif directive == 'org':
            self.context.org(Parser.parse_int(value))
        return nodes

    # def STRING(self, token):
    #    return token


'''
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
            debug = True
            with open(file_name, 'rt') as gr:
                cls._inst.or_parser = Lark(gr, parser='lalr', propagate_positions=True, cache=True, debug=debug,
                                           postlex=MatchTag(context=kwargs['context']), start=['start', 'insegdirlist',
                                                                                               'instruction', 'expr',
                                                                                               'equtype', '_directivelist'])

            cls._inst.parser = copy(cls._inst.or_parser)

        return cls._inst


class ExprRemover(Transformer):
    @v_args(meta=True)
    def expr(self, meta, children):
        children = Token.remove_tokens(children, 'expr')

        return Tree('expr', children, meta)

class IncludeLoader(Transformer):

    def __init__(self, context):
        self.context = context

    def includedir(self, nodes):
        name = nodes[0].children[0].children[0][1:-1]
        # context.parser.input_str = context.input_str[:context.end_position] + '\n' + read_asm_file(name) \
        # + '\n' + context.input_str[context.end_position:]
        fullpath = os.path.join(os.path.dirname(os.path.realpath(self.context._current_file)), name)
        result = self.context.parse_include_file_lines(fullpath)
        return result




class TopDownVisitor:

    def visit(self, node, result=None):
        try:
            if result is None:
                result = []
            if isinstance(node, Tree):
                if hasattr(self, node.data):
                    result += getattr(self, node.data)(node)
                else:
                    result = self.visit(node.children, result)
            elif isinstance(node, lark.Token):
                if hasattr(self, node.type):
                    result += getattr(self, node.type)(node)
                else:
                    result += node.value
            elif isinstance(node, op.Data):
                result = self.visit(node.children)
            elif isinstance(node, list):
                if hasattr(self, 'list_visitor'):
                    result = self.list_visitor(node, result)
                else:
                    for i in node:
                        result = self.visit(i, result)
            elif isinstance(node, (str, int)):
                #print(f"{node} is a str")
                result += [f'{node}']
            elif hasattr(self, type(node).__name__):
                result = getattr(self, type(node).__name__)(node)
            else:
                import logging
                logging.error(f"Error unknown type {node}")
                raise ValueError(f"Error unknown type {node}")
        except Exception as ex:
            import traceback, logging
            i = traceback.format_exc()
            print(node, i, ex)
            sys.exit(1)
        return result


class BottomUpVisitor:

    def __init__(self, init=None, **kwargs):
        self.init = init
    def visit(self, node):
        result = copy(self.init)
        try:
            if isinstance(node, Tree):
                result = self.visit(node.children)
                if hasattr(self, node.data):
                    result = getattr(self, node.data)(node, result)
            elif isinstance(node, lark.Token):
                if hasattr(self, node.type):
                    result += getattr(self, node.type)(node)
            elif isinstance(node, list):
                for i in node:
                    result += self.visit(i)
            else:
                import logging
                logging.error(f"Error unknown type {node}")
                return self.init
                raise ValueError(f"Error unknown type {node}")
        except:
            import traceback, logging
            i = traceback.format_exc()
            raise
        return result

class AsmData2IR(TopDownVisitor):  # TODO HACK Remove it. !For missing funcitons deletes details!

    def seg(self, tree):
        return [f'seg_offset({tree.children[0]})']

    def expr(self, tree):
        self.element_size = tree.element_size
        result = self.visit(tree.children)
        if len(result) > 1:
            result = [result]
        return result

    def dupdir(self, tree):
        result = tree.repeat * self.visit(tree.children)
        return result
    def INTEGER(self, token):
        radix, sign, value = token.start_pos, token.line, token.column
        val = int(value, radix)
        if sign == '-':
            val = 2 ** (8 * self.element_size) - val
        return [val]

    def STRING(self, token):
        result = token.value
        #result = result.replace('\\', '\\\\')  # escape c \ symbol
        return list(result)

    def LABEL(self, tree):
        return [lark.Token(type='LABEL', value=tree.lower())]  # TODO HACK

    def bypass(self, tree):
        return [tree]

    offsetdir = bypass


OFFSETDIR = 'offsetdir'
LABEL = 'LABEL'
PTRDIR = 'ptrdir'
REGISTER = 'register'
SEGMENTREGISTER = 'segmentregister'
SEGOVERRIDE = 'segoverride'
SQEXPR = 'sqexpr'
INTEGER = 'integer'
MEMBERDIR = 'memberdir'
