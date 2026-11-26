# Reanalysis of public Illumina reads recapitulates published mutT–mutY SNV calls in six LTEE clones


## Abstract

In the *Escherichia coli* long-term evolution experiment, one lineage evolved a mutT hypermutator state and later mutY compensatory alleles on independent branches, reflecting the trade-off between mutational supply and genetic load in evolving populations. Public Illumina reads and Dryad genome-variation tables from a prior twenty-two-clone resequencing study make it possible to test whether clone-level variant lists can be recovered without new wet-lab work. We reanalyzed six clones—2K-A, 10K-A, 20K-A, 27K-D, 40K-A, and 40K-B—covering non-mutator time points, mutT hypermutation, and distinct mutY-E and mutY-L compensation. Paired-end and single-end reads from the Sequence Read Archive were prepared for analysis, including split of interleaved mate files where required, checked with FastQC, and mapped to REL606 with breseq version 0.40.2. Consensus single-nucleotide variants were matched to published Dryad SNV entries by chromosomal position and alternate allele. Mapping fractions ranged from about 87% to 99%, with lower rates for legacy 36 bp libraries than for deeper single-end runs. SNP counts increased with evolutionary time in non-mutators, rose sharply in the mutT isolate, and remained high in late mutY backgrounds, in qualitative agreement with published burdens. Focal mutT and mutY loci matched the expected presence–absence staging in every clone. Dryad SNV recall reached 100% for early clones and for 27K-D aside from two breseq-only SNPs, and 99.84–99.88% for 40K-A and 40K-B with no allele mismatches at shared positions. These findings show that archived LTEE short reads processed with current breseq defaults can largely reproduce published SNV catalogues and the staged mutT–mutY architecture.

**Keywords:** long-term evolution experiment; breseq; single-nucleotide variant; mutT; mutY

## Introduction

Experimental evolution in microbes makes it possible to observe adaptation and genetic change over a large number of generations under controlled laboratory conditions. The *Escherichia coli* long-term evolution experiment (LTEE), initiated by Lenski and colleagues (Lenski et al., 1991), has become a central model for studying how populations diversify, fix beneficial mutations, and sometimes evolve changes in mutation rate itself. In the LTEE, twelve populations founded from the ancestral strain REL606 have been propagated since 1988, with one population (often labeled Ara-1) providing many of the best-studied examples of parallel evolution and genomic innovation (Lenski et al., 1991; Barrick et al., 2009). Genome resequencing relative to REL606 has made it practical to catalog the precise molecular changes accumulated in evolved clones. Barrick et al. (2009) used high-throughput sequencing to characterize genomic evolution over long LTEE time spans and established a paradigm—later extended to many clones—for comparing evolved genomes to the REL606 reference. Such studies show that most clones carry dozens to hundreds of point mutations and indels, while occasional lineages become mutators with greatly elevated spontaneous mutation rates (Sniegowski et al., 1997).

Hypermutation can accelerate adaptation when many beneficial alleles are available, but it also increases genetic load from deleterious and nearly neutral mutations, creating tension between short-term advantage and long-term fitness (Sniegowski et al., 1997; Lynch, 2010). Wielgoss et al. (2013) examined this tension in an LTEE population by combining phylogenomics of 22 evolved clones with fluctuation tests and mutational spectrum analysis. They reported that a mutT hypermutator state spread in the population, increasing the point-mutation rate by ~150-fold, and was subsequently ameliorated on independent lineages by mutY alleles that act as antimutators in the mutT background. Variant calls and analysis scripts from that work have been released with the original publication, enabling independent replication of clone-level mutation lists (Wielgoss et al., 2013).

In this study, we focus on a six-clone subset spanning non-mutator time points (2K, 10K, 20K generations), a mutT clone (27K-D), and two late clones carrying mutY-E and mutY-L alleles (40K-A and 40K-B). We downloaded public Illumina reads, quality-checked them, called variants with breseq relative to REL606 (Deatherage & Barrick, 2014; Jeong et al., 2009), and compared our consensus single-nucleotide variants to the published gold-standard variant tables from Wielgoss et al. (2013), asking whether our analysis recapitulates the published mutT/mutY dynamics and SNV counts despite legacy short-read lengths. Together, these results provide an independent, sequence-level check of the Wielgoss et al. (2013) mutation-rate narrative and a practical benchmark for re-analyzing archived short-read LTEE data with current variant-calling tools.

## Methods

### Evolved clones and study design

We analyzed six clonal isolates from the LTEE population studied by Wielgoss et al. (2013), chosen to capture non-mutator time points (2K-A, 10K-A, and 20K-A at 2,000, 10,000, and 20,000 generations, respectively), a mutT-associated hypermutator (27K-D), and late mutT backgrounds carrying distinct mutY alleles (40K-A, mutY-E; 40K-B, mutY-L at 40,000 generations). Strain identifiers and evolutionary context follow the Wielgoss et al. (2013) clone nomenclature (REL1164A, REL4536A, REL8593A, REL11395, REL10938, and REL10939).

### Sequence data and reference genome

Paired- and single-end Illumina reads were retrieved from the NCBI Sequence Read Archive under BioProject PRJNA18281 (Table 1). The haploid reference was the *Escherichia coli* B strain REL606 chromosome (RefSeq NC_012967.1, assembly GCF_000017985.1; 4,629,812 bp), obtained from NCBI and used consistently with Wielgoss et al. (2013) and Jeong et al. (2009).

### Read file preparation

SRA Run Browser downloads for several paired-end libraries arrived as single interleaved FASTQ archives rather than as standard `_1` / `_2` mate files. After transfer to the analysis host, we used Python scripts (`organize_ncbi_downloads.py`, including interleaved split utilities) to assign reads to clone-specific directories and, where required, to split interleaved records into forward and reverse mates with consistent naming. Single-end runs (27K-D, 40K-B) were placed in the corresponding clone folders without mate splitting. This step was required before FastQC and breseq could consume the data in the expected paired- or single-end layouts.

### Read quality control

Per-run FastQC v0.13.0 reports were generated for all input FASTQ files to document base-call quality, read length, and adapter content. These data consist predominantly of 36 bp Illumina reads from early high-throughput platforms; QC summaries were used to contextualize mapping rates in downstream calling but reads were not additionally trimmed beyond breseq’s internal processing.

### Variant calling

Variants relative to REL606 were identified with breseq v0.40.2 (Deatherage & Barrick, 2014). For each clone, reads were processed with breseq’s default quality filters; breseq then invoked the **Bowtie2 v2.5.5** alignment software (bundled as part of the breseq pipeline) to map reads to the reference before calling differences. Paired-end libraries (2K-A, 10K-A, 20K-A, 40K-A) were analyzed with both mate files; single-end libraries (27K-D, 40K-B) were analyzed with one FASTQ per clone. Six independent breseq runs were executed in parallel, each with 15 worker threads (`breseq -j 15`). Primary outputs were breseq genome difference files (`output.gd`) and HTML inspection reports.

### Summaries and comparison to the published call set

Consensus single-nucleotide variants were enumerated from each `output.gd` file by counting distinct SNP records and consensus replacement alleles at full frequency (frequency = 1). Total mapped and input reads were extracted from breseq metadata fields for each clone. Indels and other breseq event classes (DEL, INS, MOB, JC) were tallied for descriptive burden tables. 

Published SNV positions and alternate alleles for the same six clones were taken from the Wielgoss et al. (2013) genome variation deposit on Dryad (https://datadryad.org/stash/dataset/doi:10.5061/dryad.hb3b5). This archive does not contain raw FASTQ reads; after download, the nested archive `Wielgossetal_2012_Genome_Variation_Data.zip` provides breseq-style **GVF** files (`gvf/<clone>_REL*.gvf`) used here as the published SNV call set. We compared breseq SNP calls to Dryad SNV entries by matching chromosomal position and alternate nucleotide. For each clone we computed the number of shared SNVs, Dryad-only SNVs, and breseq-only SNPs, and summarized recall as the fraction of Dryad SNV positions recovered in breseq. Structural and indel events (including the mutT frameshift near position 114034 and mutY lesions at positions 2,988,792 and 2,989,164) were inspected in breseq output for concordance with the Wielgoss mutator narrative but were excluded from SNV overlap denominators when they are not represented as SNVs in the published GVF tables.

### Software environment

Analyses used a dedicated conda environment with breseq 0.40.2, Bowtie2 2.5.5, and FastQC 0.13.0 (Bioconda). Post-calling tabulation and Dryad overlap figures were produced with Python 3 scripts; analysis code is available at https://github.com/EgoPANY/GBI-GNBF5030.

### Data sources for reproduction (Table 1)

Table 1 lists the seven primary files retrieved for this study: six SRA runs (Illumina FASTQ) and one REL606 reference sequence. Comparator GVF tables are a separate Dryad download (see *Summaries and comparison* above), not raw sequencing data.

**Table 1.** Primary download sources for sequencing reads and reference genome.

| # | Material | Clone / role | Accession | Source and download |
|---|----------|--------------|-----------|-------------------|
| 1 | Illumina FASTQ | 2K-A | SRR030253 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030253&display=download |
| 2 | Illumina FASTQ | 10K-A | SRR030255 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030255&display=download |
| 3 | Illumina FASTQ | 20K-A | SRR030257 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030257&display=download |
| 4 | Illumina FASTQ | 27K-D | ERR051725 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=ERR051725&display=download |
| 5 | Illumina FASTQ | 40K-A | SRR030258 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR030258&display=download |
| 6 | Illumina FASTQ | 40K-B | ERR051717 | https://www.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=ERR051717&display=download |
| 7 | REL606 reference (FASTA) | Ancestor | NC_012967.1 | https://www.ncbi.nlm.nih.gov/nuccore/NC_012967.1 (or NCBI efetch: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_012967&rettype=fasta&retmode=text`) |

BioProject for all six runs: PRJNA18281 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA18281).

## Results

### Read alignment and variant burden

Across all six clones, a large majority of input reads mapped to REL606 (Table 2). Mapping fractions were ~87–89% for early paired-end libraries (2K-A, 10K-A, 20K-A, 40K-A), consistent with short (36 bp) legacy reads, whereas the deeper single-end runs for 27K-D and 40K-B yielded mapping rates of 98.9% and 97.3%, respectively.

Consensus SNP counts increased with evolutionary time in non-mutator clones (3, 16, and 28 SNPs for 2K-A, 10K-A, and 20K-A), then rose sharply in the mutT clone 27K-D (309 SNPs) and remained elevated in the late mutT/mutY clones 40K-A and 40K-B (624 and 833 SNPs). This stepwise pattern mirrors the qualitative SNP burden reported by Wielgoss et al. (2013) for the same isolates (Figures 1 and 2). The breseq pipeline also reported modest numbers of indels and, in hypermutator clones, many junction (JC) records (Table 2). Wielgoss et al. (2013) emphasize genome-wide SNV phylogeny and fluctuation-test estimates of mutation rate rather than JC counts from short-read resequencing; we therefore treat elevated JC calls in 27K-D as a descriptive feature of our breseq output and as auxiliary evidence for structural/rearrangement events, not as a direct replication of a published JC metric.

**Table 2.** breseq mapping and consensus variant summary per clone.

| Clone | Strain | Background | Input reads | Mapped reads | Map fraction | Consensus SNPs | DEL | INS | JC |
|-------|--------|------------|-------------|--------------|--------------|----------------|-----|-----|-----|
| 2K-A | REL1164A | non-mutator | 7,580,912 | 6,592,355 | 0.870 | 3 | 0 | 1 | 9 |
| 10K-A | REL4536A | non-mutator | 8,297,266 | 7,360,450 | 0.887 | 16 | 2 | 3 | 22 |
| 20K-A | REL8593A | non-mutator | 7,600,360 | 6,731,945 | 0.886 | 28 | 2 | 3 | 29 |
| 27K-D | REL11395 | mutT | 28,776,640 | 28,472,934 | 0.989 | 309 | 4 | 4 | 304 |
| 40K-A | REL10938 | mutT, mutY-E | 8,411,468 | 7,495,036 | 0.891 | 624 | 4 | 5 | 32 |
| 40K-B | REL10939 | mutT, mutY-L | 9,802,636 | 9,535,604 | 0.973 | 833 | 5 | 4 | 158 |

### Mutation-rate loci (mutT and mutY)

The breseq calls identified mutator-associated lesions at the three focal loci only in clones from the mutT-bearing lineage (Table 3). At 2K, 10K, and 20K generations all three loci were absent, which is expected because the mutT hypermutator indel had not yet spread in the population and compensatory mutY alleles had not evolved. In 27K-D, the mutT indel was present but both mutY focal lesions were absent, consistent with the temporal ordering in Wielgoss et al. (2013), in which mutY antimutators arise on independent branches after the mutT state. At 40,000 generations, each late clone carried mutT plus a single mutY allele at the expected position (mutY-E in 40K-A, mutY-L in 40K-B), with the alternate mutY site absent as predicted for allele-specific lineages.

For every clone, the published and reanalyzed states agree at all three focal loci (Table 3). Where both columns read *absent · absent*, that agreement reflects the expected evolutionary stage rather than a failed detection. Conversely, focal-locus agreement is a different dimension from genome-wide SNV overlap (Table 4; see Discussion).

**Table 3.** Focal mutT/mutY lesions in breseq output compared with Wielgoss et al. (2013).

| Clone | mutT indel @ 114034 | mutY @ 2,988,792 (E) | mutY @ 2,989,164 (L) |
|-------|---------------------|----------------------|----------------------|
| 2K-A | absent · absent | absent · absent | absent · absent |
| 10K-A | absent · absent | absent · absent | absent · absent |
| 20K-A | absent · absent | absent · absent | absent · absent |
| 27K-D | present · present | absent · absent | absent · absent |
| 40K-A | present · present | present · present | absent · absent |
| 40K-B | present · present | absent · absent | present · present |

*Table 3 notes.* Each cell lists **this study · published** call status (*present* or *absent*) at the focal coordinate.

### Concordance with published Dryad SNV tables

Position- and allele-matched comparison to the Wielgoss et al. (2013) GVF SNV lists showed near-complete overlap for every clone (Table 4). Early non-mutator clones (2K-A, 10K-A, 20K-A) yielded 100% recall of published SNV positions with identical alternate alleles. Clone 27K-D recovered all 307 Dryad SNV positions; breseq reported two additional SNPs not listed as SNVs in the GVF comparator. Late clones 40K-A and 40K-B each missed one published SNV position while otherwise matching all remaining calls (recall 99.84% and 99.88%, respectively; Figure 3). No allele mismatches were observed at shared positions.

**Table 4.** Dryad GVF SNV overlap with breseq consensus SNPs.

| Clone | Dryad SNVs | breseq SNPs | Shared | Allele matches | Dryad only | breseq only | Recall (%) |
|-------|------------|-------------|--------|----------------|------------|-------------|------------|
| 2K-A | 3 | 3 | 3 | 3 | 0 | 0 | 100.00 |
| 10K-A | 16 | 16 | 16 | 16 | 0 | 0 | 100.00 |
| 20K-A | 28 | 28 | 28 | 28 | 0 | 0 | 100.00 |
| 27K-D | 307 | 309 | 307 | 307 | 0 | 2 | 100.00 |
| 40K-A | 625 | 624 | 624 | 624 | 1 | 0 | 99.84 |
| 40K-B | 834 | 833 | 833 | 833 | 1 | 0 | 99.88 |

**Figure 1.** Comparison of consensus SNP counts from this breseq reanalysis and published SNV counts from Wielgoss et al. (2013) Dryad GVF tables for six LTEE clones. Blue bars, published SNV totals; orange bars, breseq consensus SNPs. Non-mutator clones show gradual accumulation; 27K-D (mutT) shows a large increase; 40K-A and 40K-B remain elevated under mutT with mutY compensation.

**Figure 2.** breseq consensus SNP counts per clone relative to REL606. Blue, non-mutator backgrounds; red, mutT or mutT/mutY backgrounds.

**Figure 3.** Fraction of Dryad GVF SNV positions recovered at identical alleles in breseq output (recall). The y-axis is truncated to 99–100% to resolve small differences among late clones.

## Discussion

We reanalyzed archived Illumina reads with breseq and compared the resulting calls to the published Wielgoss et al. (2013) SNV tables and mutator narrative. At the level of clone-level SNV lists (Table 4; Figures 1 and 3), agreement is strong, but interpreting mutation-rate biology still requires separating what short-read variant calling recovers from what the original study established with phylogenomics, fluctuation tests, and mutational spectra.

Wielgoss et al. (2013) described a mutT hypermutator phase with greatly elevated point-mutation rates and subsequent mutY-mediated rate reduction on independent lineages—the tension between short-term mutational supply and genetic load (Sniegowski et al., 1997; Lynch, 2010). Our SNP burdens, focal mutT/mutY lesions (Table 3), and Dryad concordance are consistent with that account and with the qualitative trends reported in the original paper (Tables 2–4; Figures 1 and 2). Reproducing SNP inventories and focal lesions is nevertheless not the same as reproducing mutation-rate measurements. The authors used fluctuation tests and phylogenetic rate models; we did not repeat those assays. For example, 40K-B carries more consensus SNPs than 40K-A in both Dryad and our breseq output, while the paper reports lower instantaneous mutation rates after mutY compensation relative to the mutT-only state. Cumulative SNPs reflect ancestry since REL606, whereas fluctuation tests estimate current spontaneous mutation. We should therefore weight variant-list and locus-level concordance more heavily than raw SNP totals when comparing late clones.

Table 3 and Table 4 address complementary questions and should be read together. Table 4 matches every published SNV in the Dryad GVF files to breseq SNP rows, whereas Table 3 tracks three nominated loci, including the mutT indel that is outside the GVF SNV catalogue. Early *absent · absent* entries in Table 3 reflect the expected absence of mutT and mutY before the hypermutator sweep, not poor sensitivity at those coordinates. Across all six clones we observed complete or near-complete SNV recall with no allele mismatches at shared sites (Table 4; Figure 3); the few breseq-only or Dryad-only positions are plausibly explained by breseq version, filtering defaults, or coverage at marginal sites rather than by a different mutator architecture.

Read length and library depth also colour the results. Early paired-end libraries map at roughly 87–89% to REL606, while deeper single-end runs for 27K-D and 40K-B exceed 97% (Table 2; Barrick et al., 2009). The data are predominantly 36 bp legacy Illumina reads, so mappability and evidence per site are inherently limited compared with modern datasets. Mate-file preparation from interleaved SRA downloads was required in our pipeline; near-total SNV agreement suggests that step was sound, but preprocessing remains part of reproducible practice (Table 1). breseq separately reports indels and junction (JC) events; the elevated JC count in 27K-D is a feature of our hypermutator output, whereas Wielgoss et al. emphasize SNV phylogeny and spectra in the main text. Short-read junction evidence should be treated cautiously and not equated with the paper’s primary structural conclusions.

Only six of the twenty-two Wielgoss clones were analyzed, and we did not revisit fluctuation tests, synonymous-site dating, or spectrum analysis. Under those constraints, public SRA data processed with documented references and comparators still yield SNV catalogues nearly identical to the Dryad tables and reproduce the staged mutT and mutY lesions expected in LTEE Ara-1. The small residual discrepancies mark the limits of substitution-level recall and of what SNV overlap alone can say about mutation-rate dynamics—quantities that in the original work required functional assays beyond variant calling.

## References

Barrick, J. E., Yu, D. S., Yoon, S. H., Jeong, H., Oh, T. K., Schneider, D., Lenski, R. E., & Kim, J. F. (2009). Genome evolution and adaptation in a long-term experiment with *Escherichia coli*. *Nature*, *461*(7268), 1243–1247. https://doi.org/10.1038/nature08480

Deatherage, D. E., & Barrick, J. E. (2014). Identification of mutations in laboratory-evolved microbes from next-generation sequencing data using breseq. In L. Sun & W. Shou (Eds.), *Engineering and analyzing multicellular systems: Methods and protocols* (pp. 165–188). Humana Press. https://doi.org/10.1007/978-1-4939-0554-6_12

Jeong, H., et al. (2009). Genome sequences of *Escherichia coli* B strains REL606 and BL21(DE3). *Journal of Molecular Biology*, *394*(4), 644–652. https://doi.org/10.1016/j.jmb.2009.09.052

Lenski, R. E., Rose, M. R., Simpson, S. C., & Tadler, T. J. (1991). Long-term experimental evolution in *Escherichia coli*. I. Adaptation and divergence during 2,000 generations. *The American Naturalist*, *138*(6), 1315–1341. https://doi.org/10.1086/285289

Lynch, M. (2010). Evolution of the mutation rate. *Trends in Genetics*, *26*(8), 345–352. https://doi.org/10.1016/j.tig.2010.05.003

Sniegowski, P. D., Gerrish, P. J., & Lenski, R. E. (1997). Evolution of high mutation rates in experimental populations of *E. coli*. *Nature*, *387*(6634), 703–705. https://doi.org/10.1038/42701

Wielgoss, S., Barrick, J. E., Tenaillon, O., Wiser, M. J., Dittmar, W. J., Cruveillier, S., … Schneider, D. (2013). Mutation rate dynamics in a bacterial population reflect tension between adaptation and genetic load. *Proceedings of the National Academy of Sciences*, *110*(1), 222–227. https://doi.org/10.1073/pnas.1219574110