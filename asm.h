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

#if defined(_REAL_MODE)
#define realAddress(offset,segment) ((db *)&m+(dd)offset + 0x10*segment)
#else
#define realAddress(offset,segment) ((db *)&m+(dd)offset+selectors[segment])
#endif

#define db uint8_t
#define dw uint16_t
#define dd uint32_t

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

//#define PUSHAD memcpy (&m.stack[m.stackPointer], &m.eax.dd.val, sizeof (dd)*8); m.stackPointer+=sizeof(dd)*8; assert(m.stackPointer<STACK_SIZE)

//#define POPAD m.stackPointer-=sizeof(dd)*8; memcpy (&m.eax.dd.val, &m.stack[m.stackPointer], sizeof (dd)*8)

#define PUSH(a) memcpy (&stack[stackPointer], &a, sizeof (a)); stackPointer+=sizeof(a); assert(stackPointer<STACK_SIZE)

#define POP(a) stackPointer-=sizeof(a); memcpy (&a, &stack[stackPointer], sizeof (a))

#define AFFECT_ZF(a) ZF=(a==0)
#define AFFECT_CF(a) CF=a
#define ISNEGATIVE(a) (a & (1 << (sizeof(a)*8-1)))
#define AFFECT_SF(a) SF=ISNEGATIVE(a) //(a>>(nbBits-1))&1

// TODO: add missings affected flags on CMP
#define CMP(a,b) AFFECT_ZF(a-b); AFFECT_CF(a<b); AFFECT_SF(a-b);
#define OR(a,b) a=a|b; AFFECT_ZF(a); AFFECT_SF(nbBits, a)
#define XOR(a,b) a=a^b; AFFECT_ZF(a); AFFECT_SF(nbBits, a)
#define AND(a,b) a=a&b; AFFECT_ZF(a); AFFECT_SF(nbBits, a)
#define NEG(a) AFFECT_CF(a!=0); a=-a;
#define TEST(a,b) AFFECT_ZF((a&b)); AFFECT_CF(b<a); AFFECT_SF(a&b)

#define SHR(a,b) a=a>>b
#define SHL(a,b) a=a<<b
#define ROR(a,b) a=(a>>b | a<<(nbBits-b))
#define ROL(a,b) a=(a<<b | a>>(nbBits-b))

#define SHRD(a,b,c) a=(a>>c) | ( (b& ((1<<c)-1) ) << (nbBits-c) ) //TODO

#define SAR(a,b) a=(( (a & (1 << (nbBits-1)))?-1:0)<<(nbBits-(0x1f & b))) | (a >> (0x1f & b))  // TODO

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

#define ADD(a,b) {a=a+b; AFFECT_ZF(a); AFFECT_CF(a<b); AFFECT_SF(a);}
#define SUB(a,b) {a=a-b; AFFECT_ZF(a); AFFECT_CF(b<a); AFFECT_SF(a);}

#define ADC(a,b) {a=a+b+CF; AFFECT_ZF(a); AFFECT_CF(a<b); AFFECT_SF(a);} //TODO
#define SBB(a,b) {a=a-b-CF; AFFECT_ZF(a); AFFECT_CF(b<a); AFFECT_SF(a);} 

// TODO: should affects OF, SF, ZF, AF, and PF
#define INC(a) {a=a+1; AFFECT_ZF(a)}
#define DEC(a) {a=a-1; AFFECT_ZF(a)}

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

#define JCXZ(label) if (ecx.dw.val == 0) GOTOLABEL(label) // TODO
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

#define LFS(dest,src) dest = src; fs.dw.val = *(dw*)((char*)src + nbBits/8)
#define LES(dest,src) dest = src; es.dw.val = *(dw*)((char*)src + nbBits/8)
#define LGS(dest,src) dest = src; gs.dw.val = *(dw*)((char*)src + nbBits/8)
#define LDS(dest,src) dest = src; ds.dw.val = *(dw*)((char*)src + nbBits/8)

#define MOVZX(dest,src) dest = src
#define MOVSX(dest,src) if (ISNEGATIVE(nbBitsSrc,src)) { dest = ((-1 ^ (( 1 <<nbBitsSrc )-1)) | src ); } else { dest = src; }

#define BT(dest,src) CF = dest & (1 << src) //TODO
#define BTS(dest,src) CF = dest & (1 << src); dest |= 1 << src
#define BTC(dest,src) CF = dest & (1 << src); dest ^= (1 << src)
#define BTR(dest,src) CF = dest & (1 << src); dest &= ~(1 << src)

// LEA - Load Effective Address
#define LEA(dest,src) dest = src

#define XCHG(dest,src) XCHG(dest,src) //TODO

// MOVSx (DF FLAG not implemented)
#define MOVSS(a,ecx) src=realAddress(esi,ds); dest=realAddress(edi,es); \
	if (labs(((char *)dest)-((char *)src))<=a) { \
		for(i=0; i<ecx; i++) {  \
			src=realAddress(esi,ds); dest=realAddress(edi,es); \
			memmove(dest,src,a); edi+=a; esi+=a; } \
	} else { \
		memmove(dest,src,a*ecx); edi+=a*ecx; esi+=a*ecx; \
	}


#define MOVS(dest,src)  \
                        memmove(dest,src,nbBits/8); dest+=nbBits/8; src+=nbBits/8; } \

#define CMPS(a,ecx) \
	for(size_t i=0; i<ecx; i++) {  \
			src=realAddress(esi,ds); dest=realAddress(edi,es); \
			AFFECT_ZF( (*(char*)dest-*(char*)src) ); edi+=a; esi+=a; \
			if (!ZF) break; \
	}

#define REPE_CMPS(b) CMPS(b,ecx)
#define REPE_CMPSB REPE_CMPS(1)
#define CBW ah = al & (1 << 7)?-1:0 // TODO
#define CWD dx = ax & (1 << 15)?-1:0
#define CWDE eax |= ax & (1 << 15)?(-1 & 0xffff0000):0

#define MOVSB MOVSS(1,1)
#define MOVSW MOVSS(2,1)
#define MOVSD MOVSS(4,1)

#define REP_MOVSS(b) MOVSS(b,ecx)
#define REP_MOVS(dest,src) for(i=0; i<ecx;i++) {MOVS(dest,src)}
#define REP_MOVSB REP_MOVSS(1)
#define REP_MOVSW REP_MOVSS(2)
#define REP_MOVSD REP_MOVSS(4)

#define STOS(a,b) memcpy (realAddress(edi,es), ((db *)&eax)+b, a); edi+=a

#ifdef MSB_FIRST
#define STOSB STOS(1,3)
#define STOSW STOS(2,2)
#else
#define STOSB STOS(1,0)
#define STOSW STOS(2,0)
#endif

#define STOSD STOS(4,0)

#define REP_STOSB for (i=0; i<ecx; i++) { STOSB; }
#define REP_STOSW for (i=0; i<ecx; i++) { STOSW; }
#define REP_STOSD for (i=0; i<ecx; i++) { STOSD; }

#define LODS(a,b) memcpy (((db *)&eax)+b, realAddress(esi,ds), a); esi+=a

#ifdef MSB_FIRST
#define LODSB LODS(1,3)
#define LODSW LODS(2,2)
#else
#define LODSB LODS(1,0)
#define LODSW LODS(2,0)
#endif

#define LODSD LODS(4,0)

#define REP_LODS(a,b) for (i=0; i<ecx; i++) { LODS(a,b); }

#ifdef MSB_FIRST
#define REP_LODSB REP_LODS(1,3)
#define REP_LODSW REP_LODS(2,2)
#else
#define REP_LODSB REP_LODS(1,0)
#define REP_LODSW REP_LODS(2,0)
#endif

#define REP_LODSD REP_LODS(4,0)

// JMP - Unconditional Jump
#define JMP(label) GOTOLABEL(label)
#define GOTOLABEL(a) goto a

#define LOOP(label) DEC(32,ecx); JNZ(label)
#define LOOPE(label) --ecx; if (ecx!=0 && ZF) GOTOLABEL(label) //TODO

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
#define PUSHF
#define POPF
#define NOP

#define CALL(label) \
	if (setjmp(jmpbuffer) == 0) { \
		PUSH(jmpbuffer); \
		JMP(label); \
	}

#define RET POP(jmpbuffer); longjmp(jmpbuffer, 0);

#define RETN RET //TODO test
#define RETF RET

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
