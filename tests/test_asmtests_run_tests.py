import os
import shlex
import shutil
from pathlib import Path
import subprocess
import sys

from asmTests.run_tests import compile_runtime, get_opt_flags, generated_cpp_sources, generated_data_sources


def test_generated_cpp_sources_include_segment_files(tmp_path: Path) -> None:
    for name in ("snake_seg001.cpp", "snake.cpp", "snake_seg000.cpp", "other_seg000.cpp"):
        (tmp_path / name).write_text("", encoding="utf-8")

    assert generated_cpp_sources(tmp_path, "snake") == [
        "snake.cpp",
        "snake_seg000.cpp",
        "snake_seg001.cpp",
    ]


def test_generated_data_sources_include_split_reference_files(tmp_path: Path) -> None:
    for name in ("_data_refs_002.cpp", "_data.cpp", "_data_refs_000.cpp"):
        (tmp_path / name).write_text("", encoding="utf-8")

    assert generated_data_sources(tmp_path) == [
        "_data.cpp",
        "_data_refs_000.cpp",
        "_data_refs_002.cpp",
    ]


def test_ret_used_as_near_indirect_jump_reaches_target() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "asmTests/run_tests.py", "--filter", "rtjmp.asm", "--jobs", "1"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    log = repo_root / "asmTests" / ".test-logs" / "rtjmp.log"
    assert "Graceful exit al=0" in log.read_text(encoding="utf-8", errors="replace")


def test_retf_to_psp_termination_vector_does_not_resume_caller() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "asmTests/run_tests.py", "--filter", "retexit.asm", "--jobs", "1"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    log = repo_root / "asmTests" / ".test-logs" / "retexit.log"
    assert "Graceful exit al=1" not in log.read_text(encoding="utf-8", errors="replace")


def test_inline_data_after_call_can_be_consumed_by_return_address() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "asmTests/run_tests.py", "--filter", "inldata.asm", "--jobs", "1"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    log = repo_root / "asmTests" / ".test-logs" / "inldata.log"
    assert "Graceful exit al=0" in log.read_text(encoding="utf-8", errors="replace")


def test_cross_proc_jump_in_single_syntax_case_executes() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "asmTests/run_tests.py", "--filter", "single_crossproc.asm", "--jobs", "1"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    log = repo_root / "asmTests" / ".test-logs" / "single_crossproc.log"
    assert "Graceful exit al=0" in log.read_text(encoding="utf-8", errors="replace")


def test_cross_proc_jump_runs_with_single_mode_merge(tmp_path: Path) -> None:
    """Translate and execute a cross-proc jump fixture using `-m single`."""
    repo_root = Path(__file__).resolve().parents[1]
    asm_tests = repo_root / "asmTests"
    name = "single_crossproc.asm"
    work_dir = tmp_path / "single_crossproc_single"
    work_dir.mkdir(parents=True, exist_ok=True)

    for source in (asm_tests / name,):
        shutil.copy2(source, work_dir / name)

    for pattern in ("*.inc", "*.asm", "*.lst", "*.map", "*.txt"):
        for source in asm_tests.glob(pattern):
            destination = work_dir / source.name
            if destination.exists():
                continue
            try:
                os.symlink(source, destination)
            except OSError:
                shutil.copy2(source, destination)

    cxx = os.environ.get("CXX", "g++")
    compile_runtime(asm_tests, cxx)

    opt_flags = get_opt_flags(asm_tests)
    translate = [
        sys.executable,
        str(repo_root / "masm2c.py"),
        "-m",
        "single",
        name,
    ]
    translation = subprocess.run(translate, cwd=work_dir, capture_output=True, text=True, check=False)
    assert translation.returncode == 0, translation.stdout + translation.stderr

    base = Path(name).stem
    compile_cmd = [
        cxx,
        *generated_data_sources(work_dir),
        *generated_cpp_sources(work_dir, base),
        str(repo_root / "asm.o"),
        str(repo_root / "memmgr.o"),
        str(repo_root / "shadowstack.o"),
        *shlex.split(opt_flags),
        f"-I{asm_tests}",
        f"-I{repo_root}",
        "-o",
        base,
    ]
    build = subprocess.run(compile_cmd, cwd=work_dir, capture_output=True, text=True, check=False)
    assert build.returncode == 0, build.stdout + build.stderr

    run = subprocess.run([str(work_dir / base)], cwd=work_dir, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    assert "Graceful exit al=0" in (run.stdout + run.stderr)


def test_cmpsb_source_segment_override_compares_code_segment_byte() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "asmTests/run_tests.py", "--filter", "cmpscs.asm", "--jobs", "1"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    log = repo_root / "asmTests" / ".test-logs" / "cmpscs.log"
    assert "Graceful exit al=0" in log.read_text(encoding="utf-8", errors="replace")
