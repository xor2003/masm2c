.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov dx, 3dah
in al, dx

mov dx, 3c0h
mov al, 12h
out dx, al
mov al, 34h
out dx, al

mov dx, 3dah
in al, dx

mov dx, 3c0h
mov al, 12h
out dx, al
mov dx, 3c1h
in al, dx
cmp al, 34h
mov al, 1
jne failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
