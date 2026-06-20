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
mov al, 1
jz failure

xor ax, ax
int 33h
cmp ax, 0ffffh
mov al, 2
jne failure
cmp bx, 2
mov al, 3
jb failure

mov ax, 1000h
mov bx, 55aah
int 33h
cmp ax, 1000h
mov al, 4
jne failure
cmp bx, 55aah
mov al, 5
jne failure

mov ax, 4
mov cx, 100
mov dx, 50
int 33h

mov ax, 3
int 33h
cmp cx, 100
mov al, 6
jne failure
cmp dx, 50
mov al, 7
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
