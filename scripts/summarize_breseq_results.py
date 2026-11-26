#!/usr/bin/env python3
"""Summarize breseq output.gd across 6-clone subset; write CSV + optional bar chart."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRESEQ = ROOT / "results" / "breseq"
OUT_DIR = ROOT / "results" / "analysis"
FIG_DIR = ROOT / "results" / "figures"
MANIFEST = ROOT / "data" / "SUBSET_MANIFEST.csv"

# Wielgoss PNAS 2013 / follow-up (REL606 NC_012967.1 coordinates)
PAPER_LOCI = {
    "mutT_frameshift_114034": 114034,
    "mutY_L40W": 2_988_792,
    "mutY_L164_stop": 2_989_164,
}

CLONE_ORDER = ["2K-A", "10K-A", "20K-A", "27K-D", "40K-A", "40K-B"]


def load_manifest() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with MANIFEST.open(newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["clone"]] = row
    return out


def parse_meta(lines: list[str]) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in lines:
        if not line.startswith("#="):
            break
        key, _, val = line[2:].partition("\t")
        meta[key] = val
    return meta


def parse_gd(path: Path) -> tuple[dict[str, str], Counter[str], set[int]]:
    text = path.read_text(errors="replace").splitlines()
    meta = parse_meta(text)
    types = Counter()
    consensus_positions: set[int] = set()
    for line in text:
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        kind = parts[0]
        if kind in {"SNP", "DEL", "INS", "MOB", "JC", "MC", "UN", "RA"}:
            types[kind] += 1
        if kind == "SNP":
            try:
                consensus_positions.add(int(parts[4]))
            except (IndexError, ValueError):
                pass
        if kind == "RA" and "prediction=consensus" in line and "\tfrequency=1\t" in line:
            try:
                consensus_positions.add(int(parts[4]))
            except (IndexError, ValueError):
                pass
    return meta, types, consensus_positions


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    rows: list[dict] = []
    locus_rows: list[dict] = []

    for clone in CLONE_ORDER:
        gd = BRESEQ / clone / "output" / "output.gd"
        if not gd.is_file():
            raise SystemExit(f"missing {gd}")
        meta, types, positions = parse_gd(gd)
        mapped = meta.get("MAPPED-READS", "")
        input_reads = meta.get("INPUT-READS", "")
        snp = types.get("SNP", 0)
        row = {
            "clone": clone,
            "strain_id": manifest[clone].get("strain_id", ""),
            "mutator_bg": manifest[clone].get("mutator_bg", ""),
            "input_reads": input_reads,
            "mapped_reads": mapped,
            "map_fraction": f"{float(mapped) / float(input_reads):.4f}" if mapped and input_reads else "",
            "consensus_snp_calls": snp,
            "del": types.get("DEL", 0),
            "ins": types.get("INS", 0),
            "mob": types.get("MOB", 0),
            "jc": types.get("JC", 0),
            "mc": types.get("MC", 0),
            "ra_rows": types.get("RA", 0),
        }
        rows.append(row)
        for name, pos in PAPER_LOCI.items():
            locus_rows.append(
                {
                    "clone": clone,
                    "locus": name,
                    "position": pos,
                    "called_in_breseq": "yes" if pos in positions else "no",
                }
            )

    summary_path = OUT_DIR / "breseq_summary.csv"
    with summary_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    locus_path = OUT_DIR / "paper_locus_presence.csv"
    with locus_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(locus_rows[0].keys()))
        w.writeheader()
        w.writerows(locus_rows)

    # Simple bar chart without extra deps (matplotlib in conda env)
    try:
        import matplotlib.pyplot as plt

        from plot_style import apply_report_style

        apply_report_style()

        labels = [r["clone"] for r in rows]
        counts = [int(r["consensus_snp_calls"]) for r in rows]
        colors = ["#4C72B0" if "mutT" not in r["mutator_bg"] else "#C44E52" for r in rows]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(labels, counts, color=colors)
        ax.set_ylabel("Consensus SNP count")
        ax.set_xlabel("Clone")
        fig.tight_layout()
        fig.savefig(OUT_DIR / "fig2_snp_count_by_clone.png", dpi=150)
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIG_DIR / "fig2_snp_count_by_clone.png", dpi=150)
        plt.close(fig)
    except ImportError:
        pass

    print(f"Wrote {summary_path}")
    print(f"Wrote {locus_path}")
    if (OUT_DIR / "fig2_snp_count_by_clone.png").exists():
        print(f"Wrote {OUT_DIR / 'fig2_snp_count_by_clone.png'}")


if __name__ == "__main__":
    main()