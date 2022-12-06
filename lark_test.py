import json
from pprint import pprint

import jsonpickle
from lark import Lark, Transformer, Discard, v_args, Tree, logger

from masm2c.Token import Token
import logging

#logger.setLevel(logging.DEBUG)

with open('masm2c/_masm61.lark') as g:
    l = Lark(g, parser='lalr', propagate_positions=True, debug=True)  # , keep_all_tokens=True)

t = l.parse(""".386p

_DATA   segment use16 word public 'DATA' ;IGNORE
db 88h,3 dup(0),87h
_dword_1DCEC	dd 10524E49h		; DATA XREF: _loadcfg+1Ar
var1 db 2.3E+4
ASCII DB '00000000',0Dh,0Ah,'$' ; buffer for ASCII string
_a070295122642\tdb '07/02/95 12:26:42',0 ; DATA XREF: seg003:off_2462E\x19o
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start:
mov ax,'Z' - 'A' + 1 ;coment
;inc bx
;lahf
add word ptr [var1-2],3h+5o*5
add eax, large ds:4000h
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
