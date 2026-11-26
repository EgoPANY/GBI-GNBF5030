#!/usr/bin/env python3
"""Move NCBI Run Browser FASTQ uploads into per-clone dirs; split interleaved PAIRED runs.

See docs/PROTOCOL_01_DOWNLOAD.md. Run from project root after uploading .fastq.gz files
into data/raw_fastq/_staging/ (or any single bulk folder).
"""

from __future__ import annotations

import csv
import gzip
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_fastq"
SUBSET = ROOT / "data" / "SUBSET_MANIFEST.csv"
STAGING = RAW / "_staging"

RUN_RE = re.compile(r"^(SRR\d+|ERR\d+)(?:[._].*)?\.fastq\.gz$", re.I)


def ena_read_count(run: str) -> int | None:
    import urllib.request

    url = (
        "https://www.ebi.ac.uk/ena/portal/api/filereport?"
        f"accession={run}&result=read_run&fields=read_count,library_layout"
    )
    with urllib.request.urlopen(url, timeout=60) as r:
        lines = r.read().decode().strip().split("\n")
    if len(lines) < 2:
        return None
    h = lines[0].split("\t")
    v = lines[1].split("\t")
    row = dict(zip(h, v))
    return int(row["read_count"]), row["library_layout"]


def count_records(path: Path) -> int:
    n = 0
    with gzip.open(path, "rt") as f:
        for line in f:
            if line.startswith("@"):
                n += 1
    return n


def split_interleaved(src: Path, out1: Path, out2: Path) -> tuple[int, int]:
    n1 = n2 = 0
    out1.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(src, "rt") as fin, gzip.open(out1, "wt", compresslevel=6) as f1, gzip.open(
        out2, "wt", compresslevel=6
    ) as f2:
        toggle = True
        while True:
            lines = [fin.readline() for _ in range(4)]
            if not lines[0]:
                break
            if not all(lines):
                raise ValueError(f"truncated FASTQ in {src}")
            if toggle:
                f1.writelines(lines)
                n1 += 1
            else:
                f2.writelines(lines)
                n2 += 1
            toggle = not toggle
    return n1, n2


def run_id_from_name(name: str) -> str | None:
    m = RUN_RE.match(name)
    if not m:
        return None
    base = m.group(1).upper()
    if "_1." in name or "_2." in name:
        return base
    return base


def load_clone_map() -> dict[str, str]:
    out: dict[str, str] = {}
    with SUBSET.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["run_accession"].upper()] = row["clone"]
    return out


def discover_gz_files() -> list[Path]:
    files: list[Path] = []
    for d in [STAGING, RAW / "2K-A", RAW]:
        if not d.is_dir():
            continue
        for p in d.glob("*.fastq.gz"):
            files.append(p)
    # dedupe paths
    return sorted(set(files))


def main() -> None:
    clone_by_run = load_clone_map()
    files = discover_gz_files()
    if not files:
        print("No .fastq.gz in _staging or raw_fastq", file=sys.stderr)
        sys.exit(1)

    processed: list[str] = []
    for src in files:
        name = src.name
        if "_1.fastq.gz" in name or "_2.fastq.gz" in name:
            run = run_id_from_name(name)
            if not run:
                continue
            clone = clone_by_run.get(run)
            if not clone:
                print(f"SKIP unknown run in name: {name}")
                continue
            dest_dir = RAW / clone
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / name
            if src.resolve() != dest.resolve():
                shutil.move(str(src), str(dest))
            processed.append(f"{clone}: kept {name}")
            continue

        run = run_id_from_name(name)
        if not run or run not in clone_by_run:
            print(f"SKIP {name}")
            continue
        clone = clone_by_run[run]
        dest_dir = RAW / clone
        dest_dir.mkdir(parents=True, exist_ok=True)

        meta = ena_read_count(run)
        if meta is None:
            print(f"WARN no ENA meta for {run}")
            n_records = count_records(src)
            layout = "UNKNOWN"
            spot = n_records
        else:
            spot, layout = meta
            n_records = count_records(src)

        if layout == "PAIRED" and n_records == 2 * spot:
            out1 = dest_dir / f"{run}_1.fastq.gz"
            out2 = dest_dir / f"{run}_2.fastq.gz"
            print(f"SPLIT {name} -> {clone}/ (interleaved {n_records} -> 2x{spot})")
            n1, n2 = split_interleaved(src, out1, out2)
            if n1 != n2 or n1 != spot:
                raise SystemExit(f"split mismatch {run}: {n1}+{n2} vs ENA {spot}")
            src.unlink()
            processed.append(f"{clone}: split {run} -> _1/_2 ({n1} reads each)")
        elif layout == "SINGLE" and n_records == spot:
            dest = dest_dir / f"{run}.fastq.gz"
            if src.resolve() != dest.resolve():
                shutil.move(str(src), str(dest))
            else:
                pass
            processed.append(f"{clone}: single {run}.fastq.gz ({n_records} reads)")
        else:
            raise SystemExit(
                f"Unhandled {name}: layout={layout} records={n_records} ENA spot={spot} "
                "(see PROTOCOL §5–6)"
            )

    print("---")
    for line in processed:
        print(line)
    print(f"Done. {len(processed)} file groups.")


if __name__ == "__main__":
    main()