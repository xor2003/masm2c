.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT,ds:_TEXT

start proc near
    mov word ptr ds:[2], 1234h
    mov word ptr ds:[80h], 5678h

    mov dx, 222h
    mov ah, 26h
    int 21h

    mov ax, 222h
    mov es, ax

    mov al, 1
    cmp word ptr es:[2], 1234h
    jne failure

    mov al, 2
    cmp word ptr es:[80h], 5678h
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
