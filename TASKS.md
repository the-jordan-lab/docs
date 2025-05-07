# Lab Task List

This file tracks all ongoing lab and dev tasks. Issues created via GitHub and the Lab Agent are appended automatically below.

---

# TASKS

_Note: This file is now automatically updated by the agent/task-runner. Tasks are marked done when experiments are completed, and new tasks may be added as needed._

## Lab Tasks
### Ybx1 Knockdown mRNA Stability Experiment (EXP-0225)
- [ ] Day 1 (May 6, 2025): Complete reverse transfection setup
  - [ ] Thaw HEK293T cells and check viability
  - [ ] Prepare transfection master mixes (siRNA targeting Ybx1 and Control siRNA)
  - [ ] Set up reverse transfection in 24-well plates
  - [ ] Update experiment status in repository
- [ ] Day 3 (May 8, 2025): Verify Ybx1 knockdown by qPCR
- [ ] Day 3 (May 8, 2025): Begin actinomycin D time course experiment
  - [ ] Collect t=0 samples before actinomycin D addition
  - [ ] Add actinomycin D (5 μg/ml) to remaining wells
  - [ ] Collect samples at 2h, 4h, and 8h timepoints
- [ ] Day 4 (May 9, 2025): Complete RNA extractions
- [ ] Day 4 (May 9, 2025): Synthesize cDNA and perform qPCR
- [ ] Submit final data to repository and link to experimental record

### YBX1-CEBPA Co-Immunoprecipitation (EXP-0226)
- [ ] Day 1 (May 8, 2025): Set up 3T3 cells
  - [ ] Seed 3T3 cells in six 10 cm dishes
  - [ ] Prepare stock solutions for adipogenic induction
- [ ] Day 2 (May 9, 2025): Begin adipogenic treatment
  - [ ] Prepare fresh adipogenic induction medium
  - [ ] Treat cells with control or adipogenic medium
- [ ] Day 3 (May 10, 2025): Harvest and process cells
  - [ ] Collect cell lysates from all conditions
  - [ ] Measure protein concentrations
  - [ ] Set up antibody incubation for co-immunoprecipitation
- [ ] Day 4 (May 11, 2025): Complete Co-IP and Western blotting
  - [ ] Process IP samples with protein A/G beads
  - [ ] Run SDS-PAGE gels and transfer to membranes
  - [ ] Blot for protein interactions
  - [ ] Image and quantify results
- [ ] Analyze protein interaction data and prepare figures

### Materials and Resources
- [ ] Confirm Actinomycin D stock availability
- [ ] Ensure sufficient RNA extraction reagents are available
- [ ] Check qPCR primer stocks for all target genes
- [ ] Order YBX1 and C/EBPα antibodies for Co-IP
- [ ] Verify Invitrogen gel and transfer system availability

## Development Tasks
- [ ] Reorganize repository structure: convert "projects" to "aims" and "subprojects" to "projects" for better GitHub integration
- [ ] Improve GitHub issue integration with short hash identifiers for future-proofing
- [ ] Update documentation to reflect new naming conventions
- [ ] Evaluate need for TASKS.md file in the new structure (consider GitHub issues as primary task tracker)

_This file will be updated as tasks are added or completed during implementation._ - [ ] [#9](https://github.com/the-jordan-lab/docs/issues/9) Pre-build Dev Container for instant Agent boot  _(added 2025-05-07 10:37)_
- [ ] [#10](https://github.com/the-jordan-lab/docs/issues/10) Add repo-level OPENAI_API_KEY secret & document  _(added 2025-05-07 10:37)_
- [ ] [#11](https://github.com/the-jordan-lab/docs/issues/11) Rewrite README Quick-Start for students  _(added 2025-05-07 10:37)_
- [ ] [#12](https://github.com/the-jordan-lab/docs/issues/12) Implement automated ISSUE → TASKS.md hook  _(added 2025-05-07 10:37)_
- [ ] [#13](https://github.com/the-jordan-lab/docs/issues/13) Add GitLens default issue view configuration  _(added 2025-05-07 10:37)_
- [ ] [#14](https://github.com/the-jordan-lab/docs/issues/14) CI: Codespace headless smoke test  _(added 2025-05-07 10:37)_
- [ ] [#15](https://github.com/the-jordan-lab/docs/issues/15) [Wet-Lab] Complete HEK293T thaw & viability check  _(added 2025-05-07 10:37)_
- [ ] [#16](https://github.com/the-jordan-lab/docs/issues/16) [Wet-Lab] Prepare Ybx1 & control siRNA mixes  _(added 2025-05-07 10:37)_
