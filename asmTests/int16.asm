.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT,ds:_TEXT

start proc near
    mov ah, 01h
    int 16h
    mov al, 1
    jnz failure

    mov cx, 1e41h
    mov ah, 05h
    int 16h
    cmp al, 0
    mov al, 2
    jne failure

    mov ah, 01h
    int 16h
    mov bx, ax
    mov al, 3
    jz failure
    cmp bx, 1e41h
    mov al, 4
    jne failure

    mov ah, 00h
    int 16h
    cmp ax, 1e41h
    mov al, 5
    jne failure

    mov ah, 01h
    int 16h
    mov al, 6
    jnz failure

    xor al, al
    jmp exitLabel

failure:
exitLabel:
    mov ah, 4ch
    int 21h
start endp

_TEXT ends
end start
