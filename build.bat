del iplay_f.obj iplay_f.exe
lzasm /q /la /w2 /c /kh32768 iplay_f.asm
rem wlink  name iplay_f.exe system dos file iplay_f.obj option verbose
alink -m -oEXE iplay_f.obj
D:\upx.exe  --ultra-brute iplay_f.exe
type IPLAY.PCT >> iplay_f.exe
