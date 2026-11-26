#!/usr/bin/env bash
# Run breseq for all 6 clones IN PARALLEL (one breseq process per clone).
# Resource policy: ~90 vCPU -> 6 jobs x -j (nproc/6) default 15.
# breseq/bowtie2 are CPU-only; NVIDIA H20 GPUs are NOT used by this pipeline.
# Full rationale: docs/REPRODUCIBILITY.md
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Use active conda env (breseq 0.40.2). See README.md.
if [[ -z "${CONDA_PREFIX:-}" ]]; then
  echo "Activate conda env with breseq before running." >&2
  exit 1
fi
export PATH="${CONDA_PREFIX}/bin:${PATH}"

REF="data/reference/REL606_NC_012967.fasta"
mkdir -p logs results/breseq

NPROC="$(nproc)"
NCLONES=6
# Threads per breseq job (bowtie2 + internal workers); divide CPUs evenly across clones.
J="${BRESEQ_THREADS_PER_CLONE:-$(( NPROC / NCLONES ))}"
if [[ "$J" -lt 1 ]]; then J=1; fi

echo "=== breseq parallel batch ==="
echo "host CPUs: ${NPROC} · clones: ${NCLONES} · -j per clone: ${J} · total ~$(( J * NCLONES )) threads"
breseq --version
echo "started: $(date -Iseconds)"

run_paired() {
  local clone=$1
  local out="results/breseq/${clone}"
  local r1 r2
  r1="$(find "data/raw_fastq/${clone}" -name '*_1.fastq.gz' | head -1)"
  r2="$(find "data/raw_fastq/${clone}" -name '*_2.fastq.gz' | head -1)"
  [[ -f "$r1" && -f "$r2" ]] || { echo "FATAL $clone: missing pairs" >&2; return 1; }
  mkdir -p "$out"
  echo "=== breseq PAIRED $clone (-j ${J}) ==="
  breseq -j "$J" -r "$REF" -o "$out" -n "$clone" "$r1" "$r2" \
    >"logs/breseq_${clone}.log" 2>&1
}

run_single() {
  local clone=$1 fq=$2
  local out="results/breseq/${clone}"
  [[ -f "$fq" ]] || { echo "FATAL $clone: $fq" >&2; return 1; }
  mkdir -p "$out"
  echo "=== breseq SINGLE $clone (-j ${J}) ==="
  breseq -j "$J" -r "$REF" -o "$out" -n "$clone" "$fq" \
    >"logs/breseq_${clone}.log" 2>&1
}

pids=()
names=()

launch() {
  local name=$1
  shift
  (
    "$@"
  ) &
  pids+=("$!")
  names+=("$name")
}

launch 2K-A   run_paired 2K-A
launch 10K-A  run_paired 10K-A
launch 20K-A  run_paired 20K-A
launch 27K-D  run_single 27K-D data/raw_fastq/27K-D/ERR051725.fastq.gz
launch 40K-A  run_paired 40K-A
launch 40K-B  run_single 40K-B data/raw_fastq/40K-B/ERR051717.fastq.gz

fail=0
for i in "${!pids[@]}"; do
  if ! wait "${pids[$i]}"; then
    echo "FAILED: ${names[$i]} (pid ${pids[$i]})" >&2
    fail=1
  else
    echo "OK: ${names[$i]}"
  fi
done

echo "finished: $(date -Iseconds)"
if [[ "$fail" -ne 0 ]]; then
  exit 1
fi
echo "All 6 breseq jobs finished successfully."