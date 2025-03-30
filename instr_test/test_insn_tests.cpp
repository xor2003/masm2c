#include <gtest/gtest.h>

//--------------------------------------------
#define _BITS 32
#define _PROTECTED_MODE 1

#include <asm.h>

namespace m2c{
struct Memory{
db stack[STACK_SIZE];
db heap[HEAP_SIZE];
};

struct Memory m;
db(& stack)[STACK_SIZE]=m.stack;
db(& heap)[HEAP_SIZE]=m.heap;
}

namespace m2c{ m2cf* _ENTRY_POINT_ = 0;}


m2c::_STATE sstate;
m2c::_STATE* _state=&sstate;
X86_REGREF

bool from_callf;

namespace m2c{
void log_debug(const char *fmt, ...){printf("unimp ");}
void log_error(const char *fmt, ...){printf("unimp ");}
//void log_spaces(int){}
}
//--------------------------------------------


namespace m2c
{
class EmulatedInstructionsTest : public ::testing::Test {
 protected:
      m2c::_STATE state; 
      m2c::_STATE* _state=&state; 

    void SetUp() override {
       memset(&state, 0, sizeof(m2c::_STATE)); 
    }

    template <typename D, typename S>
    void TestADD(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      ADD(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestADC(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      CF = initial_CF;
      ADC(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestSUB(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      SUB(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestSBB(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      CF = initial_CF;
      SBB(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestOR(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      OR(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, false);
      ASSERT_EQ(OF, false);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestAND(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      AND(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, false);
      ASSERT_EQ(OF, false);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestXOR(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      XOR(dest, src);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, false);
      ASSERT_EQ(OF, false);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D>
    void TestINC(D initial_value, D expected_result, bool expected_OF, bool expected_SF, bool expected_ZF) {
      X86_REGREF
      D value = initial_value;
      INC(value);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D>
    void TestDEC(D initial_value, D expected_result, bool expected_OF, bool expected_SF, bool expected_ZF) {
      X86_REGREF
      D value = initial_value;
      DEC(value);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestSHR(D initial_value, S shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      SHR(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestSHL(D initial_value, S shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      SHL(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestROR(D initial_value, S shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      ROR(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
    }

    template <typename D, typename S>
    void TestROL(D initial_value, S shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      ROL(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
    }

    template <typename D, typename C>
    void TestRCL(D initial_value, C shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      CF = initial_CF;
      RCL(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
    }

    template <typename D, typename C>
    void TestRCR(D initial_value, C shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      CF = initial_CF;
      RCR(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
    }

    template <typename D>
    void TestSHLD(D initial_dest, D src, size_t count, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      SHLD(dest, src, count);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D>
    void TestSHRD(D initial_dest, D src, size_t count, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D dest = initial_dest;
      SHRD(dest, src, count);
      ASSERT_EQ(dest, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D, typename S>
    void TestSAR(D initial_value, S shift_amount, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      SAR(value, shift_amount);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D>
    void TestNEG(D initial_value, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF, bool initial_CF = false) {
      X86_REGREF
      D value = initial_value;
      NEG(value);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }

    template <typename D>
    void TestNOT(D initial_value, D expected_result, bool expected_CF, bool expected_SF, bool expected_ZF) {
      X86_REGREF
      D value = initial_value;
      NOT(value);
      ASSERT_EQ(value, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }
};

  TEST_F(EmulatedInstructionsTest, ADD) {

    TestADD<dd>(0x12345678, 0x0812fada, 0x1a475152, false, false, false, false, false);
    

    TestADD<dw>(0x12345678, 0x0812fada, 0x12345152, true, false, false, false, false);
    

    TestADD<db>(0x12345678, 0x0812fada, 0x12345652, true, false, false, false, false);
    

    TestADD<dd>(0x00012341, 0x00012341, 0x00024682, false, false, false, false, false);
    

    TestADD<dw>(0x00012341, 0x00012341, 0x00014682, false, false, false, false, false);
    

    TestADD<db>(0x00012341, 0x00012341, 0x00012382, false, true, true, false, false);
    

    TestADD<dd>(0x00012341, 0xfffedcbf, 0x00000000, true, false, false, true, false);
    

    TestADD<dw>(0x00012341, 0xfffedcbf, 0x00010000, true, false, false, true, false);
    

    TestADD<db>(0x00012341, 0xfffedcbf, 0x00012300, true, false, false, true, false);
    

    TestADD<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestADD<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestADD<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestADD<dd>(0xffffffff, 0xffffffff, 0xfffffffe, true, false, true, false, false);
    

    TestADD<dw>(0xffffffff, 0xffffffff, 0xfffffffe, true, false, true, false, false);
    

    TestADD<db>(0xffffffff, 0xffffffff, 0xfffffffe, true, false, true, false, false);
    

    TestADD<dd>(0xffffffff, 0x00000001, 0x00000000, true, false, false, true, false);
    

    TestADD<dw>(0xffffffff, 0x00000001, 0xffff0000, true, false, false, true, false);
    

    TestADD<db>(0xffffffff, 0x00000001, 0xffffff00, true, false, false, true, false);
    

    TestADD<dd>(0xffffffff, 0x00000002, 0x00000001, true, false, false, false, false);
    

    TestADD<dw>(0xffffffff, 0x00000002, 0xffff0001, true, false, false, false, false);
    

    TestADD<db>(0xffffffff, 0x00000002, 0xffffff01, true, false, false, false, false);
    

    TestADD<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestADD<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestADD<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestADD<dd>(0x7fffffff, 0x00000001, 0x80000000, false, true, true, false, false);
    

    TestADD<dw>(0x7fffffff, 0x00000001, 0x7fff0000, true, false, false, true, false);
    

    TestADD<db>(0x7fffffff, 0x00000001, 0x7fffff00, true, false, false, true, false);
    

    TestADD<dd>(0x7fffffff, 0xffffffff, 0x7ffffffe, true, false, false, false, false);
    

    TestADD<dw>(0x7fffffff, 0xffffffff, 0x7ffffffe, true, false, true, false, false);
    

    TestADD<db>(0x7fffffff, 0xffffffff, 0x7ffffffe, true, false, true, false, false);
    

    TestADD<dd>(0x80000000, 0xffffffff, 0x7fffffff, true, true, false, false, false);
    

    TestADD<dw>(0x80000000, 0xffffffff, 0x8000ffff, false, false, true, false, false);
    

    TestADD<db>(0x80000000, 0xffffffff, 0x800000ff, false, false, true, false, false);
    

    TestADD<dd>(0x80000000, 0x00000001, 0x80000001, false, false, true, false, false);
    

    TestADD<dw>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestADD<db>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestADD<dd>(0x80000000, 0xfffffffe, 0x7ffffffe, true, true, false, false, false);
    

    TestADD<dw>(0x80000000, 0xfffffffe, 0x8000fffe, false, false, true, false, false);
    

    TestADD<db>(0x80000000, 0xfffffffe, 0x800000fe, false, false, true, false, false);
    

    TestADD<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestADD<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestADD<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestADD<dd>(0x12347fff, 0x00000001, 0x12348000, false, false, false, false, false);
    

    TestADD<dw>(0x12347fff, 0x00000001, 0x12348000, false, true, true, false, false);
    

    TestADD<db>(0x12347fff, 0x00000001, 0x12347f00, true, false, false, true, false);
    

    TestADD<dd>(0x12347fff, 0xffffffff, 0x12347ffe, true, false, false, false, false);
    

    TestADD<dw>(0x12347fff, 0xffffffff, 0x12347ffe, true, false, false, false, false);
    

    TestADD<db>(0x12347fff, 0xffffffff, 0x12347ffe, true, false, true, false, false);
    

    TestADD<dd>(0x12348000, 0xffffffff, 0x12347fff, true, false, false, false, false);
    

    TestADD<dw>(0x12348000, 0xffffffff, 0x12347fff, true, true, false, false, false);
    

    TestADD<db>(0x12348000, 0xffffffff, 0x123480ff, false, false, true, false, false);
    

    TestADD<dd>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestADD<dw>(0x12348000, 0x00000001, 0x12348001, false, false, true, false, false);
    

    TestADD<db>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestADD<dd>(0x12348000, 0xfffffffe, 0x12347ffe, true, false, false, false, false);
    

    TestADD<dw>(0x12348000, 0xfffffffe, 0x12347ffe, true, true, false, false, false);
    

    TestADD<db>(0x12348000, 0xfffffffe, 0x123480fe, false, false, true, false, false);
    

    TestADD<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestADD<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestADD<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestADD<dd>(0x12347f7f, 0x00000001, 0x12347f80, false, false, false, false, false);
    

    TestADD<dw>(0x12347f7f, 0x00000001, 0x12347f80, false, false, false, false, false);
    

    TestADD<db>(0x12347f7f, 0x00000001, 0x12347f80, false, true, true, false, false);
    

    TestADD<dd>(0x12347f7f, 0xffffffff, 0x12347f7e, true, false, false, false, false);
    

    TestADD<dw>(0x12347f7f, 0xffffffff, 0x12347f7e, true, false, false, false, false);
    

    TestADD<db>(0x12347f7f, 0xffffffff, 0x12347f7e, true, false, false, false, false);
    

    TestADD<dd>(0x12348080, 0xffffffff, 0x1234807f, true, false, false, false, false);
    

    TestADD<dw>(0x12348080, 0xffffffff, 0x1234807f, true, false, true, false, false);
    

    TestADD<db>(0x12348080, 0xffffffff, 0x1234807f, true, true, false, false, false);
    

    TestADD<dd>(0x12348080, 0x00000001, 0x12348081, false, false, false, false, false);
    

    TestADD<dw>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestADD<db>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestADD<dd>(0x12348080, 0xfffffffe, 0x1234807e, true, false, false, false, false);
    

    TestADD<dw>(0x12348080, 0xfffffffe, 0x1234807e, true, false, true, false, false);
    

    TestADD<db>(0x12348080, 0xfffffffe, 0x1234807e, true, true, false, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, SUB) {

    TestSUB<dd>(0x12345678, 0x0812fada, 0x0a215b9e, false, false, false, false, false);
    

    TestSUB<dw>(0x12345678, 0x0812fada, 0x12345b9e, true, false, false, false, false);
    

    TestSUB<db>(0x12345678, 0x0812fada, 0x1234569e, true, true, true, false, false);
    

    TestSUB<dd>(0x00012341, 0x00012341, 0x00000000, false, false, false, true, false);
    

    TestSUB<dw>(0x00012341, 0x00012341, 0x00010000, false, false, false, true, false);
    

    TestSUB<db>(0x00012341, 0x00012341, 0x00012300, false, false, false, true, false);
    

    TestSUB<dd>(0x00012341, 0xfffedcbf, 0x00024682, true, false, false, false, false);
    

    TestSUB<dw>(0x00012341, 0xfffedcbf, 0x00014682, true, false, false, false, false);
    

    TestSUB<db>(0x00012341, 0xfffedcbf, 0x00012382, true, true, true, false, false);
    

    TestSUB<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSUB<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dd>(0xffffffff, 0xffffffff, 0x00000000, false, false, false, true, false);
    

    TestSUB<dw>(0xffffffff, 0xffffffff, 0xffff0000, false, false, false, true, false);
    

    TestSUB<db>(0xffffffff, 0xffffffff, 0xffffff00, false, false, false, true, false);
    

    TestSUB<dd>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestSUB<dw>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestSUB<db>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestSUB<dd>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestSUB<dw>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestSUB<db>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestSUB<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestSUB<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestSUB<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestSUB<dd>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, false, false, false);
    

    TestSUB<dw>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, true, false, false);
    

    TestSUB<db>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, true, false, false);
    

    TestSUB<dd>(0x7fffffff, 0xffffffff, 0x80000000, true, true, true, false, false);
    

    TestSUB<dw>(0x7fffffff, 0xffffffff, 0x7fff0000, false, false, false, true, false);
    

    TestSUB<db>(0x7fffffff, 0xffffffff, 0x7fffff00, false, false, false, true, false);
    

    TestSUB<dd>(0x80000000, 0xffffffff, 0x80000001, true, false, true, false, false);
    

    TestSUB<dw>(0x80000000, 0xffffffff, 0x80000001, true, false, false, false, false);
    

    TestSUB<db>(0x80000000, 0xffffffff, 0x80000001, true, false, false, false, false);
    

    TestSUB<dd>(0x80000000, 0x00000001, 0x7fffffff, false, true, false, false, false);
    

    TestSUB<dw>(0x80000000, 0x00000001, 0x8000ffff, true, false, true, false, false);
    

    TestSUB<db>(0x80000000, 0x00000001, 0x800000ff, true, false, true, false, false);
    

    TestSUB<dd>(0x80000000, 0xfffffffe, 0x80000002, true, false, true, false, false);
    

    TestSUB<dw>(0x80000000, 0xfffffffe, 0x80000002, true, false, false, false, false);
    

    TestSUB<db>(0x80000000, 0xfffffffe, 0x80000002, true, false, false, false, false);
    

    TestSUB<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestSUB<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestSUB<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestSUB<dd>(0x12347fff, 0x00000001, 0x12347ffe, false, false, false, false, false);
    

    TestSUB<dw>(0x12347fff, 0x00000001, 0x12347ffe, false, false, false, false, false);
    

    TestSUB<db>(0x12347fff, 0x00000001, 0x12347ffe, false, false, true, false, false);
    

    TestSUB<dd>(0x12347fff, 0xffffffff, 0x12348000, true, false, false, false, false);
    

    TestSUB<dw>(0x12347fff, 0xffffffff, 0x12348000, true, true, true, false, false);
    

    TestSUB<db>(0x12347fff, 0xffffffff, 0x12347f00, false, false, false, true, false);
    

    TestSUB<dd>(0x12348000, 0xffffffff, 0x12348001, true, false, false, false, false);
    

    TestSUB<dw>(0x12348000, 0xffffffff, 0x12348001, true, false, true, false, false);
    

    TestSUB<db>(0x12348000, 0xffffffff, 0x12348001, true, false, false, false, false);
    

    TestSUB<dd>(0x12348000, 0x00000001, 0x12347fff, false, false, false, false, false);
    

    TestSUB<dw>(0x12348000, 0x00000001, 0x12347fff, false, true, false, false, false);
    

    TestSUB<db>(0x12348000, 0x00000001, 0x123480ff, true, false, true, false, false);
    

    TestSUB<dd>(0x12348000, 0xfffffffe, 0x12348002, true, false, false, false, false);
    

    TestSUB<dw>(0x12348000, 0xfffffffe, 0x12348002, true, false, true, false, false);
    

    TestSUB<db>(0x12348000, 0xfffffffe, 0x12348002, true, false, false, false, false);
    

    TestSUB<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<dd>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestSUB<dw>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestSUB<db>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestSUB<dd>(0x12347f7f, 0xffffffff, 0x12347f80, true, false, false, false, false);
    

    TestSUB<dw>(0x12347f7f, 0xffffffff, 0x12347f80, true, false, false, false, false);
    

    TestSUB<db>(0x12347f7f, 0xffffffff, 0x12347f80, true, true, true, false, false);
    

    TestSUB<dd>(0x12348080, 0xffffffff, 0x12348081, true, false, false, false, false);
    

    TestSUB<dw>(0x12348080, 0xffffffff, 0x12348081, true, false, true, false, false);
    

    TestSUB<db>(0x12348080, 0xffffffff, 0x12348081, true, false, true, false, false);
    

    TestSUB<dd>(0x12348080, 0x00000001, 0x1234807f, false, false, false, false, false);
    

    TestSUB<dw>(0x12348080, 0x00000001, 0x1234807f, false, false, true, false, false);
    

    TestSUB<db>(0x12348080, 0x00000001, 0x1234807f, false, true, false, false, false);
    

    TestSUB<dd>(0x12348080, 0xfffffffe, 0x12348082, true, false, false, false, false);
    

    TestSUB<dw>(0x12348080, 0xfffffffe, 0x12348082, true, false, true, false, false);
    

    TestSUB<db>(0x12348080, 0xfffffffe, 0x12348082, true, false, true, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, XOR) {

    TestXOR<dd>(0x12345678, 0x0812fada, 0x1a26aca2, false, false, false, false, false);
    

    TestXOR<dw>(0x12345678, 0x0812fada, 0x1234aca2, false, false, true, false, false);
    

    TestXOR<db>(0x12345678, 0x0812fada, 0x123456a2, false, false, true, false, false);
    

    TestXOR<dd>(0x00012341, 0x00012341, 0x00000000, false, false, false, true, false);
    

    TestXOR<dw>(0x00012341, 0x00012341, 0x00010000, false, false, false, true, false);
    

    TestXOR<db>(0x00012341, 0x00012341, 0x00012300, false, false, false, true, false);
    

    TestXOR<dd>(0x00012341, 0xfffedcbf, 0xfffffffe, false, false, true, false, false);
    

    TestXOR<dw>(0x00012341, 0xfffedcbf, 0x0001fffe, false, false, true, false, false);
    

    TestXOR<db>(0x00012341, 0xfffedcbf, 0x000123fe, false, false, true, false, false);
    

    TestXOR<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestXOR<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestXOR<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestXOR<dd>(0xffffffff, 0xffffffff, 0x00000000, false, false, false, true, false);
    

    TestXOR<dw>(0xffffffff, 0xffffffff, 0xffff0000, false, false, false, true, false);
    

    TestXOR<db>(0xffffffff, 0xffffffff, 0xffffff00, false, false, false, true, false);
    

    TestXOR<dd>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestXOR<dw>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestXOR<db>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestXOR<dd>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestXOR<dw>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestXOR<db>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestXOR<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestXOR<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestXOR<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestXOR<dd>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, false, false, false);
    

    TestXOR<dw>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, true, false, false);
    

    TestXOR<db>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, true, false, false);
    

    TestXOR<dd>(0x7fffffff, 0xffffffff, 0x80000000, false, false, true, false, false);
    

    TestXOR<dw>(0x7fffffff, 0xffffffff, 0x7fff0000, false, false, false, true, false);
    

    TestXOR<db>(0x7fffffff, 0xffffffff, 0x7fffff00, false, false, false, true, false);
    

    TestXOR<dd>(0x80000000, 0xffffffff, 0x7fffffff, false, false, false, false, false);
    

    TestXOR<dw>(0x80000000, 0xffffffff, 0x8000ffff, false, false, true, false, false);
    

    TestXOR<db>(0x80000000, 0xffffffff, 0x800000ff, false, false, true, false, false);
    

    TestXOR<dd>(0x80000000, 0x00000001, 0x80000001, false, false, true, false, false);
    

    TestXOR<dw>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestXOR<db>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestXOR<dd>(0x80000000, 0xfffffffe, 0x7ffffffe, false, false, false, false, false);
    

    TestXOR<dw>(0x80000000, 0xfffffffe, 0x8000fffe, false, false, true, false, false);
    

    TestXOR<db>(0x80000000, 0xfffffffe, 0x800000fe, false, false, true, false, false);
    

    TestXOR<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestXOR<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestXOR<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestXOR<dd>(0x12347fff, 0x00000001, 0x12347ffe, false, false, false, false, false);
    

    TestXOR<dw>(0x12347fff, 0x00000001, 0x12347ffe, false, false, false, false, false);
    

    TestXOR<db>(0x12347fff, 0x00000001, 0x12347ffe, false, false, true, false, false);
    

    TestXOR<dd>(0x12347fff, 0xffffffff, 0xedcb8000, false, false, true, false, false);
    

    TestXOR<dw>(0x12347fff, 0xffffffff, 0x12348000, false, false, true, false, false);
    

    TestXOR<db>(0x12347fff, 0xffffffff, 0x12347f00, false, false, false, true, false);
    

    TestXOR<dd>(0x12348000, 0xffffffff, 0xedcb7fff, false, false, true, false, false);
    

    TestXOR<dw>(0x12348000, 0xffffffff, 0x12347fff, false, false, false, false, false);
    

    TestXOR<db>(0x12348000, 0xffffffff, 0x123480ff, false, false, true, false, false);
    

    TestXOR<dd>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestXOR<dw>(0x12348000, 0x00000001, 0x12348001, false, false, true, false, false);
    

    TestXOR<db>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestXOR<dd>(0x12348000, 0xfffffffe, 0xedcb7ffe, false, false, true, false, false);
    

    TestXOR<dw>(0x12348000, 0xfffffffe, 0x12347ffe, false, false, false, false, false);
    

    TestXOR<db>(0x12348000, 0xfffffffe, 0x123480fe, false, false, true, false, false);
    

    TestXOR<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestXOR<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestXOR<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestXOR<dd>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestXOR<dw>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestXOR<db>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestXOR<dd>(0x12347f7f, 0xffffffff, 0xedcb8080, false, false, true, false, false);
    

    TestXOR<dw>(0x12347f7f, 0xffffffff, 0x12348080, false, false, true, false, false);
    

    TestXOR<db>(0x12347f7f, 0xffffffff, 0x12347f80, false, false, true, false, false);
    

    TestXOR<dd>(0x12348080, 0xffffffff, 0xedcb7f7f, false, false, true, false, false);
    

    TestXOR<dw>(0x12348080, 0xffffffff, 0x12347f7f, false, false, false, false, false);
    

    TestXOR<db>(0x12348080, 0xffffffff, 0x1234807f, false, false, false, false, false);
    

    TestXOR<dd>(0x12348080, 0x00000001, 0x12348081, false, false, false, false, false);
    

    TestXOR<dw>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestXOR<db>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestXOR<dd>(0x12348080, 0xfffffffe, 0xedcb7f7e, false, false, true, false, false);
    

    TestXOR<dw>(0x12348080, 0xfffffffe, 0x12347f7e, false, false, false, false, false);
    

    TestXOR<db>(0x12348080, 0xfffffffe, 0x1234807e, false, false, false, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, AND) {

    TestAND<dd>(0x12345678, 0x0812fada, 0x00105258, false, false, false, false, false);
    

    TestAND<dw>(0x12345678, 0x0812fada, 0x12345258, false, false, false, false, false);
    

    TestAND<db>(0x12345678, 0x0812fada, 0x12345658, false, false, false, false, false);
    

    TestAND<dd>(0x00012341, 0x00012341, 0x00012341, false, false, false, false, false);
    

    TestAND<dw>(0x00012341, 0x00012341, 0x00012341, false, false, false, false, false);
    

    TestAND<db>(0x00012341, 0x00012341, 0x00012341, false, false, false, false, false);
    

    TestAND<dd>(0x00012341, 0xfffedcbf, 0x00000001, false, false, false, false, false);
    

    TestAND<dw>(0x00012341, 0xfffedcbf, 0x00010001, false, false, false, false, false);
    

    TestAND<db>(0x00012341, 0xfffedcbf, 0x00012301, false, false, false, false, false);
    

    TestAND<dd>(0xffffffff, 0x00000000, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0xffffffff, 0x00000000, 0xffff0000, false, false, false, true, false);
    

    TestAND<db>(0xffffffff, 0x00000000, 0xffffff00, false, false, false, true, false);
    

    TestAND<dd>(0xffffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestAND<dw>(0xffffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestAND<db>(0xffffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestAND<dd>(0xffffffff, 0x00000001, 0x00000001, false, false, false, false, false);
    

    TestAND<dw>(0xffffffff, 0x00000001, 0xffff0001, false, false, false, false, false);
    

    TestAND<db>(0xffffffff, 0x00000001, 0xffffff01, false, false, false, false, false);
    

    TestAND<dd>(0xffffffff, 0x00000002, 0x00000002, false, false, false, false, false);
    

    TestAND<dw>(0xffffffff, 0x00000002, 0xffff0002, false, false, false, false, false);
    

    TestAND<db>(0xffffffff, 0x00000002, 0xffffff02, false, false, false, false, false);
    

    TestAND<dd>(0x7fffffff, 0x00000000, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0x7fffffff, 0x00000000, 0x7fff0000, false, false, false, true, false);
    

    TestAND<db>(0x7fffffff, 0x00000000, 0x7fffff00, false, false, false, true, false);
    

    TestAND<dd>(0x7fffffff, 0x00000001, 0x00000001, false, false, false, false, false);
    

    TestAND<dw>(0x7fffffff, 0x00000001, 0x7fff0001, false, false, false, false, false);
    

    TestAND<db>(0x7fffffff, 0x00000001, 0x7fffff01, false, false, false, false, false);
    

    TestAND<dd>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, false, false, false);
    

    TestAND<dw>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, true, false, false);
    

    TestAND<db>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, true, false, false);
    

    TestAND<dd>(0x80000000, 0xffffffff, 0x80000000, false, false, true, false, false);
    

    TestAND<dw>(0x80000000, 0xffffffff, 0x80000000, false, false, false, true, false);
    

    TestAND<db>(0x80000000, 0xffffffff, 0x80000000, false, false, false, true, false);
    

    TestAND<dd>(0x80000000, 0x00000001, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0x80000000, 0x00000001, 0x80000000, false, false, false, true, false);
    

    TestAND<db>(0x80000000, 0x00000001, 0x80000000, false, false, false, true, false);
    

    TestAND<dd>(0x80000000, 0xfffffffe, 0x80000000, false, false, true, false, false);
    

    TestAND<dw>(0x80000000, 0xfffffffe, 0x80000000, false, false, false, true, false);
    

    TestAND<db>(0x80000000, 0xfffffffe, 0x80000000, false, false, false, true, false);
    

    TestAND<dd>(0x12347fff, 0x00000000, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0x12347fff, 0x00000000, 0x12340000, false, false, false, true, false);
    

    TestAND<db>(0x12347fff, 0x00000000, 0x12347f00, false, false, false, true, false);
    

    TestAND<dd>(0x12347fff, 0x00000001, 0x00000001, false, false, false, false, false);
    

    TestAND<dw>(0x12347fff, 0x00000001, 0x12340001, false, false, false, false, false);
    

    TestAND<db>(0x12347fff, 0x00000001, 0x12347f01, false, false, false, false, false);
    

    TestAND<dd>(0x12347fff, 0xffffffff, 0x12347fff, false, false, false, false, false);
    

    TestAND<dw>(0x12347fff, 0xffffffff, 0x12347fff, false, false, false, false, false);
    

    TestAND<db>(0x12347fff, 0xffffffff, 0x12347fff, false, false, true, false, false);
    

    TestAND<dd>(0x12348000, 0xffffffff, 0x12348000, false, false, false, false, false);
    

    TestAND<dw>(0x12348000, 0xffffffff, 0x12348000, false, false, true, false, false);
    

    TestAND<db>(0x12348000, 0xffffffff, 0x12348000, false, false, false, true, false);
    

    TestAND<dd>(0x12348000, 0x00000001, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0x12348000, 0x00000001, 0x12340000, false, false, false, true, false);
    

    TestAND<db>(0x12348000, 0x00000001, 0x12348000, false, false, false, true, false);
    

    TestAND<dd>(0x12348000, 0xfffffffe, 0x12348000, false, false, false, false, false);
    

    TestAND<dw>(0x12348000, 0xfffffffe, 0x12348000, false, false, true, false, false);
    

    TestAND<db>(0x12348000, 0xfffffffe, 0x12348000, false, false, false, true, false);
    

    TestAND<dd>(0x12347f7f, 0x00000000, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0x12347f7f, 0x00000000, 0x12340000, false, false, false, true, false);
    

    TestAND<db>(0x12347f7f, 0x00000000, 0x12347f00, false, false, false, true, false);
    

    TestAND<dd>(0x12347f7f, 0x00000001, 0x00000001, false, false, false, false, false);
    

    TestAND<dw>(0x12347f7f, 0x00000001, 0x12340001, false, false, false, false, false);
    

    TestAND<db>(0x12347f7f, 0x00000001, 0x12347f01, false, false, false, false, false);
    

    TestAND<dd>(0x12347f7f, 0xffffffff, 0x12347f7f, false, false, false, false, false);
    

    TestAND<dw>(0x12347f7f, 0xffffffff, 0x12347f7f, false, false, false, false, false);
    

    TestAND<db>(0x12347f7f, 0xffffffff, 0x12347f7f, false, false, false, false, false);
    

    TestAND<dd>(0x12348080, 0xffffffff, 0x12348080, false, false, false, false, false);
    

    TestAND<dw>(0x12348080, 0xffffffff, 0x12348080, false, false, true, false, false);
    

    TestAND<db>(0x12348080, 0xffffffff, 0x12348080, false, false, true, false, false);
    

    TestAND<dd>(0x12348080, 0x00000001, 0x00000000, false, false, false, true, false);
    

    TestAND<dw>(0x12348080, 0x00000001, 0x12340000, false, false, false, true, false);
    

    TestAND<db>(0x12348080, 0x00000001, 0x12348000, false, false, false, true, false);
    

    TestAND<dd>(0x12348080, 0xfffffffe, 0x12348080, false, false, false, false, false);
    

    TestAND<dw>(0x12348080, 0xfffffffe, 0x12348080, false, false, true, false, false);
    

    TestAND<db>(0x12348080, 0xfffffffe, 0x12348080, false, false, true, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, OR) {

    TestOR<dd>(0x12345678, 0x0812fada, 0x1a36fefa, false, false, false, false, false);
    

    TestOR<dw>(0x12345678, 0x0812fada, 0x1234fefa, false, false, true, false, false);
    

    TestOR<db>(0x12345678, 0x0812fada, 0x123456fa, false, false, true, false, false);
    

    TestOR<dd>(0x00012341, 0x00012341, 0x00012341, false, false, false, false, false);
    

    TestOR<dw>(0x00012341, 0x00012341, 0x00012341, false, false, false, false, false);
    

    TestOR<db>(0x00012341, 0x00012341, 0x00012341, false, false, false, false, false);
    

    TestOR<dd>(0x00012341, 0xfffedcbf, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x00012341, 0xfffedcbf, 0x0001ffff, false, false, true, false, false);
    

    TestOR<db>(0x00012341, 0xfffedcbf, 0x000123ff, false, false, true, false, false);
    

    TestOR<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestOR<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestOR<dd>(0xffffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0xffffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<db>(0xffffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dd>(0xffffffff, 0x00000001, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0xffffffff, 0x00000001, 0xffffffff, false, false, true, false, false);
    

    TestOR<db>(0xffffffff, 0x00000001, 0xffffffff, false, false, true, false, false);
    

    TestOR<dd>(0xffffffff, 0x00000002, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0xffffffff, 0x00000002, 0xffffffff, false, false, true, false, false);
    

    TestOR<db>(0xffffffff, 0x00000002, 0xffffffff, false, false, true, false, false);
    

    TestOR<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestOR<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestOR<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestOR<dd>(0x7fffffff, 0x00000001, 0x7fffffff, false, false, false, false, false);
    

    TestOR<dw>(0x7fffffff, 0x00000001, 0x7fffffff, false, false, true, false, false);
    

    TestOR<db>(0x7fffffff, 0x00000001, 0x7fffffff, false, false, true, false, false);
    

    TestOR<dd>(0x7fffffff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, true, false, false);
    

    TestOR<db>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, true, false, false);
    

    TestOR<dd>(0x80000000, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x80000000, 0xffffffff, 0x8000ffff, false, false, true, false, false);
    

    TestOR<db>(0x80000000, 0xffffffff, 0x800000ff, false, false, true, false, false);
    

    TestOR<dd>(0x80000000, 0x00000001, 0x80000001, false, false, true, false, false);
    

    TestOR<dw>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestOR<db>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestOR<dd>(0x80000000, 0xfffffffe, 0xfffffffe, false, false, true, false, false);
    

    TestOR<dw>(0x80000000, 0xfffffffe, 0x8000fffe, false, false, true, false, false);
    

    TestOR<db>(0x80000000, 0xfffffffe, 0x800000fe, false, false, true, false, false);
    

    TestOR<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestOR<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestOR<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestOR<dd>(0x12347fff, 0x00000001, 0x12347fff, false, false, false, false, false);
    

    TestOR<dw>(0x12347fff, 0x00000001, 0x12347fff, false, false, false, false, false);
    

    TestOR<db>(0x12347fff, 0x00000001, 0x12347fff, false, false, true, false, false);
    

    TestOR<dd>(0x12347fff, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x12347fff, 0xffffffff, 0x1234ffff, false, false, true, false, false);
    

    TestOR<db>(0x12347fff, 0xffffffff, 0x12347fff, false, false, true, false, false);
    

    TestOR<dd>(0x12348000, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x12348000, 0xffffffff, 0x1234ffff, false, false, true, false, false);
    

    TestOR<db>(0x12348000, 0xffffffff, 0x123480ff, false, false, true, false, false);
    

    TestOR<dd>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestOR<dw>(0x12348000, 0x00000001, 0x12348001, false, false, true, false, false);
    

    TestOR<db>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestOR<dd>(0x12348000, 0xfffffffe, 0xfffffffe, false, false, true, false, false);
    

    TestOR<dw>(0x12348000, 0xfffffffe, 0x1234fffe, false, false, true, false, false);
    

    TestOR<db>(0x12348000, 0xfffffffe, 0x123480fe, false, false, true, false, false);
    

    TestOR<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestOR<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestOR<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestOR<dd>(0x12347f7f, 0x00000001, 0x12347f7f, false, false, false, false, false);
    

    TestOR<dw>(0x12347f7f, 0x00000001, 0x12347f7f, false, false, false, false, false);
    

    TestOR<db>(0x12347f7f, 0x00000001, 0x12347f7f, false, false, false, false, false);
    

    TestOR<dd>(0x12347f7f, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x12347f7f, 0xffffffff, 0x1234ffff, false, false, true, false, false);
    

    TestOR<db>(0x12347f7f, 0xffffffff, 0x12347fff, false, false, true, false, false);
    

    TestOR<dd>(0x12348080, 0xffffffff, 0xffffffff, false, false, true, false, false);
    

    TestOR<dw>(0x12348080, 0xffffffff, 0x1234ffff, false, false, true, false, false);
    

    TestOR<db>(0x12348080, 0xffffffff, 0x123480ff, false, false, true, false, false);
    

    TestOR<dd>(0x12348080, 0x00000001, 0x12348081, false, false, false, false, false);
    

    TestOR<dw>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestOR<db>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestOR<dd>(0x12348080, 0xfffffffe, 0xfffffffe, false, false, true, false, false);
    

    TestOR<dw>(0x12348080, 0xfffffffe, 0x1234fffe, false, false, true, false, false);
    

    TestOR<db>(0x12348080, 0xfffffffe, 0x123480fe, false, false, true, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, CMP) {

    TestSUB<dd>(0x12345678, 0x0812fada, 0x12345678, false, false, false, false, false);
    

    TestSUB<dw>(0x12345678, 0x0812fada, 0x12345678, true, false, false, false, false);
    

    TestSUB<db>(0x12345678, 0x0812fada, 0x12345678, true, true, true, false, false);
    

    TestSUB<dd>(0x00012341, 0x00012341, 0x00012341, false, false, false, true, false);
    

    TestSUB<dw>(0x00012341, 0x00012341, 0x00012341, false, false, false, true, false);
    

    TestSUB<db>(0x00012341, 0x00012341, 0x00012341, false, false, false, true, false);
    

    TestSUB<dd>(0x00012341, 0xfffedcbf, 0x00012341, true, false, false, false, false);
    

    TestSUB<dw>(0x00012341, 0xfffedcbf, 0x00012341, true, false, false, false, false);
    

    TestSUB<db>(0x00012341, 0xfffedcbf, 0x00012341, true, true, true, false, false);
    

    TestSUB<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSUB<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dd>(0xffffffff, 0xffffffff, 0xffffffff, false, false, false, true, false);
    

    TestSUB<dw>(0xffffffff, 0xffffffff, 0xffffffff, false, false, false, true, false);
    

    TestSUB<db>(0xffffffff, 0xffffffff, 0xffffffff, false, false, false, true, false);
    

    TestSUB<dd>(0xffffffff, 0x00000001, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dw>(0xffffffff, 0x00000001, 0xffffffff, false, false, true, false, false);
    

    TestSUB<db>(0xffffffff, 0x00000001, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dd>(0xffffffff, 0x00000002, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dw>(0xffffffff, 0x00000002, 0xffffffff, false, false, true, false, false);
    

    TestSUB<db>(0xffffffff, 0x00000002, 0xffffffff, false, false, true, false, false);
    

    TestSUB<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestSUB<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestSUB<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestSUB<dd>(0x7fffffff, 0x00000001, 0x7fffffff, false, false, false, false, false);
    

    TestSUB<dw>(0x7fffffff, 0x00000001, 0x7fffffff, false, false, true, false, false);
    

    TestSUB<db>(0x7fffffff, 0x00000001, 0x7fffffff, false, false, true, false, false);
    

    TestSUB<dd>(0x7fffffff, 0xffffffff, 0x7fffffff, true, true, true, false, false);
    

    TestSUB<dw>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, false, true, false);
    

    TestSUB<db>(0x7fffffff, 0xffffffff, 0x7fffffff, false, false, false, true, false);
    

    TestSUB<dd>(0x80000000, 0xffffffff, 0x80000000, true, false, true, false, false);
    

    TestSUB<dw>(0x80000000, 0xffffffff, 0x80000000, true, false, false, false, false);
    

    TestSUB<db>(0x80000000, 0xffffffff, 0x80000000, true, false, false, false, false);
    

    TestSUB<dd>(0x80000000, 0x00000001, 0x80000000, false, true, false, false, false);
    

    TestSUB<dw>(0x80000000, 0x00000001, 0x80000000, true, false, true, false, false);
    

    TestSUB<db>(0x80000000, 0x00000001, 0x80000000, true, false, true, false, false);
    

    TestSUB<dd>(0x80000000, 0xfffffffe, 0x80000000, true, false, true, false, false);
    

    TestSUB<dw>(0x80000000, 0xfffffffe, 0x80000000, true, false, false, false, false);
    

    TestSUB<db>(0x80000000, 0xfffffffe, 0x80000000, true, false, false, false, false);
    

    TestSUB<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestSUB<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestSUB<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestSUB<dd>(0x12347fff, 0x00000001, 0x12347fff, false, false, false, false, false);
    

    TestSUB<dw>(0x12347fff, 0x00000001, 0x12347fff, false, false, false, false, false);
    

    TestSUB<db>(0x12347fff, 0x00000001, 0x12347fff, false, false, true, false, false);
    

    TestSUB<dd>(0x12347fff, 0xffffffff, 0x12347fff, true, false, false, false, false);
    

    TestSUB<dw>(0x12347fff, 0xffffffff, 0x12347fff, true, true, true, false, false);
    

    TestSUB<db>(0x12347fff, 0xffffffff, 0x12347fff, false, false, false, true, false);
    

    TestSUB<dd>(0x12348000, 0xffffffff, 0x12348000, true, false, false, false, false);
    

    TestSUB<dw>(0x12348000, 0xffffffff, 0x12348000, true, false, true, false, false);
    

    TestSUB<db>(0x12348000, 0xffffffff, 0x12348000, true, false, false, false, false);
    

    TestSUB<dd>(0x12348000, 0x00000001, 0x12348000, false, false, false, false, false);
    

    TestSUB<dw>(0x12348000, 0x00000001, 0x12348000, false, true, false, false, false);
    

    TestSUB<db>(0x12348000, 0x00000001, 0x12348000, true, false, true, false, false);
    

    TestSUB<dd>(0x12348000, 0xfffffffe, 0x12348000, true, false, false, false, false);
    

    TestSUB<dw>(0x12348000, 0xfffffffe, 0x12348000, true, false, true, false, false);
    

    TestSUB<db>(0x12348000, 0xfffffffe, 0x12348000, true, false, false, false, false);
    

    TestSUB<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<dd>(0x12347f7f, 0x00000001, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<dw>(0x12347f7f, 0x00000001, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<db>(0x12347f7f, 0x00000001, 0x12347f7f, false, false, false, false, false);
    

    TestSUB<dd>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, false);
    

    TestSUB<dw>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, false);
    

    TestSUB<db>(0x12347f7f, 0xffffffff, 0x12347f7f, true, true, true, false, false);
    

    TestSUB<dd>(0x12348080, 0xffffffff, 0x12348080, true, false, false, false, false);
    

    TestSUB<dw>(0x12348080, 0xffffffff, 0x12348080, true, false, true, false, false);
    

    TestSUB<db>(0x12348080, 0xffffffff, 0x12348080, true, false, true, false, false);
    

    TestSUB<dd>(0x12348080, 0x00000001, 0x12348080, false, false, false, false, false);
    

    TestSUB<dw>(0x12348080, 0x00000001, 0x12348080, false, false, true, false, false);
    

    TestSUB<db>(0x12348080, 0x00000001, 0x12348080, false, true, false, false, false);
    

    TestSUB<dd>(0x12348080, 0xfffffffe, 0x12348080, true, false, false, false, false);
    

    TestSUB<dw>(0x12348080, 0xfffffffe, 0x12348080, true, false, true, false, false);
    

    TestSUB<db>(0x12348080, 0xfffffffe, 0x12348080, true, false, true, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, ADC) {

    TestADC<dd>(0x12345678, 0x0812fada, 0x1a475152, false, false, false, false, false);
    

    TestADC<dw>(0x12345678, 0x0812fada, 0x12345152, true, false, false, false, false);
    

    TestADC<db>(0x12345678, 0x0812fada, 0x12345652, true, false, false, false, false);
    

    TestADC<dd>(0x12345678, 0x0812fada, 0x1a475153, false, false, false, false, true);
    

    TestADC<dw>(0x12345678, 0x0812fada, 0x12345153, true, false, false, false, true);
    

    TestADC<db>(0x12345678, 0x0812fada, 0x12345653, true, false, false, false, true);
    

    TestADC<dd>(0x00012341, 0x00012341, 0x00024682, false, false, false, false, false);
    

    TestADC<dw>(0x00012341, 0x00012341, 0x00014682, false, false, false, false, false);
    

    TestADC<db>(0x00012341, 0x00012341, 0x00012382, false, true, true, false, false);
    

    TestADC<dd>(0x00012341, 0x00012341, 0x00024683, false, false, false, false, true);
    

    TestADC<dw>(0x00012341, 0x00012341, 0x00014683, false, false, false, false, true);
    

    TestADC<db>(0x00012341, 0x00012341, 0x00012383, false, true, true, false, true);
    

    TestADC<dd>(0x00012341, 0xfffedcbf, 0x00000000, true, false, false, true, false);
    

    TestADC<dw>(0x00012341, 0xfffedcbf, 0x00010000, true, false, false, true, false);
    

    TestADC<db>(0x00012341, 0xfffedcbf, 0x00012300, true, false, false, true, false);
    

    TestADC<dd>(0x00012341, 0xfffedcbf, 0x00000001, true, false, false, false, true);
    

    TestADC<dw>(0x00012341, 0xfffedcbf, 0x00010001, true, false, false, false, true);
    

    TestADC<db>(0x00012341, 0xfffedcbf, 0x00012301, true, false, false, false, true);
    

    TestADC<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestADC<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestADC<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestADC<dd>(0xffffffff, 0x00000000, 0x00000000, true, false, false, true, true);
    

    TestADC<dw>(0xffffffff, 0x00000000, 0xffff0000, true, false, false, true, true);
    

    TestADC<db>(0xffffffff, 0x00000000, 0xffffff00, true, false, false, true, true);
    

    TestADC<dd>(0xffffffff, 0xffffffff, 0xfffffffe, true, false, true, false, false);
    

    TestADC<dw>(0xffffffff, 0xffffffff, 0xfffffffe, true, false, true, false, false);
    

    TestADC<db>(0xffffffff, 0xffffffff, 0xfffffffe, true, false, true, false, false);
    

    TestADC<dd>(0xffffffff, 0xffffffff, 0xffffffff, true, false, true, false, true);
    

    TestADC<dw>(0xffffffff, 0xffffffff, 0xffffffff, true, false, true, false, true);
    

    TestADC<db>(0xffffffff, 0xffffffff, 0xffffffff, true, false, true, false, true);
    

    TestADC<dd>(0xffffffff, 0x00000001, 0x00000000, true, false, false, true, false);
    

    TestADC<dw>(0xffffffff, 0x00000001, 0xffff0000, true, false, false, true, false);
    

    TestADC<db>(0xffffffff, 0x00000001, 0xffffff00, true, false, false, true, false);
    

    TestADC<dd>(0xffffffff, 0x00000001, 0x00000001, true, false, false, false, true);
    

    TestADC<dw>(0xffffffff, 0x00000001, 0xffff0001, true, false, false, false, true);
    

    TestADC<db>(0xffffffff, 0x00000001, 0xffffff01, true, false, false, false, true);
    

    TestADC<dd>(0xffffffff, 0x00000002, 0x00000001, true, false, false, false, false);
    

    TestADC<dw>(0xffffffff, 0x00000002, 0xffff0001, true, false, false, false, false);
    

    TestADC<db>(0xffffffff, 0x00000002, 0xffffff01, true, false, false, false, false);
    

    TestADC<dd>(0xffffffff, 0x00000002, 0x00000002, true, false, false, false, true);
    

    TestADC<dw>(0xffffffff, 0x00000002, 0xffff0002, true, false, false, false, true);
    

    TestADC<db>(0xffffffff, 0x00000002, 0xffffff02, true, false, false, false, true);
    

    TestADC<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestADC<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestADC<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestADC<dd>(0x7fffffff, 0x00000000, 0x80000000, false, true, true, false, true);
    

    TestADC<dw>(0x7fffffff, 0x00000000, 0x7fff0000, true, false, false, true, true);
    

    TestADC<db>(0x7fffffff, 0x00000000, 0x7fffff00, true, false, false, true, true);
    

    TestADC<dd>(0x7fffffff, 0x00000001, 0x80000000, false, true, true, false, false);
    

    TestADC<dw>(0x7fffffff, 0x00000001, 0x7fff0000, true, false, false, true, false);
    

    TestADC<db>(0x7fffffff, 0x00000001, 0x7fffff00, true, false, false, true, false);
    

    TestADC<dd>(0x7fffffff, 0x00000001, 0x80000001, false, true, true, false, true);
    

    TestADC<dw>(0x7fffffff, 0x00000001, 0x7fff0001, true, false, false, false, true);
    

    TestADC<db>(0x7fffffff, 0x00000001, 0x7fffff01, true, false, false, false, true);
    

    TestADC<dd>(0x7fffffff, 0xffffffff, 0x7ffffffe, true, false, false, false, false);
    

    TestADC<dw>(0x7fffffff, 0xffffffff, 0x7ffffffe, true, false, true, false, false);
    

    TestADC<db>(0x7fffffff, 0xffffffff, 0x7ffffffe, true, false, true, false, false);
    

    TestADC<dd>(0x7fffffff, 0xffffffff, 0x7fffffff, true, false, false, false, true);
    

    TestADC<dw>(0x7fffffff, 0xffffffff, 0x7fffffff, true, false, true, false, true);
    

    TestADC<db>(0x7fffffff, 0xffffffff, 0x7fffffff, true, false, true, false, true);
    

    TestADC<dd>(0x80000000, 0xffffffff, 0x7fffffff, true, true, false, false, false);
    

    TestADC<dw>(0x80000000, 0xffffffff, 0x8000ffff, false, false, true, false, false);
    

    TestADC<db>(0x80000000, 0xffffffff, 0x800000ff, false, false, true, false, false);
    

    TestADC<dd>(0x80000000, 0xffffffff, 0x80000000, true, false, true, false, true);
    

    TestADC<dw>(0x80000000, 0xffffffff, 0x80000000, true, false, false, true, true);
    

    TestADC<db>(0x80000000, 0xffffffff, 0x80000000, true, false, false, true, true);
    

    TestADC<dd>(0x80000000, 0x00000001, 0x80000001, false, false, true, false, false);
    

    TestADC<dw>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestADC<db>(0x80000000, 0x00000001, 0x80000001, false, false, false, false, false);
    

    TestADC<dd>(0x80000000, 0x00000001, 0x80000002, false, false, true, false, true);
    

    TestADC<dw>(0x80000000, 0x00000001, 0x80000002, false, false, false, false, true);
    

    TestADC<db>(0x80000000, 0x00000001, 0x80000002, false, false, false, false, true);
    

    TestADC<dd>(0x80000000, 0xfffffffe, 0x7ffffffe, true, true, false, false, false);
    

    TestADC<dw>(0x80000000, 0xfffffffe, 0x8000fffe, false, false, true, false, false);
    

    TestADC<db>(0x80000000, 0xfffffffe, 0x800000fe, false, false, true, false, false);
    

    TestADC<dd>(0x80000000, 0xfffffffe, 0x7fffffff, true, true, false, false, true);
    

    TestADC<dw>(0x80000000, 0xfffffffe, 0x8000ffff, false, false, true, false, true);
    

    TestADC<db>(0x80000000, 0xfffffffe, 0x800000ff, false, false, true, false, true);
    

    TestADC<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestADC<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestADC<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestADC<dd>(0x12347fff, 0x00000000, 0x12348000, false, false, false, false, true);
    

    TestADC<dw>(0x12347fff, 0x00000000, 0x12348000, false, true, true, false, true);
    

    TestADC<db>(0x12347fff, 0x00000000, 0x12347f00, true, false, false, true, true);
    

    TestADC<dd>(0x12347fff, 0x00000001, 0x12348000, false, false, false, false, false);
    

    TestADC<dw>(0x12347fff, 0x00000001, 0x12348000, false, true, true, false, false);
    

    TestADC<db>(0x12347fff, 0x00000001, 0x12347f00, true, false, false, true, false);
    

    TestADC<dd>(0x12347fff, 0x00000001, 0x12348001, false, false, false, false, true);
    

    TestADC<dw>(0x12347fff, 0x00000001, 0x12348001, false, true, true, false, true);
    

    TestADC<db>(0x12347fff, 0x00000001, 0x12347f01, true, false, false, false, true);
    

    TestADC<dd>(0x12347fff, 0xffffffff, 0x12347ffe, true, false, false, false, false);
    

    TestADC<dw>(0x12347fff, 0xffffffff, 0x12347ffe, true, false, false, false, false);
    

    TestADC<db>(0x12347fff, 0xffffffff, 0x12347ffe, true, false, true, false, false);
    

    TestADC<dd>(0x12347fff, 0xffffffff, 0x12347fff, true, false, false, false, true);
    

    TestADC<dw>(0x12347fff, 0xffffffff, 0x12347fff, true, false, false, false, true);
    

    TestADC<db>(0x12347fff, 0xffffffff, 0x12347fff, true, false, true, false, true);
    

    TestADC<dd>(0x12348000, 0xffffffff, 0x12347fff, true, false, false, false, false);
    

    TestADC<dw>(0x12348000, 0xffffffff, 0x12347fff, true, true, false, false, false);
    

    TestADC<db>(0x12348000, 0xffffffff, 0x123480ff, false, false, true, false, false);
    

    TestADC<dd>(0x12348000, 0xffffffff, 0x12348000, true, false, false, false, true);
    

    TestADC<dw>(0x12348000, 0xffffffff, 0x12348000, true, false, true, false, true);
    

    TestADC<db>(0x12348000, 0xffffffff, 0x12348000, true, false, false, true, true);
    

    TestADC<dd>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestADC<dw>(0x12348000, 0x00000001, 0x12348001, false, false, true, false, false);
    

    TestADC<db>(0x12348000, 0x00000001, 0x12348001, false, false, false, false, false);
    

    TestADC<dd>(0x12348000, 0x00000001, 0x12348002, false, false, false, false, true);
    

    TestADC<dw>(0x12348000, 0x00000001, 0x12348002, false, false, true, false, true);
    

    TestADC<db>(0x12348000, 0x00000001, 0x12348002, false, false, false, false, true);
    

    TestADC<dd>(0x12348000, 0xfffffffe, 0x12347ffe, true, false, false, false, false);
    

    TestADC<dw>(0x12348000, 0xfffffffe, 0x12347ffe, true, true, false, false, false);
    

    TestADC<db>(0x12348000, 0xfffffffe, 0x123480fe, false, false, true, false, false);
    

    TestADC<dd>(0x12348000, 0xfffffffe, 0x12347fff, true, false, false, false, true);
    

    TestADC<dw>(0x12348000, 0xfffffffe, 0x12347fff, true, true, false, false, true);
    

    TestADC<db>(0x12348000, 0xfffffffe, 0x123480ff, false, false, true, false, true);
    

    TestADC<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestADC<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestADC<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestADC<dd>(0x12347f7f, 0x00000000, 0x12347f80, false, false, false, false, true);
    

    TestADC<dw>(0x12347f7f, 0x00000000, 0x12347f80, false, false, false, false, true);
    

    TestADC<db>(0x12347f7f, 0x00000000, 0x12347f80, false, true, true, false, true);
    

    TestADC<dd>(0x12347f7f, 0x00000001, 0x12347f80, false, false, false, false, false);
    

    TestADC<dw>(0x12347f7f, 0x00000001, 0x12347f80, false, false, false, false, false);
    

    TestADC<db>(0x12347f7f, 0x00000001, 0x12347f80, false, true, true, false, false);
    

    TestADC<dd>(0x12347f7f, 0x00000001, 0x12347f81, false, false, false, false, true);
    

    TestADC<dw>(0x12347f7f, 0x00000001, 0x12347f81, false, false, false, false, true);
    

    TestADC<db>(0x12347f7f, 0x00000001, 0x12347f81, false, true, true, false, true);
    

    TestADC<dd>(0x12347f7f, 0xffffffff, 0x12347f7e, true, false, false, false, false);
    

    TestADC<dw>(0x12347f7f, 0xffffffff, 0x12347f7e, true, false, false, false, false);
    

    TestADC<db>(0x12347f7f, 0xffffffff, 0x12347f7e, true, false, false, false, false);
    

    TestADC<dd>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, true);
    

    TestADC<dw>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, true);
    

    TestADC<db>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, true);
    

    TestADC<dd>(0x12348080, 0xffffffff, 0x1234807f, true, false, false, false, false);
    

    TestADC<dw>(0x12348080, 0xffffffff, 0x1234807f, true, false, true, false, false);
    

    TestADC<db>(0x12348080, 0xffffffff, 0x1234807f, true, true, false, false, false);
    

    TestADC<dd>(0x12348080, 0xffffffff, 0x12348080, true, false, false, false, true);
    

    TestADC<dw>(0x12348080, 0xffffffff, 0x12348080, true, false, true, false, true);
    

    TestADC<db>(0x12348080, 0xffffffff, 0x12348080, true, false, true, false, true);
    

    TestADC<dd>(0x12348080, 0x00000001, 0x12348081, false, false, false, false, false);
    

    TestADC<dw>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestADC<db>(0x12348080, 0x00000001, 0x12348081, false, false, true, false, false);
    

    TestADC<dd>(0x12348080, 0x00000001, 0x12348082, false, false, false, false, true);
    

    TestADC<dw>(0x12348080, 0x00000001, 0x12348082, false, false, true, false, true);
    

    TestADC<db>(0x12348080, 0x00000001, 0x12348082, false, false, true, false, true);
    

    TestADC<dd>(0x12348080, 0xfffffffe, 0x1234807e, true, false, false, false, false);
    

    TestADC<dw>(0x12348080, 0xfffffffe, 0x1234807e, true, false, true, false, false);
    

    TestADC<db>(0x12348080, 0xfffffffe, 0x1234807e, true, true, false, false, false);
    

    TestADC<dd>(0x12348080, 0xfffffffe, 0x1234807f, true, false, false, false, true);
    

    TestADC<dw>(0x12348080, 0xfffffffe, 0x1234807f, true, false, true, false, true);
    

    TestADC<db>(0x12348080, 0xfffffffe, 0x1234807f, true, true, false, false, true);
    
  }

  TEST_F(EmulatedInstructionsTest, SBB) {

    TestSBB<dd>(0x12345678, 0x0812fada, 0x0a215b9e, false, false, false, false, false);
    

    TestSBB<dw>(0x12345678, 0x0812fada, 0x12345b9e, true, false, false, false, false);
    

    TestSBB<db>(0x12345678, 0x0812fada, 0x1234569e, true, true, true, false, false);
    

    TestSBB<dd>(0x12345678, 0x0812fada, 0x0a215b9d, false, false, false, false, true);
    

    TestSBB<dw>(0x12345678, 0x0812fada, 0x12345b9d, true, false, false, false, true);
    

    TestSBB<db>(0x12345678, 0x0812fada, 0x1234569d, true, true, true, false, true);
    

    TestSBB<dd>(0x00012341, 0x00012341, 0x00000000, false, false, false, true, false);
    

    TestSBB<dw>(0x00012341, 0x00012341, 0x00010000, false, false, false, true, false);
    

    TestSBB<db>(0x00012341, 0x00012341, 0x00012300, false, false, false, true, false);
    

    TestSBB<dd>(0x00012341, 0x00012341, 0xffffffff, true, false, true, false, true);
    

    TestSBB<dw>(0x00012341, 0x00012341, 0x0001ffff, true, false, true, false, true);
    

    TestSBB<db>(0x00012341, 0x00012341, 0x000123ff, true, false, true, false, true);
    

    TestSBB<dd>(0x00012341, 0xfffedcbf, 0x00024682, true, false, false, false, false);
    

    TestSBB<dw>(0x00012341, 0xfffedcbf, 0x00014682, true, false, false, false, false);
    

    TestSBB<db>(0x00012341, 0xfffedcbf, 0x00012382, true, true, true, false, false);
    

    TestSBB<dd>(0x00012341, 0xfffedcbf, 0x00024681, true, false, false, false, true);
    

    TestSBB<dw>(0x00012341, 0xfffedcbf, 0x00014681, true, false, false, false, true);
    

    TestSBB<db>(0x00012341, 0xfffedcbf, 0x00012381, true, true, true, false, true);
    

    TestSBB<dd>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSBB<dw>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSBB<db>(0xffffffff, 0x00000000, 0xffffffff, false, false, true, false, false);
    

    TestSBB<dd>(0xffffffff, 0x00000000, 0xfffffffe, false, false, true, false, true);
    

    TestSBB<dw>(0xffffffff, 0x00000000, 0xfffffffe, false, false, true, false, true);
    

    TestSBB<db>(0xffffffff, 0x00000000, 0xfffffffe, false, false, true, false, true);
    

    TestSBB<dd>(0xffffffff, 0xffffffff, 0x00000000, false, false, false, true, false);
    

    TestSBB<dw>(0xffffffff, 0xffffffff, 0xffff0000, false, false, false, true, false);
    

    TestSBB<db>(0xffffffff, 0xffffffff, 0xffffff00, false, false, false, true, false);
    

    TestSBB<dd>(0xffffffff, 0xffffffff, 0xffffffff, true, false, true, false, true);
    

    TestSBB<dw>(0xffffffff, 0xffffffff, 0xffffffff, true, false, true, false, true);
    

    TestSBB<db>(0xffffffff, 0xffffffff, 0xffffffff, true, false, true, false, true);
    

    TestSBB<dd>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestSBB<dw>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestSBB<db>(0xffffffff, 0x00000001, 0xfffffffe, false, false, true, false, false);
    

    TestSBB<dd>(0xffffffff, 0x00000001, 0xfffffffd, false, false, true, false, true);
    

    TestSBB<dw>(0xffffffff, 0x00000001, 0xfffffffd, false, false, true, false, true);
    

    TestSBB<db>(0xffffffff, 0x00000001, 0xfffffffd, false, false, true, false, true);
    

    TestSBB<dd>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestSBB<dw>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestSBB<db>(0xffffffff, 0x00000002, 0xfffffffd, false, false, true, false, false);
    

    TestSBB<dd>(0xffffffff, 0x00000002, 0xfffffffc, false, false, true, false, true);
    

    TestSBB<dw>(0xffffffff, 0x00000002, 0xfffffffc, false, false, true, false, true);
    

    TestSBB<db>(0xffffffff, 0x00000002, 0xfffffffc, false, false, true, false, true);
    

    TestSBB<dd>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, false, false, false);
    

    TestSBB<dw>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestSBB<db>(0x7fffffff, 0x00000000, 0x7fffffff, false, false, true, false, false);
    

    TestSBB<dd>(0x7fffffff, 0x00000000, 0x7ffffffe, false, false, false, false, true);
    

    TestSBB<dw>(0x7fffffff, 0x00000000, 0x7ffffffe, false, false, true, false, true);
    

    TestSBB<db>(0x7fffffff, 0x00000000, 0x7ffffffe, false, false, true, false, true);
    

    TestSBB<dd>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, false, false, false);
    

    TestSBB<dw>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, true, false, false);
    

    TestSBB<db>(0x7fffffff, 0x00000001, 0x7ffffffe, false, false, true, false, false);
    

    TestSBB<dd>(0x7fffffff, 0x00000001, 0x7ffffffd, false, false, false, false, true);
    

    TestSBB<dw>(0x7fffffff, 0x00000001, 0x7ffffffd, false, false, true, false, true);
    

    TestSBB<db>(0x7fffffff, 0x00000001, 0x7ffffffd, false, false, true, false, true);
    

    TestSBB<dd>(0x7fffffff, 0xffffffff, 0x80000000, true, true, true, false, false);
    

    TestSBB<dw>(0x7fffffff, 0xffffffff, 0x7fff0000, false, false, false, true, false);
    

    TestSBB<db>(0x7fffffff, 0xffffffff, 0x7fffff00, false, false, false, true, false);
    

    TestSBB<dd>(0x7fffffff, 0xffffffff, 0x7fffffff, true, false, false, false, true);
    

    TestSBB<dw>(0x7fffffff, 0xffffffff, 0x7fffffff, true, false, true, false, true);
    

    TestSBB<db>(0x7fffffff, 0xffffffff, 0x7fffffff, true, false, true, false, true);
    

    TestSBB<dd>(0x80000000, 0xffffffff, 0x80000001, true, false, true, false, false);
    

    TestSBB<dw>(0x80000000, 0xffffffff, 0x80000001, true, false, false, false, false);
    

    TestSBB<db>(0x80000000, 0xffffffff, 0x80000001, true, false, false, false, false);
    

    TestSBB<dd>(0x80000000, 0xffffffff, 0x80000000, true, false, true, false, true);
    

    TestSBB<dw>(0x80000000, 0xffffffff, 0x80000000, true, false, false, true, true);
    

    TestSBB<db>(0x80000000, 0xffffffff, 0x80000000, true, false, false, true, true);
    

    TestSBB<dd>(0x80000000, 0x00000001, 0x7fffffff, false, true, false, false, false);
    

    TestSBB<dw>(0x80000000, 0x00000001, 0x8000ffff, true, false, true, false, false);
    

    TestSBB<db>(0x80000000, 0x00000001, 0x800000ff, true, false, true, false, false);
    

    TestSBB<dd>(0x80000000, 0x00000001, 0x7ffffffe, false, true, false, false, true);
    

    TestSBB<dw>(0x80000000, 0x00000001, 0x8000fffe, true, false, true, false, true);
    

    TestSBB<db>(0x80000000, 0x00000001, 0x800000fe, true, false, true, false, true);
    

    TestSBB<dd>(0x80000000, 0xfffffffe, 0x80000002, true, false, true, false, false);
    

    TestSBB<dw>(0x80000000, 0xfffffffe, 0x80000002, true, false, false, false, false);
    

    TestSBB<db>(0x80000000, 0xfffffffe, 0x80000002, true, false, false, false, false);
    

    TestSBB<dd>(0x80000000, 0xfffffffe, 0x80000001, true, false, true, false, true);
    

    TestSBB<dw>(0x80000000, 0xfffffffe, 0x80000001, true, false, false, false, true);
    

    TestSBB<db>(0x80000000, 0xfffffffe, 0x80000001, true, false, false, false, true);
    

    TestSBB<dd>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestSBB<dw>(0x12347fff, 0x00000000, 0x12347fff, false, false, false, false, false);
    

    TestSBB<db>(0x12347fff, 0x00000000, 0x12347fff, false, false, true, false, false);
    

    TestSBB<dd>(0x12347fff, 0x00000000, 0x12347ffe, false, false, false, false, true);
    

    TestSBB<dw>(0x12347fff, 0x00000000, 0x12347ffe, false, false, false, false, true);
    

    TestSBB<db>(0x12347fff, 0x00000000, 0x12347ffe, false, false, true, false, true);
    

    TestSBB<dd>(0x12347fff, 0x00000001, 0x12347ffe, false, false, false, false, false);
    

    TestSBB<dw>(0x12347fff, 0x00000001, 0x12347ffe, false, false, false, false, false);
    

    TestSBB<db>(0x12347fff, 0x00000001, 0x12347ffe, false, false, true, false, false);
    

    TestSBB<dd>(0x12347fff, 0x00000001, 0x12347ffd, false, false, false, false, true);
    

    TestSBB<dw>(0x12347fff, 0x00000001, 0x12347ffd, false, false, false, false, true);
    

    TestSBB<db>(0x12347fff, 0x00000001, 0x12347ffd, false, false, true, false, true);
    

    TestSBB<dd>(0x12347fff, 0xffffffff, 0x12348000, true, false, false, false, false);
    

    TestSBB<dw>(0x12347fff, 0xffffffff, 0x12348000, true, true, true, false, false);
    

    TestSBB<db>(0x12347fff, 0xffffffff, 0x12347f00, false, false, false, true, false);
    

    TestSBB<dd>(0x12347fff, 0xffffffff, 0x12347fff, true, false, false, false, true);
    

    TestSBB<dw>(0x12347fff, 0xffffffff, 0x12347fff, true, false, false, false, true);
    

    TestSBB<db>(0x12347fff, 0xffffffff, 0x12347fff, true, false, true, false, true);
    

    TestSBB<dd>(0x12348000, 0xffffffff, 0x12348001, true, false, false, false, false);
    

    TestSBB<dw>(0x12348000, 0xffffffff, 0x12348001, true, false, true, false, false);
    

    TestSBB<db>(0x12348000, 0xffffffff, 0x12348001, true, false, false, false, false);
    

    TestSBB<dd>(0x12348000, 0xffffffff, 0x12348000, true, false, false, false, true);
    

    TestSBB<dw>(0x12348000, 0xffffffff, 0x12348000, true, false, true, false, true);
    

    TestSBB<db>(0x12348000, 0xffffffff, 0x12348000, true, false, false, true, true);
    

    TestSBB<dd>(0x12348000, 0x00000001, 0x12347fff, false, false, false, false, false);
    

    TestSBB<dw>(0x12348000, 0x00000001, 0x12347fff, false, true, false, false, false);
    

    TestSBB<db>(0x12348000, 0x00000001, 0x123480ff, true, false, true, false, false);
    

    TestSBB<dd>(0x12348000, 0x00000001, 0x12347ffe, false, false, false, false, true);
    

    TestSBB<dw>(0x12348000, 0x00000001, 0x12347ffe, false, true, false, false, true);
    

    TestSBB<db>(0x12348000, 0x00000001, 0x123480fe, true, false, true, false, true);
    

    TestSBB<dd>(0x12348000, 0xfffffffe, 0x12348002, true, false, false, false, false);
    

    TestSBB<dw>(0x12348000, 0xfffffffe, 0x12348002, true, false, true, false, false);
    

    TestSBB<db>(0x12348000, 0xfffffffe, 0x12348002, true, false, false, false, false);
    

    TestSBB<dd>(0x12348000, 0xfffffffe, 0x12348001, true, false, false, false, true);
    

    TestSBB<dw>(0x12348000, 0xfffffffe, 0x12348001, true, false, true, false, true);
    

    TestSBB<db>(0x12348000, 0xfffffffe, 0x12348001, true, false, false, false, true);
    

    TestSBB<dd>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSBB<dw>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSBB<db>(0x12347f7f, 0x00000000, 0x12347f7f, false, false, false, false, false);
    

    TestSBB<dd>(0x12347f7f, 0x00000000, 0x12347f7e, false, false, false, false, true);
    

    TestSBB<dw>(0x12347f7f, 0x00000000, 0x12347f7e, false, false, false, false, true);
    

    TestSBB<db>(0x12347f7f, 0x00000000, 0x12347f7e, false, false, false, false, true);
    

    TestSBB<dd>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestSBB<dw>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestSBB<db>(0x12347f7f, 0x00000001, 0x12347f7e, false, false, false, false, false);
    

    TestSBB<dd>(0x12347f7f, 0x00000001, 0x12347f7d, false, false, false, false, true);
    

    TestSBB<dw>(0x12347f7f, 0x00000001, 0x12347f7d, false, false, false, false, true);
    

    TestSBB<db>(0x12347f7f, 0x00000001, 0x12347f7d, false, false, false, false, true);
    

    TestSBB<dd>(0x12347f7f, 0xffffffff, 0x12347f80, true, false, false, false, false);
    

    TestSBB<dw>(0x12347f7f, 0xffffffff, 0x12347f80, true, false, false, false, false);
    

    TestSBB<db>(0x12347f7f, 0xffffffff, 0x12347f80, true, true, true, false, false);
    

    TestSBB<dd>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, true);
    

    TestSBB<dw>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, true);
    

    TestSBB<db>(0x12347f7f, 0xffffffff, 0x12347f7f, true, false, false, false, true);
    

    TestSBB<dd>(0x12348080, 0xffffffff, 0x12348081, true, false, false, false, false);
    

    TestSBB<dw>(0x12348080, 0xffffffff, 0x12348081, true, false, true, false, false);
    

    TestSBB<db>(0x12348080, 0xffffffff, 0x12348081, true, false, true, false, false);
    

    TestSBB<dd>(0x12348080, 0xffffffff, 0x12348080, true, false, false, false, true);
    

    TestSBB<dw>(0x12348080, 0xffffffff, 0x12348080, true, false, true, false, true);
    

    TestSBB<db>(0x12348080, 0xffffffff, 0x12348080, true, false, true, false, true);
    

    TestSBB<dd>(0x12348080, 0x00000001, 0x1234807f, false, false, false, false, false);
    

    TestSBB<dw>(0x12348080, 0x00000001, 0x1234807f, false, false, true, false, false);
    

    TestSBB<db>(0x12348080, 0x00000001, 0x1234807f, false, true, false, false, false);
    

    TestSBB<dd>(0x12348080, 0x00000001, 0x1234807e, false, false, false, false, true);
    

    TestSBB<dw>(0x12348080, 0x00000001, 0x1234807e, false, false, true, false, true);
    

    TestSBB<db>(0x12348080, 0x00000001, 0x1234807e, false, true, false, false, true);
    

    TestSBB<dd>(0x12348080, 0xfffffffe, 0x12348082, true, false, false, false, false);
    

    TestSBB<dw>(0x12348080, 0xfffffffe, 0x12348082, true, false, true, false, false);
    

    TestSBB<db>(0x12348080, 0xfffffffe, 0x12348082, true, false, true, false, false);
    

    TestSBB<dd>(0x12348080, 0xfffffffe, 0x12348081, true, false, false, false, true);
    

    TestSBB<dw>(0x12348080, 0xfffffffe, 0x12348081, true, false, true, false, true);
    

    TestSBB<db>(0x12348080, 0xfffffffe, 0x12348081, true, false, true, false, true);
    
  }

  TEST_F(EmulatedInstructionsTest, INC) {

    TestINC<dd>(0x12345678, 0x12345679, false, false, false);
    

    TestINC<dw>(0x12345678, 0x12345679, false, false, false);
    

    TestINC<db>(0x12345678, 0x12345679, false, false, false);
    

    TestINC<dd>(0x12345678, 0x12345679, false, false, false);
    

    TestINC<dw>(0x12345678, 0x12345679, false, false, false);
    

    TestINC<db>(0x12345678, 0x12345679, false, false, false);
    

    TestINC<dd>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dw>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<db>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dd>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dw>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<db>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dd>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dw>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<db>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dd>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dw>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<db>(0x00012341, 0x00012342, false, false, false);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0xffffffff, 0x00000000, false, false, true);
    

    TestINC<dw>(0xffffffff, 0xffff0000, false, false, true);
    

    TestINC<db>(0xffffffff, 0xffffff00, false, false, true);
    

    TestINC<dd>(0x7fffffff, 0x80000000, true, true, false);
    

    TestINC<dw>(0x7fffffff, 0x7fff0000, false, false, true);
    

    TestINC<db>(0x7fffffff, 0x7fffff00, false, false, true);
    

    TestINC<dd>(0x7fffffff, 0x80000000, true, true, false);
    

    TestINC<dw>(0x7fffffff, 0x7fff0000, false, false, true);
    

    TestINC<db>(0x7fffffff, 0x7fffff00, false, false, true);
    

    TestINC<dd>(0x7fffffff, 0x80000000, true, true, false);
    

    TestINC<dw>(0x7fffffff, 0x7fff0000, false, false, true);
    

    TestINC<db>(0x7fffffff, 0x7fffff00, false, false, true);
    

    TestINC<dd>(0x7fffffff, 0x80000000, true, true, false);
    

    TestINC<dw>(0x7fffffff, 0x7fff0000, false, false, true);
    

    TestINC<db>(0x7fffffff, 0x7fffff00, false, false, true);
    

    TestINC<dd>(0x7fffffff, 0x80000000, true, true, false);
    

    TestINC<dw>(0x7fffffff, 0x7fff0000, false, false, true);
    

    TestINC<db>(0x7fffffff, 0x7fffff00, false, false, true);
    

    TestINC<dd>(0x7fffffff, 0x80000000, true, true, false);
    

    TestINC<dw>(0x7fffffff, 0x7fff0000, false, false, true);
    

    TestINC<db>(0x7fffffff, 0x7fffff00, false, false, true);
    

    TestINC<dd>(0x80000000, 0x80000001, false, true, false);
    

    TestINC<dw>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<db>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<dd>(0x80000000, 0x80000001, false, true, false);
    

    TestINC<dw>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<db>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<dd>(0x80000000, 0x80000001, false, true, false);
    

    TestINC<dw>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<db>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<dd>(0x80000000, 0x80000001, false, true, false);
    

    TestINC<dw>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<db>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<dd>(0x80000000, 0x80000001, false, true, false);
    

    TestINC<dw>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<db>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<dd>(0x80000000, 0x80000001, false, true, false);
    

    TestINC<dw>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<db>(0x80000000, 0x80000001, false, false, false);
    

    TestINC<dd>(0x12347fff, 0x12348000, false, false, false);
    

    TestINC<dw>(0x12347fff, 0x12348000, true, true, false);
    

    TestINC<db>(0x12347fff, 0x12347f00, false, false, true);
    

    TestINC<dd>(0x12347fff, 0x12348000, false, false, false);
    

    TestINC<dw>(0x12347fff, 0x12348000, true, true, false);
    

    TestINC<db>(0x12347fff, 0x12347f00, false, false, true);
    

    TestINC<dd>(0x12347fff, 0x12348000, false, false, false);
    

    TestINC<dw>(0x12347fff, 0x12348000, true, true, false);
    

    TestINC<db>(0x12347fff, 0x12347f00, false, false, true);
    

    TestINC<dd>(0x12347fff, 0x12348000, false, false, false);
    

    TestINC<dw>(0x12347fff, 0x12348000, true, true, false);
    

    TestINC<db>(0x12347fff, 0x12347f00, false, false, true);
    

    TestINC<dd>(0x12347fff, 0x12348000, false, false, false);
    

    TestINC<dw>(0x12347fff, 0x12348000, true, true, false);
    

    TestINC<db>(0x12347fff, 0x12347f00, false, false, true);
    

    TestINC<dd>(0x12347fff, 0x12348000, false, false, false);
    

    TestINC<dw>(0x12347fff, 0x12348000, true, true, false);
    

    TestINC<db>(0x12347fff, 0x12347f00, false, false, true);
    

    TestINC<dd>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dw>(0x12348000, 0x12348001, false, true, false);
    

    TestINC<db>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dd>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dw>(0x12348000, 0x12348001, false, true, false);
    

    TestINC<db>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dd>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dw>(0x12348000, 0x12348001, false, true, false);
    

    TestINC<db>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dd>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dw>(0x12348000, 0x12348001, false, true, false);
    

    TestINC<db>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dd>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dw>(0x12348000, 0x12348001, false, true, false);
    

    TestINC<db>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dd>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dw>(0x12348000, 0x12348001, false, true, false);
    

    TestINC<db>(0x12348000, 0x12348001, false, false, false);
    

    TestINC<dd>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<dw>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<db>(0x12347f7f, 0x12347f80, true, true, false);
    

    TestINC<dd>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<dw>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<db>(0x12347f7f, 0x12347f80, true, true, false);
    

    TestINC<dd>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<dw>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<db>(0x12347f7f, 0x12347f80, true, true, false);
    

    TestINC<dd>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<dw>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<db>(0x12347f7f, 0x12347f80, true, true, false);
    

    TestINC<dd>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<dw>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<db>(0x12347f7f, 0x12347f80, true, true, false);
    

    TestINC<dd>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<dw>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestINC<db>(0x12347f7f, 0x12347f80, true, true, false);
    

    TestINC<dd>(0x12348080, 0x12348081, false, false, false);
    

    TestINC<dw>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<db>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<dd>(0x12348080, 0x12348081, false, false, false);
    

    TestINC<dw>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<db>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<dd>(0x12348080, 0x12348081, false, false, false);
    

    TestINC<dw>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<db>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<dd>(0x12348080, 0x12348081, false, false, false);
    

    TestINC<dw>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<db>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<dd>(0x12348080, 0x12348081, false, false, false);
    

    TestINC<dw>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<db>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<dd>(0x12348080, 0x12348081, false, false, false);
    

    TestINC<dw>(0x12348080, 0x12348081, false, true, false);
    

    TestINC<db>(0x12348080, 0x12348081, false, true, false);
    
  }

  TEST_F(EmulatedInstructionsTest, DEC) {

    TestDEC<dd>(0x12345678, 0x12345677, false, false, false);
    

    TestDEC<dw>(0x12345678, 0x12345677, false, false, false);
    

    TestDEC<db>(0x12345678, 0x12345677, false, false, false);
    

    TestDEC<dd>(0x12345678, 0x12345677, false, false, false);
    

    TestDEC<dw>(0x12345678, 0x12345677, false, false, false);
    

    TestDEC<db>(0x12345678, 0x12345677, false, false, false);
    

    TestDEC<dd>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dw>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<db>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dd>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dw>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<db>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dd>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dw>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<db>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dd>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dw>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<db>(0x00012341, 0x00012340, false, false, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dw>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<db>(0xffffffff, 0xfffffffe, false, true, false);
    

    TestDEC<dd>(0x7fffffff, 0x7ffffffe, false, false, false);
    

    TestDEC<dw>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<db>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<dd>(0x7fffffff, 0x7ffffffe, false, false, false);
    

    TestDEC<dw>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<db>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<dd>(0x7fffffff, 0x7ffffffe, false, false, false);
    

    TestDEC<dw>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<db>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<dd>(0x7fffffff, 0x7ffffffe, false, false, false);
    

    TestDEC<dw>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<db>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<dd>(0x7fffffff, 0x7ffffffe, false, false, false);
    

    TestDEC<dw>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<db>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<dd>(0x7fffffff, 0x7ffffffe, false, false, false);
    

    TestDEC<dw>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<db>(0x7fffffff, 0x7ffffffe, false, true, false);
    

    TestDEC<dd>(0x80000000, 0x7fffffff, true, false, false);
    

    TestDEC<dw>(0x80000000, 0x8000ffff, false, true, false);
    

    TestDEC<db>(0x80000000, 0x800000ff, false, true, false);
    

    TestDEC<dd>(0x80000000, 0x7fffffff, true, false, false);
    

    TestDEC<dw>(0x80000000, 0x8000ffff, false, true, false);
    

    TestDEC<db>(0x80000000, 0x800000ff, false, true, false);
    

    TestDEC<dd>(0x80000000, 0x7fffffff, true, false, false);
    

    TestDEC<dw>(0x80000000, 0x8000ffff, false, true, false);
    

    TestDEC<db>(0x80000000, 0x800000ff, false, true, false);
    

    TestDEC<dd>(0x80000000, 0x7fffffff, true, false, false);
    

    TestDEC<dw>(0x80000000, 0x8000ffff, false, true, false);
    

    TestDEC<db>(0x80000000, 0x800000ff, false, true, false);
    

    TestDEC<dd>(0x80000000, 0x7fffffff, true, false, false);
    

    TestDEC<dw>(0x80000000, 0x8000ffff, false, true, false);
    

    TestDEC<db>(0x80000000, 0x800000ff, false, true, false);
    

    TestDEC<dd>(0x80000000, 0x7fffffff, true, false, false);
    

    TestDEC<dw>(0x80000000, 0x8000ffff, false, true, false);
    

    TestDEC<db>(0x80000000, 0x800000ff, false, true, false);
    

    TestDEC<dd>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<dw>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<db>(0x12347fff, 0x12347ffe, false, true, false);
    

    TestDEC<dd>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<dw>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<db>(0x12347fff, 0x12347ffe, false, true, false);
    

    TestDEC<dd>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<dw>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<db>(0x12347fff, 0x12347ffe, false, true, false);
    

    TestDEC<dd>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<dw>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<db>(0x12347fff, 0x12347ffe, false, true, false);
    

    TestDEC<dd>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<dw>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<db>(0x12347fff, 0x12347ffe, false, true, false);
    

    TestDEC<dd>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<dw>(0x12347fff, 0x12347ffe, false, false, false);
    

    TestDEC<db>(0x12347fff, 0x12347ffe, false, true, false);
    

    TestDEC<dd>(0x12348000, 0x12347fff, false, false, false);
    

    TestDEC<dw>(0x12348000, 0x12347fff, true, false, false);
    

    TestDEC<db>(0x12348000, 0x123480ff, false, true, false);
    

    TestDEC<dd>(0x12348000, 0x12347fff, false, false, false);
    

    TestDEC<dw>(0x12348000, 0x12347fff, true, false, false);
    

    TestDEC<db>(0x12348000, 0x123480ff, false, true, false);
    

    TestDEC<dd>(0x12348000, 0x12347fff, false, false, false);
    

    TestDEC<dw>(0x12348000, 0x12347fff, true, false, false);
    

    TestDEC<db>(0x12348000, 0x123480ff, false, true, false);
    

    TestDEC<dd>(0x12348000, 0x12347fff, false, false, false);
    

    TestDEC<dw>(0x12348000, 0x12347fff, true, false, false);
    

    TestDEC<db>(0x12348000, 0x123480ff, false, true, false);
    

    TestDEC<dd>(0x12348000, 0x12347fff, false, false, false);
    

    TestDEC<dw>(0x12348000, 0x12347fff, true, false, false);
    

    TestDEC<db>(0x12348000, 0x123480ff, false, true, false);
    

    TestDEC<dd>(0x12348000, 0x12347fff, false, false, false);
    

    TestDEC<dw>(0x12348000, 0x12347fff, true, false, false);
    

    TestDEC<db>(0x12348000, 0x123480ff, false, true, false);
    

    TestDEC<dd>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dw>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<db>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dd>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dw>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<db>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dd>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dw>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<db>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dd>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dw>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<db>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dd>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dw>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<db>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dd>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dw>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<db>(0x12347f7f, 0x12347f7e, false, false, false);
    

    TestDEC<dd>(0x12348080, 0x1234807f, false, false, false);
    

    TestDEC<dw>(0x12348080, 0x1234807f, false, true, false);
    

    TestDEC<db>(0x12348080, 0x1234807f, true, false, false);
    

    TestDEC<dd>(0x12348080, 0x1234807f, false, false, false);
    

    TestDEC<dw>(0x12348080, 0x1234807f, false, true, false);
    

    TestDEC<db>(0x12348080, 0x1234807f, true, false, false);
    

    TestDEC<dd>(0x12348080, 0x1234807f, false, false, false);
    

    TestDEC<dw>(0x12348080, 0x1234807f, false, true, false);
    

    TestDEC<db>(0x12348080, 0x1234807f, true, false, false);
    

    TestDEC<dd>(0x12348080, 0x1234807f, false, false, false);
    

    TestDEC<dw>(0x12348080, 0x1234807f, false, true, false);
    

    TestDEC<db>(0x12348080, 0x1234807f, true, false, false);
    

    TestDEC<dd>(0x12348080, 0x1234807f, false, false, false);
    

    TestDEC<dw>(0x12348080, 0x1234807f, false, true, false);
    

    TestDEC<db>(0x12348080, 0x1234807f, true, false, false);
    

    TestDEC<dd>(0x12348080, 0x1234807f, false, false, false);
    

    TestDEC<dw>(0x12348080, 0x1234807f, false, true, false);
    

    TestDEC<db>(0x12348080, 0x1234807f, true, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, NEG) {

    TestNEG<dd>(0x12345678, 0xedcba988, true, false, true, false);
    

    TestNEG<dw>(0x12345678, 0x1234a988, true, false, true, false);
    

    TestNEG<db>(0x12345678, 0x12345688, true, false, true, false);
    

    TestNEG<dd>(0x12345678, 0xedcba988, true, false, true, false);
    

    TestNEG<dw>(0x12345678, 0x1234a988, true, false, true, false);
    

    TestNEG<db>(0x12345678, 0x12345688, true, false, true, false);
    

    TestNEG<dd>(0x00012341, 0xfffedcbf, true, false, true, false);
    

    TestNEG<dw>(0x00012341, 0x0001dcbf, true, false, true, false);
    

    TestNEG<db>(0x00012341, 0x000123bf, true, false, true, false);
    

    TestNEG<dd>(0x00012341, 0xfffedcbf, true, false, true, false);
    

    TestNEG<dw>(0x00012341, 0x0001dcbf, true, false, true, false);
    

    TestNEG<db>(0x00012341, 0x000123bf, true, false, true, false);
    

    TestNEG<dd>(0x00012341, 0xfffedcbf, true, false, true, false);
    

    TestNEG<dw>(0x00012341, 0x0001dcbf, true, false, true, false);
    

    TestNEG<db>(0x00012341, 0x000123bf, true, false, true, false);
    

    TestNEG<dd>(0x00012341, 0xfffedcbf, true, false, true, false);
    

    TestNEG<dw>(0x00012341, 0x0001dcbf, true, false, true, false);
    

    TestNEG<db>(0x00012341, 0x000123bf, true, false, true, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0xffffffff, 0x00000001, true, false, false, false);
    

    TestNEG<dw>(0xffffffff, 0xffff0001, true, false, false, false);
    

    TestNEG<db>(0xffffffff, 0xffffff01, true, false, false, false);
    

    TestNEG<dd>(0x7fffffff, 0x80000001, true, false, true, false);
    

    TestNEG<dw>(0x7fffffff, 0x7fff0001, true, false, false, false);
    

    TestNEG<db>(0x7fffffff, 0x7fffff01, true, false, false, false);
    

    TestNEG<dd>(0x7fffffff, 0x80000001, true, false, true, false);
    

    TestNEG<dw>(0x7fffffff, 0x7fff0001, true, false, false, false);
    

    TestNEG<db>(0x7fffffff, 0x7fffff01, true, false, false, false);
    

    TestNEG<dd>(0x7fffffff, 0x80000001, true, false, true, false);
    

    TestNEG<dw>(0x7fffffff, 0x7fff0001, true, false, false, false);
    

    TestNEG<db>(0x7fffffff, 0x7fffff01, true, false, false, false);
    

    TestNEG<dd>(0x7fffffff, 0x80000001, true, false, true, false);
    

    TestNEG<dw>(0x7fffffff, 0x7fff0001, true, false, false, false);
    

    TestNEG<db>(0x7fffffff, 0x7fffff01, true, false, false, false);
    

    TestNEG<dd>(0x7fffffff, 0x80000001, true, false, true, false);
    

    TestNEG<dw>(0x7fffffff, 0x7fff0001, true, false, false, false);
    

    TestNEG<db>(0x7fffffff, 0x7fffff01, true, false, false, false);
    

    TestNEG<dd>(0x7fffffff, 0x80000001, true, false, true, false);
    

    TestNEG<dw>(0x7fffffff, 0x7fff0001, true, false, false, false);
    

    TestNEG<db>(0x7fffffff, 0x7fffff01, true, false, false, false);
    

    TestNEG<dd>(0x80000000, 0x80000000, true, true, true, false);
    

    TestNEG<dw>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<db>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<dd>(0x80000000, 0x80000000, true, true, true, false);
    

    TestNEG<dw>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<db>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<dd>(0x80000000, 0x80000000, true, true, true, false);
    

    TestNEG<dw>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<db>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<dd>(0x80000000, 0x80000000, true, true, true, false);
    

    TestNEG<dw>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<db>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<dd>(0x80000000, 0x80000000, true, true, true, false);
    

    TestNEG<dw>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<db>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<dd>(0x80000000, 0x80000000, true, true, true, false);
    

    TestNEG<dw>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<db>(0x80000000, 0x80000000, false, false, false, true);
    

    TestNEG<dd>(0x12347fff, 0xedcb8001, true, false, true, false);
    

    TestNEG<dw>(0x12347fff, 0x12348001, true, false, true, false);
    

    TestNEG<db>(0x12347fff, 0x12347f01, true, false, false, false);
    

    TestNEG<dd>(0x12347fff, 0xedcb8001, true, false, true, false);
    

    TestNEG<dw>(0x12347fff, 0x12348001, true, false, true, false);
    

    TestNEG<db>(0x12347fff, 0x12347f01, true, false, false, false);
    

    TestNEG<dd>(0x12347fff, 0xedcb8001, true, false, true, false);
    

    TestNEG<dw>(0x12347fff, 0x12348001, true, false, true, false);
    

    TestNEG<db>(0x12347fff, 0x12347f01, true, false, false, false);
    

    TestNEG<dd>(0x12347fff, 0xedcb8001, true, false, true, false);
    

    TestNEG<dw>(0x12347fff, 0x12348001, true, false, true, false);
    

    TestNEG<db>(0x12347fff, 0x12347f01, true, false, false, false);
    

    TestNEG<dd>(0x12347fff, 0xedcb8001, true, false, true, false);
    

    TestNEG<dw>(0x12347fff, 0x12348001, true, false, true, false);
    

    TestNEG<db>(0x12347fff, 0x12347f01, true, false, false, false);
    

    TestNEG<dd>(0x12347fff, 0xedcb8001, true, false, true, false);
    

    TestNEG<dw>(0x12347fff, 0x12348001, true, false, true, false);
    

    TestNEG<db>(0x12347fff, 0x12347f01, true, false, false, false);
    

    TestNEG<dd>(0x12348000, 0xedcb8000, true, false, true, false);
    

    TestNEG<dw>(0x12348000, 0x12348000, true, true, true, false);
    

    TestNEG<db>(0x12348000, 0x12348000, false, false, false, true);
    

    TestNEG<dd>(0x12348000, 0xedcb8000, true, false, true, false);
    

    TestNEG<dw>(0x12348000, 0x12348000, true, true, true, false);
    

    TestNEG<db>(0x12348000, 0x12348000, false, false, false, true);
    

    TestNEG<dd>(0x12348000, 0xedcb8000, true, false, true, false);
    

    TestNEG<dw>(0x12348000, 0x12348000, true, true, true, false);
    

    TestNEG<db>(0x12348000, 0x12348000, false, false, false, true);
    

    TestNEG<dd>(0x12348000, 0xedcb8000, true, false, true, false);
    

    TestNEG<dw>(0x12348000, 0x12348000, true, true, true, false);
    

    TestNEG<db>(0x12348000, 0x12348000, false, false, false, true);
    

    TestNEG<dd>(0x12348000, 0xedcb8000, true, false, true, false);
    

    TestNEG<dw>(0x12348000, 0x12348000, true, true, true, false);
    

    TestNEG<db>(0x12348000, 0x12348000, false, false, false, true);
    

    TestNEG<dd>(0x12348000, 0xedcb8000, true, false, true, false);
    

    TestNEG<dw>(0x12348000, 0x12348000, true, true, true, false);
    

    TestNEG<db>(0x12348000, 0x12348000, false, false, false, true);
    

    TestNEG<dd>(0x12347f7f, 0xedcb8081, true, false, true, false);
    

    TestNEG<dw>(0x12347f7f, 0x12348081, true, false, true, false);
    

    TestNEG<db>(0x12347f7f, 0x12347f81, true, false, true, false);
    

    TestNEG<dd>(0x12347f7f, 0xedcb8081, true, false, true, false);
    

    TestNEG<dw>(0x12347f7f, 0x12348081, true, false, true, false);
    

    TestNEG<db>(0x12347f7f, 0x12347f81, true, false, true, false);
    

    TestNEG<dd>(0x12347f7f, 0xedcb8081, true, false, true, false);
    

    TestNEG<dw>(0x12347f7f, 0x12348081, true, false, true, false);
    

    TestNEG<db>(0x12347f7f, 0x12347f81, true, false, true, false);
    

    TestNEG<dd>(0x12347f7f, 0xedcb8081, true, false, true, false);
    

    TestNEG<dw>(0x12347f7f, 0x12348081, true, false, true, false);
    

    TestNEG<db>(0x12347f7f, 0x12347f81, true, false, true, false);
    

    TestNEG<dd>(0x12347f7f, 0xedcb8081, true, false, true, false);
    

    TestNEG<dw>(0x12347f7f, 0x12348081, true, false, true, false);
    

    TestNEG<db>(0x12347f7f, 0x12347f81, true, false, true, false);
    

    TestNEG<dd>(0x12347f7f, 0xedcb8081, true, false, true, false);
    

    TestNEG<dw>(0x12347f7f, 0x12348081, true, false, true, false);
    

    TestNEG<db>(0x12347f7f, 0x12347f81, true, false, true, false);
    

    TestNEG<dd>(0x12348080, 0xedcb7f80, true, false, true, false);
    

    TestNEG<dw>(0x12348080, 0x12347f80, true, false, false, false);
    

    TestNEG<db>(0x12348080, 0x12348080, true, true, true, false);
    

    TestNEG<dd>(0x12348080, 0xedcb7f80, true, false, true, false);
    

    TestNEG<dw>(0x12348080, 0x12347f80, true, false, false, false);
    

    TestNEG<db>(0x12348080, 0x12348080, true, true, true, false);
    

    TestNEG<dd>(0x12348080, 0xedcb7f80, true, false, true, false);
    

    TestNEG<dw>(0x12348080, 0x12347f80, true, false, false, false);
    

    TestNEG<db>(0x12348080, 0x12348080, true, true, true, false);
    

    TestNEG<dd>(0x12348080, 0xedcb7f80, true, false, true, false);
    

    TestNEG<dw>(0x12348080, 0x12347f80, true, false, false, false);
    

    TestNEG<db>(0x12348080, 0x12348080, true, true, true, false);
    

    TestNEG<dd>(0x12348080, 0xedcb7f80, true, false, true, false);
    

    TestNEG<dw>(0x12348080, 0x12347f80, true, false, false, false);
    

    TestNEG<db>(0x12348080, 0x12348080, true, true, true, false);
    

    TestNEG<dd>(0x12348080, 0xedcb7f80, true, false, true, false);
    

    TestNEG<dw>(0x12348080, 0x12347f80, true, false, false, false);
    

    TestNEG<db>(0x12348080, 0x12348080, true, true, true, false);
    
  }

  TEST_F(EmulatedInstructionsTest, NOT) {

    TestNOT<dd>(0x12345678, 0xedcba987, false, false, false);
    

    TestNOT<dw>(0x12345678, 0x1234a987, false, false, false);
    

    TestNOT<db>(0x12345678, 0x12345687, false, false, false);
    

    TestNOT<dd>(0x12345678, 0xedcba987, false, false, false);
    

    TestNOT<dw>(0x12345678, 0x1234a987, false, false, false);
    

    TestNOT<db>(0x12345678, 0x12345687, false, false, false);
    

    TestNOT<dd>(0x00012341, 0xfffedcbe, false, false, false);
    

    TestNOT<dw>(0x00012341, 0x0001dcbe, false, false, false);
    

    TestNOT<db>(0x00012341, 0x000123be, false, false, false);
    

    TestNOT<dd>(0x00012341, 0xfffedcbe, false, false, false);
    

    TestNOT<dw>(0x00012341, 0x0001dcbe, false, false, false);
    

    TestNOT<db>(0x00012341, 0x000123be, false, false, false);
    

    TestNOT<dd>(0x00012341, 0xfffedcbe, false, false, false);
    

    TestNOT<dw>(0x00012341, 0x0001dcbe, false, false, false);
    

    TestNOT<db>(0x00012341, 0x000123be, false, false, false);
    

    TestNOT<dd>(0x00012341, 0xfffedcbe, false, false, false);
    

    TestNOT<dw>(0x00012341, 0x0001dcbe, false, false, false);
    

    TestNOT<db>(0x00012341, 0x000123be, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0xffffffff, 0x00000000, false, false, false);
    

    TestNOT<dw>(0xffffffff, 0xffff0000, false, false, false);
    

    TestNOT<db>(0xffffffff, 0xffffff00, false, false, false);
    

    TestNOT<dd>(0x7fffffff, 0x80000000, false, false, false);
    

    TestNOT<dw>(0x7fffffff, 0x7fff0000, false, false, false);
    

    TestNOT<db>(0x7fffffff, 0x7fffff00, false, false, false);
    

    TestNOT<dd>(0x7fffffff, 0x80000000, false, false, false);
    

    TestNOT<dw>(0x7fffffff, 0x7fff0000, false, false, false);
    

    TestNOT<db>(0x7fffffff, 0x7fffff00, false, false, false);
    

    TestNOT<dd>(0x7fffffff, 0x80000000, false, false, false);
    

    TestNOT<dw>(0x7fffffff, 0x7fff0000, false, false, false);
    

    TestNOT<db>(0x7fffffff, 0x7fffff00, false, false, false);
    

    TestNOT<dd>(0x7fffffff, 0x80000000, false, false, false);
    

    TestNOT<dw>(0x7fffffff, 0x7fff0000, false, false, false);
    

    TestNOT<db>(0x7fffffff, 0x7fffff00, false, false, false);
    

    TestNOT<dd>(0x7fffffff, 0x80000000, false, false, false);
    

    TestNOT<dw>(0x7fffffff, 0x7fff0000, false, false, false);
    

    TestNOT<db>(0x7fffffff, 0x7fffff00, false, false, false);
    

    TestNOT<dd>(0x7fffffff, 0x80000000, false, false, false);
    

    TestNOT<dw>(0x7fffffff, 0x7fff0000, false, false, false);
    

    TestNOT<db>(0x7fffffff, 0x7fffff00, false, false, false);
    

    TestNOT<dd>(0x80000000, 0x7fffffff, false, false, false);
    

    TestNOT<dw>(0x80000000, 0x8000ffff, false, false, false);
    

    TestNOT<db>(0x80000000, 0x800000ff, false, false, false);
    

    TestNOT<dd>(0x80000000, 0x7fffffff, false, false, false);
    

    TestNOT<dw>(0x80000000, 0x8000ffff, false, false, false);
    

    TestNOT<db>(0x80000000, 0x800000ff, false, false, false);
    

    TestNOT<dd>(0x80000000, 0x7fffffff, false, false, false);
    

    TestNOT<dw>(0x80000000, 0x8000ffff, false, false, false);
    

    TestNOT<db>(0x80000000, 0x800000ff, false, false, false);
    

    TestNOT<dd>(0x80000000, 0x7fffffff, false, false, false);
    

    TestNOT<dw>(0x80000000, 0x8000ffff, false, false, false);
    

    TestNOT<db>(0x80000000, 0x800000ff, false, false, false);
    

    TestNOT<dd>(0x80000000, 0x7fffffff, false, false, false);
    

    TestNOT<dw>(0x80000000, 0x8000ffff, false, false, false);
    

    TestNOT<db>(0x80000000, 0x800000ff, false, false, false);
    

    TestNOT<dd>(0x80000000, 0x7fffffff, false, false, false);
    

    TestNOT<dw>(0x80000000, 0x8000ffff, false, false, false);
    

    TestNOT<db>(0x80000000, 0x800000ff, false, false, false);
    

    TestNOT<dd>(0x12347fff, 0xedcb8000, false, false, false);
    

    TestNOT<dw>(0x12347fff, 0x12348000, false, false, false);
    

    TestNOT<db>(0x12347fff, 0x12347f00, false, false, false);
    

    TestNOT<dd>(0x12347fff, 0xedcb8000, false, false, false);
    

    TestNOT<dw>(0x12347fff, 0x12348000, false, false, false);
    

    TestNOT<db>(0x12347fff, 0x12347f00, false, false, false);
    

    TestNOT<dd>(0x12347fff, 0xedcb8000, false, false, false);
    

    TestNOT<dw>(0x12347fff, 0x12348000, false, false, false);
    

    TestNOT<db>(0x12347fff, 0x12347f00, false, false, false);
    

    TestNOT<dd>(0x12347fff, 0xedcb8000, false, false, false);
    

    TestNOT<dw>(0x12347fff, 0x12348000, false, false, false);
    

    TestNOT<db>(0x12347fff, 0x12347f00, false, false, false);
    

    TestNOT<dd>(0x12347fff, 0xedcb8000, false, false, false);
    

    TestNOT<dw>(0x12347fff, 0x12348000, false, false, false);
    

    TestNOT<db>(0x12347fff, 0x12347f00, false, false, false);
    

    TestNOT<dd>(0x12347fff, 0xedcb8000, false, false, false);
    

    TestNOT<dw>(0x12347fff, 0x12348000, false, false, false);
    

    TestNOT<db>(0x12347fff, 0x12347f00, false, false, false);
    

    TestNOT<dd>(0x12348000, 0xedcb7fff, false, false, false);
    

    TestNOT<dw>(0x12348000, 0x12347fff, false, false, false);
    

    TestNOT<db>(0x12348000, 0x123480ff, false, false, false);
    

    TestNOT<dd>(0x12348000, 0xedcb7fff, false, false, false);
    

    TestNOT<dw>(0x12348000, 0x12347fff, false, false, false);
    

    TestNOT<db>(0x12348000, 0x123480ff, false, false, false);
    

    TestNOT<dd>(0x12348000, 0xedcb7fff, false, false, false);
    

    TestNOT<dw>(0x12348000, 0x12347fff, false, false, false);
    

    TestNOT<db>(0x12348000, 0x123480ff, false, false, false);
    

    TestNOT<dd>(0x12348000, 0xedcb7fff, false, false, false);
    

    TestNOT<dw>(0x12348000, 0x12347fff, false, false, false);
    

    TestNOT<db>(0x12348000, 0x123480ff, false, false, false);
    

    TestNOT<dd>(0x12348000, 0xedcb7fff, false, false, false);
    

    TestNOT<dw>(0x12348000, 0x12347fff, false, false, false);
    

    TestNOT<db>(0x12348000, 0x123480ff, false, false, false);
    

    TestNOT<dd>(0x12348000, 0xedcb7fff, false, false, false);
    

    TestNOT<dw>(0x12348000, 0x12347fff, false, false, false);
    

    TestNOT<db>(0x12348000, 0x123480ff, false, false, false);
    

    TestNOT<dd>(0x12347f7f, 0xedcb8080, false, false, false);
    

    TestNOT<dw>(0x12347f7f, 0x12348080, false, false, false);
    

    TestNOT<db>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestNOT<dd>(0x12347f7f, 0xedcb8080, false, false, false);
    

    TestNOT<dw>(0x12347f7f, 0x12348080, false, false, false);
    

    TestNOT<db>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestNOT<dd>(0x12347f7f, 0xedcb8080, false, false, false);
    

    TestNOT<dw>(0x12347f7f, 0x12348080, false, false, false);
    

    TestNOT<db>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestNOT<dd>(0x12347f7f, 0xedcb8080, false, false, false);
    

    TestNOT<dw>(0x12347f7f, 0x12348080, false, false, false);
    

    TestNOT<db>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestNOT<dd>(0x12347f7f, 0xedcb8080, false, false, false);
    

    TestNOT<dw>(0x12347f7f, 0x12348080, false, false, false);
    

    TestNOT<db>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestNOT<dd>(0x12347f7f, 0xedcb8080, false, false, false);
    

    TestNOT<dw>(0x12347f7f, 0x12348080, false, false, false);
    

    TestNOT<db>(0x12347f7f, 0x12347f80, false, false, false);
    

    TestNOT<dd>(0x12348080, 0xedcb7f7f, false, false, false);
    

    TestNOT<dw>(0x12348080, 0x12347f7f, false, false, false);
    

    TestNOT<db>(0x12348080, 0x1234807f, false, false, false);
    

    TestNOT<dd>(0x12348080, 0xedcb7f7f, false, false, false);
    

    TestNOT<dw>(0x12348080, 0x12347f7f, false, false, false);
    

    TestNOT<db>(0x12348080, 0x1234807f, false, false, false);
    

    TestNOT<dd>(0x12348080, 0xedcb7f7f, false, false, false);
    

    TestNOT<dw>(0x12348080, 0x12347f7f, false, false, false);
    

    TestNOT<db>(0x12348080, 0x1234807f, false, false, false);
    

    TestNOT<dd>(0x12348080, 0xedcb7f7f, false, false, false);
    

    TestNOT<dw>(0x12348080, 0x12347f7f, false, false, false);
    

    TestNOT<db>(0x12348080, 0x1234807f, false, false, false);
    

    TestNOT<dd>(0x12348080, 0xedcb7f7f, false, false, false);
    

    TestNOT<dw>(0x12348080, 0x12347f7f, false, false, false);
    

    TestNOT<db>(0x12348080, 0x1234807f, false, false, false);
    

    TestNOT<dd>(0x12348080, 0xedcb7f7f, false, false, false);
    

    TestNOT<dw>(0x12348080, 0x12347f7f, false, false, false);
    

    TestNOT<db>(0x12348080, 0x1234807f, false, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, SHL) {

    TestSHL<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSHL<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSHL<dd>(0x12345678, 0x00000001, 0x2468acf0, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000001, 0x1234acf0, false, true, true, false, false);
    

    TestSHL<db>(0x12345678, 0x00000001, 0x123456f0, false, true, true, false, false);
    

    TestSHL<dd>(0x12345678, 0x00000002, 0x48d159e0, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000002, 0x123459e0, true, false, false, false, false);
    

    TestSHL<db>(0x12345678, 0x00000002, 0x123456e0, true, false, true, false, false);
    

    TestSHL<dd>(0x12345678, 0x00000003, 0x91a2b3c0, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000003, 0x1234b3c0, false, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x00000003, 0x123456c0, true, false, true, false, false);
    

    TestSHL<dd>(0x12345678, 0x00000004, 0x23456780, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000004, 0x12346780, true, false, false, false, false);
    

    TestSHL<db>(0x12345678, 0x00000004, 0x12345680, true, false, true, false, false);
    

    TestSHL<dd>(0x12345678, 0x00000005, 0x468acf00, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000005, 0x1234cf00, false, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x00000005, 0x12345600, true, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000006, 0x8d159e00, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000006, 0x12349e00, true, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x00000006, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000007, 0x1a2b3c00, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000007, 0x12343c00, true, false, false, false, false);
    

    TestSHL<db>(0x12345678, 0x00000007, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000008, 0x34567800, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000008, 0x12347800, false, false, false, false, false);
    

    TestSHL<db>(0x12345678, 0x00000008, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000009, 0x68acf000, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000009, 0x1234f000, false, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x00000009, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000000a, 0xd159e000, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000000a, 0x1234e000, true, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x0000000a, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000000b, 0xa2b3c000, true, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000000b, 0x1234c000, true, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x0000000b, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000000c, 0x45678000, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000000c, 0x12348000, true, false, true, false, false);
    

    TestSHL<db>(0x12345678, 0x0000000c, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000000d, 0x8acf0000, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000000d, 0x12340000, true, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000000d, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000000e, 0x159e0000, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000000e, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000000e, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000000f, 0x2b3c0000, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000000f, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000000f, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000010, 0x56780000, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000010, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000010, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000011, 0xacf00000, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000011, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000011, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000012, 0x59e00000, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000012, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000012, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000013, 0xb3c00000, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000013, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000013, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000014, 0x67800000, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000014, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000014, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000015, 0xcf000000, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000015, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000015, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000016, 0x9e000000, true, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000016, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000016, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000017, 0x3c000000, true, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000017, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000017, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000018, 0x78000000, false, false, false, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000018, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000018, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x00000019, 0xf0000000, false, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x00000019, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x00000019, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000001a, 0xe0000000, true, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000001a, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000001a, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000001b, 0xc0000000, true, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000001b, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000001b, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000001c, 0x80000000, true, false, true, false, false);
    

    TestSHL<dw>(0x12345678, 0x0000001c, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000001c, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000001d, 0x00000000, true, false, false, true, false);
    

    TestSHL<dw>(0x12345678, 0x0000001d, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000001d, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000001e, 0x00000000, false, false, false, true, false);
    

    TestSHL<dw>(0x12345678, 0x0000001e, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000001e, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x12345678, 0x0000001f, 0x00000000, false, false, false, true, false);
    

    TestSHL<dw>(0x12345678, 0x0000001f, 0x12340000, false, false, false, true, false);
    

    TestSHL<db>(0x12345678, 0x0000001f, 0x12345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000001, 0x0468acf2, true, true, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000001, 0x8234acf2, false, true, true, false, false);
    

    TestSHL<db>(0x82345679, 0x00000001, 0x823456f2, false, true, true, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000002, 0x08d159e4, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000002, 0x823459e4, true, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x00000002, 0x823456e4, true, false, true, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000003, 0x11a2b3c8, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000003, 0x8234b3c8, false, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x00000003, 0x823456c8, true, false, true, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000004, 0x23456790, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000004, 0x82346790, true, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x00000004, 0x82345690, true, false, true, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000005, 0x468acf20, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000005, 0x8234cf20, false, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x00000005, 0x82345620, true, false, false, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000006, 0x8d159e40, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000006, 0x82349e40, true, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x00000006, 0x82345640, false, false, false, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000007, 0x1a2b3c80, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000007, 0x82343c80, true, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x00000007, 0x82345680, false, false, true, false, false);
    

    TestSHL<dd>(0x82345679, 0x00000008, 0x34567900, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000008, 0x82347900, false, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x00000008, 0x82345600, true, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000009, 0x68acf200, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000009, 0x8234f200, false, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x00000009, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000000a, 0xd159e400, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000000a, 0x8234e400, true, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x0000000a, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000000b, 0xa2b3c800, true, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000000b, 0x8234c800, true, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x0000000b, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000000c, 0x45679000, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000000c, 0x82349000, true, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x0000000c, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000000d, 0x8acf2000, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000000d, 0x82342000, true, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x0000000d, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000000e, 0x159e4000, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000000e, 0x82344000, false, false, false, false, false);
    

    TestSHL<db>(0x82345679, 0x0000000e, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000000f, 0x2b3c8000, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000000f, 0x82348000, false, false, true, false, false);
    

    TestSHL<db>(0x82345679, 0x0000000f, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000010, 0x56790000, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000010, 0x82340000, true, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000010, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000011, 0xacf20000, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000011, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000011, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000012, 0x59e40000, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000012, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000012, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000013, 0xb3c80000, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000013, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000013, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000014, 0x67900000, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000014, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000014, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000015, 0xcf200000, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000015, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000015, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000016, 0x9e400000, true, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000016, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000016, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000017, 0x3c800000, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000017, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000017, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000018, 0x79000000, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000018, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000018, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x00000019, 0xf2000000, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x00000019, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x00000019, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000001a, 0xe4000000, true, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000001a, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x0000001a, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000001b, 0xc8000000, true, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000001b, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x0000001b, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000001c, 0x90000000, true, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000001c, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x0000001c, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000001d, 0x20000000, true, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000001d, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x0000001d, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000001e, 0x40000000, false, false, false, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000001e, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x0000001e, 0x82345600, false, false, false, true, false);
    

    TestSHL<dd>(0x82345679, 0x0000001f, 0x80000000, false, false, true, false, false);
    

    TestSHL<dw>(0x82345679, 0x0000001f, 0x82340000, false, false, false, true, false);
    

    TestSHL<db>(0x82345679, 0x0000001f, 0x82345600, false, false, false, true, false);
    
  }

  TEST_F(EmulatedInstructionsTest, SHR) {

    TestSHR<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000001, 0x091a2b3c, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000001, 0x12342b3c, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000001, 0x1234563c, false, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000002, 0x048d159e, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000002, 0x1234159e, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000002, 0x1234561e, false, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000003, 0x02468acf, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000003, 0x12340acf, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000003, 0x1234560f, false, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000004, 0x01234567, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000004, 0x12340567, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000004, 0x12345607, true, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000005, 0x0091a2b3, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000005, 0x123402b3, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000005, 0x12345603, true, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000006, 0x0048d159, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000006, 0x12340159, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000006, 0x12345601, true, false, false, false, false);
    

    TestSHR<dd>(0x12345678, 0x00000007, 0x002468ac, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000007, 0x123400ac, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000007, 0x12345600, true, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000008, 0x00123456, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000008, 0x12340056, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000008, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000009, 0x00091a2b, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000009, 0x1234002b, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x00000009, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000000a, 0x00048d15, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000000a, 0x12340015, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x0000000a, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000000b, 0x0002468a, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000000b, 0x1234000a, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x0000000b, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000000c, 0x00012345, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000000c, 0x12340005, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x0000000c, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000000d, 0x000091a2, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000000d, 0x12340002, true, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x0000000d, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000000e, 0x000048d1, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000000e, 0x12340001, false, false, false, false, false);
    

    TestSHR<db>(0x12345678, 0x0000000e, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000000f, 0x00002468, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000000f, 0x12340000, true, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000000f, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000010, 0x00001234, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000010, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000010, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000011, 0x0000091a, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000011, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000011, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000012, 0x0000048d, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000012, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000012, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000013, 0x00000246, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000013, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000013, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000014, 0x00000123, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000014, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000014, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000015, 0x00000091, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000015, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000015, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000016, 0x00000048, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000016, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000016, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000017, 0x00000024, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000017, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000017, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000018, 0x00000012, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000018, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000018, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x00000019, 0x00000009, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x00000019, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x00000019, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000001a, 0x00000004, true, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000001a, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000001a, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000001b, 0x00000002, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000001b, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000001b, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000001c, 0x00000001, false, false, false, false, false);
    

    TestSHR<dw>(0x12345678, 0x0000001c, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000001c, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000001d, 0x00000000, true, false, false, true, false);
    

    TestSHR<dw>(0x12345678, 0x0000001d, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000001d, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000001e, 0x00000000, false, false, false, true, false);
    

    TestSHR<dw>(0x12345678, 0x0000001e, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000001e, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x12345678, 0x0000001f, 0x00000000, false, false, false, true, false);
    

    TestSHR<dw>(0x12345678, 0x0000001f, 0x12340000, false, false, false, true, false);
    

    TestSHR<db>(0x12345678, 0x0000001f, 0x12345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000001, 0x411a2b3c, true, true, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000001, 0x82342b3c, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000001, 0x8234563c, true, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000002, 0x208d159e, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000002, 0x8234159e, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000002, 0x8234561e, false, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000003, 0x10468acf, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000003, 0x82340acf, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000003, 0x8234560f, false, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000004, 0x08234567, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000004, 0x82340567, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000004, 0x82345607, true, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000005, 0x0411a2b3, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000005, 0x823402b3, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000005, 0x82345603, true, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000006, 0x0208d159, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000006, 0x82340159, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000006, 0x82345601, true, false, false, false, false);
    

    TestSHR<dd>(0x82345679, 0x00000007, 0x010468ac, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000007, 0x823400ac, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000007, 0x82345600, true, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000008, 0x00823456, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000008, 0x82340056, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000008, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000009, 0x00411a2b, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000009, 0x8234002b, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x00000009, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000000a, 0x00208d15, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000000a, 0x82340015, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x0000000a, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000000b, 0x0010468a, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000000b, 0x8234000a, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x0000000b, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000000c, 0x00082345, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000000c, 0x82340005, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x0000000c, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000000d, 0x000411a2, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000000d, 0x82340002, true, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x0000000d, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000000e, 0x000208d1, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000000e, 0x82340001, false, false, false, false, false);
    

    TestSHR<db>(0x82345679, 0x0000000e, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000000f, 0x00010468, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000000f, 0x82340000, true, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000000f, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000010, 0x00008234, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000010, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000010, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000011, 0x0000411a, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000011, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000011, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000012, 0x0000208d, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000012, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000012, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000013, 0x00001046, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000013, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000013, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000014, 0x00000823, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000014, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000014, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000015, 0x00000411, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000015, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000015, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000016, 0x00000208, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000016, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000016, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000017, 0x00000104, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000017, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000017, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000018, 0x00000082, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000018, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000018, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x00000019, 0x00000041, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x00000019, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x00000019, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000001a, 0x00000020, true, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000001a, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000001a, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000001b, 0x00000010, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000001b, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000001b, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000001c, 0x00000008, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000001c, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000001c, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000001d, 0x00000004, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000001d, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000001d, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000001e, 0x00000002, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000001e, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000001e, 0x82345600, false, false, false, true, false);
    

    TestSHR<dd>(0x82345679, 0x0000001f, 0x00000001, false, false, false, false, false);
    

    TestSHR<dw>(0x82345679, 0x0000001f, 0x82340000, false, false, false, true, false);
    

    TestSHR<db>(0x82345679, 0x0000001f, 0x82345600, false, false, false, true, false);
    
  }

  TEST_F(EmulatedInstructionsTest, SAL) {
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
    // Unhandled instruction: SAL
  }

  TEST_F(EmulatedInstructionsTest, SAR) {

    TestSAR<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000001, 0x091a2b3c, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000001, 0x12342b3c, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000001, 0x1234563c, false, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000002, 0x048d159e, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000002, 0x1234159e, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000002, 0x1234561e, false, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000003, 0x02468acf, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000003, 0x12340acf, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000003, 0x1234560f, false, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000004, 0x01234567, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000004, 0x12340567, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000004, 0x12345607, true, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000005, 0x0091a2b3, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000005, 0x123402b3, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000005, 0x12345603, true, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000006, 0x0048d159, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000006, 0x12340159, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000006, 0x12345601, true, false, false, false, false);
    

    TestSAR<dd>(0x12345678, 0x00000007, 0x002468ac, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000007, 0x123400ac, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000007, 0x12345600, true, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000008, 0x00123456, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000008, 0x12340056, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000008, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000009, 0x00091a2b, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000009, 0x1234002b, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x00000009, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000000a, 0x00048d15, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000000a, 0x12340015, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x0000000a, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000000b, 0x0002468a, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000000b, 0x1234000a, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x0000000b, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000000c, 0x00012345, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000000c, 0x12340005, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x0000000c, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000000d, 0x000091a2, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000000d, 0x12340002, true, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x0000000d, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000000e, 0x000048d1, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000000e, 0x12340001, false, false, false, false, false);
    

    TestSAR<db>(0x12345678, 0x0000000e, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000000f, 0x00002468, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000000f, 0x12340000, true, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000000f, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000010, 0x00001234, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000010, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000010, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000011, 0x0000091a, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000011, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000011, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000012, 0x0000048d, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000012, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000012, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000013, 0x00000246, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000013, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000013, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000014, 0x00000123, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000014, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000014, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000015, 0x00000091, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000015, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000015, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000016, 0x00000048, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000016, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000016, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000017, 0x00000024, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000017, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000017, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000018, 0x00000012, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000018, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000018, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x00000019, 0x00000009, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x00000019, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x00000019, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000001a, 0x00000004, true, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000001a, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000001a, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000001b, 0x00000002, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000001b, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000001b, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000001c, 0x00000001, false, false, false, false, false);
    

    TestSAR<dw>(0x12345678, 0x0000001c, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000001c, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000001d, 0x00000000, true, false, false, true, false);
    

    TestSAR<dw>(0x12345678, 0x0000001d, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000001d, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000001e, 0x00000000, false, false, false, true, false);
    

    TestSAR<dw>(0x12345678, 0x0000001e, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000001e, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x12345678, 0x0000001f, 0x00000000, false, false, false, true, false);
    

    TestSAR<dw>(0x12345678, 0x0000001f, 0x12340000, false, false, false, true, false);
    

    TestSAR<db>(0x12345678, 0x0000001f, 0x12345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000001, 0xc11a2b3c, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000001, 0x82342b3c, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000001, 0x8234563c, true, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000002, 0xe08d159e, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000002, 0x8234159e, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000002, 0x8234561e, false, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000003, 0xf0468acf, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000003, 0x82340acf, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000003, 0x8234560f, false, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000004, 0xf8234567, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000004, 0x82340567, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000004, 0x82345607, true, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000005, 0xfc11a2b3, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000005, 0x823402b3, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000005, 0x82345603, true, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000006, 0xfe08d159, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000006, 0x82340159, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000006, 0x82345601, true, false, false, false, false);
    

    TestSAR<dd>(0x82345679, 0x00000007, 0xff0468ac, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000007, 0x823400ac, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000007, 0x82345600, true, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000008, 0xff823456, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000008, 0x82340056, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000008, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000009, 0xffc11a2b, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000009, 0x8234002b, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x00000009, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000000a, 0xffe08d15, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000000a, 0x82340015, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x0000000a, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000000b, 0xfff0468a, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000000b, 0x8234000a, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x0000000b, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000000c, 0xfff82345, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000000c, 0x82340005, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x0000000c, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000000d, 0xfffc11a2, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000000d, 0x82340002, true, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x0000000d, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000000e, 0xfffe08d1, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000000e, 0x82340001, false, false, false, false, false);
    

    TestSAR<db>(0x82345679, 0x0000000e, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000000f, 0xffff0468, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000000f, 0x82340000, true, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000000f, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000010, 0xffff8234, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000010, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000010, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000011, 0xffffc11a, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000011, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000011, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000012, 0xffffe08d, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000012, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000012, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000013, 0xfffff046, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000013, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000013, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000014, 0xfffff823, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000014, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000014, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000015, 0xfffffc11, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000015, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000015, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000016, 0xfffffe08, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000016, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000016, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000017, 0xffffff04, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000017, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000017, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000018, 0xffffff82, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000018, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000018, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x00000019, 0xffffffc1, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x00000019, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x00000019, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000001a, 0xffffffe0, true, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000001a, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000001a, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000001b, 0xfffffff0, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000001b, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000001b, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000001c, 0xfffffff8, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000001c, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000001c, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000001d, 0xfffffffc, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000001d, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000001d, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000001e, 0xfffffffe, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000001e, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000001e, 0x82345600, false, false, false, true, false);
    

    TestSAR<dd>(0x82345679, 0x0000001f, 0xffffffff, false, false, true, false, false);
    

    TestSAR<dw>(0x82345679, 0x0000001f, 0x82340000, false, false, false, true, false);
    

    TestSAR<db>(0x82345679, 0x0000001f, 0x82345600, false, false, false, true, false);
    
  }

  TEST_F(EmulatedInstructionsTest, ROL) {

    TestROL<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000001, 0x2468acf0, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000001, 0x1234acf0, false, true, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000001, 0x123456f0, false, true, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000002, 0x48d159e0, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000002, 0x123459e1, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000002, 0x123456e1, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000003, 0x91a2b3c0, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000003, 0x1234b3c2, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000003, 0x123456c3, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000004, 0x23456781, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000004, 0x12346785, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000004, 0x12345687, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000005, 0x468acf02, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000005, 0x1234cf0a, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000005, 0x1234560f, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000006, 0x8d159e04, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000006, 0x12349e15, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000006, 0x1234561e, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000007, 0x1a2b3c09, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000007, 0x12343c2b, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000007, 0x1234563c, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000008, 0x34567812, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000008, 0x12347856, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000008, 0x12345678, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000009, 0x68acf024, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000009, 0x1234f0ac, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000009, 0x123456f0, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000000a, 0xd159e048, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000000a, 0x1234e159, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000000a, 0x123456e1, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000000b, 0xa2b3c091, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000000b, 0x1234c2b3, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000000b, 0x123456c3, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000000c, 0x45678123, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000000c, 0x12348567, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000000c, 0x12345687, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000000d, 0x8acf0246, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000000d, 0x12340acf, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000000d, 0x1234560f, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000000e, 0x159e048d, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000000e, 0x1234159e, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000000e, 0x1234561e, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000000f, 0x2b3c091a, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000000f, 0x12342b3c, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000000f, 0x1234563c, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000010, 0x56781234, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000010, 0x12345678, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000010, 0x12345678, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000011, 0xacf02468, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000011, 0x1234acf0, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000011, 0x123456f0, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000012, 0x59e048d1, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000012, 0x123459e1, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000012, 0x123456e1, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000013, 0xb3c091a2, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000013, 0x1234b3c2, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000013, 0x123456c3, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000014, 0x67812345, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000014, 0x12346785, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000014, 0x12345687, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000015, 0xcf02468a, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000015, 0x1234cf0a, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000015, 0x1234560f, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000016, 0x9e048d15, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000016, 0x12349e15, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000016, 0x1234561e, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000017, 0x3c091a2b, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000017, 0x12343c2b, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000017, 0x1234563c, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000018, 0x78123456, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000018, 0x12347856, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000018, 0x12345678, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x00000019, 0xf02468ac, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x00000019, 0x1234f0ac, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x00000019, 0x123456f0, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000001a, 0xe048d159, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000001a, 0x1234e159, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000001a, 0x123456e1, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000001b, 0xc091a2b3, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000001b, 0x1234c2b3, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000001b, 0x123456c3, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000001c, 0x81234567, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000001c, 0x12348567, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000001c, 0x12345687, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000001d, 0x02468acf, true, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000001d, 0x12340acf, true, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000001d, 0x1234560f, true, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000001e, 0x048d159e, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000001e, 0x1234159e, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000001e, 0x1234561e, false, false, false, false, false);
    

    TestROL<dd>(0x12345678, 0x0000001f, 0x091a2b3c, false, false, false, false, false);
    

    TestROL<dw>(0x12345678, 0x0000001f, 0x12342b3c, false, false, false, false, false);
    

    TestROL<db>(0x12345678, 0x0000001f, 0x1234563c, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000001, 0x0468acf3, true, true, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000001, 0x8234acf2, false, true, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000001, 0x823456f2, false, true, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000002, 0x08d159e6, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000002, 0x823459e5, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000002, 0x823456e5, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000003, 0x11a2b3cc, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000003, 0x8234b3ca, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000003, 0x823456cb, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000004, 0x23456798, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000004, 0x82346795, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000004, 0x82345697, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000005, 0x468acf30, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000005, 0x8234cf2a, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000005, 0x8234562f, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000006, 0x8d159e60, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000006, 0x82349e55, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000006, 0x8234565e, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000007, 0x1a2b3cc1, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000007, 0x82343cab, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000007, 0x823456bc, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000008, 0x34567982, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000008, 0x82347956, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000008, 0x82345679, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000009, 0x68acf304, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000009, 0x8234f2ac, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000009, 0x823456f2, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000000a, 0xd159e608, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000000a, 0x8234e559, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000000a, 0x823456e5, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000000b, 0xa2b3cc11, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000000b, 0x8234cab3, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000000b, 0x823456cb, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000000c, 0x45679823, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000000c, 0x82349567, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000000c, 0x82345697, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000000d, 0x8acf3046, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000000d, 0x82342acf, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000000d, 0x8234562f, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000000e, 0x159e608d, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000000e, 0x8234559e, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000000e, 0x8234565e, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000000f, 0x2b3cc11a, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000000f, 0x8234ab3c, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000000f, 0x823456bc, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000010, 0x56798234, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000010, 0x82345679, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000010, 0x82345679, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000011, 0xacf30468, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000011, 0x8234acf2, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000011, 0x823456f2, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000012, 0x59e608d1, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000012, 0x823459e5, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000012, 0x823456e5, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000013, 0xb3cc11a2, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000013, 0x8234b3ca, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000013, 0x823456cb, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000014, 0x67982345, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000014, 0x82346795, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000014, 0x82345697, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000015, 0xcf30468a, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000015, 0x8234cf2a, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000015, 0x8234562f, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000016, 0x9e608d15, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000016, 0x82349e55, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000016, 0x8234565e, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000017, 0x3cc11a2b, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000017, 0x82343cab, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000017, 0x823456bc, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000018, 0x79823456, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000018, 0x82347956, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000018, 0x82345679, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x00000019, 0xf30468ac, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x00000019, 0x8234f2ac, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x00000019, 0x823456f2, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000001a, 0xe608d159, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000001a, 0x8234e559, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000001a, 0x823456e5, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000001b, 0xcc11a2b3, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000001b, 0x8234cab3, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000001b, 0x823456cb, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000001c, 0x98234567, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000001c, 0x82349567, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000001c, 0x82345697, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000001d, 0x30468acf, true, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000001d, 0x82342acf, true, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000001d, 0x8234562f, true, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000001e, 0x608d159e, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000001e, 0x8234559e, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000001e, 0x8234565e, false, false, false, false, false);
    

    TestROL<dd>(0x82345679, 0x0000001f, 0xc11a2b3c, false, false, false, false, false);
    

    TestROL<dw>(0x82345679, 0x0000001f, 0x8234ab3c, false, false, false, false, false);
    

    TestROL<db>(0x82345679, 0x0000001f, 0x823456bc, false, false, false, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, ROR) {

    TestROR<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000001, 0x091a2b3c, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000001, 0x12342b3c, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000001, 0x1234563c, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000002, 0x048d159e, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000002, 0x1234159e, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000002, 0x1234561e, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000003, 0x02468acf, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000003, 0x12340acf, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000003, 0x1234560f, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000004, 0x81234567, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000004, 0x12348567, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000004, 0x12345687, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000005, 0xc091a2b3, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000005, 0x1234c2b3, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000005, 0x123456c3, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000006, 0xe048d159, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000006, 0x1234e159, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000006, 0x123456e1, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000007, 0xf02468ac, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000007, 0x1234f0ac, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000007, 0x123456f0, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000008, 0x78123456, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000008, 0x12347856, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000008, 0x12345678, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000009, 0x3c091a2b, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000009, 0x12343c2b, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000009, 0x1234563c, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000000a, 0x9e048d15, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000000a, 0x12349e15, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000000a, 0x1234561e, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000000b, 0xcf02468a, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000000b, 0x1234cf0a, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000000b, 0x1234560f, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000000c, 0x67812345, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000000c, 0x12346785, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000000c, 0x12345687, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000000d, 0xb3c091a2, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000000d, 0x1234b3c2, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000000d, 0x123456c3, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000000e, 0x59e048d1, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000000e, 0x123459e1, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000000e, 0x123456e1, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000000f, 0xacf02468, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000000f, 0x1234acf0, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000000f, 0x123456f0, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000010, 0x56781234, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000010, 0x12345678, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000010, 0x12345678, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000011, 0x2b3c091a, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000011, 0x12342b3c, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000011, 0x1234563c, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000012, 0x159e048d, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000012, 0x1234159e, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000012, 0x1234561e, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000013, 0x8acf0246, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000013, 0x12340acf, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000013, 0x1234560f, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000014, 0x45678123, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000014, 0x12348567, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000014, 0x12345687, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000015, 0xa2b3c091, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000015, 0x1234c2b3, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000015, 0x123456c3, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000016, 0xd159e048, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000016, 0x1234e159, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000016, 0x123456e1, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000017, 0x68acf024, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000017, 0x1234f0ac, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000017, 0x123456f0, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000018, 0x34567812, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000018, 0x12347856, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000018, 0x12345678, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x00000019, 0x1a2b3c09, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x00000019, 0x12343c2b, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x00000019, 0x1234563c, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000001a, 0x8d159e04, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000001a, 0x12349e15, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000001a, 0x1234561e, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000001b, 0x468acf02, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000001b, 0x1234cf0a, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000001b, 0x1234560f, false, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000001c, 0x23456781, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000001c, 0x12346785, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000001c, 0x12345687, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000001d, 0x91a2b3c0, true, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000001d, 0x1234b3c2, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000001d, 0x123456c3, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000001e, 0x48d159e0, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000001e, 0x123459e1, false, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000001e, 0x123456e1, true, false, false, false, false);
    

    TestROR<dd>(0x12345678, 0x0000001f, 0x2468acf0, false, false, false, false, false);
    

    TestROR<dw>(0x12345678, 0x0000001f, 0x1234acf0, true, false, false, false, false);
    

    TestROR<db>(0x12345678, 0x0000001f, 0x123456f0, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000001, 0xc11a2b3c, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000001, 0x8234ab3c, true, true, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000001, 0x823456bc, true, true, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000002, 0x608d159e, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000002, 0x8234559e, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000002, 0x8234565e, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000003, 0x30468acf, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000003, 0x82342acf, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000003, 0x8234562f, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000004, 0x98234567, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000004, 0x82349567, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000004, 0x82345697, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000005, 0xcc11a2b3, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000005, 0x8234cab3, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000005, 0x823456cb, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000006, 0xe608d159, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000006, 0x8234e559, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000006, 0x823456e5, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000007, 0xf30468ac, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000007, 0x8234f2ac, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000007, 0x823456f2, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000008, 0x79823456, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000008, 0x82347956, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000008, 0x82345679, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000009, 0x3cc11a2b, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000009, 0x82343cab, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000009, 0x823456bc, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000000a, 0x9e608d15, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000000a, 0x82349e55, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000000a, 0x8234565e, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000000b, 0xcf30468a, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000000b, 0x8234cf2a, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000000b, 0x8234562f, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000000c, 0x67982345, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000000c, 0x82346795, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000000c, 0x82345697, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000000d, 0xb3cc11a2, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000000d, 0x8234b3ca, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000000d, 0x823456cb, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000000e, 0x59e608d1, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000000e, 0x823459e5, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000000e, 0x823456e5, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000000f, 0xacf30468, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000000f, 0x8234acf2, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000000f, 0x823456f2, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000010, 0x56798234, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000010, 0x82345679, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000010, 0x82345679, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000011, 0x2b3cc11a, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000011, 0x8234ab3c, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000011, 0x823456bc, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000012, 0x159e608d, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000012, 0x8234559e, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000012, 0x8234565e, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000013, 0x8acf3046, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000013, 0x82342acf, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000013, 0x8234562f, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000014, 0x45679823, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000014, 0x82349567, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000014, 0x82345697, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000015, 0xa2b3cc11, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000015, 0x8234cab3, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000015, 0x823456cb, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000016, 0xd159e608, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000016, 0x8234e559, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000016, 0x823456e5, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000017, 0x68acf304, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000017, 0x8234f2ac, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000017, 0x823456f2, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000018, 0x34567982, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000018, 0x82347956, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000018, 0x82345679, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x00000019, 0x1a2b3cc1, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x00000019, 0x82343cab, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x00000019, 0x823456bc, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000001a, 0x8d159e60, true, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000001a, 0x82349e55, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000001a, 0x8234565e, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000001b, 0x468acf30, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000001b, 0x8234cf2a, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000001b, 0x8234562f, false, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000001c, 0x23456798, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000001c, 0x82346795, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000001c, 0x82345697, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000001d, 0x11a2b3cc, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000001d, 0x8234b3ca, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000001d, 0x823456cb, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000001e, 0x08d159e6, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000001e, 0x823459e5, false, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000001e, 0x823456e5, true, false, false, false, false);
    

    TestROR<dd>(0x82345679, 0x0000001f, 0x0468acf3, false, false, false, false, false);
    

    TestROR<dw>(0x82345679, 0x0000001f, 0x8234acf2, true, false, false, false, false);
    

    TestROR<db>(0x82345679, 0x0000001f, 0x823456f2, true, false, false, false, false);
    
  }

  TEST_F(EmulatedInstructionsTest, RCR) {

    TestRCR<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000000, 0x12345678, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000000, 0x12345678, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000000, 0x12345678, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000001, 0x091a2b3c, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000001, 0x12342b3c, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000001, 0x1234563c, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000001, 0x891a2b3c, false, true, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000001, 0x1234ab3c, false, true, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000001, 0x123456bc, false, true, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000002, 0x048d159e, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000002, 0x1234159e, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000002, 0x1234561e, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000002, 0x448d159e, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000002, 0x1234559e, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000002, 0x1234565e, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000003, 0x02468acf, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000003, 0x12340acf, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000003, 0x1234560f, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000003, 0x22468acf, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000003, 0x12342acf, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000003, 0x1234562f, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000004, 0x01234567, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000004, 0x12340567, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000004, 0x12345607, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000004, 0x11234567, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000004, 0x12341567, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000004, 0x12345617, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000005, 0x8091a2b3, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000005, 0x123482b3, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000005, 0x12345683, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000005, 0x8891a2b3, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000005, 0x12348ab3, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000005, 0x1234568b, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000006, 0xc048d159, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000006, 0x1234c159, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000006, 0x123456c1, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000006, 0xc448d159, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000006, 0x1234c559, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000006, 0x123456c5, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000007, 0xe02468ac, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000007, 0x1234e0ac, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000007, 0x123456e0, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000007, 0xe22468ac, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000007, 0x1234e2ac, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000007, 0x123456e2, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000008, 0xf0123456, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000008, 0x1234f056, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000008, 0x123456f0, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000008, 0xf1123456, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000008, 0x1234f156, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000008, 0x123456f1, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000009, 0x78091a2b, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000009, 0x1234782b, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000009, 0x12345678, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000009, 0x78891a2b, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000009, 0x123478ab, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000009, 0x12345678, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000000a, 0x3c048d15, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000000a, 0x12343c15, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000000a, 0x1234563c, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000000a, 0x3c448d15, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000000a, 0x12343c55, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000000a, 0x123456bc, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000000b, 0x9e02468a, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000000b, 0x12349e0a, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000000b, 0x1234561e, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000000b, 0x9e22468a, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000000b, 0x12349e2a, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000000b, 0x1234565e, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000000c, 0xcf012345, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000000c, 0x1234cf05, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000000c, 0x1234560f, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000000c, 0xcf112345, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000000c, 0x1234cf15, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000000c, 0x1234562f, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000000d, 0x678091a2, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000000d, 0x12346782, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000000d, 0x12345607, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000000d, 0x678891a2, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000000d, 0x1234678a, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000000d, 0x12345617, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000000e, 0xb3c048d1, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000000e, 0x1234b3c1, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000000e, 0x12345683, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000000e, 0xb3c448d1, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000000e, 0x1234b3c5, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000000e, 0x1234568b, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000000f, 0x59e02468, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000000f, 0x123459e0, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000000f, 0x123456c1, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000000f, 0x59e22468, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000000f, 0x123459e2, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000000f, 0x123456c5, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000010, 0xacf01234, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000010, 0x1234acf0, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000010, 0x123456e0, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000010, 0xacf11234, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000010, 0x1234acf1, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000010, 0x123456e2, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000011, 0x5678091a, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000011, 0x12345678, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000011, 0x123456f0, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000011, 0x5678891a, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000011, 0x12345678, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000011, 0x123456f1, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000012, 0x2b3c048d, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000012, 0x12342b3c, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000012, 0x12345678, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000012, 0x2b3c448d, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000012, 0x1234ab3c, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000012, 0x12345678, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000013, 0x159e0246, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000013, 0x1234159e, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000013, 0x1234563c, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000013, 0x159e2246, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000013, 0x1234559e, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000013, 0x123456bc, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000014, 0x8acf0123, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000014, 0x12340acf, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000014, 0x1234561e, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000014, 0x8acf1123, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000014, 0x12342acf, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000014, 0x1234565e, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000015, 0x45678091, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000015, 0x12340567, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000015, 0x1234560f, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000015, 0x45678891, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000015, 0x12341567, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000015, 0x1234562f, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000016, 0xa2b3c048, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000016, 0x123482b3, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000016, 0x12345607, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000016, 0xa2b3c448, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000016, 0x12348ab3, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000016, 0x12345617, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000017, 0xd159e024, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000017, 0x1234c159, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000017, 0x12345683, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000017, 0xd159e224, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000017, 0x1234c559, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000017, 0x1234568b, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000018, 0x68acf012, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000018, 0x1234e0ac, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000018, 0x123456c1, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000018, 0x68acf112, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000018, 0x1234e2ac, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000018, 0x123456c5, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x00000019, 0x34567809, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x00000019, 0x1234f056, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x00000019, 0x123456e0, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x00000019, 0x34567889, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x00000019, 0x1234f156, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x00000019, 0x123456e2, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000001a, 0x1a2b3c04, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000001a, 0x1234782b, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000001a, 0x123456f0, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000001a, 0x1a2b3c44, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000001a, 0x123478ab, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000001a, 0x123456f1, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000001b, 0x8d159e02, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000001b, 0x12343c15, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000001b, 0x12345678, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000001b, 0x8d159e22, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000001b, 0x12343c55, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000001b, 0x12345678, true, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000001c, 0x468acf01, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000001c, 0x12349e0a, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000001c, 0x1234563c, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000001c, 0x468acf11, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000001c, 0x12349e2a, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000001c, 0x123456bc, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000001d, 0x23456780, true, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000001d, 0x1234cf05, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000001d, 0x1234561e, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000001d, 0x23456788, true, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000001d, 0x1234cf15, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000001d, 0x1234565e, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000001e, 0x91a2b3c0, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000001e, 0x12346782, true, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000001e, 0x1234560f, false, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000001e, 0x91a2b3c4, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000001e, 0x1234678a, true, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000001e, 0x1234562f, false, false, false, false, true);
    

    TestRCR<dd>(0x12345678, 0x0000001f, 0x48d159e0, false, false, false, false, false);
    

    TestRCR<dw>(0x12345678, 0x0000001f, 0x1234b3c1, false, false, false, false, false);
    

    TestRCR<db>(0x12345678, 0x0000001f, 0x12345607, true, false, false, false, false);
    

    TestRCR<dd>(0x12345678, 0x0000001f, 0x48d159e2, false, false, false, false, true);
    

    TestRCR<dw>(0x12345678, 0x0000001f, 0x1234b3c5, false, false, false, false, true);
    

    TestRCR<db>(0x12345678, 0x0000001f, 0x12345617, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000000, 0x82345679, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000000, 0x82345679, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000000, 0x82345679, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000001, 0x411a2b3c, true, true, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000001, 0x82342b3c, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000001, 0x8234563c, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000001, 0xc11a2b3c, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000001, 0x8234ab3c, true, true, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000001, 0x823456bc, true, true, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000002, 0xa08d159e, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000002, 0x8234959e, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000002, 0x8234569e, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000002, 0xe08d159e, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000002, 0x8234d59e, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000002, 0x823456de, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000003, 0x50468acf, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000003, 0x82344acf, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000003, 0x8234564f, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000003, 0x70468acf, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000003, 0x82346acf, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000003, 0x8234566f, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000004, 0x28234567, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000004, 0x82342567, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000004, 0x82345627, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000004, 0x38234567, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000004, 0x82343567, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000004, 0x82345637, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000005, 0x9411a2b3, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000005, 0x823492b3, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000005, 0x82345693, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000005, 0x9c11a2b3, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000005, 0x82349ab3, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000005, 0x8234569b, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000006, 0xca08d159, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000006, 0x8234c959, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000006, 0x823456c9, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000006, 0xce08d159, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000006, 0x8234cd59, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000006, 0x823456cd, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000007, 0xe50468ac, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000007, 0x8234e4ac, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000007, 0x823456e4, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000007, 0xe70468ac, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000007, 0x8234e6ac, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000007, 0x823456e6, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000008, 0xf2823456, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000008, 0x8234f256, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000008, 0x823456f2, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000008, 0xf3823456, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000008, 0x8234f356, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000008, 0x823456f3, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000009, 0x79411a2b, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000009, 0x8234792b, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000009, 0x82345679, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000009, 0x79c11a2b, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000009, 0x823479ab, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000009, 0x82345679, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000000a, 0x3ca08d15, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000000a, 0x82343c95, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000000a, 0x8234563c, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000000a, 0x3ce08d15, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000000a, 0x82343cd5, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000000a, 0x823456bc, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000000b, 0x9e50468a, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000000b, 0x82349e4a, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000000b, 0x8234569e, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000000b, 0x9e70468a, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000000b, 0x82349e6a, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000000b, 0x823456de, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000000c, 0xcf282345, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000000c, 0x8234cf25, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000000c, 0x8234564f, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000000c, 0xcf382345, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000000c, 0x8234cf35, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000000c, 0x8234566f, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000000d, 0x679411a2, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000000d, 0x82346792, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000000d, 0x82345627, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000000d, 0x679c11a2, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000000d, 0x8234679a, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000000d, 0x82345637, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000000e, 0xb3ca08d1, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000000e, 0x8234b3c9, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000000e, 0x82345693, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000000e, 0xb3ce08d1, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000000e, 0x8234b3cd, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000000e, 0x8234569b, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000000f, 0x59e50468, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000000f, 0x823459e4, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000000f, 0x823456c9, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000000f, 0x59e70468, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000000f, 0x823459e6, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000000f, 0x823456cd, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000010, 0xacf28234, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000010, 0x8234acf2, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000010, 0x823456e4, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000010, 0xacf38234, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000010, 0x8234acf3, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000010, 0x823456e6, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000011, 0x5679411a, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000011, 0x82345679, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000011, 0x823456f2, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000011, 0x5679c11a, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000011, 0x82345679, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000011, 0x823456f3, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000012, 0x2b3ca08d, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000012, 0x82342b3c, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000012, 0x82345679, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000012, 0x2b3ce08d, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000012, 0x8234ab3c, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000012, 0x82345679, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000013, 0x159e5046, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000013, 0x8234959e, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000013, 0x8234563c, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000013, 0x159e7046, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000013, 0x8234d59e, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000013, 0x823456bc, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000014, 0x8acf2823, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000014, 0x82344acf, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000014, 0x8234569e, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000014, 0x8acf3823, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000014, 0x82346acf, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000014, 0x823456de, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000015, 0x45679411, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000015, 0x82342567, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000015, 0x8234564f, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000015, 0x45679c11, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000015, 0x82343567, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000015, 0x8234566f, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000016, 0xa2b3ca08, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000016, 0x823492b3, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000016, 0x82345627, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000016, 0xa2b3ce08, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000016, 0x82349ab3, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000016, 0x82345637, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000017, 0xd159e504, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000017, 0x8234c959, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000017, 0x82345693, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000017, 0xd159e704, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000017, 0x8234cd59, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000017, 0x8234569b, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000018, 0x68acf282, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000018, 0x8234e4ac, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000018, 0x823456c9, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000018, 0x68acf382, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000018, 0x8234e6ac, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000018, 0x823456cd, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x00000019, 0x34567941, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x00000019, 0x8234f256, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x00000019, 0x823456e4, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x00000019, 0x345679c1, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x00000019, 0x8234f356, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x00000019, 0x823456e6, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000001a, 0x1a2b3ca0, true, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000001a, 0x8234792b, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000001a, 0x823456f2, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000001a, 0x1a2b3ce0, true, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000001a, 0x823479ab, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000001a, 0x823456f3, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000001b, 0x8d159e50, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000001b, 0x82343c95, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000001b, 0x82345679, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000001b, 0x8d159e70, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000001b, 0x82343cd5, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000001b, 0x82345679, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000001c, 0x468acf28, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000001c, 0x82349e4a, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000001c, 0x8234563c, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000001c, 0x468acf38, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000001c, 0x82349e6a, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000001c, 0x823456bc, true, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000001d, 0x23456794, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000001d, 0x8234cf25, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000001d, 0x8234569e, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000001d, 0x2345679c, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000001d, 0x8234cf35, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000001d, 0x823456de, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000001e, 0x11a2b3ca, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000001e, 0x82346792, true, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000001e, 0x8234564f, false, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000001e, 0x11a2b3ce, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000001e, 0x8234679a, true, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000001e, 0x8234566f, false, false, false, false, true);
    

    TestRCR<dd>(0x82345679, 0x0000001f, 0x08d159e5, false, false, false, false, false);
    

    TestRCR<dw>(0x82345679, 0x0000001f, 0x8234b3c9, false, false, false, false, false);
    

    TestRCR<db>(0x82345679, 0x0000001f, 0x82345627, true, false, false, false, false);
    

    TestRCR<dd>(0x82345679, 0x0000001f, 0x08d159e7, false, false, false, false, true);
    

    TestRCR<dw>(0x82345679, 0x0000001f, 0x8234b3cd, false, false, false, false, true);
    

    TestRCR<db>(0x82345679, 0x0000001f, 0x82345637, true, false, false, false, true);
    
  }

  TEST_F(EmulatedInstructionsTest, RCL) {

    TestRCL<dd>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000000, 0x12345678, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000000, 0x12345678, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000000, 0x12345678, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000000, 0x12345678, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000001, 0x2468acf0, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000001, 0x1234acf0, false, true, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000001, 0x123456f0, false, true, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000001, 0x2468acf1, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000001, 0x1234acf1, false, true, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000001, 0x123456f1, false, true, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000002, 0x48d159e0, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000002, 0x123459e0, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000002, 0x123456e0, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000002, 0x48d159e2, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000002, 0x123459e2, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000002, 0x123456e2, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000003, 0x91a2b3c0, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000003, 0x1234b3c1, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000003, 0x123456c1, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000003, 0x91a2b3c4, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000003, 0x1234b3c5, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000003, 0x123456c5, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000004, 0x23456780, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000004, 0x12346782, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000004, 0x12345683, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000004, 0x23456788, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000004, 0x1234678a, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000004, 0x1234568b, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000005, 0x468acf01, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000005, 0x1234cf05, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000005, 0x12345607, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000005, 0x468acf11, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000005, 0x1234cf15, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000005, 0x12345617, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000006, 0x8d159e02, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000006, 0x12349e0a, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000006, 0x1234560f, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000006, 0x8d159e22, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000006, 0x12349e2a, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000006, 0x1234562f, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000007, 0x1a2b3c04, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000007, 0x12343c15, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000007, 0x1234561e, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000007, 0x1a2b3c44, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000007, 0x12343c55, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000007, 0x1234565e, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000008, 0x34567809, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000008, 0x1234782b, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000008, 0x1234563c, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000008, 0x34567889, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000008, 0x123478ab, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000008, 0x123456bc, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000009, 0x68acf012, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000009, 0x1234f056, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000009, 0x12345678, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000009, 0x68acf112, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000009, 0x1234f156, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000009, 0x12345678, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000000a, 0xd159e024, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000000a, 0x1234e0ac, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000000a, 0x123456f0, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000000a, 0xd159e224, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000000a, 0x1234e2ac, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000000a, 0x123456f1, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000000b, 0xa2b3c048, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000000b, 0x1234c159, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000000b, 0x123456e0, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000000b, 0xa2b3c448, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000000b, 0x1234c559, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000000b, 0x123456e2, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000000c, 0x45678091, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000000c, 0x123482b3, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000000c, 0x123456c1, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000000c, 0x45678891, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000000c, 0x12348ab3, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000000c, 0x123456c5, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000000d, 0x8acf0123, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000000d, 0x12340567, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000000d, 0x12345683, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000000d, 0x8acf1123, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000000d, 0x12341567, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000000d, 0x1234568b, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000000e, 0x159e0246, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000000e, 0x12340acf, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000000e, 0x12345607, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000000e, 0x159e2246, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000000e, 0x12342acf, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000000e, 0x12345617, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000000f, 0x2b3c048d, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000000f, 0x1234159e, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000000f, 0x1234560f, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000000f, 0x2b3c448d, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000000f, 0x1234559e, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000000f, 0x1234562f, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000010, 0x5678091a, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000010, 0x12342b3c, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000010, 0x1234561e, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000010, 0x5678891a, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000010, 0x1234ab3c, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000010, 0x1234565e, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000011, 0xacf01234, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000011, 0x12345678, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000011, 0x1234563c, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000011, 0xacf11234, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000011, 0x12345678, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000011, 0x123456bc, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000012, 0x59e02468, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000012, 0x1234acf0, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000012, 0x12345678, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000012, 0x59e22468, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000012, 0x1234acf1, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000012, 0x12345678, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000013, 0xb3c048d1, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000013, 0x123459e0, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000013, 0x123456f0, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000013, 0xb3c448d1, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000013, 0x123459e2, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000013, 0x123456f1, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000014, 0x678091a2, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000014, 0x1234b3c1, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000014, 0x123456e0, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000014, 0x678891a2, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000014, 0x1234b3c5, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000014, 0x123456e2, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000015, 0xcf012345, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000015, 0x12346782, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000015, 0x123456c1, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000015, 0xcf112345, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000015, 0x1234678a, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000015, 0x123456c5, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000016, 0x9e02468a, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000016, 0x1234cf05, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000016, 0x12345683, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000016, 0x9e22468a, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000016, 0x1234cf15, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000016, 0x1234568b, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000017, 0x3c048d15, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000017, 0x12349e0a, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000017, 0x12345607, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000017, 0x3c448d15, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000017, 0x12349e2a, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000017, 0x12345617, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000018, 0x78091a2b, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000018, 0x12343c15, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000018, 0x1234560f, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000018, 0x78891a2b, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000018, 0x12343c55, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000018, 0x1234562f, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x00000019, 0xf0123456, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x00000019, 0x1234782b, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x00000019, 0x1234561e, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x00000019, 0xf1123456, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x00000019, 0x123478ab, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x00000019, 0x1234565e, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000001a, 0xe02468ac, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000001a, 0x1234f056, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000001a, 0x1234563c, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000001a, 0xe22468ac, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000001a, 0x1234f156, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000001a, 0x123456bc, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000001b, 0xc048d159, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000001b, 0x1234e0ac, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000001b, 0x12345678, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000001b, 0xc448d159, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000001b, 0x1234e2ac, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000001b, 0x12345678, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000001c, 0x8091a2b3, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000001c, 0x1234c159, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000001c, 0x123456f0, false, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000001c, 0x8891a2b3, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000001c, 0x1234c559, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000001c, 0x123456f1, false, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000001d, 0x01234567, true, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000001d, 0x123482b3, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000001d, 0x123456e0, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000001d, 0x11234567, true, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000001d, 0x12348ab3, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000001d, 0x123456e2, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000001e, 0x02468acf, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000001e, 0x12340567, true, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000001e, 0x123456c1, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000001e, 0x22468acf, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000001e, 0x12341567, true, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000001e, 0x123456c5, true, false, false, false, true);
    

    TestRCL<dd>(0x12345678, 0x0000001f, 0x048d159e, false, false, false, false, false);
    

    TestRCL<dw>(0x12345678, 0x0000001f, 0x12340acf, false, false, false, false, false);
    

    TestRCL<db>(0x12345678, 0x0000001f, 0x12345683, true, false, false, false, false);
    

    TestRCL<dd>(0x12345678, 0x0000001f, 0x448d159e, false, false, false, false, true);
    

    TestRCL<dw>(0x12345678, 0x0000001f, 0x12342acf, false, false, false, false, true);
    

    TestRCL<db>(0x12345678, 0x0000001f, 0x1234568b, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000000, 0x82345679, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000000, 0x82345679, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000000, 0x82345679, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000000, 0x82345679, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000001, 0x0468acf2, true, true, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000001, 0x8234acf2, false, true, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000001, 0x823456f2, false, true, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000001, 0x0468acf3, true, true, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000001, 0x8234acf3, false, true, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000001, 0x823456f3, false, true, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000002, 0x08d159e5, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000002, 0x823459e4, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000002, 0x823456e4, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000002, 0x08d159e7, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000002, 0x823459e6, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000002, 0x823456e6, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000003, 0x11a2b3ca, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000003, 0x8234b3c9, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000003, 0x823456c9, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000003, 0x11a2b3ce, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000003, 0x8234b3cd, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000003, 0x823456cd, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000004, 0x23456794, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000004, 0x82346792, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000004, 0x82345693, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000004, 0x2345679c, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000004, 0x8234679a, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000004, 0x8234569b, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000005, 0x468acf28, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000005, 0x8234cf25, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000005, 0x82345627, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000005, 0x468acf38, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000005, 0x8234cf35, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000005, 0x82345637, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000006, 0x8d159e50, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000006, 0x82349e4a, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000006, 0x8234564f, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000006, 0x8d159e70, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000006, 0x82349e6a, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000006, 0x8234566f, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000007, 0x1a2b3ca0, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000007, 0x82343c95, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000007, 0x8234569e, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000007, 0x1a2b3ce0, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000007, 0x82343cd5, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000007, 0x823456de, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000008, 0x34567941, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000008, 0x8234792b, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000008, 0x8234563c, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000008, 0x345679c1, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000008, 0x823479ab, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000008, 0x823456bc, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000009, 0x68acf282, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000009, 0x8234f256, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000009, 0x82345679, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000009, 0x68acf382, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000009, 0x8234f356, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000009, 0x82345679, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000000a, 0xd159e504, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000000a, 0x8234e4ac, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000000a, 0x823456f2, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000000a, 0xd159e704, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000000a, 0x8234e6ac, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000000a, 0x823456f3, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000000b, 0xa2b3ca08, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000000b, 0x8234c959, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000000b, 0x823456e4, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000000b, 0xa2b3ce08, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000000b, 0x8234cd59, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000000b, 0x823456e6, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000000c, 0x45679411, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000000c, 0x823492b3, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000000c, 0x823456c9, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000000c, 0x45679c11, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000000c, 0x82349ab3, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000000c, 0x823456cd, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000000d, 0x8acf2823, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000000d, 0x82342567, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000000d, 0x82345693, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000000d, 0x8acf3823, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000000d, 0x82343567, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000000d, 0x8234569b, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000000e, 0x159e5046, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000000e, 0x82344acf, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000000e, 0x82345627, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000000e, 0x159e7046, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000000e, 0x82346acf, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000000e, 0x82345637, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000000f, 0x2b3ca08d, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000000f, 0x8234959e, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000000f, 0x8234564f, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000000f, 0x2b3ce08d, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000000f, 0x8234d59e, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000000f, 0x8234566f, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000010, 0x5679411a, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000010, 0x82342b3c, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000010, 0x8234569e, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000010, 0x5679c11a, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000010, 0x8234ab3c, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000010, 0x823456de, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000011, 0xacf28234, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000011, 0x82345679, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000011, 0x8234563c, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000011, 0xacf38234, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000011, 0x82345679, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000011, 0x823456bc, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000012, 0x59e50468, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000012, 0x8234acf2, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000012, 0x82345679, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000012, 0x59e70468, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000012, 0x8234acf3, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000012, 0x82345679, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000013, 0xb3ca08d1, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000013, 0x823459e4, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000013, 0x823456f2, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000013, 0xb3ce08d1, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000013, 0x823459e6, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000013, 0x823456f3, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000014, 0x679411a2, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000014, 0x8234b3c9, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000014, 0x823456e4, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000014, 0x679c11a2, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000014, 0x8234b3cd, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000014, 0x823456e6, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000015, 0xcf282345, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000015, 0x82346792, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000015, 0x823456c9, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000015, 0xcf382345, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000015, 0x8234679a, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000015, 0x823456cd, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000016, 0x9e50468a, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000016, 0x8234cf25, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000016, 0x82345693, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000016, 0x9e70468a, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000016, 0x8234cf35, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000016, 0x8234569b, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000017, 0x3ca08d15, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000017, 0x82349e4a, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000017, 0x82345627, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000017, 0x3ce08d15, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000017, 0x82349e6a, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000017, 0x82345637, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000018, 0x79411a2b, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000018, 0x82343c95, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000018, 0x8234564f, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000018, 0x79c11a2b, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000018, 0x82343cd5, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000018, 0x8234566f, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x00000019, 0xf2823456, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x00000019, 0x8234792b, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x00000019, 0x8234569e, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x00000019, 0xf3823456, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x00000019, 0x823479ab, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x00000019, 0x823456de, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000001a, 0xe50468ac, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000001a, 0x8234f256, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000001a, 0x8234563c, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000001a, 0xe70468ac, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000001a, 0x8234f356, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000001a, 0x823456bc, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000001b, 0xca08d159, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000001b, 0x8234e4ac, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000001b, 0x82345679, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000001b, 0xce08d159, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000001b, 0x8234e6ac, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000001b, 0x82345679, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000001c, 0x9411a2b3, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000001c, 0x8234c959, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000001c, 0x823456f2, false, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000001c, 0x9c11a2b3, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000001c, 0x8234cd59, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000001c, 0x823456f3, false, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000001d, 0x28234567, true, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000001d, 0x823492b3, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000001d, 0x823456e4, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000001d, 0x38234567, true, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000001d, 0x82349ab3, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000001d, 0x823456e6, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000001e, 0x50468acf, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000001e, 0x82342567, true, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000001e, 0x823456c9, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000001e, 0x70468acf, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000001e, 0x82343567, true, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000001e, 0x823456cd, true, false, false, false, true);
    

    TestRCL<dd>(0x82345679, 0x0000001f, 0xa08d159e, false, false, false, false, false);
    

    TestRCL<dw>(0x82345679, 0x0000001f, 0x82344acf, false, false, false, false, false);
    

    TestRCL<db>(0x82345679, 0x0000001f, 0x82345693, true, false, false, false, false);
    

    TestRCL<dd>(0x82345679, 0x0000001f, 0xe08d159e, false, false, false, false, true);
    

    TestRCL<dw>(0x82345679, 0x0000001f, 0x82346acf, false, false, false, false, true);
    

    TestRCL<db>(0x82345679, 0x0000001f, 0x8234569b, true, false, false, false, true);
    
  }

  TEST_F(EmulatedInstructionsTest, SHLD) {

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000000, 0x12345678, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000000, 0x12345678, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000001, 0x2468acf0, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000001, 0x1234acf0, false, true, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000002, 0x48d159e0, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000002, 0x123459e0, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000003, 0x91a2b3c1, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000003, 0x1234b3c1, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000004, 0x23456782, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000004, 0x12346783, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000005, 0x468acf04, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000005, 0x1234cf07, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000006, 0x8d159e08, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000006, 0x12349e0f, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000007, 0x1a2b3c10, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000007, 0x12343c1e, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000008, 0x34567821, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000008, 0x1234783d, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000009, 0x68acf043, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000009, 0x1234f07a, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000000a, 0xd159e086, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000000a, 0x1234e0f4, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000000b, 0xa2b3c10d, true, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000000b, 0x1234c1e9, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000000c, 0x4567821a, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000000c, 0x123483d3, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000000d, 0x8acf0435, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000000d, 0x123407a6, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000000e, 0x159e086b, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000000e, 0x12340f4d, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000000f, 0x2b3c10d6, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000000f, 0x12341e9a, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000010, 0x567821ad, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000010, 0x12343d34, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000011, 0xacf0435a, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000011, 0x12347a68, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000012, 0x59e086b4, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000012, 0x1234f4d1, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000013, 0xb3c10d69, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000013, 0x1234e9a2, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000014, 0x67821ad3, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000014, 0x1234d345, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000015, 0xcf0435a7, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000015, 0x1234a68a, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000016, 0x9e086b4f, true, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000016, 0x12344d15, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000017, 0x3c10d69e, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000017, 0x12349a2b, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000018, 0x7821ad3d, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000018, 0x12343456, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x00000019, 0xf0435a7a, false, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x00000019, 0x123468ac, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000001a, 0xe086b4f4, true, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000001a, 0x1234d159, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000001b, 0xc10d69e9, true, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000001b, 0x1234a2b3, true, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000001c, 0x821ad3d3, true, false, true, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000001c, 0x12344567, true, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000001d, 0x0435a7a6, true, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000001d, 0x12348acf, false, false, true, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000001e, 0x086b4f4d, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000001e, 0x1234159e, false, false, false, false);
    

    TestSHLD<dd>(0x12345678, 0x21ad3d34, 0x0000001f, 0x10d69e9a, false, false, false, false);
    

    TestSHLD<dw>(0x12345678, 0x21ad3d34, 0x0000001f, 0x12342b3c, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000000, 0x82345679, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000000, 0x82345679, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000001, 0x0468acf3, true, true, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000001, 0x8234acf2, false, true, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000002, 0x08d159e6, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000002, 0x823459e4, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000003, 0x11a2b3cc, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000003, 0x8234b3c9, false, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000004, 0x23456798, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000004, 0x82346793, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000005, 0x468acf30, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000005, 0x8234cf26, false, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000006, 0x8d159e60, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000006, 0x82349e4d, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000007, 0x1a2b3cc0, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000007, 0x82343c9a, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000008, 0x34567981, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000008, 0x82347934, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000009, 0x68acf302, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000009, 0x8234f268, false, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000000a, 0xd159e604, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000000a, 0x8234e4d0, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000000b, 0xa2b3cc09, true, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000000b, 0x8234c9a1, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000000c, 0x45679813, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000000c, 0x82349342, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000000d, 0x8acf3027, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000000d, 0x82342684, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000000e, 0x159e604f, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000000e, 0x82344d08, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000000f, 0x2b3cc09f, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000000f, 0x82349a10, false, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000010, 0x5679813f, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000010, 0x82343421, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000011, 0xacf3027e, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000011, 0x82346842, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000012, 0x59e604fc, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000012, 0x8234d085, false, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000013, 0xb3cc09f9, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000013, 0x8234a10a, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000014, 0x679813f3, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000014, 0x82344215, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000015, 0xcf3027e6, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000015, 0x8234842a, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000016, 0x9e604fcd, true, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000016, 0x82340855, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000017, 0x3cc09f9a, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000017, 0x823410ab, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000018, 0x79813f34, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000018, 0x82342156, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x00000019, 0xf3027e68, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x00000019, 0x823442ac, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000001a, 0xe604fcd0, true, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000001a, 0x82348559, true, false, true, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000001b, 0xcc09f9a1, true, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000001b, 0x82340ab3, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000001c, 0x9813f342, true, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000001c, 0x82341567, true, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000001d, 0x3027e684, true, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000001d, 0x82342acf, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000001e, 0x604fcd08, false, false, false, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000001e, 0x8234559e, false, false, false, false);
    

    TestSHLD<dd>(0x82345679, 0x813f3421, 0x0000001f, 0xc09f9a10, false, false, true, false);
    

    TestSHLD<dw>(0x82345679, 0x813f3421, 0x0000001f, 0x8234ab3c, true, false, true, false);
    
  }

  TEST_F(EmulatedInstructionsTest, SHRD) {

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000000, 0x12345678, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000000, 0x12345678, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000001, 0x091a2b3c, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000001, 0x12342b3c, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000002, 0x048d159e, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000002, 0x1234159e, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000003, 0x82468acf, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000003, 0x12348acf, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000004, 0x41234567, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000004, 0x12344567, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000005, 0xa091a2b3, true, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000005, 0x1234a2b3, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000006, 0xd048d159, true, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000006, 0x1234d159, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000007, 0x682468ac, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000007, 0x123468ac, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000008, 0x34123456, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000008, 0x12343456, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000009, 0x9a091a2b, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000009, 0x12349a2b, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000000a, 0x4d048d15, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000000a, 0x12344d15, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000000b, 0xa682468a, true, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000000b, 0x1234a68a, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000000c, 0xd3412345, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000000c, 0x1234d345, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000000d, 0xe9a091a2, true, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000000d, 0x1234e9a2, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000000e, 0xf4d048d1, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000000e, 0x1234f4d1, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000000f, 0x7a682468, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000000f, 0x12347a68, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000010, 0x3d341234, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000010, 0x12343d34, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000011, 0x9e9a091a, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000011, 0x12341e9a, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000012, 0x4f4d048d, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000012, 0x12340f4d, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000013, 0xa7a68246, true, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000013, 0x123407a6, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000014, 0xd3d34123, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000014, 0x123483d3, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000015, 0x69e9a091, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000015, 0x1234c1e9, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000016, 0xb4f4d048, true, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000016, 0x1234e0f4, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000017, 0x5a7a6824, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000017, 0x1234f07a, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000018, 0xad3d3412, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000018, 0x1234783d, false, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x00000019, 0xd69e9a09, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x00000019, 0x12343c1e, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000001a, 0x6b4f4d04, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000001a, 0x12349e0f, true, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000001b, 0x35a7a682, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000001b, 0x1234cf07, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000001c, 0x1ad3d341, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000001c, 0x12346783, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000001d, 0x0d69e9a0, true, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000001d, 0x1234b3c1, false, false, true, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000001e, 0x86b4f4d0, false, false, true, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000001e, 0x123459e0, true, false, false, false);
    

    TestSHRD<dd>(0x12345678, 0x21ad3d34, 0x0000001f, 0x435a7a68, false, false, false, false);
    

    TestSHRD<dw>(0x12345678, 0x21ad3d34, 0x0000001f, 0x1234acf0, false, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000000, 0x82345679, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000000, 0x82345679, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000001, 0xc11a2b3c, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000001, 0x8234ab3c, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000002, 0x608d159e, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000002, 0x8234559e, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000003, 0x30468acf, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000003, 0x82342acf, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000004, 0x18234567, true, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000004, 0x82341567, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000005, 0x0c11a2b3, true, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000005, 0x82340ab3, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000006, 0x8608d159, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000006, 0x82348559, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000007, 0x430468ac, true, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000007, 0x823442ac, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000008, 0x21823456, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000008, 0x82342156, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000009, 0x10c11a2b, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000009, 0x823410ab, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000000a, 0x08608d15, true, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000000a, 0x82340855, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000000b, 0x8430468a, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000000b, 0x8234842a, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000000c, 0x42182345, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000000c, 0x82344215, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000000d, 0xa10c11a2, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000000d, 0x8234a10a, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000000e, 0xd08608d1, false, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000000e, 0x8234d085, false, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000000f, 0x68430468, true, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000000f, 0x82346842, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000010, 0x34218234, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000010, 0x82343421, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000011, 0x9a10c11a, false, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000011, 0x82349a10, false, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000012, 0xcd08608d, false, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000012, 0x82344d08, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000013, 0xe6843046, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000013, 0x82342684, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000014, 0xf3421823, false, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000014, 0x82349342, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000015, 0xf9a10c11, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000015, 0x8234c9a1, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000016, 0xfcd08608, true, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000016, 0x8234e4d0, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000017, 0x7e684304, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000017, 0x8234f268, false, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000018, 0x3f342182, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000018, 0x82347934, false, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x00000019, 0x9f9a10c1, false, false, true, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x00000019, 0x82343c9a, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000001a, 0x4fcd0860, true, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000001a, 0x82349e4d, true, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000001b, 0x27e68430, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000001b, 0x8234cf26, false, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000001c, 0x13f34218, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000001c, 0x82346793, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000001d, 0x09f9a10c, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000001d, 0x8234b3c9, false, false, true, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000001e, 0x04fcd086, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000001e, 0x823459e4, true, false, false, false);
    

    TestSHRD<dd>(0x82345679, 0x813f3421, 0x0000001f, 0x027e6843, false, false, false, false);
    

    TestSHRD<dw>(0x82345679, 0x813f3421, 0x0000001f, 0x8234acf2, false, false, true, false);
    
  }

}  // namespace


int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
