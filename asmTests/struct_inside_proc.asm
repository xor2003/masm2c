.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT

start proc near
local_struct struc
    first dw ?
    second db ?
local_struct ends

rows local_struct <1234h, 56h>
     local_struct <789Ah, 0BCh>

mov ax, cs:local_struct.first[si]
mov al, 0
mov ah, 4ch
int 21h
start endp

_TEXT ends ;IGNORE
end start ;IGNORE
