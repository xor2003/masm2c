#include "../asm.h"
#include <cstring>
#include <cstdio>

void init_get_fname(char *dst, char *src);

//Initializer - is startet if executed file is SCHICKM.EXE/BLADEM.EXE or GEN.EXE
//Returns true if the desired programm is started
bool masm2c_init(char *name, unsigned short reloc, unsigned short _cs, unsigned short ip)
{

	char fname[81];
	int ver;

	init_get_fname(fname, name);

	if (strcmp(fname, "vikings.exe")) return false;

	return true;
}


namespace m2c
{
  void load_drivers()
  {
//    fread(raddr(0x24ed,0x100),0xffff,1,fopen("DN386.HSQ","r"));
//    fread(raddr(0x47d8,0x100),0xffff,1,fopen("DNSBP.HSQ","r"));
//    fread(raddr(0x4d44,0x100),0xffff,1,fopen("DNMID.HSQ","r"));
    

  }
}