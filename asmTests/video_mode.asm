.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov ax, 13h
int 10h

mov ah, 0fh
int 10h
cmp al, 13h
jne failure
cmp ah, 80
jne failure
cmp bh, 0
jne failure

mov ax, 3
int 10h

xor al, al
jmp exitLabel

failure:
mov al, 1

exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
