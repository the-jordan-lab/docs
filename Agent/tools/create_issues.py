#!/usr/bin/env python3
"""
Issue Creator for Lab Agent

This script:
1. Reads morning_push_2025-05-07.md
2. Extracts issues to create from the table
3. Checks if issues already exist
4. Creates issues and assigns them to james-m-jordan
5. Runs post_issue.py hook to update TASKS.md and ISSUES_LOG.md
"""

import os
import re
import json
import subprocess
from pathlib import Path

# Configuration
PUSH_PLAN = "morning_push_2025-05-07.md"
ASSIGNEE = "james-m-jordan"
REPO = "the-jordan-lab/docs"

def read_push_plan():
    """Read the push plan markdown file."""
    try:
        with open(PUSH_PLAN, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {PUSH_PLAN}")
        return None

def extract_issues(content):
    """Extract issues from the GitHub Issues table in the markdown."""
    # Find the issues section
    issues_section_match = re.search(r'## 3\. GitHub Issues to Create.*?\|\s*#\s*\|\s*Title\s*\|\s*Labels\s*\|.*?\|(.*?)(?=\n\n|$)', 
                                     content, re.DOTALL)
    
    if not issues_section_match:
        print("Error: Could not find GitHub Issues section in push plan")
        return []
    
    issues_content = issues_section_match.group(1)
    
    # Extract rows from the table
    rows = re.findall(r'\|\s*(\d+|\…)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', issues_content)
    
    issues = []
    for row in rows:
        if row[0] == '…':
            continue  # Skip placeholder row
            
        issues.append({
            'number': row[0],
            'title': row[1].strip(),
            'labels': [label.strip() for label in row[2].split(',')]
        })
    
    return issues

def check_issue_exists(title):
    """Check if an issue with the given title already exists."""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'list', '--repo', REPO, '--state', 'all', '--json', 'title'],
            capture_output=True, text=True, check=True
        )
        issues = json.loads(result.stdout)
        return any(issue['title'] == title for issue in issues)
    except subprocess.CalledProcessError as e:
        print(f"Error checking for existing issues: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return False

def create_issue(title, labels, section_ref):
    """Create a GitHub issue with the given title and labels."""
    try:
        # Create the issue
        cmd = [
            'gh', 'issue', 'create',
            '--repo', REPO,
            '--title', title,
            '--body', f"See {PUSH_PLAN}#{section_ref}",
            '--assignee', ASSIGNEE
        ]
        
        # Add labels
        for label in labels:
            cmd.extend(['--label', label])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Extract issue number and URL from the output
        # The output typically looks like: "https://github.com/user/repo/issues/123"
        url = result.stdout.strip()
        issue_number = url.split('/')[-1]
        
        print(f"Created issue #{issue_number}: {title}")
        return issue_number, url
    except subprocess.CalledProcessError as e:
        print(f"Error creating issue '{title}': {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return None, None

def run_post_issue_hook(issue_number, title, url):
    """Run the post_issue.py hook to update TASKS.md and ISSUES_LOG.md."""
    try:
        subprocess.run(
            ['python', 'Agent/hooks/post_issue.py', issue_number, title, url],
            check=True
        )
        print(f"Updated TASKS.md and ISSUES_LOG.md with issue #{issue_number}")
    except subprocess.CalledProcessError as e:
        print(f"Error running post-issue hook: {e}")

def main():
    """Main function to create issues from push plan."""
    print(f"Reading push plan from {PUSH_PLAN}...")
    content = read_push_plan()
    if not content:
        return
    
    issues = extract_issues(content)
    print(f"Found {len(issues)} issues to process")
    
    for issue in issues:
        title = issue['title']
        if check_issue_exists(title):
            print(f"Issue already exists: {title}")
            continue
        
        # Determine the section reference from title content
        section_ref = "1" if any(keyword in title.lower() for keyword in ['container', 'api', 'key', 'readme', 'hook', 'gitlens', 'ci']) else "2"
        
        issue_number, url = create_issue(title, issue['labels'], section_ref)
        if issue_number and url:
            run_post_issue_hook(issue_number, title, url)

if __name__ == "__main__":
    main() 