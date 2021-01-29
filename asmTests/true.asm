_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT
start proc near

MOV     AX,4C00h
INT     21h
start endp

_TEXT   ends ;IGNORE

end start ;IGNORE
