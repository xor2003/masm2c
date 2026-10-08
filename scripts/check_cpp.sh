#!/bin/sh
# Lint committed C/C++ sources with clang-check (parse/semantic gate) and
# clang-tidy (static analyzer, see .clang-tidy).
#
# Coverage policy:
#   - every committed .c/.cpp file that can be parsed standalone is run
#     through clang-check with the same flags the project builds with;
#   - handwritten sources additionally get clang-tidy;
#   - generated translator outputs (vikings/, examples/) and vendored QEMU
#     test harnesses are skipped or only parse-checked: their warnings cannot
#     be fixed without touching code that is regenerated or upstream;
#   - headers are not parsed standalone (they are not self-contained); they
#     are covered transitively through the translation units.
set -eu

cd "$(dirname "$0")/.."

# Flags mirroring instr_test/Makefile (32-bit-model emulator runtime).
BASE_FLAGS="-std=c++14 -Wno-narrowing -mno-ms-bitfields -Wno-multichar -Wno-overflow -DNOSDL -DNOCURSES -D_GNU_SOURCE=1 -DINSTRUCTION_TESTS -DM2CDEBUG=2 -I."

# Files committed to git that are generated outputs kept on disk only
# (vikings/, examples/), not parseable standalone, or not real sources at
# all (convert.cpp is a committed preprocessed dump).
EXCLUDE_RE='^examples/|^vikings/|^qemu_tests/convert\.cpp$'

failures=0

check_flags() {
    case "$1" in
        qemu_tests/*.c)
            echo "-std=gnu89 -O0 -w -m32 -I." ;;
        qemu_tests/*.cpp)
            echo "-std=gnu++11 -O0 -w -fpermissive -m32 -I. -DNOSDL -DNO_SHADOW_STACK" ;;
        wine16.cpp)
            echo "-std=c++14 $(sdl2-config --cflags) -DNOCURSES -I." ;;
        *)
            echo "$BASE_FLAGS" ;;
    esac
}

is_tidy_target() {
    # Handwritten runtime/test sources only.
    case "$1" in
        asm.cpp|memmgr.cpp|shadowstack.cpp|win.cpp|wine16.cpp|instr_test/*.cpp) return 0 ;;
        *) return 1 ;;
    esac
}

for f in $(git ls-files '*.c' '*.cpp' | grep -vE "$EXCLUDE_RE"); do
    flags=$(check_flags "$f")
    if [ "$f" = "wine16.cpp" ] && ! sdl2-config --version >/dev/null 2>&1; then
        echo "SKIP $f (sdl2-config not found)"
        continue
    fi
    echo "clang-check $f"
    if ! clang-check "$f" -- $flags; then
        failures=$((failures + 1))
        continue
    fi
    if is_tidy_target "$f"; then
        echo "clang-tidy  $f"
        clang-tidy "$f" --warnings-as-errors='*' -- $flags || failures=$((failures + 1))
    fi
done

if [ "$failures" -ne 0 ]; then
    echo "check_cpp: $failures file(s) failed" >&2
    exit 1
fi
echo "check_cpp: OK"
