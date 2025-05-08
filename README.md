# Jordan Lab Doc Repo

---

# Lab Workspace Quick-Start

Welcome to the Lab Codespace! This environment is pre-configured for you. Just follow these steps:

## 🚀 1. Open the Codespace

- Click "Code" > "Codespaces" > "Create codespace on main" (or your assigned branch).

## ⏳ 2. Wait for Setup
- The environment will build automatically. This takes ~1-2 minutes the first time.
- All dependencies, the Lab Agent, and required secrets (like the OpenAI API key) are pre-loaded.

## 💬 3. Start Chatting
- Open the **Cursor** or **Copilot Chat** tab in VS Code.
- Type your request (e.g., "Create a new experiment using the cell staining protocol tomorrow at 10 AM").
- The Lab Agent will handle the rest!

---

### FAQ
- **Do I need to set up any API keys or secrets?**
  - _No!_ All required secrets are injected automatically. You cannot see them, but the Agent can use them.
- **What if I see a warning about missing tools?**
  - Try rebuilding the container (F1 > "Rebuild Container"). If issues persist, contact @james-m-jordan.
- **Where do my files and issues go?**
  - Protocols, experiments, and projects are saved in their respective folders. Issues you create are logged and visible in the repo (see below).

---

### For Maintainers
- **OpenAI API Key**: Add it as a Codespaces secret at the repo level (`OPENAI_API_KEY`).
- **GitHub CLI Authentication**: The CLI is pre-installed, but requires one-time auth per user:
  ```bash
  gh auth login
  # Choose GitHub.com → HTTPS → Paste a token with 'repo' scope
  ```
- **Auto-Issue Tracking**: Issues are automatically added to `TASKS.md` and `ISSUES_LOG.md` via hooks.
- **Robot Context**: `ROBOT_README.md` contains repository structure information for AI assistants.
- For more advanced setup or troubleshooting, see `ENVIRONMENT_SETUP.md` and `LAB_AGENT_GUIDE.md`.

---

Enjoy your streamlined lab experience!

---

## 🚀 Quick Start (for Researchers)

1. **Open in GitHub Codespaces** (or locally with Dev Containers)
2. **Set secrets** (once per user):
   - `OPENAI_API_KEY` (for Smart-Fill)
   - `GITHUB_TOKEN` (usually set by Codespaces)
3. Wait for the container to build (Python deps & agent auto-start)
4. **Open the _Cursor_ / _Copilot Chat_ tab** in VS Code
5. Start talking! e.g. `"Create a new experiment using the cell staining protocol tomorrow at 10 AM"`

> **New to the system? Start with [LAB_AGENT_GUIDE.md](./LAB_AGENT_GUIDE.md) for hands-on instructions and examples.**

---

## ✨ How it feels to use (Chat Example)

```
User: Create a protocol called "RNA Extraction v2" based on the existing v1 but increase incubation to 15 min.
Agent → creates `Protocols/rna_extraction_v2.yaml`, commits it, and tells you the file path.

User: I'm starting an experiment tomorrow using RNA Extraction v2 on sample 123.
Agent → scaffolds an experiment YAML in `Experiments/`, auto-fills metadata, commits, and links it to the protocol.

User: Mark experiment EXP-0005 completed and add results "Yield was 250 ng/µL".
Agent → updates the YAML, validates required fields, commits, and updates TASKS.md.
```

---

## 🛠️ Troubleshooting & FAQ
- If you get stuck, see the [Troubleshooting & FAQ section in LAB_AGENT_GUIDE.md](./LAB_AGENT_GUIDE.md#7-troubleshooting--faq)
- For developer/maintainer info, see the end of this README and the Guide.

---

# Implementation Plan: Chat-Driven Lab Management System

Overview and Goals

This plan outlines a smart, chat-driven lab management system for the the-jordan-lab/docs repository. The system will operate entirely within GitHub Codespaces, requiring no local setup. Users (students or researchers) will interact via natural language chat with an AI Cursor agent to manage lab protocols, experiments, and data. The agent will translate instructions into structured YAML files and perform actions through a deterministic Python task-runner. Key goals include:
	•	Monorepo Organization: A unified repository structure (Protocols/, Projects/, Experiments/, Data/, Templates/, etc.) to centralize protocols, experiment plans, data, and templates for easy access and traceability ￼. This eliminates scattered notes or "it's on my machine" issues by keeping all records in one place, under version control.
	•	Fully Containerized Environment: A .devcontainer configuration ensures a consistent, reproducible development environment on Codespaces ￼. This allows any lab member to launch a ready-to-use workspace with all necessary tools (Python, libraries, etc.) pre-installed, avoiding manual setup.
	•	Cursor Chat Agent with Function Calling: Use an AI assistant (Cursor) that interprets lab instructions (e.g. "Plan a PCR experiment using antibody X next week") and produces structured outputs. The agent employs OpenAI-style function calling to output JSON/YAML actions, enabling reliable multi-step workflows where the AI can take actions like creating files or updating records ￼. The structured output approach ensures the AI's responses strictly conform to expected schemas for deterministic execution.
	•	Deterministic Task Runner: A Python-based task-runner will consume the agent's JSON instructions and execute them (create/edit YAML files, commit to git, etc.). This separation guarantees that while the AI suggests actions, only the controlled code performs changes, ensuring reproducibility and preventing non-deterministic AI direct edits. Every action is logged and versioned.
	•	"Smart-Fill" Metadata Suggestions: The system will intelligently auto-populate metadata fields (e.g. reagents, conditions) to reduce user burden. It leverages:
	1.	Vector embeddings of the repository's own content – protocols and past experiment YAMLs – to find relevant context and similar entries for suggestions ￼.
	2.	User history to personalize suggestions (e.g. frequently used cell lines or instruments by that user).
	3.	Lightweight RAG (Retrieval-Augmented Generation) from trusted external sources like PubMed for domain knowledge (e.g. auto-suggesting an antibody target or concentration from literature).
	•	GitHub Integration & Automation: Tight integration with GitHub features for collaboration and oversight. The task-runner will auto-create Issues, Draft PRs, and commits with descriptive messages as needed. This ensures the lab PI and team have full visibility of changes and can review via normal GitHub workflows. Automation is favored (with auto-commit/auto-PR) to streamline usage, but the system will request user clarification when confidence in an action is low or ambiguous.
	•	Persistent Tracking & Documentation: The repository will include Markdown documents to track tasks and status across AI sessions. This allows the AI (and users) to resume work with full context after interruptions. A human-readable "LabAgent Guide" will also be provided so any team member can understand how to use the system or pick up where someone left off.

By implementing these components, the lab management process becomes centralized, reproducible, and user-friendly, turning conversational instructions into documented lab actions with minimal friction.

System Architecture Overview

1. Codespace & Dev Container: The project will use GitHub Codespaces with a custom .devcontainer. The devcontainer includes all dependencies (Python, necessary libraries, vector DB, GitHub CLI, etc.) and configuration needed to run the agent and task-runner. This guarantees every user's environment is identical and ready-to-go ￼. When a user opens the repository in a Codespace, the container builds automatically, installing the AI agent backend and tools. No local installs are required – "it works on my machine" problems are eliminated by containerizing the dev environment ￼.

2. Cursor Agent (LLM): At the core is a chat-driven AI agent (powered by a language model such as GPT-4 with function calling support). The agent runs in the Codespace (either via a VSCode extension or a CLI interface) and accepts natural language instructions. A custom function schema is defined for lab management actions (e.g. create_protocol, start_experiment, log_result, open_issue, etc.), each with a JSON schema for arguments. The agent is instructed (via system prompt) to use these functions to perform tasks rather than free-form text. For example, if the user says "Create a new protocol for cell staining with antibody ABC," the agent will output a JSON invoking create_protocol{name: ..., type: ..., fields: ...}. This structured output approach (with JSON mode strict schemas) ensures the model's output can be parsed deterministically ￼. The Cursor agent essentially plans the steps and expresses them in a machine-readable form.

3. Python Task-Runner: A persistent Python process (started on container launch) listens for the agent's function call outputs (perhaps via a file or IPC mechanism). When the agent emits a JSON action, the task-runner parses it and executes the corresponding Python function. This could be implemented with a loop reading actions from the agent's API or via the Cursor MCP (Model Context Protocol) plugin interface ￼ ￼. Each function in the task-runner is carefully written to be idempotent and deterministic – performing exactly the file system or Git operation specified. For instance, create_protocol will scaffold a new YAML file in Protocols/ with the provided content, and open_issue will call the GitHub API or CLI to create an issue. After execution, the task-runner can feed a result back to the agent (e.g. success or any output) to continue multi-step workflows. This design lets the AI chain multiple actions (tool use) reliably, akin to an agentic workflow where the LLM can "think then act" in cycles until the instruction is fulfilled ￼.

4. Data Storage (YAML & Git): All lab information is stored as human-editable text (YAML or Markdown) in the repository. The monorepo layout organizes this data (detailed in the next section). By using text-based YAML, we ensure that adding or editing entries (protocols, experiments, etc.) is transparent and trackable via Git diff. YAML is chosen for its readability and structure – it serves as a simple database for lab metadata. Notably, YAML protocols are already used in some lab automation contexts as a high-level experiment language ￼, underscoring its suitability. The Git history provides an audit trail; every change by the agent is committed with a message, so one can trace what happened when, by whom (the agent will sign off with the user's name or a bot identity). This versioning also aids reproducibility: if a protocol changes over time, one can retrieve exactly what protocol was used for an experiment by referencing commit IDs or tags.

5. Smart-Fill Recommendation Engine: Alongside the agent and runner, the architecture includes a metadata suggestion subsystem. This is composed of:
	•	An Embedding Index built from the repository's contents. On Codespace startup (or on demand), a script scans files in Protocols/ and sample YAML entries from Experiments/ and Projects/, converting them into vector embeddings. This uses a pre-trained text embedding model (e.g. SentenceTransformers or OpenAI embeddings). The result is a lightweight vector database (possibly just an in-memory FAISS index or a local SQLite via ChromaDB) that can be queried for similarity.
	•	A History Tracker that maintains context about the current user and recent actions. For example, if user "Alice" has recently done several cell culture experiments, the system notes the cell lines or treatments she used frequently. This could be as simple as storing a JSON with per-user stats (e.g. last used protocol, commonly used reagent names) updated after each session.
	•	External Knowledge Fetcher: A minimal integration to query external databases like PubMed or protocols.io when needed. This will not be a persistent heavy service, but rather an API call using something like Biopython's Entrez or a requests call to NCBI E-utilities. For instance, if a user asks for a protocol that includes a specific antibody, and the agent doesn't find it in local files, it might query PubMed for that antibody to gather suggested usage or metadata (publication info, recommended dilutions, etc.). Only trusted sources (PubMed, DOI resolvers) are used to avoid misinformation.

All these components come together such that a user can simply describe what they want, and the system handles the plan → action → record → commit cycle automatically. Below, we detail the implementation plan for each part of this architecture.

Repository Structure and Scaffolding

We will organize the-jordan-lab/docs as a monorepo containing all relevant subfolders for protocols, experiments, data, etc. The following folders (and key files) will be created in the root of the repository:
	•	Protocols/ – contains standard operating procedures and experimental protocols. Each protocol is a YAML (or Markdown + YAML front-matter) file describing a repeatable procedure. Convention: Use a short descriptive name for the file, plus a version or date if needed (e.g. Protocols/cell_staining_v1.yaml). These files include fields like name, description, steps, materials, version, author, etc. For example, a protocol YAML might look like:

name: Cell Staining Protocol
id: PROT-0001
description: Protocol for immunofluorescence staining of cells
author: Alice Smith
created: 2025-05-05
version: 1.0
materials:
  - Antibody: Anti-XYZ (1:500 dilution)
  - Stain: DAPI
  - Buffer: PBS 1X
steps:
  - "Fix cells with 4% PFA for 10 minutes."
  - "Wash 3x with PBS."
  - "Add primary antibody (Anti-XYZ) for 1 hour at RT."
  - "Wash 3x with PBS."
  - "Add DAPI stain for 5 minutes."
  - "Wash and image."
notes: |
  This protocol is derived from Doe et al. 2023.

Each protocol gets a unique ID or name. We will include a brief README.md in Protocols/ explaining how to add new protocols via the agent and the YAML schema expected (for human reference).

	•	Projects/ – groups related experiments under broad project titles (e.g., a project might be "Tumor Growth Study 2025"). Each subfolder or YAML file in Projects/ outlines a project's goals, team, and links to relevant experiments. We may use one YAML per project (e.g. Projects/tumor_growth_2025.yaml) containing metadata: title, description, lead, team_members, associated_protocols, and a list of experiment IDs under it. This helps organize experiments logically (one project to many experiments relationship).
	•	Experiments/ – records of individual experiments or lab sessions. Each experiment is a YAML file (or folder) that captures the plan, execution, and outcome of an experiment. Convention: We use a timestamp or incremental ID in the filename for uniqueness, possibly prefixed by project or user. For example, Experiments/2025-05-10_cell_staining_Alice.yaml or Experiments/EXP-0002.yaml. The YAML fields include:
	•	Reference to Protocol: e.g. protocol: cell_staining_v1 (which correlates with a file in Protocols/). If a protocol is modified for this experiment, the changes can be noted in a deviations: field.
	•	Parameters/Metadata: e.g. date, researcher, sample_id, reagents_used, instrument, settings, etc. The agent's Smart-Fill will attempt to populate these. For instance, if protocol is known and has expected reagents, it can auto-fill the reagents_used list.
	•	Procedure Steps: Optionally, a list of steps (could be auto-copied from the protocol for completeness, then annotated with any changes).
	•	Results: free-form notes or links to data outputs (if small data, possibly included; if large, stored in Data/).
	•	Status: e.g. status: ongoing or completed or planned – to track the state.
	•	Links: to project, or related experiments.
Example snippet for an experiment YAML:

experiment_id: EXP-0002
project: Tumor Growth Study 2025
title: Staining Tumor Cells with Anti-XYZ
date: 2025-05-10
researcher: Alice Smith
protocol: Cell Staining Protocol (v1.0)
materials:
  Antibody: Anti-XYZ (lot #12345)
  Cell line: HeLa
parameters:
  Cell_count: 1e5
  Incubation_time: 60  # minutes
results:
  images: ["Data/Images/exp0002_image1.png", "Data/Images/exp0002_image2.png"]
  observations: "Strong fluorescence observed in nucleus."
status: completed

The plan will include scaffolding a template experiment YAML in Templates/ (see below) that lists all required fields, which the agent can clone and fill for each new experiment to ensure completeness.

	•	Data/ – storage for data outputs or references to data. Large raw data might reside outside Git (e.g. on cloud or a drive), but small data files or processed results can be saved here. We will organize subfolders by experiment or project, for example Data/Images/EXP-0002/ for images from experiment 0002, or Data/Sequencing/ProjectX/... etc. If data is external, the YAML records in Experiments can contain pointers (URLs or filesystem paths) to where the data is stored. A README.md in Data/ will clarify how to add data or link external data (the agent could automate adding placeholders or verifying links).
	•	Templates/ – contains starter templates for various YAML structures (protocol, experiment, project). For instance:
	•	Templates/protocol_template.yaml with all fields blank or example values.
	•	Templates/experiment_template.yaml with required sections (and perhaps comments).
	•	Templates/project_template.yaml.
The Cursor agent's task-runner will use these templates when scaffolding new files to ensure consistency. Deterministic conventions (like which keys to include and in what order) come from these templates, so all YAML files follow a standard format. This reduces variability and makes it easier to parse or validate entries later.
	•	Agent/ (or automation/ or similar) – this folder will hold the code for the AI agent integration. E.g., a Python module agent_runner.py for the task-runner, any utilities for embedding or PubMed queries, and perhaps prompt templates for the LLM. Keeping this code in the repo means it's versioned and can be improved via pull requests like any other code. This folder can also include the function definitions (possibly in JSON format or as Python descriptors) that define the interface between the LLM and the functions.
	•	Root files: In the repository root, we'll add:
	•	A detailed README.md explaining the repository purpose and structure. It will outline each directory and how they fit into lab workflows (essentially summarizing parts of this plan for end-users). It will emphasize that this is an electronic lab notebook / management system and how to get started with it in Codespaces.
	•	Documentation files for the agent system:
	•	LAB_AGENT_GUIDE.md (name tentative): Documentation for users on how to interact with the chat agent. For example, how to phrase requests, what the agent can do, and tips (like "you can ask the agent to show an experiment summary or to search protocols by keyword"). It will also describe the fallback behavior (when the agent might ask questions) so users know what to expect.
	•	TASKS.md: A Markdown task tracker (details in a later section) listing outstanding development tasks or lab to-dos. This might be used both for continuing the implementation of the system and for high-level lab tasks that the AI can help manage. The idea is to enable the AI (and humans) to see a to-do list and mark items done across sessions.
	•	CHANGELOG.md or STATUS_LOG.md: A log that the system (and users) update each session to summarize what was done. For example, each time the agent runs a major command, it appends "2025-05-10: Created experiment EXP-0002 (Cell Staining) via agent for Alice." Keeping this log in markdown ensures that if the conversation context is lost, the next session can quickly reconstruct it by reading the recent log. It also provides the PI a quick way to see recent activity at a glance without combing through individual commits.

Scaffolding these folders and files will be the first step. We will create stub files (even if empty or with placeholder text) for templates and documentation so that everything is in place. With this deterministic structure, the AI agent always knows where to put or find things. For example, when asked to create a new protocol, it knows to place a YAML in Protocols/ and update any relevant index or list.

This monorepo approach centralizes all experimental knowledge. As Labguru advertises, centralizing experiments, protocols, and data in one hub improves collaboration and eliminates lost information ￼. Our structure echoes that philosophy: experiments link to protocols and data, projects link to experiments, etc., all under one version-controlled roof.

Codespaces Environment and DevContainer Setup

To make the system fully operational inside GitHub Codespaces, we define a .devcontainer configuration in the repository. This includes at minimum a devcontainer.json and a Dockerfile or image specification that sets up:
	•	Base Image & OS: Use an image like mcr.microsoft.com/devcontainers/python:3.10 (for Python environment) or a lightweight Ubuntu with Python. The image should have git and basic tools.
	•	Python Environment: Install Python 3 and required pip packages. These likely include:
	•	OpenAI SDK (for calling the GPT API, if using OpenAI's service for the agent).
	•	LangChain or similar (optional, for structured output handling or vector store management).
	•	faiss-cpu or chromadb (for embeddings storage and similarity search).
	•	PyYAML (for reading/writing YAML files).
	•	GitPython or GitHub's gh CLI (to automate Git and GitHub actions if not using direct CLI).
	•	biopython (for PubMed Entrez API) or requests for external queries.
	•	Any Cursor-specific agent library if needed (if Cursor provides a Python package to interface with MCP or agent API).
	•	Possibly small utility libraries for text processing, etc.
	•	VS Code Extensions: The devcontainer can recommend/install extensions such as:
	•	GitHub Codespaces / Dev Containers extension (usually default).
	•	YAML extension for nice editing.
	•	Python extension for coding.
	•	If available, a Cursor extension or GitHub Copilot Chat – anything to facilitate the chat interface in the VSCode environment. If Cursor has an extension for VSCode, include it (or instructions to connect to Cursor).
	•	Environment Variables: We'll configure any needed environment vars. For example, OPENAI_API_KEY (which the user would supply via Codespaces secrets for security). Or a GITHUB_TOKEN (Codespaces provides a token by default for the repo, which can be used with gh CLI to auth to that repository's scope). The devcontainer might include an .env or use the Codespaces secrets to ensure the agent can authenticate to required services (OpenAI, GitHub).
	•	Post-create Setup: Use the postCreateCommand to run setup tasks, such as:
	•	Index the repository content for embeddings (so the vector store is ready).
	•	Possibly launch the agent backend. For example, start the Python task-runner or MCP server. We might run a command like python agent/agent_runner.py --serve & to have it listening in the background.
	•	Run any migrations or checks (e.g., ensure the Templates folder has the latest schema, or verify YAMLs).
	•	Print a welcome message with next steps (maybe a reminder to open the chat interface).

Once configured, any contributor can open a Codespace and within minutes have a fully functional AI-assisted lab notebook environment. The reproducibility is key: "Dev Containers... ensure every developer uses the same environment, eliminating the 'works on my machine' problem" ￼. In our case, it ensures every student in the lab has the same tools and sees the same AI behavior.

Notably, no local installation is necessary. If someone prefers local development, they could use VS Code with the Remote - Containers extension to instantiate the same devcontainer locally. But the target is to use GitHub Codespaces in the cloud for ease. This means even on an iPad or a low-power laptop, a user can access the full system via a browser.

We also ensure that the Codespace has no external server dependencies: all logic runs inside (the LLM calls go out to OpenAI or are handled by Cursor's service, but we are not hosting our own server outside). The agent and task-runner run within the container. There's no need to deploy separate web services or databases – we rely on the GitHub platform (issues, PRs) for collaboration and lightweight local stores (YAML files, embeddings index) for data.

Cursor Agent & Function-Calling Task Orchestration

The Cursor agent is the AI assistant that interprets user instructions and decides which actions to perform. To implement this reliably, we will use OpenAI's function calling JSON protocol (or an equivalent) to constrain the agent's output to a set of pre-defined actions ￼. This ensures determinism and safety – the agent can't execute arbitrary code or make changes unless it's through one of our vetted functions.

Defining Functions (Actions): We enumerate the main actions the agent should handle in a JSON schema format to register with the LLM. For example:
	•	create_protocol(name: str, purpose: str, steps: list, materials: list, version: str): Creates a new protocol YAML in Protocols/. The agent will fill in fields like steps and materials if provided (or use template placeholders).
	•	create_experiment(project: str, protocol: str, date: str, researcher: str, parameters: dict): Creates a new experiment record in Experiments/. The agent should supply a unique ID or date for the experiment. Many of these arguments can come from conversation (or be guessed by Smart-Fill).
	•	update_experiment(id: str, results: str): Log results or update status of an experiment.
	•	suggest_metadata(field: str, context: str): A special function where the agent can call into the Smart-Fill system. This might trigger the Python side to do an embedding lookup or external search and return suggestions. (This could also be handled implicitly by the agent's knowledge, but having a tool function allows deterministic retrieval from external sources.)
	•	open_issue(title: str, body: str): Creates a GitHub Issue for tracking. E.g., if a user says "Flag this for PI review," the agent might call this to open an issue.
	•	open_pr(branch: str, title: str, body: str): Creates a Draft Pull Request. Typically used after significant changes (like adding multiple files for a new project) to request review. The task-runner can gather all uncommitted changes on a branch and push them, then open PR.
	•	commit_and_push(message: str): Commits current staged changes with the given message and pushes to GitHub. (The workflow could be commit after each atomic action or batch commit; we will likely commit at logical milestones to keep history readable.)

These function definitions (with their parameter schema and documentation strings) will be given to the LLM in the system message or via the Cursor MCP interface. This way, when the user instructs something that maps to an action, the model will choose to output a function call JSON.

Example Interaction:
User: "I'm starting a new experiment tomorrow using the cell staining protocol on sample 123, please set it up."
System/Agent (internally): The agent parses this and decides it needs to create a new experiment entry. It gathers details: protocol = "cell staining protocol", date = tomorrow's date, researcher = (from user profile or ask), sample id = 123. It might also recall from embeddings that "cell staining protocol" expects an antibody and cell line, and use Smart-Fill to guess or ask. Finally, it responds not in natural language but with a function call, e.g.:

{
  "function": "create_experiment",
  "arguments": {
    "project": "Unassigned",
    "protocol": "Cell Staining Protocol (v1.0)",
    "date": "2025-05-06",
    "researcher": "Alice",
    "parameters": {
       "sample_id": "123",
       "cell_line": "HeLa",
       "antibody": "Anti-XYZ"
    }
  }
}

The Python task-runner receives this JSON and executes create_experiment.

Python Task-Runner Implementation: In agent/agent_runner.py, we will implement a loop (or use an asynchronous event system if integrated with Cursor's MCP) to handle incoming function calls. For each function:
	•	Log the action to console or a log file (for debugging/audit).
	•	Perform the action:
	•	For file creation, use template files from Templates/, fill in the YAML fields from args, and write to the appropriate path. Mark the new file with a new experiment ID if not provided (the runner can generate the next ID by simple increment or timestamp).
	•	For updates, open the YAML, modify the necessary fields, and save.
	•	For suggestion retrieval (if suggest_metadata is called), call the embedding search or PubMed API accordingly (more details in Smart-Fill section) and return the results to the agent. The agent might then decide which suggestion to use and continue the function calls.
	•	For Git operations, use the GitHub CLI (gh) or a library. For example, open_issue can run gh issue create -t "title" -b "body", or use PyGithub if we prefer Python. Similarly, commit_and_push can run shell git commands or use a library to commit and push.
	•	Handle errors gracefully: if something fails (e.g. file already exists, or network error opening an issue), catch it and send a message back to the agent (the LLM) indicating failure. The agent can then relay to user or attempt a different approach. Ensuring error messages are succinct and useful (e.g. "Failed to create file, it may already exist") will help if the AI or user needs to intervene.

After each significant action, the task-runner can optionally call back to the agent with a brief result. For example, after create_experiment, it could respond with a message like: "Experiment EXP-0002 created in Experiments/. Ready for additional details." or supply the new experiment ID as return value. This can be done via the OpenAI function calling mechanism by returning a value. The agent might use that to inform its next message to the user.

The Cursor MCP route: If using Cursor's Model Context Protocol, we would implement an MCP server in the container that Cursor (the editor) connects to. This MCP server would expose endpoints corresponding to our functions. The advantage of MCP is tighter integration (Cursor can call them as if the AI decided to), and it allows using Cursor's UI features. Either approach (OpenAI API or MCP) results in similar behavior. Since the question references "Cursor's function-calling JSON protocol," it suggests we can use either OpenAI's API with JSON mode or Cursor's own mechanism. We will plan for OpenAI's API usage for generality, but note that the devcontainer can support running Cursor's own environment if needed.

Determinism and Schema Enforcement: We will use the strict: true setting for structured outputs if available ￼. This means the model is required to produce exactly the JSON schema for function arguments. The benefit is 100% reliable parsing of outputs into our functions (no misformatted JSON) ￼. By constraining the AI to these schemas, we essentially get a guarantee that the agent's "thoughts" manifest as concrete, reproducible actions in our system, not just suggestions.

Multi-step Workflows: The user's request may require multiple steps. The agent can call a sequence of functions in a single conversation turn or multiple turns. For instance, "Set up a new project for RNA extraction and create two experiments in it" might lead to:
	1.	create_project (makes a project YAML).
	2.	create_experiment (for experiment 1 under that project).
	3.	create_experiment (for experiment 2).
	4.	open_pr (open a draft PR with all these new files, maybe tagging the PI).

The agent will do this stepwise, possibly asking for confirmation or missing info in between. The task-runner will execute each in order. If any step requires more info (say the project description wasn't provided), the agent could either guess (Smart-Fill could provide a generic description) or ask the user for that detail before proceeding.

This agent-runner loop essentially forms an automated lab assistant. It's important that by default, it tries to fill in blanks automatically (using intelligent defaults or suggestions) to avoid pestering the user. Only when something is truly ambiguous or critical (confidence is low) will it pause to ask (see Automation vs Clarification below for strategy).

Security Considerations: All actions are local to the repo or via GitHub API with the user's token, so there's minimal risk. We ensure the agent cannot execute arbitrary shell commands beyond our allowed functions. It also should not have internet access beyond what we explicitly code (like PubMed queries), which prevents it from doing unapproved external calls or data leak. (In a production setting, we'd further sandbox this if needed.)

Smart-Fill Metadata Suggestion System

One highlight of this system is Smart-Fill, which reduces the manual effort in providing complete metadata for protocols and experiments. This system combines local knowledge and external references to suggest likely values for fields.

A. Vector Embeddings of Repo Content:
We will preprocess the content of our protocols and templates to create an embedding index. For example:
	•	For each protocol in Protocols/, compute an embedding of its text (including name, description, steps). Store these in an index keyed by protocol ID.
	•	For each existing experiment YAML, embed its contents or at least key fields (title, protocol used, materials, results summary).
	•	For each project, embed its description and scope.
	•	Possibly also embed any lab glossary or inventory if available (e.g., list of antibodies the lab commonly uses, list of cell lines, etc. – this could simply be another YAML file we maintain).

We'll use a model like OpenAI's text-embedding-ada-002 or a local alternative (to avoid external calls, maybe a locally hosted MiniLM or SBERT model). The embeddings (vectors) are stored in memory or a small database file. The suggest_metadata function in our runner can query this index with a question or partially known info.

Use Cases of Embeddings:
	•	Protocol Suggestion: If a user describes an experiment aim but doesn't specify a protocol, the agent can search the protocol embeddings for relevant ones. E.g., user says "I want to count cells after treatment" – the agent finds a "Cell Counting" protocol in the index as a likely match.
	•	Parameter Guessing: If an experiment is created with a known protocol, the agent can look up similar experiments (via embeddings of experiment descriptions) to see what parameters were used. For instance, if doing "cell staining on HeLa cells," and previously an experiment had cell_line: HeLa and used antibody X at 1:500, it might suggest the same antibody and dilution if context matches.
	•	Preventing omissions: The vector search can be used to ensure completeness. Suppose an experiment YAML is missing the antibody field but protocol suggests one – the agent can notice from the protocol text that an antibody is needed and prompt or auto-fill it.
	•	Contextual answers: If the user asks a question like "What was the result of the last experiment using protocol Y?" the agent can embed the query and find the relevant experiment record to answer.

Because these suggestions come from the lab's own data, they are highly relevant and help maintain consistency. As one reference notes, "embeddings help LLMs generate more precise responses by retrieving contextually relevant information" ￼. We are applying that by feeding the agent with relevant snippets when needed. The agent can incorporate retrieved data either directly into its function arguments or as additional context in the conversation.

B. Per-User Activity History:
We will maintain a simple log or profile for each user (perhaps identified by their GitHub username or a provided name). This could be a JSON in Agent/user_profiles.json with entries like:

{
  "alice": {
     "last_active": "2025-05-05",
     "frequent_protocols": ["Cell Staining Protocol", "Flow Cytometry Protocol"],
     "frequent_samples": ["HeLa", "Mouse fibroblast"],
     "recent_experiments": ["EXP-0002", "EXP-0005"]
  },
  "bob": {
     ...
  }
}

This data can be updated automatically: each time an experiment is created, add to that user's recent experiments; each time they use a protocol, increment a counter. The agent can use this to tailor suggestions. For example, if Alice usually works with HeLa cells, the agent might default to cell_line: HeLa in a new experiment unless told otherwise. Or for Bob, maybe default to a different cell type.

This personalization makes the agent feel more "assistant-like" and further reduces repetition. It also helps disambiguation: if two possible protocols fit a request but one is the user's favorite, pick that.

C. External RAG (e.g. PubMed):
For expanding beyond the lab's internal knowledge, we integrate a minimal retrieval from external sources:
	•	PubMed queries: We can use NCBI's API to fetch article titles or abstracts related to a keyword. For instance, if a user mentions a gene or compound unknown to our system, the agent can do suggest_metadata("What is XYZ compound used for?") which our runner handles by querying PubMed for "XYZ compound protocol" or similar. The results (top 1-3) could be returned to the agent, which might glean that "Compound XYZ is often used as a staining agent in concentration 5 µM ￼" etc. The agent can then use that info to fill in details or cite sources.
	•	Protocols.io or other repositories: If internet access is allowed, the agent can search protocols.io via API (SciNote integration suggests many protocols are easily importable ￼). We won't focus on heavy integration due to time, but in future, the agent could fetch a template protocol from protocols.io if the lab doesn't have one internally.
	•	Safety and Trust: Only use well-known databases (PubMed, maybe ArXiv for methods) to avoid retrieving from random web sources. The assistant should cite or log any external info used, for transparency. Perhaps in the experiment notes it can add "Suggestion from PubMed: [citation]".

Smart-Fill Workflow:
When the agent is about to call a function but lacks some info, it has options:
	1.	Check embeddings: e.g., it has protocol name and wants default parameters – it queries similar experiments/protocols.
	2.	If embeddings yield clear result, fill the field automatically and proceed.
	3.	If still uncertain, attempt an external query if appropriate (e.g., unknown term).
	4.	If still uncertain or multiple possibilities, ask the user. For example: "I see two possible antibodies (Anti-ABC and Anti-XYZ) used in similar contexts. Which one are you using?" The agent would only reach this step if automation fails to give a confident answer.

Confidence can be gauged by embedding similarity score or by whether a field is critical and no data found. We'll design simple thresholds (e.g., if cosine similarity > 0.8 for a suggestion, assume it's good; if less, ask). This aligns with the requirement: prefer automation and auto-confirmation, with clarification only when confidence is low.

Metadata Completeness:
Upon creating or updating any YAML, the task-runner can include a validation step. Using a template or schema (possibly defined in Templates/ or via a JSON Schema in code), verify required fields are present (and not placeholders). If something is missing, the runner can prompt the agent for a follow-up. E.g., if after filling everything an experiment YAML still has cell_line: TBD or no results when marked completed, it can alert the agent or user. This ensures high-quality records. Essentially, the Smart-Fill tries to ensure that by the time an experiment is marked "completed," all fields (like date, protocol, materials, results, etc.) are filled and meaningful. This emphasis on completeness and accuracy improves reproducibility – future lab members can read the record and know exactly what was done ￼.

As an example of Smart-Fill in action: A student says "I treated cells with DrugX for 24 hours." The agent creates an experiment entry. The Smart-Fill might detect "DrugX" is not in our protocols, so it queries PubMed. It finds an article about DrugX usage. From that, it guesses the treatment concentration might be, say, 10 µM and the cell line used was MCF-7 (just hypothetical). It can fill treatment: DrugX 10µM for 24h and perhaps add a note "(suggested parameters from Doe et al. 2024)". If the student or PI later sees this and wants to adjust, they can – but the system provided a starting point automatically, which might otherwise require searching literature manually.

By combining internal data and external references, the lab agent becomes a proactive assistant, not just a passive recorder. It helps novices fill out forms correctly and reminds experienced users of details they might overlook.

GitHub Integration: Issues, PRs, and Commits

To integrate with the lab's existing workflow and ensure PI visibility, we leverage GitHub features via automation:

Automated Git Commits: Every change made through the agent is committed to the repository. We will configure the task-runner to stage and commit files at appropriate intervals. Likely approaches:
	•	One commit per high-level command: e.g., the user says "Record experiment results," which triggers updating two files – the experiment YAML and maybe a summary in a project file. The runner can commit both together with message "Add results for EXP-0002 (Cell Staining experiment)".
	•	Auto commit after creation: When a new protocol or experiment file is created, commit it immediately with message like "Create new protocol: Cell Staining Protocol v1.0" or "Log experiment EXP-0003 (staining test)".
	•	Structured Commit Messages: We might adopt a consistent format for commit messages to make them scannable. For example, prefix with the type of action: Protocol: for protocol additions, Experiment: for experiment updates, etc. e.g., "Experiment: EXP-0002 created for cell staining assay". We can also allow the agent to draft the commit message since it knows the context; however, to keep it deterministic, the task-runner could assemble the message from known parameters (like using the file's title or ID).
	•	The Cursor agent or the Cursor editor might have an AI commit message feature ￼, but since we want determinism, we'll rely on our own controlled messaging.

Git Branching and Pull Requests:
By default, the system could commit to the default branch (e.g., main) for immediate record-keeping. However, for oversight, we might prefer changes to go to a branch and open a PR for review. Two modes are possible:
	•	Direct Commit Mode: Simpler tasks (adding an experiment log, small updates) commit directly to main with the assumption that the PI trusts these incremental notes (just as they'd trust a student writing in a paper notebook). Since everything is logged, any issue can be fixed via another commit.
	•	Pull Request Mode: Significant or potentially sensitive changes (like adding a new protocol or a large batch of edits) trigger a Draft PR. The task-runner will create a new branch (maybe named lab-agent/<feature> or <user>-<task>), push the changes, then open a PR with a summary. The PR description can be generated by the agent, listing what was done, and perhaps tagging @PI (the PI's GitHub handle) for review. Mark it as Draft if not ready for merge. The PI can then review the changes in a familiar interface, comment, request changes, or approve and merge. The agent could monitor the PR status and report back if merged or if changes are requested (though that may be beyond MVP).

We will integrate with GitHub using either:
	•	GitHub CLI (gh): which is straightforward inside Codespaces. E.g. gh issue create ... or gh pr create .... We'll ensure gh is authenticated (Codespaces usually provides a token). This avoids handling tokens in code.
	•	PyGithub or GraphQL API: a Python library to create issues/PRs programmatically. This might be slightly more complex to implement but allows more fine-grained control within our Python runner (e.g., check if an issue exists, etc.). For our plan, gh CLI is sufficient and simpler.

Issue Creation:
Issues can be used for various purposes:
	•	Task tracking: If the agent encounters something it can't do automatically or needs human input later, it could open an issue as a reminder. For instance, "Experiment EXP-0005 lacks results – awaiting data" could be an issue assigned to the student to fill in results later.
	•	PI notifications: The system might open an issue to notify about a new project or a completed experiment. The PI (if subscribed) gets an email. The issue body can contain a summary, and perhaps the PI can respond with feedback right there.
	•	Feature requests/bugs: On the development side, if the AI fails to parse something or an error occurs, it could log it as an issue for developers to fix the agent. This way improvement needs don't get lost.

Automatic Linking: We can have the agent include references in commit messages or issue bodies to tie things together. E.g., commit message "Experiment EXP-0002... (see #12)" to refer to issue #12 about that experiment's review. Or in an issue describing a project, include links to the YAML files or PRs.

Mirroring with Gitea: The plan notes that Gitea is passively mirroring, so we don't need to do anything for Gitea specifically. We just push to GitHub; the mirror container will update Gitea. So effectively, all data is also available on the lab's internal Gitea server for backup. We should ensure not to use any GitHub-specific feature that doesn't mirror well. However, issues and PRs won't mirror to Gitea (since it's just a git mirror). The lab should be aware that the single source of truth for issues/PRs is GitHub (or at least the PI should check GitHub, not Gitea, for those). We'll clarify that in documentation.

PI Visibility & Notifications:
Once these integrations are in place, the PI can simply watch the repository on GitHub to get notifications of all commits and issues. Additionally, by involving the PI in PRs or having them assigned to oversee certain issue labels (like "review needed"), we create a workflow where nothing significant happens without the PI seeing it. The PI can also browse the Markdown logs (CHANGELOG.md or the commit history) at any time to see a chronological list of what the lab has done recently, ensuring transparency. This addresses the need for PI visibility with minimal friction: the students don't have to separately email updates or fill out reports – the system automatically produces those updates in the normal course of using it.

Persistent Task Tracking and Session Management

To facilitate working across multiple sessions (since AI context is not persistent unless stored) and enable resuming work seamlessly, we will implement Markdown-based trackers and logs.

Task Tracker (TASKS.md):
This file will list ongoing tasks or implementation steps, potentially in a checklist format. There can be two sections: Development Tasks (for building out this system itself) and Lab Tasks (for actual lab work to be done via the system). The AI agent can reference and update this file. For example:

## Lab Tasks
- [x] Set up project "Tumor Growth Study 2025" (created by lab agent on 2025-05-01)
- [ ] Run Experiment EXP-0007 (cell viability assay) – **in progress** (assigned to Bob)
- [ ] Analyze results of EXP-0005 and generate report – *pending data*

## Development Tasks
- [x] Scaffold repository structure (done in initial commit)
- [x] Implement create_experiment function
- [ ] Integrate PubMed metadata suggestions
- [ ] Write user guide documentation

The agent can mark items as done ([x]) when completed. For instance, after it finishes integrating PubMed suggestions, it would check that off (and perhaps add a line in a commit message referencing the task). This provides continuity – if the agent session ends and restarts, it can load TASKS.md to see what remains. It also helps a human collaborator see progress at a glance without diving into commit logs.

Session Log (SESSION_LOG.md or CHANGELOG.md):
This will be appended with each session or major action. We might structure it by date:

# Lab Agent Activity Log

## 2025-05-05 Session (Alice)
- Created protocol "Cell Staining Protocol v1.0" via agent.
- Created experiment EXP-0002 using "Cell Staining Protocol" for sample 123.
- Auto-filled experiment metadata (antibody Anti-XYZ, cell line HeLa).
- Committed changes and opened PR #5 for PI review.

## 2025-05-06 Session (Alice)
- Added results to EXP-0002 (observations and images).
- Marked EXP-0002 as completed. Commit abcdef1.
- PI approved PR #5 and merged.

This log provides full context to resume work at any time with full context. If the same or another user comes back a week later, they can read the latest session entry to recall what the agent did and what is pending. The agent itself, on start, can be programmed to read the last N lines of this log and incorporate that into its system message (so it knows the recent history without needing the conversation memory). This is critical because the AI model's conversational memory won't persist across sessions unless explicitly given.

We will have the agent update this log as part of its workflow. Possibly, after every high-level user command is done, append a bullet in the log file summarizing it. The task-runner can facilitate this (since it's safer for the runner to write to files than trusting the AI to phrase it consistently).

Resuming Context:
When starting a new conversation with the agent (say the next day), the system can:
	•	Inject the content of TASKS.md and the last session's log as part of the prompt (system or assistant message) to give the AI the context of what's happening.
	•	The user doesn't have to repeat where they left off; they can say "Let's continue with the viability assay" and the agent will understand from the log which experiment that is referring to and what the status is.

Documentation for Continuation:
We will document this mechanism in the user guide (LAB_AGENT_GUIDE.md). For example, instruct the user: "If you come back to the project after some time, read the Lab Agent Activity Log above to recall context. You can ask the agent what's the status of my experiments? – it will summarize using the log and current data. The agent keeps this log updated so you don't have to." This way, even if a different student takes over or assists, they can quickly get up to speed.

Finally, all these markdown files (TASKS.md, SESSION_LOG.md, etc.) are also visible on GitHub, meaning the PI or any collaborator can view them outside Codespaces too. This layered documentation ensures that even outside the AI interface, the project's state is well-communicated.

Automation vs. User Clarification Strategy

To meet the requirement of preferring automation with minimal user prompts, we design the agent's behavior as follows:
	•	Auto-Execution by Default: For any well-understood instruction, the agent will proceed to carry it out fully without asking "Are you sure?" or "Should I do it?" It will confirm by performing the action (and the user will see the result in the repository or via a brief summary message). For instance, "Log that I added 1 µL of reagent X" -> the agent finds the experiment YAML, updates it, commits "Update EXP-0003: added reagent X detail" – and then tells the user "Noted: I added that detail to EXP-0003." No extra confirmation needed because it's a straightforward update.
	•	Implicit Confirmation: In cases where an action is reversible or minor (most git-tracked changes are reversible), the agent just does them. Users can always fix via another command if needed. This keeps the interaction flowing and avoids interrupting the user for permission frequently.
	•	When to Ask for Clarification: The agent will pause and ask the user only when:
	•	It's truly unsure how to proceed and the consequence of guessing wrong might be significant/confusing. For example, user says "schedule experiment next Monday" but there are two experiments that could be meant – the agent might ask "Do you want to create a new experiment entry for next Monday, or schedule an existing one?"
	•	A required piece of info is missing that Smart-Fill cannot confidently supply. E.g., user says "do X with antibody" but doesn't name the antibody, and multiple antibodies are possible. The agent might say: "Which antibody will you use? (e.g., Anti-ABC or Anti-XYZ)"
	•	The user's request is unusual or potentially dangerous (not likely in lab context, but if user asked to delete a project, the agent should confirm since that's destructive).
	•	Confidence Thresholds: The agent's decision to auto-fill vs ask can be guided by confidence measures:
	•	If using OpenAI functions, the model itself might indicate uncertainty ("I think it's X"). We can parse that. If not, we rely on our Smart-Fill scores. For example, if the top embedding match for a missing parameter has a high similarity and clearly fits, we auto-use it. If two matches are close or low similarity, we then ask.
	•	For numeric or scientific suggestions (like a concentration), if the agent finds conflicting values from sources, better to ask the user or at least present the suggestion as a question: "I assumed 10 µM as the concentration based on literature – let me know if that's correct."
	•	Auto-Confirmation of Actions: After an action, the agent does usually describe what it did ("I've created the experiment entry with ID EXP-0007 and filled in the details."). This serves as an implicit confirmation to the user that it interpreted the request correctly. The user can always say "Actually, change X..." if they notice something off. This design aligns with a helpful assistant that takes initiative yet remains responsive to corrections.

By minimizing explicit questions to the user, the workflow becomes efficient – the student can rattle off a series of instructions and trust the agent to handle them. Only occasionally will the agent ping them for clarification. This reduces friction especially for routine tasks. It's akin to a real lab assistant who mostly knows what to do and only asks when absolutely necessary.

Of course, during initial deployment, we'll monitor if the agent maybe should ask more often in certain cases (to avoid assumptions). We can tune this by adjusting the agent prompt (for example, giving it guidelines on when to ask vs act).

Ensuring Reproducibility and Metadata Quality

Reproducibility is a top priority in lab work. Our system reinforces this in several ways:
	•	Comprehensive Metadata Capture: Every experiment's YAML is structured to capture who, what, when, how, and results. By enforcing templates and using Smart-Fill to populate them, we ensure fields aren't left blank. The agent will include as much detail as possible (including environmental conditions, instrument settings if mentioned, etc.). This addresses the concern that "details about experiments... are quickly forgotten unless they are written down" ￼. The system diligently writes everything down in the notebook (YAML), so nothing relies on memory.
	•	Protocol Linking and Versioning: Experiments reference protocols by name and version. If a protocol is updated, a new version file can be created (and the old one kept). The experiment continues to point to the version it used. This way, years later one can see the exact procedure used. We could even have the agent automatically record the git commit hash of the protocol file at time of use (to absolutely pin the version). This might be overkill, but it's an idea.
	•	Validation of Entries: The task-runner can include a validate function that runs after an experiment is marked completed to check that it has results and conclusion. Similarly for protocols: check that steps are not empty, etc. If something's missing, tag the YAML or open an issue. E.g., if a student forgot to fill "conclusion" in an experiment, the system might open an issue "Please add conclusion for EXP-0007" or leave a TODO in the file. This ensures completeness before experiments are considered done.
	•	PI Review Workflow: By involving the PI via PRs or even periodic review of the logs, we introduce a human check. The PI might notice if something is odd (like an experiment missing a control) and can comment. The agent can then help the student address that (maybe via a new experiment for the control).
	•	Minimal Friction for Students: All the above is achieved with minimal extra work for students because the agent does the heavy lifting. The interface is just a chat. Students don't need to remember to fill every field – if they forget, the agent either fills it or reminds them. The tedious parts of record-keeping (formatting, structuring, committing) are automated. This lowers the barrier to maintaining good records (one of the biggest challenges in research). The system essentially nudges users into good data practices by automating them.
	•	Reproducible Environment for Execution: If any code or analysis is part of experiments, the devcontainer ensures that running analysis scripts (if added to the repo) will yield the same results environment-wise. This goes beyond lab wet-work, but it's worth noting for completeness: e.g., if an experiment includes an analysis Jupyter notebook, the container has the packages to run it, making even computational parts reproducible.
	•	Documentation for Users and PI: We'll write a CONTRIBUTING.md or an onboarding doc for new students explaining this system's purpose: emphasize that it's an electronic lab notebook and task manager, why writing everything (via the agent) is important, and how it benefits them (searchable history, easier report writing, etc.). Also a note to PIs on how to get their reports from it (maybe instruct on using GitHub's interface to filter by user or date, or to use the logs to compile results).

In summary, by combining structured data capture, automated suggestion, and integrated review, the system will greatly enhance the completeness and reliability of lab records. Students can focus on science rather than paperwork, while the PI can be confident that no key detail has been omitted from the records. As one system demonstrated, using structured YAML protocols can even drive automated lab equipment reliably ￼; in our case, it drives record-keeping and planning with the same rigor.

Documentation and Next Steps

Finally, we prepare documentation to ensure the system is maintainable and users can learn it quickly:
	•	User Guide (Lab Agent Guide): As mentioned, a Markdown guide explaining how to use the chat interface, with examples:
	•	e.g. "To create a protocol, just tell the agent e.g. 'Create a protocol for solution preparation.' The agent will walk you through or auto-complete the details."
	•	List of things the agent can do (create/edit/list/search).
	•	How to phrase questions vs commands.
	•	Troubleshooting: what to do if the agent seems stuck or makes a mistake (e.g., manually edit the file, or revert a commit, etc., and let the agent know).
	•	How the GitHub integration works (so they're not surprised by auto commits or issues).
	•	Remind them to always push changes if they do anything manually.
	•	Developer Guide: Although the primary audience is lab users, we include some notes (maybe in the repository README or a separate DEV_NOTES.md) about the system's architecture for future maintainers. E.g., instructions to update the function schema if needed, or how to upgrade the embedding model, etc. Since this is a long-lived lab tool, eventually someone might need to tweak it (for example, if OpenAI API changes or if they switch to another LLM provider). Clear comments in code and a high-level doc will facilitate this.
	•	Resuming Work Documentation: In the README or Guide, explicitly mention that all progress is saved in the repository, and one can resume by reading TASKS.md and SESSION_LOG.md. Encourage committing these frequently (the agent will do so anyway). Essentially, "the system never forgets because it writes everything down", so users should trust the logs more than their memory when resuming.
	•	GitHub Usage Documentation: A short section on how to use issues/PRs produced. For instance, if an issue is opened for them by the agent, they should know to close it once done or comment. If a PR is opened, they should know how to view the changes and merge if appropriate. Not all students might be familiar with GitHub PRs, so a brief intro could help (or link to GitHub docs).
	•	No External Servers: Document that the system runs fully in Codespaces and pushes to GitHub. If the lab's Gitea is down or inaccessible, it doesn't affect using the agent (aside from mirror). And conversely, if Codespaces is down, one can still access the data on Gitea (but the agent wouldn't be running). This is more of an FYI for the PI about redundancy.

With all pieces in place – repository structure, devcontainer, agent & runner, smart-fill, integration, and docs – we will have a robust production-ready lab management system. It will have the following tangible outcomes:
	•	Folders and files scaffolded (protocols, experiments, etc., with templates).
	•	Working chat interface in Codespaces where the agent responds to lab commands.
	•	Example use case executed (perhaps in the README, illustrate creating a protocol and an experiment and show the resulting YAML and commit).
	•	Version control integration tested (ensuring commits and PRs happen correctly).
	•	Smart-Fill suggestions validated with a few test queries (maybe add a dummy protocol and see if it suggests it when querying).

Finally, after implementation, we'll likely do a dry run with a lab member's actual experiment to fine-tune any issues. But the plan as detailed covers the blueprint to implement this step-by-step.

To conclude, this plan provides a comprehensive path to deploy the smart lab assistant in the-jordan-lab/docs. By capitalizing on modern LLM capabilities within a structured, containerized framework, we greatly streamline lab workflows while maintaining rigorous documentation standards. This meets the lab's needs for completeness, reproducibility, and ease of use, transforming the GitHub repository into a living lab notebook maintained through natural conversation and intelligent automation.

Sources:
	•	Dev Containers for consistent Codespaces environments ￼
	•	OpenAI function calling for structured, multi-step tool use ￼
	•	YAML protocols as structured experiment scripts in automation ￼
	•	Importance of embeddings in retrieval-augmented responses ￼
	•	Labguru on centralizing experiments, protocols, and data for teamwork ￼
	•	Need for detailed record-keeping in lab notebooks ￼

---

# Implementation Progress Checklist (v1)

This checklist tracks the stepwise implementation of the lab management system as described above. Each burst of work will check off completed items and add new ones as needed. See commit history for details of each burst.

## Burst 1: Monorepo Scaffolding
- [x] Create main folders: Protocols/, Projects/, Experiments/, Data/, Templates/, Agent/
- [x] Add placeholder README.md files in each folder
- [x] Add protocol, experiment, and project template YAMLs in Templates/
- [x] Add stub documentation files (LAB_AGENT_GUIDE.md, TASKS.md, CHANGELOG.md)
- [ ] Add devcontainer scaffolding
- [ ] Implement agent/task-runner code scaffolding
- [ ] Add example protocol and experiment files
- [ ] Add usage instructions to folder READMEs

_Note: Burst 2 created LAB_AGENT_GUIDE.md, TASKS.md, and CHANGELOG.md as stubs for documentation and tracking. Next, devcontainer scaffolding and agent code will be started._

## Burst 3: Devcontainer and Agent Code Scaffolding
- [x] Add devcontainer scaffolding
- [x] Implement agent/task-runner code scaffolding
- [ ] Add example protocol and experiment files
- [ ] Add usage instructions to folder READMEs

_Note: Burst 3 created .devcontainer/devcontainer.json, .devcontainer/Dockerfile, and requirements.txt for Codespaces environment setup. Next, agent/task-runner code scaffolding will begin._

## Burst 4: Example Protocol and Experiment Files
- [x] Add example protocol and experiment files
- [x] Add usage instructions to folder READMEs

_Note: Burst 4 created Agent/agent_runner.py (scaffolded with class/function stubs) and Agent/__init__.py. Protocols/cell_staining_v1.yaml and Experiments/2025-05-10_cell_staining_Alice.yaml now serve as example files. Folder README.md files now include usage instructions and reference these examples. Next, further agent/task-runner implementation and Smart-Fill features will be developed._

## Burst 5: Smart-Fill Metadata Suggestion System
- [x] Implement Smart-Fill (embedding-based metadata suggestion)
- [ ] Integrate PubMed/external RAG for unknown terms
- [ ] Add per-user history for personalized suggestions

_Note: Burst 5 implemented Smart-Fill using ChromaDB and OpenAI embeddings to suggest metadata fields for protocols and experiments based on repository content. Next, GitHub integration (commit, push, issues, PRs) will be developed._

## Burst 6: GitHub Integration
- [x] Implement commit and push logic
- [x] Implement GitHub issue creation with short hash identifiers
- [ ] Implement draft pull request creation
- [ ] Add structured commit messages and PR descriptions
- [ ] Begin repository structure reorganization

_Note: Burst 6 implemented basic GitHub integration including commit/push functionality and issue creation with unique hash identifiers for better traceability. Work has begun on converting projects to aims and subprojects to projects for better GitHub issue organization._

## Burst 7: Ybx1 Knockdown mRNA Stability Experiment
- [x] Create project for Post-transcriptional regulation by Ybx1
- [x] Create subproject for mRNA stability measurements
- [x] Create protocol for Ybx1 knockdown mRNA stability assay (PROT-0035)
- [x] Generate experiment YAML for initial Ybx1 knockdown study (EXP-0225)
- [x] Create data directories for experiment results
- [x] Create morning push checklist (2025-05-06)
- [x] Create GitHub issues with unique hash identifiers for experiment tracking

_Note: Burst 7 implemented the first real-world experiment using the system, creating all necessary files, issues, and documentation with the new hash identifier system for better future-proofing._

## Burst 8: Repository Restructuring for GitHub Integration
- [ ] Convert "projects" to "aims" for higher-level organization
- [ ] Convert "subprojects" to "projects" for better GitHub issue integration
- [ ] Update all existing YAML files to reflect new structure
- [ ] Update documentation to reflect new naming conventions
- [ ] Create migration guide for users

_Note: This burst focuses on reorganizing the repository structure to better integrate with GitHub project management features, enabling more intuitive issue organization and tracking._

## Burst 9: Experiment Update, Validation, and Logging
- [x] Implement experiment update logic (handle_update_experiment)
- [x] Add validation for required fields on experiment completion
- [x] Open GitHub issue if validation fails
- [x] Append action summaries to CHANGELOG.md after each major action
- [x] Mark tasks as done in TASKS.md when experiments are completed

_Note: The agent/task-runner now automatically updates CHANGELOG.md and TASKS.md after relevant actions. Validation ensures completed experiments have all required fields, and missing data triggers a GitHub issue for follow-up._

---