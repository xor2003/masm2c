#ifndef __asm_h__
#define __asm_h__

#define MYINLINE inline

#include <cstdlib>
#include <cstdarg>
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <cassert>

#include <cstring>

#include <vector>

#ifndef NOSDL
 #ifdef __LIBSDL2__
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
 #endif
#endif

extern bool from_callf;

#ifdef DOSBOX_CUSTOM
#include "json.hpp"
#include <typeinfo>

#include "custom.h"
#include "regs.h"
#include "cpu.h"
#include "mem.h"
#include "inout.h"

#include <pic.h>
#include <video.h>
#include <timer.h>
#include <vector>

extern int ticksRemain;
extern volatile bool from_interpreter;
extern bool trace_instructions;
extern bool collect_rt_info;
extern volatile bool compare_jump;

extern bool compare_instructions;

void increaseticks();
#include <callback.h>

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

#include <stdint.h>
#include <stdbool.h>

 #define MYPACKED __attribute__((__packed__))
 #define MYINT_ENUM : int
#endif


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


#ifndef DOSBOX_CUSTOM
#include "memmgr.h"
static void CPU_Exception(int){assert(0);}
typedef int Bits;
#endif

namespace m2c {

    extern struct Memory m;

    extern size_t debug;

    extern size_t counter;

    extern db _indent;
    extern const char *_str;

    extern size_t inst_size(dw cs, dd eip);

    struct _STATE;
    void stackDump(_STATE *_state=0);

    bool fix_segs();

#if DOSBOX_CUSTOM

    extern void log_regs_dbx(const char *file, int line, const char *instr, const CPU_Regs &r, const Segments &s);


    extern void execute_irqs();
    void run_hw_interrupts();

    extern void single_step();
#else
    extern void log_regs_m2c(const char *file, int line, const char *instr, _STATE* _state);
#endif

struct flagBits{
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
};

union flagsUnion{
 flagBits bits;
 dd value;
};

    typedef dd _offsets;

// Regs
struct _STATE{
        _STATE() {
            call_source=0;
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
        bool TF;
dd other_flags;
int call_source;
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

#ifndef DOSBOX_CUSTOM //masm2c

    class ShadowStack {
        struct Frame {
            const char *file;
            size_t line;
            dd sp;
            dw cs;
            dd ip;
            dd value;
            dw *pointer_;
            size_t addcounter;
            size_t remcounter;
            bool itwascall;
            size_t call_deep;
        };

        std::vector<Frame> m_ss;
        size_t m_current=0;
        bool m_itiscall=false;
        bool m_itisret=false;
        size_t m_deep=1;
    public:
        int m_needtoskipcall=0;
        bool m_active=true;
        bool m_forceactive=false;

        size_t m_currentdeep=0;

        void enable() {m_active=true;}
        void disable() {m_active=false;}
        void forceenable() {m_forceactive=true;}
        void forcedisable() {m_forceactive=false;}

        void push(_STATE *_state, dd value);

        void pop(_STATE *_state);

        void print(_STATE *_state);
        void print_frame(const Frame& f);

        void itiscall() {m_itiscall=true;}
        void itisret() {m_itisret=true;}
        bool itwascall() {return m_ss[m_current].itwascall;}

        void decreasedeep();
        bool needtoskipcalls();
        size_t getneedtoskipcallndclean(){int ret = m_needtoskipcall; m_needtoskipcall = 0; return ret;}
        void noneedreturn(){--m_needtoskipcall;}
    };

    extern ShadowStack shadow_stack;

class eflags
{

 _STATE* _state;
public:
 explicit eflags(_STATE* _state):_state(_state)
 {}

dd getvalue() const noexcept
 { flagsUnion f;
  f.value=_state->other_flags & ~0x8000; // 286+
  f.bits._CF=_state->CF;
  f.bits._PF=_state->PF;
  f.bits._AF=_state->AF;
  f.bits._ZF=_state->ZF;
  f.bits._SF=_state->SF;
  f.bits._TF=_state->TF;
  f.bits._IF=_state->IF;
  f.bits._DF=_state->DF;
  f.bits._OF=_state->OF;
  return f.value; 
 }
void setvalue(dd v) noexcept
{
 flagsUnion f;
 f.value = v;
 _state->other_flags=v;
 _state->CF=f.bits._CF;
 _state->PF=f.bits._PF;
 _state->AF=f.bits._AF;
 _state->ZF=f.bits._ZF;
 _state->SF=f.bits._SF;
 _state->TF=f.bits._TF;
 _state->IF=f.bits._IF;
 _state->DF=f.bits._DF;
 _state->OF=f.bits._OF;
 }
#define REGDEF_flags(Z) \
    inline bool set##Z##F(bool i) noexcept {return _state-> Z##F=i;} \
    inline bool get##Z##F() const noexcept {return _state-> Z##F;}
    inline void reset(){
 _state->CF=false;
 _state->PF=false;
 _state->AF=false;
 _state->ZF=false;
 _state->SF=false;
 _state->TF=false;
 _state->IF=false;
 _state->DF=false;
 _state->OF=false;
}
 
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
m2c::eflags m2cflags(_state); \
dd& stackPointer = _state->esp;\
m2c::_offsets __disp; \
dw _source;

#else // libdosbox

class eflags
{
 dd& _value;

public:
eflags(uint32_t& flags): _value((dd&)flags)
{}

dd getvalue() const noexcept
{ return _value; }
void setvalue(dd v) noexcept
{ _value=v; }
#define REGDEF_flags(Z) \
    inline bool set##Z##F(bool i) noexcept {return (reinterpret_cast<flagsUnion*>(&_value)->bits._##Z##F=i);} \
    inline bool get##Z##F() const noexcept {return reinterpret_cast<flagsUnion*>(&_value)->bits._##Z##F;}
    inline void reset(){_value=0;}
 
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

// #define m2cflags cpu_regs.flags

#define X86_REGREF \
db& al =  cpu_regs.regs[REGI_AX].byte[BL_INDEX]; \
db& ah =  cpu_regs.regs[REGI_AX].byte[BH_INDEX]; \
dw& ax =  cpu_regs.regs[REGI_AX].word[W_INDEX]; \
dd& eax =  *(dd*)&cpu_regs.regs[REGI_AX].dword[DW_INDEX]; \
 \
db& bl =  cpu_regs.regs[REGI_BX].byte[BL_INDEX]; \
db& bh =  cpu_regs.regs[REGI_BX].byte[BH_INDEX]; \
dw& bx =  cpu_regs.regs[REGI_BX].word[W_INDEX]; \
dd& ebx =  *(dd*)&cpu_regs.regs[REGI_BX].dword[DW_INDEX]; \
 \
db& cl =  cpu_regs.regs[REGI_CX].byte[BL_INDEX]; \
db& ch =  cpu_regs.regs[REGI_CX].byte[BH_INDEX]; \
dw& cx =  cpu_regs.regs[REGI_CX].word[W_INDEX]; \
dd& ecx =  *(dd*)&cpu_regs.regs[REGI_CX].dword[DW_INDEX]; \
 \
db& dl =  cpu_regs.regs[REGI_DX].byte[BL_INDEX]; \
db& dh =  cpu_regs.regs[REGI_DX].byte[BH_INDEX]; \
dw& dx =  cpu_regs.regs[REGI_DX].word[W_INDEX]; \
dd& edx =  *(dd*)&cpu_regs.regs[REGI_DX].dword[DW_INDEX]; \
 \
dw& si =  cpu_regs.regs[REGI_SI].word[W_INDEX]; \
dd& esi =  *(dd*)&cpu_regs.regs[REGI_SI].dword[DW_INDEX]; \
 \
dw& di =  cpu_regs.regs[REGI_DI].word[W_INDEX]; \
dd& edi =  *(dd*)&cpu_regs.regs[REGI_DI].dword[DW_INDEX]; \
 \
dw& sp =  cpu_regs.regs[REGI_SP].word[W_INDEX]; \
dd& esp =  *(dd*)&cpu_regs.regs[REGI_SP].dword[DW_INDEX]; \
 \
dw& bp =  cpu_regs.regs[REGI_BP].word[W_INDEX]; \
dd& ebp =  *(dd*)&cpu_regs.regs[REGI_BP].dword[DW_INDEX]; \
 \
dw& ip =  cpu_regs.ip.word[W_INDEX]; \
dd& eip =  *(dd*)&cpu_regs.ip.dword[DW_INDEX]; \
dw& cs = Segs.val[SegNames::cs]; \
dw& ds = Segs.val[SegNames::ds]; \
dw& es = Segs.val[SegNames::es]; \
dw& fs = Segs.val[SegNames::fs]; \
dw& gs = Segs.val[SegNames::gs]; \
dw& ss = Segs.val[SegNames::ss]; \
                      \
m2c::eflags m2cflags(cpu_regs.flags); \
dd& stackPointer = esp;\
m2c::_offsets __disp; \
dd _source;


#endif

typedef bool m2cf(_offsets, struct _STATE*); // common masm2c function

template<class S>
    constexpr bool isaddrbelongtom(const S *const a) {
        return ((const db *const) &m < (const db *const) a) && ((const db *const) &m + 16 * 1024 * 1024 >
                                                                (const db *const) a);
    }

    static bool isaddrbelongtovga(dd a) {
        return (0xa0000 <= a) && (a < 0xc0000);
    }
    //template<class S>
    //S getdata(const S &s);

//    extern struct Memory types;

//    static int log_debug(const char *format, ...);

    template<class S>
    inline void check_type(const S &) {
/*
#if M2CDEBUG >=4
  size_t addr = (((db*)&s)-((db*)&m2c::m));
  if (addr >= (0x1920+0x100) && addr < (0x1920+0x10000) && ( *(S*)(((db*)&m2c::types)+addr) )==0 && s !=0)
     log_debug("Read of uninit addr:%zx size:%zd %zx\n",addr-0x1920,(size_t)sizeof(S),(*(S*)(((db*)&m2c::types)+addr)) );
#endif
*/
    }

#if DOSBOX_CUSTOM
    static inline db getdata(const db &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, sizeof(s));
            return mem_readb((db *) &s - (db *) &m);
        }
        else return s;
    }

    static inline dw getdata(const dw &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, sizeof(s));
            return mem_readw((db *) &s - (db *) &m);
        }
        else return s;
    }

    static inline dd getdata(const dd &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, sizeof(s));
            return mem_readd((db *) &s - (db *) &m);
        }
        else return s;
    }

//    template<>
    static inline db getdata(const char &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, sizeof(s));
            return mem_readb((db *) &s - (db *) &m);
        }
        else return s;
    }

    static inline dw getdata(const short int &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, sizeof(s));
            return mem_readw((db *) &s - (db *) &m);
        }
        else return s;
    }

    static inline dd getdata(const int &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, sizeof(s));
            return mem_readd((db *) &s - (db *) &m);
        }
        else return s;
    }

    static inline dd getdata(const long &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, 4);
            return mem_readd((db *) &s - (db *) &m);
        }
        else return s;
    }

    static inline dd getdata(const long long &s) {
        if (m2c::isaddrbelongtom(&s)) {
            check_type(s);
            //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)&s, 4);
            return mem_readd((db *) &s - (db *) &m);
        }
        else return s;
    }

    template<class S>
    inline void set_type(const S &) {
    }

    static inline void setdata(db *d, db s) {
        if (m2c::isaddrbelongtom(d)) {
            set_type(*d);
         //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)d, sizeof(*d));
            mem_writeb((db *) d - (db *) &m, s);
        }
        else *d = s;
    }

    static inline void setdata(char *d, db s) {
        if (m2c::isaddrbelongtom(d)) {
            set_type(*d);
         //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)d, sizeof(*d));
            mem_writeb((db *) d - (db *) &m, s);
        }
        else *d = s;
    }

    static inline void setdata(dw *d, dw s) {
        if (m2c::isaddrbelongtom(d)) {
            set_type(*d);
         //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)d, sizeof(*d));
            mem_writew((db *) d - (db *) &m, s);
        }
        else *d = s;
    }

    static inline void setdata(dd *d, dd s) {
        if (m2c::isaddrbelongtom(d)) {
            set_type(*d);
         //   if (collect_rt_info) m2c::shadow_memory.collect_data((db*)d, sizeof(*d));
            mem_writed((db *) d - (db *) &m, s);
        }
        else *d = s;
    }

#else
    template<class S>
    inline void set_type(const S &) {
    }

inline db getdata(const db& s)
{ return s; }
inline dw getdata(const dw& s)
{ return s; }
inline dd getdata(const dd& s)
{ return s; }
inline char getdata(const char& s)
{ return s; }
inline short int getdata(const short int& s)
{ return s; }
inline int getdata(const int& s)
{ return s; }
inline long getdata(const long& s)
{ return s; }

    static inline void setdata(db *d, db s) {
  #if SDL_MAJOR_VERSION == 2 && !defined(NOSDL)
	if (m2c::isaddrbelongtom(d) && d < (db*)&m + 0xc0000 && d >= (db*)&m + 0xa0000)
		{ 
          dw di = d - (db*)&m;
	  SDL_SetRenderDrawColor(renderer, vgaPalette[3*s+2], vgaPalette[3*s+1], vgaPalette[3*s], 255); 
          SDL_RenderDrawPoint(renderer, di%320, di/320); \
  	  SDL_RenderPresent(renderer); 
                 } 
	else 
  #endif
        {
           *d = s;
	}
    }

    static inline void setdata(char *d, db s) {
        *d = s;
    }

    static inline void setdata(dw *d, dw s) {
           *d = s;
    }

    static inline void setdata(dd *d, dd s) {
        *d = s;
    }
#endif

extern FILE * logDebug;

// Asm functions
#ifdef DOSBOX_CUSTOM


    extern int log_debug(const char *format, ...);
//#define log_debug printf
#define log_error log_debug
#define log_info log_debug

    extern const char *log_spaces(int n);

#else
void log_error(const char *fmt, ...);
void log_debug(const char *fmt, ...);
void log_info(const char *fmt, ...);
void log_debug2(const char *fmt, ...);

const char* log_spaces(int n);

#endif

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


#define seg_offset(segment) ((dw)(((db*)(&segment)-(db*)(&m2c::m))>>4))

// DJGPP
#define MASK_LINEAR(addr)     (((size_t)addr) & 0x000FFFFF)
#define RM_TO_LINEAR(addr)    (((((size_t)addr) & 0xFFFF0000) >> 12) + (((size_t)addr) & 0xFFFF))
#define RM_OFFSET(addr)       (((size_t)addr) & 0xF)
#define RM_SEGMENT(addr)      ((((size_t)addr) >> 4) & 0xFFFF)


    extern class ShadowStack shadow_stack;

#ifdef DOSBOX_CUSTOM
#define PUSH(a) {m2c::PUSH_(a);}

    template<typename S>
    void PUSH_(S a);

    template<>
    inline void PUSH_<dw>(dw a) { fix_segs();CPU_Push16(a); }

    template<>
    inline void PUSH_<dd>(dd a) { fix_segs();CPU_Push32(a); }

    template<>
    inline void PUSH_<short int>(short int a) { fix_segs();CPU_Push16(a); }

    template<>
    inline void PUSH_<int>(int a) { fix_segs();CPU_Push32(a); }

 #define POP(a) {m2c::POP_(a);}

    inline void POP_(dw &a) { fix_segs();a = CPU_Pop16(); }

    inline void POP_(dd &a) { fix_segs();a = CPU_Pop32(); }

#else

#ifndef NO_SHADOW_STACK
 #define SHADOW_PUSH(a) m2c::shadow_stack.push(_state,(dd)(a))
 #define SHADOW_POP() m2c::shadow_stack.pop(_state)
#else
 #define SHADOW_PUSH(a)
 #define SHADOW_POP()
#endif

 #ifdef M2CDEBUG
  #define PUSH(a) {dd averytemporary=a;stackPointer-=sizeof(a); \
		memcpy (m2c::raddr_(ss,stackPointer), &averytemporary, sizeof (a)); \
		m2c::log_debug("after push %x\n",stackPointer); \
               SHADOW_PUSH(a); \
               }
//		assert((m2c::raddr_(ss,stackPointer) - ((db*)&stack))>8);

  #define POP(a) {SHADOW_POP();\
                  m2c::log_debug("before pop %x\n",stackPointer);memcpy (&a, m2c::raddr_(ss,stackPointer), sizeof (a));stackPointer+=sizeof(a);}
 #else
   #define PUSH(a) {dd averytemporary=a;stackPointer-=sizeof(a); \
		memcpy (m2c::raddr_(ss,stackPointer), &averytemporary, sizeof (a));\
               SHADOW_PUSH(a); \
               }

   #define POP(a) {SHADOW_POP();\
                   memcpy (&a, m2c::raddr_(ss,stackPointer), sizeof (a));stackPointer+=sizeof(a);}
 #endif

#endif

#define PUSHAD m2c::PUSHAD_(_state)
//pusha AX, CX, DX, BX, SP, BP, SI, DI
    static void PUSHAD_(_STATE* _state) {
        X86_REGREF
        dd oldesp = esp;
        PUSH(eax);
        PUSH(ecx);
        PUSH(edx);
        PUSH(ebx);
        PUSH(oldesp);
        PUSH(ebp);
        PUSH(esi);
        PUSH(edi);
    }
//pushad EAX, ECX, EDX, EBX, ESP, EBP, ESI, EDI
#define POPAD m2c::POPAD_(_state)

    static void POPAD_(_STATE* _state) {
        X86_REGREF
        POP(edi);
        POP(esi);
        POP(ebp);
        POP(ebx);
        POP(ebx);
        POP(edx);
        POP(ecx);
        POP(eax);
    }

#define PUSHA {dw oldsp=sp;PUSH(ax);PUSH(cx);PUSH(dx);PUSH(bx); PUSH(oldsp);PUSH(bp);PUSH(si);PUSH(di);}
#define POPA {POP(di);POP(si);POP(bp); POP(bx); POP(bx);POP(dx);POP(cx);POP(ax); }

#define GET_DF() m2cflags.getDF()
#define GET_CF() m2cflags.getCF()
#define GET_AF() m2cflags.getAF()
#define GET_OF() m2cflags.getOF()
#define GET_SF() m2cflags.getSF()
#define GET_ZF() m2cflags.getZF()
#define GET_PF() m2cflags.getPF()
#define GET_IF() m2cflags.getIF()
#define AFFECT_DF(a) m2cflags.setDF(a)
#define AFFECT_CF(a) m2cflags.setCF(a)
#define AFFECT_AF(a) m2cflags.setAF(a)
#define AFFECT_OF(a) m2cflags.setOF(a)
#define AFFECT_IF(a) m2cflags.setIF(a)
#define ISNEGATIVE(f,a) ( (a) & (1 << (m2c::bitsizeof(f)-1)) )
#define AFFECT_SF(a) m2cflags.setSF(a)
#define AFFECT_SF_(f, a) {AFFECT_SF(ISNEGATIVE(f,a));}
#define AFFECT_ZF(a) m2cflags.setZF(a)
#define AFFECT_ZFifz(a) m2cflags.setZF((a)==0)
#define AFFECT_PF(a) m2cflags.setPF(a)

#if DOSBOX_CUSTOM
#define STI {CPU_STI();}
#define CLI {CPU_CLI();}
#else
#define STI UNIMPLEMENTED
#define CLI UNIMPLEMENTED
#endif

#define CMP(a, b) m2c::CMP_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void CMP_(const D &dest_, const S &src_, m2c::eflags &m2cflags) {
//printf("\n\n%s %s ",typeid(D).name(),typeid(S).name());
        auto dest = m2c::getdata(dest_);
        auto src = m2c::getdata(src_);
        decltype(dest) result = dest - src;
		AFFECT_CF(result>dest); 
        const D highestbitset = (1 << (m2c::bitsizeof(dest) - 1));
          AFFECT_OF(((dest ^ src) & (dest ^ result)) & highestbitset);
		AFFECT_ZFifz(result); 
		AFFECT_SF_(result,result); 
}


#define OR(a, b) m2c::OR_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void OR_(D &dest, const S &src, m2c::eflags &m2cflags) {
        D result = m2c::getdata(dest) | static_cast<D>(m2c::getdata(src));
        m2c::setdata(&dest, result);
        AFFECT_ZFifz(result);
        AFFECT_SF_(result, result);
		AFFECT_CF(0);
		AFFECT_OF(0);
 }

#define XOR(a, b) m2c::XOR_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void XOR_(D &dest, const S &src, m2c::eflags &m2cflags) {
        D result = m2c::getdata(dest) ^ static_cast<D>(m2c::getdata(src));
        m2c::setdata(&dest, result);
        AFFECT_ZFifz(result);
        AFFECT_SF_(result, result);
		AFFECT_CF(0);
		AFFECT_OF(0);
 }

#define AND(a, b) m2c::AND_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void AND_(D &dest, const S &src, m2c::eflags &m2cflags) {
        D result = m2c::getdata(dest) & static_cast<D>(m2c::getdata(src));
        m2c::setdata(&dest, result);
        AFFECT_ZFifz(result);
        AFFECT_SF_(result, result);
		AFFECT_CF(0);
		AFFECT_OF(0);
 }

#define NEG(a) m2c::NEG_(a, m2cflags)
template <class D>
    MYINLINE void NEG_(D &a, m2c::eflags &m2cflags) {
AFFECT_CF((a)!=0);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF(a==highestbitset);
		a=-a;
		AFFECT_ZFifz(a); 
		AFFECT_SF_(a,a);
}

#define TEST(a, b) m2c::TEST_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void TEST_(D &a, const S &b, m2c::eflags &m2cflags) {
        AFFECT_ZFifz((a) & (b));
		AFFECT_CF(0);
		AFFECT_SF_(a,(a)&(b));
		AFFECT_OF(0);
}

#define SHR(a, b) m2c::SHR_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void SHR_(D &a, const S &b, m2c::eflags &m2cflags) {
        if (b) {
            AFFECT_CF((a >> (b - 1)) & 1);
            const D highestbitset = (1 << (m2c::bitsizeof(a) - 1));
                D res=a>>b;
            AFFECT_OF((b & 0x1f) == 1 ? (a & highestbitset) != 0 : false);
		AFFECT_ZFifz(res);
		AFFECT_SF_(res,res);
                a = res;
		}
}

#define SHL(a, b) m2c::SHL_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void SHL_(D &a, const S &b, m2c::eflags &m2cflags) {
        if (b) {
            AFFECT_CF((a) & (1 << (m2c::bitsizeof(a) - (b))));
                D olda = a;
		a=a<<b;
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
            AFFECT_OF((a ^ olda) & highestbitset);
        }
}

#define ROR(a, b) m2c::ROR_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void ROR_(D &a, S b, m2c::eflags &m2cflags) {
        if (b) {
            AFFECT_CF(((a) >> (m2c::shiftmodule(a, b) - 1)) & 1);\
		a=((a)>>(m2c::shiftmodule(a,b)) | a<<(m2c::bitsizeof(a)-(m2c::shiftmodule(a,b))));
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF((a ^ (a << 1)) & highestbitset );
		}
}

#define ROL(a, b) m2c::ROL_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void ROL_(D &a, S b, m2c::eflags &m2cflags) {
        if (b) {
            a = (((a) << (shiftmodule(a, b))) | (a) >> (bitsizeof(a) - (shiftmodule(a, b))));\
		AFFECT_CF(LSB(a));
		AFFECT_OF((a & 1) ^ (a >> (m2c::bitsizeof(a)-1)));
		}
}


#define RCL(a, b) m2c::RCL_(a, b, m2cflags)
template <class D, class C>
    MYINLINE void RCL_(D &op1, C op2, m2c::eflags &m2cflags) {
	db lf_var2b=op2%(m2c::bitsizeof(op1) + 1);
	if (!lf_var2b) return;
	D cf=GET_CF()&1;
	D lf_var1w=op1;									
        D lf_resw;
		if (lf_var2b == 1) {
			lf_resw = (lf_var1w << 1) | cf;
		} else {

			lf_resw=(lf_var1w << lf_var2b) |					
			(cf << (lf_var2b-1)) |						
			(lf_var1w >> ((m2c::bitsizeof(op1) + 1)-lf_var2b));				
		}
	op1 = lf_resw;
	AFFECT_CF((lf_var1w >> (m2c::bitsizeof(op1)-lf_var2b)) & 1);	
	AFFECT_OF(GET_CF() ^ m2c::MSB(op1));
}

#define RCR(a, b) m2c::RCR_(a, b, m2cflags)
template <class D, class C>
    MYINLINE void RCR_(D &op1, C op2, m2c::eflags &m2cflags) {
	db lf_var2b=op2%(m2c::bitsizeof(op1) + 1);
	if (!lf_var2b) return;
	D cf=GET_CF()&1;
	D lf_var1w=op1;									
        D lf_resw;
        if (lf_var2b == 1) {
			lf_resw = (lf_var1w >> 1) | (cf << (m2c::bitsizeof(op1) - 1));
        } else {
			lf_resw = (lf_var1w >> lf_var2b) | (cf << (m2c::bitsizeof(op1) - lf_var2b)) |
			(lf_var1w << ((m2c::bitsizeof(op1) + 1) - lf_var2b));
		}
	op1 = lf_resw;
	AFFECT_CF((lf_var1w >> (lf_var2b-1)) & 1);	
	D highestbitset = (1<<( m2c::bitsizeof(op1)-1));
	AFFECT_OF((lf_resw ^ (lf_resw << 1))&highestbitset);
}

template <class D>
void SHLD_(D& Destination, D Source, size_t Count, m2c::eflags& m2cflags);

template <class D>
    MYINLINE void SHRD_(D &Destination, D Source, size_t Count, m2c::eflags &m2cflags) {
 if(Count != 0) {
            size_t TCount = Count & (2 * m2c::bitsizeof(Destination) - 1);

            if (TCount > m2c::bitsizeof(Destination)) {
                SHLD_(Destination, Source, 2 * m2c::bitsizeof(Destination) - TCount, m2cflags);
            }
            else {
                AFFECT_CF(m2c::getbit(Destination, TCount - 1));
                Destination >>= TCount;
		for(int i = m2c::bitsizeof(Destination) - TCount; i <= m2c::bitsizeof(Destination) - 1; ++i) 
                    if (i >= 0) {
                        m2c::bitset(Destination, m2c::getbit(Source, i + TCount - m2c::bitsizeof(Destination)), i);
                    }
                if (m2c::bitsizeof(Destination) - TCount < 0) {
                    AFFECT_CF(m2c::getbit(Source, TCount - m2c::bitsizeof(Destination) - 1));
                }
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
    static void SHLD_(dw &Destination, dw Source, size_t Count, m2c::eflags &m2cflags) {
 if(Count != 0) {
            size_t TCount = Count & (2 * m2c::bitsizeof(Destination) - 1);
            if (TCount > m2c::bitsizeof(Destination)) {
                SHRD_(Destination, Source, 2 * m2c::bitsizeof(Destination) - TCount, m2cflags);
            }
            else {
      //AFFECT_CF(((Destination<<m2c::bitsizeof(Destination)+Source) >> (32 - Count)) & 1);
      AFFECT_CF(m2c::getbit(Destination,m2c::bitsizeof(Destination)-TCount));
                dw originalDest = Destination;
		Destination<<=TCount;
		for(int i = 0; i < TCount; ++i) 
                    if (i >= 0) {
                        m2c::bitset(Destination, m2c::getbit(Source, m2c::bitsizeof(Destination) - TCount + i), i);
                    }
//        AFFECT_CF((Destination >> (32 - TCount)) & 1);
      AFFECT_OF((Destination ^ originalDest) & 0x8000);
   }
               }
}

//template <>
    static void SHLD_(dd &op1, dd op2, size_t op3, m2c::eflags &m2cflags) {
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

/*
#define SAR(a,b) {if (b) {bool sign = m2c::MSB(a);\
	 int shift = (m2c::bitsizeof(a)-b);\
         shift = shift>0?shift:0;\
	 dd sigg=shift<(m2c::bitsizeof(a))?( (sign?-1:0)<<shift):0;\
         a = b>m2c::bitsizeof(a)?0:a;\
	 AFFECT_CF((a >> (b-1))&1);\
	 a=sigg | (a >> b);\
		AFFECT_ZFifz(a);\
		AFFECT_SF_(a,a);}} // TODO optimize
*/
#define SAR(a, b) m2c::SAR_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void SAR_(D &op1, const S &op2, m2c::eflags &m2cflags) {
if (op2){
            D lf_var1w = op1;
            db lf_var2b = op2;
        AFFECT_CF((op1>>(op2-1))&1);
	if (lf_var2b>m2c::bitsizeof(op1)) lf_var2b=m2c::bitsizeof(op1);
		D highestbitset = (1<<( m2c::bitsizeof(op1)-1));
        D lf_resw;
	if (lf_var1w & highestbitset) {
		lf_resw=(lf_var1w >> lf_var2b)|
		(((D)(-1)) << (m2c::bitsizeof(op1) - lf_var2b));
	} else {
		lf_resw=lf_var1w >> lf_var2b;
    }
	op1 = lf_resw;								
        AFFECT_ZFifz(lf_resw);
        AFFECT_SF_(lf_resw,lf_resw);
	AFFECT_OF(false);
        }
}

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
    MYINLINE void ADD_(D &dest, const S &src, m2c::eflags &m2cflags) {
 D result=dest+(D)src; 
		AFFECT_CF(result<dest); 
        const D highestbitset = (1 << (m2c::bitsizeof(dest) - 1));
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
    MYINLINE void SUB_(D &dest, const S &src, m2c::eflags &m2cflags) {
 dd result=(dest-src) & m2c::MASK[sizeof(dest)]; 
		AFFECT_CF(result>dest); 
        const D highestbitset = (1 << (m2c::bitsizeof(dest) - 1));
          AFFECT_OF(((dest ^ src) & (dest ^ result)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}

#define ADC(a, b) m2c::ADC_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void ADC_(D &dest, const S &src, m2c::eflags &m2cflags) {
 dq result=(dq)dest+(dq)src+(dq)GET_CF(); 
		AFFECT_CF((result)>m2c::MASK[sizeof(dest)]); 
        const D highestbitset = (1 << (m2c::bitsizeof(dest) - 1));
          AFFECT_OF(((dest ^ src ^ highestbitset ) & (result ^ src)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}

#define SBB(a, b) m2c::SBB_(a, b, m2cflags)
template <class D, class S>
    MYINLINE void SBB_(D &dest, const S &src, m2c::eflags &m2cflags) {
 bool oldCF = GET_CF();
 dq result=((dq)dest-(dq)src-(dq)GET_CF()) & m2c::MASK[sizeof(dest)]; 
		AFFECT_CF(result>dest || (oldCF && (src==m2c::MASK[sizeof(dest)]) )); 
        const D highestbitset = (1 << (m2c::bitsizeof(dest) - 1));
          AFFECT_OF(((dest ^ src) & (dest ^ result)) & highestbitset);
   dest = result;
		AFFECT_ZFifz(dest); 
		AFFECT_SF_(dest,dest); 
}

// TODO: should affects OF, SF, ZF, AF, and PF
#define INC(a) m2c::INC_(a, m2cflags)
template <class D>
    MYINLINE void INC_(D &a, m2c::eflags &m2cflags) {
        a += 1;
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		D highestbitset = (1<<( m2c::bitsizeof(a)-1));
		AFFECT_OF(a==highestbitset);
}
            
#define DEC(a) m2c::DEC_(a, m2cflags)
template <class D>
    MYINLINE void DEC_(D &a, m2c::eflags &m2cflags) {
        a -= 1;
		AFFECT_ZFifz(a);
		AFFECT_SF_(a,a);
		D a7fff = (1<<( m2c::bitsizeof(a)-1))-1;
		AFFECT_OF(a==a7fff);
}


// #num_args _ #bytes
#define IMUL1_1(a) {ax=((int8_t)al)*((int8_t)(a)); AFFECT_OF(AFFECT_CF((ax & 0xff80)!=0xff80&&(ax & 0xff80)!=0));AFFECT_ZFifz(al);AFFECT_SF_(al,al);}
#define IMUL1_2(a) {int32_t averytemporary=(int32_t)((int16_t)ax)*((int16_t)(a));ax=averytemporary;dx=averytemporary>>16; AFFECT_OF(AFFECT_CF((averytemporary & 0xffff8000)!=0xffff8000&&(averytemporary & 0xffff8000)!=0));AFFECT_ZFifz(ax);AFFECT_SF_(ax,ax);}
#define IMUL1_4(a) {int64_t averytemporary=(int64_t)((int32_t)eax)*((int32_t)(a));eax=averytemporary;edx=averytemporary>>32; AFFECT_OF(AFFECT_CF((averytemporary & 0xffffffff80000000)!=0xffffffff80000000&&(averytemporary & 0xffffffff80000000)!=0));AFFECT_ZFifz(eax);AFFECT_SF_(eax,eax);}
#define IMUL2_2(a,b) {int32_t averytemporary = ((int16_t)(a)) * ((int16_t)(b)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>= -32768)  && (averytemporary<=32767)?false:true));}
#define IMUL2_4(a,b) {int64_t averytemporary = ((int64_t)(a)) * ((int32_t)(b)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>=-((int64_t)(2147483647)+1)) && (averytemporary<=(int64_t)2147483647)?false:true));}
#define IMUL3_2(a,b,c) {int32_t averytemporary = ((int16_t)(b)) * ((int16_t)(c)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>= -32768)  && (averytemporary<=32767)?false:true));}
#define IMUL3_4(a,b,c) {int64_t averytemporary = ((int64_t)(b)) * ((int32_t)(c)); a=averytemporary;AFFECT_OF(AFFECT_CF((averytemporary>=-((int64_t)(2147483647)+1)) && (averytemporary<=(int64_t)2147483647)?false:true));}

#define MUL1_1(a) {ax=(dw)al*(a); AFFECT_OF(AFFECT_CF(ah));AFFECT_ZFifz(al);}
#define MUL1_2(a) {dd averytemporary=(dd)ax*(a);ax=averytemporary;dx=averytemporary>>16; AFFECT_ZFifz(ax);AFFECT_OF(AFFECT_CF(dx));}
#define MUL1_4(a) {dq averytemporary=(dq)eax*(a);eax=averytemporary;edx=averytemporary>>32; AFFECT_ZFifz(eax); AFFECT_OF(AFFECT_CF(edx));}
#define MUL2_2(a,b) {dd averytemporary=(dd)(a)*(b);a=averytemporary; AFFECT_ZFifz(a); AFFECT_OF(AFFECT_CF(averytemporary>>16));}
#define MUL2_4(a,b) {dq averytemporary=(dq)(a)*(b);a=averytemporary; AFFECT_ZFifz(a); AFFECT_OF(AFFECT_CF(averytemporary>>32));}
#define MUL3_2(a,b,c) {dd averytemporary=(dd)(b)*(c);a=averytemporary; AFFECT_ZFifz(a); AFFECT_OF(AFFECT_CF(averytemporary>>16));}
#define MUL3_4(a,b,c) {dq averytemporary=(dq)(b)*(c);a=averytemporary; AFFECT_ZFifz(a); AFFECT_OF(AFFECT_CF(averytemporary>>32));}

/*
#define IDIV1(a) {SETFLAGBIT(OF,0);if(a) {int16_t averytemporary=ax;al=averytemporary/((int8_t)a); ah=averytemporary%((int8_t)a); AFFECT_OF(false);}}
#define IDIV2(a) {SETFLAGBIT(OF,0);if(a) {int32_t averytemporary=(((int32_t)(int16_t)dx)<<16)|ax; ax=averytemporary/((int16_t)a);dx=averytemporary%((int16_t)a); AFFECT_OF(false);}}
#define IDIV4(a) {SETFLAGBIT(OF,0);if(a) {int64_t averytemporary=(((int64_t)(int32_t)edx)<<32)|eax;eax=averytemporary/((int32_t)a);edx=averytemporary%((int32_t)a); AFFECT_OF(false);}}
*/
#define IDIV1(op1)                                \
{                                                            \
    Bits val=(int8_t)(op1);                            \
    if (val==0)    CPU_Exception(0);                                \
    Bits quo=((int16_t)ax) / val;                        \
    int8_t rem=(int8_t)((int16_t)ax % val);                \
    int8_t quo8s=(int8_t)(quo&0xff);                            \
    if (quo!=(int16_t)quo8s) CPU_Exception(0);                    \
    ah=rem;                                                \
    al=quo8s;                                            \
    AFFECT_OF(false);                                    \
}


#define IDIV2(op1)                                \
{                                                            \
    Bits val=(int16_t)(op1);                            \
    if (val==0) CPU_Exception(0);                                    \
    Bits num=(int32_t)((dx<<16)|ax);                    \
    Bits quo=num/val;                                        \
    int16_t rem=(int16_t)(num % val);                            \
    int16_t quo16s=(int16_t)quo;                                \
    if (quo!=(int32_t)quo16s) CPU_Exception(0);                    \
    dx=rem;                                                \
    ax=quo16s;                                            \
    AFFECT_OF(false);                                    \
}

#define IDIV4(op1)                                \
{                                                            \
    Bits val=(int32_t)(op1);                            \
    if (val==0) CPU_Exception(0);                                    \
    int64_t num=(((uint64_t)edx)<<32)|eax;                \
    int64_t quo=num/val;                                        \
    int32_t rem=(int32_t)(num % val);                            \
    int32_t quo32s=(int32_t)(quo&0xffffffff);                    \
    if (quo!=(int64_t)quo32s) CPU_Exception(0);                    \
    edx=rem;                                            \
    eax=quo32s;                                            \
    AFFECT_OF(false);                                    \
}

#define DIV1(a) {if(a) {dw averytemporary=ax;al=averytemporary/(a);ah=averytemporary%(a); AFFECT_OF(false);}}
#define DIV2(a) {if(a) {dd averytemporary=((((dd)dx)<<16)|ax);ax=averytemporary/(a);dx=averytemporary%(a); AFFECT_OF(false);}}
#define DIV4(a) {if(a) {uint64_t averytemporary=((((dq)edx)<<32)|eax);eax=averytemporary/(a);edx=averytemporary%(a); AFFECT_OF(false);}}

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

#define JGE(label) if (GET_SF()==GET_OF()) GOTOLABEL(label)
#define JNL(label) JGE(label)

#define JG(label) if (!GET_ZF() && !GET_SF()) GOTOLABEL(label)
#define JNLE(label) JG(label)

#define JLE(label) if (GET_ZF() || GET_SF()!=GET_OF()) GOTOLABEL(label) // TODO
#define JNG(label) JLE(label)

#define JL(label) if (GET_SF()!=GET_OF()) GOTOLABEL(label) // TODO
#define JNGE(label) JL(label)

#define JCXZ(label) if (cx == 0) GOTOLABEL(label) // TODO
#define JECXZ(label) if (ecx == 0) GOTOLABEL(label) // TODO

#define JS(label) if (GET_SF()) GOTOLABEL(label)
#define JNS(label) if (!GET_SF()) GOTOLABEL(label)

#define JO(label) if (GET_OF()) GOTOLABEL(label)
#define JNO(label) if (!GET_OF()) GOTOLABEL(label)

//#define JP(label) if (GET_PF()) GOTOLABEL(label)
//#define JNP(label) if (!GET_PF()) GOTOLABEL(label)
/*
#if M2CDEBUG >= 3
 #define MOV(dest,src) {log_debug("%s := %x\n",#dest, src); dest = src;}
#else
 #define MOV(dest,src) {dest = src;}
#endif
*/

#define MOV(dest,src) {m2c::MOV_(&dest,src);}

template <class D, class S>
    MYINLINE void MOV_(D *dest, const S &src) { m2c::setdata(dest, static_cast<D>(m2c::getdata(src))); }

#define LEAVE {MOV(esp, ebp));POP(ebp);}
#define LFS(dest, src) {dw seg= *(dw*)((db*)&(src) + sizeof(dest));dest = src;fs=seg;}
#define LES(dest, src) {dw seg= *(dw*)((db*)&(src) + sizeof(dest));dest = src;es=seg;}
#define LGS(dest, src) {dw seg= *(dw*)((db*)&(src) + sizeof(dest));dest = src;gs=seg;}
#define LDS(dest, src) {dw seg= *(dw*)((db*)&(src) + sizeof(dest));dest = src;ds=seg;}

#define MOVZX(dest,src) {dest = src;}
#define MOVSX(dest,src) {if (ISNEGATIVE(src,src)) { dest = ((-1 ^ (( 1 << (m2c::bitsizeof(src)) )-1)) | src ); } else { dest = src; }}

#define BT(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src));} //TODO
#define BTS(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src)); dest |= m2c::nthbitone(dest,src);}
#define BTC(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src)); dest ^= m2c::nthbitone(dest,src);}
#define BTR(dest,src) {AFFECT_CF(dest & m2c::nthbitone(dest,src)); dest &= ~(m2c::nthbitone(dest,src));}

// LEA - Load Effective Address
#define LEA(dest,src) {dest = src;}

#define XCHG(dest, src) m2c::XCHG_(dest,src)

    template<class D>
    MYINLINE void XCHG_(D &dest, D &src) {
        D t = dest;
        dest = src;
        src = t;
    }//std::swap(dest,src); TODO


#define MOVS(dest,src,destreg,srcreg,s)  {dest=src; destreg+=(GET_DF()==0)?s:-s; srcreg+=(GET_DF()==0)?s:-s; }
//                        {memmove(dest,src,s); dest+=s; src+=s; } \


#define CBW {ah = ((int8_t)al) < 0?-1:0;} // TODO
#define CWD {dx = ((int16_t)ax) < 0?-1:0;}
#define CWDE {*(((dw*)&eax)+1) = ((int16_t)ax) < 0?-1:0;}

// MOVSx (DF FLAG not implemented)

//#define MOVSB MOVSS(1)
//#define MOVSW MOVSS(2)
//#define MOVSD MOVSS(4)



#ifdef MSB_FIRST
#define LODSB LODSS(1,3)
#define LODSW LODSS(2,2)
    //#else
    // #define LODSB LODSS(1,0)
    // #define LODSW LODSS(2,0)
#endif

//#define LODSD LODSS(4,0)



// JMP - Unconditional Jump
#define JMP(label) GOTOLABEL(label)
#define GOTOLABEL(a) {_source=__LINE__;goto a;}


#define CLD {AFFECT_DF(0);}
#define STD {AFFECT_DF(1);}

#define STC {AFFECT_CF(1);}
#define CLC {AFFECT_CF(0);}
#define CMC {AFFECT_CF(GET_CF() ^ 1);}

#define PUSHF {PUSH( (m2c::MWORDSIZE)m2cflags.getvalue() );}
#define POPF {m2c::MWORDSIZE averytemporary; POP(averytemporary); m2cflags.setvalue(averytemporary);} //286+

// directjeu nosetjmp,2
// directmenu

#define NOP {;}

#define LAHF {ah = m2cflags.getvalue();}
#define SAHF {m2cflags.setvalue(ah);}
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
#if SINGLEPROC
#define RETN(i) {m2c::RETN_(i, _state); __disp=(cs<<16)+eip;goto __dispatch_call;}
    static void RETN_(size_t i, struct _STATE *_state)
    {
        X86_REGREF
       if (debug>2) log_debug("before ret %x\n",stackPointer);
       m2c::MWORDSIZE averytemporary9=0; POP(averytemporary9);
       eip=averytemporary9;
       esp+=i;
       if (debug>2) {log_debug("after ret %x\n",stackPointer);
       m2c::_indent -= 1;
       m2c::_str = m2c::log_spaces(m2c::_indent);
          log_debug("return eip %x\n",eip);}
    }

#define RETF(i) {m2c::RETF_(i, _state); __disp=(cs<<16)+eip;goto __dispatch_call;}
    static void RETF_(size_t i, struct _STATE *_state)
    {
        X86_REGREF
            if (debug>2) log_debug("before retf %x\n",stackPointer);
       m2c::MWORDSIZE averytemporary9=0; POP(averytemporary9);
       eip=averytemporary9;
        dw averytemporary11;POP(averytemporary11); cs=averytemporary11;
       esp+=i;
       if (debug>2) {log_debug("after retf %x\n",stackPointer);
       m2c::_indent -= 1;
       m2c::_str = m2c::log_spaces(m2c::_indent);
          log_debug("return eip %x\n",eip);}
    }

#define CALL(label, disp) {m2c::CALL_(label, _state, disp);if (disp) {__disp=disp;} else {__disp=m2c::k##label;}goto __dispatch_call;}
    static void CALL_(m2cf* label, struct _STATE* _state, _offsets _i=0) {
     X86_REGREF
    from_callf=true;
          MWORDSIZE averytemporary8=eip+2; PUSH(averytemporary8);

          if (debug>2) {log_debug("after call %x\n",stackPointer);
          if (_state) {++m2c::_indent;m2c::_str=m2c::log_spaces(_state->_indent);};}
     }
#else

// #define RETN(i) {m2c::MWORDSIZE averytemporary11=0; POP(averytemporary11);  \
//	esp+=i;return true;}

struct StackPop
{
   explicit StackPop(size_t deep=1)
    :deep(deep)
   {}

   size_t deep;
};

#define RETN(i) {if (m2c::RETN_(i, _state)) {return true;} else  {__disp=(cs<<16)+eip;goto __dispatch_call;}}

    static bool RETN_(size_t i, struct _STATE *_state) {
        X86_REGREF
        if (debug>2) log_debug("before ret %x\n", stackPointer);

#ifndef NO_SHADOW_STACK
        shadow_stack.itisret();
#endif
        POP(ip);
        bool ret(true);
#ifndef NO_SHADOW_STACK
        ret = shadow_stack.itwascall();
        int skip = shadow_stack.getneedtoskipcallndclean();
        if (!ret) {
            log_error("Warning. Return address wasn't created by native CALL (found %x)\n", ip);
	}
#endif
        esp += i;
        if (debug>2) {
            log_debug("after ret %x\n", stackPointer);
            m2c::_indent -= 1;
            m2c::_str = m2c::log_spaces(m2c::_indent);
	}
#ifndef NO_SHADOW_STACK
        if (skip>0) 
          {
log_debug("~~will throw exception skip call=%d\n",skip);

throw StackPop(skip);
}
        if (ret) {m2c::shadow_stack.decreasedeep();}
#endif
	return(ret);
    }

//#define RETF(i) {m2c::RETF_(i); if (ip=='xy') {m2c::shadow_stack.decreasedeep(); return true;} else  {return __dispatch_call((cs<<16)+eip,0);}}
#define RETF(i) {m2c::RETF_(i, _state); return true;}

    static bool RETF_(size_t i, struct _STATE *_state) {
        X86_REGREF
        if (debug>2) log_debug("before retf %x\n", stackPointer);

//        m2c::MWORDSIZE averytemporary9 = 0;
//        log_error("~~RETF before 1pop\n");
#ifndef NO_SHADOW_STACK
        shadow_stack.itisret();
#endif
        POP(ip);
        bool ret(true);
#ifndef NO_SHADOW_STACK
        ret = shadow_stack.itwascall();
        if (!ret) {
            log_error("Warning. Return address wasn't created by native CALL (found %x)\n", ip);
//            m2c::stackDump();
            exit(1);
        }
//        log_error("~~RETF after 1pop\n");
//        bool need = shadow_stack.needtoskipcalls();
        int skip = shadow_stack.getneedtoskipcallndclean();
#endif
//        log_error("~~RETF before 2pop\n");
        POP(cs);
//        log_error("~~RETF after 2pop\n");
        esp += i;
log_debug("new %x:%x\n", cs,ip);
        if (debug>2) {
            log_debug("after retf %x\n", stackPointer);
            m2c::_indent -= 1;
            m2c::_str = m2c::log_spaces(m2c::_indent);
        }
#ifndef NO_SHADOW_STACK
        if (skip>0) 
          {
log_debug("~~will throw exception skip call=%d\n",skip);
//shadow_stack.print(0);
throw StackPop(skip);
          }

        m2c::shadow_stack.decreasedeep();
#endif
        return ret;
    }
#define CALL(label, disp) {m2c::CALL_(label, _state, disp);}
    static bool CALL_(m2cf *label, struct _STATE *_state, _offsets _i = 0) {
 X86_REGREF
        from_callf = true;
#ifndef NO_SHADOW_STACK
        shadow_stack.itiscall();
#endif
//        m2c::MWORDSIZE averytemporary8 = 'xy';
        m2c::MWORDSIZE return_addr = ip;
#if DOSBOX_CUSTOM
        if (compare_instructions) ip+=inst_size(cs,eip);
#endif
        PUSH(return_addr);

        if (debug>2) {
            log_debug("after call %x\n", stackPointer);
// 	  if (_state) {++_state->_indent;_state->_str=m2c::log_spaces(_state->_indent);};
            m2c::_indent += 1;
            m2c::_str = m2c::log_spaces(m2c::_indent);
        }
        _state->call_source = 2;
        try{
	  label(_i, _state);
 if(return_addr != ip&& ((dw)(ip - return_addr)) > 5 ) {
  log_error("~~Return address not equal to call addr %x %x\n",return_addr,ip);
return false;
 }
        }
        catch(const StackPop& ex)
        {
#ifndef NO_SHADOW_STACK
shadow_stack.decreasedeep();
             if (ex.deep > 0)
             {  log_debug("~~Rethrowing upper\n");
		throw StackPop(ex.deep-1);
             }
             else
             {  log_debug("~~Finished with skipping calls\n");

             }
#endif
        }
       return true;
    }


#endif

#define RET RETN(0)
/*
#define IRET {m2c::MWORDSIZE averytemporary11=0; POP(averytemporary11); eip=averytemporary11;\
	POP(cs); \
        POPF; \
	return;}
*/
#if DOSBOX_CUSTOM
#define IRET {m2c::fix_segs();CPU_IRET(false,0);m2c::execute_irqs();return true;}
#else
#define IRET RETF(0)
#endif
//#define RETF {dw averytemporary=0; POP(averytemporary); RET;}
#define BSWAP(op1)														\
	op1 = (op1>>24)|((op1>>8)&0xFF00)|((op1<<8)&0xFF0000)|((op1<<24)&0xFF000000);

#define RDTSC {dq averytemporary = realElapsedTime(); eax=averytemporary&0xffffffff; edx=(averytemporary>32)&0xffffffff;}


#if M2CDEBUG>0
// clean format
//    #define R(a) {log_debug("%s%x:%d:%s eax: %x ebx: %x ecx: %x edx: %x ebp: %x ds: %x esi: %x es: %x edi: %x fs: %x esp: %x\n",_state->_str,cs/*pthread_self()*/,__LINE__,#a, \
//eax, ebx, ecx, edx, ebp, ds, esi, es, edi, fs, esp);} \
//	a 

// dosbox logcpu format
    #define R(a) {m2c::log_regs_m2c(__FILE__,__LINE__,#a,_state);a;}
    #define J(a) {m2c::log_regs_m2c(__FILE__,__LINE__,#a,_state);a;}
    #define T(a) {m2c::log_regs_m2c(__FILE__,__LINE__,#a,_state);a;}
    #define X(a) {m2c::log_regs_m2c(__FILE__,__LINE__,#a,_state);a;}

#else
    #define R(a) a
    #define J(a) R(a)
    #define T(a) R(a)
    #define X(a) R(a)
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

#ifdef DOSBOX_CUSTOM
#define _INT(num) {m2c::fix_segs();CALLBACK_RunRealInt(num);}

#define OUT(port, value) m2c::OUT_(port,value)

    static void OUT_(dw port, db value) { IO_WriteB(port, value); }

    static void OUT_(dw port, dw value) { IO_WriteW(port, value); }

#define IN(res, port) m2c::IN_(res, port)

    static void IN_(db &res, dw port) { res = IO_ReadB(port); }

    static void IN_(dw &res, dw port) { res = IO_ReadW(port); }

#else

#define _INT(a) {m2c::asm2C_INT(_state,a);}

void asm2C_OUT(int16_t address, int data,_STATE* _state);

#define OUT(a,b) m2c::asm2C_OUT(a,b,_state)
int8_t asm2C_IN(int16_t data,_STATE* _state);
#define IN(a,b) a = m2c::asm2C_IN(b,_state);
#endif

#define XLATP(x) {al = *(x + al);}
#if DOSBOX_CUSTOM
    void mycopy(db *, db *, size_t, const char *);
    void cmpHexDump(void *addr1, void *addr2, int len);
#endif

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

#if DOSBOX_CUSTOM
    extern bool Jstart(const char *file, int line, const char *instr);

    extern void Jend();

    extern bool Tstart(const char *file, int line, const char *instr);

    extern void Tend(const char *file, int line, const char *instr);

    extern bool Xstart(const char *file, int line, const char *instr);

    extern void Xend(const char *file, int line, const char *instr);

#endif
    extern void interpret_unknown_callf(dw cs, dd eip, db source=0);

//extern void log_regs(int line, const char * instr, struct _STATE* _state);

    static bool oldZF = false;
    static bool repForMov = false;

#define TODB(X) (*(db*)(&(X)))
#define TODW(X) (*(dw*)(&(X)))
#define TODD(X) (*(dd*)(&(X)))
#define TODQ(X) (*(dq*)(&(X)))

} // namespace m2c

#if DOSBOX_CUSTOM
extern void print_instruction(Bit16u newcs, Bit32u newip);
extern void print_instruction_direct(Bit16u newcs, Bit32u newip);
#endif

extern struct SDL_Renderer *renderer;

#endif

