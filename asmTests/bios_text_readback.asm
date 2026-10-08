.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

start proc near
    mov ax, 0003h
    int 10h

    mov ah, 02h
    mov bh, 00h
    mov dh, 04h
    mov dl, 07h
    int 10h

    mov ah, 09h
    mov al, 'Z'
    mov bh, 00h
    mov bl, 1Eh
    mov cx, 1
    int 10h

    mov ah, 02h
    mov bh, 00h
    mov dh, 04h
    mov dl, 07h
    int 10h

    mov ah, 08h
    mov bh, 00h
    int 10h

    cmp al, 'Z'
    jne failure
    cmp ah, 1Eh
    jne failure

    mov al, 0
    jmp exitLabel

failure:
    mov al, 1

exitLabel:
    mov ah, 4ch
    int 21h
start endp

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
