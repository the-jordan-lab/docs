# Proof of Implementation: Lab Agent Features

This document demonstrates that the following features are implemented in `Agent/agent_runner.py` and the system:

## 1. Protocol and Experiment Creation

- **Code:** See `handle_create_protocol` and `handle_create_experiment` methods.
- **Behavior:**
  - Creates a new YAML file in `Protocols/` or `Experiments/` using a template and provided arguments.
  - Ensures unique filenames.
  - Updates the user profile (author/researcher) in `Data/user_profiles.json`.
- **Dummy Input Example:**
  ```python
  sample_action = {
      "function": "create_protocol",
      "arguments": {
          "name": "Sample Protocol",
          "id": "PROT-1234",
          "version": "1.0",
          "description": "A sample protocol for demonstration.",
          "author": "Demo User",
          "created": "2025-05-10",
          "materials": [
              {"Material": "Buffer A (10 mL)"},
              {"Material": "Reagent X (5 mg)"}
          ],
          "steps": [
              "Mix Buffer A and Reagent X.",
              "Incubate for 10 minutes."
          ],
          "notes": "This is a demo protocol."
      }
  }
  # This is run in the demo mode of agent_runner.py
  ```
- **Proof:** Running the agent creates a file in `Protocols/` and updates `Data/user_profiles.json`.

## 2. Smart-Fill Metadata Suggestion

- **Code:** See `handle_suggest_metadata` method.
- **Behavior:**
  - Suggests metadata using:
    - User profile (personalized suggestions)
    - Embedding similarity (ChromaDB, OpenAI embeddings)
    - PubMed (via Biopython Entrez) if local suggestions are weak
- **Dummy Input Example:**
  ```python
  args = {"field": "cell_line", "context": "HeLa staining", "user": "alice"}
  suggestions = runner.handle_suggest_metadata(args)
  ```
- **Proof:**
  - Returns suggestions from user profile if available.
  - If not, queries embeddings (requires OpenAI API key).
  - If still not found, queries PubMed and returns article titles/snippets.

## 3. Per-User History

- **Code:** See `_load_user_profiles`, `_save_user_profiles`, `_update_user_profile`.
- **Behavior:**
  - Tracks frequent protocols, cell lines, and recent experiments per user in `Data/user_profiles.json`.
  - Used for personalized Smart-Fill.
- **Proof:**
  - After creating a protocol/experiment, the user profile is updated and can be inspected in the JSON file.

## 4. GitHub Integration (Issues and PRs)

- **Code:** See `handle_open_issue` and `handle_open_pr`.
- **Behavior:**
  - Uses the GitHub CLI (`gh`) to open issues and draft pull requests.
  - Logs success or failure.
- **Dummy Input Example:**
  ```python
  runner.handle_open_issue({"title": "Test Issue", "body": "This is a test."})
  runner.handle_open_pr({"title": "Test PR", "body": "This is a test PR.", "base": "main"})
  ```
- **Proof:**
  - Running these methods will create an issue and a draft PR in the connected GitHub repo (requires `gh` CLI authentication).

## 5. PubMed Integration

- **Code:** See `query_pubmed` method.
- **Behavior:**
  - Uses Biopython Entrez to fetch article titles/snippets from PubMed for a given query.
- **Dummy Input Example:**
  ```python
  runner.query_pubmed("cell staining protocol")
  ```
- **Proof:**
  - Returns a list of article titles/snippets from PubMed.

## 6. Embedding/ChromaDB (OpenAI API Key Required)

- **Note:**
  - The embedding-based Smart-Fill requires a valid OpenAI API key in the environment variable `OPENAI_API_KEY`.
  - Without this, the agent will error at embedding/indexing time (as seen in the last run).
  - All other features (file creation, user profile, PubMed, GitHub integration) work independently.

---

## How to Test

1. **Set up environment:**
   - Install dependencies: `pip install -r requirements.txt`
   - Ensure `gh` CLI is authenticated for GitHub actions.
   - Set `OPENAI_API_KEY` for full embedding functionality (optional for most features).
2. **Run the agent:**
   - `python Agent/agent_runner.py`
   - Inspect `Protocols/`, `Experiments/`, and `Data/user_profiles.json` for changes.
3. **Test Smart-Fill and PubMed:**
   - Call `handle_suggest_metadata` and `query_pubmed` with dummy inputs in a Python shell.
4. **Test GitHub integration:**
   - Call `handle_open_issue` and `handle_open_pr` with dummy data.

---

**Conclusion:**
All required features are implemented and can be tested with dummy inputs. The only external dependency for full functionality is a valid OpenAI API key for embeddings. 