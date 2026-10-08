CXX ?= g++
PYTHON ?= python3
SDL = -DNOSDL
CURSES = -DNOCURSES
OPT = -std=c++14 -Wno-narrowing -mno-ms-bitfields -Wno-multichar -Wno-overflow $(SDL) $(CURSES) -D_GNU_SOURCE=1 -DNOSDL -ggdb3 -O0 -I. -I.. -I../.. -DINSTRUCTION_TESTS -DM2CDEBUG=2

SRC = ../asm.cpp ../memmgr.cpp ../shadowstack.cpp test_globals.cpp pm16_test.cpp $(wildcard generated_tests_*.cpp)
OBJ = $(SRC:.cpp=.o)
EXE = instruction_tests

# Sanitized build (AddressSanitizer + UndefinedBehaviorSanitizer), built with
# clang++: -fsanitize-ignorelist is a clang-only flag and the second compiler
# exercises the runtime differently than g++. Entries in
# sanitize_ignorelist.txt are verified-intentional 16-bit behaviors.
SAN_CXX ?= clang++
SAN_OPT = $(OPT) -Wno-constant-conversion -fsanitize=address,undefined -fno-omit-frame-pointer -fsanitize-ignorelist=sanitize_ignorelist.txt
SAN_OBJ = $(SRC:.cpp=.san.o)
SAN_EXE = instruction_tests_asan

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

$(SAN_EXE): $(SAN_OBJ)
	$(SAN_CXX) $(SAN_OPT) $^ -lgtest -lpthread -o $@

%.san.o: %.cpp
	$(SAN_CXX) $(SAN_OPT) -c $< -o $@

clean:
	rm -f $(OBJ) $(SAN_OBJ) generated_tests_*.cpp $(GEN_STAMP) $(EXE) $(SAN_EXE)

test: $(GEN_STAMP)
	@$(MAKE) --no-print-directory $(EXE)
	./$(EXE)

test-sanitize: $(GEN_STAMP)
	@$(MAKE) --no-print-directory $(SAN_EXE)
	ASAN_OPTIONS=detect_leaks=0 ./$(SAN_EXE)

.PHONY: all clean test test-sanitize