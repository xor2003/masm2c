# AGENTS.md

## Project Purpose
`masm2c` is a source-to-source translator that converts 16-bit x86 MASM/IDA listings (`.asm`, `.lst`) into compilable C/C++ plus segment metadata (`.seg`).

Primary implementation is Python (`masm2c/` package). The repo also contains many generated artifacts, historical experiments, and test fixtures.

## Canonical Entrypoints
- CLI module: `masm2c/cli.py`
- Script wrapper: `masm2c.py` (calls `masm2c.cli.main`)
- Installed console script: `masm2c` -> `masm2c.cli:main` (from `pyproject.toml`)

## Core Translation Flow
- Parse arguments in `masm2c/cli.py` (`parse_args`)
- For each `.asm`/`.lst` input, run `process(...)`
- `Parser` (`masm2c/parser.py`) parses and builds context
- `Cpp` (`masm2c/cpp.py`) generates `.cpp/.h` and optional globals list
- `.seg` inputs are merged via `Cpp.convert_segment_files_into_datacpp(...)`

## Important CLI Flags
- `-m/--mergeprocs`: `separate|persegment|single`
- `-p/--passes`: `1|2`
- `-lo/--loadsegment`: load segment (default `0x1a2`)
- `-AT`: force DOS `.com` load segment (`0x192`)
- `-FL/--list`: emit `.list` globals/procs/labels

## Environment and Dependencies
- Python `>=3.9`
- Runtime deps: `lark`, `jsonpickle`
- Dev/test deps: `pytest`, `mock`, `coverage`

Install:
```bash
rtk pip install -r requirements.txt
```

## Recommended Commands
Run translator:
```bash
rtk python masm2c.py game.asm
rtk python -m masm2c.cli -m persegment -FL game.asm
```

Run Python tests:
```bash
rtk pytest -q
```

Run unified Python quality checks:
```bash
rtk python scripts/qa.py
```

Run C++ instruction test target:
```bash
rtk make check
```

## File Editing Policy
Prefer editing these source files:
- `masm2c/*.py` (especially `cli.py`, `parser.py`, `cpp.py`, `proc.py`, `op.py`, `Token.py`, `Macro.py`)
- Packaging/config files (`pyproject.toml`, `requirements.txt`, `pytest.ini`, `Makefile`)
- Tests in `tests/`

Avoid editing generated or bulky artifacts unless explicitly required:
- `masm2c/*.c`, `masm2c/*.html` (generated Cython/coverage outputs)
- Root-level generated outputs (`*.seg`, many `*.cpp/*.h` fixture outputs, `*.log`, `*.list`, `asmTests` outputs)

## Testing Expectations for Changes
- Parser/CLI/codegen changes: run at least `rtk pytest -q`
- Instruction-emulation/runtime-sensitive changes: also run `rtk make check`
- If output format changes, validate with a representative `.asm` sample and inspect generated `.cpp/.h/.seg`

## CI/CD Expectations
- Keep GitHub Actions simple and conventional: install deps, lint, type-check, unit test, then integration scripts.
- Required quality gates for Python changes:
  - `python scripts/qa.py`
- Integration/script checks should remain runnable via shell:
  - `make ci-qa`
  - `make ci-pytest`
  - `make ci-asmtests` (local regression pass; `popf.asm` unsupported and intentionally skipped)
  - `make ci-qemu-tests`
- Prefer updating existing workflows under `.github/workflows/` instead of adding redundant pipelines.

## Safe Refactor Workflow
For parser/transpiler cleanup (especially recursive parsing and shared state), use this strict loop:
1. Establish baseline first with `rtk pytest -q` and only refactor on green tests.
2. Make one small change at a time (single concern, minimal diff).
3. Re-run `rtk pytest -q` after every small change.
4. If a step fails, revert or fix immediately before continuing.
5. After the final step, run `rtk pytest -q` again and summarize behavior-impact explicitly.

Additional rule for include/recursion code:
- Preserve deterministic LIFO state restoration for file/segment/proc context; avoid unordered containers for stack-like behavior.

## Practical Notes
- The repository is intentionally mixed: production code + reverse-engineering artifacts + historical binaries.
- Limit scope to relevant package code and targeted tests; do not mass-reformat generated fixture outputs.
- Keep behavior compatible with MASM 6 style syntax and IDA `.lst` workflows described in `README.md`.
