_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT,ss:_TEXT
org 100h
start proc near

MOV     AH,4Dh
INT     21h
mov ah,0

    mov     bx,10          ;CONST
    xor     cx,cx          ;Reset counter
a: xor     dx,dx          ;Setup for division DX:AX / BX
    div     bx             ; -> AX is Quotient, Remainder DX=[0,9]
    push    dx             ;(1) Save remainder for now
    inc     cx             ;One more digit
    test    ax,ax          ;Is quotient zero?
    jnz     a             ;No, use as next dividend
b: pop     dx             ;(1)
    add     dl,"0"         ;Turn into character [0,9] -> ["0","9"]
    mov     ah,02h         ;DOS.DisplayCharacter
    int     21h            ; -> AL
    loop    b

    mov     dl,0dh
    mov     ah,02h         ;DOS.DisplayCharacter
    int     21h            ; -> AL
    mov     dl,0ah
    mov     ah,02h         ;DOS.DisplayCharacter
    int     21h            ; -> AL

MOV     AH,4Ch
INT     21h
start endp

_TEXT   ends ;IGNORE

end start ;IGNORE
