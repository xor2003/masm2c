"C:\MinGW\bin\g++.exe" -mno-ms-bitfields %1.cpp pdcurses.lib  -o %1 -O0  -Wno-multichar   -lgdi32 -lcomdlg32  -I\MinGW\include\SDL2 -lmingw32 -lSDL2main -lSDL2 -ggdb3 -DDEBUG=3
rem "C:\MinGW\bin\g++.exe" -O3 -mno-ms-bitfields iplay_masm_.cpp pdcurses.lib -c  -o iplay_masm_.o  -Wno-multichar   -lgdi32 -lcomdlg32  -I\MinGW\include\SDL2 -lmingw32 -lSDL2main -lSDL2 -ggdb3 -fno-ipa-icf -fno-ipa-cp-clone  > iplay_masm_.err