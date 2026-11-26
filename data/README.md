# Data (not stored in this Git repository)

This folder only contains **accession manifests**. Large files stay on disk locally or in public archives.

## Clone subset (six isolates)

| Clone | SRA run | Layout |
|-------|---------|--------|
| 2K-A | SRR030253 | paired |
| 10K-A | SRR030255 | paired |
| 20K-A | SRR030257 | paired |
| 27K-D | ERR051725 | single |
| 40K-A | SRR030258 | paired |
| 40K-B | ERR051717 | single |

Details: `SUBSET_MANIFEST.csv`, `CLONE_MANIFEST.csv`.

## Download pointers

- **Reads:** https://www.ncbi.nlm.nih.gov/bioproject/PRJNA18281  
- **Reference:** https://www.ncbi.nlm.nih.gov/nuccore/NC_012967.1  

```bash
curl -fsS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_012967&rettype=fasta&retmode=text" \
  -o data/reference/REL606_NC_012967.fasta
```

- **Published SNV tables:** https://doi.org/10.5061/dryad.hb3b5 → extract GVF files to `data/dryad/extracted/gvf/`