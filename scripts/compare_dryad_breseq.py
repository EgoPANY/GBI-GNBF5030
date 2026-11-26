#!/usr/bin/env python3
"""Dryad GVF (published SNV) vs this project breseq output.gd — overlap + burden figure."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GVF_DIR = ROOT / "data" / "dryad" / "extracted" / "gvf"
BRESEQ = ROOT / "results" / "breseq"
OUT = ROOT / "results" / "analysis"
FIG_DIR = ROOT / "results" / "figures"

CLONES: list[tuple[str, str]] = [
    ("2K-A", "02K-A_REL1164A.gvf"),
    ("10K-A", "10K-A_REL4536A.gvf"),
    ("20K-A", "20K-A_REL8593A.gvf"),
    ("27K-D", "27K-D_REL11395.gvf"),
    ("40K-A", "40K-A_REL10938.gvf"),
    ("40K-B", "40K-B_REL10939.gvf"),
]


def parse_dryad_snv(gvf_path: Path) -> dict[int, str]:
    """position -> variant allele (single nucleotide)."""
    out: dict[int, str] = {}
    for line in gvf_path.read_text(errors="replace").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 9 or parts[2] != "SNV":
            continue
        pos = int(parts[3])
        attrs = parts[8]
        m = re.search(r"Variant_seq=([^;]+)", attrs)
        if not m:
            continue
        out[pos] = m.group(1).strip()
    return out


def parse_breseq_snp(gd_path: Path) -> dict[int, str]:
    """Consensus SNP rows from output.gd (SNP type lines)."""
    out: dict[int, str] = {}
    for line in gd_path.read_text(errors="replace").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if parts[0] != "SNP" or len(parts) < 6:
            continue
        pos = int(parts[4])
        out[pos] = parts[5].strip()
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict] = []
    detail_rows: list[dict] = []

    for clone, gvf_name in CLONES:
        gvf = GVF_DIR / gvf_name
        gd = BRESEQ / clone / "output" / "output.gd"
        if not gvf.is_file() or not gd.is_file():
            raise SystemExit(f"missing inputs: {gvf} or {gd}")

        dryad = parse_dryad_snv(gvf)
        ours = parse_breseq_snp(gd)
        dryad_pos = set(dryad)
        our_pos = set(ours)
        shared = dryad_pos & our_pos
        dryad_only = dryad_pos - our_pos
        our_only = our_pos - dryad_pos

        match_allele = 0
        mismatch_allele = 0
        for p in shared:
            if dryad[p].upper() == ours[p].upper():
                match_allele += 1
                detail_rows.append(
                    {
                        "clone": clone,
                        "position": p,
                        "status": "match",
                        "dryad_allele": dryad[p],
                        "breseq_allele": ours[p],
                    }
                )
            else:
                mismatch_allele += 1
                detail_rows.append(
                    {
                        "clone": clone,
                        "position": p,
                        "status": "mismatch_allele",
                        "dryad_allele": dryad[p],
                        "breseq_allele": ours[p],
                    }
                )
        for p in sorted(dryad_only):
            detail_rows.append(
                {
                    "clone": clone,
                    "position": p,
                    "status": "dryad_only",
                    "dryad_allele": dryad[p],
                    "breseq_allele": "",
                }
            )
        for p in sorted(our_only):
            detail_rows.append(
                {
                    "clone": clone,
                    "position": p,
                    "status": "breseq_only",
                    "dryad_allele": "",
                    "breseq_allele": ours[p],
                }
            )

        n_d = len(dryad)
        overlap_pct = 100.0 * len(shared) / n_d if n_d else 0.0
        summary_rows.append(
            {
                "clone": clone,
                "dryad_snv": n_d,
                "breseq_snp": len(ours),
                "shared_positions": len(shared),
                "allele_match": match_allele,
                "allele_mismatch": mismatch_allele,
                "dryad_only": len(dryad_only),
                "breseq_only": len(our_only),
                "recall_vs_dryad_pct": f"{overlap_pct:.2f}",
            }
        )

    summary_path = OUT / "dryad_breseq_overlap_summary.csv"
    detail_path = OUT / "dryad_breseq_overlap_detail.csv"
    with summary_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)
    with detail_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(detail_rows[0].keys()))
        w.writeheader()
        w.writerows(detail_rows)

    # Follow-on analysis (one figure): published vs replicate SNV burden (Fig. 1B style)
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        from plot_style import apply_report_style

        apply_report_style()

        labels = [r["clone"] for r in summary_rows]
        dryad_n = [int(r["dryad_snv"]) for r in summary_rows]
        breseq_n = [int(r["breseq_snp"]) for r in summary_rows]
        recall = [float(r["recall_vs_dryad_pct"]) for r in summary_rows]
        x = np.arange(len(labels))
        w = 0.36
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(x - w / 2, dryad_n, w, label="Dryad GVF (published SNV)", color="#4C72B0")
        ax.bar(x + w / 2, breseq_n, w, label="This study breseq SNP", color="#DD8452")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel("SNV / SNP count")
        ax.legend(loc="upper left")
        fig.tight_layout()
        fig_path = FIG_DIR / "fig1_snp_burden_dryad_vs_breseq.png"
        fig.savefig(fig_path, dpi=150)
        plt.close(fig)
        fig.savefig(OUT / "fig1_snp_burden_dryad_vs_breseq.png", dpi=150)

        fig2, ax2 = plt.subplots(figsize=(7, 4))
        ax2.bar(labels, recall, color="#55A868")
        ax2.set_ylim(99, 100.05)
        ax2.set_ylabel("Recall vs Dryad SNV positions (%)")
        ax2.set_xlabel("Clone")
        fig2.tight_layout()
        recall_path = FIG_DIR / "fig3_dryad_recall_by_clone.png"
        fig2.savefig(recall_path, dpi=150)
        plt.close(fig2)
        print(f"Wrote {fig_path}")
        print(f"Wrote {recall_path}")
    except ImportError:
        pass

    print(f"Wrote {summary_path}")
    print(f"Wrote {detail_path}")
    for r in summary_rows:
        print(
            f"{r['clone']}: dryad={r['dryad_snv']} breseq={r['breseq_snp']} "
            f"shared={r['shared_positions']} recall={r['recall_vs_dryad_pct']}%"
        )


if __name__ == "__main__":
    main()