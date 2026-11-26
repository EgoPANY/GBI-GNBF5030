#!/usr/bin/env python3
"""Resolve sample_accession -> run_accession via ENA filereport API."""
from __future__ import annotations

import csv
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "CLONE_MANIFEST.csv"
OUT = ROOT / "data" / "RUN_MANIFEST.csv"


def filereport(sample: str) -> tuple[str, str]:
    url = (
        "https://www.ebi.ac.uk/ena/portal/api/filereport?"
        f"accession={sample}&result=read_run"
        "&fields=run_accession,library_layout,fastq_bytes"
    )
    with urllib.request.urlopen(url, timeout=60) as r:
        lines = r.read().decode().strip().split("\n")
    if len(lines) < 2:
        return "", ""
    parts = lines[1].split("\t")
    return parts[0], parts[1] if len(parts) > 1 else ""


def main() -> None:
    rows_out = []
    with MANIFEST.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            run, layout = filereport(row["sample_accession"])
            rows_out.append({**row, "run_accession": run, "library_layout": layout})
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows_out[0].keys())
        w.writeheader()
        w.writerows(rows_out)
    print(f"Wrote {OUT} ({len(rows_out)} runs)")


if __name__ == "__main__":
    main()