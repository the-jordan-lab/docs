---
# EXPERIMENT METADATA
experiment_id: EXP-0226
title: "YBX1-CEBPA Protein Interaction in Early Adipogenesis (Iteration 2)"
date: 2025-05-08
researchers:
  - james-m-jordan
  - linda-onsei
protocol_id: PROT-0036
protocol_name: "Adipogenic Induction Treatment"
status: planned  # planned | in-progress | completed | failed
aim: "Investigate physical interaction between YBX1 and C/EBPα during early adipogenesis (24h post-induction) in 3T3 cells using reciprocal co-immunoprecipitation"
project: "Transcriptional Regulation in Early Adipogenesis"
---

---
# SAMPLE METADATA
cell_lines:
  - name: "3T3"
    media: "DMEM high glucose + 10% FBS + 1% Pen-Strep"
    passage: "P8-P12"
plate_format: "10 cm dishes"
condition_map: |
  Dish 1-3: 3T3 + Control medium (24h)
  Dish 4-6: 3T3 + Adipogenic induction medium (24h)
replicates: 3
---

---
# REAGENTS & INSTRUMENT SETTINGS
adipogenic_induction:
  reagents:
    - name: "IBMX"
      concentration: "0.5 mM"
      supplier: "Sigma-Aldrich (I5879)"
    - name: "Dexamethasone"
      concentration: "1 µM"
      supplier: "Sigma-Aldrich (D4902)"
    - name: "Insulin"
      concentration: "10 µg/mL"
      supplier: "Sigma-Aldrich (I6634)"
cell_lysis:
  buffer: "RIPA Buffer with protease inhibitors"
  volume: "500 µL per dish"
  incubation: "30 min on ice with occasional vortexing"
co_immunoprecipitation:
  antibodies:
    - name: "Anti-YBX1"
      amount: "5 µg per IP"
      supplier: "Cell Signaling Technology (#4202)"
    - name: "Anti-C/EBPα"
      amount: "5 µg per IP"
      supplier: "Cell Signaling Technology (#8178)"
    - name: "Normal Rabbit IgG (control)"
      amount: "5 µg per IP"
      supplier: "Cell Signaling Technology (#2729)"
  beads: "Protein A/G magnetic beads"
  volume: "30 µL per IP"
  binding: "Overnight at 4°C with rotation"
western_blot:
  gel: "Invitrogen NuPAGE 4-12% Bis-Tris"
  transfer: "iBlot 3 Dry Blotting System (P0 program, 7 min)"
  antibody_detection: "iBind 3 Western System"
  primary_antibodies:
    - name: "Anti-YBX1"
      dilution: "1:1000"
      supplier: "Cell Signaling Technology (#4202)"
    - name: "Anti-C/EBPα"
      dilution: "1:1000"
      supplier: "Cell Signaling Technology (#8178)"
  secondary_antibody: "Anti-rabbit HRP, 1:5000"
  imaging: "ChemiDoc Imaging System"
instruments:
  - name: "Invitrogen iBlot 3"
    settings: "P0 program, 7 minutes"
  - name: "Invitrogen iBind 3"
    settings: "Standard protocol, 3 hours"
  - name: "ChemiDoc Imaging System"
    settings: "Chemiluminescence, auto-exposure"
---

# 1️⃣ Experiment Timeline & Execution

## Day 1: 2025-05-08
- [ ] Seed 3T3 cells in six 10 cm dishes at density of 5 × 10⁵ cells/dish
- [ ] Incubate overnight at 37°C, 5% CO₂
- [ ] Prepare stock solutions for adipogenic induction medium

## Day 2: 2025-05-09
- [ ] Verify cells are ~90% confluent
- [ ] Prepare fresh adipogenic induction medium:
  - [ ] IBMX (0.5 mM)
  - [ ] Dexamethasone (1 µM)
  - [ ] Insulin (10 µg/mL)
- [ ] Replace media:
  - [ ] Dishes 1-3: Regular complete medium (control)
  - [ ] Dishes 4-6: Adipogenic induction medium
- [ ] Incubate for 24 hours at 37°C, 5% CO₂

## Day 3: 2025-05-10
- [ ] Harvest cells from all dishes:
  - [ ] Wash twice with ice-cold PBS
  - [ ] Add 500 µL RIPA buffer with protease inhibitors per dish
  - [ ] Scrape cells and collect lysate
  - [ ] Incubate 30 min on ice with occasional vortexing
  - [ ] Centrifuge at 14,000 × g for 15 min at 4°C
  - [ ] Transfer supernatant to new tubes
- [ ] Measure protein concentration using BCA assay
- [ ] Prepare samples for co-immunoprecipitation:
  - [ ] 500 µg protein per IP reaction
  - [ ] 3 IPs per condition (YBX1, CEBPA, IgG control)
- [ ] Add antibodies to lysates (5 µg each):
  - [ ] Anti-YBX1
  - [ ] Anti-C/EBPα
  - [ ] Normal Rabbit IgG (control)
- [ ] Incubate overnight at 4°C with rotation

## Day 4: 2025-05-11
- [ ] Add 30 µL Protein A/G magnetic beads to each IP sample
- [ ] Incubate 3 hours at 4°C with rotation
- [ ] Wash beads 5× with IP wash buffer
- [ ] Elute proteins with 50 µL 1× Laemmli buffer at 95°C for 5 min
- [ ] Load samples on Invitrogen NuPAGE 4-12% Bis-Tris gels:
  - [ ] Input (10% of lysate)
  - [ ] IP samples (YBX1, CEBPA, IgG for each condition)
- [ ] Run gels at 150V for 1 hour
- [ ] Transfer to PVDF membranes using iBlot 3 (P0 program, 7 min)
- [ ] Process membranes on iBind 3 with appropriate antibodies:
  - [ ] YBX1 pull-down: blot with anti-CEBPA
  - [ ] CEBPA pull-down: blot with anti-YBX1
- [ ] Image blots on ChemiDoc system
- [ ] Quantify band intensity using ImageJ

# 2️⃣ Raw Data & Resources
_Place files in `Data/EXP-0226/raw/` and list/link them here._

| Filename | Description | Date Added |
|----------|-------------|------------|
| `BCA_protein_assay.xlsx` | Protein concentration measurements | 2025-05-10 |
| `YBX1_pulldown_blots.tif` | YBX1 IP probed with anti-CEBPA | 2025-05-11 |
| `CEBPA_pulldown_blots.tif` | CEBPA IP probed with anti-YBX1 | 2025-05-11 |
| `input_controls.tif` | Input samples for both conditions | 2025-05-11 |

# 3️⃣ Results & Analysis

## Protein Concentration
_To be filled after BCA assay._

## Co-IP Efficiency
_To be filled after Western blot imaging._

## YBX1-CEBPA Interaction Analysis
_To be filled after completing Western blot quantification._

```
# To be filled after completing Western blot quantification

| Sample | YBX1 pulldown | CEBPA pulldown | IgG control |
|--------|---------------|----------------|-------------|
| Control | | | |
| Adipogenic | | | |
| Fold change | | | |
```

## Analysis Notes
_Add notes about analysis methods, tools used, etc._

Analysis script: `Analysis/EXP-0226_CoIP_quantification.R`

* Band intensity quantified using ImageJ
* Interaction strength calculated as ratio of co-IPed protein to pulled-down protein
* Statistical analysis: paired t-test between conditions

# 4️⃣ Interpretation

## Summary of Findings
_To be completed after experiment_

## Comparison to Previous Iteration
_Compare results with first iteration of this experiment_

## Relation to Project Goals
This experiment directly addresses our hypothesis that YBX1 and C/EBPα physically interact during early adipogenesis. By comparing 3T3 cells with and without adipogenic stimulation, we can determine if this interaction is enhanced during the early stages of adipocyte differentiation (24h post-induction).

# 5️⃣ Next Steps ✅
_Check boxes when complete. These can auto-update TASKS.md._

- [ ] Repeat Co-IP with additional binding partners (C/EBPβ, C/EBPδ)
- [ ] Perform reciprocal Co-IP at multiple timepoints (6h, 12h, 24h, 48h)
- [ ] Characterize binding domains through truncation mutants
- [ ] Present results at lab meeting on 2025-05-15
- [ ] Consider ChIP-seq to identify co-regulated genes

# 6️⃣ Team Discussion
_Use this section for team comments, suggestions, and feedback._

> **james-m-jordan (2025-05-07):** This is the second iteration of this experiment. In the first iteration (EXP-0218), we saw a weak interaction in control conditions that was strongly enhanced after adipogenic stimulation. Let's make sure our lysis conditions are optimal for capturing these interactions.

> **linda-onsei (2025-05-07):** Should we also check protein levels by straight Western blot? I'm wondering if the increased interaction is partly due to increased expression of either protein.

# 7️⃣ References & Related Experiments
- Related protocol: [Adipogenic Induction Treatment](Protocols/adipogenic_induction_treatment_v1.yaml)
- Previous experiment: [EXP-0218](Experiments/EXP-0218_YBX1_CEBPA_interaction_3T3.md)
- Literature: Girard J, et al. (2018) YBX1 interacts with C/EBP transcription factors to regulate adipogenesis. Cell Reports 25:788-801. 