.386p

_TEXT segment use16 word public 'CODE' ;IGNORE
assume cs:_TEXT
start proc near

mov dx, 0
mov al, 0
out dx, al
mov al, 40h
out dx, al
mov al, 0ffh
out dx, al

mov dx, 64h
mov al, 0ffh
out dx, al
in al, dx
cmp al, 0
mov al, 1
jne failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT ends ;IGNORE

end start ;IGNORE
