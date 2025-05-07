import os
import yaml
import shutil
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("lab")

def create_experiment_with_plate(
    experiment_id: str,
    aim: str,
    project: str,
    researcher: str,
    plate: Dict[str, Any],
    sample_preparation: Optional[Dict[str, Any]] = None,
    downstream_application: Optional[Dict[str, Any]] = None,
    status: str = "in_progress"
) -> str:
    """
    Create a new experiment with plate layout information.
    
    Args:
        experiment_id: Unique identifier for the experiment (EXP-YYYYMMDD format)
        aim: Brief description of the experiment's goal
        project: Project this experiment belongs to
        researcher: GitHub username or name of the researcher
        plate: Dictionary with plate ID and layout information
        sample_preparation: Optional dictionary with sample preparation details
        downstream_application: Optional dictionary with downstream application details
        status: Current status of the experiment (default: in_progress)
        
    Returns:
        Path to the created experiment file
    """
    logger.info(f"Creating experiment {experiment_id} for {researcher}")
    
    # Create basic experiment structure
    experiment = {
        "experiment_id": experiment_id,
        "aim": aim,
        "project": project,
        "researcher": researcher,
        "status": status,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "plate": plate,
        "tasks": []
    }
    
    # Add optional sections if provided
    if sample_preparation:
        experiment["sample_preparation"] = sample_preparation
    
    if downstream_application:
        experiment["downstream_application"] = downstream_application
        
    # Create data directory for this experiment if it doesn't exist
    data_dir = os.path.join("Data", experiment_id)
    os.makedirs(data_dir, exist_ok=True)
    
    # Save the experiment file
    experiment_file = f"Experiments/{experiment_id}.yaml"
    with open(experiment_file, "w") as f:
        yaml.dump(experiment, f, sort_keys=False)
    
    logger.info(f"Experiment file created: {experiment_file}")
    return experiment_file

def add_experiment_task(experiment_id: str, task_title: str) -> Dict[str, Any]:
    """
    Add a task to an experiment and create a corresponding GitHub Issue.
    
    Args:
        experiment_id: ID of the experiment to add task to
        task_title: Title of the task/Issue
        
    Returns:
        Dictionary with the created issue details
    """
    logger.info(f"Adding task '{task_title}' to experiment {experiment_id}")
    
    # Create GitHub Issue
    cmd = f'gh issue create --title "{task_title}" --body "Experiment: {experiment_id}\n\nTask for experiment {experiment_id}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Failed to create GitHub Issue: {result.stderr}")
        raise Exception(f"Failed to create GitHub Issue: {result.stderr}")
    
    # Extract issue number from URL
    issue_url = result.stdout.strip()
    issue_number = issue_url.split("/")[-1]
    
    # Add issue to project board
    add_to_project_cmd = f'gh issue edit {issue_number} --add-project "Lab Tasks Board"'
    subprocess.run(add_to_project_cmd, shell=True)
    
    # Update experiment YAML
    experiment_file = f"Experiments/{experiment_id}.yaml"
    with open(experiment_file, "r") as f:
        experiment = yaml.safe_load(f)
    
    # Add task to tasks array
    task = {
        "id": issue_number,
        "title": task_title,
        "status": "open"
    }
    
    if "tasks" not in experiment:
        experiment["tasks"] = []
    
    experiment["tasks"].append(task)
    
    with open(experiment_file, "w") as f:
        yaml.dump(experiment, f, sort_keys=False)
    
    logger.info(f"Added task {issue_number} to experiment {experiment_id}")
    return task

def record_data(exp_id: str, file_path: str, data_type: str) -> Dict[str, Any]:
    """
    Record data file for an experiment. This function:
    1. Computes checksum of the file
    2. Copies file to Data/{exp_id}/ if not already there
    3. Adds entry to the experiment's YAML data section
    
    Args:
        exp_id: Experiment ID 
        file_path: Path to the data file
        data_type: Type of data (e.g., qPCR, flow_cytometry, imaging)
        
    Returns:
        The data entry added to the experiment
    """
    logger.info(f"Recording {data_type} data for experiment {exp_id}")
    
    # Verify the experiment exists
    experiment_file = f"Experiments/{exp_id}.yaml"
    if not os.path.exists(experiment_file):
        raise FileNotFoundError(f"Experiment {exp_id} not found")
    
    # Make sure the data directory exists
    data_dir = os.path.join("Data", exp_id)
    os.makedirs(data_dir, exist_ok=True)
    
    # Compute file checksum
    with open(file_path, "rb") as f:
        file_data = f.read()
        sha256 = hashlib.sha256(file_data).hexdigest()
    
    # Get just the filename
    filename = os.path.basename(file_path)
    
    # Construct target path in the data directory
    target_path = os.path.join(data_dir, filename)
    
    # Copy file if it's not already in the data directory
    if os.path.abspath(file_path) != os.path.abspath(target_path):
        shutil.copy2(file_path, target_path)
        logger.info(f"Copied data file to {target_path}")
    
    # Update the experiment YAML
    with open(experiment_file, "r") as f:
        experiment = yaml.safe_load(f)
    
    # Create the data entry
    data_entry = {
        "path": f"Data/{exp_id}/{filename}",
        "type": data_type,
        "sha256": sha256,
        "added": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Add to data array
    if "data" not in experiment:
        experiment["data"] = []
    
    experiment["data"].append(data_entry)
    
    # Save the updated experiment file
    with open(experiment_file, "w") as f:
        yaml.dump(experiment, f, sort_keys=False)
    
    # Commit the changes
    commit_cmd = f'git add "{target_path}" "{experiment_file}" && git commit -m "Data: add {data_type} result for {exp_id}"'
    subprocess.run(commit_cmd, shell=True)
    
    logger.info(f"Recorded data file {filename} for experiment {exp_id}")
    return data_entry

def close_task(issue_number: int) -> None:
    """
    Close a GitHub Issue and update the corresponding experiment task status.
    
    Args:
        issue_number: The GitHub Issue number to close
    """
    logger.info(f"Closing task (issue #{issue_number})")
    
    # Close the GitHub issue
    close_cmd = f'gh issue close {issue_number}'
    result = subprocess.run(close_cmd, shell=True)
    
    if result.returncode != 0:
        logger.error(f"Failed to close GitHub Issue #{issue_number}")
        return
    
    # Find which experiment this issue belongs to
    experiments_dir = "Experiments"
    for filename in os.listdir(experiments_dir):
        if not filename.endswith(".yaml"):
            continue
            
        file_path = os.path.join(experiments_dir, filename)
        with open(file_path, "r") as f:
            experiment = yaml.safe_load(f)
            
        if "tasks" not in experiment:
            continue
            
        # Check if this issue is in the tasks
        for i, task in enumerate(experiment["tasks"]):
            if str(task.get("id")) == str(issue_number):
                # Update task status
                experiment["tasks"][i]["status"] = "closed"
                
                # Save the updated experiment
                with open(file_path, "w") as f:
                    yaml.dump(experiment, f, sort_keys=False)
                    
                logger.info(f"Updated task status in experiment {experiment['experiment_id']}")
                
                # Commit the change
                commit_cmd = f'git add "{file_path}" && git commit -m "Task: close issue #{issue_number} for {experiment["experiment_id"]}"'
                subprocess.run(commit_cmd, shell=True)
                return

    logger.warning(f"Could not find task {issue_number} in any experiment")

def finish_experiment(exp_id: str) -> bool:
    """
    Finish an experiment by:
    1. Verifying all tasks are closed
    2. Checking data exists
    3. Setting status to completed
    4. Updating SESSION_LOG.md
    
    Args:
        exp_id: Experiment ID to finish
        
    Returns:
        True if experiment was successfully completed, False otherwise
    """
    logger.info(f"Attempting to finish experiment {exp_id}")
    
    # Verify the experiment exists
    experiment_file = f"Experiments/{exp_id}.yaml"
    if not os.path.exists(experiment_file):
        logger.error(f"Experiment {exp_id} not found")
        return False
    
    # Load the experiment
    with open(experiment_file, "r") as f:
        experiment = yaml.safe_load(f)
    
    # Check if all tasks are closed
    if "tasks" in experiment:
        open_tasks = [task for task in experiment["tasks"] if task.get("status") != "closed"]
        if open_tasks:
            task_ids = [task.get("id") for task in open_tasks]
            logger.warning(f"Cannot finish experiment: open tasks remain: {task_ids}")
            return False
    
    # Check if data exists
    if "data" not in experiment or not experiment["data"]:
        logger.warning(f"Cannot finish experiment: no data recorded")
        return False
    
    # Update status to completed
    experiment["status"] = "completed"
    experiment["completed"] = datetime.now().strftime("%Y-%m-%d")
    
    # Save the updated experiment
    with open(experiment_file, "w") as f:
        yaml.dump(experiment, f, sort_keys=False)
    
    # Update SESSION_LOG.md
    session_log_path = "SESSION_LOG.md"
    if not os.path.exists(session_log_path):
        with open(session_log_path, "w") as f:
            f.write("# Lab Session Log\n\n")
    
    with open(session_log_path, "a") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d')} - {experiment['researcher']}\n")
        f.write(f"- Completed experiment {exp_id}: {experiment['aim']}\n")
        f.write(f"- Data files: {len(experiment['data'])}\n")
    
    # Commit the changes
    commit_cmd = f'git add "{experiment_file}" "{session_log_path}" && git commit -m "Experiment: completed {exp_id}"'
    subprocess.run(commit_cmd, shell=True)
    
    logger.info(f"Successfully completed experiment {exp_id}")
    return True

def list_experiments(status_filter=None):
    """
    List all experiments, optionally filtered by status.
    
    Args:
        status_filter: Optional filter for experiment status ('in_progress', 'completed', etc.)
        
    Returns:
        List of experiment dictionaries
    """
    experiments = []
    experiments_dir = "Experiments"
    
    if not os.path.exists(experiments_dir):
        return []
        
    for filename in os.listdir(experiments_dir):
        if not filename.endswith(".yaml"):
            continue
            
        file_path = os.path.join(experiments_dir, filename)
        with open(file_path, "r") as f:
            experiment = yaml.safe_load(f)
            
        if status_filter is None or experiment.get("status") == status_filter:
            experiments.append(experiment)
            
    return experiments

def record_cli():
    """Entry point for lab-record CLI command"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Record data for an experiment")
    parser.add_argument("--exp", required=True, help="Experiment ID")
    parser.add_argument("--file", required=True, help="Path to data file")
    parser.add_argument("--type", required=True, help="Type of data")
    
    args = parser.parse_args()
    try:
        result = record_data(args.exp, args.file, args.type)
        print(f"Data recorded successfully: {result['path']}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def main():
    """Entry point for lab CLI command"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Lab Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Record data command
    record_parser = subparsers.add_parser("record", help="Record data for an experiment")
    record_parser.add_argument("--exp", required=True, help="Experiment ID")
    record_parser.add_argument("--file", required=True, help="Path to data file")
    record_parser.add_argument("--type", required=True, help="Type of data")
    
    # Close task command
    close_parser = subparsers.add_parser("close-task", help="Close a task/issue")
    close_parser.add_argument("--issue", type=int, required=True, help="Issue number to close")
    
    # Finish experiment command
    finish_parser = subparsers.add_parser("finish", help="Mark an experiment as completed")
    finish_parser.add_argument("--exp", required=True, help="Experiment ID to finish")
    
    # List experiments command
    list_parser = subparsers.add_parser("list", help="List experiments")
    list_parser.add_argument("--status", help="Filter by status")
    
    # Initialize command (mostly for documentation, actual impl. is in init_extensions.py)
    init_parser = subparsers.add_parser("init-extensions", help="Initialize extensions and environment")
    
    # Parse arguments and execute
    args = parser.parse_args()
    
    if args.command == "record":
        record_data(args.exp, args.file, args.type)
    elif args.command == "close-task":
        close_task(args.issue)
    elif args.command == "finish":
        finish_experiment(args.exp)
    elif args.command == "list":
        experiments = list_experiments(args.status)
        for exp in experiments:
            print(f"{exp.get('experiment_id', 'No ID')} - {exp.get('aim', 'No description')} - {exp.get('status', 'unknown')}")
    elif args.command == "init-extensions":
        print("Please run 'lab-init-extensions' instead")
    else:
        parser.print_help()

# Command-line interface
if __name__ == "__main__":
    main() 