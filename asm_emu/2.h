#define STACK_CHECK

typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;

#define _jmp(label) asm_jmp(this,label)
#define _ja(label) asm_ja(this,label)
#define _jae(label) asm_jae(this,label)
#define _jb(label) asm_jb(this,label)
#define _jbe(label) asm_jbe(this,label)
#define _jc(label) asm_jc(this,label)
#define _jcxz(label) asm_jcxz(this,label)
#define _jecxz(label) asm_jecxz(this,label)
#define _je(label) asm_je(this,label)
#define _jg(label) asm_jg(this,label)
#define _jge(label) asm_jge(this,label)
#define _jl(label) asm_jl(this,label)
#define _jle(label) asm_jle(this,label)
#define _jna(label) asm_jna(this,label)
#define _jnae(label) asm_jnae(this,label)
#define _jnb(label) asm_jnb(this,label)
#define _jnbe(label) asm_jnbe(this,label)
#define _jnc(label) asm_jnc(this,label)
#define _jne(label) asm_jne(this,label)
#define _jng(label) asm_jng(this,label)
#define _jnge(label) asm_jnge(this,label)
#define _jnl(label) asm_jnl(this,label)
#define _jnle(label) asm_jnle(this,label)
#define _jno(label) asm_jno(this,label)
#ifdef X86_PF
#define _jnp(label) asm_jnp(this,label)
#endif
#define _jns(label) asm_jns(this,label)
#define _jnz(label) asm_jnz(this,label)
#define _jo(label) asm_jo(this,label)
#ifdef X86_PF
#define _jp(label) asm_jp(this,label)
#define _jpe(label) asm_jpe(this,label)
#define _jpo(label) asm_jpo(this,label)
#endif
#define _js(label) asm_js(this,label)
#define _jz(label) asm_jz(this,label)

#define _read_cf() read_cf(this->_eflags)
#define _write_cf(state) write_cf(this->_eflags, state)
#ifdef X86_PF
/* PARITY FLAG */
#define _read_pf() read_pf(this->_eflags)
#define _write_pf(state) write_pf(this->_eflags, state)
#endif
#ifdef X86_AF
/* ADJUST FLAG */
#define _read_af() read_af(this->_eflags)
#define _write_af(state) write_af(this->_eflags, state)
#endif
/* ZERO FLAG */
#define _read_zf() read_zf(this->_eflags)
#define _write_zf(state) write_zf(this->_eflags, state)
/* SIGN FLAG */
#define _read_sf() read_sf(this->_eflags)
#define _write_sf(state) write_sf(this->_eflags, state)
/* DIRECTION FLAG */
#define _read_df() read_df(this->_eflags)
#define _write_df(state) write_df(this->_eflags, state)
/* OVERFLOW FLAG */
#define _read_of() read_of(this->_eflags)
#define _write_of(state) write_of(this->_eflags, state)

