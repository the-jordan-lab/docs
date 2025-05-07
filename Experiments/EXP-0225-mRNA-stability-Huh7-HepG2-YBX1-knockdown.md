---
# EXPERIMENT METADATA
experiment_id: EXP-0225
title: "mRNA Stability Assay with YBX1 Knockdown in Huh7 and HepG2 Cells"
date: 2025-05-07
researchers:
  - james-m-jordan
  - jack-zhao
protocol_id: PROT-0035
protocol_name: "YBX1 Knockdown mRNA Stability Assay"
status: planned  # planned | in-progress | completed | failed
aim: "Measure the effect of YBX1 knockdown on mRNA stability in HepG2 and Huh7 cells by monitoring decay of target mRNAs after transcription inhibition with actinomycin D"
project: "Post-transcriptional regulation by Ybx1"
---

---
# SAMPLE METADATA
cell_lines:
  - name: "Huh7"
    media: "RPMI-1640 + 10% FBS + antibiotics"
    passage: "P5-P10"
  - name: "HepG2"
    media: "DMEM/F-12 + 10% FBS + antibiotics"
    passage: "P3-P8"
plate_format: "24-well"
condition_map: |
  A1-A6: Huh7 + siYBX1
  B1-B6: Huh7 + siCTRL
  C1-C6: HepG2 + siYBX1
  D1-D6: HepG2 + siCTRL
replicates: 6
---

---
# REAGENTS & INSTRUMENT SETTINGS
transfection:
  reagent: "Lipofectamine RNAiMAX"
  siRNA_volume_per_well: "1 µL"
  complex_volume: "52 µL"
  incubation_time: "5 min"
siRNA:
  - name: "siYBX1"
    concentration: "10 nM final"
    supplier: "Dharmacon"
  - name: "siCTRL (non-targeting)"
    concentration: "10 nM final"
    supplier: "Dharmacon"
actinomycin_D:
  concentration: "5 µg/mL"
  solvent: "DMSO"
  storage: "-20°C, protected from light"
timepoints:
  - "0h (before ActD)"
  - "1h"
  - "2h"
  - "4h"
  - "8h"
target_genes:
  - "YBX1 (knockdown verification)"
  - "GAPDH (reference gene)"
  - "ACTB (reference gene)"
  - "IL6 (example YBX1 target)"
  - "MYC (example YBX1 target)"
instruments:
  - name: "Real-time PCR System"
    model: "Applied Biosystems QuantStudio 3"
    settings: "95°C 15s, 60°C 60s for 40 cycles"
---

# 1️⃣ Experiment Timeline & Execution

## Day 1: 2025-05-07
- [ ] Seed cells in 24-well plates:
  - Huh7: 5 × 10⁴ cells / well
  - HepG2: 6 × 10⁴ cells / well
- [ ] Prepare plates and label wells according to condition map
- [ ] Incubate O/N at 37°C + 5% CO₂

## Day 2: 2025-05-08
- [ ] Prepare siRNA transfection:
  - Solution A: siRNA in Opti-MEM (26 µL per well)
  - Solution B: RNAiMAX in Opti-MEM (26 µL per well)
  - Combine A+B, incubate 5 min at RT
- [ ] Aspirate spent medium from wells
- [ ] Add 0.9 mL fresh complete medium to each well
- [ ] Add 52 µL transfection complex to appropriate wells
- [ ] Gently rock plate to distribute complexes
- [ ] Return plates to 37°C + 5% CO₂ incubator

## Day 3: 2025-05-09
- [ ] Collect one well from each condition for knockdown verification:
  - Extract RNA using TRIzol
  - RT-qPCR for YBX1 (vs control wells)
  - Confirm >70% knockdown

## Day 4: 2025-05-10
- [ ] Preparation for actinomycin D treatment:
  - Label tubes for all timepoints
  - Thaw actinomycin D (protect from light)
- [ ] Collect t=0 samples (before actinomycin D)
- [ ] Add actinomycin D (5 µg/mL final) to all remaining wells
- [ ] Collect cells at timepoints (1h, 2h, 4h, 8h):
  - Aspirate medium
  - Add TRIzol directly to wells (500 µL)
  - Transfer lysate to labeled tubes
  - Store at -80°C

## Day 5: 2025-05-11
- [ ] Complete RNA isolation from all samples using TRIzol protocol
- [ ] Quantify RNA and verify integrity
- [ ] Perform cDNA synthesis using SuperScript III RT kit

## Day 6: 2025-05-12
- [ ] Perform qPCR for target genes and reference genes
- [ ] Calculate relative expression and half-lives
- [ ] Analyze differences between control and YBX1 knockdown

# 2️⃣ Raw Data & Resources
_Place files in `Data/EXP-0225/raw/` and list/link them here._

| Filename | Description | Date Added |
|----------|-------------|------------|
| `knockdown_qPCR.xlsx` | Day 3 YBX1 knockdown verification | 2025-05-09 |
| `timecourse_qPCR.xlsx` | Timepoint qPCR data for all targets | 2025-05-12 |
| `RNA_concentrations.xlsx` | RNA yield and A260/280 ratios | 2025-05-11 |

# 3️⃣ Results & Analysis

## QC Metrics
_Add RNA integrity values, knockdown efficiency, etc._

## Knockdown Efficiency
```
# To be filled after Day 3 verification
```

## Half-life Calculations
```
# To be filled after completing qPCR analysis

| Gene | t½ (Huh7 siCTRL) | t½ (Huh7 siYBX1) | Ratio | p-value |
|------|------------------|------------------|-------|---------|
| IL6  |                  |                  |       |         |
| MYC  |                  |                  |       |         |

| Gene | t½ (HepG2 siCTRL) | t½ (HepG2 siYBX1) | Ratio | p-value |
|------|-------------------|-------------------|-------|---------|
| IL6  |                   |                   |       |         |
| MYC  |                   |                   |       |         |
```

## Analysis Notes
_Add notes about analysis methods, tools used, etc._

Analysis script: `Analysis/EXP-0225_mRNA_stability_analysis.R`

* Half-life calculated by plotting ln(relative mRNA level) vs time
* Linear regression slope (k) used to calculate t½ = ln(2)/|k|
* Statistical analysis: paired t-test between conditions

# 4️⃣ Interpretation

## Summary of Findings
_To be completed after experiment_

## Cell Type Comparison
_Compare the effect of YBX1 knockdown on mRNA stability between Huh7 and HepG2 cells_

## Relation to Project Goals
This experiment directly addresses our hypothesis that YBX1 stabilizes specific mRNAs in liver cancer cells. By comparing two liver cancer cell lines (Huh7 and HepG2), we can determine if YBX1's role in mRNA stability is conserved across different liver cancer subtypes or if it's cell-line specific.

# 5️⃣ Next Steps ✅
_Check boxes when complete. These can auto-update TASKS.md._

- [ ] Verify YBX1 knockdown at protein level by western blot
- [ ] Repeat experiment with additional YBX1 target genes
- [ ] Compare results with m6A-seq data to correlate with methylation sites
- [ ] Present results at lab meeting on 2025-05-17
- [ ] Consider rescue experiment with YBX1 overexpression

# 6️⃣ Team Discussion
_Use this section for team comments, suggestions, and feedback._

> **james-m-jordan (2025-05-07):** Let's make sure we're collecting enough material for both RNA and protein analysis. We might want to include a few extra wells for protein extraction to verify knockdown by western blot too.

> **jack-zhao (2025-05-07):** I suggest we include MALAT1 as another target - it's a long non-coding RNA reported to interact with YBX1.

# 7️⃣ References & Related Experiments
- Related protocol: [YBX1 Knockdown mRNA Stability Assay](Protocols/ybx1_knockdown_mrna_stability_protocol.yaml)
- Previous experiment: [EXP-0220](Experiments/EXP-0220_YBX1_expression_profiling.md)
- Literature: Wei YY, et al. (2021) YBX1 binds to m6A-methylated mRNAs to promote their stability and translation. Nature Communications 12:1278 