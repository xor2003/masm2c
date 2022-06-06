#include "shadowstack.h"
    extern ShadowStack shadow_stack;

#define REGDEF_hl(Z)   \
extern uint32_t e##Z##x; \
uint16_t& Z##x = *(uint16_t *)& e##Z##x; \
uint8_t& Z##l = *(uint8_t *)& e##Z##x; \
uint8_t& Z##h = *(((uint8_t *)& e##Z##x)+1); 

#define REGDEF_l(Z) \
extern uint32_t e##Z; \
uint16_t& Z = *(uint16_t *)& e##Z ; \
uint8_t&  Z##l = *(uint8_t *)& e##Z ;

#define REGDEF_nol(Z) \
extern uint32_t e##Z; \
uint16_t& Z = *(uint16_t *)& e##Z ;

extern bool CF;       
extern bool PF;       
extern bool AF;       
extern bool ZF;       
extern bool SF;       
extern bool DF;       
extern bool OF;       
extern bool IF;       
extern bool TF;       
extern dd other_flags;       

class eflags
{

 _STATE* _state;
public:
 explicit eflags(_STATE* _state):_state(_state)
 {}

dd getvalue() const noexcept
 { flagsUnion f;
  f.value=other_flags & ~0x8000; // 286+
  f.bits._CF=CF;
  f.bits._PF=PF;
  f.bits._AF=AF;
  f.bits._ZF=ZF;
  f.bits._SF=SF;
  f.bits._TF=TF;
  f.bits._IF=IF;
  f.bits._DF=DF;
  f.bits._OF=OF;
  return f.value; 
 }
void setvalue(dd v) noexcept
{
 flagsUnion f;
 f.value = v;
 other_flags=v;
 CF=f.bits._CF;
 PF=f.bits._PF;
 AF=f.bits._AF;
 ZF=f.bits._ZF;
 SF=f.bits._SF;
 TF=f.bits._TF;
 IF=f.bits._IF;
 DF=f.bits._DF;
 OF=f.bits._OF;
 }
#define REGDEF_flags(Z) \
    inline bool set##Z##F(bool i) noexcept {return Z##F=i;} \
    inline bool get##Z##F() const noexcept {return Z##F;}
    inline void reset(){
 CF=false;
 PF=false;
 AF=false;
 ZF=false;
 SF=false;
 TF=false;
 IF=false;
 DF=false;
 OF=false;
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
extern dw cs;         \
extern dw ds;         \
extern dw es;         \
extern dw fs;         \
extern dw gs;         \
extern dw ss;         \
                      \
extern bool CF;       \
extern bool PF;       \
extern bool AF;       \
extern bool ZF;       \
extern bool SF;       \
extern bool DF;       \
extern bool OF;       \
extern bool IF;       \
m2c::eflags m2cflags(_state); \
extern dd other_flags;\
dd& stackPointer = esp;\
m2c::_offsets __disp; \
dw _source;
