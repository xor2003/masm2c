.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT

emit_msg macro name
    %OUT +++ Undefined reserved word - &name
endm

start proc near
emit_msg AUTO
xor al, al
mov ah, 4ch
int 21h
start endp

_TEXT   ends ;IGNORE

end start ;IGNORE
