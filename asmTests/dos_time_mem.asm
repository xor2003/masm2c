.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov ah, 2ah
int 21h
cmp cx, 1980
mov al, 1
jb failure
cmp dh, 1
mov al, 2
jb failure
cmp dh, 12
mov al, 3
ja failure
cmp dl, 1
mov al, 4
jb failure
cmp dl, 31
mov al, 5
ja failure

mov cx, 2026
mov dh, 6
mov dl, 20
mov ah, 2bh
int 21h
cmp al, 0
mov al, 6
jne failure

mov ch, 4
mov cl, 5
mov dh, 6
mov dl, 7
mov ah, 2dh
int 21h
cmp al, 0
mov al, 7
jne failure

mov ah, 2ch
int 21h
cmp ch, 23
mov al, 8
ja failure
cmp cl, 59
mov al, 9
ja failure
cmp dh, 59
mov al, 10
ja failure

mov ax, 1234h
mov es, ax
mov bx, 10h
mov ah, 4ah
int 21h
mov al, 11
jc failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
