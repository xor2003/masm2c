.386p

DATASEG segment use16 word public 'DATA'
marker db 7
DATASEG ends

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT, ds:DATASEG

start proc near
mov ax, DATASEG
mov ds, ax

mov bx, SEG marker
mov es, bx
mov si, OFFSET marker
mov al, es:[si]
cmp al, 7
mov al, 1
jne failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT ends

end start
