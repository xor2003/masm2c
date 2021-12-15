#ifndef __asm_32_h__
#define __asm_32_h__

static inline db* raddr_(dw segment,dd offset) {return reinterpret_cast<db *>(offset);}

 typedef dd MWORDSIZE;
 #define offset(segment,name) ((size_t)(db*)&name)

 #define MOVSS(a) {void * dest;void * src;src=realAddress(esi,ds); dest=realAddress(edi,es); \
		memmove(dest,src,a); edi+=(GET_DF()==0)?a:-a; esi+=(GET_DF()==0)?a:-a; }
 #define STOS(a,b) {memcpy (realAddress(edi,es), ((db *)&eax)+b, a); edi+=(GET_DF()==0)?a:-a;}

 #define REP ecx++;while (--ecx != 0)
 #define REPE AFFECT_ZFifz(0);ecx++;while (--ecx != 0 && GET_ZF())
 #define REPNE AFFECT_ZFifz(1);ecx++;while (--ecx != 0 && !GET_ZF())
 #define XLAT {al = *m2c::raddr_(ds,ebx+al);}
 #define CMPSB \
	{  \
			db* src=realAddress(esi,ds); db* dest=realAddress(edi,es); \
			CMP(*src, *dest); edi+=(GET_DF()==0)?1:-1; esi+=(GET_DF()==0)?1:-1; \
	}
 #define CMPSW \
	{  \
			dw* src=(dw*)realAddress(esi,ds); dw* dest=(dw*)realAddress(edi,es); \
			CMP(*src, *dest); edi+=(GET_DF()==0)?2:-2; esi+=(GET_DF()==0)?2:-2; \
	}

//  printf("~%08X_",*(dd*)realAddress(esi,ds)); printf("%08X~",*(dd*)realAddress(edi,es)); \

 #define CMPSD \
	{ \
			dd* src=(dd*)realAddress(esi,ds); dd* dest=(dd*)realAddress(edi,es); \
			CMP(*src, *dest); edi+=(GET_DF()==0)?4:-4; esi+=(GET_DF()==0)?4:-4; \
	}

//printf("~%02X",al);printf("%02X~",*realAddress(edi,es));

 #define SCASB \
	{  \
			CMP(al, *(db*)realAddress(edi,es)); edi+=(GET_DF()==0)?1:-1; \
	}
 #define SCASW \
	{  \
			CMP(ax, *(dw*)realAddress(edi,es)); edi+=(GET_DF()==0)?2:-2; \
	}
 #define SCASD \
	{  \
			CMP(eax, *(dd*)realAddress(edi,es)); edi+=(GET_DF()==0)?4:-4; \
	}

 #define LODS(addr,s) {memcpy (((db *)&eax), &(addr), s);; esi+=(GET_DF()==0)?s:-s;} // TODO not always si!!!
 #define LODSS(a,b) {memcpy (((db *)&eax)+b, realAddress(esi,ds), a); esi+=(GET_DF()==0)?a:-a;}

 #ifdef MSB_FIRST
  #define STOSB STOS(1,3)
  #define STOSW STOS(2,2)
 #else
  #define STOSB STOS(1,0)
   #ifdef A_NORMAL
    #define STOSW {if (es>=0xB800) {STOS(2,0);} else {attron(COLOR_PAIR(ah)); mvaddch(edi/160, (edi/2)%80, al); /*attroff(COLOR_PAIR(ah))*/;edi+=(GET_DF()==0)?2:-2;refresh();}}
   #else
    #define STOSW STOS(2,0)
   #endif
 #endif
 #define STOSD STOS(4,0)

 #define INSB {db averytemporary3 = asm2C_IN(dx);*realAddress(edi,es)=averytemporary3;edi+=(GET_DF()==0)?1:-1;}
 #define INSW {dw averytemporary3 = asm2C_INW(dx);*realAddress(edi,es)=averytemporary3;edi+=(GET_DF()==0)?2:-2;}

 #define LOOP(label) DEC(ecx); JNZ(label)
 #define LOOPE(label) --ecx; if (ecx!=0 && GET_ZF()) GOTOLABEL(label) //TODO
 #define LOOPNE(label) --ecx; if (ecx!=0 && !GET_ZF()) GOTOLABEL(label) //TODO



#endif

