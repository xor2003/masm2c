"""Parser performance benchmark for asmTests fixtures.

Runs parser-only passes over .asm and .lst files from asmTests without invoking
gen/compile/runtime tooling.
"""

from __future__ import annotations

import argparse
import cProfile
import os
import logging
import statistics
import time
from pathlib import Path
from typing import Sequence

from masm2c.parser import Parser


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark parser-only throughput")
    parser.add_argument("cases_dir", nargs="?", default="asmTests", help="Directory with .asm/.lst fixtures")
    parser.add_argument("--passes", type=int, default=2, help="Parser passes per file")
    parser.add_argument("--engine", default="postlex", help="Parser engine: postlex or cython")
    parser.add_argument(
        "--runs",
        type=int,
        default=0,
        help="Number of measured runs; 0 means benchmark by target seconds",
    )
    parser.add_argument(
        "--target-seconds",
        type=float,
        default=float(os.getenv("PARSER_BENCH_TARGET_SECONDS", "60")),
        help="Target runtime for sampled benchmark in seconds (default: 60)",
    )
    parser.add_argument(
        "--max-runs",
        type=int,
        default=int(os.getenv("PARSER_BENCH_MAX_RUNS", "500")),
        help="Safety cap when benchmarking by time",
    )
    parser.add_argument("--warmup", type=int, default=1, help="Number of warmup runs")
    parser.add_argument("--profile", default="", help="Optional cProfile output path")
    parser.add_argument("--no-sort", action="store_true", help="Keep natural file ordering")
    parser.add_argument("--quiet", action="store_true", help="Suppress parser logging during benchmark")
    return parser.parse_args()


def collect_cases(path: Path, sort_names: bool) -> list[str]:
    cases: list[str] = [str(p) for p in path.glob("*.asm")]
    cases.extend(str(p) for p in path.glob("*.lst"))
    if sort_names:
        cases = sorted(cases)
    return cases


def run_once(cases: Sequence[str], args: argparse.Namespace) -> None:
    parser_args = {"mergeprocs": "separate", "passes": args.passes}
    for name in cases:
        p = Parser(parser_args)
        counter = Parser.c_dummy_label[0]
        p.parse_file(name)
        if args.passes >= 2:
            p.next_pass(counter)
            p.parse_file(name)


def benchmark(cases: Sequence[str], args: argparse.Namespace) -> list[float]:
    if args.warmup:
        for _ in range(args.warmup):
            run_once(cases, args)

    times: list[float] = []
    if args.runs > 0:
        for _ in range(args.runs):
            start = time.perf_counter()
            run_once(cases, args)
            times.append(time.perf_counter() - start)
        return times

    if args.max_runs <= 0:
        raise ValueError("max_runs must be >= 1 when using time-based benchmarking")

    start = time.perf_counter()
    while True:
        if len(times) >= args.max_runs:
            break
        run_start = time.perf_counter()
        run_once(cases, args)
        times.append(time.perf_counter() - run_start)
        if time.perf_counter() - start >= args.target_seconds:
            break
    return times


def print_stats(times: list[float]) -> None:
    total = sum(times)
    avg = statistics.mean(times)
    median = statistics.median(times)
    mn = min(times)
    mx = max(times)
    stdev = statistics.pstdev(times) if len(times) > 1 else 0.0
    print(f"runs={len(times)} min={mn:.4f}s max={mx:.4f}s mean={avg:.4f}s median={median:.4f}s stdev={stdev:.4f}s total={total:.4f}s")


def main() -> int:
    args = parse_args()

    if args.passes <= 0:
        raise ValueError("passes must be >= 1")
    if args.runs < 0:
        raise ValueError("runs must be >= 0")

    cases_dir = Path(args.cases_dir)
    cases = collect_cases(cases_dir, sort_names=not args.no_sort)

    print(f"parser benchmark: dir={cases_dir} files={len(cases)} engine={args.engine} passes={args.passes}")
    if not cases:
        print("no input files found")
        return 1

    os.environ["MASM2C_PARSER_ENGINE"] = args.engine
    if args.quiet:
        logging.disable(logging.CRITICAL)

    if args.profile:
        prof = cProfile.Profile()
        prof.enable()
        times = benchmark(cases, args)
        prof.disable()
        prof.dump_stats(args.profile)
    else:
        times = benchmark(cases, args)

    print_stats(times)
    print(f"files per second: {len(cases) / statistics.mean(times):.2f}")
    print("samples")
    print(" " + " ".join(f"{t:.4f}" for t in times))
    if args.profile:
        print(f"profile saved: {args.profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
