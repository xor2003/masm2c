.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov dx, 3c4h
mov al, 4
out dx, al
inc dx
mov al, 6
out dx, al
in al, dx
cmp al, 6
mov al, 1
jne failure

mov dx, 3ceh
mov al, 5
out dx, al
inc dx
mov al, 40h
out dx, al
in al, dx
cmp al, 40h
mov al, 2
jne failure

mov dx, 3d4h
mov al, 9
out dx, al
inc dx
mov al, 31h
out dx, al
in al, dx
cmp al, 31h
mov al, 3
jne failure

mov dx, 61h
mov al, 3
out dx, al
in al, dx
cmp al, 3
mov al, 4
jne failure

mov dx, 40h
mov al, 34h
out dx, al
in al, dx
cmp al, 34h
mov al, 5
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
