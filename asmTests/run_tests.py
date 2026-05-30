#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKIP_CASES = {
    "popf.asm": "unsupported: call loc_15c4a+1",
}


@dataclass
class CaseResult:
    name: str
    status: str  # PASS|FAIL|SKIP
    rc: int
    reason: str = ""
    log_file: Path | None = None


def discover_cases(script_dir: Path) -> list[str]:
    cases: list[str] = []
    for p in sorted(script_dir.glob("*.asm")):
        cases.append(p.name)
    for p in sorted(script_dir.glob("*.lst")):
        cases.append(p.name)
    return sorted(cases)


def compile_runtime(script_dir: Path, cxx: str) -> None:
    parent = script_dir.parent
    cfg = script_dir / "_config.sh"
    compile_targets = ("asm.cpp", "memmgr.cpp", "shadowstack.cpp")
    for source in compile_targets:
        cmd = (
            f"set -euo pipefail; "
            f". '{cfg}'; "
            f"'{cxx}' $OPT '{source}' -c"
        )
        subprocess.run(["bash", "-lc", cmd], cwd=parent, check=True)


def run_case(script_dir: Path, name: str, logs_dir: Path, cxx: str) -> CaseResult:
    base = name.rsplit(".", 1)[0]
    log_file = logs_dir / f"{base}.log"

    if name in SKIP_CASES:
        msg = f"Testing {name}:\nSKIP {SKIP_CASES[name]}\n"
        log_file.write_text(msg, encoding="utf-8")
        return CaseResult(name=name, status="SKIP", rc=0, reason=SKIP_CASES[name], log_file=log_file)

    cmd = ["bash", str(script_dir / "_singletest.sh"), name]
    env = os.environ.copy()
    env["CXX"] = cxx
    env["PYTHON"] = sys.executable
    proc = subprocess.run(cmd, cwd=script_dir, env=env, capture_output=True, text=True)
    output = f"Testing {name}:\n{proc.stdout}{proc.stderr}"
    log_file.write_text(output, encoding="utf-8", errors="replace")
    if proc.returncode == 0:
        return CaseResult(name=name, status="PASS", rc=0, log_file=log_file)
    return CaseResult(name=name, status="FAIL", rc=proc.returncode, reason=f"exit={proc.returncode}", log_file=log_file)


def summarize(results: Iterable[CaseResult], logs_dir: Path) -> int:
    ordered = list(results)
    passed = sum(1 for r in ordered if r.status == "PASS")
    skipped = sum(1 for r in ordered if r.status == "SKIP")
    failed = sum(1 for r in ordered if r.status == "FAIL")
    total = len(ordered)

    print("\n==================== asmTests summary ====================")
    for r in ordered:
        if r.status == "FAIL":
            print(f"{r.status:<5} {r.name} ({r.reason})")
        elif r.status == "SKIP":
            print(f"{r.status:<5} {r.name} ({r.reason})")
        else:
            print(f"{r.status:<5} {r.name}")
    print("----------------------------------------------------------")
    print(f"Total: {total}  Passed: {passed}  Skipped: {skipped}  Failed: {failed}")
    print(f"Logs: {logs_dir}")
    print("==========================================================")
    return failed


def main() -> int:
    ap = argparse.ArgumentParser(description="Run asmTests suite")
    ap.add_argument("--jobs", "-j", type=int, default=int(os.environ.get("JOBS", "1")), help="parallel jobs")
    ap.add_argument("--filter", default="", help="substring filter for case names")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    logs_dir = script_dir / ".test-logs"
    logs_dir.mkdir(exist_ok=True)

    cxx = os.environ.get("CXX", "g++")
    print(f"Preparing runtime objects (CXX={cxx}, JOBS={args.jobs})...")
    compile_runtime(script_dir, cxx)

    cases = discover_cases(script_dir)
    if args.filter:
        cases = [c for c in cases if args.filter in c]
    print(f"Discovered {len(cases)} tests.")
    if not cases:
        return 0

    results: list[CaseResult] = []
    if args.jobs <= 1:
        for c in cases:
            results.append(run_case(script_dir, c, logs_dir, cxx))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futs = [ex.submit(run_case, script_dir, c, logs_dir, cxx) for c in cases]
            for f in concurrent.futures.as_completed(futs):
                results.append(f.result())
        results.sort(key=lambda r: r.name)

    result_log = script_dir / "_result.log"
    with result_log.open("w", encoding="utf-8") as out:
        for r in results:
            if r.log_file and r.log_file.exists():
                out.write(r.log_file.read_text(encoding="utf-8", errors="replace"))
                out.write("\n")

    failures = summarize(results, logs_dir)
    print(f"Total result: {failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
