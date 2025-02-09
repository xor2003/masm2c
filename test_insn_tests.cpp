#include <gtest/gtest.h>
#include "asm.h"

using namespace m2c;

typedef struct _STATE STATE;

template<typename T>
void test_instruction_base(T& a, T& b, T expected) {
    STATE state;
    state.CF = false;
    state.ZF = false;
    state.SF = false;
    state.OF = false;
    state.AF = false;
    state.PF = false;
    state.IF = false;
    
    ADD_(a, b, state.m2cflags);
    
    ASSERT_EQ(expected, a) << "Instruction result mismatch";
}

template<typename T>
void test_instruction_flags(T& a, T& b, bool CF_expected, 
                           bool ZF_expected, bool SF_expected, 
                           bool OF_expected, bool AF_expected) {
    STATE state;
    memset(&state, 0, sizeof(STATE));
    
    ADD_(a, b, state.m2cflags);
    
    ASSERT_EQ(CF_expected, state.CF) << "CF flag mismatch";
    ASSERT_EQ(ZF_expected, state.ZF) << "ZF flag mismatch";
    ASSERT_EQ(SF_expected, state.SF) << "SF flag mismatch";
    ASSERT_EQ(OF_expected, state.OF) << "OF flag mismatch";
    ASSERT_EQ(AF_expected, state.AF) << "AF flag mismatch";
}

class InsnTests : public ::testing::Test {
protected:
    virtual void SetUp() {}
    virtual void TearDown() {}
};

TEST_F(InsnTests, ADD_8bit) {
    db a = 0x10;
    db b = 0x20;
    test_instruction_base(a, b, 0x30);
}

TEST_F(InsnTests, ADD_16bit) {
    dw a = 0x100;
    dw b = 0x200;
    test_instruction_base(a, b, 0x300);
}

TEST_F(InsnTests, ADD_32bit) {
    dd a = 0x10000000;
    dd b = 0x20000000;
    test_instruction_base(a, b, 0x30000000);
}

TEST_F(InsnTests, ADC_8bit) {
    db a = 0x10;
    db b = 0x20;
    db CF = 1;
    test_instruction_base(a, b, 0x31);
}

// Add more test cases for different instructions and edge cases...
// This is just a starting point, we should add:
// - Subtraction operations (SUB_)
// - Bit manipulation (AND_, OR_, XOR_)
// - Shift/rotate operations (SHL_, SHR_, etc.)
// - Flag-specific tests
// - Overflow cases
// - Zero/Negative/Carry/Parity checks

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
