# Reproducibility

## Data to obtain locally

1. **Six SRA runs** — see `data/SUBSET_MANIFEST.csv` (BioProject [PRJNA18281](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA18281)).  
   Layout after download: `data/raw_fastq/<clone>/` (paired `_1`/`_2` or single-end `.fastq.gz`).  
   Use `scripts/organize_ncbi_downloads.py` if downloads arrive as interleaved pairs.

2. **Reference** — REL606 `NC_012967.1` FASTA at `data/reference/REL606_NC_012967.fasta`  
   (efetch example in `data/README.md`).

3. **Dryad comparator** — unpack [10.5061/dryad.hb3b5](https://doi.org/10.5061/dryad.hb3b5) so GVF files live under  
   `data/dryad/extracted/gvf/`.

## Software

- **breseq 0.40.2** with **Bowtie2** (bundled in bioconda breseq)  
- **FastQC** 0.13.x (optional QC)  
- **Python 3** + matplotlib for figures  

Example environment:

```bash
conda create -n ltee-breseq -c bioconda -c conda-forge -y breseq=0.40.2 fastqc
conda activate ltee-breseq
```

## Pipeline order

1. Optional: `fastqc` on FASTQ → `results/fastqc/`  
2. `bash scripts/run_breseq_subset_parallel.sh` → `results/breseq/<clone>/output/output.gd`  
3. `python3 scripts/summarize_breseq_results.py`  
4. `python3 scripts/compare_dryad_breseq.py`  

Committed CSVs under `results/analysis/` are snapshots from the author’s run; regenerate to verify.

## Documentation

Pipeline summary: `docs/METHODS.md`. Figure files: `docs/FIGURES.md`.