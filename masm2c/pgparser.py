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
from masm2c.op import Data, _assignment, baseop

import os
import re
import sys
from collections import OrderedDict
from collections.abc import Iterator
from copy import copy, deepcopy
from typing import Any, cast

from lark import Discard, Lark, Transformer, Tree, v_args

from . import op
from .enumeration import IndirectionType
from .Token import Token

macronamere = re.compile(r"([A-Za-z_@$?][A-Za-z0-9_@$?]*)")
commentid = re.compile(r"COMMENT\s+([^ ]).*?\1[^\r\n]*", flags=re.DOTALL)


def _token_text(token: Any) -> str:
    return str(token)


def _token_lower(token: Any) -> str:
    return str(token).lower()


def _is_token(token: Any) -> bool:
    return (
        hasattr(token, "type")
        and hasattr(token, "value")
    )

class MatchTag:
    __slots__ = ("context", "last_type", "last")
    always_accept = "LABEL", "structinstdir", "STRUCTNAME", "RECORDNAME"

    def __init__(self, context: "Parser") -> None:
        self.context = context
        self.last_type = ""
        self.last = ""

    def process(self, stream: Iterator[Any]) -> Iterator[Any]:
        for t in stream:
            yield self._process_token(t)

    def __call__(self, token: Any) -> Any:
        return self._process_token(token)

    def _process_token(self, token: Any) -> Any:
        token_text = _token_lower(token.value)
        if self.last_type == "LABEL" and token.type == "LABEL" and token_text in {"struc", "struct", "union"}:  # HACK workaround
            token.type = "STRUCTHDR"
        if token.type == "LABEL" and token_text == "ends":  # HACK workaround
            token.type = "endsdir"

        if self.last_type == "LABEL" and token.type == "STRUCTHDR":
            assert self.context
            self.context.declare_structure_name(self.last)

        # if token.type == "STRUCTHDR":
        if self.context.has_any_structures() and self.last_type == "LABEL" \
                and token.type == "LABEL" and self.context.match_known_structure_name(_token_text(token.value)):
            token.type = "STRUCTNAME"
        if token.type == "LABEL" and self.context.match_known_record_name(_token_text(token.value)):
            token.type = "RECORDNAME"

        self.last_type = token.type
        self.last = _token_text(token.value)
        return token

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
    __slots__ = ("context", "_expression", "input_str")

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
    __slots__ = ("argvaluedict",)

    def __init__(self, params, args) -> None:
        self.argvaluedict = OrderedDict(zip(params, args))

    def __call__(self, token):
        return self.argvaluedict[token.children]



class Asm2IR(CommonCollector):
    __slots__ = ()

    def __init__(self, context: "Parser", input_str: str="") -> None:
        super().__init__(context, input_str)

    def _clear_expression(self) -> None:
        self._expression = None

    def _finish_expression(self, children: list[Any]) -> Expression:
        expr = self.expression
        expr.children = children
        if (
            not expr.segment_overriden
            and expr.indirection == IndirectionType.POINTER
            and expr.registers.intersection({"bp", "ebp", "sp", "esp"})
        ):
            expr.segment_register = "ss"
        self._clear_expression()
        return expr

    def externdef(self, nodes: list[lark.Tree | lark.Token]) -> list[lark.Tree | lark.Token]:
        label, symbol_type = nodes
        resolved_type: str | lark.Token
        if isinstance(symbol_type, lark.Tree):
            node = symbol_type
            while isinstance(node, lark.Tree) and node.children:
                child = node.children[0]
                if isinstance(child, lark.Tree):
                    node = child
                    continue
                resolved_type = str(child).lower()
                break
            else:
                resolved_type = "word"
        else:
            resolved_type = str(symbol_type).lower()
        logging.debug("externdef %s", nodes)
        self.context.declare_external_symbol(str(label), resolved_type)
        return nodes

    @v_args(meta=True)
    def equdir(self, meta: lark.tree.Meta, nodes: list[lark.Tree | lark.Token]):
        pending_name = self.context.consume_pending_mnemonic()
        if pending_name:
            name, value = pending_name, nodes[0]
        else:
            name, value = str(nodes[0]), nodes[1]
        logging.debug("equdir %s ~~", nodes)

        return self.context.define_equ(name, cast(Expression, value), raw=get_raw(self.input_str, meta),
                                       line_number=get_line_number(meta))

    @v_args(meta=True)
    def assdir(self, meta: lark.tree.Meta, nodes: list[lark.lexer.Token | Expression]) -> _assignment:
        name, value = str(nodes[0]), nodes[1]
        logging.debug("assdir %s ~~", nodes)
        assert isinstance(name, str) and isinstance(value, Expression)
        return self.context.define_assignment(name, value, raw=get_raw(self.input_str, meta),
                                              line_number=get_line_number(meta))

    @v_args(meta=True)
    def labeldef(self, meta, nodes):
        logging.debug("labeldef %s ~~", nodes)
        raw = get_raw_line(self.input_str, meta)
        if len(nodes) >= 2:
            name, colon = str(nodes[0]), nodes[1]
        else:
            mtch = re.match(r"^\s*([A-Za-z_@$?][A-Za-z0-9_@$?]*)\s*(::|:)", raw)
            if not mtch:
                raise ValueError(f"cannot recover label name from line: {raw!r}")
            name, colon = mtch.group(1), mtch.group(2)
        return self.context.define_label(name, raw=raw,
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
        return self._finish_expression(children)

    def initvalue(self, expr: list[lark.Token]) -> lark.Tree:
        return lark.Tree(data="exprlist", children=[self.expr(expr)])

    def dupdir(self, children: list[Expression | lark.Tree]) -> lark.Tree:
        repeat = copy(children[0])
        assert isinstance(repeat, Expression)
        repeat_int = self.context.evaluate_repeat_count(repeat)
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
        token = children[0]
        token_value = _token_lower(token)
        self.expression.mods.add(token_value)
        return token_value

    @v_args(meta=True)
    def ptrdir(self, meta: lark.tree.Meta, children: list[str | list[lark.lexer.Token] | lark.lexer.Token | list[lark.Tree] | lark.Tree]) -> list[str | list[lark.lexer.Token] | lark.lexer.Token | list[lark.Tree] | lark.Tree]:
        if self.expression.indirection == IndirectionType.VALUE:  # set above
            self.expression.indirection = IndirectionType.POINTER
        try:
            assert isinstance(children[0], str) or _is_token(children[0])
            type = _token_lower(children[0])  # TODO handle jmp short near abc
        except Exception:
            logging.exception("Error %s:%s", get_line_number(meta), get_raw_line(self.input_str, meta))
            sys.exit(11)
        #if self._size: # TODO why need another variable?
        self.expression.ptr_size = self.context.sizeof_type(type)
        if type not in {"far", "near"}:
            self.expression.mods.add("size_changed")
        self.expression.original_type = type
        children = children[1:]
        self.expression.element_size = 0
        return children

    def ptrdir2(self, children: list[lark.Tree | lark.lexer.Token]) -> list[lark.Tree | lark.lexer.Token]:  # tasm?
        self.expression.indirection = IndirectionType.POINTER
        self.expression.segment_overriden = True
        assert isinstance(children[0], str) or _is_token(children[0])
        self.expression.ptr_size = self.context.sizeof_type(_token_text(children[0]))
        self.expression.mods.add("size_changed")
        self.expression.original_type = _token_lower(children[0])
        return children[3:]

    def datadecl(self, children: list[lark.Token]) -> str:
        return str(children[0]).lower()

    def ANYTHING(self, value: lark.lexer.Token) -> lark.lexer.Token:
        return self.INTEGER("0")

    def INTEGER(self, value: lark.lexer.Token | str) -> lark.lexer.Token:
        from .gen import guess_int_size
        from .parser import parse_asm_number

        radix, sign, value = parse_asm_number(value, self.context.radix)

        val = int(value, radix)
        if sign == "-":
            val *= -1
        self.expression.element_size_guess = guess_int_size(val)
        sign_int = -1 if sign=="-" else 1
        t = lark.Token(type="INTEGER", value=sign + value)
        t.start_pos, t.line, t.value = radix, sign_int, value
        return t  # Token('INTEGER', Cpp(self.context.convert_asm_number_into_c(nodes, self.context.radix))  # TODO remove this

    def commentkw(self, _head, s, pos):
        # multiline comment
        if s[pos:pos + 7] == "COMMENT" and (mtch := commentid.match(s[pos:])):
            return mtch.group(0)
        return None

    def macroname(self, s, pos):
        if mtch := macronamere.match(s[pos:]):
            result = mtch.group().lower()
            if self.context.is_known_macro(result):
                logging.debug(" ~^~%s~^~ in macronames", result)
                return result
        return None

    def macrodirhead(self, nodes: list[lark.Tree | lark.Token]):
        # macro definition header
        name_token = nodes[0]
        param_names: list[str] = []
        if len(nodes) > 2:
            found_params = Token.find_tokens(nodes[2:], "LABEL")
            if found_params:
                param_names = [str(i).lower() for i in found_params]
        macro_name = str(name_token).lower()
        self.context.begin_named_macro(macro_name, param_names)
        logging.debug("macroname added ~~%s~~", macro_name)
        return nodes

    def repeatbegin(self, nodes: list[lark.Tree | lark.Token]):
        # start of repeat macro
        repeat_value = 0
        if len(nodes) > 1:
            repeat_node = nodes[1]
            if isinstance(repeat_node, Expression):
                repeat_value = self.context.evaluate_repeat_count(repeat_node)
            elif isinstance(repeat_node, lark.Tree):
                integer_tokens = Token.find_tokens(repeat_node.children, "INTEGER")
                if integer_tokens:
                    repeat_value = int(str(integer_tokens[0]), 0)
            elif _is_token(repeat_node):
                repeat_value = int(str(repeat_node), 0)
        self.context.begin_repeat_macro(repeat_value)
        logging.debug("repeatbegin")
        return nodes

    def macend(self, nodes):
        # macro definition end
        if not self.context.macro_names_stack:
            return nodes
        name = self.context.end_macro_definition()
        logging.debug("macend %s", name)
        return nodes

    def macrocall(self, nodes, name, args):
        # macro usage
        logging.debug("macrocall %s~~", name)
        macros = self.context.get_macro(name)
        instructions = deepcopy(macros.instructions)
        param_assigner = self.Getmacroargval(macros.getparameters(), args)
        for instruction in instructions:
            instruction.children = Token.find_and_replace_tokens(instruction.children, "LABEL", param_assigner)
        self.context.append_current_statements(instructions)
        return nodes

    def structname(self, s, pos):
        if mtch := macronamere.match(s[pos:]):
            if result := self.context.match_known_structure_name(mtch.group()):
                logging.debug(" ~^~%s~^~ in structures", result)
                return result
        return None

    def structdirhdr(self, nodes: list[lark.Token]) -> list[lark.Token]:
        if len(nodes) < 2:
            return nodes
        name = nodes[0]
        type = nodes[1]
        # structure definition header
        self.context.begin_structure_definition(str(name), str(type))
        logging.debug("structname added ~~%s~~", name)
        return nodes

    @v_args(meta=True)
    def structinstdir(self, meta:     lark.tree.Meta, nodes: list[lark.Tree | lark.lexer.Token]) -> _DiscardType:
        logging.debug("structinstdir %s", nodes)
        label = None
        if len(nodes) == 2:
            struct_type, values = nodes
        elif len(nodes) == 3:
            label, struct_type, values = nodes
        else:
            raise ValueError(f"Unexpected structinstdir node count: {len(nodes)}")
        assert isinstance(values, lark.Tree)
        args = values.children[0]
        if args is None:
            args = []
        name = _token_text(label) if _is_token(label) else ""
        struct_type_name = _token_text(struct_type)
        assert isinstance(args, list)
        self.context.define_struct_instance(name, struct_type_name, args, raw=get_raw(self.input_str, meta))
        return Discard

    def insegdir(self, children: list) -> list[lark.Tree | Data | _assignment]:
        self._clear_expression()
        self.context.flush_pending_source_comment()
        return children

    @v_args(meta=True)
    def datadir(self, meta:     lark.tree.Meta, children: list) -> _DiscardType | Data | list:
        logging.debug("datadir %s ~~", children)
        if not children:
            return Discard

        if len(children)==1: # TODO why?
            children = children[0]
        pending_label = self.context.consume_pending_mnemonic()
        label = self.context.normalize_label(pending_label) if pending_label else ""
        if not label and _is_token(children[0]) and children[0].type == "LABEL":
            label = self.context.normalize_label(children.pop(0))
        type = _token_lower(children.pop(0))
        values_node = None
        for item in children:
            if isinstance(item, lark.Tree):
                values_node = item
                break
        if values_node is None:
            values_node = lark.Tree(data="data", children=[])
        if values_node.data != "data":
            values = lark.Tree(data="data", children=values_node.children)
        else:
            values = values_node

        is_string = any("string" in expr.mods for expr in values.children if isinstance(expr, Expression) and expr.data == "expr") \
                    and not any(isinstance(expr, lark.Tree) and expr.data == "dupdir" for expr in values.children)

        self._clear_expression()
        return self.context.define_data(label, type, values, is_string=is_string, raw=get_raw(self.input_str, meta),
                                        line_number=get_line_number(meta))


    def segdir(self, nodes: list):
        segtype = nodes[-1] if nodes else ""
        logging.debug("segdir %s ~~", nodes)
        self.context.begin_simple_segment(_token_lower(segtype))
        self._clear_expression()
        return nodes


    def LABEL(self, value_in: lark.lexer.Token) -> lark.lexer.Token:
        value = self.context.resolve_label_for_expression(value_in, self.expression)
        logging.debug("name = %s", value)
        token = lark.Token("LABEL", value)
        if (g := self.context.lookup_global_symbol(value)) is None:
            # Handle dummy labels that haven't been added to symbol table yet
            # This can happen during parsing when dummy labels are referenced before they're defined
            logging.debug("Label %s not found in symbol table (may be dummy label)", value)
            # For dummy labels, just return the token without additional processing
        elif isinstance(g, op.Struct):
            logging.debug("get_size res %d", g.size)

        return token


    @v_args(meta=True)
    def segmentdir(self, meta, nodes):
        logging.debug("segmentdir %s ~~", nodes)

        name = self.context.normalize_label(nodes[0])
        opts = set()
        segclass = None
        """
        if options:
            for o in options:
                if isinstance(o, str):
                    opts.add(_token_lower(o))
                elif isinstance(o, lark.Tree) and o.data == 'label':
                    segclass = _token_lower(o.children[0])
                    if segclass[0] in ['"', "'"] and segclass[0] == segclass[-1]:
                        segclass = segclass[1:-1]
                else:
                    logging.warning('Unknown segment option')
        """
        self.context.begin_named_segment(name, options=opts, segclass=segclass, raw=get_raw(self.input_str, meta))
        self._clear_expression()
        return nodes

    def endsdir(self, nodes: list[lark.lexer.Token]) -> list[lark.lexer.Token]:
        logging.debug("ends %s ~~", nodes)
        self.context.end_current_scope()
        self._clear_expression()
        return nodes

    def poptions(self, options: list):
        self.context.set_pending_proc_options([str(item) for item in options])
        return Discard

    @v_args(meta=True)
    def procdir(self, meta, nodes):
        name, type = nodes[0], self.context.consume_pending_proc_options()
        logging.debug("procdir %s ~~", nodes)
        self.context.begin_procedure(name, type, line_number=get_line_number(meta),
                                     raw=get_raw_line(self.input_str, meta))
        self._expression = None
        return nodes

    def endpdir(self, nodes):
        name = nodes[0]
        logging.debug("endp %s ~~", name)
        self.context.end_procedure()
        return nodes


    @v_args(meta=True)
    def instrprefix(self, meta:     lark.tree.Meta, nodes: list[lark.Token]) -> _DiscardType:
        logging.debug("instrprefix %s ~~", nodes)
        instruction = str(nodes[0])
        self.context.dispatch_instruction(instruction, [], raw=get_raw_line(self.input_str, meta),
                                          line_number=get_line_number(meta))
        return Discard

    def mnemonic(self, name: list[lark.Token]) -> _DiscardType:
        self.context.set_pending_mnemonic(str(name[0]))
        return Discard

    def comment(self, children: list[lark.Token]) -> _DiscardType:
        text = "".join(str(i) for i in children).strip()
        if text:
            self.context.set_pending_source_comment(text)
        return Discard

    @v_args(meta=True)
    def instruction(self, meta:     lark.tree.Meta, nodes: list[Any | lark.Tree]) -> baseop | _DiscardType:
        logging.debug("asminstruction %s ~~", nodes)

        instruction = self.context.consume_pending_mnemonic()
        args = nodes[0].children if len(nodes) else []
        args = self.context.prepare_instruction_args(instruction, args)
        self._clear_expression()
        return self.context.dispatch_instruction(instruction, args, raw=get_raw_line(self.input_str, meta),
                                                 line_number=get_line_number(meta)) or Discard

    def enddir(self, children):
        logging.debug("end %s ~~", children)
        self.context.finish_program(children[0].children[0] if children else "")
        return children


    @property
    def expression(self) -> Expression:
        self._expression = self._expression or Expression()
        assert self._expression
        return self._expression

    def register(self, children: list[lark.Token]) ->     lark.Tree:
        reg = _token_lower(children[0])
        self.context.apply_register_reference(self.expression, reg)
        return Tree(data="register", children=[reg])  # Token('segmentregister', nodes[0].lower())

    def segmentregister(self, children: list[lark.Token]) ->     lark.Tree:
        reg = _token_lower(children[0])
        self.context.apply_segment_register_reference(self.expression, reg)
        return Tree(data="segmentregister", children=[reg])  # Token('segmentregister', nodes[0].lower())

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
        if _is_token(nodes[0]):  # for labels, not for memberdir
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
            if not self.context.is_lst_mode():  # not for IDA .lst
                string = string.replace("''", "'").replace('""', '"')  # masm behaviour
            self.expression.element_number = len(string)
            self.expression.element_size = 1
            self.expression.mods.add("string")
            nodes = lark.Token(type="STRING", value=string)
        return nodes  # Token('STRING', nodes)

    def structinstance(self, nodes: list[Any | lark.Tree]) -> list[Any | lark.Tree]: #, values):
        return nodes  # Token('structinstance', values)

    def memberdir(self, nodes: list[lark.Token]) ->     lark.Tree:
        return lark.Tree("memberdir", [self.context.normalize_label(str(node)) for node in nodes])

    def radixdir(self, children):
        self.context.set_radix(int(children[0]))
        return children


    def maked(self, nodes):
        # TODO dirty workaround for now
        if _token_lower(nodes[0]) == "size":
            return [f"sizeof({nodes[1].children.lower()})"]
        else:
            return nodes

    def offsetdirtype(self, nodes):
        directive = _token_lower(nodes[0])
        logging.debug("offsetdirtype %s", nodes)
        value = str(nodes[1].children[0]) if len(nodes)==2 else 2
        self.context.apply_offset_directive(directive, value)
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
    _PARSER_ENGINE_FORCE_POSTLEX = "postlex"
    _PARSER_ENGINE_FORCE_CYTHON = "cython"

    parser: Final[list] = []
    expr_parser: Final[list] = []
    _postlex: MatchTag | None = None
    _lexer_callback: MatchTag | None = None
    _lark_cython_plugins: Any | None = None
    _parser_engine: str | None = None
    start_parser: Final[list] = []
    instruction_parser: Final[list] = []
    equtype_parser: Final[list] = []
    insegdirlist_parser: Final[list] = []
    directivelist_parser: Final[list] = []
    @classmethod
    def _configured_parser_engine(cls) -> str:
        if cls._parser_engine is None:
            mode = os.getenv("MASM2C_PARSER_ENGINE", "").strip().lower()
            if mode in {"", "auto"}:
                cls._parser_engine = cls._PARSER_ENGINE_FORCE_POSTLEX
            elif mode in {"postlex", "python", "reference", "lalr", "lark"}:
                cls._parser_engine = cls._PARSER_ENGINE_FORCE_POSTLEX
            elif mode in {"cython", "lark-cython", "lark_cython", "lark-cy"}:
                cls._parser_engine = cls._PARSER_ENGINE_FORCE_CYTHON
            else:
                cls._parser_engine = "auto"
        return cls._parser_engine

    def __init__(self, context: "Parser") -> None:
        if self.parser:
            return

        logging.debug("Allocated LarkParser instance")

        file_name = f"{os.path.dirname(os.path.realpath(__file__))}/_masm61.lark"
        parser_engine = self.__class__._configured_parser_engine()
        debug = os.getenv("MASM2C_PARSER_DEBUG", "0").lower() in {"1", "true", "yes", "on"}

        if self.__class__._lark_cython_plugins is None and parser_engine != self._PARSER_ENGINE_FORCE_POSTLEX:
            try:
                from lark_cython import plugins as lark_cython_plugins  # type: ignore[import-not-found, import-untyped]
            except Exception:
                lark_cython_plugins = None
            self.__class__._lark_cython_plugins = lark_cython_plugins
            if parser_engine == self._PARSER_ENGINE_FORCE_CYTHON and lark_cython_plugins is None:
                raise RuntimeError("MASM2C_PARSER_ENGINE=cython requested but lark_cython is not installed")

        if self.__class__._postlex is None:
            self.__class__._postlex = MatchTag(context=context)
            self.__class__._lexer_callback = MatchTag(context=context)
        else:
            self.__class__._postlex.context = context
            if self.__class__._lexer_callback is not None:
                self.__class__._lexer_callback.context = context

        use_postlex = self.__class__._lark_cython_plugins is None or parser_engine == self._PARSER_ENGINE_FORCE_POSTLEX
        lark_kwargs = {
            "parser": "lalr",
            "propagate_positions": True,
            "cache": True,
            "debug": debug,
        }
        if use_postlex:
            lark_kwargs["start"] = [
                "start",
                "insegdirlist",
                "instruction",
                "expr",
                "equtype",
                "_directivelist",
            ]
        else:
            lark_kwargs["start"] = "start"
        if use_postlex:
            lark_kwargs["postlex"] = self.__class__._postlex
        else:
            assert self.__class__._lexer_callback is not None
            lark_kwargs["lexer_callbacks"] = {"LABEL": self.__class__._lexer_callback}
            lark_kwargs["_plugins"] = self.__class__._lark_cython_plugins
        with open(file_name) as gr:
            grammar = gr.read()
        self.parser.append(Lark(grammar, **lark_kwargs))
        if not use_postlex:
            def _build_expr_parser(start: str) -> None:
                start_kwargs = {
                    "parser": "lalr",
                    "propagate_positions": True,
                    "cache": True,
                    "debug": debug,
                    "start": start,
                    "postlex": self.__class__._postlex,
                }
                if start == "expr":
                    self.expr_parser.append(Lark(grammar, **start_kwargs))
                elif start == "instruction":
                    self.instruction_parser.append(Lark(grammar, **start_kwargs))
                elif start == "equtype":
                    self.equtype_parser.append(Lark(grammar, **start_kwargs))
                elif start == "insegdirlist":
                    self.insegdirlist_parser.append(Lark(grammar, **start_kwargs))
                elif start == "_directivelist":
                    self.directivelist_parser.append(Lark(grammar, **start_kwargs))
                else:
                    raise RuntimeError(f"unsupported cython helper start rule: {start}")

            for helper_start in ["expr", "instruction", "equtype", "insegdirlist", "_directivelist"]:
                _build_expr_parser(helper_start)

            fallback_kwargs = {
                "parser": "lalr",
                "propagate_positions": True,
                "cache": True,
                "debug": debug,
                "start": [
                    "start",
                    "insegdirlist",
                    "instruction",
                    "expr",
                    "equtype",
                    "_directivelist",
                ],
                "postlex": self.__class__._postlex,
            }
            self.start_parser.append(Lark(grammar, **fallback_kwargs))
            #print(sorted([term.pattern.value for term in cls._inst.or_parser.terminals if term.pattern.type == 'str']))

    def bind_context(self, context: "Parser") -> None:
        if self.__class__._postlex is not None:
            self.__class__._postlex.context = context
            self.__class__._postlex.last_type = ""
            self.__class__._postlex.last = ""
        if self.__class__._lexer_callback is not None:
            self.__class__._lexer_callback.context = context
            self.__class__._lexer_callback.last_type = ""
            self.__class__._lexer_callback.last = ""



class ExprRemover(Transformer):
    @v_args(meta=True)
    def expr(self, meta:     lark.tree.Meta, children: list[lark.Tree | lark.lexer.Token]) ->     lark.Tree:
        children = Token.remove_tokens(children, ["expr"])

        return Tree("expr", children, meta)

class IncludeLoader(Transformer):

    def __init__(self, context: "Parser") -> None:
        self.context = context

    def includedir(self, nodes):
        if isinstance(nodes, Tree):
            nodes = nodes.children
        name = nodes[0]
        while isinstance(name, Tree):
            name = name.children[0]
        name = str(name)
        name = name[1:-1] if name[0] == "<" and name[-1] == ">" else name
        return self.context.parse_include_directive(name)




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
            elif _is_token(node):
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
        except Exception:
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
            elif _is_token(node):
                if hasattr(self, node.type):
                    result += getattr(self, node.type)(node)
            elif isinstance(node, list):
                for i in node:
                    assert result is not None
                    result += self.visit(i)
            else:
                import logging
                logging.debug(f"Error unknown type {node} (may be dummy label)")
                assert self.init is not None
                return self.init
        except Exception as ex:
            import logging
            logging.debug(f"Exception processing node {node}: {ex}")
            assert self.init is not None
            return self.init
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
        return [lark.Token(type="LABEL", value=_token_lower(tree))]  # TODO HACK

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
