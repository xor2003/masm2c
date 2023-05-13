from collections.abc import Iterator

import jsonpickle

from lark import Lark, Transformer, Tree, lark, v_args
from masm2c.Token import Token


class MatchTag:
    always_accept = "LABEL", "STRUCTHDR"

    def __init__(self) -> None:
        self.last_type = None
        self.last = None

    def process(self, stream: Iterator[lark.Token]) -> Iterator[lark.Token]:
        for t in stream:
            if t.type == "LABEL":
                if t.value == 'struc':
                    t.type = "STRUCTHDR"
                elif t.value == 'ends':
                    t.type = "endsdir"
            #if t.type == "STRUCTHDR":
            if self.last_type == 'LABEL' and t.type == "LABEL" and t.value == 'VECTOR':
                t.type = "STRUCTNAME"
            self.last_type = t.type
            self.last = t.value
            yield t

with open('masm2c/_masm61.lark') as g:
    l = Lark(g, parser='lalr', propagate_positions=True, debug=True,
             postlex=MatchTag())  # , keep_all_tokens=True)

"""
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

 var_transshape = TRANSFORMEDSHAPE ptr -50
"""
t = l.parse(""".386p
a = byte ptr -50
b = -50
d equ 8


_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start:
call    dword ptr [ebx-4]
shr     dx, cl
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


print(Tr().transform(t))
