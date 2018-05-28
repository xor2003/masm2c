.386p

_DATA   segment use32 dword public 'DATA' ;IGNORE
_DATA   ends ;IGNORE

_TEXT   segment use32 dword public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
_start proc near
start: ;IGNORE


mov edx,2
neg edx
jnC failure

cmp edx,-2
jne failure

xor ebx,ebx
neg ebx
jc failure

mov eax,011111111111111111111111111111111b
not eax
cmp eax,0
jne failure

mov eax,0
mov ax,01111111111111111b
not ax
cmp eax,0
jne failure

mov eax,0
mov ax,01010101010101010b
not ax
cmp eax,0101010101010101b
jne failure
;;;;;;
mov eax,0
cbw
cmp eax,0                
jne failure

mov eax,-5
cbw
cmp eax,-5                
jne failure

mov eax,0
mov al,-5
cbw
cmp ax,-5                
jne failure

mov eax,0ffffff03h
cbw
cmp eax,0ffff0003h
jne failure

mov eax,0ffff00f3h
cbw
cmp eax,0fffffff3h
jne failure
;;;;;;
mov eax,0
mov edx,0
cwd
cmp eax,0                
jne failure
cmp edx,0                
jne failure

mov eax,-5
mov edx,0
cwd
cmp eax,-5
jne failure
cmp edx,0ffffh
jne failure

mov eax,0ffffff03h
mov edx,0
cwd
cmp eax,0ffffff03h
jne failure
cmp edx,0ffffh
jne failure

mov eax,0ffff00f3h
mov edx,0
cwd
cmp eax,0ffff00f3h
jne failure
cmp edx,0
jne failure
;;;;;
mov eax,0
cwde
cmp eax,0                
jne failure

mov eax,-5
cwde
cmp eax,-5                
jne failure

mov eax,0ffffff03h
cwde
cmp eax,0ffffff03h
jne failure

mov eax,0ffff00f3h
cwde
cmp eax,000f3h
jne failure
;;;;;;

clc
jc failure

stc
jnc failure

clc
cmc
jnc failure
cmc
jc failure

xor eax,eax
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h

_start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE

