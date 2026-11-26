# GBI-GNBF5030 · LTEE mutT–mutY SNV reanalysis

Reanalysis of six public Illumina clones from the *Escherichia coli* long-term evolution experiment (LTEE), with **breseq** calls against REL606 and comparison to published Dryad GVF SNV tables (Wielgoss et al., PNAS 2013).

This repository contains **code**, **small result tables**, and **report figures**. It does **not** ship raw FASTQ, reference FASTA, Dryad archives, or full breseq output trees (use public downloads; see `docs/REPRODUCIBILITY.md`).

## Quick start

```bash
git clone <YOUR_REPO_URL>
cd <repo>
conda create -n ltee-breseq -c bioconda -c conda-forge -y breseq=0.40.2 bowtie2 fastqc
conda activate ltee-breseq
```

After you place data locally (see `data/README.md`):

```bash
# ... run breseq per docs/REPRODUCIBILITY.md ...
python3 scripts/summarize_breseq_results.py
python3 scripts/compare_dryad_breseq.py
```

Precomputed summary CSVs and figures matching the course report are under `results/`.

## Layout

| Path | Purpose |
|------|---------|
| `docs/REPORT.md` | Report manuscript (Markdown) |
| `docs/REPRODUCIBILITY.md` | Data sources and pipeline order |
| `scripts/` | Download helpers, breseq drivers, analysis |
| `data/*.csv` | Six-clone SRA accession manifest |
| `results/analysis/` | Tables for report |
| `results/figures/` | Figures 1–3 |

See `GITHUB_CONTENTS.md` for include/exclude policy.

## Citation

Wielgoss, S., et al. (2013). Mutation rate dynamics in a bacterial population reflect tension between adaptation and genetic load. *PNAS*, *110*(1), 222–227. https://doi.org/10.1073/pnas.1219574110
