# Pipeline overview (GBI-GNBF5030)

Technical summary for reproducibility. Full course report is not hosted here.

**Code:** https://github.com/EgoPANY/GBI-GNBF5030

## Abstract

In the *Escherichia coli* long-term evolution experiment, one lineage evolved a mutT hypermutator state and later mutY compensatory alleles on independent branches, reflecting the trade-off between mutational supply and genetic load in evolving populations. Public Illumina reads and Dryad genome-variation tables from a prior twenty-two-clone resequencing study make it possible to test whether clone-level variant lists can be recovered without new wet-lab work. We reanalyzed six clones, 2K-A, 10K-A, 20K-A, 27K-D, 40K-A, and 40K-B, covering non-mutator time points, mutT hypermutation, and distinct mutY-E and mutY-L compensation. Paired-end and single-end reads from the Sequence Read Archive were prepared for analysis, including split of interleaved mate files where required, checked with FastQC, and mapped to REL606 with breseq 0.40.2. Consensus single-nucleotide variants were matched to published Dryad SNV entries by chromosomal position and alternate allele. Mapping fractions ranged from about 87% to 99%, with lower rates for legacy 36 bp libraries than for deeper single-end runs. SNP counts increased with evolutionary time in non-mutators, rose sharply in the mutT isolate, and remained high in late mutY backgrounds, in qualitative agreement with published burdens. Focal mutT and mutY loci matched the expected presence–absence staging in every clone. Dryad SNV recall reached 100% for early clones and for 27K-D aside from two breseq-only SNPs, and 99.84–99.88% for 40K-A and 40K-B with no allele mismatches at shared positions. These findings show that archived LTEE short reads processed with current breseq defaults can largely reproduce published SNV catalogues and the staged mutT–mutY architecture.

## Keywords

long-term evolution experiment; single-nucleotide variant; mutation; LTEE; mutT–mutY architecture

## Methods

### Evolved clones and study design

We analyzed six clonal isolates from the LTEE population studied by Wielgoss et al. (2013), chosen to capture non-mutator time points (2K-A, 10K-A, and 20K-A at 2,000, 10,000, and 20,000 generations, respectively), a mutT-associated hypermutator (27K-D), and late mutT backgrounds carrying distinct mutY alleles (40K-A, mutY-E; 40K-B, mutY-L at 40,000 generations). Strain identifiers follow Wielgoss et al. (2013) nomenclature (REL1164A, REL4536A, REL8593A, REL11395, REL10938, and REL10939).

### Sequence data and reference genome

Paired- and single-end Illumina reads were retrieved from the NCBI Sequence Read Archive under BioProject [PRJNA18281](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA18281) (Table 1). The haploid reference was the *Escherichia coli* B strain REL606 chromosome (RefSeq [NC_012967.1](https://www.ncbi.nlm.nih.gov/nuccore/NC_012967.1), assembly [GCF_000017985.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000017985.1); 4,629,812 bp), consistent with Wielgoss et al. (2013) and Jeong et al. (2009).

### Read file preparation

SRA Run Browser downloads for paired-end libraries often arrive as single interleaved FASTQ archives rather than as standard forward and reverse mate files. Python utilities assign reads to clone-specific directories and, where required, split interleaved records into forward and reverse mates. Single-end runs (27K-D, 40K-B) are placed in the corresponding clone folders without mate splitting. This step is required before FastQC and breseq can consume the data in paired- or single-end layouts.

### Read quality control

Per-run FastQC v0.13.0 reports document base-call quality, read length, and adapter content. Libraries are predominantly 36 bp Illumina reads from early high-throughput platforms. QC summaries contextualize mapping rates; reads were not trimmed beyond breseq’s internal processing.

### Variant calling

Variants relative to REL606 were identified with breseq v0.40.2 (Deatherage & Barrick, 2014). Reads were processed with breseq’s default quality filters; breseq invoked Bowtie2 v2.5.5 (bundled with the bioconda breseq build) to map reads before calling differences. Paired-end libraries (2K-A, 10K-A, 20K-A, 40K-A) used both mate files; single-end libraries (27K-D, 40K-B) used one FASTQ per clone. Six independent breseq runs were executed in parallel (`breseq -j 15` per clone). Primary outputs are genome difference files (`output.gd`) and HTML inspection reports.

### Summaries and comparison to the published call set

Consensus single-nucleotide variants were enumerated from each `output.gd` by counting distinct SNP records and consensus replacement alleles at frequency 1. Mapped and input read totals were taken from breseq metadata. Indels and other event classes (DEL, INS, MOB, JC) were tallied for burden tables.

Published SNV positions and alternate alleles for the same six clones were taken from the Wielgoss et al. (2013) deposit on Dryad ([10.5061/dryad.hb3b5](https://doi.org/10.5061/dryad.hb3b5); landing page [datadryad dataset record](https://datadryad.org/stash/dataset/doi:10.5061/dryad.hb3b5)). The archive does not contain raw FASTQ; the variation bundle provides breseq-style GVF files used as the published SNV comparator. breseq SNP calls were matched to Dryad SNV entries by chromosomal position and alternate nucleotide. Per clone we report shared SNVs, Dryad-only and breseq-only SNPs, and recall (fraction of Dryad SNV positions recovered). Focal mutT/mutY lesions near positions 114034, 2,988,792, and 2,989,164 were inspected in breseq output but excluded from SNV overlap denominators when absent from GVF SNV rows.

### Compute environment (hardware)

Primary analyses were run on a **Linux** shared compute host (November 2025) with the following resources:

| Resource | Specification | Used in this project |
|----------|---------------|----------------------|
| CPU | 90 logical processors (`nproc` = 90) | Yes: six concurrent `breseq` jobs, 15 worker threads per clone (`breseq -j 15`, ~90 threads total) |
| System memory | ~850 GiB installed | Yes: sufficient for six parallel breseq runs |
| GPU | 2 × NVIDIA H20 | **No**: breseq, Bowtie2, and FastQC in this workflow are CPU-only |
| Storage | Network-attached workspace | FASTQ staging, breseq output trees, and summary CSVs |

**FastQC** was run with `-t 2` per input file (low thread count; QC is lightweight compared with alignment). **Python 3** tabulation and plotting used a single process per script on the same host.

Replication on a laptop or smaller VM is possible but wall-clock time for breseq will scale with available CPU cores; GPU is not required.

### Software environment and code availability

Analyses used conda with breseq 0.40.2, Bowtie2 2.5.5, and FastQC 0.13.0 (Bioconda). Tabulation and overlap figures were produced with Python 3 scripts in this repository: https://github.com/EgoPANY/GBI-GNBF5030

### Data sources for reproduction (Table 1)

Table 1 lists six SRA runs and the REL606 reference. Comparator GVF tables are a separate Dryad download (see above).

**Table 1.** Primary download sources for sequencing reads and reference genome.

| Material | Clone | Accession | Source |
|----------|-------|-----------|--------|
| Illumina FASTQ | 2K-A | SRR030253 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030253&display=download |
| Illumina FASTQ | 10K-A | SRR030255 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030255&display=download |
| Illumina FASTQ | 20K-A | SRR030257 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030257&display=download |
| Illumina FASTQ | 27K-D | ERR051725 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=ERR051725&display=download |
| Illumina FASTQ | 40K-A | SRR030258 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030258&display=download |
| Illumina FASTQ | 40K-B | ERR051717 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=ERR051717&display=download |
| REL606 reference FASTA | Ancestor | NC_012967.1 | https://www.ncbi.nlm.nih.gov/nuccore/NC_012967.1 or efetch: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_012967&rettype=fasta&retmode=text |

BioProject for all six runs: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA18281