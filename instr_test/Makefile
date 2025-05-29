CXX ?= g++
SDL = -DNOSDL
CURSES = -DNOCURSES
OPT = -std=c++14 -Wno-narrowing -mno-ms-bitfields -Wno-multichar -Wno-overflow $(SDL) $(CURSES) -D_GNU_SOURCE=1 -ggdb3 -O0 -I. -I.. -I../..

SRC = ../asm.cpp ../memmgr.cpp ../shadowstack.cpp test_insn_tests.cpp
OBJ = $(SRC:.cpp=.o)
EXE = test_insn_tests

all: $(EXE)

$(EXE): $(OBJ)
	$(CXX) $(OPT) $^ -lgtest -lgtest_main -o $@

%.o: %.cpp
	$(CXX) $(OPT) -c $< -o $@

clean:
	rm -f $(OBJ) $(EXE)

test: test_insn_tests
	./test_insn_tests

.PHONY: all clean