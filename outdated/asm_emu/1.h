#include "asm_emu/x86.h"
#include "asm_emu/2.h"
//static struct assembler_state_t asm_cpu_state;
class asm_emu : public assembler_state_t
{
public:

inline void _adc(uint8_t &dst, const uint8_t src)
{
	 asm_adcb(this, src, &dst);
}

inline void _adc(uint32_t &dst, const uint32_t src)
{
	 asm_adcl(this, src, &dst);
}

inline void _adc(uint16_t &dst, const uint16_t src)
{
	 asm_adcw(this, src, &dst);
}

inline void _add(uint8_t &dst, const uint8_t src)
{
	 asm_addb(this, src, &dst);
}

inline void _add(uint32_t &dst, const uint32_t src)
{
	 asm_addl(this, src, &dst);
}

inline void _add(uint16_t &dst, const uint16_t src)
{
	 asm_addw(this, src, &dst);
}

inline void _and(uint8_t &dst, const uint8_t src)
{
	 asm_andb(this, src, &dst);
}

inline void _and(uint32_t &dst, const uint32_t src)
{
	 asm_andl(this, src, &dst);
}

inline void _and(uint16_t &dst, const uint16_t src)
{
	 asm_andw(this, src, &dst);
}

inline void _cmp(uint8_t dst, uint8_t src)
{
	 asm_cmpb(this, src, dst);
}

inline void _cmp(uint32_t dst, uint32_t src)
{
	 asm_cmpl(this, src, dst);
}

inline void _cmp(uint16_t dst, uint16_t src)
{
	 asm_cmpw(this, src, dst);
}

inline void _dec(uint8_t &dst)
{
	 asm_decb(this, &dst);
}

inline void _dec(uint32_t &dst)
{
	 asm_decl(this, &dst);
}

inline void _dec(uint16_t &dst)
{
	 asm_decw(this, &dst);
}

inline void _div(const uint8_t src)
{
	 asm_divb(this, src);
}

inline void _div(const uint32_t src)
{
	 asm_divl(this, src);
}

inline void _div(const uint16_t src)
{
	 asm_divw(this, src);
}

inline void _finit()
{
	 asm_finit(this);;
}

inline void _mul(const uint8_t src)
{
	 asm_imul_1_b(this, src);
}

inline void _mul(uint32_t src)
{
	 asm_imul_1_l(this, src);
}

inline void _mul(const uint16_t src)
{
	 asm_imul_1_w(this, src);
}

inline void _mul(uint8_t &dst, const uint8_t src)
{
	 asm_imul_2_b(this, src, &dst);
}

inline void _mul(uint32_t &dst, uint32_t src)
{
	 asm_imul_2_l(this, src, &dst);
}

inline void _mul(uint16_t &dst, const uint16_t src)
{
	 asm_imul_2_w(this, src, &dst);
}

inline void _inc(uint8_t &dst)
{
	 asm_incb(this, &dst);
}

inline void _inc(uint32_t &dst)
{
	 asm_incl(this, &dst);
}

inline void _inc(uint16_t &dst)
{
	 asm_incw(this, &dst);
}

inline void _lea(uint8_t &dst, uint8_t src)
{
	 asm_leab(this, src, &dst);
}

inline void _lea(uint32_t &dst, uint32_t src)
{
	 asm_leal(this, src, &dst);
}

inline void _lea(uint16_t &dst, uint16_t src)
{
	 asm_leaw(this, src, &dst);
}

inline void _mov(uint8_t &dst, uint8_t src)
{
	 asm_movb(this, src, &dst);
}

inline void _mov(uint32_t &dst, uint32_t src)
{
	 asm_movl(this, src, &dst);
}

inline void _mov(uint16_t &dst, uint16_t src)
{
	 asm_movw(this, src, &dst);
}

inline void _neg(uint8_t &dst)
{
	 asm_negb(this, &dst);
}

inline void _neg(uint32_t &dst)
{
	 asm_negl(this, &dst);
}

inline void _neg(uint16_t &dst)
{
	 asm_negw(this, &dst);
}

inline void _or(uint8_t &dst, const uint8_t src)
{
	 asm_orb(this, src, &dst);
}

inline void _or(uint32_t &dst, const uint32_t src)
{
	 asm_orl(this, src, &dst);
}

inline void _or(uint16_t &dst, const uint16_t src)
{
	 asm_orw(this, src, &dst);
}

inline void _pop(uint8_t &dst)
{
	 asm_popb(this, &dst);
}

inline void _pop(uint32_t &dst)
{
	 asm_popl(this, &dst);
}

inline void _pop(uint16_t &dst)
{
	 asm_popw(this, &dst);
}

inline void _push(const uint8_t src)
{
	 asm_pushb(this, src);
}

inline void _push(const uint32_t src)
{
	 asm_pushl(this, src);
}

inline void _push(const uint16_t src)
{
	 asm_pushw(this, src);
}

inline void _rep_stosb()
{
	 asm_rep_stosb(this);
}

inline void _rep_stosd()
{
	 asm_rep_stosl(this);
}

inline void _rep_stosw()
{
	 asm_rep_stosw(this);
}

inline void _sahf()
{
	 asm_sahf(this);
}

inline void _sar(uint8_t &dst, uint8_t count)
{
	 asm_sarb(this, count, &dst);
}

inline void _sar(uint32_t &dst, uint8_t count)
{
	 asm_sarl(this, count, &dst);
}

inline void _sar(uint16_t &dst, uint8_t count)
{
	 asm_sarw(this, count, &dst);
}

inline void _sbb(uint8_t &dst, uint8_t src)
{
	 asm_sbbb(this, src, &dst);
}

inline void _sbb(uint32_t &dst, uint32_t src)
{
	 asm_sbbl(this, src, &dst);
}

inline void _sbb(uint16_t &dst, uint16_t src)
{
	 asm_sbbw(this, src, &dst);
}

inline void _shl(uint8_t &dst, uint8_t count)
{
	 asm_shlb(this, count, &dst);
}

inline void _shld(uint32_t &dst, const uint32_t src, uint8_t count)
{
	 asm_shldl(this, count, src, &dst);
}

inline void _shl(uint32_t &dst, uint8_t count)
{
	 asm_shll(this, count, &dst);
}

inline void _shl(uint16_t &dst, uint8_t count)
{
	 asm_shlw(this, count, &dst);
}

inline void _shr(uint8_t &dst, uint8_t count)
{
	 asm_shrb(this, count, &dst);
}

inline void _shrd(uint32_t &dst, const uint32_t src, uint8_t count)
{
	 asm_shrdl(this, count, src, &dst);
}

inline void _shr(uint32_t &dst, uint8_t count)
{
	 asm_shrl(this, count, &dst);
}

inline void _shr(uint16_t &dst, uint8_t count)
{
	 asm_shrw(this, count, &dst);
}

inline void _stosb()
{
	 asm_stosb(this);
}

inline void _stosd()
{
	 asm_stosl(this);
}

inline void _stosw()
{
	 asm_stosw(this);
}

inline void _sub(uint8_t &dst, const uint8_t src)
{
	 asm_subb(this, src, &dst);
}

inline void _sub(uint32_t &dst, const uint32_t src)
{
	 asm_subl(this, src, &dst);
}

inline void _sub(uint16_t &dst, const uint16_t src)
{
	 asm_subw(this, src, &dst);
}

inline void _test(uint8_t src1, uint8_t src2)
{
	 asm_testb(this, src1, src2);
}

inline void _test(uint32_t src1, uint32_t src2)
{
	 asm_testl(this, src1, src2);
}

inline void _test(uint16_t src1, uint16_t src2)
{
	 asm_testw(this, src1, src2);
}

inline void _xor(uint8_t &dst, const uint8_t src)
{
	 asm_xorb(this, src, &dst);
}

inline void _xor(uint32_t &dst, const uint32_t src)
{
	 asm_xorl(this, src, &dst);
}

inline void _xor(uint16_t &dst, const uint16_t src)
{
	 asm_xorw(this, src, &dst);
}

};
