.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT

ORG 0+20O
db 90h
ORG $-1

start proc near
xor al, al
mov ah, 4ch
int 21h
start endp

_TEXT   ends ;IGNORE

end start ;IGNORE
