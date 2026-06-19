.386
;extern va1: byte
_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
org 100h
start:

mov ax,seg _DATA
mov ds,ax
cmp byte ptr [var1],2
jne failure

MOV al,0
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h

_TEXT   ends ;IGNORE

_DATA   segment use16 word public 'DATA' ;IGNORE
var1 db 2
_DATA   ends ;IGNORE


end start ;IGNORE
