#!/usr/bin/env bash
# Run breseq for all 6 clones in SUBSET_MANIFEST. Requires gnbf5030 on PATH.
set -euo pipefail

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

run_paired() {
  local clone=$1
  local out="results/breseq/${clone}"
  local r1 r2
  r1="$(find "data/raw_fastq/${clone}" -name '*_1.fastq.gz' | head -1)"
  r2="$(find "data/raw_fastq/${clone}" -name '*_2.fastq.gz' | head -1)"
  [[ -f "$r1" && -f "$r2" ]] || { echo "SKIP $clone: missing pairs"; return 1; }
  mkdir -p "$out"
  echo "=== breseq PAIRED $clone ==="
  breseq -j 2 -r "$REF" -o "$out" -n "$clone" "$r1" "$r2" 2>&1 | tee "logs/breseq_${clone}.log"
}

run_single() {
  local clone=$1 fq=$2
  local out="results/breseq/${clone}"
  [[ -f "$fq" ]] || { echo "SKIP $clone: $fq"; return 1; }
  mkdir -p "$out"
  echo "=== breseq SINGLE $clone ==="
  breseq -j 2 -r "$REF" -o "$out" -n "$clone" "$fq" 2>&1 | tee "logs/breseq_${clone}.log"
}

breseq --version

run_paired 2K-A
run_paired 10K-A
run_paired 20K-A
run_single 27K-D data/raw_fastq/27K-D/ERR051725.fastq.gz
run_paired 40K-A
run_single 40K-B data/raw_fastq/40K-B/ERR051717.fastq.gz

echo "All breseq jobs finished."