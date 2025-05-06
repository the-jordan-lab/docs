# Lab Agent Guide (v2)

Welcome! This guide explains how to use the **chat-driven lab management system** that lives inside this repository.  It covers everyday workflows (for researchers) _and_ advanced features (for power users / maintainers).

---

## 1. What *is* the Lab Agent?

The Lab Agent is an AI assistant that turns plain-language instructions (typed in a chat window) into structured actions:

* Creating or updating YAML files in `Protocols/`, `Experiments/`, or `Projects/`  
* Suggesting metadata ("Smart-Fill") using past lab records or PubMed  
* Committing changes, opening GitHub Issues, or drafting Pull Requests so the PI can review

Think of it as a smart electronic lab notebook that lives entirely in this repo and **never** forgets to save or commit your work.

---

## 2. Quick-Start Checklist (⚡ _5 minutes_)  
1. **Open this repo in GitHub Codespaces** (or locally with Dev Containers).  
2. **Set secrets** (once per user):  
   • `OPENAI_API_KEY` – required for embeddings & Smart-Fill  
   • `GITHUB_TOKEN` – Codespaces usually injects one automatically  
3. Wait for the container to build (it installs Python deps & starts the Agent runner automatically).  
4. **Open the _Cursor_ / _Copilot Chat_ tab** inside VS Code.  
5. Start talking! e.g. `"Create a new experiment using the cell staining protocol tomorrow at 10 AM"`.

> 💡 **Tips**  
> • If chat replies look like JSON function calls, _that's expected_ – the Agent is planning deterministic actions.  
> • All generated files & commits appear immediately in the Explorer + Git view.

---

## 3. Everyday Workflows

### 3.1 Create a Protocol
```text
User: Create a protocol called "RNA Extraction v2" based on the existing v1 but increase incubation to 15 min.
Agent → creates `Protocols/rna_extraction_v2.yaml`, commits it, and tells you the file path.
```

### 3.2 Start an Experiment
```text
User: I'm starting an experiment tomorrow using RNA Extraction v2 on sample 123.
Agent → scaffolds an experiment YAML in `Experiments/`, auto-fills metadata, commits, and links it to the protocol.
```

### 3.3 Log Results / Update Status
```text
User: Mark experiment EXP-0005 completed and add results "Yield was 250 ng/µL".
Agent → updates the YAML, validates required fields, commits, and updates TASKS.md.
```

### 3.4 Get Smart-Fill Suggestions
```text
User: Suggest metadata for cell line HeLa in my staining experiment.
Agent → returns top suggestions from previous experiments + PubMed if needed.
```

### 3.5 Open an Issue for PI Review
```text
User: Flag experiment EXP-0005 for PI review.
Agent → `gh issue create` with a pre-filled title/body and commits reference.
```

---

## 4. Available Commands / Phrases
The Agent understands natural language, but these verbs map 1-to-1 with internal functions.  
| Action | Example Phrase | Notes |
| --- | --- | --- |
| **create_protocol** | "Make a protocol for western blotting" | Will duplicate `Templates/protocol_template.yaml` |
| **create_experiment** | "Plan an experiment using XYZ protocol next Monday" | Auto IDs the file with date & researcher |
| **update_experiment** | "Add results to EXP-0007" | Triggers validation if `status: completed` |
| **suggest_metadata** | "Suggest antibody concentration for HeLa staining" | Uses embeddings + PubMed |
| **commit_and_push** | Usually automatic | Manual call: "Commit with message ..." |
| **open_issue** | "Open an issue titled ..." | Uses `gh issue` CLI |
| **open_pr** | "Open a draft PR for my changes" | Creates branch & PR |

---

## 5. Where Things Go
```
Protocols/    standard procedures (YAML)
Experiments/  individual runs / lab sessions (YAML)
Projects/     high-level grouping (YAML)
Data/         small data or links to external storage
Templates/    starting skeletons for new YAMLs
Agent/        Python code for the runner + embeddings
```
The Agent follows these conventions automatically. If you add files manually, keep the same structure so Smart-Fill can find them.

---

## 6. Logs & Task Tracking
| File | Purpose |
| --- | --- |
| **CHANGELOG.md** | Auto-appended summary of each significant action |
| **TASKS.md** | Checklist for ongoing lab or dev tasks; Agent checks boxes when done |
| **SESSION_LOG.md** (optional) | Human-readable session summaries you or the Agent can append |

You can always skim these files (or GitHub commit history) to catch up after a break.

---

## 7. Troubleshooting & FAQ
**Q 1. The Agent says it can't find my protocol.**  
• Check the filename (lowercase, underscores instead of spaces).  
• Run `Agent/agent_runner.py` again if you added the file manually – it re-indexes on start.

**Q 2. `gh` command not found / authentication failure.**  
• Inside the container run `gh auth status`. Follow prompts if unauthenticated.  
• Codespaces usually sets this up, but personal tokens may expire.

**Q 3. Smart-Fill suggestions are empty.**  
• Ensure `OPENAI_API_KEY` is set (`echo $OPENAI_API_KEY`).  
• There may be no similar content yet – add more protocols/experiments.

**Q 4. I want to edit YAML manually.**  
• That's fine! The Agent will pick up changes on the next run.  
• Remember to commit – or ask the Agent _"Commit with message ..."_.

---

## 8. Advanced Usage
* **Branching/PR Flow** – Say *"Create a branch feature/rna-cleanup and open a draft PR"*.  
* **Bulk imports** – Paste multiple steps; the Agent can chain actions in one go.  
* **External RAG** – If a term isn't in the repo, Smart-Fill queries PubMed; the Agent cites article titles in suggestions.

---

## 9. Developer Notes (for Maintainers)
* Runner entry point: `Agent/agent_runner.py`  
* Add new functions by implementing `handle_<function>` then registering it in the Agent prompt.  
* Embedding index lives in `Data/chroma_index/`; delete it to rebuild from scratch.  
* Tests: `pytest` coming soon (stub).

---

Made with ☕ and 🤖.  Enjoy streamlined, reproducible record-keeping! 