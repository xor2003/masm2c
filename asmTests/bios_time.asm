.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

xor ah, ah
int 1ah
mov al, 1
jc failure

mov ah, 02h
int 1ah
mov al, 2
jc failure
cmp ch, 23h
mov al, 3
ja failure
cmp cl, 59h
mov al, 4
ja failure
cmp dh, 59h
mov al, 5
ja failure

mov ah, 04h
int 1ah
mov al, 6
jc failure
cmp ch, 20h
mov al, 7
jb failure
cmp dh, 1
mov al, 8
jb failure
cmp dh, 12h
mov al, 9
ja failure
cmp dl, 1
mov al, 10
jb failure
cmp dl, 31h
mov al, 11
ja failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
