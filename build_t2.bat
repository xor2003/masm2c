del iplay_t1.obj iplay_t2.obj iplay_t.exe
rem lzasm /zi /q /la /w2 /c /kh32768 iplay_t.asm
tasm /zi /m2 /q /la /w2 /c /kh32768 iplay_t1.asm
tasm /zi /m2 /q /la /w2 /c /kh32768 iplay_t2.asm
rem wlink  name iplay_t.exe system dos file iplay_t.obj option verbose
tlink7 /v /3  iplay_t1.obj iplay_t2.obj,iplay_t.exe
rem \upx.exe  --ultra-brute iplay_t.exe
rem type IPLAY.PCT >> iplay_t.exe

