.386p

        SUBTTL  top-level label fragment

_DATA   segment use16 word public 'DATA'
_DATA   ends

assume  cs:_TEXT,ds:_DATA
start:
        xor ax,ax
        mov ah,4ch
        int 21h

end start
