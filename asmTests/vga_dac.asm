.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov dx, 3c8h
mov al, 12h
out dx, al
inc dx
mov al, 11h
out dx, al
mov al, 22h
out dx, al
mov al, 33h
out dx, al

mov dx, 3c7h
mov al, 12h
out dx, al
mov dx, 3c9h
in al, dx
cmp al, 11h
mov al, 1
jne failure
in al, dx
cmp al, 22h
mov al, 2
jne failure
in al, dx
cmp al, 33h
mov al, 3
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
