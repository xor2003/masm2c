.386p

.RADIX 8

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov al, 10
cmp al, 8D
mov al, 1
jne failure

.RADIX 10
mov bl, 10
cmp bl, 10
mov al, 2
jne failure

xor al, al

failure:
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
