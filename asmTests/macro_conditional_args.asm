.386p

EMIT    MACRO   A,B,C,D
        DB      A
IFNB    <B>
        DB      B
ENDIF
IFNB    <D>
        DB      C
        DB      D
ENDIF
IFB     <D>
 IFNB   <C>
        DB      C
 ENDIF
ENDIF
ENDM

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

jmp exitLabel
EMIT 2

exitLabel:
xor al, al
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
