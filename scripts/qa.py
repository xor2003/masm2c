#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_step(name: str, cmd: list[str]) -> None:
    print(f"\n==> {name}")
    print(f"$ {' '.join(shlex.quote(part) for part in cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run project quality checks (ruff, mypy, basta, lizard, clang, pytest)."
    )
    parser.add_argument(
        "--no-pytest",
        action="store_true",
        help="Skip pytest.",
    )
    parser.add_argument(
        "--no-clang",
        action="store_true",
        help="Skip the clang-check/clang-tidy pass over committed C/C++ files.",
    )
    parser.add_argument(
        "--no-basta",
        action="store_true",
        help="Skip the basta dead-code check (requires the basta binary, "
             "e.g. via 'npm install -g basta').",
    )
    args = parser.parse_args()

    run_step("Ruff", [sys.executable, "-m", "ruff", "check", "masm2c", "tests",
                      "scripts", "asmTests", "docs", "instr_test", "masm2c.py"])
    run_step("Mypy", [sys.executable, "-m", "mypy", "masm2c"])
    if not args.no_basta:
        run_step(
            "Basta",
            [
                "basta",
                "masm2c",
                "tests",
                "scripts",
                "asmTests",
                "instr_test",
                "masm2c.py",
                "--include-tests",
                "--exit-code",
                "1",
            ],
        )
    run_step("Lizard", [sys.executable, "-m", "lizard", "masm2c"])

    if not args.no_clang:
        run_step("Clang checks", ["sh", "scripts/check_cpp.sh"])

    if not args.no_pytest:
        run_step("Pytest", [sys.executable, "-m", "pytest", "-q"])

    print("\nQA checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
