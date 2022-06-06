#include "shadowstack.h"
    extern ShadowStack shadow_stack;

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
