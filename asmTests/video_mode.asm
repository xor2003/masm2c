.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov ax, 13h
int 10h

mov ah, 0fh
int 10h
cmp al, 13h
mov al, 1
jne failure
cmp ah, 80
mov al, 2
jne failure
cmp bh, 0
mov al, 3
jne failure

mov dx, 3c4h
mov al, 2
out dx, al
inc dx
in al, dx
cmp al, 0fh
mov al, 4
jne failure

dec dx
mov al, 4
out dx, al
inc dx
in al, dx
cmp al, 0eh
mov al, 5
jne failure

mov dx, 3ceh
mov al, 5
out dx, al
inc dx
in al, dx
cmp al, 40h
mov al, 6
jne failure

mov ax, 3
int 10h

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
