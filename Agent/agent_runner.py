import os
import yaml
import logging
from typing import Dict, Any, List
import shutil
from datetime import datetime
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import git
from Bio import Entrez
import json

class AgentTaskRunner:
    """
    Main class for running agent-driven lab management actions.
    Handles loading function call JSON, dispatching to handlers, and logging results.
    """
    def __init__(self, actions_path: str = "actions.json"):
        self.actions_path = actions_path
        self.logger = self._setup_logger()
        # Initialize ChromaDB client for Smart-Fill
        self.chroma_client = chromadb.Client(Settings(persist_directory="Data/chroma_index"))
        self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY", "sk-..."),
            model_name="text-embedding-ada-002"
        )
        # Build or load embedding index
        self.protocol_collection = self.chroma_client.get_or_create_collection("protocols", embedding_function=self.embedding_fn)
        self.experiment_collection = self.chroma_client.get_or_create_collection("experiments", embedding_function=self.embedding_fn)
        self.index_repo_content()
        # TODO: Initialize other state as needed (e.g., repo paths, templates)

    def _setup_logger(self):
        logger = logging.getLogger("AgentTaskRunner")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
        logger.addHandler(handler)
        return logger

    def load_actions(self) -> Dict[str, Any]:
        """
        Load the next action(s) for the agent to execute (e.g., from a JSON file or IPC).
        """
        # TODO: Implement loading logic
        return {}

    def run(self):
        """
        Main loop: load actions, dispatch to handler, log results.
        """
        self.logger.info("AgentTaskRunner started.")
        # DEMO: Simulate loading a sample action
        sample_action = {
            "function": "create_protocol",
            "arguments": {
                "name": "Sample Protocol",
                "id": "PROT-1234",
                "version": "1.0",
                "description": "A sample protocol for demonstration.",
                "author": "Demo User",
                "created": datetime.now().strftime("%Y-%m-%d"),
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
        # Dispatch demo action
        if sample_action["function"] == "create_protocol":
            self.handle_create_protocol(sample_action["arguments"])
        # TODO: Replace with real action loading and dispatch loop
        # TODO: Implement Smart-Fill (suggest_metadata) and GitHub integration in future bursts

    def _load_user_profiles(self):
        path = os.path.join("Data", "user_profiles.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def _save_user_profiles(self, profiles):
        path = os.path.join("Data", "user_profiles.json")
        with open(path, "w") as f:
            json.dump(profiles, f, indent=2)

    def _update_user_profile(self, username, key, value):
        profiles = self._load_user_profiles()
        user = profiles.get(username, {})
        if key in user and isinstance(user[key], list):
            if value not in user[key]:
                user[key].append(value)
        else:
            user[key] = [value]
        user["last_active"] = datetime.now().strftime("%Y-%m-%d")
        profiles[username] = user
        self._save_user_profiles(profiles)

    def handle_create_protocol(self, args: Dict[str, Any]):
        """
        Handle creation of a new protocol YAML in Protocols/.
        """
        template_path = os.path.join("Templates", "protocol_template.yaml")
        with open(template_path, "r") as f:
            template = yaml.safe_load(f)
        # Fill in template with args
        for key, value in args.items():
            template[key] = value
        # Generate filename
        name = args.get("name", "unnamed_protocol").lower().replace(" ", "_")
        version = args.get("version", "1.0")
        filename = f"{name}_v{version}.yaml"
        out_path = os.path.join("Protocols", filename)
        # Ensure unique filename if exists
        i = 1
        base_filename = filename
        while os.path.exists(out_path):
            filename = f"{name}_v{version}_{i}.yaml"
            out_path = os.path.join("Protocols", filename)
            i += 1
        with open(out_path, "w") as f:
            yaml.dump(template, f, sort_keys=False)
        self.logger.info(f"Created protocol: {out_path}")
        # Update user profile
        author = args.get("author", "unknown").replace(" ", "_").lower()
        self._update_user_profile(author, "frequent_protocols", args.get("name", "unnamed_protocol"))

    def handle_create_experiment(self, args: Dict[str, Any]):
        """
        Handle creation of a new experiment YAML in Experiments/.
        """
        template_path = os.path.join("Templates", "experiment_template.yaml")
        with open(template_path, "r") as f:
            template = yaml.safe_load(f)
        # Fill in template with args
        for key, value in args.items():
            template[key] = value
        # Generate filename
        date = args.get("date", datetime.now().strftime("%Y-%m-%d"))
        researcher = args.get("researcher", "unknown").replace(" ", "_")
        title = args.get("title", "untitled").lower().replace(" ", "_")
        filename = f"{date}_{title}_{researcher}.yaml"
        out_path = os.path.join("Experiments", filename)
        # Ensure unique filename if exists
        i = 1
        base_filename = filename
        while os.path.exists(out_path):
            filename = f"{date}_{title}_{researcher}_{i}.yaml"
            out_path = os.path.join("Experiments", filename)
            i += 1
        with open(out_path, "w") as f:
            yaml.dump(template, f, sort_keys=False)
        self.logger.info(f"Created experiment: {out_path}")
        # Update user profile
        researcher = args.get("researcher", "unknown").replace(" ", "_").lower()
        if "cell_line" in args:
            self._update_user_profile(researcher, "frequent_cell_lines", args["cell_line"])
        self._update_user_profile(researcher, "recent_experiments", filename)
        
        # Extract tasks from experiment and prepare for issue creation
        if args.get("tasks"):
            self.extract_tasks_and_preview(filename, template)

    def extract_tasks_and_preview(self, experiment_filename: str, experiment_data: Dict[str, Any]):
        """
        Extract tasks from an experiment and preview them before creating GitHub issues.
        
        Args:
            experiment_filename: The filename of the experiment YAML
            experiment_data: The experiment data dictionary
        """
        tasks = experiment_data.get("tasks", [])
        if not tasks:
            self.logger.info(f"No tasks found in experiment {experiment_filename}")
            return
            
        # Get other relevant experiment metadata
        experiment_id = experiment_data.get("experiment_id", experiment_filename)
        title = experiment_data.get("title", "Untitled Experiment")
        assignees = experiment_data.get("assignees", {})
        
        # Format tasks with assignees for preview
        preview_tasks = []
        for i, task in enumerate(tasks):
            task_description = task.get("description", "No description")
            task_assignee = task.get("assignee")
            assignee_username = assignees.get(task_assignee, "unassigned") if task_assignee else "unassigned"
            
            preview_tasks.append({
                "id": i + 1,
                "description": task_description,
                "assignee": assignee_username,
                "due_date": task.get("due_date", "No due date"),
                "experiment_id": experiment_id
            })
        
        # Log the preview
        self.logger.info(f"Preview of tasks for experiment {experiment_id}:")
        for task in preview_tasks:
            self.logger.info(f"Task #{task['id']}: {task['description']} (Assignee: {task['assignee']}, Due: {task['due_date']})")
            
        # Store the preview for confirmation
        self._store_task_preview(experiment_id, preview_tasks)
        
        # Create a GitHub issue for task preview confirmation
        preview_body = f"Experiment: {title} ({experiment_id})\n\n"
        preview_body += "The following tasks will be created as GitHub issues:\n\n"
        for task in preview_tasks:
            preview_body += f"- #{task['id']}: {task['description']} (Assignee: {task['assignee']}, Due: {task['due_date']})\n"
        preview_body += "\nTo confirm and create these issues, please comment 'confirm' on this issue."
        
        self.handle_open_issue({
            "title": f"Task Preview for {experiment_id}: {title}",
            "body": preview_body,
            "labels": ["task-preview"]
        })

    def _store_task_preview(self, experiment_id: str, tasks: List[Dict[str, Any]]):
        """
        Store task preview data for later confirmation.
        
        Args:
            experiment_id: The experiment identifier
            tasks: List of task dictionaries
        """
        preview_path = os.path.join("Data", "task_previews")
        os.makedirs(preview_path, exist_ok=True)
        
        preview_file = os.path.join(preview_path, f"{experiment_id}_task_preview.json")
        with open(preview_file, "w") as f:
            json.dump(tasks, f, indent=2)
            
        self.logger.info(f"Stored task preview at {preview_file}")

    def handle_confirm_tasks(self, args: Dict[str, Any]):
        """
        Create GitHub issues from previously previewed tasks.
        
        Args:
            args: Dictionary with experiment_id to confirm tasks for
        """
        experiment_id = args.get("experiment_id")
        if not experiment_id:
            self.logger.error("Missing experiment_id for confirm_tasks.")
            return
            
        preview_file = os.path.join("Data", "task_previews", f"{experiment_id}_task_preview.json")
        if not os.path.exists(preview_file):
            self.logger.error(f"No task preview found for experiment {experiment_id}")
            return
            
        with open(preview_file, "r") as f:
            tasks = json.load(f)
            
        for task in tasks:
            issue_title = f"[{experiment_id}] Task #{task['id']}: {task['description']}"
            issue_body = f"Experiment: {experiment_id}\n"
            issue_body += f"Description: {task['description']}\n"
            issue_body += f"Due Date: {task.get('due_date', 'Not specified')}\n\n"
            issue_body += f"This task is part of experiment {experiment_id}."
            
            # Create the issue
            self.handle_open_issue({
                "title": issue_title,
                "body": issue_body,
                "assignee": task.get("assignee"),
                "labels": ["experiment-task", experiment_id]
            })
            
            # Mark as created in TASKS.md
            self.add_task_to_tasks_md(task['description'], experiment_id)
            
        # Remove the preview file after creating issues
        os.remove(preview_file)
        self.logger.info(f"Created {len(tasks)} GitHub issues for experiment {experiment_id}")
        
        # Update the experiment YAML to indicate tasks were created
        self.update_experiment_tasks_status(experiment_id)

    def add_task_to_tasks_md(self, task_description: str, experiment_id: str):
        """
        Add a task entry to TASKS.md.
        
        Args:
            task_description: Description of the task
            experiment_id: ID of the experiment the task belongs to
        """
        if not os.path.exists("TASKS.md"):
            with open("TASKS.md", "w") as f:
                f.write("# Lab Tasks\n\n")
                
        with open("TASKS.md", "r") as f:
            lines = f.readlines()
            
        # Find the Lab Tasks section or create it
        lab_tasks_index = -1
        for i, line in enumerate(lines):
            if line.strip() == "# Lab Tasks" or line.strip() == "## Lab Tasks":
                lab_tasks_index = i
                break
                
        if lab_tasks_index == -1:
            lines.append("\n## Lab Tasks\n\n")
            lab_tasks_index = len(lines) - 3
            
        # Add the new task after the Lab Tasks heading
        task_line = f"- [ ] {task_description} ({experiment_id})\n"
        lines.insert(lab_tasks_index + 2, task_line)
        
        with open("TASKS.md", "w") as f:
            f.writelines(lines)
            
        self.logger.info(f"Added task to TASKS.md: {task_description}")

    def update_experiment_tasks_status(self, experiment_id: str):
        """
        Update the experiment YAML file to indicate tasks were created.
        
        Args:
            experiment_id: ID of the experiment
        """
        # Find experiment file
        exp_dir = "Experiments"
        exp_file = None
        for fname in os.listdir(exp_dir):
            if experiment_id in fname:
                exp_file = os.path.join(exp_dir, fname)
                break
                
        if not exp_file or not os.path.exists(exp_file):
            self.logger.error(f"Experiment file not found for id: {experiment_id}")
            return
            
        # Update the experiment YAML
        with open(exp_file, "r") as f:
            exp = yaml.safe_load(f)
            
        if "tasks" in exp:
            for task in exp["tasks"]:
                task["github_issue_created"] = True
                
        with open(exp_file, "w") as f:
            yaml.dump(exp, f, sort_keys=False)
            
        self.logger.info(f"Updated experiment {experiment_id} to mark tasks as created")

    def handle_update_experiment(self, args: Dict[str, Any]):
        """
        Handle updating an existing experiment YAML (e.g., add results, change status).
        Args should include: experiment_id (filename or unique id), updates (dict of fields to update)
        """
        experiment_id = args.get("experiment_id")
        updates = args.get("updates", {})
        if not experiment_id or not updates:
            self.logger.error("Missing experiment_id or updates for update_experiment.")
            return
        # Find experiment file
        exp_dir = "Experiments"
        exp_file = None
        for fname in os.listdir(exp_dir):
            if experiment_id in fname:
                exp_file = os.path.join(exp_dir, fname)
                break
        if not exp_file or not os.path.exists(exp_file):
            self.logger.error(f"Experiment file not found for id: {experiment_id}")
            return
        # Load, update, and save YAML
        with open(exp_file, "r") as f:
            exp = yaml.safe_load(f)
        exp.update(updates)
        with open(exp_file, "w") as f:
            yaml.dump(exp, f, sort_keys=False)
        self.logger.info(f"Updated experiment: {exp_file}")
        # Validate if status is completed
        if exp.get("status", "").lower() == "completed":
            missing = []
            for field in ["results", "conclusion"]:
                if not exp.get(field):
                    missing.append(field)
            if missing:
                issue_title = f"Experiment {experiment_id} missing required fields"
                issue_body = f"The following required fields are missing: {', '.join(missing)}. Please update the experiment record."
                self.handle_open_issue({"title": issue_title, "body": issue_body})
        # Log to changelog
        self.append_changelog(f"Updated experiment {experiment_id}: {list(updates.keys())}")
        # Optionally update tasks
        self.mark_task_done_for_experiment(experiment_id)
        
        # If tasks have been added or modified, handle task preview
        if "tasks" in updates and updates["tasks"]:
            with open(exp_file, "r") as f:
                updated_exp = yaml.safe_load(f)
            self.extract_tasks_and_preview(experiment_id, updated_exp)

    def append_changelog(self, entry: str):
        with open("CHANGELOG.md", "a") as f:
            f.write(f"- {datetime.now().strftime('%Y-%m-%d %H:%M')}: {entry}\n")

    def mark_task_done_for_experiment(self, experiment_id: str):
        # Mark a lab task as done in TASKS.md if it references this experiment
        if not os.path.exists("TASKS.md"): return
        with open("TASKS.md", "r") as f:
            lines = f.readlines()
        updated = False
        for i, line in enumerate(lines):
            if experiment_id in line and line.strip().startswith("- [ ]"):
                lines[i] = line.replace("- [ ]", "- [x]", 1)
                updated = True
        if updated:
            with open("TASKS.md", "w") as f:
                f.writelines(lines)

    def handle_suggest_metadata(self, args: Dict[str, Any]):
        """
        Handle metadata suggestion using embeddings or external sources.
        Args should include: field (str), context (str)
        """
        field = args.get("field")
        context = args.get("context", "")
        username = args.get("user", "unknown").replace(" ", "_").lower()
        # Personalized suggestions from user profile
        profiles = self._load_user_profiles()
        user = profiles.get(username, {})
        personalized = []
        if field == "cell_line" and "frequent_cell_lines" in user:
            for cl in user["frequent_cell_lines"]:
                personalized.append({"source": "user_profile", "text": cl})
        if field == "protocol" and "frequent_protocols" in user:
            for p in user["frequent_protocols"]:
                personalized.append({"source": "user_profile", "text": p})
        # Query both protocol and experiment collections for similar content
        results = self.protocol_collection.query(query_texts=[context], n_results=3)
        exp_results = self.experiment_collection.query(query_texts=[context], n_results=3)
        suggestions = personalized
        for r in results["documents"][0]:
            suggestions.append({"source": "protocol", "text": r})
        for r in exp_results["documents"][0]:
            suggestions.append({"source": "experiment", "text": r})
        # If suggestions are weak or empty, query PubMed
        if not suggestions or all(not s["text"].strip() for s in suggestions):
            pubmed_suggestions = self.query_pubmed(context)
            for s in pubmed_suggestions:
                suggestions.append({"source": "pubmed", "text": s})
        self.logger.info(f"Smart-Fill suggestions for '{field}' (user: {username}): {suggestions}")
        return suggestions

    def query_pubmed(self, query: str, max_results: int = 3):
        """
        Query PubMed for relevant articles using Biopython Entrez.
        Returns a list of article titles and snippets.
        """
        Entrez.email = os.getenv("ENTREZ_EMAIL", "labagent@example.com")
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            ids = record["IdList"]
            if not ids:
                return []
            handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="medline", retmode="text")
            abstracts = handle.read().split("\n\n")
            results = []
            for abs_text in abstracts:
                lines = abs_text.split("\n")
                title = next((l[6:] for l in lines if l.startswith("TI - ")), "")
                snippet = next((l[6:] for l in lines if l.startswith("AB - ")), "")
                if title:
                    results.append(f"{title} {'- ' + snippet if snippet else ''}")
            return results[:max_results]
        except Exception as e:
            self.logger.error(f"PubMed query failed: {e}")
            return []

    def handle_commit_and_push(self, args: Dict[str, Any]):
        """
        Handle committing and pushing changes to GitHub.
        Args should include: message (str)
        """
        repo = git.Repo(os.getcwd())
        message = args.get("message", "Lab agent commit")
        # Stage all changes
        repo.git.add(A=True)
        # Commit
        repo.index.commit(message)
        self.logger.info(f"Committed changes: {message}")
        # Push
        origin = repo.remote(name='origin')
        origin.push()
        self.logger.info("Pushed changes to origin.")

    def handle_open_issue(self, args: Dict[str, Any]):
        """
        Handle opening a GitHub issue via CLI (gh).
        Args should include: title (str), body (str), assignee (str, optional), labels (list, optional)
        """
        title = args.get("title", "Lab Agent Issue")
        body = args.get("body", "Created by lab agent.")
        assignee = args.get("assignee")
        labels = args.get("labels", [])
        
        # Build the command
        cmd = f'gh issue create --title "{title}" --body "{body}"'
        
        # Add assignee if provided
        if assignee and assignee != "unassigned":
            cmd += f' --assignee "{assignee}"'
            
        # Add labels if provided
        if labels:
            label_str = ",".join(labels)
            cmd += f' --label "{label_str}"'
        
        result = os.system(cmd)
        if result == 0:
            self.logger.info(f"Opened GitHub issue: {title}")
            # Add to ISSUES_LOG.md
            self._add_to_issues_log(title, assignee)
        else:
            self.logger.error(f"Failed to open GitHub issue: {title}")

    def _add_to_issues_log(self, title: str, assignee: str = None):
        """
        Add an entry to ISSUES_LOG.md
        
        Args:
            title: Issue title
            assignee: GitHub username of assignee (optional)
        """
        if not os.path.exists("ISSUES_LOG.md"):
            with open("ISSUES_LOG.md", "w") as f:
                f.write("# GitHub Issues Log\n\n")
                
        with open("ISSUES_LOG.md", "a") as f:
            entry = f"- {datetime.now().strftime('%Y-%m-%d %H:%M')}: {title}"
            if assignee and assignee != "unassigned":
                entry += f" (Assigned to: {assignee})"
            f.write(entry + "\n")

    def handle_open_pr(self, args: Dict[str, Any]):
        """
        Handle opening a draft pull request via CLI (gh).
        Args should include: title (str), body (str), base (str, optional)
        """
        title = args.get("title", "Lab Agent Draft PR")
        body = args.get("body", "Draft PR created by lab agent.")
        base = args.get("base", "main")
        cmd = f'gh pr create --title "{title}" --body "{body}" --base {base} --draft'
        result = os.system(cmd)
        if result == 0:
            self.logger.info(f"Opened draft PR: {title}")
        else:
            self.logger.error(f"Failed to open draft PR: {title}")

    def _make_commit_message(self, action_type: str, details: Dict[str, Any]) -> str:
        """
        Helper to generate a structured commit message.
        """
        if action_type == "create_protocol":
            return f"Protocol: Created {details.get('name', 'unnamed protocol')} v{details.get('version', '')}"
        elif action_type == "create_experiment":
            return f"Experiment: Created {details.get('title', 'untitled experiment')} ({details.get('experiment_id', '')})"
        elif action_type == "update_experiment":
            return f"Experiment: Updated {details.get('experiment_id', '')}"
        elif action_type == "open_issue":
            return f"Issue: {details.get('title', 'No title')}"
        elif action_type == "open_pr":
            return f"PR: {details.get('title', 'No title')}"
        return "Lab agent commit"

    def index_repo_content(self):
        """
        Index all Protocols/ and Experiments/ YAMLs for Smart-Fill suggestions.
        """
        # Index protocols
        protocol_dir = "Protocols"
        for fname in os.listdir(protocol_dir):
            if fname.endswith(".yaml"):
                with open(os.path.join(protocol_dir, fname), "r") as f:
                    doc = yaml.safe_load(f)
                doc_id = f"protocol_{fname}"
                content = f"{doc.get('name', '')} {doc.get('description', '')} {doc.get('materials', '')} {doc.get('steps', '')}"
                self.protocol_collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[{"file": fname}]
                )
        # Index experiments
        exp_dir = "Experiments"
        for fname in os.listdir(exp_dir):
            if fname.endswith(".yaml"):
                with open(os.path.join(exp_dir, fname), "r") as f:
                    doc = yaml.safe_load(f)
                doc_id = f"experiment_{fname}"
                content = f"{doc.get('title', '')} {doc.get('protocol', '')} {doc.get('materials', '')} {doc.get('parameters', '')} {doc.get('results', '')}"
                self.experiment_collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[{"file": fname}]
                )
        self.logger.info("Indexed protocols and experiments for Smart-Fill.")

if __name__ == "__main__":
    runner = AgentTaskRunner()
    runner.run() 