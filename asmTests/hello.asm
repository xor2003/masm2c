.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
_msg    db 'Hello World!',13,10,'$'

_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
  assume  cs:_TEXT,ds:_DATA
start proc near



sti                             ; Set The Interrupt Flag
cld                             ; Clear The Direction Flag

mov cx,0
;div cx

push _data
pop ds
mov ah,9                        ; AH=09h - Print DOS Message
mov dx,offset _msg             ; DS:EDX -> $ Terminated String
int 21h                         ; DOS INT 21h

; weird test...
mov ebx,-1
mov bl,0
cmp ebx,0ffffff00h
jne failure

xor eax,eax
jmp exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h                     ; DOS INT 21h
start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
