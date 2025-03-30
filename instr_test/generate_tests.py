import re

def generate_test_body(instruction, operands, result, initial_flags, expected_flags, data_type):
  """Generates the body of a Google Test case for a given instruction."""
  initial_cf = "true" if int(initial_flags, 16) & 0x0001 else "false"
  expected_cf = "true" if int(expected_flags, 16) & 0x0001 else "false"
  expected_of = "true" if int(expected_flags, 16) & 0x0800 else "false"
  expected_sf = "true" if int(expected_flags, 16) & 0x0080 else "false"
  expected_zf = "true" if int(expected_flags, 16) & 0x0040 else "false"

  if instruction in ["ADD", "ADC", "SUB", "SBB", "OR", "AND", "XOR", "CMP", "TEST"]:
    initial_dest = operands[0]
    src = operands[1]
    if instruction == "CMP":
        instruction = "SUB"  # CMP uses the same logic as SUB for flags
    if instruction == "TEST":
        instruction = "AND"  # TEST uses the same logic as AND for flags
    test_body = f"""
    Test{instruction}<{data_type}>({initial_dest}, {src}, {result}, {expected_cf}, {expected_of}, {expected_sf}, {expected_zf}, {initial_cf});
    """
  elif instruction in ["INC", "DEC", "NOT"]:
    initial_value = operands[0]
    test_body = f"""
    Test{instruction}<{data_type}>({initial_value}, {result}, {expected_of}, {expected_sf}, {expected_zf});
    """
  elif instruction in ["SHR", "SHL", "SAR", "ROL", "ROR", "RCL", "RCR"]:
    initial_value = operands[0]
    shift_amount = operands[1]
    test_body = f"""
    Test{instruction}<{data_type}>({initial_value}, {shift_amount}, {result}, {expected_cf}, {expected_of}, {expected_sf}, {expected_zf}, {initial_cf});
    """
  elif instruction in ["SHLD", "SHRD"]:
    initial_dest = operands[0]
    src = operands[1]
    count = operands[2]
    test_body = f"""
    Test{instruction}<{data_type}>({initial_dest}, {src}, {count}, {result}, {expected_cf}, {expected_of}, {expected_sf}, {expected_zf});
    """
  elif instruction == "NEG":
    initial_value = operands[0]
    test_body = f"""
    TestNEG<{data_type}>({initial_value}, {result}, {expected_cf}, {expected_of}, {expected_sf}, {expected_zf});
    """
  elif instruction in ["DAA", "DAS", "AAA", "AAS", "AAM", "AAD"]:
    initial_value = operands[0]
    test_body = f"""
    Test{instruction}<{data_type}>({initial_value}, {result}, {expected_cf}, {expected_of}, {expected_sf}, {expected_zf}, {initial_cf});
    """
  elif instruction == "BSWAP":
    initial_value = operands[0]
    test_body = f"""
    TestBSWAP<{data_type}>({initial_value}, {result});
    """
  elif instruction in ["CBW", "CWDE", "CWD", "CDQ"]:
    initial_value = operands[0]
    test_body = f"""
    Test{instruction}<{data_type}>({initial_value}, {result});
    """
  else:
    test_body = f"    // Unhandled instruction: {instruction}"

  return test_body

def main():
  """Parses the test file and generates Google Test cases."""
  with open("test-i386_conv.txt", "r") as f:
    lines = f.readlines()

  tests = {}
  for line in lines:
    # Match instructions with optional operands B and C using named groups
    match = re.match(r"(?P<instruction>[a-z]+)(?P<datatype>[lwb])\s+A=(?P<operandA>[0-9a-fA-F]+)\s+(B=(?P<operandB>[0-9a-fA-F]+)\s+)?(C=(?P<operandC>[0-9a-fA-F]+)\s+)?(AH=(?P<operandAH>[0-9a-fA-F]+)\s+AL=(?P<operandAL>[0-9a-fA-F]+)\s+)?(RH=(?P<resultH>[0-9a-fA-F]+)\s+RL=(?P<resultL>[0-9a-fA-F]+)\s+)?R=(?P<result>[0-9a-fA-F]+)\s+CCIN=(?P<initial_flags>[0-9a-fA-F]+)\s+CC=(?P<expected_flags>[0-9a-fA-F]+)", line)
    if match:
      instruction = match.group("instruction").upper()
      data_type = "dd" if match.group("datatype") == 'l' else ("dw" if match.group("datatype") == 'w' else "db")
      operands = [f"0x{match.group('operandA')}"]
      if match.group("operandB"):
        operands.append(f"0x{match.group('operandB')}")
      if match.group("operandC"):
        operands.append(f"0x{match.group('operandC')}")
      if match.group("operandAH") and match.group("operandAL"):
        operands = [f"0x{match.group('operandAH')}", f"0x{match.group('operandAL')}"]
      # Construct result based on available groups
      result = f"0x{match.group('result')}" if match.group('result') else (f"0x{match.group('resultH')}", f"0x{match.group('resultL')}") if match.group('resultH') and match.group('resultL') else None
      initial_flags = match.group("initial_flags")
      expected_flags = match.group("expected_flags")

      if instruction not in tests:
        tests[instruction] = []
      tests[instruction].append((operands, result, initial_flags, expected_flags, data_type))

  print("```cpp")
  print("#include <gtest/gtest.h>")
  print("#include \"asm.h\"")
  print()
  print("namespace {")
  print("  class EmulatedInstructionsTest : public ::testing::Test {")
  print("   protected:")
  print("    m2c::_STATE state;")
  print()
  print("    void SetUp() override {")
  print("      m2cflags.reset();")
  print("    }")
  print()
  for instruction, test_cases in tests.items():
    print(f"  TEST_F(EmulatedInstructionsTest, {instruction}) {{")
    for operands, result, initial_flags, expected_flags, data_type in test_cases:
      if result is None:
        print(f"    // Skipping test case with missing result for {instruction}")
        continue
      if isinstance(result, tuple):
        result = f"std::make_pair({result[0]}, {result[1]})"
      test_body = generate_test_body(instruction, operands, result, initial_flags, expected_flags, data_type)
      print(test_body)
    print("  }")
    print()
  print("  };")
  print("}  // namespace")
  print("```")

if __name__ == "__main__":
  main()