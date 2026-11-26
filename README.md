# GBI-GNBF5030

Computational reanalysis pipeline for six public LTEE Illumina clones: **breseq** variant calling on REL606, overlap with published Dryad GVF SNV tables (Wielgoss et al., PNAS 2013).

This repository provides **scripts**, **accession manifests**, **summary tables**, and **figures**. Raw FASTQ, reference FASTA, and Dryad archives are obtained from public sources (see `docs/METHODS.md`).

## Contents

| Path | Description |
|------|-------------|
| `docs/METHODS.md` | Abstract, keywords, methods, hardware, download table |
| `docs/REPRODUCIBILITY.md` | End-to-end rerun steps |
| `scripts/` | Download prep, breseq drivers, summarisation |
| `data/*.csv` | Six-clone SRA manifest |
| `results/analysis/` | CSV summaries (Tables 2–4 in report) |
| `results/figures/` | PNG exports |

## Quick start

```bash
conda create -n ltee-breseq -c bioconda -c conda-forge -y breseq=0.40.2 fastqc
conda activate ltee-breseq
```

Download data per `docs/METHODS.md`, then see `docs/REPRODUCIBILITY.md`.

## Primary references

- Wielgoss et al. (2013) https://doi.org/10.1073/pnas.1219574110  
- Dryad variation data https://doi.org/10.5061/dryad.hb3b5  
- Reads BioProject https://www.ncbi.nlm.nih.gov/bioproject/PRJNA18281  