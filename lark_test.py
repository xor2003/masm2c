import json
from pprint import pprint
from typing import Iterator

import jsonpickle
from lark import Lark, Transformer, Discard, v_args, Tree, logger, lark

import logging

import masm2c
from masm2c.Token import Token


#logger.setLevel(logging.DEBUG)
class MatchTag:
    always_accept = "LABEL", "STRUCTHDR"

    def __init__(self):
        self.last_type = None
        self.last = None

    def process(self, stream: Iterator[lark.Token]) -> Iterator[lark.Token]:
        for t in stream:
            if t.type == "LABEL" and t.value == 'struc':
                #print(1, self.last_type, self.last, t)
                t.type = "STRUCTHDR"
            #if t.type == "STRUCTHDR":
            #    print(2, t)
            #    print(self.last)
            if self.last_type == 'LABEL' and t.type == "LABEL" and t.value == 'VECTOR':
                #print(3, t)
                t.type = "STRUCTNAME"
            self.last_type = t.type
            self.last = t.value
            yield t

with open('masm2c/_masm61.lark') as g:
    l = Lark(g, parser='lalr', propagate_positions=True, debug=True,
             postlex=MatchTag())  # , keep_all_tokens=True)

''' 
'''
t = l.parse(""".386p
VECTOR struc
    vx dw ?
 VECTOR ends
 
 TRANSFORMEDSHAPE struc
    ts_shapeptr dw ?
    ts_rectptr dw ?
    ;ts_rOTvec VECTOR <>
    ;ts_vec VECTOR 3 dup (<>)
 TRANSFORMEDSHAPE ends
 var_transshape = TRANSFORMEDSHAPE ptr -50
 
GAMEINFO struc
game_opponenttype dw ?
game_opponentmaterial dd ?
game_opponentcarid db 4 dup (?)
GAMEINFO ends
extrn gameconfig:GAMEINFO


 var_transshape = TRANSFORMEDSHAPE ptr -50


_DATA   segment use16 word public 'DATA' ;IGNORE
head db '^',10,10
var3 db 5*5 dup (0)
var3 db 5*5 dup (0,testEqu*2,2*2*3,3)
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
