#ifndef __asm_h__
#define __asm_h__



//#include <setjmp.h>
/*
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <assert.h>
*/
#include <cstdlib>
#include <cstdarg>
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <cassert>

#include <cstring>

#ifndef NOSDL
 #ifdef __LIBSDL2__
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
 #endif
#endif

// Types
#ifdef __BORLANDC__
 typedef unsigned long uint32_t;
 typedef long int32_t;
 typedef unsigned short int uint16_t;
 typedef short int int16_t;
 typedef unsigned char uint8_t;
 typedef char int8_t;
 struct uint64_t
 {
	long a;
	long b;
 };

 #define MYPACKED
 #define MYINT_ENUM
#else
// #include <stdint.h>
// #include <stdbool.h>
 #include <cstdint>
 #include <cstdbool>
 #define MYPACKED __attribute__((__packed__))
 #define MYINT_ENUM : int
#endif
//#include <pthread.h>

typedef uint8_t db;
typedef uint16_t dw;
typedef uint32_t dd;
typedef uint64_t dq;
//typedef uint80_t dt;

typedef db byte;
typedef dw word;
typedef dd dword;
typedef dq qword;
//typedef dt tbyte;
typedef float real4;
typedef double real8;
typedef long double real10;


#include "memmgr.h"

namespace m2c {
extern FILE * logDebug;

// Asm functions
void log_error(const char *fmt, ...);
void log_debug(const char *fmt, ...);
void log_info(const char *fmt, ...);
void log_debug2(const char *fmt, ...);

const char* log_spaces(int n);


#define VGARAM_SIZE (320*200)

#ifdef __BORLANDC__
 #define STACK_SIZE 4096
 #define HEAP_SIZE 1024
#else
 #define STACK_SIZE (1024*64-16)
 #define HEAP_SIZE 1024*1024 - 16 - STACK_SIZE
#endif

#define NB_SELECTORS 128

#ifdef __cplusplus
//extern "C" {
#endif

static const uint32_t MASK[]={0, 0xff, 0xffff, 0xffffff, 0xffffffff};
#define bitsizeof(dest) (8*sizeof(dest))
#define shiftmodule(dest,shiftbit) (shiftbit&(bitsizeof(dest)-1))
#define bitget(dest,bit) ((bit>=0)?(( (dest) >> bit)&1):0)
#define nthbitone(dest,bit) ( (dq)1 << shiftmodule(dest,bit))
#define bitset(dest,src,bit) {dest=(bit>=0)?(( (dest) & (~nthbitone(dest,bit))) | ((src&1) << bit)):dest;}
#define LSB(a) ((a)&1)
#define MSB(a) (( (a)>>( bitsizeof(a)-1) )&1)

#if defined(_WIN32) || defined(__INTEL_COMPILER)
 #define INLINE __inline
#elif defined(__STDC_VERSION__) && __STDC_VERSION__>=199901L
 #define INLINE inline
#elif defined(__GNUC__)
 #define INLINE __inline__
#else
 #define INLINE
#endif

#if _BITS == 32
  #include "asm_32.h"
#else
  #include "asm_16.h"
#endif

#define realAddress(offset, segment) raddr(segment,offset)


#define seg_offset(segment) ((offset(m2c::m,(segment)))>>4)

// DJGPP
#define MASK_LINEAR(addr)     (((size_t)addr) & 0x000FFFFF)
#define RM_TO_LINEAR(addr)    (((((size_t)addr) & 0xFFFF0000) >> 12) + (((size_t)addr) & 0xFFFF))
#define RM_OFFSET(addr)       (((size_t)addr) & 0xF)
#define RM_SEGMENT(addr)      ((((size_t)addr) >> 4) & 0xFFFF)




//pusha AX, CX, DX, BX, SP, BP, SI, DI
//pushad EAX, ECX, EDX, EBX, ESP, EBP, ESI, EDI
#define PUSHAD {PUSH(eax);PUSH(ecx);PUSH(edx);PUSH(ebx); PUSH(esp);PUSH(ebp);PUSH(esi);PUSH(edi);}
#define POPAD {POP(edi);POP(esi);POP(ebp); POP(ebx); POP(ebx);POP(edx);POP(ecx);POP(eax); }

#define PUSHA {PUSH(ax);PUSH(cx);PUSH(dx);PUSH(bx); PUSH(sp);PUSH(bp);PUSH(si);PUSH(di);}
#define POPA {POP(di);POP(si);POP(bp); POP(bx); POP(bx);POP(dx);POP(cx);POP(ax); }

/*
#define PUSH(a) {memcpy (&stack[stackPointer], &a, sizeof (a)); stackPointer+=sizeof(a); assert(stackPointer<STACK_SIZE);\
	log_debug("after push %d\n",stackPointer);}

#define POP(a) {log_debug("before pop %d\n",stackPointer); \
	stackPointer-=sizeof(a); memcpy (&a, &stack[stackPointer], sizeof (a));}
#define PUSH(a) {stackPointer-=sizeof(a); memcpy (&m.stack[stackPointer], &a, sizeof (a));  assert(stackPointer>8);}
*/
#ifdef DEBUG
 #define PUSH(a) {dd averytemporary=a;stackPointer-=sizeof(a); \
		memcpy (raddr(ss,stackPointer), &averytemporary, sizeof (a)); \
		m2c::log_debug("after push %x\n",stackPointer);}
//		assert((raddr(ss,stackPointer) - ((db*)&stack))>8);}

 #define POP(a) { m2c::log_debug("before pop %x\n",stackPointer);memcpy (&a, raddr(ss,stackPointer), sizeof (a));stackPointer+=sizeof(a);}
#else
 #define PUSH(a) {dd averytemporary=a;stackPointer-=sizeof(a); \
		memcpy (raddr(ss,stackPointer), &averytemporary, sizeof (a));}

 #define POP(a) {memcpy (&a, raddr(ss,stackPointer), sizeof (a));stackPointer+=sizeof(a);}
#endif


#define AFFECT_ZF(a) {ZF=((a)==0);}
#define AFFECT_CF(a) {CF=(a);}
#define AFFECT_AF(a) {AF=(a);}
#define AFFECT_OF(a) {OF=(a);}
//#define ISNEGATIVE(a) (a & (1 << (sizeof(a)*8-1)))
//#define AFFECT_SF(a) {SF=ISNEGATIVE(a);}
#define ISNEGATIVE(f,a) ( (a) & (1 << (bitsizeof(f)-1)) )
#define AFFECT_SF(f, a) {SF=ISNEGATIVE(f,a);}

#define CMP(a,b) {dd averytemporary=((a)-(b))& m2c::MASK[sizeof(a)]; \
		AFFECT_CF((averytemporary)>(a)); \
		AFFECT_ZF(averytemporary); \
		AFFECT_SF(a,averytemporary);}

#define OR(a,b) {a=(a)|(b); \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a); \
		AFFECT_CF(0);}

#define XOR(a,b) {a=(a)^(b); \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a) \
		AFFECT_CF(0);}

#define AND(a,b) {a=(a)&(b); \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a) \
		AFFECT_CF(0);}

#define NEG(a) {AFFECT_CF((a)!=0); \
		a=-a;\
		AFFECT_ZF(a); \
		AFFECT_SF(a,a)}

#define TEST(a,b) {AFFECT_ZF((a)&(b)); \
		AFFECT_CF(0); \
		AFFECT_SF(a,(a)&(b))}

#define SHR(a,b) {if (b) {CF=(a>>(b-1))&1;\
		a=a>>b;\
		AFFECT_ZF(a);\
		AFFECT_SF(a,a)}}

#define SHL(a,b) {if (b) {CF=(a) & (1 << (bitsizeof(a)-(b)));\
		a=a<<b;\
		AFFECT_ZF(a);\
		AFFECT_SF(a,a)}}

#define ROR(a,b) {if (b) {CF=((a)>>(shiftmodule(a,b)-1))&1;\
		a=((a)>>(shiftmodule(a,b)) | a<<(bitsizeof(a)-(shiftmodule(a,b))));}}

#define ROL(a,b) {if (b) {a=(((a)<<(shiftmodule(a,b))) | (a)>>(bitsizeof(a)-(shiftmodule(a,b))));\
		AFFECT_CF(LSB(a));}}

#define RCL(a, b) m2c::RCL_(a, b, CF)
template <class D, class C>
void RCL_(D& Destination, C Count, bool& CF_)
{ 
		int TemporaryCount = Count % (bitsizeof(Destination) + 1);
			while(TemporaryCount) {
				bool TemporaryCF = MSB(Destination);
				Destination = (Destination << 1) + CF_;
				CF_ = TemporaryCF;
				--TemporaryCount;
			}
}

#define RCR(a, b) m2c::RCR_(a, b, CF)
template <class D, class C>
void RCR_(D& Destination, C Count, bool& CF_)
{ 
		int TemporaryCount = Count % (bitsizeof(Destination) + 1);
			while(TemporaryCount != 0) {
				bool TemporaryCF = LSB(Destination);
				Destination = (Destination >> 1) + (CF_ << (bitsizeof(Destination)-1));
				CF_ = TemporaryCF;
				--TemporaryCount;
			}
}

template <class D>
void SHLD_(D& Destination, D Source, int Count, bool& CF_);

template <class D>
void SHRD_(D& Destination, D Source, int Count, bool& CF_)
{ 
 if(Count != 0) {
int TCount = Count&(2*bitsizeof(D)-1);

if (TCount>bitsizeof(D)) {SHLD_(Destination, Source, 2*bitsizeof(D)-TCount, CF_);} 
else
{
		CF_ = bitget(Destination,TCount-1); Destination>>=TCount;
		for(int i = bitsizeof(D) - TCount; i <= bitsizeof(D) - 1; ++i) 
			if (i>=0) {bitset(Destination,bitget(Source,i + TCount - bitsizeof(D)),i);}
		if (bitsizeof(D) - TCount<0)	 {CF_ = bitget(Source,TCount-bitsizeof(D)-1);}
}
 }
}

template <class D>
void SHLD_(D& Destination, D Source, int Count, bool& CF_)
{ 
 if(Count != 0) {
int TCount = Count&(2*bitsizeof(D)-1);
if (TCount>bitsizeof(D)) {SHRD_(Destination, Source, 2*bitsizeof(D)-TCount, CF_);} 
else
{
		CF_ = bitget(Destination,bitsizeof(D)-TCount); Destination<<=TCount;
		for(int i = 0; i < TCount; ++i) 
			if (i>=0) {bitset(Destination,bitget(Source,bitsizeof(D) - TCount + i),i);}
}
 }
}

#define SHRD(a, b, c) {m2c::SHRD_(a, b, c, CF);if (c) {AFFECT_ZF(a);AFFECT_SF(a,a);}}
#define SHLD(a, b, c) {m2c::SHLD_(a, b, c, CF);if (c) {AFFECT_ZF(a);AFFECT_SF(a,a);}}
/*
 //TODO CF=(a) & (1 << (sizeof(f)*8-b));
#define SHRD(a,b,c) {if(c) {\
			int shift = c&(2*bitsizeof(a)-1); \
			dd a1=a>>shift; \
			a=a1 | ( (b& ((1<<shift)-1) ) << (bitsizeof(a)-shift) ); \
		AFFECT_ZF(a|b);\
		AFFECT_SF(a,a);}} //TODO optimize
*/

#define SAR(a,b) {if (b) {bool sign = MSB(a);\
	 int shift = (bitsizeof(a)-b);\
         shift = shift>0?shift:0;\
	 dd sigg=shift<(bitsizeof(a))?( (sign?-1:0)<<shift):0;\
         a = b>bitsizeof(a)?0:a;\
	 AFFECT_CF((a >> (b-1))&1);\
	 a=sigg | (a >> b);\
		AFFECT_ZF(a);\
		AFFECT_SF(a,a);}} // TODO optimize

#define SAL(a,b) SHL(a,b)


//#define AAD {al = al + (ah * 10) & 0xFF; ah = 0;} //TODO
/*
#define DAA	{											\
	if (((al & 0x0F)>0x09) || AF) {				\
		if ((al > 0x99) || CF) {					\
			al+=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF(false);							\
		}													\
		al+=0x06;										\
		AFFECT_AF(true);								\
	} else {												\
		if ((al > 0x99) || CF) {					\
			al+=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF(false);							\
		}													\
		AFFECT_AF(false);								\
	}														\
	SF=(al&0x80);							\
	AFFECT_ZF(al);}


#define DAS												\
{															\
	db osigned=al & 0x80;							\
	if (((al & 0x0f) > 9) || AF) {				\
		if ((al>0x99) || CF) {					\
			al-=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF((al<=0x05));					\
		}													\
		al-=6;											\
		AFFECT_AF(true);								\
	} else {												\
		if ((al>0x99) || CF) {					\
			al-=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF(false);							\
		}													\
		AFFECT_AF(false);								\
	}														\
	AFFECT_OF(osigned && ((al&0x80)==0));			\
	SF=(al&0x80);							\
	AFFECT_ZF(al); \
}
*/

#define SALC	{AL=CF?0xff:0;}

#define AAA	{											\
	SF=((al>=0x7a) && (al<=0xf9));		\
	if ((al & 0xf) > 9) {								\
		AFFECT_OF((al&0xf0)==0x70);					\
		ax += 0x106;									\
		AFFECT_CF(true);								\
		AFFECT_ZF(al);						\
		AFFECT_AF(true);								\
	} else if (AF) {									\
		ax += 0x106;									\
		AFFECT_OF(false);								\
		AFFECT_CF(true);								\
		ZF=false;								\
		AFFECT_AF(true);								\
	} else {												\
		AFFECT_OF(false);								\
		AFFECT_CF(false);								\
		AFFECT_ZF(al);						\
		AFFECT_AF(false);								\
	}														\
	al &= 0x0F;}

#define AAS {												\
	if ((al & 0x0f)>9) {								\
		SF=(al>0x85);						\
		ax -= 0x106;									\
		AFFECT_OF(false);								\
		AFFECT_CF(true);								\
		AFFECT_AF(true);								\
	} else if (AF) {									\
		AFFECT_OF(((al>=0x80) && (al<=0x85)));	\
		SF=(al<0x06) || (al>0x85);		\
		ax -= 0x106;									\
		AFFECT_CF(true);								\
		AFFECT_AF(true);								\
	} else {												\
		SF=(al>=0x80);						\
		AFFECT_OF(false);								\
		AFFECT_CF(false);								\
		AFFECT_AF(false);								\
	}														\
	AFFECT_ZF((al == 0));							\
	al &= 0x0F;}

#define AAM1(x)											\
{															\
	db dv=x;											\
	if (dv!=0) {											\
		ah=al / dv;									\
		al=al % dv;									\
		SF=(al & 0x80);						\
		AFFECT_ZF(al);						\
		AFFECT_CF(false);								\
		AFFECT_OF(false);								\
		AFFECT_AF(false);								\
	} \
}

#define AAM AAM1(10)

#define AAD1(x)											\
	{														\
		al = ah * x + al;								\
		ah = 0;											\
		AFFECT_CF(false);								\
		AFFECT_OF(false);								\
		AFFECT_AF(false);								\
		SF=(al >= 0x80);						\
		AFFECT_ZF(al);							\
	}

#define AAD AAD1(10)

#define ADD(a,b) {dq averytemporary=(dq)a+(dq)b; \
		AFFECT_CF((averytemporary)>m2c::MASK[sizeof(a)]); \
		a=averytemporary; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a);}

#define XADD(a,b) {dq averytemporary=(dq)a+(dq)b; \
		AFFECT_CF((averytemporary)>m2c::MASK[sizeof(a)]); \
		b=a; \
		a=averytemporary; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a);}

#define SUB(a,b) {dd averytemporary=(a-b)& m2c::MASK[sizeof(a)]; \
		AFFECT_CF((averytemporary)>(a)); \
		a=averytemporary; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a);}

#define ADC(a,b) {dq averytemporary=(dq)a+(dq)b+(dq)CF; \
		AFFECT_CF((averytemporary)>m2c::MASK[sizeof(a)]); \
		a=averytemporary; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a);}

#define SBB(a,b) {dq averytemporary=(dq)a-(dq)b-(dq)CF; \
		AFFECT_CF((averytemporary)>m2c::MASK[sizeof(a)]); \
		a=averytemporary; \
		AFFECT_ZF(a); \
		AFFECT_SF(a,a);} 

// TODO: should affects OF, SF, ZF, AF, and PF
#define INC(a) {a+=1; \
		AFFECT_ZF(a);\
		AFFECT_SF(a,a);} 

#define DEC(a) {a-=1; \
		AFFECT_ZF(a);\
		AFFECT_SF(a,a);} 

// #num_args _ #bytes
#define IMUL1_1(a) {ax=((int8_t)al)*((int8_t)(a)); OF=CF=(ax & 0xff80)==0xff80||(ax & 0xff80)==0?false:true;}
#define IMUL1_2(a) {int32_t averytemporary=(int32_t)((int16_t)ax)*((int16_t)(a));ax=averytemporary;dx=averytemporary>>16; OF=CF=(averytemporary & 0xffff8000)==0xffff8000||(averytemporary & 0xffff8000)==0?false:true;}
#define IMUL1_4(a) {int64_t averytemporary=(int64_t)((int32_t)eax)*((int32_t)(a));eax=averytemporary;edx=averytemporary>>32; OF=CF=(averytemporary & 0xffffffff80000000)==0xffffffff80000000||(averytemporary & 0xffffffff80000000)==0?false:true;}
#define IMUL2_2(a,b) {int32_t averytemporary = ((int16_t)(a)) * ((int16_t)(b)); a=averytemporary;OF=CF=(averytemporary>= -32768)  && (averytemporary<=32767)?false:true;}
#define IMUL2_4(a,b) {int64_t averytemporary = ((int64_t)(a)) * ((int32_t)(b)); a=averytemporary;OF=CF=(averytemporary>=-((int64_t)(2147483647)+1)) && (averytemporary<=(int64_t)2147483647)?false:true;}
#define IMUL3_2(a,b,c) {int32_t averytemporary = ((int16_t)(b)) * ((int16_t)(c)); a=averytemporary;OF=CF=(averytemporary>= -32768)  && (averytemporary<=32767)?false:true;}
#define IMUL3_4(a,b,c) {int64_t averytemporary = ((int64_t)(b)) * ((int32_t)(c)); a=averytemporary;OF=CF=(averytemporary>=-((int64_t)(2147483647)+1)) && (averytemporary<=(int64_t)2147483647)?false:true;}

#define MUL1_1(a) {ax=(dw)al*(a); OF=CF=ah;}
#define MUL1_2(a) {dd averytemporary=(dd)ax*(a);ax=averytemporary;dx=averytemporary>>16; OF=CF=dx;}
#define MUL1_4(a) {dq averytemporary=(dq)eax*(a);eax=averytemporary;edx=averytemporary>>32; OF=CF=edx;}
#define MUL2_2(a,b) {dd averytemporary=(dd)(a)*(b);a=averytemporary; OF=CF=averytemporary>>16;}
#define MUL2_4(a,b) {dq averytemporary=(dq)(a)*(b);a=averytemporary; OF=CF=averytemporary>>32;}
#define MUL3_2(a,b,c) {dd averytemporary=(dd)(b)*(c);a=averytemporary; OF=CF=averytemporary>>16;}
#define MUL3_4(a,b,c) {dq averytemporary=(dq)(b)*(c);a=averytemporary; OF=CF=averytemporary>>32;}

#define IDIV1(a) {int16_t averytemporary=ax;al=averytemporary/((int8_t)a); ah=averytemporary%((int8_t)a); AFFECT_OF(false);}
#define IDIV2(a) {int32_t averytemporary=(((int32_t)(int16_t)dx)<<16)|ax; ax=averytemporary/((int16_t)a);dx=averytemporary%((int16_t)a); AFFECT_OF(false);}
#define IDIV4(a) {int64_t averytemporary=(((int64_t)(int32_t)edx)<<32)|eax;eax=averytemporary/((int32_t)a);edx=averytemporary%((int32_t)a); AFFECT_OF(false);}

#define DIV1(a) {dw averytemporary=ax;al=averytemporary/(a);ah=averytemporary%(a); AFFECT_OF(false);}
#define DIV2(a) {dd averytemporary=((((dd)dx)<<16)|ax);ax=averytemporary/(a);dx=averytemporary%(a); AFFECT_OF(false);}
#define DIV4(a) {uint64_t averytemporary=((((dq)edx)<<32)|eax);eax=averytemporary/(a);edx=averytemporary%(a); AFFECT_OF(false);}

#define NOT(a) a= ~(a);// AFFECT_ZF(a) //TODO

#define SETA(a) a=CF==0 && ZF==0;
#define SETNBE(a) a=CF==0 && ZF==0;
#define SETAE(a) a=CF==0;
#define SETNB(a) a=CF==0;
#define SETNC(a) a=CF==0;
#define SETBE(a) a=CF || ZF;
#define SETNA(a) a=CF || ZF;
#define SETB(a) a=CF;
#define SETNAE(a) a=CF;
#define SETC(a) a=CF;
#define SETL(a) a=SF!=OF;
#define SETNGE(a) a=SF!=OF;
#define SETNS(a) a=SF==0;
#define SETS(a) a=SF;
#define SETGE(a) a=SF==OF;
#define SETNL(a) a=SF==OF;
#define SETG(a) a=ZF==0 && SF==OF;
#define SETNLE(a) a=ZF==0 && SF==OF;
#define SETNE(a) a=ZF==0;
#define SETNZ(a) a=ZF==0;
#define SETLE(a) a=ZF || SF!=OF;
#define SETNG(a) a=ZF || SF!=OF;
#define SETE(a) a=ZF;
#define SETZ(a) a=ZF;
#define SETNO(x) a=!OF;
#define SETNP(x) a=!PF;
#define SETO(x) a=OF;
#define SETP(x) a=PF;


#define JE(label) if (ZF) GOTOLABEL(label)
#define JZ(label) JE(label)

#define JNE(label) if (!ZF) GOTOLABEL(label)
#define JNZ(label) JNE(label)

#define JNB(label) if (!CF) GOTOLABEL(label)
#define JAE(label) JNB(label)
#define JNC(label) JNB(label)

#define JB(label) if (CF) GOTOLABEL(label)
#define JC(label) JB(label)
#define JNAE(label) JB(label)

#define JA(label) if (!CF && !ZF) GOTOLABEL(label)
#define JNBE(label) JA(label)

#define JNA(label) if (CF || ZF) GOTOLABEL(label)
#define JBE(label) JNA(label)

#define JGE(label) if (!SF) GOTOLABEL(label)
#define JNL(label) JGE(label)

#define JG(label) if (!ZF && !SF) GOTOLABEL(label)
#define JNLE(label) JG(label)

#define JLE(label) if (ZF || SF) GOTOLABEL(label) // TODO
#define JNG(label) JLE(label)

#define JL(label) if (SF) GOTOLABEL(label) // TODO
#define JNGE(label) JL(label)

#define JCXZ(label) if (cx == 0) GOTOLABEL(label) // TODO
#define JECXZ(label) if (ecx == 0) GOTOLABEL(label) // TODO

#define JS(label) if (SF) GOTOLABEL(label)
#define JNS(label) if (!SF) GOTOLABEL(label)

/*
#if DEBUG >= 3
 #define MOV(dest,src) {log_debug("%s := %x\n",#dest, src); dest = src;}
#else
 #define MOV(dest,src) {dest = src;}
#endif
*/

#if DEBUG >= 3
#define MOV(dest,src) {m2c::log_debug("%x := (%x)\n",&dest, src); m2c::MOV_(&dest,src);}
#else
#define MOV(dest,src) {m2c::MOV_(&dest,src);}
#endif
template <class D, class S>
void MOV_(D* dest, const S& src)
{ *dest = static_cast<D>(src); }

#define LFS(dest,src) {dest = src; fs= *(dw*)((db*)&(src) + sizeof(dest));}
#define LES(dest,src) {dest = src; es = *(dw*)((db*)&(src) + sizeof(dest));}
#define LGS(dest,src) {dest = src; gs = *(dw*)((db*)&(src) + sizeof(dest));}
#define LDS(dest,src) {dest = src; ds = *(dw*)((db*)&(src) + sizeof(dest));}

#define MOVZX(dest,src) dest = src
#define MOVSX(dest,src) {if (ISNEGATIVE(src,src)) { dest = ((-1 ^ (( 1 << (bitsizeof(src)) )-1)) | src ); } else { dest = src; }}

#define BT(dest,src) {CF = dest & nthbitone(dest,src);} //TODO
#define BTS(dest,src) {CF = dest & nthbitone(dest,src); dest |= nthbitone(dest,src);}
#define BTC(dest,src) {CF = dest & nthbitone(dest,src); dest ^= nthbitone(dest,src);}
#define BTR(dest,src) {CF = dest & nthbitone(dest,src); dest &= ~(nthbitone(dest,src));}

// LEA - Load Effective Address
#define LEA(dest,src) dest = src

#define XCHG(dest,src) {dd averytemporary = (dd) dest; dest = src; src = averytemporary;}//std::swap(dest,src); TODO


#define MOVS(dest,src,s)  {dest=src; dest+=(DF==0)?s:-s; src+=(DF==0)?s:-s; }
//                        {memmove(dest,src,s); dest+=s; src+=s; } \


#define CBW {ah = ((int8_t)al) < 0?-1:0;} // TODO
#define CWD {dx = ((int16_t)ax) < 0?-1:0;}
#define CWDE {*(((dw*)&eax)+1) = ((int16_t)ax) < 0?-1:0;}

// MOVSx (DF FLAG not implemented)

#define MOVSB MOVSS(1)
#define MOVSW MOVSS(2)
#define MOVSD MOVSS(4)



#ifdef MSB_FIRST
 #define LODSB LODSS(1,3)
 #define LODSW LODSS(2,2)
#else
 #define LODSB LODSS(1,0)
 #define LODSW LODSS(2,0)
#endif

#define LODSD LODSS(4,0)


// JMP - Unconditional Jump
#define JMP(label) GOTOLABEL(label)
#define GOTOLABEL(a) {_source=__LINE__;goto a;}


#define CLD {DF=0;}
#define STD {DF=1;}

#define STC {CF=1;}
#define CLC {CF=0;}
#define CMC {CF ^= 1;}

//struct _STATE;

// directjeu nosetjmp,2
// directmenu
#define _INT(a) {m2c::asm2C_INT(_state,a); TESTJUMPTOBACKGROUND;}

#define TESTJUMPTOBACKGROUND  //if (jumpToBackGround) CALL(moveToBackGround);

void asm2C_OUT(int16_t address, int data);

#define OUT(a,b) m2c::asm2C_OUT(a,b)
int8_t asm2C_IN(int16_t data);
#define IN(a,b) a = m2c::asm2C_IN(b); TESTJUMPTOBACKGROUND

//#define PUSHF {dd averytemporary = CF+(ZF<<1)+(DF<<2)+(SF<<3); PUSH(averytemporary);}
//#define POPF {dd averytemporary; POP(averytemporary); CF=averytemporary&1; ZF=(averytemporary>>1)&1; DF=(averytemporary>>2)&1; SF=(averytemporary>>3)&1;}

#define PUSHF {PUSH( (dd) ((CF?1:0)|(PF?4:0)|(AF?0x10:0)|(ZF?0x40:0)|(SF?0x80:0)|(DF?0x400:0)|(OF?0x800:0)) );}
#define POPF {dd averytemporary; POP(averytemporary); CF=averytemporary&1;  PF=(averytemporary&4);AF=(averytemporary&0x10);ZF=(averytemporary&0x40);SF=(averytemporary&0x80);DF=(averytemporary&0x400);OF=(averytemporary&0x800);}
#define NOP

#define LAHF {ah= ((CF?1:0)|2|(PF?4:0)|(AF?0x10:0)|(ZF?0x40:0)|(SF?0x80:0)) ;}
#define SAHF {CF=ah&1; PF=ah&4; AF=ah&0x10; ZF=ah&0x40; SF=ah&0x80;}

/*
#define CALLF(label) {log_debug("before callf %d\n",stackPointer);PUSH(cs);CALL(label);}
#define CALL(label) \
	{ log_debug("before call %d\n",stackPointer); db averytemporary4='x';  \
	if (setjmp(jmpbuffer) == 0) { \
		PUSH(jmpbuffer); PUSH(averytemporary4);\
		JMP(label); \
	} }

#define RET {log_debug("before ret %d\n",stackPointer); db averytemporary5=0; POP(averytemporary5); if (averytemporary5!='x') {log_error("Stack corrupted.\n");exit(1);} \
 		POP(jmpbuffer); log_debug("after ret %d\n",stackPointer);longjmp(jmpbuffer, 0);}

#define RETN RET
#define RETF {log_debug("before ret %d\n",stackPointer); db averytemporary5=0; POP(averytemporary5); if (averytemporary5!='x') {log_error("Stack corrupted.\n");exit(1);} \
 		POP(jmpbuffer); stackPointer-=2; log_debug("after retf %d\n",stackPointer);longjmp(jmpbuffer, 0);}
*/
#define CALLF(label) {PUSH(cs);CALL(label);}
/*
#define CALL(label) \
	{ db averytemporary6='x';  \
	if (setjmp(jmpbuffer) == 0) { \
		PUSH(jmpbuffer); PUSH(averytemporary6);\
		JMP(label); \
	} }

#define RET {db averytemporary7=0; POP(averytemporary7); if (averytemporary7!='x') {log_error("Stack corrupted.\n");exit(1);} \
 		POP(jmpbuffer); longjmp(jmpbuffer, 0);}
#define RETF {db averytemporary7=0; POP(averytemporary7); if (averytemporary7!='x') {log_error("Stack corrupted.\n");exit(1);} \
 		POP(jmpbuffer); stackPointer-=2; longjmp(jmpbuffer, 0);}
*/

#if DEBUG

 #define RET {m2c::log_debug("before ret %x\n",stackPointer); m2c::MWORDSIZE averytemporary9=0; POP(averytemporary9); if (averytemporary9!='xy') {m2c::log_error("Emulated stack corruption detected %x.\n",averytemporary9);exit(1);} \
	m2c::log_debug("after ret %x\n",stackPointer); \
	--_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);return;}

 #define RETF {m2c::log_debug("before retf %x\n",stackPointer); m2c::MWORDSIZE averytemporary9=0; POP(averytemporary9); if (averytemporary9!='xy') {m2c::log_error("Emulated stack corruption detected %x.\n",averytemporary9);exit(1);} \
	dw averytemporary11;POP(averytemporary11); \
	m2c::log_debug("after retf %x\n",stackPointer); \
	--_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);return;}
#else

 #define RET {m2c::MWORDSIZE averytemporary11=0; POP(averytemporary11);  \
	return;}

 #define RETF {m2c::MWORDSIZE averytemporary11=0; POP(averytemporary11); \
	dw averytemporary2;POP(averytemporary2); \
	return;}
#endif

/*
#ifdef SINGLEPROCSTRATEGY

#if DEBUG
 #define CALL(label) \
	{ MWORDSIZE averytemporary8='xy'; PUSH(averytemporary8); \
	  log_debug("after call %x\n",stackPointer); \
	  ++_state->_indent;_state->_str=log_spaces(_state->_indent);\
	  mainproc(label, _state); \
	}
#else
 #define CALL(label) \
	{ MWORDSIZE averytemporary10='xy'; PUSH(averytemporary10); \
	  mainproc(label, _state); \
	}
#endif

#else // SINGLEPROCSTRATEGY end separate procs start
*/
#if DEBUG
 #define CALL(label) \
	{ m2c::MWORDSIZE averytemporary8='xy'; PUSH(averytemporary8); \
	  m2c::log_debug("after call %x\n",stackPointer); \
	  ++_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);\
	  label(__disp, _state); \
	}
#else
 #define CALL(label) \
	{ m2c::MWORDSIZE averytemporary10='xy'; PUSH(averytemporary10); \
	  label(__disp, _state); \
	}
#endif

//#endif // end separate procs

#define RETN RET
#define IRET RETF
//#define RETF {dw averytemporary=0; POP(averytemporary); RET;}
#define BSWAP(op1)														\
	op1 = (op1>>24)|((op1>>8)&0xFF00)|((op1<<8)&0xFF0000)|((op1<<24)&0xFF000000);

#define RDTSC {dq averytemporary = realElapsedTime(); eax=averytemporary&0xffffffff; edx=(averytemporary>32)&0xffffffff;}

#if DEBUG==2
    #define R(a) {m2c::log_debug("l:%s%d:%s\n",_state->_str,__LINE__,#a);}; a
#elif DEBUG>=3
// clean format
//    #define R(a) {log_debug("%s%x:%d:%s eax: %x ebx: %x ecx: %x edx: %x ebp: %x ds: %x esi: %x es: %x edi: %x fs: %x esp: %x\n",_state->_str,cs/*pthread_self()*/,__LINE__,#a, \
//eax, ebx, ecx, edx, ebp, ds, esi, es, edi, fs, esp);} \
//	a 

// dosbox logcpu format
    #define R(a) {m2c::log_debug("%05d %04X:%08X  %-54s EAX:%08X EBX:%08X ECX:%08X EDX:%08X ESI:%08X EDI:%08X EBP:%08X ESP:%08X DS:%04X ES:%04X FS:%04X GS:%04X SS:%04X CF:%d ZF:%d SF:%d OF:%d AF:%d PF:%d IF:%d\n", \
                         __LINE__,cs,eip,#a,       eax,     ebx,     ecx,     edx,     esi,     edi,     ebp,     esp,     ds,     es,     fs,     gs,     ss,     CF   ,ZF   ,SF   ,OF   ,AF   ,PF,   IF);} \
	a 

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

// ---------unimplemented
#define UNIMPLEMENTED m2c::log_debug("unimplemented\n");
/*
#define CMPXCHG8B(a) UNIMPLEMENTED // not in dosbox
#define CMOVA(a,b) UNIMPLEMENTED // not in dosbox
#define CMOVB(a,b) UNIMPLEMENTED
#define CMOVBE(a,b) UNIMPLEMENTED
#define CMOVG(a,b) UNIMPLEMENTED
#define CMOVGE(a,b) UNIMPLEMENTED
#define CMOVL(a,b) UNIMPLEMENTED
#define CMOVLE(a,b) UNIMPLEMENTED
#define CMOVNB(a,b) UNIMPLEMENTED
#define CMOVNO(a,b) UNIMPLEMENTED
#define CMOVNP(a,b) UNIMPLEMENTED
#define CMOVNS(a,b) UNIMPLEMENTED
#define CMOVNZ(a,b) UNIMPLEMENTED
#define CMOVO(a,b) UNIMPLEMENTED
#define CMOVP(a,b) UNIMPLEMENTED
#define CMOVS(a,b) UNIMPLEMENTED
#define CMOVZ(a,b) UNIMPLEMENTED

#define JNO(x) UNIMPLEMENTED
#define JNP(x) UNIMPLEMENTED
#define JO(x) UNIMPLEMENTED
#define JP(x) UNIMPLEMENTED


#define BSR(a,b) UNIMPLEMENTED


#define CMPXCHG UNIMPLEMENTED

#define LOOPW(x) UNIMPLEMENTED
#define LOOPWE(x) UNIMPLEMENTED
#define LOOPWNE(x) UNIMPLEMENTED
*/
#define DAA UNIMPLEMENTED
#define DAS UNIMPLEMENTED
#define CDQ UNIMPLEMENTED

#define STI UNIMPLEMENTED
#define CLI UNIMPLEMENTED

#define ORG(x) 
#define XLATB XLAT

typedef unsigned short _offsets;
/*
#ifndef __BORLANDC__
enum  _offsets : int;
#else
enum  _offsets;
#endif
*/

// Regs
struct _STATE{
       _STATE()
       {_str="";
        _indent=0;
       }

dd eax;
dd ebx;
dd ecx;
dd edx;
dd esi;
dd edi;
dd esp;
dd ebp;
dd eip;

dw cs;         
dw ds;         
dw es;         
dw fs;         
dw gs;         
dw ss;         
                      
bool CF;       
bool PF;       
bool AF;       
bool ZF;       
bool SF;       
bool DF;       
bool OF;       
bool IF;       
db _indent; 
const char *_str;
};

#define REGDEF_hl(Z)   \
uint32_t& e##Z##x = _state->e##Z##x; \
uint16_t& Z##x = *(uint16_t *)& e##Z##x; \
uint8_t& Z##l = *(uint8_t *)& e##Z##x; \
uint8_t& Z##h = *(((uint8_t *)& e##Z##x)+1); 

#define REGDEF_l(Z) \
uint32_t& e##Z = _state->e##Z; \
uint16_t& Z = *(uint16_t *)& e##Z ; \
uint8_t&  Z##l = *(uint8_t *)& e##Z ;

#define REGDEF_nol(Z) \
uint32_t& e##Z = _state->e##Z; \
uint16_t& Z = *(uint16_t *)& e##Z ;

#define X86_REGREF \
    REGDEF_hl(a);     \
    REGDEF_hl(b);     \
    REGDEF_hl(c);     \
    REGDEF_hl(d);     \
                      \
    REGDEF_l(si);     \
    REGDEF_l(di);     \
    REGDEF_l(sp);     \
    REGDEF_l(bp);     \
                      \
    REGDEF_nol(ip);   \
                      \
dw& cs = _state->cs;         \
dw& ds = _state->ds;         \
dw& es = _state->es;         \
dw& fs = _state->fs;         \
dw& gs = _state->gs;         \
dw& ss = _state->ss;         \
                      \
bool& CF = _state->CF;       \
bool& PF = _state->PF;       \
bool& AF = _state->AF;       \
bool& ZF = _state->ZF;       \
bool& SF = _state->SF;       \
bool& DF = _state->DF;       \
bool& OF = _state->OF;       \
bool& IF = _state->IF;       \
dd& stackPointer = _state->esp;\
m2c::_offsets __disp; \
dw _source;

/*
#define X86_REGREF \
dw __disp; \
dw _source;
*/
void stackDump(struct _STATE* state);
void hexDump (void *addr, int len);
void asm2C_INT(struct _STATE* state, int a);
void asm2C_init();
void asm2C_printOffsets(unsigned int offset);
double realElapsedTime(void);

void realtocurs();
dw getscan();

// SDL2 VGA
//struct SDL_Renderer;

extern db vgaPalette[256*3];

//extern chtype vga_to_curses[256];

#ifdef __cplusplus
//}
#endif

// ---------

struct /*__attribute__((__packed__))*/ Memory;
extern Memory& m;
extern db(& stack)[STACK_SIZE];
extern db(& heap)[HEAP_SIZE];
typedef void m2cf(_offsets, struct _STATE*); // common masm2c function
extern  m2cf* _ENTRY_POINT_;


#define TODB(X) (*(db*)(&(X)))
#define TODW(X) (*(dw*)(&(X)))
#define TODD(X) (*(dd*)(&(X)))
#define TODQ(X) (*(dq*)(&(X)))

}

extern struct SDL_Renderer *renderer;

#endif

