#!/usr/bin/env bash
set -euo pipefail

if [ -z "${CXX:-}" ]; then
  export CXX=g++
fi

name="${1:-}"
if [ -z "${name}" ]; then
  exit 0
fi
if [ ! -r "${name}" ]; then
  echo "No such file ${name}"
  exit 2
fi

base="${name%.*}"
work_log="${base}.txt"

cleanup_outputs() {
  rm -f \
    "${base}.cpp" "${base}.h" "${base}.err" "${base}.log" "${base}.txt" \
    "${base}.asm.log" "${base}.o" "${base}" asm.log
}

run_step() {
  local step_name="$1"
  shift
  if ! "$@" > "${work_log}" 2>&1; then
    echo "Step failed: ${step_name}"
    cat "${work_log}"
    return 1
  fi
}

cleanup_outputs

run_step "translate" "${PYTHON:-python3}" ../masm2c.py -m separate "${name}"
run_step "build" ./build.sh "${base}"
run_step "execute" "./${base}"
