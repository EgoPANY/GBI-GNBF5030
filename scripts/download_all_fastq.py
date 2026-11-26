#!/usr/bin/env python3
"""Download all 22 Wielgoss clones from ENA FTP (optional; often fails on NAS).

Preferred workflow: local NCBI download + upload — see docs/PROTOCOL_01_DOWNLOAD.md.
Course subset: data/SUBSET_MANIFEST.csv (6 clones).
"""

from __future__ import annotations

import csv
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "CLONE_MANIFEST.csv"
RAW = ROOT / "data" / "raw_fastq"
LOG = ROOT / "logs" / "download_fastq.log"
RESOLVED = ROOT / "data" / "RUN_MANIFEST.csv"


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def ena_filereport(sample_accession: str) -> list[dict]:
    url = (
        "https://www.ebi.ac.uk/ena/portal/api/filereport?"
        f"accession={sample_accession}&result=read_run"
        "&fields=run_accession,fastq_ftp,fastq_bytes,fastq_md5"
    )
    with urllib.request.urlopen(url, timeout=60) as r:
        text = r.read().decode()
    lines = [ln for ln in text.strip().split("\n") if ln]
    if len(lines) < 2:
        return []
    headers = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        parts = ln.split("\t")
        rows.append(dict(zip(headers, parts)))
    return rows


def wget(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size > 0:
        log(f"SKIP exists {dest.name} ({dest.stat().st_size} bytes)")
        return
    log(f"GET {url} -> {dest}")
    subprocess.run(
        ["wget", "-q", "--show-progress", "-O", str(dest), url],
        check=True,
    )


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    resolved_rows: list[dict] = []

    with MANIFEST.open(encoding="utf-8") as f:
        clones = list(csv.DictReader(f))

    for row in clones:
        clone = row["clone"]
        sample = row["sample_accession"]
        log(f"--- {clone} sample={sample} ---")
        fr = ena_filereport(sample)
        if not clone:
            continue
        if not fr:
            log(f"ERROR no ENA filereport for {sample}")
            return 1
        for i, run in enumerate(fr):
            run_acc = run["run_accession"]
            ftps = [u for u in run.get("fastq_ftp", "").split(";") if u]
            bytes_parts = [int(x) for x in run.get("fastq_bytes", "").split(";") if x.isdigit()]
            for j, ftp_path in enumerate(ftps):
                url = f"ftp://{ftp_path}"
                fname = Path(ftp_path).name
                dest = RAW / clone / fname
                wget(url, dest)
                resolved_rows.append(
                    {
                        "clone": clone,
                        "strain_id": row["strain_id"],
                        "sample_accession": sample,
                        "run_accession": run_acc,
                        "fastq_file": str(dest.relative_to(ROOT)),
                        "fastq_bytes": bytes_parts[j] if j < len(bytes_parts) else "",
                        "mutator_bg": row["mutator_bg"],
                    }
                )

    with RESOLVED.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=resolved_rows[0].keys())
        w.writeheader()
        w.writerows(resolved_rows)
    log(f"Wrote {RESOLVED}")
    total = sum(
        p.stat().st_size for p in RAW.rglob("*.fastq.gz") if p.is_file()
    )
    log(f"Done. Total on disk: {total / 1e9:.2f} GB under {RAW}")
    return 0


if __name__ == "__main__":
    sys.exit(main())