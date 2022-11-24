import json
from pprint import pprint

import jsonpickle
from lark import Lark, Transformer, Discard, v_args, Tree

from masm2c.Token import Token

with open('masm2c/_masm61.lark') as g:
    l = Lark(g, parser='lalr', propagate_positions=True, debug=True)  # , keep_all_tokens=True)

t = l.parse(""".386p

_DATA   segment use16 word public 'DATA' ;IGNORE
var1 db 2
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start:
mov ax,'Z' - 'A' + 1 ;coment
;inc bx
;lahf
add word ptr [var1-2],3+5*5
add word ptr [var1+3],5+5
mov bl,-3
mov cl,+5

_TEXT   ends ;IGNORE

end start ;IGNORE
""")


class ExprRemover(Transformer):
    @v_args(meta=True)
    def expr(self, meta, children):
        children = Token.remove_tokens(children, 'expr')

        return Tree('expr', children, meta)


e = ExprRemover()
t = e.transform(t)

print(t)
print(t.pretty())


class Tr(Transformer):

    def asminstruction(self, nodes):
        print(jsonpickle.dumps(nodes, indent=2))
        return nodes

    # def expr(self, nodes):
    #    print(nodes)
    #    return nodes


print(Tr().transform(t))
