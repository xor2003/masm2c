#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import os
import shutil
import shlex
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


def get_opt_flags(script_dir: Path) -> str:
    cfg = script_dir / "_config.sh"
    cmd = f"set -euo pipefail; . '{cfg}'; printf '%s' \"$OPT\""
    proc = subprocess.run(["bash", "-lc", cmd], cwd=script_dir.parent, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def generated_cpp_sources(work_dir: Path, base: str) -> list[str]:
    sources = [f"{base}.cpp"]
    sources.extend(path.name for path in sorted(work_dir.glob(f"{base}_*.cpp")))
    return sources


def prepare_case_workspace(script_dir: Path, name: str) -> Path:
    base = name.rsplit(".", 1)[0]
    work_root = script_dir / ".test-work"
    work_dir = work_root / base
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    src_case = script_dir / name
    shutil.copy2(src_case, work_dir / name)

    # Preserve include compatibility for isolated per-case runs.
    for pattern in ("*.inc", "*.asm", "*.lst", "*.map", "*.txt"):
        for src in script_dir.glob(pattern):
            dst = work_dir / src.name
            if dst.exists():
                continue
            try:
                os.symlink(src, dst)
            except OSError:
                shutil.copy2(src, dst)
    return work_dir


def run_case(script_dir: Path, name: str, logs_dir: Path, cxx: str, opt_flags: str) -> CaseResult:
    base = name.rsplit(".", 1)[0]
    log_file = logs_dir / f"{base}.log"

    if name in SKIP_CASES:
        msg = f"Testing {name}:\nSKIP {SKIP_CASES[name]}\n"
        log_file.write_text(msg, encoding="utf-8")
        return CaseResult(name=name, status="SKIP", rc=0, reason=SKIP_CASES[name], log_file=log_file)

    work_dir = prepare_case_workspace(script_dir, name)
    repo_root = script_dir.parent
    output_chunks: list[str] = [f"Testing {name}:"]

    translate = [
        sys.executable,
        str(repo_root / "masm2c.py"),
        "-m",
        "separate",
        name,
    ]
    t = subprocess.run(translate, cwd=work_dir, capture_output=True, text=True)
    output_chunks.append(t.stdout)
    output_chunks.append(t.stderr)
    if t.returncode != 0:
        output_chunks.append("Step failed: translate\n")
        output = "\n".join(output_chunks)
        log_file.write_text(output, encoding="utf-8", errors="replace")
        return CaseResult(name=name, status="FAIL", rc=t.returncode, reason=f"exit={t.returncode}", log_file=log_file)

    compile_cmd = [
        cxx,
        "_data.cpp",
        *generated_cpp_sources(work_dir, base),
        str(repo_root / "asm.o"),
        str(repo_root / "memmgr.o"),
        str(repo_root / "shadowstack.o"),
        *shlex.split(opt_flags),
        f"-I{script_dir}",
        f"-I{repo_root}",
        "-o",
        base,
    ]
    b = subprocess.run(compile_cmd, cwd=work_dir, capture_output=True, text=True)
    output_chunks.append(b.stdout)
    output_chunks.append(b.stderr)
    if b.returncode != 0:
        output_chunks.append("Step failed: build\n")
        output = "\n".join(output_chunks)
        log_file.write_text(output, encoding="utf-8", errors="replace")
        return CaseResult(name=name, status="FAIL", rc=b.returncode, reason=f"exit={b.returncode}", log_file=log_file)

    e = subprocess.run([str(work_dir / base)], cwd=work_dir, capture_output=True, text=True)
    output_chunks.append(e.stdout)
    output_chunks.append(e.stderr)
    if e.returncode != 0:
        output_chunks.append("Step failed: execute\n")
        output = "\n".join(output_chunks)
        log_file.write_text(output, encoding="utf-8", errors="replace")
        return CaseResult(name=name, status="FAIL", rc=e.returncode, reason=f"exit={e.returncode}", log_file=log_file)

    output = "\n".join(output_chunks)
    log_file.write_text(output, encoding="utf-8", errors="replace")
    return CaseResult(name=name, status="PASS", rc=0, log_file=log_file)


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
    if failed:
        print("\nFailure details (last log lines per file):")
        for r in ordered:
            if r.status != "FAIL" or not r.log_file or not r.log_file.exists():
                continue
            print(f"\n--- {r.name} ({r.reason}) ---")
            try:
                lines = r.log_file.read_text(encoding="utf-8", errors="replace").splitlines()
                tail = lines[-40:] if len(lines) > 40 else lines
                for line in tail:
                    print(line)
            except Exception as ex:
                print(f"[could not read log: {ex}]")
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
    opt_flags = get_opt_flags(script_dir)
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
            results.append(run_case(script_dir, c, logs_dir, cxx, opt_flags))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futs = [ex.submit(run_case, script_dir, c, logs_dir, cxx, opt_flags) for c in cases]
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
