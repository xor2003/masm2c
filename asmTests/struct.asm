.286
.model medium

GAMEINFO struc
    game_opponentcarid db 4 dup (?)
    game_opponenttype dw ?
GAMEINFO ends

VECTOR struc
    vx dw ?
    vy dw ?
    vz dw ?
VECTOR ends

TRANSFORMEDSHAPE struc
    ts_shapeptr dw ?
    ts_rectptr dw ?
    ts_rotvec VECTOR <?, ?, ?>
TRANSFORMEDSHAPE ends

var_transshape = TRANSFORMEDSHAPE ptr -50


_DATA   segment use16 word public 'DATA' ;IGNORE
gameconfig GAMEINFO < <1>, 5 >

ts TRANSFORMEDSHAPE < 6, 7, <8> >
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near


sti                             ; Set The Interrupt Flag
cld                             ; Clear The Direction Flag

MOV ax, _data
MOV ds, ax

t equ -2

mov al,1
cmp gameconfig.game_opponenttype, 5
jne failure

mov al,2
mov bx, offset gameconfig.game_opponenttype+t
cmp bx, (offset gameconfig.game_opponenttype-2)
jne failure

mov bx,-4
mov al,3
cmp[bx + ts.ts_rotvec.vz], 8
jne failure

;mov bp, -4
;mov al,4
;cmp[bp + var_transshape.ts_rotvec.vz], 3
;jne failure

MOV al,0
JMP exitLabel
failure:
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h
start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
