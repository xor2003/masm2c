.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA

start proc near



xor edx,edx
mov ecx,10
toto:
INC edx
loop toto

cmp edx,10
jne failure

xor edx,edx
mov ecx,10
toto1:
INC edx
sub eax,eax
loope toto1

cmp edx,10
jne failure

xor edx,edx
mov ecx,10
toto2:
INC edx
sub eax,eax
inc eax
loope toto2

cmp edx,1
jne failure


MOV al,0
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h

start endp

_TEXT   ends ;IGNORE



stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?) ;IGNORE
stackseg   ends ;IGNORE

end start ;IGNORE
