.386p

_DATA   segment use16 word public 'DATA'
_DATA   ends

_TEXT   segment use16 word public 'CODE'
assume  cs:_TEXT,ds:_DATA
start proc near

xor ax,ax
mov ah,4ch
int 21h
start endp

end start
