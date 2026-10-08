#!/usr/bin/env python3
"""
CLI Test Case Parser for QEMU test-i386.txt

This script parses CLI test cases from qemu_tests/test-i386.txt and generates
C++ unit tests in the format used by test_insn_tests.cpp, split into
multiple smaller files.
"""

import re
import sys
from typing import List, Dict, Any, Iterator, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestCase:
    """Represents a single, generalized test case from the CLI format"""
    instruction: str
    size: str
    params: Dict[str, Any] = field(default_factory=dict)
    line: str = ""

    @property
    def instruction_base(self) -> str:
        """Get the base instruction name without size suffix"""
        return self.instruction.rstrip('lwb').replace(" ", "_")

    @property
    def cpp_type(self) -> str:
        """Get the C++ type for this test case"""
        type_map = {
            'l': 'uint32_t',
            'w': 'uint16_t',
            'b': 'uint8_t'
        }
        return type_map.get(self.size, 'uint32_t')


class TestParser:
    """Parser for QEMU test-i386.txt format"""

    PATTERNS = [
        # Standard format: addl A=... B=... R=... CCIN=... CC=...
        re.compile(
            r'^\s*(?P<instr>\w+)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CCIN=(?P<CCIN>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # inc/dec/neg/not format: incl A=... R=... CCIN=... CC=...
        re.compile(
            r'^\s*(?P<instr>inc\w*|dec\w*|neg\w*|not\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CCIN=(?P<CCIN>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # BSF/BSR format: bsfl A=... R=... 0/1
        re.compile(
            r'^\s*(?P<instr>bsf\w*|bsr\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'(?P<ZF_flag>[01])'
        ),
        # BSWAP format: bswapl : A=... R=...
        re.compile(
            r'^\s*(?P<instr>bswapl)\s*:\s*'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)'
        ),
        # String operations format: cmpsb ESI=...
        re.compile(
            r'^\s*(?P<instr>(rep(n?z)?\s)?(cmpsb|cmpsw|cmpsl|movsb|movsw|movsl|lodsb|lodsw|lodsl|stosb|stosw|stosl|scasb|scasw|scasl))\s+'
            r'ESI=(?P<ESI>[0-9a-fA-F]+)\s+'
            r'EDI=(?P<EDI>[0-9a-fA-F]+)\s+'
            r'EAX=(?P<EAX>[0-9a-fA-F]+)\s+'
            r'ECX=(?P<ECX>[0-9a-fA-F]+)\s+'
            r'EFL=(?P<EFL>[0-9a-fA-F]+)'
        ),
        # shrd/shld format: shrdl A=... B=... C=... R=... CCIN=... CC=...
        re.compile(
            r'^\s*(?P<instr>shrd\w*|shld\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'C=(?P<C>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CCIN=(?P<CCIN>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # imul/mul format: imulb A=... B=... R=... CC=...
        re.compile(
            r'^\s*(?P<instr>imul\w*|mul\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # imul/mul with AH/AL format: imulw AH=... AL=... B=... RH=... RL=... CC=...
        re.compile(
            r'^\s*(?P<instr>imul\w*|mul\w*)\s+'
            r'AH=(?P<AH>[0-9a-fA-F]+)\s+'
            r'AL=(?P<AL>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'RH=(?P<RH>[0-9a-fA-F]+)\s+'
            r'RL=(?P<RL>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # imul im format: imulw im A=... B=... R=... CC=...
        re.compile(
            r'^\s*(?P<instr>imul\w*\s+im)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # idiv/div format: idivb A=... B=... R=... CC=...
        re.compile(
            r'^\s*(?P<instr>idiv\w*|div\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # idiv/div with AH/AL format: idivw AH=... AL=... B=... RH=... RL=... CC=...
        re.compile(
            r'^\s*(?P<instr>idiv\w*|div\w*)\s+'
            r'AH=(?P<AH>[0-9a-fA-F]+)\s+'
            r'AL=(?P<AL>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)\s+'
            r'RH=(?P<RH>[0-9a-fA-F]+)\s+'
            r'RL=(?P<RL>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # jcc/setcc format: jne 0/1
        re.compile(
            r'^\s*(?P<instr>j\w+|set\w+)\s+(?P<val>[01])'
        ),
        # jcxz/jecxz format: jcxz ECX=... ZF=... r=...
        re.compile(
            r'^\s*(?P<instr>jcxz|jecxz)\s+'
            r'ECX=(?P<ECX>[0-9a-fA-F]+)\s+'
            r'ZF=(?P<ZF>[01])\s+'
            r'r=(?P<r>[01])'
        ),
        # loop format: loopw ECX=... ZF=... r=...
        re.compile(
            r'^\s*(?P<instr>loop\w*)\s+'
            r'ECX=(?P<ECX>[0-9a-fA-F]+)\s+'
            r'ZF=(?P<ZF>[01])\s+'
            r'r=(?P<r>[01])'
        ),
        # daa/das format: daa A=... R=... CCIN=... CC=...
        re.compile(
            r'^\s*(?P<instr>daa|das)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CCIN=(?P<CCIN>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # aaa/aas format: aaa A=... R=... CCIN=... CC=...
        re.compile(
            r'^\s*(?P<instr>aaa|aas)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CCIN=(?P<CCIN>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # aam/aad format: aam A=... R=... CCIN=... CC=...
        re.compile(
            r'^\s*(?P<instr>aam|aad)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[0-9a-fA-F]+)\s+'
            r'CCIN=(?P<CCIN>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # xchg format: xchgl A=... B=...
        re.compile(
            r'^\s*(?P<instr>xchg\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)'
        ),
        # xadd format: xaddl A=... B=...
        re.compile(
            r'^\s*(?P<instr>xadd\w*)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'B=(?P<B>[0-9a-fA-F]+)'
        ),
        # xadd same format: xaddl same res=...
        re.compile(
            r'^\s*(?P<instr>xadd\w*)\s+same\s+res=(?P<res>[0-9a-fA-F]+)'
        ),
        # cmpxchg format: cmpxchgl EAX=... A=... C=...
        re.compile(
            r'^\s*(?P<instr>cmpxchg\w*)\s+'
            r'EAX=(?P<EAX>[0-9a-fA-F]+)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'C=(?P<C>[0-9a-fA-F]+)'
        ),
        # cmpxchg8b format: cmpxchg8b: eax=... edx=... op1=... CC=...
        re.compile(
            r'^\s*(?P<instr>cmpxchg8b)\s*:\s*'
            r'eax=(?P<eax>[0-9a-fA-F]+)\s+'
            r'edx=(?P<edx>[0-9a-fA-F]+)\s+'
            r'op1=(?P<op1>[0-9a-fA-F]+)\s+'
            r'CC=(?P<CC>[0-9a-fA-F]+)'
        ),
        # xlat format: xlat: EAX=...
        re.compile(
            r'^\s*(?P<instr>xlat)\s*:\s*'
            r'EAX=(?P<EAX>[0-9a-fA-F]+)'
        ),
        # pop format: popl esp=...
        re.compile(
            r'^\s*(?P<instr>pop\w*)\s+'
            r'esp=(?P<esp>[0-9a-fA-F]+)'
        ),
        # lea format: lea ... = ...
        re.compile(
            r'^\s*(?P<instr>lea)\s+(?P<addr>.*)\s*=\s*(?P<R>[0-9a-fA-F]+)'
        ),
        # cbw/cwde/cwd/cdq format: cbw A=... R=...
        re.compile(
            r'^\s*(?P<instr>cbw|cwde|cwd|cdq)\s+'
            r'A=(?P<A>[0-9a-fA-F]+)\s+'
            r'R=(?P<R>[\da-fA-F:]+)'
        ),
    ]

    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        self.test_cases: List[TestCase] = []

    def parse(self) -> List[TestCase]:
        """Parse the input file and return list of test cases"""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        with open(self.input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                for pattern in self.PATTERNS:
                    match = pattern.match(line)
                    if match:
                        params = {k: v for k, v in match.groupdict().items() if v is not None}
                        instruction = params.pop('instr')
                        
                        # Convert hex values to int
                        for key, value in params.items():
                            if isinstance(value, str) and value.startswith(('0x', '0X')) or all(c in '0123456789abcdefABCDEF' for c in value):
                                try:
                                    params[key] = int(value, 16)
                                except ValueError:
                                    pass # Keep as string if not a valid hex

                        test_case = TestCase(
                            instruction=instruction,
                            size=instruction[-1] if instruction[-1] in 'lwb' else 'l',
                            params=params,
                            line=line
                        )
                        self.test_cases.append(test_case)
                        break
                else:
                    # This block will be executed if no pattern matches
                    print(f"Warning: No parser found for line {line_num}: {line}")

        return self.test_cases


class CppTestGenerator:
    """Generator for C++ unit tests"""

    def __init__(self, test_cases: List[TestCase]):
        self.test_cases = test_cases

    def extract_flags(self, cc_value: int) -> Dict[str, bool]:
        """Extract individual flag values from CC value"""
        return {
            'CF': bool(cc_value & 0x0001),
            'ZF': bool(cc_value & 0x0040),
            'SF': bool(cc_value & 0x0080),
            'OF': bool(cc_value & 0x0800)
        }

    def generate_test_case(self, test: TestCase) -> str:
        """Generate a single C++ test case by dispatching to the correct method"""
        base_instruction = test.instruction_base
        
        handler_name = f"_generate_{base_instruction}_test"
        handler = getattr(self, handler_name, self._generate_unsupported_test)
        return handler(test)

    def _generate_unsupported_test(self, test: TestCase) -> str:
        return f"// Unsupported instruction: {test.instruction} on line: {test.line}"

    def _generate_standard_test(self, test: TestCase, test_function: str) -> str:
        flags = self.extract_flags(test.params['CC'])
        return f"""TEST_F(EmulatedInstructionsTest, {test.instruction}_{test.params['A']:08x}_{test.params['B']:08x}) {{
    {test_function}<{test.cpp_type}>(
        0x{test.params['A']:08x},  // initial_dest
        0x{test.params['B']:08x},  // src
        0x{test.params['R']:08x},  // expected_result
        {str(flags['CF']).lower()},  // expected_CF
        {str(flags['OF']).lower()},  // expected_OF
        {str(flags['SF']).lower()},  // expected_SF
        {str(flags['ZF']).lower()}   // expected_ZF
    );
}}"""

    def _generate_add_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestADD')

    def _generate_sub_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestSUB')

    def _generate_xor_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestXOR')

    def _generate_and_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestAND')

    def _generate_or_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestOR')

    def _generate_adc_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestADC')

    def _generate_sbb_test(self, test: TestCase) -> str:
        return self._generate_standard_test(test, 'TestSBB')

    def _generate_cmp_test(self, test: TestCase) -> str:
        flags = self.extract_flags(test.params['CC'])
        return f"""TEST_F(EmulatedInstructionsTest, {test.instruction}_{test.params['A']:08x}_{test.params['B']:08x}) {{
    TestCMP<{test.cpp_type}>(
        0x{test.params['A']:08x},  // initial_dest
        0x{test.params['B']:08x},  // src
        0x{test.params['R']:08x},  // expected_result (for comparison)
        {str(flags['CF']).lower()},  // expected_CF
        {str(flags['OF']).lower()},  // expected_OF
        {str(flags['SF']).lower()},  // expected_SF
        {str(flags['ZF']).lower()}   // expected_ZF
    );
}}"""

    def generate_header(self, filename: str) -> str:
        """Generate the header for the test file"""
        return f"""// Auto-generated test cases from QEMU test-i386.txt
// Generated by test_parser.py
// Target file: {filename}

#include "gtest/gtest.h"
#include <cstdint>

//--------------------------------------------
#define _BITS 32
#define _PROTECTED_MODE 1

#include <asm.h>

namespace m2c{{
struct Memory{{
db stack[STACK_SIZE];
db heap[HEAP_SIZE];
}};

struct Memory m;
db(& stack)[STACK_SIZE]=m.stack;
db(& heap)[HEAP_SIZE]=m.heap;
}}

m2c::_STATE sstate;
m2c::_STATE* _state=&sstate;
X86_REGREF

//--------------------------------------------

namespace m2c
{{
class EmulatedInstructionsTest : public ::testing::Test {{
 protected:
      m2c::_STATE state; 
      m2c::_STATE* _state=&state; 

    void SetUp() override {{
       memset(&state, 0, sizeof(m2c::_STATE)); 
    }}

    template <typename D, typename S>
    void TestCMP(D initial_dest, S src, D expected_result, bool expected_CF, bool expected_OF, bool expected_SF, bool expected_ZF) {{
      X86_REGREF
      D dest = initial_dest;
      D result = dest - src;
      ASSERT_EQ(result, expected_result);
      ASSERT_EQ(CF, expected_CF);
      ASSERT_EQ(OF, expected_OF);
      ASSERT_EQ(SF, expected_SF);
      ASSERT_EQ(ZF, expected_ZF);
    }}
}};
"""

    def generate_footer(self) -> str:
        """Generate the footer for the test file"""
        return "}  // namespace m2c"

    def generate_all_tests(self) -> Iterator[Tuple[str, str]]:
        """Generate all test cases, yielding one file at a time"""
        instruction_groups = {}
        for test in self.test_cases:
            base = test.instruction_base
            if base not in instruction_groups:
                instruction_groups[base] = []
            instruction_groups[base].append(test)

        for instruction_type, tests in sorted(instruction_groups.items()):
            filename = f"generated_tests_{instruction_type}.cpp"
            lines = [self.generate_header(filename)]
            
            lines.append(f"\n// {instruction_type.upper()} tests")
            for test in tests:
                test_code = self.generate_test_case(test)
                lines.append(test_code)
                lines.append("")

            lines.append(self.generate_footer())
            yield filename, "\n".join(lines)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Parse QEMU test-i386.txt and generate C++ unit tests')
    parser.add_argument('-i', '--input', default='qemu_tests/test-i386.txt',
                        help='Input test file (default: qemu_tests/test-i386.txt)')
    parser.add_argument('-o', '--output-dir', default='instr_test/generated',
                        help='Output directory for C++ files (default: instr_test/generated)')

    args = parser.parse_args()

    try:
        print(f"Parsing test cases from {args.input}...")
        parser = TestParser(args.input)
        test_cases = parser.parse()
        print(f"Found {len(test_cases)} test cases")

        print(f"Generating C++ tests to {args.output_dir}...")
        generator = CppTestGenerator(test_cases)
        
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for filename, content in generator.generate_all_tests():
            output_path = output_dir / filename
            with open(output_path, 'w') as f:
                f.write(content)
            print(f"  - Wrote {output_path}")

        print("Generation complete!")

        instruction_counts = {}
        for test in test_cases:
            base = test.instruction_base
            instruction_counts[base] = instruction_counts.get(base, 0) + 1

        print("\nTest case summary:")
        for instr, count in sorted(instruction_counts.items()):
            print(f"  {instr}: {count}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()