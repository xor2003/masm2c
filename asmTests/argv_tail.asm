.386p

_TEXT segment use16 word public 'CODE' ;IGNORE
assume cs:_TEXT
start proc near

xor ax, ax
mov ds, ax

mov al, 1
cmp byte ptr ds:[80h], 9
jne failure

mov al, 2
cmp byte ptr ds:[81h], ' '
jne failure
mov al, 3
cmp byte ptr ds:[82h], 'S'
jne failure
mov al, 4
cmp byte ptr ds:[83h], 'N'
jne failure
mov al, 5
cmp byte ptr ds:[84h], ' '
jne failure
mov al, 6
cmp byte ptr ds:[85h], 'M'
jne failure
mov al, 7
cmp byte ptr ds:[86h], 'N'
jne failure
mov al, 8
cmp byte ptr ds:[87h], ' '
jne failure
mov al, 9
cmp byte ptr ds:[88h], 'Q'
jne failure
mov al, 10
cmp byte ptr ds:[89h], 'S'
jne failure
mov al, 11
cmp byte ptr ds:[8ah], 0dh
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
