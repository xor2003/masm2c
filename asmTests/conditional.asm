.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start:

mov al,0

IFNB <VALUE>
mov bl,1
ELSE
mov bl,2
ENDIF
cmp bl,1
jne failure

IFIDNI <Abc>,<aBC>
mov bh,3
ELSE
mov bh,4
ENDIF
cmp bh,3
jne failure

IFDIF <LEFT>,<RIGHT>
mov cl,5
ELSE
mov cl,6
ENDIF
cmp cl,5
jne failure

IFB <>
mov dl,7
ELSE
mov dl,8
ENDIF
cmp dl,7
jne failure

jmp exitLabel

failure:
mov al,1

exitLabel:
mov ah,4ch
int 21h

_TEXT   ends ;IGNORE

stackseg segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg ends ;IGNORE

end start ;IGNORE
