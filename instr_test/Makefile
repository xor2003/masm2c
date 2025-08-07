CXX ?= g++
SDL = -DNOSDL
CURSES = -DNOCURSES
OPT = -std=c++14 -Wno-narrowing -mno-ms-bitfields -Wno-multichar -Wno-overflow $(SDL) $(CURSES) -D_GNU_SOURCE=1 -ggdb3 -O0 -I. -I.. -I../.. -DINSTRUCTION_TESTS

SRC = ../asm.cpp ../memmgr.cpp ../shadowstack.cpp test_globals.cpp $(wildcard generated_tests_*.cpp)
OBJ = $(SRC:.cpp=.o)
EXE = instruction_tests

all: $(EXE)

$(EXE): $(OBJ)
	$(CXX) $(OPT) $^ -lgtest -lpthread -o $@

%.o: %.cpp
	$(CXX) $(OPT) -c $< -o $@

clean:
	rm -f $(OBJ) $(EXE)

test: instruction_tests
	./instruction_tests

.PHONY: all clean