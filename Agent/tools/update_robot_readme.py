#!/usr/bin/env python3
"""
Robot README Updater

This script automatically updates ROBOT_README.md based on the repository structure.
It scans for top-level markdown files and directories, generating a structured table
of contents for AI assistants to understand the repository organization.

Usage:
  python update_robot_readme.py

This can be run manually or as a pre-commit hook to ensure the robot table of
contents stays in sync with the repository.
"""

import os
import re
from collections import defaultdict
from pathlib import Path

# Configuration
ROBOT_README = "ROBOT_README.md"
REPO_ROOT = "."  # Current directory
EXCLUDE_DIRS = [".git", ".github", ".vscode", "__pycache__", "node_modules"]
EXCLUDE_FILES = [ROBOT_README]  # Don't include self in the listing

# Descriptions for known files and directories
FILE_DESCRIPTIONS = {
    "README.md": "Main repository README with quick-start instructions and overview.",
    "ENVIRONMENT_SETUP.md": "Guide for setting up the development environment, including GitHub CLI and OpenAI API key configuration.",
    "LAB_AGENT_GUIDE.md": "Detailed guide on how to use the Lab Agent, including examples and troubleshooting.",
    "TASKS.md": "Tracks ongoing lab and development tasks, automatically updated by the Lab Agent.",
    "ISSUES_LOG.md": "Logs all GitHub issues created, automatically updated by the Lab Agent.",
    "morning_push_2025-05-06.md": "Checklist for May 6, 2025 morning push tasks.",
    "morning_push_2025-05-07.md": "Checklist for May 7, 2025 morning push tasks.",
}

DIR_DESCRIPTIONS = {
    "Protocols": "Contains standard operating procedures and experimental protocols.",
    "Projects": "Groups related experiments under broad project titles.",
    "Experiments": "Records of individual experiments or lab sessions.",
    "Data": "Storage for data outputs or references to data.",
    "Templates": "Contains starter templates for various YAML structures.",
    "Agent": "Contains the code for the AI agent integration, including the task-runner and hooks.",
}

def scan_repository():
    """Scan the repository for top-level markdown files and directories."""
    md_files = []
    directories = []
    
    for item in os.listdir(REPO_ROOT):
        path = Path(os.path.join(REPO_ROOT, item))
        
        # Skip excluded items
        if item in EXCLUDE_DIRS or item in EXCLUDE_FILES:
            continue
        
        # Skip hidden files and directories
        if item.startswith('.'):
            continue
            
        if path.is_file() and item.endswith('.md'):
            md_files.append(item)
        elif path.is_dir() and not item.startswith('.'):
            directories.append(item)
    
    return sorted(md_files), sorted(directories)

def extract_existing_descriptions():
    """Extract existing descriptions from ROBOT_README.md if it exists."""
    descriptions = defaultdict(str)
    
    if not os.path.exists(ROBOT_README):
        return descriptions
        
    with open(ROBOT_README, 'r') as f:
        content = f.read()
        
    # Extract existing descriptions using regex
    file_matches = re.findall(r'\*\*([^*]+\.md)\*\*:\s*([^\n]+)', content)
    dir_matches = re.findall(r'\*\*([^*]+)/\*\*:\s*([^\n]+)', content)
    
    for name, desc in file_matches + dir_matches:
        descriptions[name] = desc.strip()
    
    return descriptions

def get_description(item, is_dir, existing_descriptions):
    """Get description for an item, using existing description if available."""
    if item in (FILE_DESCRIPTIONS if not is_dir else DIR_DESCRIPTIONS):
        return FILE_DESCRIPTIONS[item] if not is_dir else DIR_DESCRIPTIONS[item]
    elif item in existing_descriptions:
        return existing_descriptions[item]
    else:
        return "No description available." if not is_dir else "Directory containing repository files."

def generate_robot_readme(md_files, directories, existing_descriptions):
    """Generate the content for ROBOT_README.md."""
    content = [
        "# Robot Table of Contents",
        "",
        "This file serves as a robot table of contents for the repository. It lists the structure of the repository and points to relevant .md files for context.",
        "",
        "## Repository Structure",
        ""
    ]
    
    # Add markdown files
    if md_files:
        for file in md_files:
            description = get_description(file, False, existing_descriptions)
            content.append(f"- **{file}**: {description}")
        content.append("")
    
    # Add directories section
    if directories:
        content.append("## Additional Directories")
        content.append("")
        for directory in directories:
            description = get_description(directory, True, existing_descriptions)
            content.append(f"- **{directory}/**: {description}")
        content.append("")
    
    # Add footer
    content.append("---")
    content.append("")
    content.append("_This file will be updated whenever the repository structure changes to ensure the robot has the latest context._")
    
    return "\n".join(content)

def update_robot_readme():
    """Update ROBOT_README.md if the content has changed."""
    existing_descriptions = extract_existing_descriptions()
    md_files, directories = scan_repository()
    new_content = generate_robot_readme(md_files, directories, existing_descriptions)
    
    # Check if the file exists and if content has changed
    if os.path.exists(ROBOT_README):
        with open(ROBOT_README, 'r') as f:
            current_content = f.read()
            
        if current_content.strip() == new_content.strip():
            print(f"No changes needed for {ROBOT_README}")
            return False
    
    # Write the updated content
    with open(ROBOT_README, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {ROBOT_README} with latest repository structure")
    return True

if __name__ == "__main__":
    update_robot_readme() 