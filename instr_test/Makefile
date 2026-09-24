CXX ?= g++
PYTHON ?= python3
SDL = -DNOSDL
CURSES = -DNOCURSES
OPT = -std=c++14 -Wno-narrowing -mno-ms-bitfields -Wno-multichar -Wno-overflow $(SDL) $(CURSES) -D_GNU_SOURCE=1 -DNOSDL -ggdb3 -O0 -I. -I.. -I../.. -DINSTRUCTION_TESTS -DM2CDEBUG=2

SRC = ../asm.cpp ../memmgr.cpp ../shadowstack.cpp test_globals.cpp $(wildcard generated_tests_*.cpp)
OBJ = $(SRC:.cpp=.o)
EXE = instruction_tests

# generated_tests_*.cpp are produced by generate_tests.py from test-i386_conv.txt.
# They are built through a sub-make so that the wildcard above is re-expanded
# after generation on a fresh checkout.
GEN_STAMP = .generated_tests.stamp

all: $(GEN_STAMP)
	@$(MAKE) --no-print-directory $(EXE)

$(GEN_STAMP): test-i386_conv.txt generate_tests.py
	$(PYTHON) generate_tests.py
	touch $@

$(EXE): $(OBJ)
	$(CXX) $(OPT) $^ -lgtest -lpthread -o $@

%.o: %.cpp
	$(CXX) $(OPT) -c $< -o $@

clean:
	rm -f $(OBJ) generated_tests_*.cpp $(GEN_STAMP) $(EXE)

test: $(GEN_STAMP)
	@$(MAKE) --no-print-directory $(EXE)
	./$(EXE)

.PHONY: all clean test