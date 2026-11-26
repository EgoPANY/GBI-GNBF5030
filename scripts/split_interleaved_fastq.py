#!/usr/bin/env python3
"""Split interleaved paired FASTQ (.fastq.gz) into _1 and _2 gzip outputs."""

from __future__ import annotations

import argparse
import gzip
import sys
from pathlib import Path


def split_interleaved(in_path: Path, out1: Path, out2: Path) -> tuple[int, int]:
    n1 = n2 = 0
    with gzip.open(in_path, "rt") as fin, gzip.open(out1, "wt", compresslevel=6) as f1, gzip.open(
        out2, "wt", compresslevel=6
    ) as f2:
        toggle = True
        while True:
            lines = [fin.readline() for _ in range(4)]
            if not lines[0]:
                break
            if not all(lines):
                raise ValueError("truncated FASTQ record")
            if toggle:
                f1.writelines(lines)
                n1 += 1
            else:
                f2.writelines(lines)
                n2 += 1
            toggle = not toggle
            if (n1 + n2) % 500_000 == 0:
                print(f"... {n1} + {n2}", file=sys.stderr)
    return n1, n2


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("-1", "--read1", type=Path, required=True)
    p.add_argument("-2", "--read2", type=Path, required=True)
    args = p.parse_args()
    n1, n2 = split_interleaved(args.input, args.read1, args.read2)
    print(f"Wrote {args.read1} ({n1} reads)")
    print(f"Wrote {args.read2} ({n2} reads)")
    if n1 != n2:
        raise SystemExit(f"ERROR: read count mismatch {n1} vs {n2}")


if __name__ == "__main__":
    main()