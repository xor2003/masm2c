.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
a db 0ffh,0dfh,0h
b db 2

_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near
_start: ;IGNORE

mov ax,2
jmp [cs:table+ax]
jmp failure

@df@@@@8:

mov ax,3
call [cs:table+ax]
jmp next
@df@@@@9:
ret

next:

mov eax,-1
test eax,eax
js @df@@@@
@df@@@@:
jns failure

xor eax,eax
js failure

mov ax,-1
test ax,ax
jns failure

mov al,[a]
mov bl,[a+1]
cmp bl,al
ja failure


mov bl,192
cmp bl,192
jb failure

cmp bl,193
jnb failure

mov dx,-1
cmp dx,0
jns failure

mov dx,1
cmp dx,0
js failure


mov ecx,000ff00ffh
mov cx,1
or cx,cx
jz failure

xor cx,cx
jnz failure

lea esi,b
cmp byte ptr [esi],1
jb failure

cmp byte ptr [esi],4
ja failure

mov byte ptr [esi],-2
cmp byte ptr [esi],1
jb failure  ; // because unsigned comparaison

mov dx,-1
cmp dx,0
jg failure

mov dx,5
cmp dx,5
jg failure

mov eax,5
cmp eax,4
jg @df@@@@1
jmp failure
@df@@@@1:

mov eax,4
cmp eax,4
jge @df@@@@2
jmp failure
@df@@@@2:

mov eax,5
cmp eax,4
jge @df@@@@3
jmp failure
@df@@@@3:

mov dx,-1
cmp dx,0
jge failure

;;;;;
mov dx,0
cmp dx,-1
jl failure

mov dx,5
cmp dx,5
jl failure

mov eax,4
cmp eax,5
jl @df@@@@4
jmp failure
@df@@@@4:

mov eax,4
cmp eax,4
jle @df@@@@5
jmp failure
@df@@@@5:

mov eax,4
cmp eax,5
jle @df@@@@6
jmp failure
@df@@@@6:

mov dx,0
cmp dx,-1
jle failure

mov cx,-1
jcxz failure

mov cx,0
jcxz @df@@@@7
jmp failure
@df@@@@7:


good:
MOV al,0
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h


table   dw 0
	dw offset failure
  dw @df@@@@8
  dw @df@@@@9

start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
