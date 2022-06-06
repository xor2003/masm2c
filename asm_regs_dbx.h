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
