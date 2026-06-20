.386p

_TEXT segment use16 word public 'CODE' ;IGNORE
assume cs:_TEXT
start proc near

mov al, 55h
mov ah, 14h
stc
int 80h
mov al, 1
jc failure
cmp al, 55h
mov al, 2
je failure

mov al, 55h
mov ah, 05h
stc
int 81h
mov al, 3
jc failure
cmp al, 55h
mov al, 4
je failure

mov al, 7
mov ah, 4
stc
int 80h
mov al, 5
jc failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT ends ;IGNORE

end start ;IGNORE
