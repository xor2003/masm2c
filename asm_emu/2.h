typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;

#define _jmp(label) asm_jmp(asm_cpu_state,label)
#define _ja(label) asm_ja(asm_cpu_state,label)
#define _jae(label) asm_jae(asm_cpu_state,label)
#define _jb(label) asm_jb(asm_cpu_state,label)
#define _jbe(label) asm_jbe(asm_cpu_state,label)
#define _jc(label) asm_jc(asm_cpu_state,label)
#define _jcxz(label) asm_jcxz(asm_cpu_state,label)
#define _jecxz(label) asm_jecxz(asm_cpu_state,label)
#define _je(label) asm_je(asm_cpu_state,label)
#define _jg(label) asm_jg(asm_cpu_state,label)
#define _jge(label) asm_jge(asm_cpu_state,label)
#define _jl(label) asm_jl(asm_cpu_state,label)
#define _jle(label) asm_jle(asm_cpu_state,label)
#define _jna(label) asm_jna(asm_cpu_state,label)
#define _jnae(label) asm_jnae(asm_cpu_state,label)
#define _jnb(label) asm_jnb(asm_cpu_state,label)
#define _jnbe(label) asm_jnbe(asm_cpu_state,label)
#define _jnc(label) asm_jnc(asm_cpu_state,label)
#define _jne(label) asm_jne(asm_cpu_state,label)
#define _jng(label) asm_jng(asm_cpu_state,label)
#define _jnge(label) asm_jnge(asm_cpu_state,label)
#define _jnl(label) asm_jnl(asm_cpu_state,label)
#define _jnle(label) asm_jnle(asm_cpu_state,label)
#define _jno(label) asm_jno(asm_cpu_state,label)
#ifdef X86_PF
#define _jnp(label) asm_jnp(asm_cpu_state,label)
#endif
#define _jns(label) asm_jns(asm_cpu_state,label)
#define _jnz(label) asm_jnz(asm_cpu_state,label)
#define _jo(label) asm_jo(asm_cpu_state,label)
#ifdef X86_PF
#define _jp(label) asm_jp(asm_cpu_state,label)
#define _jpe(label) asm_jpe(asm_cpu_state,label)
#define _jpo(label) asm_jpo(asm_cpu_state,label)
#endif
#define _js(label) asm_js(asm_cpu_state,label)
#define _jz(label) asm_jz(asm_cpu_state,label)
