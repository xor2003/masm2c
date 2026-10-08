_TEXT segment use16 word public 'CODE'
assume cs:_TEXT,ds:_TEXT,ss:_TEXT
org 100h

start proc near
    mov dl,'A'
    mov ah,06h
    int 21h
    cmp al,'A'
    jne fail

    mov dl,0ffh
    mov ah,06h
    int 21h
    jnz fail

    mov ax,4c00h
    int 21h

fail:
    mov ax,4c01h
    int 21h
start endp

_TEXT ends
end start
