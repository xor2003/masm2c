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
        description="Run project quality checks (ruff, mypy, vulture, radon, pytest)."
    )
    parser.add_argument(
        "--no-pytest",
        action="store_true",
        help="Skip pytest.",
    )
    parser.add_argument(
        "--min-vulture-confidence",
        type=int,
        default=80,
        help="Vulture minimum confidence threshold (default: 80).",
    )
    args = parser.parse_args()

    run_step("Ruff", [sys.executable, "-m", "ruff", "check", "masm2c", "tests"])
    run_step("Mypy", [sys.executable, "-m", "mypy", "masm2c"])
    run_step(
        "Vulture",
        [
            sys.executable,
            "-m",
            "vulture",
            "masm2c",
            "--min-confidence",
            str(args.min_vulture_confidence),
        ],
    )
    run_step("Radon CC", [sys.executable, "-m", "radon", "cc", "-s", "-a", "masm2c"])

    if not args.no_pytest:
        run_step("Pytest", [sys.executable, "-m", "pytest", "-q"])

    print("\nQA checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
