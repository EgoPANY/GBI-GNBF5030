# Figure files

Matplotlib defaults: Times New Roman (`scripts/plot_style.py`).

| Figure | File |
|--------|------|
| 1 | `results/figures/fig1_snp_burden_dryad_vs_breseq.png` |
| 2 | `results/figures/fig2_snp_count_by_clone.png` |
| 3 | `results/figures/fig3_dryad_recall_by_clone.png` |

Regenerate (requires local breseq outputs and Dryad GVF):

```bash
python3 scripts/summarize_breseq_results.py
python3 scripts/compare_dryad_breseq.py
```