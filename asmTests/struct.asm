.286
.model tiny

e struc
    ddd dw ?
    f dw ?
e ends


b struc
    gogo e <?,?>
    aa db ?
b ends

GAMEINFO struc
    a db ?
    game_opponentcarid db 4 dup (?)
    d b <<?,?>,?>
    game_opponenttype dw ?
GAMEINFO ends

VECTOR struc
    vx dw ?
    vy dw ?
    vz dw ?
VECTOR ends

TRANSFORMEDSHAPE struc
    ts_shapeptr db ?
    ts_rotvec VECTOR <?, ?, ?>
    ts_rectptr db ?
TRANSFORMEDSHAPE ends

;var_transshape = TRANSFORMEDSHAPE ptr -50

_TEXT   segment public 'CODE' ;IGNORE
assume  ds:_TEXT
start proc near


gameconfig GAMEINFO < 0, <1>, <<2,3>,4>, 5>
db 0ffh
ts TRANSFORMEDSHAPE < 6, <7, 8, 9>, 10 >

fff e <>


sti                             ; Set The Interrupt Flag
cld                             ; Clear The Direction Flag

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
;cmp[bx + ts.ts_rotvec.vz], 8
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
