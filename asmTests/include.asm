.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near


mov eax,1

     include  <included.inc>    ; OKOK

failure:
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
