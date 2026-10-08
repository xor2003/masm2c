.386p

_DATA   segment use16 word public 'DATA'
dest dw 0
source dw 1234h
_DATA   ends

_TEXT   segment use16 word public 'CODE'
assume  cs:_TEXT,ds:_DATA
start proc near

push _DATA
pop ds
push _DATA
pop es

cld
mov si,offset source
mov di,offset dest
movs word ptr [es:di],word ptr source

mov al,1
cmp dest,1234h
jne failure
mov al,2
cmp si,offset source+2
jne failure
mov al,3
cmp di,offset dest+2
jne failure

mov si,offset source
xor ax,ax
lods word ptr source
mov bl,4
cmp ax,1234h
jne failure_bl
mov bl,5
cmp si,offset source+2
jne failure_bl

xor al,al
jmp exitLabel

failure:
failure_bl:
mov al,bl
exitLabel:
mov ah,4ch
int 21h
start endp

_TEXT   ends

end start
