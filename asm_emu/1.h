#include "asm_emu/x86.h"
#include "asm_emu/2.h"
static struct assembler_state_t asm_cpu_state;
static inline void _adc(const uint8_t src, uint8_t *dst)
{
	 asm_adcb(&asm_cpu_state, src, dst);
}

static inline void _adc(const uint32_t src, uint32_t *dst)
{
	 asm_adcl(&asm_cpu_state, src, dst);
}

static inline void _adc(const uint16_t src, uint16_t *dst)
{
	 asm_adcw(&asm_cpu_state, src, dst);
}

static inline void _add(const uint8_t src, uint8_t *dst)
{
	 asm_addb(&asm_cpu_state, src, dst);
}

static inline void _add(const uint32_t src, uint32_t *dst)
{
	 asm_addl(&asm_cpu_state, src, dst);
}

static inline void _add(const uint16_t src, uint16_t *dst)
{
	 asm_addw(&asm_cpu_state, src, dst);
}

static inline void _and(const uint8_t src, uint8_t *dst)
{
	 asm_andb(&asm_cpu_state, src, dst);
}

static inline void _and(const uint32_t src, uint32_t *dst)
{
	 asm_andl(&asm_cpu_state, src, dst);
}

static inline void _and(const uint16_t src, uint16_t *dst)
{
	 asm_andw(&asm_cpu_state, src, dst);
}

static inline void _cmp(uint8_t src, uint8_t dst)
{
	 asm_cmpb(&asm_cpu_state, src, dst);
}

static inline void _cmp(uint32_t src, uint32_t dst)
{
	 asm_cmpl(&asm_cpu_state, src, dst);
}

static inline void _cmp(uint16_t src, uint16_t dst)
{
	 asm_cmpw(&asm_cpu_state, src, dst);
}

static inline void _dec(uint8_t *dst)
{
	 asm_decb(&asm_cpu_state, dst);
}

static inline void _dec(uint32_t *dst)
{
	 asm_decl(&asm_cpu_state, dst);
}

static inline void _dec(uint16_t *dst)
{
	 asm_decw(&asm_cpu_state, dst);
}

static inline void _div(const uint8_t src)
{
	 asm_divb(&asm_cpu_state, src);
}

static inline void _div(const uint32_t src)
{
	 asm_divl(&asm_cpu_state, src);
}

static inline void _div(const uint16_t src)
{
	 asm_divw(&asm_cpu_state, src);
}

static inline void _finit()
{
	 asm_finit(&asm_cpu_state);;
}

static inline void _imul_1_(const uint8_t src)
{
	 asm_imul_1_b(&asm_cpu_state, src);
}

static inline void _imul_1_(uint32_t src)
{
	 asm_imul_1_l(&asm_cpu_state, src);
}

static inline void _imul_1_(const uint16_t src)
{
	 asm_imul_1_w(&asm_cpu_state, src);
}

static inline void _imul_2_(const uint8_t src, uint8_t *dst)
{
	 asm_imul_2_b(&asm_cpu_state, src, dst);
}

static inline void _imul_2_(uint32_t src, uint32_t *dst)
{
	 asm_imul_2_l(&asm_cpu_state, src, dst);
}

static inline void _imul_2_(const uint16_t src, uint16_t *dst)
{
	 asm_imul_2_w(&asm_cpu_state, src, dst);
}

static inline void _inc(uint8_t *dst)
{
	 asm_incb(&asm_cpu_state, dst);
}

static inline void _inc(uint32_t *dst)
{
	 asm_incl(&asm_cpu_state, dst);
}

static inline void _inc(uint16_t *dst)
{
	 asm_incw(&asm_cpu_state, dst);
}

static inline void _lea(uint8_t src, uint8_t *dst) {*dst = src;}
{
	 asm_leab(&asm_cpu_state, src, dst) {*dst = src;};;
}

static inline void _lea(uint32_t src, uint32_t *dst) {*dst = src;}
{
	 asm_leal(&asm_cpu_state, src, dst) {*dst = src;};;
}

static inline void _lea(uint16_t src, uint16_t *dst) {*dst = src;}
{
	 asm_leaw(&asm_cpu_state, src, dst) {*dst = src;};;
}

static inline void _mov(uint8_t src, uint8_t *dst) {*dst = src;}
{
	 asm_movb(&asm_cpu_state, src, dst) {*dst = src;};;
}

static inline void _mov(uint32_t src, uint32_t *dst) {*dst = src;}
{
	 asm_movl(&asm_cpu_state, src, dst) {*dst = src;};;
}

static inline void _mov(uint16_t src, uint16_t *dst) {*dst = src;}
{
	 asm_movw(&asm_cpu_state, src, dst) {*dst = src;};;
}

static inline void _neg(uint8_t *dst)
{
	 asm_negb(&asm_cpu_state, dst);
}

static inline void _neg(uint32_t *dst)
{
	 asm_negl(&asm_cpu_state, dst);
}

static inline void _neg(uint16_t *dst)
{
	 asm_negw(&asm_cpu_state, dst);
}

static inline void _or(const uint8_t src, uint8_t *dst)
{
	 asm_orb(&asm_cpu_state, src, dst);
}

static inline void _or(const uint32_t src, uint32_t *dst)
{
	 asm_orl(&asm_cpu_state, src, dst);
}

static inline void _or(const uint16_t src, uint16_t *dst)
{
	 asm_orw(&asm_cpu_state, src, dst);
}

static inline void _pop(uint8_t *dst)
{
	 asm_popb(&asm_cpu_state, dst);
}

static inline void _pop(uint32_t *dst)
{
	 asm_popl(&asm_cpu_state, dst);
}

static inline void _pop(uint16_t *dst)
{
	 asm_popw(&asm_cpu_state, dst);
}

static inline void _push(const uint8_t src)
{
	 asm_pushb(&asm_cpu_state, src);
}

static inline void _push(const uint32_t src)
{
	 asm_pushl(&asm_cpu_state, src);
}

static inline void _push(const uint16_t src)
{
	 asm_pushw(&asm_cpu_state, src);
}

static inline void _rep_stos()
{
	 asm_rep_stosb(&asm_cpu_state);
}

static inline void _rep_stos()
{
	 asm_rep_stosl(&asm_cpu_state);
}

static inline void _rep_stos()
{
	 asm_rep_stosw(&asm_cpu_state);
}

static inline void _sahf()
{
	 asm_sahf(&asm_cpu_state);
}

static inline void _sar(uint8_t count, uint8_t *dst)
{
	 asm_sarb(&asm_cpu_state, count, dst);
}

static inline void _sar(uint8_t count, uint32_t *dst)
{
	 asm_sarl(&asm_cpu_state, count, dst);
}

static inline void _sar(uint8_t count, uint16_t *dst)
{
	 asm_sarw(&asm_cpu_state, count, dst);
}

static inline void _sbb(uint8_t src, uint8_t *dst)
{
	 asm_sbbb(&asm_cpu_state, src, dst);
}

static inline void _sbb(uint32_t src, uint32_t *dst)
{
	 asm_sbbl(&asm_cpu_state, src, dst);
}

static inline void _sbb(uint16_t src, uint16_t *dst)
{
	 asm_sbbw(&asm_cpu_state, src, dst);
}

static inline void _shl(uint8_t count, uint8_t *dst)
{
	 asm_shlb(&asm_cpu_state, count, dst);
}

static inline void _shld(uint8_t count, const uint32_t src, uint32_t *dst)
{
	 asm_shldl(&asm_cpu_state, count, src, dst);
}

static inline void _shl(uint8_t count, uint32_t *dst)
{
	 asm_shll(&asm_cpu_state, count, dst);
}

static inline void _shl(uint8_t count, uint16_t *dst)
{
	 asm_shlw(&asm_cpu_state, count, dst);
}

static inline void _shr(uint8_t count, uint8_t *dst)
{
	 asm_shrb(&asm_cpu_state, count, dst);
}

static inline void _shrd(uint8_t count, const uint32_t src, uint32_t *dst)
{
	 asm_shrdl(&asm_cpu_state, count, src, dst);
}

static inline void _shr(uint8_t count, uint32_t *dst)
{
	 asm_shrl(&asm_cpu_state, count, dst);
}

static inline void _shr(uint8_t count, uint16_t *dst)
{
	 asm_shrw(&asm_cpu_state, count, dst);
}

static inline void _stos()
{
	 asm_stosb(&asm_cpu_state);
}

static inline void _stos()
{
	 asm_stosl(&asm_cpu_state);
}

static inline void _stos()
{
	 asm_stosw(&asm_cpu_state);
}

static inline void _sub(const uint8_t src, uint8_t *dst)
{
	 asm_subb(&asm_cpu_state, src, dst);
}

static inline void _sub(const uint8_t src, uint8_t *dst)
{
	 asm_subb(&asm_cpu_state, src, dst);;
}

static inline void _sub(const uint32_t src, uint32_t *dst)
{
	 asm_subl(&asm_cpu_state, src, dst);
}

static inline void _sub(const uint32_t src, uint32_t *dst)
{
	 asm_subl(&asm_cpu_state, src, dst);;
}

static inline void _sub(const uint16_t src, uint16_t *dst)
{
	 asm_subw(&asm_cpu_state, src, dst);
}

static inline void _sub(const uint16_t src, uint16_t *dst)
{
	 asm_subw(&asm_cpu_state, src, dst);;
}

static inline void _test(uint8_t src1, uint8_t src2)
{
	 asm_testb(&asm_cpu_state, src1, src2);
}

static inline void _test(uint32_t src1, uint32_t src2)
{
	 asm_testl(&asm_cpu_state, src1, src2);
}

static inline void _test(uint16_t src1, uint16_t src2)
{
	 asm_testw(&asm_cpu_state, src1, src2);
}

static inline void _update_af(uint32_t *_eflags, const uint32_t newreg, const uint32_t oldreg)
{
	 asm_update_af(_eflags, newreg, oldreg);
}

static inline void _update_pf(uint32_t *_eflags, const uint32_t reg)
{
	 asm_update_pf(_eflags, reg);
}

static inline void _xor(const uint8_t src, uint8_t *dst)
{
	 asm_xorb(&asm_cpu_state, src, dst);
}

static inline void _xor(const uint32_t src, uint32_t *dst)
{
	 asm_xorl(&asm_cpu_state, src, dst);
}

static inline void _xor(const uint16_t src, uint16_t *dst)
{
	 asm_xorw(&asm_cpu_state, src, dst);
}

