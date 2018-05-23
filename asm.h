#ifndef __asm_h__
#define __asm_h__

#include <stdint.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>
#include <setjmp.h>
#include <stddef.h>
#include <stdio.h>
#include <assert.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#if defined(_WIN32) || defined(__INTEL_COMPILER)
#define INLINE __inline
#elif defined(__STDC_VERSION__) && __STDC_VERSION__>=199901L
#define INLINE inline
#elif defined(__GNUC__)
#define INLINE __inline__
#else
#define INLINE
#endif

#define _REAL_MODE 1
#if defined(_REAL_MODE)
#define raddr(segment,offset) (((db *)&m + offset + (segment<<4) ))
#else
#define raddr(segment,offset) ((db *)&m+(db)(offset)+selectors[segment])
#endif

#define realAddress(offset, segment) raddr(segment,offset)
#define offset(segment,name) offsetof(struct Mem,name)-offsetof(struct Mem,segment)
#define seg_offset(segment) ((offsetof(struct Mem,segment)+0xf)>>4)

typedef uint8_t db;
typedef uint16_t dw;
typedef uint32_t dd;

#ifdef MSB_FIRST
typedef struct dblReg {
	db v0;
	db v1;
	db v2;
	db val;
} dblReg;
typedef struct dbhReg {
	db v0;
	db v1;
	db val;
	db v2;
} dbhReg;
typedef struct dwReg {
	dw v0;
	dw val;
} dwReg;
typedef struct dblReg16 {
	db v0;
	db val;
} dblReg16;
typedef struct dbhReg16 {
	db val;
	db v0;
} dbhReg16;
#else
typedef struct dblReg {
	db val;
	db v0;
	db v1;
	db v2;
} dblReg;
typedef struct dbhReg {
	db v0;
	db val;
	db v1;
	db v2;
} dbhReg;
typedef struct dwReg {
	dw val;
	dw v0;
} dwReg;
typedef struct dblReg16 {
	db val;
	db v0;
} dblReg16;
typedef struct dbhReg16 {
	db v0;
	db val;
} dbhReg16;
#endif

typedef struct ddReg {
	dd val;
} ddReg;


typedef union registry32Bits
{
	struct dblReg dbl;
	struct dbhReg dbh;
	struct dwReg dw;
	struct ddReg dd;
} registry32Bits;


typedef struct dwReg16 {
	dw val;
} dwReg16;                                       



typedef union registry16Bits
{
	struct dblReg16 dbl;
	struct dbhReg16 dbh;
	struct dwReg16 dw;
} registry16Bits;


#define VGARAM_SIZE 320*200
#define STACK_SIZE 1024*sizeof(dd)
#define HEAP_SIZE 1024*1024*4
#define NB_SELECTORS 128

#define XLAT {al = *raddr(ds,bx+al);}
//#define PUSHAD memcpy (&m.stack[m.stackPointer], &m.eax.dd.val, sizeof (dd)*8); m.stackPointer+=sizeof(dd)*8; assert(m.stackPointer<STACK_SIZE)
#define PUSHAD {PUSH(eax);PUSH(ebx);PUSH(ecx);PUSH(edx); PUSH(esi);PUSH(edi);PUSH(ebp);PUSH(ebp);}
#define PUSHA PUSHAD

//#define POPAD m.stackPointer-=sizeof(dd)*8; memcpy (&m.eax.dd.val, &m.stack[m.stackPointer], sizeof (dd)*8)
#define POPAD {POP(ebp);POP(ebp);POP(edi);POP(esi); POP(edx);POP(ecx);POP(ebx);POP(eax); }
#define POPA POPAD

#define PUSH(a) {dd t=(dd)a; memcpy (&stack[stackPointer], &t, sizeof (a)); stackPointer+=sizeof(a); assert(stackPointer<STACK_SIZE);}

#define POP(a) {stackPointer-=sizeof(a); memcpy (&a, &stack[stackPointer], sizeof (a));}

#define AFFECT_ZF(a) {ZF=((a)==0);}
#define AFFECT_CF(a) {CF=(a);}
//#define ISNEGATIVE(a) (a & (1 << (sizeof(a)*8-1)))
//#define AFFECT_SF(a) {SF=ISNEGATIVE(a);}
#define AFFECT_SF(f, a) {SF=((a)>>(sizeof(f)*8-1));}
#define ISNEGATIVE(f,a) ( (a) & (1 << (sizeof(f)*8-1)) )

// TODO: add missings affected flags on CMP
#define CMP(a,b) {AFFECT_ZF( ((a)& MASK[sizeof(a)]) !=((b)& MASK[sizeof(a)]) ); \
		AFFECT_CF((a)<(b)); \
		AFFECT_SF(a, ((a)-(b))&(1 << sizeof(a)*8 - 1) );}
#define OR(a,b) {a=a|b; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a)}
#define XOR(a,b) {a=a^b; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a)}
#define AND(a,b) {a=a&b; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a)}

#define NEG(a) {AFFECT_CF((a)!=0); \
		a=-a;}
#define TEST(a,b) {AFFECT_ZF((a)&(b)); \
		AFFECT_CF((b)<(a)); \
		AFFECT_SF(a,(a)&(b))}

#define SHR(a,b) {a=a>>b;}
#define SHL(a,b) {a=a<<b;}
#define ROR(a,b) {a=(a>>b | a<<(sizeof(a)*8-b));}
#define ROL(a,b) {a=(a<<b | a>>(sizeof(a)*8-b));}

#define SHRD(a,b,c) {a=(a>>c) | ( (b& ((1<<c)-1) ) << (sizeof(a)*8-c) );} //TODO

#define SAR(a,b) {a=(( (a & (1 << (sizeof(a)*8-1)))?-1:0)<<(sizeof(a)*8-(0x1f & b))) | (a >> (0x1f & b));}  // TODO

#define READDDp(a) ((dd *) &m.a)
#define READDWp(a) ((dw *) &m.a)
#define READDBp(a) ((db *) &m.a)

#define READDD(a) (a)

#ifdef MSB_FIRST
#define READDBhW(a) (*(((db *) &a)+0))
#define READDBhD(a) (*(((db *) &a)+2))
#define READDBlW(a) (*(((db *) &a)+1))
#define READDBlD(a) (*(((db *) &a)+3))
#else
#define READDBhW(a) (*(((db *) &a)+1))
#define READDBhD(a) (*(((db *) &a)+1))
#define READDBlW(a) (*(((db *) &a)))
#define READDBlD(a) (*(((db *) &a)))
#endif

#define READDW(a) (*((dw *) &m.a.dw.val))
#define READDBh(a) (*((db *) &m.a.dbh.val))
#define READDBl(a) (*((db *) &m.a.dbl.val))

#define AAD {al = al + (ah * 10) & 0xFF; ah = 0;} //TODO

#define ADD(a,b) {a=a+b; \
		AFFECT_ZF(a); \
		AFFECT_CF((a)<(b)); \
		AFFECT_SF(a,a);}

#define SUB(a,b) {a=a-b; \
		AFFECT_ZF(a); \
		AFFECT_CF((b)<(a)); \
		AFFECT_SF(a,a);}

#define ADC(a,b) {a=a+b+CF; \
		AFFECT_ZF(a); \
		AFFECT_CF((a)<(b)); \
		AFFECT_SF(a,a);} //TODO
#define SBB(a,b) {a=a-b-CF; \
		AFFECT_ZF(a); \
		AFFECT_CF((b)<(a)); \
		AFFECT_SF(a,a);} 

// TODO: should affects OF, SF, ZF, AF, and PF
#define INC(a) {a+=1; \
		AFFECT_ZF(a);}
#define DEC(a) {a-=1; \
		AFFECT_ZF(a);}

#define IMUL1_1(a) ax=(int8_t)al*(int8_t)a
#define IMUL1_2(a) {int32_t t=(int16_t)ax*(int16_t)a;ax=t;dx=t>>16;}
#define IMUL1_4(a) {int64_t t=(int32_t)eax*(int32_t)a;eax=t;edx=t>>32;}
#define IMUL2_2(a,b) {a = (int16_t)a * (int16_t)b;}
#define IMUL2_4(a,b) {a = (int32_t)a * (int32_t)b;}
#define IMUL3_2(a,b,c) {a = (int16_t)b * (int16_t)c;}
#define IMUL3_4(a,b,c) {a = (int32_t)b * (int32_t)c;}

#define MUL1_1(a) ax=al*a
#define MUL1_2(a) {dd t=ax*a;ax=t;dx=t>>16;}
#define MUL1_4(a) {uint64_t t=eax*a;eax=t;edx=t>>32;}
#define MUL2_2(a,b) {a *= b;}
#define MUL2_4(a,b) {a *= b;}
#define MUL3_2(a,b,c) {a = b * c;}
#define MUL3_4(a,b,c) {a = b * c;}

#define IDIV1(a) {al=(int16_t)ax/a;ah=(int16_t)ax%a;}
#define IDIV2(a) {ax=((int32_t)dx<<16+(int16_t)ax)/a;dx=((int16_t)dx<<16+(int16_t)ax)%a;}
#define IDIV4(a) {eax=((int64_t)edx<<32+(int32_t)eax)/a;edx=((int64_t)edx<<32+(int32_t)eax)%a;}

#define DIV1(a) {al=ax/a;ah=ax%a;}
#define DIV2(a) {ax=(dx<<16+ax)/a;dx=(dx<<16+ax)%a;}
#define DIV4(a) {eax=(edx<<32+eax)/a;edx=(edx<<32+eax)%a;}

#define NOT(a) a= ~a;// AFFECT_ZF(a) //TODO
#define SETNZ(a) a= (!ZF)&1; //TODO
#define SETZ(a) a= (ZF)&1; //TODO
#define SETB(a) a= (CF)&1; //TODO


#define JE(label) if (ZF) GOTOLABEL(label)
#define JZ(label) JE(label)

#define JNE(label) if (!ZF) GOTOLABEL(label)
#define JNZ(label) JNE(label)

#define JNB(label) if (!CF) GOTOLABEL(label)
#define JAE(label) JNB(label)
#define JNC(label) JNB(label)

#define JGE(label) if (!SF) GOTOLABEL(label) // TODO
#define JG(label) if (!ZF && !SF) GOTOLABEL(label) // TODO

#define JLE(label) if (ZF || SF) GOTOLABEL(label) // TODO
#define JL(label) if (SF) GOTOLABEL(label) // TODO

#define JCXZ(label) if (cx == 0) GOTOLABEL(label) // TODO
#define JECXZ(label) if (ecx == 0) GOTOLABEL(label) // TODO


#define JB(label) if (CF) GOTOLABEL(label)
#define JC(label) JB(label)
#define JNAE(label) JB(label)

#define JA(label) if (!CF && !ZF) GOTOLABEL(label)
#define JNBE(label) JA(label)

#define JS(label) if (SF) GOTOLABEL(label)
#define JNS(label) if (!SF) GOTOLABEL(label)

#define JNA(label) if (CF || ZF) GOTOLABEL(label)
#define JBE(label) JNA(label)

#define MOV(dest,src) dest = src

#define LFS(dest,src) dest = src; fs= *(dw*)((db*)&(src) + sizeof(dest))
#define LES(dest,src) dest = src; es = *(dw*)((db*)&(src) + sizeof(dest))
#define LGS(dest,src) dest = src; gs = *(dw*)((db*)&(src) + sizeof(dest))
#define LDS(dest,src) dest = src; ds = *(dw*)((db*)&(src) + sizeof(dest))

#define MOVZX(dest,src) dest = src
#define MOVSX(dest,src) if (ISNEGATIVE(src,src)) { dest = ((-1 ^ (( 1 << (sizeof(src)*8) )-1)) | src ); } else { dest = src; }

#define BT(dest,src) CF = dest & (1 << src) //TODO
#define BTS(dest,src) CF = dest & (1 << src); dest |= 1 << src
#define BTC(dest,src) CF = dest & (1 << src); dest ^= (1 << src)
#define BTR(dest,src) CF = dest & (1 << src); dest &= ~(1 << src)

// LEA - Load Effective Address
#define LEA(dest,src) dest = src

#define XCHG(dest,src) std::swap(dest,src); //TODO


#define MOVS(dest,src,s)  {dest=src; dest+=s; src+=s; }
//                        {memmove(dest,src,s); dest+=s; src+=s; } \

#define CMPS(a) \
	{  \
			src=realAddress(si,ds); dest=realAddress(di,es); \
			AFFECT_ZF( (*(char*)dest-*(char*)src) ); di+=a; si+=a; \
	}

#define SCASB \
	{  \
			dest=realAddress(di,es); \
			AFFECT_ZF( (*(char*)dest-al) ); di+=1; \
	}

#define CMPSB CMPS(1)
#define CBW ah = al & (1 << 7)?-1:0 // TODO
#define CWD dx = ax & (1 << 15)?-1:0
#define CWDE {*(((dw*)&eax)+1) = ax & (1 << 15)?-1:0;}

// MOVSx (DF FLAG not implemented)
#define MOVSS(a) {src=realAddress(si,ds); dest=realAddress(di,es); \
		memmove(dest,src,a); di+=a; si+=a; }

#define MOVSB MOVSS(1)
#define MOVSW MOVSS(2)
#define MOVSD MOVSS(4)

#define REP while (cx-- > 0)
#define REPE AFFECT_ZF(0);while (cx-- > 0 && ZF)
#define REPNE AFFECT_ZF(1);while (cx-- > 0 && !ZF)
/*
#define REP_MOVSS(b) MOVSS(b,cx)
#define REP_MOVS(dest,src) while (cx-- > 0) {MOVS(dest,src);}
#define REP_MOVSB REP_MOVSS(1)
#define REP_MOVSW REP_MOVSS(2)
#define REP_MOVSD REP_MOVSS(4)
*/
#define STOS(a,b) {memcpy (realAddress(di,es), ((db *)&eax)+b, a); di+=a;}

#ifdef MSB_FIRST
#define STOSB STOS(1,3)
#define STOSW STOS(2,2)
#else
#define STOSB STOS(1,0)
#define STOSW STOS(2,0)
#define STOSD STOS(4,0)
#endif


//#define REP_STOSB while (cx>0) { STOSB; --cx;}
//#define REP_STOSW while (cx>0) { STOSW; --cx;}
//#define REP_STOSD while (cx>0) { STOSD; --cx;}

#define LODS(addr,s) {memcpy (((db *)&eax), &(addr), s);; si+=s;} // TODO not always si!!!
#define LODSS(a,b) {memcpy (((db *)&eax)+b, realAddress(si,ds), a); si+=a;}

#ifdef MSB_FIRST
#define LODSB LODSS(1,3)
#define LODSW LODSS(2,2)
#else
#define LODSB LODSS(1,0)
#define LODSW LODSS(2,0)
#endif
#define LODSD LODSS(4,0)

/*
#define REP_LODS(a,b) for (i=0; i<ecx; i++) { LODS(a,b); }

#ifdef MSB_FIRST
#define REP_LODSB REP_LODS(1,3)
#define REP_LODSW REP_LODS(2,2)
#else
#define REP_LODSB REP_LODS(1,0)
#define REP_LODSW REP_LODS(2,0)
#define REP_LODSD REP_LODS(4,0)
#endif
*/

// JMP - Unconditional Jump
#define JMP(label) GOTOLABEL(label)
#define GOTOLABEL(a) goto a

#define LOOP(label) DEC(cx); JNZ(label)
#define LOOPE(label) --cx; if (cx!=0 && ZF) GOTOLABEL(label) //TODO

#define CLD DF=0
#define STD DF=1

#define STC CF=1 //TODO
#define CLC CF=0 //TODO
#define CMC CF ^= 1 //TODO

void stackDump();
void hexDump (void *addr, int len);
void asm2C_INT(int a);
void asm2C_init();
void asm2C_printOffsets(unsigned int offset);

// directjeu nosetjmp,2
// directmenu
#define INT(a) asm2C_INT(a); TESTJUMPTOBACKGROUND

#define TESTJUMPTOBACKGROUND  //if (jumpToBackGround) CALL(moveToBackGround);

void asm2C_OUT(int16_t address, int data);
#define OUT(a,b) asm2C_OUT(a,b)
int8_t asm2C_IN(int16_t data);
#define IN(a,b) a = asm2C_IN(b); TESTJUMPTOBACKGROUND

#define STI // TODO: STI not implemented
#define CLI // TODO: STI not implemented
#define PUSHF PUSH(CF+(ZF<<1)+(DF<<2)+(SF<<3))
#define POPF {dw t; POP(t); CF=t&1; ZF=(t>>1)&1; DF=(t>>2)&1; SF=(t>>3)&1;}
#define NOP

#define CALL(label) \
	if (setjmp(jmpbuffer) == 0) { \
		PUSH(jmpbuffer); \
		JMP(label); \
	}

#define RET POP(jmpbuffer); longjmp(jmpbuffer, 0);

#define RETN RET //TODO test
#define RETF RET; stackPointer-=2

#ifdef __LIBSDL2__
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#endif

#ifdef __LIBRETRO__
#include "libretro.h"
extern retro_log_printf_t log_cb;
#else
extern FILE * logDebug;
#endif

void log_error(const char *fmt, ...);
void log_debug(const char *fmt, ...);
void log_info(const char *fmt, ...);
void log_debug2(const char *fmt, ...);

#if DEBUG==2
    #define R(a) log_debug("l:%d:%s\n",__LINE__,#a); a
#else
    #define R(a) a
#endif

bool is_little_endian();

#if defined(_MSC_VER)
#define SWAP16 _byteswap_ushort
#define SWAP32 _byteswap_ulong
#else
#define SWAP16(x) ((uint16_t)(                  \
			   (((uint16_t)(x) & 0x00ff) << 8)      | \
			   (((uint16_t)(x) & 0xff00) >> 8)        \
			   ))
#define SWAP32(x) ((uint32_t)(           \
			   (((uint32_t)(x) & 0x000000ff) << 24) | \
			   (((uint32_t)(x) & 0x0000ff00) <<  8) | \
			   (((uint32_t)(x) & 0x00ff0000) >>  8) | \
			   (((uint32_t)(x) & 0xff000000) >> 24)   \
			   ))
#endif

#ifdef __cplusplus
}
#endif

#endif
