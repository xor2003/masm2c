.386p
_DATA   segment use16 word public 'DATA' ;IGNORE
db 1,2,3,4

var1 db 2,5,6
var2 dw 4,6,9
var3 dd 11,-11,2,4
var4 db 100 dup (1)
testOVerlap db 1,2,3,4,5,6,7,8,9,10,11,12,13,14
str1 db 'abcde'
str2 db 'abcde'
str3 db 'cdeab'

T EQU 4


_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

push _DATA
pop ds

push ds
pop es

cld
;jmp finTest
mov si,offset var1
mov di,offset var4
movsb
cmp [var4],2
mov al,1
jne failure



cmp si,offset var1+1
mov al,2
jne failure
cmp di,offset var4+1
mov al,3
jne failure


mov si,offset var3
mov di,offset var4
mov ecx,t
rep movsb
cmp dword ptr var4,11
mov al,4
jne failure
cmp [var4+t],1
mov al,5
jne failure


cmp si,offset var3+4
mov al,6
jne failure
cmp di,offset var4+4
mov al,7
jne failure

;mov edx,offset var1             ; DS:EDX -> $ Terminated String
;cmp edx,0
;jne failure
;mov cl, byte ptr ds:[2]
;cmp cl,6
;jne failure

mov si,offset str1
mov di,offset str2
mov ecx,5
repe cmpsb
mov al,8
jnz failure

mov si,offset str1
mov di,offset str3
mov ecx,5
repe cmpsb
mov al,9
jz failure

finTest:
mov si,offset testOVerlap
mov edi,esi
inc edi
mov ecx,10
rep movsb
lea di,testOVerlap
cmp byte ptr [testOVerlap+1],1
mov al,10
jne failure

mov byte ptr [var1+1],5
cmp byte ptr [var1+1],5
mov al,11
jne failure

mov si,offset var1
mov edi,esi
inc edi
mov ecx,10
rep movsb
lea di,var1
cmp byte ptr [var1+2],5
mov al,12
je failure ; http://blog.rewolf.pl/blog/?p=177

MOV al,0
JMP exitLabel
failure:
;mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
