#ifndef TEST_FIXTURE_H
#define TEST_FIXTURE_H

#include <gtest/gtest.h>
#include "test_globals.h"

class EmulatedInstructionsTest : public ::testing::Test {
protected:
    void SetUp() override {
        memset(&sstate, 0, sizeof(m2c::_STATE));
        _state = &sstate;
    }
};

#endif // TEST_FIXTURE_H