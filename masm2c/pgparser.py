"""
Handle the parsing of MASM code using the Lark library.
It defines grammar rules, actions for different types of instructions and directives,
and transforms the parsed tree into an intermediate representation (IR) for further processing.
"""
from typing import TYPE_CHECKING, Optional, Final

if TYPE_CHECKING:
    from masm2c.parser import Parser, Vector

import logging
import lark.lexer
import lark.tree
from lark.visitors import _DiscardType

from masm2c.Token import Expression
from masm2c.op import Data, _assignment, baseop, Struct

import os
import re
import sys
from collections import OrderedDict
from collections.abc import Iterator
from copy import copy, deepcopy
from typing import Any

from lark import Discard, Lark, Transformer, Tree, v_args

from . import op
from .enumeration import IndirectionType
from .Macro import Macro
from .Token import Token

macroses: OrderedDict[str, Macro] = OrderedDict()
macronamere = re.compile(r"([A-Za-z_@$?][A-Za-z0-9_@$?]*)")
commentid = re.compile(r"COMMENT\s+([^ ]).*?\1[^\r\n]*", flags=re.DOTALL)

class MatchTag:
    always_accept = "LABEL", "structinstdir", "STRUCTNAME"

    def __init__(self, context: "Parser") -> None:
        self.context = context
        self.last_type = ""
        self.last = ""

    def process(self, stream: Iterator[lark.Token]) -> Iterator[lark.Token]:
        for t in stream:
            if self.last_type == "LABEL" and t.type == "LABEL" and t.value.lower() in {"struc","struct","union"}:  # HACK workaround
                t.type = "STRUCTHDR"
            if t.type == "LABEL" and t.value.lower() in ["ends"]:  # HACK workaround
                print(self.last_type, self.last)
                t.type = "endsdir"

            if self.last_type == "LABEL" and t.type == "STRUCTHDR":
                assert self.last
                self.context.structures[self.last.lower()] = Struct("", "")

            # if t.type == "STRUCTHDR":
            if self.context.structures and self.last_type == "LABEL" \
                    and t.type == "LABEL" and t.value.lower() in self.context.structures:
                t.type = "STRUCTNAME"
            self.last_type = t.type
            self.last = t.value
            yield t

def get_line_number(meta: lark.tree.Meta) -> int:
    """It returns the line number of the current position in the input string.

    :param context: the context object that is passed to the action function
    :return: The line number of the current position in the input string.
    """
    return meta.line


def get_raw(input_str: str, meta: lark.tree.Meta) -> str:
    """It returns the raw text that was provided to parser.

    :param context:
    :return: The raw string from the input string.
    """
    return input_str[meta.start_pos: meta.end_pos].strip()


def get_raw_line(input_str: str, meta: lark.tree.Meta) -> str:
    """It returns the raw line of text that the cursor is currently on.

    :return: The line of text from the input string.
    """
    try:
        line_strt_pos = input_str.rfind("\n", 0, meta.start_pos) + 1

        line_eol_pos = input_str.find("\n", meta.start_pos)
        if line_eol_pos == -1:
            line_eol_pos = len(input_str)
    except Exception as ex:
        print(ex)
    return input_str[line_strt_pos: line_eol_pos]


class CommonCollector(Transformer):

    def __init__(self, context: "Parser", input_str: str="") -> None:
        self.context = context
        self._expression: Optional[Expression] = None
        self.input_str = input_str

"""
class EquCollector(CommonCollector):

    def __init__(self, context, input_str=''):
        super().__init__(context, input_str)


"""


class Getmacroargval:

    def __init__(self, params, args) -> None:
        self.argvaluedict = OrderedDict(zip(params, args))

    def __call__(self, token):
        return self.argvaluedict[token.children]



class Asm2IR(CommonCollector):

    def __init__(self, context: "Parser", input_str: str="") -> None:
        super().__init__(context, input_str)
        self._radix = 10
        self._element_type = ''

        self._size = 0
        self._poptions: list[str] = []

    def externdef(self, nodes: list[lark.Tree | lark.Token]) -> list[lark.Tree | lark.Token]:
        label, type = nodes
        assert isinstance(type, lark.Tree)
        type = type.children[0].children[0]
        logging.debug("externdef %s", nodes)
        assert isinstance(type, lark.Token)
        self.context.add_extern(str(label), type)
        return nodes

    @v_args(meta=True)
    def equdir(self, meta: lark.tree.Meta, nodes: list[lark.Tree | lark.Token]):
        name, value = str(nodes[0]), nodes[1]
        logging.debug("equdir %s ~~", nodes)

        return self.context.action_equ(name, value, raw=get_raw(self.input_str, meta),
                                       line_number=get_line_number(meta))

    @v_args(meta=True)
    def assdir(self, meta: lark.tree.Meta, nodes: list[lark.lexer.Token | Expression]) -> _assignment:
        name, value = str(nodes[0]), nodes[1]
        logging.debug("assdir %s ~~", nodes)
        assert isinstance(name, str) and isinstance(value, Expression)
        return self.context.action_assign(name, value, raw=get_raw(self.input_str, meta),
                                          line_number=get_line_number(meta))

    @v_args(meta=True)
    def labeldef(self, meta, nodes):
        logging.debug("labeldef %s ~~", nodes)
        name, colon = str(nodes[0]), nodes[1]
        return self.context.action_label(name, isproc=False, raw=get_raw_line(self.input_str, meta),
                                         line_number=get_line_number(meta),
                                         globl=(colon == "::"))


    """
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
    """

    def expr(self, children: list[Any]) -> Expression:
        # while isinstance(children, list) and len(children) == 1:
        self.expression.children = children  # [0]
        assert self._expression
        result:Expression = self._expression
        if not self.expression.segment_overriden and result.indirection == IndirectionType.POINTER and \
                result.registers.intersection({"bp", "ebp", "sp", "esp"}):
            result.segment_register = "ss"
        #if result.indirection == IndirectionType.POINTER:
        self._expression = None
        return result

    def initvalue(self, expr: list[lark.Token]) -> lark.Tree:
        return lark.Tree(data="exprlist", children=[self.expr(expr)])

    def dupdir(self, children: list[Expression | lark.Tree]) -> lark.Tree:
        from masm2c.cpp import IR2Cpp
        repeat = copy(children[0])
        assert isinstance(repeat, Expression)
        repeat.indirection = IndirectionType.VALUE
        repeat_str = "".join(IR2Cpp(self.context).visit(repeat))
        repeat_int = eval(repeat_str)
        value = [children[1]]
        result: lark.Tree = lark.Tree(data="dupdir", children=value)
        result.meta.line = repeat_int
        return result  # Token('dupdir', [times, values])

    def segoverride(self, nodes: list[list[lark.Tree] | list[lark.Tree | lark.lexer.Token] | lark.Tree | lark.lexer.Token]) -> list[list[lark.Tree] | list[lark.Tree | lark.lexer.Token] | lark.Tree | lark.lexer.Token]:
        #seg = nodes[0]
        #if isinstance(seg, list):
        #    seg = seg[0]
        self.expression.indirection = IndirectionType.POINTER
        self.expression.element_size = 0
        self.expression.segment_overriden = True
        return nodes[1:]

    def distance(self, children: list[lark.Token]) -> str:
        self.expression.mods.add(children[0].lower())
        self._size = self.context.typetosize(children[0])
        return str(children[0]).lower()

    @v_args(meta=True)
    def ptrdir(self, meta: lark.tree.Meta, children: list[str | list[lark.lexer.Token] | lark.lexer.Token | list[lark.Tree] | lark.Tree]) -> list[str | list[lark.lexer.Token] | lark.lexer.Token | list[lark.Tree] | lark.Tree]:
        if self.expression.indirection == IndirectionType.VALUE:  # set above
            self.expression.indirection = IndirectionType.POINTER
        try:
            assert isinstance(children[0], (str, lark.lexer.Token))
            type = children[0].lower()  # TODO handle jmp short near abc
        except Exception:
            logging.exception("Error %s:%s", get_line_number(meta), get_raw_line(self.input_str, meta))
            sys.exit(11)
        #if self._size: # TODO why need another variable?
        self.expression.ptr_size = self.context.typetosize(type)
        if type not in {"far", "near"}:
            self.expression.mods.add("size_changed")
        self._element_type = self.expression.original_type = type
        children = children[1:]
        self.expression.element_size = 0
        return children

    def ptrdir2(self, children: list[lark.Tree | lark.lexer.Token]) -> list[lark.Tree | lark.lexer.Token]:  # tasm?
        self.expression.indirection = IndirectionType.POINTER
        self.expression.segment_overriden = True
        assert isinstance(children[0], (str, lark.Token))
        self.expression.ptr_size = self.context.typetosize(children[0])
        self.expression.mods.add("size_changed")
        self._element_type = self.expression.original_type = children[0].lower()
        return children[3:]

    def datadecl(self, children: list[lark.Token]) -> str:
        self._size = self.context.typetosize(children[0])
        self._element_type = children[0].lower()
        return str(children[0]).lower()

    def ANYTHING(self, value: lark.lexer.Token) -> lark.lexer.Token:
        return self.INTEGER("0")

    def INTEGER(self, value: lark.lexer.Token | str) -> lark.lexer.Token:
        from .gen import guess_int_size
        from .parser import parse_asm_number

        radix, sign, value = parse_asm_number(value, self._radix)

        val = int(value, radix)
        if sign == "-":
            val *= -1
        self.expression.element_size_guess = guess_int_size(val)
        sign_int = -1 if sign=="-" else 1
        t = lark.Token(type="INTEGER", value=sign + value)
        t.start_pos, t.line, t.value = radix, sign_int, value
        return t  # Token('INTEGER', Cpp(self.context.convert_asm_number_into_c(nodes, self.context.radix))  # TODO remove this

    def commentkw(self, head, s, pos):
        # multiline comment
        if s[pos:pos + 7] == "COMMENT" and (mtch := commentid.match(s[pos:])):
            return mtch.group(0)
        return None

    def macroname(self, s, pos):
        if mtch := macronamere.match(s[pos:]):
            if macroses:
                result = mtch.group().lower()
                if result in macroses:
                    logging.debug(" ~^~%s~^~ in macronames", result)
                    return result
        return None

    def macrodirhead(self, nodes, name, parms):
        # macro definition header
        param_names = []
        if parms:
            param_names = [i.lower() for i in Token.find_tokens(parms, "LABEL")]
        self.context.current_macro = Macro(name.children.lower(), param_names)
        self.context.macro_names_stack.add(name.children.lower())
        logging.debug("macroname added ~~%s~~", name.children)
        return nodes

    def repeatbegin(self, nodes, value):
        # start of repeat macro
        self.context.current_macro = Macro("", [], value)
        self.context.macro_names_stack.add("")  # TODO
        logging.debug("repeatbegin")
        return nodes

    def endm(self, nodes):
        # macro definition end
        name = self.context.macro_names_stack.pop()
        logging.debug("endm %s", name)
        macroses[name] = self.context.current_macro
        self.context.current_macro = None
        return nodes

    def macrocall(self, nodes, name, args):
        # macro usage
        logging.debug("macrocall %s~~", name)
        macros = macroses[name]
        instructions = deepcopy(macros.instructions)
        param_assigner = self.Getmacroargval(macros.getparameters(), args)
        for instruction in instructions:
            instruction.children = Token.find_and_replace_tokens(instruction.children, "LABEL", param_assigner)
        self.context.proc.stmts += instructions
        return nodes

    def structname(self, s, pos):
        if mtch := macronamere.match(s[pos:]):
            if self.context.structures:
                result = mtch.group().lower()
                if result in self.context.structures:
                    logging.debug(" ~^~%s~^~ in structures", result)
                    return result
        return None

    def structdirhdr(self, nodes: list[lark.Token]) -> list[lark.Token]:
        name, type = nodes
        # structure definition header
        self.context.current_struct = op.Struct(name.lower(), type.lower())
        self.context.struct_names_stack.append(name.lower())
        logging.debug("structname added ~~%s~~", name)
        return nodes

    @v_args(meta=True)
    def structinstdir(self, meta:     lark.tree.Meta, nodes: list[lark.Tree | lark.lexer.Token]) -> _DiscardType:
        label, type, values = nodes
        logging.debug("structinstdir %s %s %s", label, type, values)
        assert isinstance(values, lark.Tree)
        args = values.children[0]
        if args is None:
            args = []
        assert isinstance(label, lark.Token)
        name = label.lower() if label else ""
        assert isinstance(type, lark.Token)
        assert isinstance(args, list)
        self.context.add_structinstance(name, type.lower(), args, raw=get_raw(self.input_str, meta))
        return Discard

    def insegdir(self, children: list) -> list[lark.Tree | Data | _assignment]:
        self._expression = None
        self._element_type = ""
        self._size = 0
        return children

    @v_args(meta=True)
    def datadir(self, meta:     lark.tree.Meta, children: list) -> _DiscardType | Data | list:
        logging.debug("datadir %s ~~", children)
        if not children: return Discard

        if len(children)==1: # TODO why?
            children = children[0]
        label = self.context.mangle_label(children.pop(0)) if isinstance(children[0], lark.Token) and children[0].type == "LABEL" else ""
        type = children.pop(0).lower()
        if isinstance(children[0], lark.Tree):  # Data
            values = lark.Tree(data="data", children=children[0].children)
        else:
            values = children[0][2:3][0]

        is_string = any("string" in expr.mods for expr in values.children if isinstance(expr, Expression) and expr.data == "expr") \
                    and not any(isinstance(expr, lark.Tree) and expr.data == "dupdir" for expr in values.children)

        self._expression = None
        return self.context.datadir_action(label, type, values, is_string=is_string, raw=get_raw(self.input_str, meta),
                        line_number=get_line_number(meta))


    def segdir(self, nodes: list):
        segtype = nodes[-1] if nodes else ""
        logging.debug("segdir %s ~~", nodes)
        self.context.action_simplesegment(segtype.lower(), None)  # TODO
        self._expression = None
        return nodes


    def LABEL(self, value_in: lark.lexer.Token) -> lark.lexer.Token:
        value = self.context.mangle_label(value_in)
        self.name = value

        logging.debug("name = %s", self.name)
        l = lark.Token("LABEL", value)
        if g := self.context.symbols.get_and_mark_global(self.name):
            from masm2c.proc import Proc
            if isinstance(g, (op._equ, op._assignment)):
                #if not isinstance(g.value, Expression):
                if isinstance(g.value, Expression):
                    g.size = g.value.size()
                    if (len(g.children) == 2 and isinstance(g.children[1], Expression) and
                            g.children[1].indirection == IndirectionType.POINTER):
                        self.expression.ptr_size = g.size
                    else:
                        self.expression.element_size = g.size
            elif isinstance(g, (Proc, op.label, op.var)):
                pass
            elif isinstance(g, op.Struct):
                logging.debug("get_size res %d", g.size)
                l = lark.Token(type="LABEL", value=value)
                self._size =  self.expression.element_size = g.size  # TODO too much?
            else:
                logging.debug("get_size res %d", g._size)
                self.expression.element_size = g._size
                assert False, "Dead code?"
                l.size = g._size

        return l


    @v_args(meta=True)
    def segmentdir(self, meta, nodes):
        logging.debug("segmentdir %s ~~", nodes)

        name = self.name = self.context.mangle_label(nodes[0])
        opts = set()
        segclass = None
        """
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
        """
        self.context.create_segment(name, options=opts, segclass=segclass, raw=get_raw(self.input_str, meta))
        self._expression = None
        return nodes

    def endsdir(self, nodes: list[lark.lexer.Token]) -> list[lark.lexer.Token]:
        logging.debug("ends %s ~~", nodes)
        self.context.action_ends()
        self._expression = None
        return nodes

    def poptions(self, options: list):
        self._poptions = options
        return Discard

    @v_args(meta=True)
    def procdir(self, meta, nodes):
        name, type = nodes[0], self._poptions
        self._poptions = []
        logging.debug("procdir %s ~~", nodes)
        self.context.action_proc(name, type, line_number=get_line_number(meta),
                                 raw=get_raw_line(self.input_str, meta))
        self._expression = None
        return nodes

    def endpdir(self, nodes):
        name = nodes[0]
        logging.debug("endp %s ~~", name)
        self.context.action_endp()
        return nodes


    @v_args(meta=True)
    def instrprefix(self, meta:     lark.tree.Meta, nodes: list[lark.Token]) -> _DiscardType:
        logging.debug("instrprefix %s ~~", nodes)
        instruction = str(nodes[0])
        self.context.action_instruction(instruction, [], raw=get_raw_line(self.input_str, meta),
                                        line_number=get_line_number(meta))
        return Discard

    def mnemonic(self, name: list[lark.Token]) -> _DiscardType:
        self.instruction_name = str(name[0])
        return Discard

    def comment(self, children: list[lark.Token]) -> _DiscardType:
        self._comment = children
        return Discard

    @v_args(meta=True)
    def instruction(self, meta:     lark.tree.Meta, nodes: list[Any | lark.Tree]) -> baseop | _DiscardType:
        logging.debug("asminstruction %s ~~", nodes)

        instruction = self.instruction_name
        args = nodes[0].children if len(nodes) else []
        if len(args) >= 2:
            assert isinstance(args[0], Expression)
            args[0].mods.add("destination")
        if instruction == "lea":
            for arg in args:
                assert isinstance(arg, Expression)
                arg.mods.add("lea")
        self._expression = None
        return self.context.action_instruction(instruction, args, raw=get_raw_line(self.input_str, meta),
                                               line_number=get_line_number(meta)) or Discard

    def enddir(self, children):
        logging.debug("end %s ~~", children)
        self.context.action_end(children[0].children[0] if children else "")
        return children


    @property
    def expression(self) -> Expression:
        self._expression = self._expression or Expression()
        assert self._expression
        return self._expression

    def register(self, children: list[lark.Token]) ->     lark.Tree:
        self.expression.element_size = self.context.is_register(children[0])
        self.expression.registers.add(children[0].lower())
        return Tree(data="register", children=[children[0].lower()])  # Token('segmentregister', nodes[0].lower())

    def segmentregister(self, children: list[lark.Token]) ->     lark.Tree:
        self.expression.element_size = self.context.is_register(children[0])
        self.expression.segment_register = children[0].lower()
        return Tree(data="segmentregister", children=[children[0].lower()])  # Token('segmentregister', nodes[0].lower())

    def sqexpr(self, nodes: list[lark.Tree | lark.lexer.Token | list[lark.Tree]]) -> list[lark.Tree | lark.lexer.Token | list[lark.Tree]]:
        logging.debug("/~%s~\\", nodes)
        self.expression.indirection = IndirectionType.POINTER
        self.expression.element_size = 0
        return nodes  # lark.Tree(data='sqexpr', children=nodes)

    def sqexpr2(self, nodes: list[lark.Tree | lark.lexer.Token]) -> list[lark.Tree]:
        logging.debug("/~%s~\\", nodes)
        self.expression.indirection = IndirectionType.POINTER
        self.expression.element_size = 0
        nodes.insert(1, lark.Token(type="PLUS", value="+"))
        nodes_out = [lark.Tree(data="adddir", children=nodes)]
        return nodes_out  # lark.Tree(data='sqexpr', children=nodes)

    def offsetdir(self, nodes: list[lark.Tree | lark.lexer.Token]) ->     lark.Tree:
        logging.debug("offset /~%s~\\", nodes)
        self.expression.indirection = IndirectionType.OFFSET
        self.expression.element_size = 2
        if isinstance(nodes[0], lark.Token):  # for labels, not for memberdir
            nodes = [nodes[0]]
        return lark.Tree("offsetdir", nodes)

    """
    def seg(self, nodes):
        logging.debug("segmdir /~" + str(nodes) + "~\\")
        # global indirection
        # indirection = -1
        return nodes  # Token('segmdir', nodes[1])
    """

    def labeltok(self, nodes):
        return nodes  # Token('LABEL', nodes)

    def STRING(self, nodes: lark.lexer.Token) -> lark.lexer.Token:
        if m := re.match(r'[\'"](.+)[\'"]$', nodes):
            string = m[1]
            if not self.context.itislst:  # not for IDA .lst
                string = string.replace("''", "'").replace('""', '"')  # masm behaviour
            self.expression.element_number = len(string)
            self.expression.element_size = 1
            self.expression.mods.add("string")
            nodes = lark.Token(type="STRING", value=string)
        return nodes  # Token('STRING', nodes)

    def structinstance(self, nodes: list[Any | lark.Tree]) -> list[Any | lark.Tree]: #, values):
        return nodes  # Token('structinstance', values)

    def memberdir(self, nodes: list[lark.Token]) ->     lark.Tree:
        return lark.Tree("memberdir", [self.context.mangle_label(str(node)) for node in nodes])

    def radixdir(self, children):
        self._radix = int(children[0])
        return children


    def maked(self, nodes):
        # TODO dirty workaround for now
        if nodes[0].lower() == "size":
            return [f"sizeof({nodes[1].children.lower()})"]
        else:
            return nodes

    def offsetdirtype(self, nodes):
        directive = nodes[0].lower()
        from masm2c.parser import Parser
        logging.debug("offsetdirtype %s", nodes)
        value = str(nodes[1].children[0]) if len(nodes)==2 else 2
        if directive == "align":
            self.context.align(Parser.parse_int(value))
        elif directive == "even":
            self.context.align(2)
        elif directive == "org":
            self.context.org(Parser.parse_int(value))
        return nodes

    # def STRING(self, token):


"""
recognizers = {
    'macroname': macroname,
    "structname": structname,
    "COMMENTKW": commentkw
}
"""


class LarkParser:
    parser: Final[list] = []

    def __init__(self, context: "Parser") -> None:
        if self.parser:
            return

        logging.debug("Allocated LarkParser instance")

        file_name = f"{os.path.dirname(os.path.realpath(__file__))}/_masm61.lark"
        debug = True
        with open(file_name) as gr:
            self.parser.append(Lark(gr, parser="lalr", propagate_positions=True, cache=True, debug=debug,
                                       postlex=MatchTag(context=context), start=["start", "insegdirlist",
                                                                                           "instruction", "expr",
                                                                                           "equtype", "_directivelist"]))
            #print(sorted([term.pattern.value for term in cls._inst.or_parser.terminals if term.pattern.type == 'str']))



class ExprRemover(Transformer):
    @v_args(meta=True)
    def expr(self, meta:     lark.tree.Meta, children: list[lark.Tree | lark.lexer.Token]) ->     lark.Tree:
        children = Token.remove_tokens(children, ["expr"])

        return Tree("expr", children, meta)

class IncludeLoader(Transformer):

    def __init__(self, context: "Parser") -> None:
        self.context = context

    def includedir(self, nodes):
        name = nodes[0].children[0]
        name = name[1:-1] if name[0] == "<" and name[-1] == ">" else name
        fullpath = os.path.join(os.path.dirname(os.path.realpath(self.context._current_file)), name)
        return self.context.parse_include_file_lines(fullpath)




class TopDownVisitor:

    def visit(self, node: Any, result: Any | None=None) -> list[Any]:
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
                if hasattr(self, "list_visitor"):
                    result = self.list_visitor(node, result)
                else:
                    for i in node:
                        result = self.visit(i, result)
            elif isinstance(node, (str, int)):
                result += [f"{node}"]
            elif hasattr(self, type(node).__name__):
                result = getattr(self, type(node).__name__)(node)
            else:
                logging.error(f"Error unknown type {type(node).__name__} {node}")
                raise ValueError(f"Error unknown type {type(node).__name__} {node}")
        except Exception as ex:
            logging.exception("Exception %s", node)
            sys.exit(1)
        return result


class BottomUpVisitor:

    def __init__(self, init: Optional["Vector"]=None, **kwargs) -> None:
        self.init = init
    def visit(self, node: Any) -> "Vector":
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
                    assert result is not None
                    result += self.visit(i)
            else:
                import logging
                logging.error(f"Error unknown type {node}")
                assert self.init is not None
                return self.init
        except:
            import logging
            import traceback
            i = traceback.format_exc()
            raise
        assert result is not None
        return result

class AsmData2IR(TopDownVisitor):  # TODO HACK Remove it. !For missing funcitons deletes details!

    def seg(self, tree:     lark.Tree) -> list[str]:
        return [f"seg_offset({tree.children[0]})"]

    def expr(self, tree: Expression) -> list[Any]:
        self.element_size = tree.element_size
        result = self.visit(tree.children)
        if len(result) > 1:
            result = [result]
        return result

    def dupdir(self, tree:     lark.Tree) -> list[int | list[lark.lexer.Token | str | int] | list[str | int]]:
        return tree.meta.line * self.visit(tree.children)
    def INTEGER(self, token: lark.lexer.Token) -> list[int]:
        radix, sign, value = token.start_pos, token.line, token.value
        assert radix
        val = int(value, radix)
        if sign == -1:
            val = 2 ** (8 * self.element_size) - val
        return [val]

    def STRING(self, token: lark.lexer.Token) -> list[str]:
        result = token.value
        return list(result)

    def LABEL(self, tree: lark.lexer.Token) -> list[lark.Token]:
        return [lark.Token(type="LABEL", value=tree.lower())]  # TODO HACK

    def bypass(self, tree:     lark.Tree) -> list[    lark.Tree]:
        return [tree]

    def offsetdir(self, tree:     lark.Tree) -> list[    lark.Tree]:
        return [tree]


OFFSETDIR = "offsetdir"
LABEL = "LABEL"
PTRDIR = "ptrdir"
REGISTER = "register"
SEGMENTREGISTER = "segmentregister"
SEGOVERRIDE = "segoverride"
SQEXPR = "sqexpr"
INTEGER = "integer"
MEMBERDIR = "memberdir"
