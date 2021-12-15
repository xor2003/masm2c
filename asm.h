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

struct /*__attribute__((__packed__))*/ Memory;
extern Memory& m;

class Bits{
unsigned int _CF : 1,
unused1:1,
_PF:1,
unused2:1,
_AF:1,
unused3:1,
_ZF:1,
_SF:1,
_TF:1,
_IF:1,
_DF:1,
_OF:1;
public:
#define REGDEF_flags(Z) \
    inline bool set##Z##F(bool i){return (_##Z##F=i);} \
    inline bool get##Z##F(){return _##Z##F;}
    inline void reset(){_CF=false;_PF=false;_AF=false;_ZF=false;_SF=false;_TF=false;
    _IF=false;_DF=false;_OF=false;}
 
 REGDEF_flags(C)
 REGDEF_flags(P)
 REGDEF_flags(A)
 REGDEF_flags(Z)
 REGDEF_flags(S)
 REGDEF_flags(T)
 REGDEF_flags(I)
 REGDEF_flags(D)
 REGDEF_flags(O)
};

union eflags{
 Bits bits;
 dd value;
};

typedef dd _offsets;
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
                      
eflags flags;
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
m2c::eflags& m2cflags = _state->flags;   \
dd& stackPointer = _state->esp;\
m2c::_offsets __disp; \
dw _source;

typedef void m2cf(_offsets, struct _STATE*); // common masm2c function

template<class S>
S getdata(const S& s);

template<>
inline db getdata<db>(const db& s)
{ return s; }
template<>
inline dw getdata<dw>(const dw& s)
{ return s; }
template<>
inline dd getdata<dd>(const dd& s)
{ return s; }
template<>
inline char getdata<char>(const char& s)
{ return s; }
template<>
inline short int getdata<short int>(const short int& s)
{ return s; }
template<>
inline int getdata<int>(const int& s)
{ return s; }
template<>
inline long getdata<long>(const long& s)
{ return s; }


static void setdata(db* d, db s)
{ *d = s; }
static void setdata(dw* d, dw s)
{ *d = s; }
static void setdata(dd* d, dd s)
{ *d = s; }

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

template <class D>
constexpr size_t bitsizeof(D)  // size of type in bits
{ return 8*sizeof(D); }

template <class D>
inline size_t getbit(D dest,int bit)  // get specific bit
{ return ((bit>=0)?(( (dest) >> bit)&1):0); }

template <class D>
inline size_t shiftmodule(D dest,size_t shift)  // get module of shift steps based on destiantion size in bits
{ return shift&(bitsizeof(dest)-1); }

template <class D>
inline dd nthbitone(D dest,size_t bit)  // return n-th bit with 1
{ return ( (dd)1 << shiftmodule(dest,bit)); }

template <class D, class S>
inline void bitset(D& dest, S src, size_t bit)  // set n-th bit to 1
{dest=(bit>=0)?(( (dest) & (~nthbitone(dest,bit))) | ((src&1) << bit)):dest;}

inline static db LSB(dd a) {return a&1;}  // get lower bit

template <class D>
inline db MSB(D a)  // get highest bit
{return ( (a)>>( m2c::bitsizeof(a)-1) )&1;}

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
#define raddr(s, o) m2c::raddr_(s, o)

#define realAddress(offset, segment) m2c::raddr_(segment,offset)


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
		memcpy (m2c::raddr_(ss,stackPointer), &averytemporary, sizeof (a)); \
		m2c::log_debug("after push %x\n",stackPointer);}
//		assert((m2c::raddr_(ss,stackPointer) - ((db*)&stack))>8);}

 #define POP(a) { m2c::log_debug("before pop %x\n",stackPointer);memcpy (&a, m2c::raddr_(ss,stackPointer), sizeof (a));stackPointer+=sizeof(a);}
#else
 #define PUSH(a) {dd averytemporary=a;stackPointer-=sizeof(a); \
		memcpy (m2c::raddr_(ss,stackPointer), &averytemporary, sizeof (a));}

 #define POP(a) {memcpy (&a, m2c::raddr_(ss,stackPointer), sizeof (a));stackPointer+=sizeof(a);}
#endif


#define GET_DF() m2cflags.bits.getDF()
#define GET_CF() m2cflags.bits.getCF()
#define GET_AF() m2cflags.bits.getAF()
#define GET_OF() m2cflags.bits.getOF()
#define GET_SF() m2cflags.bits.getSF()
#define GET_ZF() m2cflags.bits.getZF()
#define GET_PF() m2cflags.bits.getPF()
#define GET_IF() m2cflags.bits.getIF()
#define AFFECT_DF(a) m2cflags.bits.setDF(a)
#define AFFECT_CF(a) m2cflags.bits.setCF(a)
#define AFFECT_AF(a) m2cflags.bits.setAF(a)
#define AFFECT_OF(a) m2cflags.bits.setOF(a)
#define AFFECT_IF(a) m2cflags.bits.setIF(a)
#define ISNEGATIVE(f,a) ( (a) & (1 << (m2c::bitsizeof(f)-1)) )
#define AFFECT_SF(a) m2cflags.bits.setSF(a)
#define AFFECT_SF_(f, a) {AFFECT_SF(ISNEGATIVE(f,a));}
#define AFFECT_ZF(a) m2cflags.bits.setZF(a)
#define AFFECT_ZFifz(a) m2cflags.bits.setZF((a)==0)
#define AFFECT_PF(a) m2cflags.bits.setPF(a)


#define CMP(a, b) m2c::CMP_(a, b, m2cflags)
template <class D, class S>
inline void CMP_(D& dest, const S& src, m2c::eflags& m2cflags)
{
 dd result=(dest-src) & m2c::MASK[sizeof(dest)]; 
		AFFECT_CF(result>dest); 
            D highestbitset = (1<<( m2c::bitsizeof(dest)-1));
          AFFECT_OF(((dest ^ src) & (dest ^ result)) & highestbitset);
		AFFECT_ZFifz(result); 
		AFFECT_SF_(dest,result); 
}


#define OR(a, b) m2c::OR_(a, b, m2cflags)
template <class D, class S>
inline void OR_(D& dest, const S& src, m2c::eflags& m2cflags)
{
   D d = m2c::getdata<D>(dest);
   m2c::setdata(&dest, d | static_cast<D>(m2c::getdata<S>(src)));
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
		AFFECT_CF(0);
 }

#define XOR(a, b) m2c::XOR_(a, b, m2cflags)
template <class D, class S>
inline void XOR_(D& dest, const S& src, m2c::eflags& m2cflags)
{
   D d = m2c::getdata<D>(dest);
   m2c::setdata(&dest, d ^ static_cast<D>(m2c::getdata<S>(src)));
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
		AFFECT_CF(0);
 }

#define AND(a, b) m2c::AND_(a, b, m2cflags)
template <class D, class S>
inline void AND_(D& dest, const S& src, m2c::eflags& m2cflags)
{
   D d = m2c::getdata<D>(dest);
   m2c::setdata(&dest, d & static_cast<D>(m2c::getdata<S>(src)));
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
		AFFECT_CF(0);
 }

#define NEG(a) m2c::NEG_(a, m2cflags)
template <class D>
inline void NEG_(D& a, m2c::eflags& m2cflags)
{
AFFECT_CF((a)!=0);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF(a==highestbitset);
		a=-a;
		AFFECT_ZFifz(a); 
		AFFECT_SF_(a,a);
}

#define TEST(a, b) m2c::TEST_(a, b, m2cflags)
template <class D, class S>
inline void TEST_(D& a, const S& b, m2c::eflags& m2cflags)
{AFFECT_ZFifz((a)&(b));
		AFFECT_CF(0);
		AFFECT_SF_(a,(a)&(b));}

#define SHR(a, b) m2c::SHR_(a, b, m2cflags)
template <class D, class S>
inline void SHR_(D& a, const S& b, m2c::eflags& m2cflags)
{
	if (b) {AFFECT_CF((a>>(b-1))&1);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF(((b&0x1f)==1)?(a > highestbitset):false);
		a=a>>b;
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		}
}

#define SHL(a, b) m2c::SHL_(a, b, m2cflags)
template <class D, class S>
inline void SHL_(D& a, const S& b, m2c::eflags& m2cflags)
{
	if (b) {AFFECT_CF((a) & (1 << (m2c::bitsizeof(a)-(b))));
                D olda = a;
		a=a<<b;
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF((a ^ olda) & highestbitset);}
}

#define ROR(a, b) m2c::ROR_(a, b, m2cflags)
template <class D, class S>
inline void ROR_(D& a, S b, m2c::eflags& m2cflags)
{
	if (b) {AFFECT_CF(((a)>>(m2c::shiftmodule(a,b)-1))&1);\
		a=((a)>>(m2c::shiftmodule(a,b)) | a<<(m2c::bitsizeof(a)-(m2c::shiftmodule(a,b))));
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF((a ^ (a << 1)) & highestbitset );
		}
}

#define ROL(a, b) m2c::ROL_(a, b, m2cflags)
template <class D, class S>
inline void ROL_(D& a, S b, m2c::eflags& m2cflags)
{
	if (b) {a=(((a)<<(shiftmodule(a,b))) | (a)>>(bitsizeof(a)-(shiftmodule(a,b))));\
		AFFECT_CF(LSB(a));
		AFFECT_OF((a & 1) ^ (a >> (m2c::bitsizeof(a)-1)));
		}
}


#define RCL(a, b) m2c::RCL_(a, b, m2cflags)
template <class D, class C>
inline void RCL_(D& Destination, C Count, m2c::eflags& m2cflags)
{ 
		int TemporaryCount = Count % (m2c::bitsizeof(Destination) + 1);
			while(TemporaryCount) {
				bool TemporaryCF = m2c::MSB(Destination);
				Destination = (Destination << 1) + GET_CF();
				AFFECT_CF(TemporaryCF);
				--TemporaryCount;
			}
	AFFECT_OF(GET_CF() ^ m2c::MSB(Destination));
}

#define RCR(a, b) m2c::RCR_(a, b, m2cflags)
template <class D, class C>
inline void RCR_(D& Destination, C Count, m2c::eflags& m2cflags)
{ 
	AFFECT_OF(GET_CF() ^ m2c::MSB(Destination));
		int TemporaryCount = Count % (m2c::bitsizeof(Destination) + 1);
			while(TemporaryCount != 0) {
				bool TemporaryCF = m2c::LSB(Destination);
				Destination = (Destination >> 1) + (GET_CF() << (m2c::bitsizeof(Destination)-1));
				AFFECT_CF(TemporaryCF);
				--TemporaryCount;
			}
}

template <class D>
void SHLD_(D& Destination, D Source, size_t Count, m2c::eflags& m2cflags);

template <class D>
inline void SHRD_(D& Destination, D Source, size_t Count, m2c::eflags& m2cflags)
{ 
 if(Count != 0) {
int TCount = Count&(2*m2c::bitsizeof(Destination)-1);

if (TCount>m2c::bitsizeof(Destination)) {SHLD_(Destination, Source, 2*m2c::bitsizeof(Destination)-TCount, m2cflags);} 
else
{
		AFFECT_CF(m2c::getbit(Destination,TCount-1)); Destination>>=TCount;
		for(int i = m2c::bitsizeof(Destination) - TCount; i <= m2c::bitsizeof(Destination) - 1; ++i) 
			if (i>=0) {m2c::bitset(Destination,m2c::getbit(Source,i + TCount - m2c::bitsizeof(Destination)),i);}
		if (m2c::bitsizeof(Destination) - TCount<0)	 {AFFECT_CF(m2c::getbit(Source,TCount-m2c::bitsizeof(Destination)-1));}
}
 }
}

//template <class D>
//void SHLD_(D& op1, D op2, size_t op3, m2c::eflags& m2cflags);
/*
{ 
 if(Count != 0) {
int TCount = Count&(2*m2c::bitsizeof(Destination)-1);
if (TCount>m2c::bitsizeof(Destination)) {SHRD_(Destination, Source, 2*m2c::bitsizeof(Destination)-TCount, m2cflags);} 
else
{
AFFECT_CF(((Destination<<m2c::bitsizeof(Destination)+Source) >> (32 - Count)) & 1);
//		AFFECT_CF(m2c::getbit(Destination,m2c::bitsizeof(Destination)-TCount)); 
		Destination<<=TCount;
		for(int i = 0; i < TCount; ++i) 
			if (i>=0) {m2c::bitset(Destination,m2c::getbit(Source,m2c::bitsizeof(Destination) - TCount + i),i);}
}
 }
}
*/
//template <>
static void SHLD_(dw& Destination, dw Source, size_t Count, m2c::eflags& m2cflags)
{ 
 if(Count != 0) {
   int TCount = Count&(2*m2c::bitsizeof(Destination)-1);
   if (TCount>m2c::bitsizeof(Destination))
      {SHRD_(Destination, Source, 2*m2c::bitsizeof(Destination)-TCount, m2cflags);} 
   else
   {
      //AFFECT_CF(((Destination<<m2c::bitsizeof(Destination)+Source) >> (32 - Count)) & 1);
      AFFECT_CF(m2c::getbit(Destination,m2c::bitsizeof(Destination)-TCount));
                dw originalDest = Destination;
		Destination<<=TCount;
		for(int i = 0; i < TCount; ++i) 
			if (i>=0) {m2c::bitset(Destination,m2c::getbit(Source,m2c::bitsizeof(Destination) - TCount + i),i);}
//        AFFECT_CF((Destination >> (32 - TCount)) & 1);
      AFFECT_OF((Destination ^ originalDest) & 0x8000);
   }
               }
}

//template <>
static void SHLD_(dd& op1, dd op2, size_t op3, m2c::eflags& m2cflags)
{
	db val=op3 & 0x1F;
	if (!val) return;
	db lf_var2b=val;
        dd lf_var1d=op1;
	op1 = (lf_var1d << lf_var2b) | (op2 >> (32-lf_var2b));
        AFFECT_CF((lf_var1d >> (32 - lf_var2b)) & 1);
	AFFECT_OF((op1 ^ lf_var1d) & 0x80000000);
}

#define SHRD(a, b, c) {m2c::SHRD_(a, b, c, m2cflags);if (c) {AFFECT_ZFifz(a);AFFECT_SF_(a,a);}}
#define SHLD(a, b, c) {m2c::SHLD_(a, b, c, m2cflags);if (c) {AFFECT_ZFifz(a);AFFECT_SF_(a,a);}}

#define SAR(a,b) {if (b) {bool sign = m2c::MSB(a);\
	 int shift = (m2c::bitsizeof(a)-b);\
         shift = shift>0?shift:0;\
	 dd sigg=shift<(m2c::bitsizeof(a))?( (sign?-1:0)<<shift):0;\
         a = b>m2c::bitsizeof(a)?0:a;\
	 AFFECT_CF((a >> (b-1))&1);\
	 a=sigg | (a >> b);\
		AFFECT_ZFifz(a);\
		AFFECT_SF_(a,a);}} // TODO optimize

#define SAL(a,b) SHL(a,b)


#define DAA	{											\
	if (((al & 0x0F)>0x09) || GET_AF()) {				\
		if ((al > 0x99) || GET_CF()) {					\
			al+=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF(false);							\
		}													\
		al+=0x06;										\
		AFFECT_AF(true);								\
	} else {												\
		if ((al > 0x99) || GET_CF()) {					\
			al+=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF(false);							\
		}													\
		AFFECT_AF(false);								\
	}														\
	AFFECT_SF(al&0x80);							\
	AFFECT_ZFifz(al);}

#define DAS												\
{															\
	db osigned=al & 0x80;							\
	if (((al & 0x0f) > 9) || GET_AF()) {				\
		if ((al>0x99) || GET_CF()) {					\
			al-=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF((al<=0x05));					\
		}													\
		al-=6;											\
		AFFECT_AF(true);								\
	} else {												\
		if ((al>0x99) || GET_CF()) {					\
			al-=0x60;									\
			AFFECT_CF(true);							\
		} else {											\
			AFFECT_CF(false);							\
		}													\
		AFFECT_AF(false);								\
	}														\
	AFFECT_OF(osigned && ((al&0x80)==0));			\
	AFFECT_SF(al&0x80);							\
	AFFECT_ZFifz(al); \
}


#define SALC	{AL=GET_CF()?0xff:0;}

#define AAA	{											\
	AFFECT_SF(((al>=0x7a) && (al<=0xf9)));		\
	if ((al & 0xf) > 9) {								\
		AFFECT_OF((al&0xf0)==0x70);					\
		ax += 0x106;									\
		AFFECT_CF(true);								\
		AFFECT_ZFifz(al);						\
		AFFECT_AF(true);								\
	} else if (GET_AF()) {									\
		ax += 0x106;									\
		AFFECT_OF(false);								\
		AFFECT_CF(true);								\
		AFFECT_ZFifz(-1);								\
		AFFECT_AF(true);								\
	} else {												\
		AFFECT_OF(false);								\
		AFFECT_CF(false);								\
		AFFECT_ZFifz(al);						\
		AFFECT_AF(false);								\
	}														\
	al &= 0x0F;}

#define AAS {												\
	if ((al & 0x0f)>9) {								\
		AFFECT_SF(al>0x85);						\
		ax -= 0x106;									\
		AFFECT_OF(false);								\
		AFFECT_CF(true);								\
		AFFECT_AF(true);								\
	} else if (GET_AF()) {									\
		AFFECT_OF(((al>=0x80) && (al<=0x85)));	\
		AFFECT_SF((al<0x06) || (al>0x85));		\
		ax -= 0x106;									\
		AFFECT_CF(true);								\
		AFFECT_AF(true);								\
	} else {												\
		AFFECT_SF(al>=0x80);						\
		AFFECT_OF(false);								\
		AFFECT_CF(false);								\
		AFFECT_AF(false);								\
	}														\
	AFFECT_ZFifz((al == 0));							\
	al &= 0x0F;}

#define AAM1(x)											\
{															\
	db dv=x;											\
	if (dv!=0) {											\
		ah=al / dv;									\
		al=al % dv;									\
		AFFECT_SF(al & 0x80);						\
		AFFECT_ZFifz(al);						\
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
		AFFECT_SF(al >= 0x80);						\
		AFFECT_ZFifz(al);							\
	}

#define AAD AAD1(10)

#define ADD(a, b) m2c::ADD_(a, b, m2cflags)
template <class D, class S>
inline void ADD_(D& dest, const S& src, m2c::eflags& m2cflags)
{
 dq result=(dq)dest+(dq)src; 
		AFFECT_CF((result)>m2c::MASK[sizeof(dest)]); 
            D highestbitset = (1<<( m2c::bitsizeof(dest)-1));
          AFFECT_OF(((dest ^ src ^ highestbitset ) & (result ^ src)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}


#define XADD(a,b) {dq averytemporary=(dq)a+(dq)b; \
		AFFECT_CF((averytemporary)>m2c::MASK[sizeof(a)]); \
		a=b; \
		b=averytemporary; \
		AFFECT_ZFifz(b); \
		AFFECT_SF_(b,b);}


#define SUB(a, b) m2c::SUB_(a, b, m2cflags)
template <class D, class S>
inline void SUB_(D& dest, const S& src, m2c::eflags& m2cflags)
{
 dd result=(dest-src) & m2c::MASK[sizeof(dest)]; 
		AFFECT_CF(result>dest); 
            D highestbitset = (1<<( m2c::bitsizeof(dest)-1));
          AFFECT_OF(((dest ^ src) & (dest ^ result)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}

#define ADC(a, b) m2c::ADC_(a, b, m2cflags)
template <class D, class S>
inline void ADC_(D& dest, const S& src, m2c::eflags& m2cflags)
{
 dq result=(dq)dest+(dq)src+(dq)GET_CF(); 
		AFFECT_CF((result)>m2c::MASK[sizeof(dest)]); 
            D highestbitset = (1<<( m2c::bitsizeof(dest)-1));
          AFFECT_OF(((dest ^ src ^ highestbitset ) & (result ^ src)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}

#define SBB(a, b) m2c::SBB_(a, b, m2cflags)
template <class D, class S>
inline void SBB_(D& dest, const S& src, m2c::eflags& m2cflags)
{
 bool oldCF = GET_CF();
 dq result=((dq)dest-(dq)src-(dq)GET_CF()) & m2c::MASK[sizeof(dest)]; 
		AFFECT_CF(result>dest || (oldCF && (src==m2c::MASK[sizeof(dest)]) )); 
            D highestbitset = (1<<( m2c::bitsizeof(dest)-1));
          AFFECT_OF(((dest ^ src) & (dest ^ result)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}

// TODO: should affects OF, SF, ZF, AF, and PF
#define INC(a) m2c::INC_(a, m2cflags)
template <class D>
inline void INC_(D& a, m2c::eflags& m2cflags)
{		a+=1; 
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF(a==highestbitset);
}
            
#define DEC(a) m2c::DEC_(a, m2cflags)
template <class D>
inline void DEC_(D& a, m2c::eflags& m2cflags)
{		a-=1; 
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		D a7fff = (1<<( m2c::bitsizeof(a)-1))-1;
		AFFECT_OF(a==a7fff);
}


// #num_args _ #bytes
#define IMUL1_1(a) {ax=((int8_t)al)*((int8_t)(a)); AFFECT_OF(AFFECT_CF((ax & 0xff80)!=0xff80&&(ax & 0xff80)!=0));}
#define IMUL1_2(a) {int32_t averytemporary=(int32_t)((int16_t)ax)*((int16_t)(a));ax=averytemporary;dx=averytemporary>>16; AFFECT_OF(AFFECT_CF((averytemporary & 0xffff8000)!=0xffff8000&&(averytemporary & 0xffff8000)!=0));}
#define IMUL1_4(a) {int64_t averytemporary=(int64_t)((int32_t)eax)*((int32_t)(a));eax=averytemporary;edx=averytemporary>>32; AFFECT_OF(AFFECT_CF((averytemporary & 0xffffffff80000000)!=0xffffffff80000000&&(averytemporary & 0xffffffff80000000)!=0));}
#define IMUL2_2(a,b) {int32_t averytemporary = ((int16_t)(a)) * ((int16_t)(b)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>= -32768)  && (averytemporary<=32767)?false:true));}
#define IMUL2_4(a,b) {int64_t averytemporary = ((int64_t)(a)) * ((int32_t)(b)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>=-((int64_t)(2147483647)+1)) && (averytemporary<=(int64_t)2147483647)?false:true));}
#define IMUL3_2(a,b,c) {int32_t averytemporary = ((int16_t)(b)) * ((int16_t)(c)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>= -32768)  && (averytemporary<=32767)?false:true));}
#define IMUL3_4(a,b,c) {int64_t averytemporary = ((int64_t)(b)) * ((int32_t)(c)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>=-((int64_t)(2147483647)+1)) && (averytemporary<=(int64_t)2147483647)?false:true));}

#define MUL1_1(a) {ax=(dw)al*(a); AFFECT_OF(AFFECT_CF(ah));}
#define MUL1_2(a) {dd averytemporary=(dd)ax*(a);ax=averytemporary;dx=averytemporary>>16; AFFECT_OF(AFFECT_CF(dx));}
#define MUL1_4(a) {dq averytemporary=(dq)eax*(a);eax=averytemporary;edx=averytemporary>>32; AFFECT_OF(AFFECT_CF(edx));}
#define MUL2_2(a,b) {dd averytemporary=(dd)(a)*(b);a=averytemporary; AFFECT_OF(AFFECT_CF(averytemporary>>16));}
#define MUL2_4(a,b) {dq averytemporary=(dq)(a)*(b);a=averytemporary; AFFECT_OF(AFFECT_CF(averytemporary>>32));}
#define MUL3_2(a,b,c) {dd averytemporary=(dd)(b)*(c);a=averytemporary; AFFECT_OF(AFFECT_CF(averytemporary>>16));}
#define MUL3_4(a,b,c) {dq averytemporary=(dq)(b)*(c);a=averytemporary; AFFECT_OF(AFFECT_CF(averytemporary>>32));}

#define IDIV1(a) {int16_t averytemporary=ax;al=averytemporary/((int8_t)a); ah=averytemporary%((int8_t)a); AFFECT_OF(false);}
#define IDIV2(a) {int32_t averytemporary=(((int32_t)(int16_t)dx)<<16)|ax; ax=averytemporary/((int16_t)a);dx=averytemporary%((int16_t)a); AFFECT_OF(false);}
#define IDIV4(a) {int64_t averytemporary=(((int64_t)(int32_t)edx)<<32)|eax;eax=averytemporary/((int32_t)a);edx=averytemporary%((int32_t)a); AFFECT_OF(false);}

#define DIV1(a) {dw averytemporary=ax;al=averytemporary/(a);ah=averytemporary%(a); AFFECT_OF(false);}
#define DIV2(a) {dd averytemporary=((((dd)dx)<<16)|ax);ax=averytemporary/(a);dx=averytemporary%(a); AFFECT_OF(false);}
#define DIV4(a) {uint64_t averytemporary=((((dq)edx)<<32)|eax);eax=averytemporary/(a);edx=averytemporary%(a); AFFECT_OF(false);}

#define NOT(a) {a= ~(a);};// AFFECT_ZFifz(a) //TODO

#define SETA(a) {a=GET_CF()==0 && GET_ZF()==0;}
#define SETNBE(a) {a=GET_CF()==0 && GET_ZF()==0;}
#define SETAE(a) {a=GET_CF()==0;}
#define SETNB(a) {a=GET_CF()==0;}
#define SETNC(a) {a=GET_CF()==0;}
#define SETBE(a) {a=GET_CF() || GET_ZF();}
#define SETNA(a) {a=GET_CF() || GET_ZF();}
#define SETB(a) {a=GET_CF();}
#define SETNAE(a) {a=GET_CF();}
#define SETC(a) {a=GET_CF();}
#define SETL(a) {a=GET_SF()!=GET_OF();}
#define SETNGE(a) {a=GET_SF()!=GET_OF();}
#define SETNS(a) {a=GET_SF()==0;}
#define SETS(a) {a=GET_SF();}
#define SETGE(a) {a=GET_SF()==GET_OF();}
#define SETNL(a) {a=GET_SF()==GET_OF();}
#define SETG(a) {a=GET_ZF()==0 && GET_SF()==GET_OF();}
#define SETNLE(a) {a=GET_ZF()==0 && GET_SF()==GET_OF();}
#define SETNE(a) {a=GET_ZF()==0;}
#define SETNZ(a) {a=GET_ZF()==0;}
#define SETLE(a) {a=GET_ZF() || GET_SF()!=GET_OF();}
#define SETNG(a) {a=GET_ZF() || GET_SF()!=GET_OF();}
#define SETE(a) {a=GET_ZF();}
#define SETZ(a) {a=GET_ZF();}
#define SETNO(a) {a=!GET_OF();}
#define SETNP(a) {a=!GET_PF();}
#define SETO(a) {a=GET_OF();}
#define SETP(a) {a=GET_PF();}


#define JE(label) if (GET_ZF()) GOTOLABEL(label)
#define JZ(label) JE(label)

#define JNE(label) if (!GET_ZF()) GOTOLABEL(label)
#define JNZ(label) JNE(label)

#define JNB(label) if (!GET_CF()) GOTOLABEL(label)
#define JAE(label) JNB(label)
#define JNC(label) JNB(label)

#define JB(label) if (GET_CF()) GOTOLABEL(label)
#define JC(label) JB(label)
#define JNAE(label) JB(label)

#define JA(label) if (!GET_CF() && !GET_ZF()) GOTOLABEL(label)
#define JNBE(label) JA(label)

#define JNA(label) if (GET_CF() || GET_ZF()) GOTOLABEL(label)
#define JBE(label) JNA(label)

#define JGE(label) if (!GET_SF()) GOTOLABEL(label)
#define JNL(label) JGE(label)

#define JG(label) if (!GET_ZF() && !GET_SF()) GOTOLABEL(label)
#define JNLE(label) JG(label)

#define JLE(label) if (GET_ZF() || GET_SF()) GOTOLABEL(label) // TODO
#define JNG(label) JLE(label)

#define JL(label) if (GET_SF()) GOTOLABEL(label) // TODO
#define JNGE(label) JL(label)

#define JCXZ(label) if (cx == 0) GOTOLABEL(label) // TODO
#define JECXZ(label) if (ecx == 0) GOTOLABEL(label) // TODO

#define JS(label) if (GET_SF()) GOTOLABEL(label)
#define JNS(label) if (!GET_SF()) GOTOLABEL(label)

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
#define MOVSX(dest,src) {if (ISNEGATIVE(src,src)) { dest = ((-1 ^ (( 1 << (m2c::bitsizeof(src)) )-1)) | src ); } else { dest = src; }}

#define BT(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src));} //TODO
#define BTS(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src)); dest |= m2c::nthbitone(dest,src);}
#define BTC(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src)); dest ^= m2c::nthbitone(dest,src);}
#define BTR(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src)); dest &= ~(m2c::nthbitone(dest,src));}

// LEA - Load Effective Address
#define LEA(dest,src) dest = src

#define XCHG(dest,src) {dd averytemporary = (dd) dest; dest = src; src = averytemporary;}//std::swap(dest,src); TODO


#define MOVS(dest,src,s)  {dest=src; dest+=(GET_DF()==0)?s:-s; src+=(GET_DF()==0)?s:-s; }
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


#define CLD {AFFECT_DF(0);}
#define STD {AFFECT_DF(1);}

#define STC {AFFECT_CF(1);}
#define CLC {AFFECT_CF(0);}
#define CMC {AFFECT_CF(GET_CF() ^ 1);}

#define PUSHF {PUSH( m2cflags.value );}
#define POPF {dd averytemporary; POP(averytemporary); m2cflags.value=averytemporary;}

// directjeu nosetjmp,2
// directmenu
#define _INT(a) {m2c::asm2C_INT(_state,a); TESTJUMPTOBACKGROUND;}

#define TESTJUMPTOBACKGROUND  //if (jumpToBackGround) CALL(moveToBackGround);

void asm2C_OUT(int16_t address, int data);

#define OUT(a,b) m2c::asm2C_OUT(a,b)
int8_t asm2C_IN(int16_t data);
#define IN(a,b) a = m2c::asm2C_IN(b); TESTJUMPTOBACKGROUND

#define NOP {;}

//#define LAHF {ah= ((CF?1:0)|2|(PF?4:0)|(AF?0x10:0)|(ZF?0x40:0)|(SF?0x80:0)) ;}
//#define SAHF {CF=ah&1; PF=ah&4; AF=ah&0x10; ZF=ah&0x40; SF=ah&0x80;}
#define LAHF {ah= m2cflags.value ;}
#define SAHF {*(db*)&m2cflags.value = ah;}
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
#define CALLF(label, disp) {PUSH(cs);CALL(label, disp);}
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
	if (_state) {--_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);}return;}

 #define RETF {m2c::log_debug("before retf %x\n",stackPointer); m2c::MWORDSIZE averytemporary9=0; POP(averytemporary9); if (averytemporary9!='xy') {m2c::log_error("Emulated stack corruption detected %x.\n",averytemporary9);exit(1);} \
	dw averytemporary11;POP(averytemporary11); \
	m2c::log_debug("after retf %x\n",stackPointer); \
	if (_state) {--_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);}return;}
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
#define CALL(label, disp) {m2c::CALL_(label, _state, disp);}
static void CALL_(m2cf* label, struct _STATE* _state, _offsets _i=0) {
 X86_REGREF
	  MWORDSIZE averytemporary8='xy'; PUSH(averytemporary8);
#if DEBUG
	  m2c::log_debug("after call %x\n",stackPointer);
	  if (_state) {++_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);};
#endif
	  label(_i, _state);
 }
/*
 #define CALL(label) \
	{ m2c::MWORDSIZE averytemporary8='xy'; PUSH(averytemporary8); \
	  m2c::log_debug("after call %x\n",stackPointer); \
	  if (_state) {++_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);};\
	  label(__disp, _state); \
	}*/

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
                         __LINE__,cs,eip,#a,       eax,     ebx,     ecx,     edx,     esi,     edi,     ebp,     esp,     ds,     es,     fs,     gs,     ss,     GET_CF()   ,GET_ZF()   ,GET_SF()   ,GET_OF()   ,GET_AF()   ,GET_PF(),   GET_IF());} \
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
#define CDQ UNIMPLEMENTED

#define STI UNIMPLEMENTED
#define CLI UNIMPLEMENTED

#define ORG(x) 
#define XLATB XLAT
#define LOCK // TODO check

/*
#ifndef __BORLANDC__
enum  _offsets : int;
#else
enum  _offsets;
#endif
*/


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

extern db(& stack)[STACK_SIZE];
extern db(& heap)[HEAP_SIZE];
extern  m2cf* _ENTRY_POINT_;


#define TODB(X) (*(db*)(&(X)))
#define TODW(X) (*(dw*)(&(X)))
#define TODD(X) (*(dd*)(&(X)))
#define TODQ(X) (*(dq*)(&(X)))

}

extern struct SDL_Renderer *renderer;

#endif

