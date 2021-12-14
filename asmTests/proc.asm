.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

xor eax,eax
xor edx,edx
xor ebx,ebx
xor ecx,ecx

inc ebx
call incebx
inc ecx
inc ecx
call aincecx

mov al,1
cmp edx,1
jne failure

mov al,2
cmp ecx,3
jne failure

mov al,3
cmp ebx,3
jne failure

mov al,4
call aa
cmp ebx,4
jne failure


mov al,0
JMP exitLabel
;mov edx,offset exitLabel

MOV al,0
JMP exitLabel
failure:
;mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
start endp

incebx proc near
inc ebx
cmp ebx,TWO
je ok
ret
ok:
inc ebx
ret
inceBX endp

aincecx proc near
inc ecx
call aincedx
tWO equ 2
ret
aincecx endp

aincedx proc near
inc edx
ret
aincedx endp

aa proc near
mov ebx,555
aa endp

bb proc near
mov ebx,4
ret
bb endp


_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?) ;IGNORE
stackseg   ends ;IGNORE

end start ;IGNORE
