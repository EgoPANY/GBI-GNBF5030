# Scripts

| Script | Role |
|--------|------|
| `organize_ncbi_downloads.py` | Sort uploads into per-clone folders; split interleaved PE |
| `split_interleaved_fastq.py` | Manual interleaved FASTQ split |
| `resolve_runs.py` | Extended run list helper |
| `download_all_fastq.py` | ENA FTP helper (optional; not default) |
| `run_breseq_subset.sh` | Serial breseq (6 clones) |
| `run_breseq_subset_parallel.sh` | Parallel breseq (**default** for full re-run) |
| `summarize_breseq_results.py` | `output.gd` → `results/analysis/breseq_summary.csv` + plots |
| `compare_dryad_breseq.py` | Dryad GVF vs breseq overlap + figures |
| `plot_style.py` | Matplotlib Times New Roman defaults |

Activate a conda environment with **breseq 0.40.2** before shell drivers. All paths are relative to the repository root.