.386p

CSEG segment use16 word public 'CODE' ;IGNORE
assume cs:CSEG,ds:DSEG

DSEG segment use16 word public 'DATA' ;IGNORE
value db 2
DSEG ends ;IGNORE

constval = 2

start proc near
mov al, value
cmp al, constval
mov al, 1
jne failure

xor al, al

failure:
mov ah, 4ch
int 21h

start endp
CSEG ends ;IGNORE

end start ;IGNORE
