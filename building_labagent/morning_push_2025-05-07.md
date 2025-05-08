# Morning Push Checklist – 2025-05-07

## Objective
Deliver a **zero-friction boot experience** for students: open Codespace ➜ talk to Lab Agent immediately, with no extra setup.  All necessary secrets, tools, and docs must already be in place.

---

## 1. Infrastructure / Dev-Ops Tasks (NEW)
- [ ] **Pre-build Dev Container**
  - Configure `devcontainer.json` → `features` & `updateContentCommand` so that Python deps, GitHub CLI, and Agent embeddings are built during Codespaces prebuilds.
  - Verify a fresh Codespace reaches "Agent ready" in <2 min.
- [ ] **Centralise `OPENAI_API_KEY` secret**
  - Add repo-level Codespaces secret `OPENAI_API_KEY` (owner only).  Students inherit runtime access, cannot view value.
  - Document in README > _Secrets are pre-loaded; no action required_.
- [ ] **README Quick-Start for Students**
  - Replace multi-step environment instructions with a 3-step "Open ➜ Wait ➜ Chat" section.
  - Include GIF / screenshot.
- [ ] **Automated Issue Logging**
  - Implement small Python hook (`Agent/hooks/post_issue.py`) to append newly created GitHub issues to `TASKS.md` and `ISSUES_LOG.md`.
  - Add instructions in `Lab Agent Guide`.
- [ ] **GitLens Integration**
  - Add `.vscode/settings.json` to enable GitLens "Worktree Issues" view and pin lab-repo issues by default.
- [ ] **CI Smoke Test** (optional)
  - GitHub Action that boots Codespace headless and runs `Agent/agent_runner.py --healthcheck`.

---

## 2. Carried-Over Wet-Lab Tasks (from 2025-05-06)
These remain **open** and must be tracked alongside dev tasks.
- [ ] Thaw HEK293T cells and check viability
- [ ] Prepare transfection master mixes
  - [ ] siRNA targeting Ybx1
  - [ ] Control siRNA
- [ ] Set up reverse transfection in 24-well plates
  - [ ] Label all plates and wells
  - [ ] Prepare Lipofectamine RNAiMAX and Opti-MEM mixtures
  - [ ] Add siRNA to appropriate wells
  - [ ] Add cells to all wells
- [ ] Place plates in 37 °C incubator with 5 % CO₂
- [ ] Update experiment status in repository
- [ ] Upcoming Day 3 tasks (May 8) – verify knockdown & start actinomycin D time course
- [ ] Materials check: Actinomycin D, RNA extraction kits, qPCR primers

---

## 3. GitHub Issues to Create (assign to @james-m-jordan)
| # | Title | Labels |
|---|-------|--------|
| 1 | Pre-build Dev Container for instant Agent boot | infra, high-priority |
| 2 | Add repo-level OPENAI_API_KEY secret & document | infra, security |
| 3 | Rewrite README Quick-Start for students | docs |
| 4 | Implement automated ISSUE → TASKS.md hook | tooling |
| 5 | Add GitLens default issue view configuration | tooling |
| 6 | CI: Codespace headless smoke test | ci |
| 7 | [Wet-Lab] Complete HEK293T thaw & viability check | lab |
| 8 | [Wet-Lab] Prepare Ybx1 & control siRNA mixes | lab |
| … | _Continue one issue per checklist bullet above_ | |

> **How to batch-create:**
> ```bash
> gh issue create -t "Pre-build Dev Container for instant Agent boot" -b "See morning_push_2025-05-07.md#1" -a james-m-jordan -l infra,high-priority
> # Repeat for each row or use gh api to script.
> ```

---

## 4. Deliverables for May 7 End-of-Day
- Updated **README.md** (student quick-start)
- Merged PR implementing dev-ops tasks 1–2
- All GitHub issues above created and assigned
- `ISSUES_LOG.md` scaffold committed

---

## 5. Review & Next Steps
1. Mid-day stand-up: confirm secret injection works in fresh Codespace.
2. Evening: demo 60-second "clone → chat" workflow with new student account.
3. Plan May 8 push: continue lab experiment tracking + smoke test results.

---

_Authored automatically by Lab Agent on 2025-05-07_ 