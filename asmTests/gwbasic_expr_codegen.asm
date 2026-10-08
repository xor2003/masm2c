.386p

_DATA segment use16 word public 'DATA'
token_low db LOW OFFSET target_token
token_word dw (OFFSET target_token)
token_byte_offset_plus db OFFSET target_token+0
empty_byte db ''
_DATA ends

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT, ds:_DATA

start:
mov ax, 2386364 SHR 16
cmp ax, 36
jne failure

mov al, LOW OFFSET "%"+1
cmp al, 38
jne failure

mov al, LOW OFFSET "+"-"-"
cmp al, -2
jne failure

mov al, token_low
cmp al, LOW OFFSET target_token
jne failure

mov ax, token_word
cmp ax, OFFSET target_token
jne failure

mov al, empty_byte
cmp al, 0
jne failure

mov al, token_byte_offset_plus
cmp al, LOW OFFSET target_token
jne failure

mov al, 0
jmp exitLabel

target_token:
nop

failure:
mov al, 1

exitLabel:
mov ah, 4ch
int 21h

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
