.386p
.intel_syntax noprefix

TXT TEXTEQU <HELLO>

SETAL MACRO value
    mov al,value
ENDM

PAIR struc
    lo db ?
    hi db ?
PAIR ends

HATCH4 RECORD C3:2,C2:2,C1:2,C0:2

_DATA   segment use16 word public 'DATA' ;IGNORE
pair_labeled PAIR <1, 2>
PAIR <3, 4>
pal HATCH4 <0, 1, 2, 3>
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

push seg _DATA
pop ds

cmp pair_labeled.lo, 1
jne failure
cmp pair_labeled.hi, 2
jne failure

cmp pal, 27
jne failure

mov al,0
REPT 3
inc al
ENDM
cmp al,3
jne failure

macro_label: SETAL 6
cmp al,6
jne failure

jmp after_mov
mov:
mov al,1
jmp failure
after_mov:

mov al,0
jmp exitLabel
failure:
mov al,1

exitLabel:
mov ah,4ch
int 21h
start endp

_TEXT   ends ;IGNORE

ADDRMAC MACRO ADDR:=<0>
macro_data db 0
UNKNOWN_MACRO_OPCODE ADDR
ENDM

EMPTYMAC MACRO reg
    IFIDNI <reg>,<zz>
    nop
    ENDIF
ENDM

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?) ;IGNORE
stackseg   ends ;IGNORE

end start ;IGNORE
