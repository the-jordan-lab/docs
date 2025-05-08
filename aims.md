# Research Aims

## 1. Ybx1 in adipogenesis
### 1.1 Identifying YBX1-CEBPA-cBAF interactions in early, middle, late 3T3-L1 adipogenesis
- **Hypothesis:** YBX1 cooperates with CEBPA and cBAF complex to regulate temporal gene expression during adipogenesis
- **Approach:** Time-course analysis of 3T3-L1 differentiation (days 0, 2, 4, 6, 8)
  - ChIP-seq for YBX1, CEBPA, BRG1, SMARCD2, SMARCE1
  - RNA-seq to correlate binding with expression changes
  - Co-IP followed by MS to identify temporal protein-protein interactions
- **Expected outcomes:** Map dynamic transcriptional networks controlling adipocyte differentiation
- **Question:** Are we seeing this in all cell types?

### 1.2 YBX1 in adipogenic 3T3 metabolism
- **Hypothesis:** YBX1 regulates metabolic reprogramming during adipogenesis
- **Approach:**
  - Metabolic profiling of control vs YBX1-depleted 3T3-L1 cells during differentiation
  - Seahorse analysis of glycolysis and mitochondrial function
  - Lipidomics to characterize changes in lipid composition
  - Integration with transcriptomic data to identify YBX1-dependent metabolic pathways
- **Expected outcomes:** Define YBX1's role in adipocyte metabolic adaptation

### 1.3 Loss of SMARCD2, SMARCE1, and YBX1 in differentiating 3T3 cells
- **Hypothesis:** cBAF subunits SMARCD2, SMARCE1 cooperate with YBX1 to maintain proper adipogenic program
- **Approach:**
  - CRISPR/shRNA knockdown of individual and combined factors
  - Oil Red O staining quantification
  - RNA-seq and ATAC-seq to identify chromatin and expression changes
  - Rescue experiments with reconstituted factors
- **Expected outcomes:** Mechanistic understanding of how chromatin remodeling complex and YBX1 coordinate adipogenesis

## 2. cBAF-CEBPa regulating mir-101
- **Hypothesis:** cBAF and CEBPA coordinate to regulate miR-101 expression, impacting lipid metabolism
- **Approach:**
  - ChIP-seq for cBAF components and CEBPA at miR-101 locus
  - miR-101 overexpression and inhibition studies
  - Target validation using directional RNA-seq and ribosome profiling
  - Lipidomics to assess impact on lipid composition
- **Expected outcomes:** Novel miRNA-mediated mechanism in metabolic control

## 3. Ybx1 in metabolic reprogramming of hepatocytes
### 3.1 Transcriptional network analysis of PPARg, CEBPa, CEBPb, SMARCD2, SMARCE1, BRG1
- **Hypothesis:** Chronic fat exposure alters binding patterns of master regulators and chromatin remodelers
- **Approach:**
  - Primary hepatocytes and HepG2 cells exposed to different lipid conditions (acute vs chronic)
  - ChIP-seq for all factors
  - ATAC-seq to assess chromatin accessibility changes
  - Integration with RNA-seq to identify dysregulated pathways
- **Expected outcomes:** Map how fat exposure reshapes the regulatory landscape in hepatocytes

### 3.2 Posttranscriptional regulation of lipogenic genes by Ybx1
- **Hypothesis:** YBX1 regulates mRNA stability and translation of key lipogenic genes
- **Approach:**
  - RIP-seq for YBX1-bound mRNAs
  - mRNA decay assays in control vs YBX1-depleted cells
  - Polysome profiling coupled with RNA-seq
  - CLIP-seq to map direct YBX1-RNA interactions
- **Expected outcomes:** Novel posttranscriptional regulatory mechanism in lipid metabolism

### 3.3 YBX1 INS1 repression
- **Hypothesis:** YBX1 represses insulin signaling in non-pancreatic tissues
- **Approach:**
  - Cell-type specific analysis of YBX1 and INS1 expression
  - Reporter assays with INS1 promoter
  - YBX1 ChIP-seq in pancreatic vs non-pancreatic cells
  - CRISPR activation/repression to modulate YBX1 levels
- **Key questions:** 
  - Is YBX1 absent in pancreatic beta cells? If so, how?
  - Can targeting YBX1 be therapeutic for certain types of Type 1 diabetes?

### 3.4 YBX1-CEBPa-cBAF in lipid-exposed hepatocytes multiomics
- **Hypothesis:** Chronic lipid exposure alters the cooperative activity of YBX1-CEBPa-cBAF, leading to hepatic steatosis
- **Approach:** Comprehensive multi-omic analysis integrating:
  - mRNA-seq
  - ATAC-seq
  - ChIP-seq: YBX1, BRG1, CEBPa, CEBPb
  - CelSeq2 for single-cell resolution of heterogeneous responses
  - DUO LINK proximity assays to validate physical interactions
  - Lipidomics to correlate with phenotypic outcomes
- **Expected outcomes:** Systems-level understanding of transcriptional dysregulation in fatty liver development

## 4. Using artificial intelligence to enhance biological insights
### 4.1 Geo stacking app
- **Project goal:** Develop tool to integrate and visualize multiple GEO datasets
- **Potential applications:** Meta-analysis of metabolic disease datasets

### 4.2 Transregulator-ATAC pattern finder
- **Project goal:** Machine learning tool to predict transcription factor binding from ATAC-seq data
- **Approach:** Train models using paired ATAC-seq and ChIP-seq datasets

### 4.3 Increase read mapping speed
- **Project goal:** Optimize computational pipeline for multi-omic data analysis

### 4.4 Lab agent
- **Project goal:** Develop AI-assisted laboratory workflow management system
- **Applications:** Experiment planning, protocol optimization, data analysis

### 4.5 ML model for oil-red O image quantification
- **Project goal:** Automated quantification of lipid accumulation in cell culture
- **Approach:** Computer vision models trained on labeled microscopy images

## 5. Regulation of Ybx1 cyto-nuclear translocation
- **Hypothesis:** Nutrient status regulates YBX1 localization and function
- **Approach:**
  - Subcellular fractionation followed by western blot
  - Live-cell imaging with fluorescently tagged YBX1
  - Mass spectrometry to identify post-translational modifications
  - Mutagenesis of key regulatory sites
- **Expected outcomes:** Understanding of how metabolic signals control YBX1 localization and function

## 6. Metabolic regulation of gene expression
- **Hypothesis:** Different nutrient environments reshape the epigenetic landscape
- **Approach:**
  - Treat hepatocytes with various conditions:
    - Insulin stimulation
    - Beta-oxidation inhibitors
    - Glycolysis inhibitors
  - ATAC-seq to map chromatin accessibility changes
  - RNA-seq to identify expression changes
  - Metabolomics to correlate with cellular metabolic state
- **Expected outcomes:** Map how specific metabolic pathways influence gene regulation

## 7. Environmental effects on hepatocyte cell fate
- **Hypothesis:** Environmental factors reprogram hepatocytes through KLF-mediated mechanisms
- **Approach:**
  - HepaRG differentiation under various conditions
  - ChIP-seq for KLF family members
  - CelSeq2 for single-cell trajectory analysis
  - Functional validation of key target genes

## 8. Mice studies
- **Hypothesis:** Hepatocyte-specific YBX1 deletion protects against diet-induced fatty liver
- **Approach:**
  - Generate hepatocyte-specific YBX1 knockout mice
  - High-fat diet challenge
  - Histological and biochemical analysis
  - Multi-omic profiling of liver tissue

## 9. Miscellaneous projects

## 10. Spheroids/Organoids
- **Hypothesis:** 3D culture systems better recapitulate YBX1 function in vivo
- **Approach:**
  - Establish liver spheroid/organoid cultures
  - Manipulate YBX1 expression
  - Single-cell RNA-seq for heterogeneity analysis
  - Lipid loading experiments and imaging

## 11. Robot
- **Goal:** Automated high-throughput screening platform
- **Applications:**
  - Drug screening for metabolic disease
  - Systematic CRISPR screening
  - Automated lipid accumulation assays

## 12. Directional RNAseq
- **Hypothesis:** Antisense transcription contributes to metabolic gene regulation
- **Approach:**
  - Directional RNA-seq in normal vs lipid-exposed cells
  - Integration with ChIP-seq data
  - Functional validation of key antisense transcripts

## 13. DuoLink
- **Goal:** Map protein-protein interactions in situ
- **Applications:**
  - YBX1-CEBP interactions in different cellular compartments
  - Dynamic changes in protein complexes during lipid stress

## 14. FA Uptake
- **Hypothesis:** YBX1 regulates expression of fatty acid transporters
- **Approach:**
  - Fluorescent fatty acid uptake assays in control vs YBX1-depleted cells
  - ChIP-seq for YBX1 at fatty acid transporter gene loci
  - Rescue experiments with transporter overexpression

## 15. Proliferation
- **Hypothesis:** YBX1 balances proliferation and differentiation in hepatocytes
- **Approach:**
  - EdU incorporation assays
  - Cell cycle analysis in YBX1-manipulated cells
  - Integration with RNA-seq data

## 16. Lipidomics
- **Goal:** Comprehensive profiling of lipid species changes
- **Applications:**
  - YBX1 knockout effects on hepatocyte lipid composition
  - Temporal changes during fat-induced cellular reprogramming

## 17. Oxylipins
- **Hypothesis:** YBX1 regulates inflammatory signaling via oxylipin metabolism
- **Approach:**
  - Targeted oxylipin profiling
  - Expression analysis of oxylipin biosynthetic enzymes
  - Functional validation with specific inhibitors

## 18. CelSeq time series
- **Hypothesis:** Fat exposure creates heterogeneous cell populations with distinct trajectories
- **Approach:**
  - CelSeq2 time course during fat exposure
  - Trajectory analysis and pseudotime ordering
  - Identification of cell state markers

## 19. In vitro cytonuclear proteomics
- **Goal:** Map protein localization changes during metabolic stress
- **Approach:**
  - Subcellular fractionation followed by mass spectrometry
  - YBX1 interactome in different cellular compartments
  - **Specific focus:** Epigenetic memory mechanisms and chromatin mismatch repair