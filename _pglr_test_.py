#!/usr/bin/python3
import os
import re
import sys

from parglare import Grammar

macronames = []
structnames = []
macronamere = re.compile(r"([A-Za-z@_\$\?][A-Za-z@_\$\?0-9]*)")
commentid = re.compile(r"COMMENT\s+([^ ]).*?\1[^\r\n]*", flags=re.DOTALL)

def macro_action(context, nodes, name):
    macronames.insert(0, name.lower())
    print(f"added ~~{name}~~")
    return nodes


def macroname(head, input, pos):
    if not (mtch := macronamere.match(input[pos:])):
        return None
    result = mtch.group().lower()
    if result not in macronames:
        return None
    print(f"matched ~^~{result}~^~ in macronames")
    return result



class Token:

    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        from pprint import pformat
        return pformat(vars(self))


def get_raw(context):
    return context.input_str[context.start_position: context.end_position]


"""
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
"""


def make_token(context, nodes):
    if len(nodes) == 1 and context.production.rhs[0].name not in (
            "type", "e01", "e02", "e03", "e04", "e05", "e06", "e07", "e08", "e09", "e10", "e11"):
        nodes = Token(context.production.rhs[0].name, nodes[0])
        print(f"mt~{nodes!s}~")
    if context.production.rhs[0].name in (
            "type", "e01", "e02", "e03", "e04", "e05", "e06", "e07", "e08", "e09", "e10", "e11"):
        nodes = nodes[0]
    return nodes


cur_segment = "ds"  # !
indirection = 0  # !


def segoverride(context, nodes):
    global cur_segment
    if isinstance(nodes[0], list):
        cur_segment = nodes[0][-1]
        return nodes[0][:-1] + [Token("segoverride", nodes[0][-1]), nodes[2]]
    cur_segment = nodes[0]  # !
    return [Token("segoverride", nodes[0]), nodes[2]]


def ptrdir(context, nodes):
    if len(nodes) == 3:
        return [Token("ptrdir", nodes[0]), nodes[2]]
    else:
        return [Token("ptrdir", nodes[0]), nodes[1]]


def includedir(context, nodes, name):
    print(name)
    return nodes


def asminstruction(context, nodes, instruction, args):
    global cur_segment
    global indirection
    print(
        f"instruction {get_raw(context)} {nodes!s} ~~ {cur_segment!s} {indirection!s}",
    )
    cur_segment = "ds"  # !
    indirection = 0  # !
    return nodes


def notdir(context, nodes):
    nodes[0] = "~"
    return nodes


def ordir(context, nodes):
    nodes[1] = "|"
    return nodes


def xordir(context, nodes):
    nodes[1] = "^"
    return nodes


def anddir(context, nodes):
    nodes[1] = " & "
    return nodes


def register(context, nodes):
    return Token("register", nodes[0].lower())


def segmentregister(context, nodes):
    return Token("segmentregister", nodes[0].lower())


def sqexpr(context, nodes):
    global indirection
    indirection = 1
    res = nodes[1]

    # if isinstance(res, list):
    return Token("sqexpr", res)


def offsetdir(context, nodes):
    # global indirection
    return Token("offsetdir", nodes[1])


def segmdir(context, nodes):
    # global indirection
    return Token("segmdir", nodes[1])


def instrprefix(context, nodes):
    print(f"instrprefix /~{nodes!s}" + "~\\")
    return nodes


def LABEL(context, nodes):
    return Token("LABEL", nodes)


def STRING(context, nodes):
    return Token("STRING", nodes)


def INTEGER(context, nodes):
    return Token("INTEGER", nodes)


def expr(context, nodes):
    return Token("expr", make_token(context, nodes))

def structname(head, s, pos):
    if not (mtch := macronamere.match(s[pos:])):
        return None
    result = mtch.group().lower()
    if result not in structnames:
        return None
    logging.debug(f" ~^~{result}~^~ in structnames")
    return result

def structdir(context, nodes, name, item):
    print("structdir", nodes)
    structnames.insert(0, name.children.lower())
    print(f"structname added ~~{name.children}~~")
    return []  # Token('structdir', nodes) TODO ignore by now

def structinstdir(context, nodes, label, type, values):
    print(f"structinstdir{label!s}{type!s}{values!s}")
    return nodes  # Token('structdir', nodes) TODO ignore by now


def memberdir(context, nodes, variable, field):
    result = Token("memberdir", [variable, field])
    print(result)
    return result

def commentkw(head, s, pos):
    return mtch.group(0) if (mtch := commentid.match(s[pos:])) else None

recognizers = {
    "macroname": macroname,
    "structname": structname,
    "COMMENTKW": commentkw,
}

actions = {
    "field": make_token,
    "memberdir": memberdir,
    "structinstdir": structinstdir,
    "expr": expr,
    "structinstance": make_token,
    "structdir": structdir,
    "includedir": includedir,
    "instrprefix": instrprefix,
    "macrodir": macro_action,
    "asminstruction": asminstruction,
    "STRING": STRING,
    "LABEL": LABEL,
    "INTEGER": INTEGER,
    "aexpr": make_token,
    "cexpr": make_token,
    "cxzexpr": make_token,
    "flagname": make_token,
    "primary": make_token,
    "recordconst": make_token,
    "simpleexpr": make_token,
    "sizearg": make_token,
    "term": make_token,
    "segoverride": segoverride,
    "ptrdir": ptrdir,
    "offsetdir": offsetdir,
    "segmdir": segmdir,
    "register": register,
    "segmentregister": segmentregister,
    "sqexpr": sqexpr,
    "notdir": notdir,
    "ordir": ordir,
    "xordir": xordir,
    "anddir": anddir,
}

file_name = f"{os.path.dirname(os.path.realpath(__file__))}/masm2c/_masm61.pg"
grammar = Grammar.from_file(file_name, ignore_case=True, recognizers=recognizers)

from parglare import Parser

parser = Parser(grammar, debug=True, actions=actions, debug_colors=True)

codeset = "cp437"

if sys.version_info[0] >= 3:
    sys.stdout.reconfigure(encoding="utf-8")

for i in sys.argv[1:]:

    with open(i, encoding=codeset) as f:
        input_str = f.read()

        result = parser.parse(input_str, file_name=file_name)
    from pprint import pprint

    pprint(result)
