#!/usr/bin/env python3
"""
Label Creator for GitHub Issues

This script creates standard labels needed for the Lab Agent issue tracking system.
It ensures all labels exist before attempting to create issues.
"""

import subprocess
import sys

# Repository
REPO = "the-jordan-lab/docs"

# List of labels to create with their colors and descriptions
LABELS = [
    {
        "name": "infra",
        "color": "0366d6",
        "description": "Infrastructure and DevOps improvements"
    },
    {
        "name": "high-priority",
        "color": "d93f0b",
        "description": "High priority tasks that need immediate attention"
    },
    {
        "name": "security",
        "color": "d93f0b",
        "description": "Security-related issues and improvements"
    },
    {
        "name": "docs",
        "color": "0075ca",
        "description": "Documentation updates and additions"
    },
    {
        "name": "tooling",
        "color": "1d76db",
        "description": "Tools and automation improvements"
    },
    {
        "name": "ci",
        "color": "fbca04",
        "description": "Continuous Integration and GitHub Actions"
    },
    {
        "name": "lab",
        "color": "0e8a16",
        "description": "Wet-lab related issues and experiments"
    }
]

def create_label(label):
    """Create a label in the GitHub repository."""
    try:
        cmd = [
            'gh', 'label', 'create',
            '--repo', REPO,
            label['name'],
            '--color', label['color'],
            '--description', label['description'],
            '--force'  # Update if already exists
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Created/updated label: {label['name']}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating label '{label['name']}': {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return False

def main():
    """Create all required labels."""
    print(f"Creating labels in repository: {REPO}")
    
    success_count = 0
    for label in LABELS:
        if create_label(label):
            success_count += 1
    
    print(f"Successfully created/updated {success_count} of {len(LABELS)} labels")
    return 0 if success_count == len(LABELS) else 1

if __name__ == "__main__":
    sys.exit(main()) 