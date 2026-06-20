.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov ax, _TEXT
mov ds, ax

mov ax, 3533h
int 21h
mov ax, es
or ax, bx
jz failure

xor ax, ax
int 33h
cmp ax, 0ffffh
jne failure
cmp bx, 2
jb failure

mov ax, 4
mov cx, 100
mov dx, 50
int 33h

mov ax, 3
int 33h
cmp cx, 100
jne failure
cmp dx, 50
jne failure

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
