.386p

        TITLE   listing_title - free-form title text accepted by MASM
        SUBTITLE subtitle text with spaces and punctuation
        SUBTTL  short subtitle text
        SUBTTL  LABEL Key Processing

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

xor al, al
mov ah, 4ch
int 21h

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
