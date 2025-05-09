---
# EXPERIMENT METADATA
experiment_id: EXP-0220
title: "siRNA Knockdown with OAPAv2 and RT-qPCR Validation"
date: 2025-03-20
researchers:
  - RW
protocol_id: PROT-0042
protocol_name: "siRNA Transfection and RT-qPCR Analysis"
status: in-progress  # planned | in-progress | completed | failed
aim: "Knockdown two genes with siRNA, perform OAPAv2, isolate RNA, and validate knockdown efficiency via RT-qPCR"
project: "YBX1 Metabolic Regulation"
---

---
# SAMPLE METADATA
cell_lines:
  - name: "Huh7"
    media: "DMEM high glucose + 10% FBS + 1% Pen-Strep"
    passage: "P5-P8"
plate_format: "6-well plates"
condition_map: |
  Group 1: Negative control siRNA (scrambled)
  Group 2: siRNA targeting Gene 1
  Group 3: siRNA targeting Gene 2
replicates: 3
sample_location: "-80°C freezer, rack 2-3-1-B"
---

---
# REAGENTS & INSTRUMENT SETTINGS
siRNA_transfection:
  reagents:
    - name: "Lipofectamine RNAiMAX"
      supplier: "Thermo Fisher (13778150)"
    - name: "Opti-MEM"
      supplier: "Thermo Fisher (31985062)"
    - name: "Negative control siRNA"
      concentration: "20 μM stock"
      supplier: "Dharmacon"
    - name: "siRNA targeting Gene 1"
      concentration: "20 μM stock"
      supplier: "Dharmacon"
    - name: "siRNA targeting Gene 2"
      concentration: "20 μM stock"
      supplier: "Dharmacon"
  final_siRNA_concentration: "50 nM"
  incubation_time: "48 hours"

OAPAV2_assay:
  reagent_kit: "Oil Red O Adipocyte Assay Kit v2"
  supplier: "ZenBio (OA-300-2)"
  protocol: "Manufacturer's instructions followed with no modifications"
  
RNA_isolation:
  kit: "DirectZol RNA Miniprep Kit"
  supplier: "Zymo Research (R2052)"
  protocol: "Manufacturer's instructions followed with no modifications"
  dnase_treatment: true
  elution_volume: "50 μL"

RT_qPCR:
  cDNA_synthesis:
    kit: "High-Capacity cDNA Reverse Transcription Kit"
    supplier: "Thermo Fisher (4368814)"
    input_RNA: "1 μg"
    reaction_volume: "20 μL"
    thermal_cycler_settings: "25°C for 10 min, 37°C for 120 min, 85°C for 5 min, 4°C hold"
  
  qPCR:
    master_mix: "PowerUp SYBR Green Master Mix"
    supplier: "Thermo Fisher (A25742)"
    reaction_volume: "10 μL"
    instrument: "QuantStudio 5 Real-Time PCR System"
    cycling_conditions: "50°C for 2 min, 95°C for 2 min, 40 cycles of (95°C for 15 sec, 60°C for 1 min)"
    melt_curve: "Standard melt curve"
    
  primers:
    - name: "HPRT (housekeeping)"
      forward: "5'-TGACACTGGCAAAACAATGCA-3'"
      reverse: "5'-GGTCCTTTTCACCAGCAAGCT-3'"
      amplicon_size: "94 bp"
    - name: "VNN1"
      forward: "5'-CTGCAGCTGACATTCGACATC-3'"
      reverse: "5'-GTGCCAGTTCAGGACTGGTATT-3'"
      amplicon_size: "103 bp"
    - name: "Gene 2"
      forward: "5'-SEQUENCE-3'"
      reverse: "5'-SEQUENCE-3'"
      amplicon_size: "XX bp"
---

# 1️⃣ Experiment Timeline & Execution

## Day 1: 2025-03-20
- [x] Seed Huh7 cells in 6-well plates at 2 × 10⁵ cells/well
- [x] Incubate overnight at 37°C, 5% CO₂

## Day 2: 2025-03-21
- [x] Prepare siRNA transfection complexes:
  - [x] Dilute siRNAs in Opti-MEM
  - [x] Dilute Lipofectamine RNAiMAX in Opti-MEM
  - [x] Combine diluted siRNA with diluted Lipofectamine RNAiMAX
  - [x] Incubate for 5 minutes at room temperature
- [x] Transfect cells with siRNA complexes:
  - [x] Group 1: Negative control siRNA (scrambled)
  - [x] Group 2: siRNA targeting Gene 1
  - [x] Group 3: siRNA targeting Gene 2
- [x] Incubate for 48 hours at 37°C, 5% CO₂

## Day 4: 2025-03-23
- [x] Perform OAPAv2 assay according to manufacturer's protocol
- [x] Take photos of representative wells for each condition
- [x] For RNA isolation:
  - [x] Remove media from cells
  - [x] Add 700 μL of TRI Reagent to each well
  - [x] Collect lysate and proceed with DirectZol RNA isolation
  - [x] Include on-column DNase I treatment
  - [x] Elute RNA in 50 μL of DNase/RNase-free water
- [x] Measure RNA concentration using NanoDrop:
  - [x] Record concentration and A260/280 ratio for each sample
  - [x] Ensure A260/280 ratios are between 1.8-2.1

## Day 5: 2025-03-24
- [ ] Prepare cDNA using High-Capacity cDNA Reverse Transcription Kit:
  - [ ] Use 1 μg of total RNA from each sample
  - [ ] Prepare RT master mix according to manufacturer's protocol
  - [ ] Run RT reaction in thermal cycler
- [ ] Set up qPCR reactions:
  - [ ] Prepare qPCR master mix for each primer pair
  - [ ] Load reactions in 384-well plate
  - [ ] Include no-template controls (NTC) for each primer pair
  - [ ] Run qPCR with standard protocol and melt curve analysis
- [ ] Analyze data:
  - [ ] Calculate ΔCt values using HPRT as reference gene
  - [ ] Calculate ΔΔCt values relative to negative control siRNA
  - [ ] Calculate relative expression (2^-ΔΔCt)
  - [ ] Determine knockdown efficiency for each target gene

# 2️⃣ Raw Data & Resources

**IMPORTANT: All raw data files must be placed in the directory `data/EXP-0220/raw/` and listed in the table below!**

| Filename | Description | Date Added |
|----------|-------------|------------|
| `siRNA_transfection_layout.xlsx` | Plate layout and transfection details | 2025-03-21 |
| `OAPAV2_images.zip` | Microscopy images from OAPAv2 assay | 2025-03-23 |
| `RNA_isolation_nanodrop.xlsx` | RNA concentration and quality measurements | 2025-03-23 |
| `qPCR_data.xlsx` | Raw Ct values and analysis | [pending] |

# 3️⃣ Results & Analysis

## RNA Quality Assessment
[To be completed after RNA isolation]

## Knockdown Efficiency
[To be completed after RT-qPCR analysis]

## OAPAv2 Results
[To be completed after image analysis]

# 4️⃣ Interpretation

## Summary of Findings
[To be completed after data analysis]

## Relation to Project Goals
This experiment will validate the siRNA knockdown efficiency and assess the impact of gene knockdown on cellular phenotype through the OAPAv2 assay. Successful knockdown will provide a foundation for future experiments investigating the role of these genes in metabolic regulation and their potential interaction with YBX1.

# 5️⃣ Next Steps
_Check boxes when complete. These can auto-update TASKS.md._

- [ ] Complete RT-qPCR analysis to confirm knockdown efficiency
- [ ] Quantify OAPAv2 images to assess phenotypic changes
- [ ] Present results at lab meeting
- [ ] Design follow-up experiments based on knockdown efficiency and phenotypic changes

# 6️⃣ Team Discussion
_Use this section for team comments, suggestions, and feedback._

> **RW (2025-03-23):** RNA isolation was successful with good yields (concentration range: 250-450 ng/μL) and high quality (A260/280 ratios between 1.9-2.0). Will proceed with RT-qPCR tomorrow to assess knockdown efficiency.

# 7️⃣ References & Related Experiments
- Protocol: [siRNA Transfection and RT-qPCR Analysis](protocols/siRNA_transfection_and_rtqpcr_analysis.yaml)
- Literature: [citation for relevant gene knockdown studies] 