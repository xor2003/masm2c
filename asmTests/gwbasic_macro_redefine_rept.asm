.386p

_DATA segment use16 word public 'DATA'
NMLPT=3
NUM=377O

NDEV MACRO NAM,N
    DEV NAM&N
ENDM

NAMES MACRO
    DEV KYBD
    NLPT=0
REPT NMLPT
    NLPT=NLPT+1
    NDEV LPT,%NLPT
ENDM
ENDM

DEV MACRO NAM
    PUBLIC $_&NAM
    $_&NAM=NUM
    DB "&NAM&"
    DB OFFSET NUM
    NUM=NUM-1
ENDM

table:
    NAMES
    DB 0

DEV MACRO NAM
    DB OFFSET $_&NAM
ENDM

ids:
    NAMES

_DATA ends

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT, ds:_DATA

start:
    mov ax, _DATA
    mov ds, ax

    mov si, OFFSET table
    cmp byte ptr [si+0], 'K'
    jne failure
    cmp byte ptr [si+4], 377O
    jne failure
    cmp byte ptr [si+5], 'L'
    jne failure
    cmp byte ptr [si+8], '1'
    jne failure
    cmp byte ptr [si+9], 376O
    jne failure
    cmp byte ptr [si+13], '2'
    jne failure
    cmp byte ptr [si+14], 375O
    jne failure
    cmp byte ptr [si+19], 374O
    jne failure

    mov si, OFFSET ids
    cmp byte ptr [si+0], 377O
    jne failure
    cmp byte ptr [si+1], 376O
    jne failure
    cmp byte ptr [si+2], 375O
    jne failure
    cmp byte ptr [si+3], 374O
    jne failure

    mov al, 0
    jmp exitLabel

failure:
    mov al, 1

exitLabel:
    mov ah, 4ch
    int 21h

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
