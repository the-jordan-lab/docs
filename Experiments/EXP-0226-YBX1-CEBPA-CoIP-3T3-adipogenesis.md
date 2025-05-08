---
# EXPERIMENT METADATA
experiment_id: EXP-0226
title: "YBX1-CEBPA Protein Interaction in Early Adipogenesis (Iteration 2)"
date: 2025-05-08
researchers:
  - james-m-jordan
  - linda-onsei
  - SanjanaC
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
sample_location: "-80°C freezer, rack 1-1-4-A"
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
      amount: "2 µL of 1:1000 dilution per IP"
      supplier: "Abcam (ab268094)"
    - name: "Anti-C/EBPα"
      amount: "2 µL of 1:1000 dilution per IP"
      supplier: "Abcam (AB317442)"
    - name: "Normal Mouse IgG (control)"
      amount: "2 µL of 1:1000 dilution per IP"
      supplier: "Cell Signaling Technology (#5415)"
  beads: "Protein A/G beads (NEB S1430 and S1425 mixed 1:1)"
  volume: "30 µL per IP"
  binding: "Overnight at 4°C with rotation"
  ip_wash_buffer: "PBS + 0.02% Tween-20"
  elution_buffer: "Non-denaturing elution buffer, 20 µL per sample"
western_blot:
  gel: "Invitrogen NuPAGE 4-12% Bis-Tris mini gels (15-well)"
  transfer: "iBlot 3 Dry Blotting System (P0 program, 7 min)"
  antibody_detection: "iBind 3 Western System"
  ibind_protocol: "2 µL of 1:1000 primary antibody dilution per 2 mL iBind solution per mini gel"
  primary_antibodies:
    - name: "Anti-YBX1"
      dilution: "1:1000"
      supplier: "Abcam (ab268094)"
    - name: "Anti-C/EBPα"
      dilution: "1:1000"
      supplier: "Abcam (AB317442)"
  secondary_antibody: "Anti-mouse HRP, 1:5000"
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

### BCA Protein Assay Procedure
- [ ] Prepare BSA standards (0, 0.125, 0.25, 0.5, 1, 2 mg/mL) in the same buffer as samples
- [ ] Dilute samples 1:5 in RIPA buffer (5 µL sample + 20 µL buffer)
  - **CRITICAL INPUT: Researcher must record total lysate volume before dilution for each sample!**
  - **CRITICAL INPUT: Researcher must record dilution factor used for BCA assay!**
- [ ] Add 200 µL BCA working reagent (50:1, Reagent A:B) to 10 µL of each standard/sample in a 96-well plate
- [ ] Incubate plate at 37°C for 30 minutes
- [ ] Measure absorbance at 562 nm
- [ ] Generate standard curve by plotting absorbance vs. known BSA concentrations
- [ ] Calculate protein concentration of each sample using the standard curve equation
- [ ] Adjust for dilution factor: Final concentration = Measured concentration × Dilution factor

### Sample Preparation for Co-Immunoprecipitation
- [ ] Prepare samples for co-immunoprecipitation:
  - [ ] 500 µg protein per IP reaction
  - [ ] 2 samples per condition (control and adipogenesis induction)
  - [ ] 2 IPs per sample (YBX1 pull-down and CEBPA pull-down)
- [ ] Preclear lysates with 50% beads:
  - [ ] Add 20 µL of 50% Protein A/G beads (NEB S1430 and S1425 mixed 1:1) to each lysate
  - [ ] Incubate at 4°C with rotation for 1 hour
  - [ ] Centrifuge at 2,500 × g for 5 minutes or place on magnetic stand
  - [ ] Transfer precleared supernatant to new tubes
- [ ] Add antibodies to precleared lysates (2 µL of 1:1000 dilution each):
  - [ ] Anti-YBX1 
  - [ ] Anti-C/EBPα
  - [ ] Normal Mouse IgG (control)
- [ ] Incubate overnight at 4°C with rotation

## Day 4: 2025-05-11
- [ ] Add 30 µL Protein A/G beads (NEB S1430 and S1425 mixed 1:1) to each IP sample
- [ ] Incubate overnight at 4°C with thermomixing at 400 rpm
- [ ] Wash beads 4× with IP wash buffer (PBS + 0.02% Tween-20):
  - [ ] Add 500 µL wash buffer to each sample
  - [ ] Invert tubes several times or mix gently
  - [ ] Place on magnetic stand to separate beads
  - [ ] Remove supernatant carefully without disturbing beads
  - [ ] Repeat 3 more times (4 washes total)
- [ ] Elute proteins with non-denaturing elution:
  - [ ] Add 20 µL non-denaturing elution buffer to each sample
  - [ ] Incubate at 37°C with rotation for 5 minutes
  - [ ] Place tubes on magnetic stand to separate beads
  - [ ] **IMPORTANT: Carefully collect supernatant without disturbing beads**
  - [ ] **WARNING: DO NOT load any beads into the gel - they will interfere with migration!**
- [ ] Load samples on Invitrogen NuPAGE 4-12% Bis-Tris mini gels (2 gels):
  - [ ] Input (10% of lysate)
  - [ ] IP samples
  - [ ] Gel 1: YBX1 pull-down probed with anti-CEBPA
  - [ ] Gel 2: CEBPA pull-down probed with anti-YBX1
- [ ] Run gels at 150V for 1 hour
- [ ] Transfer to PVDF membranes using iBlot 3 (P0 program, 7 min)
- [ ] Process membranes on iBind 3:
  - [ ] Prepare iBind solution: 2 µL of 1:1000 primary antibody dilution per 2 mL iBind solution per mini gel
  - [ ] Gel 1: Probe with anti-CEBPA antibody
  - [ ] Gel 2: Probe with anti-YBX1 antibody
- [ ] Image blots on ChemiDoc system
- [ ] Quantify band intensity using ImageJ

## Gel Loading Instructions (15-well gels)

### Gel 1: YBX1 Pull-Down (Probed with anti-CEBPA)
Loading order for 15-well gel:
1. Protein ladder
2. IgG PD - Control condition (no adipogenic induction)
3. IgG PD - Adipogenic induction
4. YBX1 PD - Control condition (no adipogenic induction)
5. YBX1 PD - Adipogenic induction
6. Protein ladder
7. Input - Control condition (no adipogenic induction)
8. Input - Adipogenic induction
9. Protein ladder
10. Leftover - IgG PD Control
11. Leftover - IgG PD Adipogenic
12. Leftover - YBX1 PD Control
13. Leftover - YBX1 PD Adipogenic
14. Empty
15. Empty

### Gel 2: CEBPA Pull-Down (Probed with anti-YBX1)
Loading order for 15-well gel:
1. Protein ladder
2. IgG PD - Control condition (no adipogenic induction)
3. IgG PD - Adipogenic induction
4. CEBPA PD - Control condition (no adipogenic induction)
5. CEBPA PD - Adipogenic induction
6. Protein ladder
7. Input - Control condition (no adipogenic induction)
8. Input - Adipogenic induction
9. Protein ladder
10. Leftover - IgG PD Control
11. Leftover - IgG PD Adipogenic
12. Leftover - CEBPA PD Control
13. Leftover - CEBPA PD Adipogenic
14. Empty
15. Empty

# 2️⃣ Raw Data & Resources

**IMPORTANT: All raw data files MUST be placed in the directory `Data/EXP-0226/raw/` and listed in the table below!**

| Filename | Description | Date Added |
|----------|-------------|------------|
| `BCA_protein_assay.xlsx` | Protein concentration measurements and standard curve | 2025-05-10 |
| `YBX1_pulldown_blots.tif` | YBX1 IP probed with anti-CEBPA (includes input samples) | 2025-05-11 |
| `CEBPA_pulldown_blots.tif` | CEBPA IP probed with anti-YBX1 (includes input samples) | 2025-05-11 |

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
_Compare results with first iteration of this experiment (EXP-0224)_

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

> **james-m-jordan (2025-05-07):** This is the second iteration of this experiment. In the first iteration (EXP-0224), we saw a weak interaction in control conditions that was strongly enhanced after adipogenic stimulation. Let's make sure our lysis conditions are optimal for capturing these interactions.

> **linda-onsei (2025-05-07):** Should we also check protein levels by straight Western blot? I'm wondering if the increased interaction is partly due to increased expression of either protein.

# 7️⃣ References & Related Experiments
- Related protocol: [Adipogenic Induction Treatment](Protocols/adipogenic_induction_treatment_v1.yaml)
- Previous experiment: [EXP-0224](Experiments/EXP-0224-YBX1-CEBPA-CoIP-3T3-adipogenesis.md)
- Literature: Girard J, et al. (2018) YBX1 interacts with C/EBP transcription factors to regulate adipogenesis. Cell Reports 25:788-801. 