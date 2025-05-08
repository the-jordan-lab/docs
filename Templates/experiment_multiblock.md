---
# EXPERIMENT METADATA
experiment_id: EXP-XXXX
title: "EXPERIMENT_TITLE"
date: YYYY-MM-DD
researchers:
  - RESEARCHER1
  - RESEARCHER2
protocol_id: PROT-XXXX
protocol_name: "PROTOCOL_NAME"
status: planned  # planned | in-progress | completed | failed
aim: "Brief description of experimental aim"
project: "PROJECT_NAME"
---

---
# SAMPLE METADATA
cell_lines:
  - name: "CELL_LINE1"
    media: "MEDIA_TYPE"
    passage: "PASSAGE_NUMBER"
  - name: "CELL_LINE2"
    media: "MEDIA_TYPE"
    passage: "PASSAGE_NUMBER"
plate_format: "24-well"  # 6-well | 24-well | 96-well | etc.
condition_map: |
  A1-A6: CELL_LINE1 + TREATMENT1
  B1-B6: CELL_LINE1 + TREATMENT2
  C1-C6: CELL_LINE2 + TREATMENT1
  D1-D6: CELL_LINE2 + TREATMENT2
replicates: 6
sample_location: "-80°C freezer, rack X-X-X-X"
---

---
# REAGENTS & INSTRUMENT SETTINGS
transfection:
  reagent: "TRANSFECTION_REAGENT"
  volume_per_well: "XX µL"
  complex_volume: "XX µL"
  incubation_time: "XX min"
treatments:
  - name: "TREATMENT1"
    concentration: "XX µM/nM"
    duration: "XX h"
  - name: "TREATMENT2"
    concentration: "XX µM/nM"
    duration: "XX h"
timepoints: 
  - "0h"
  - "Xh"
  - "Xh"
instruments:
  - name: "INSTRUMENT_NAME"
    settings: "RELEVANT_SETTINGS"
---

# 1️⃣ Experiment Timeline & Execution

## Day 1: YYYY-MM-DD
- [ ] Task 1: DESCRIPTION
- [ ] Task 2: DESCRIPTION

## Day 2: YYYY-MM-DD
- [ ] Task 1: DESCRIPTION
- [ ] Task 2: DESCRIPTION

## Day 3: YYYY-MM-DD
- [ ] Task 1: DESCRIPTION
- [ ] Task 2: DESCRIPTION

# 2️⃣ Raw Data & Resources
_Place files in `Data/{{experiment_id}}/raw/` and list/link them here._

| Filename | Description | Date Added |
|----------|-------------|------------|
| `filename1.xlsx` | DESCRIPTION | YYYY-MM-DD |
| `filename2.csv` | DESCRIPTION | YYYY-MM-DD |
| `image1.png` | DESCRIPTION | YYYY-MM-DD |

# 3️⃣ Results & Analysis

## QC Metrics
_Add quality control results, RNA integrity, transfection efficiency, etc._

## Primary Results
_Add tables, plots, or images of key results._

```markdown
# Insert code blocks, tables, or embed plots here
```

## Analysis Notes
_Add notes about analysis methods, tools used, etc._

Analysis script: `Analysis/{{experiment_id}}_analysis.R`

# 4️⃣ Interpretation

## Summary of Findings
_Provide a concise summary of key findings (2-3 paragraphs)._

## Challenges & Limitations
_Note any issues encountered or limitations of the experiment._

## Relation to Project Goals
_Explain how these results contribute to the larger project._

# 5️⃣ Next Steps ✅
_Check boxes when complete. These can auto-update TASKS.md._

- [ ] Follow-up experiment: DESCRIPTION
- [ ] Additional analysis: DESCRIPTION
- [ ] Present results at lab meeting on YYYY-MM-DD
- [ ] Update protocol based on findings
- [ ] Other: DESCRIPTION

# 6️⃣ Team Discussion
_Use this section for team comments, suggestions, and feedback._

> **RESEARCHER1 (YYYY-MM-DD):** Comment text here.

> **RESEARCHER2 (YYYY-MM-DD):** Comment text here.

# 7️⃣ References & Related Experiments
- Related protocol: [PROTOCOL_NAME](Protocols/protocol_file.yaml)
- Previous experiment: [EXP-XXXX](Experiments/experiment_file.md)
- Literature: CITATION 