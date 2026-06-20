.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
key db 128 dup(0)
ticker dw 0
frames dw 0
countdown dw 3
elapsedtime dd 0
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

mov ax, _DATA
mov ds, ax
mov dx, offset dummy_timer
mov ax, 2508h
int 21h

mov ecx, 5000000
waitLoop:
cmp frames, 2
jae success
loop waitLoop
mov al, 1
jmp failure

success:
cmp ticker, 2
mov al, 2
jb failure
cmp elapsedtime, 2
mov al, 3
jb failure
cmp countdown, 3
mov al, 4
jae failure
xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

dummy_timer proc near
iret
dummy_timer endp

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
