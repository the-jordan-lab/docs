#!/usr/bin/env python3
"""
Protocol Dashboard Generator

This script creates a simple terminal-based dashboard of all your lab protocols,
showing both standalone YAML files and Markdown files with YAML frontmatter.
"""

import os
import re
import yaml
import glob
from datetime import datetime

# Configuration
PROTOCOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Protocols")

def extract_frontmatter(markdown_content):
    """Extract YAML frontmatter from markdown content"""
    pattern = r"^---\n(.*?)\n---"
    match = re.search(pattern, markdown_content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None

def load_protocol_files():
    """Load protocol data from both YAML and Markdown files"""
    protocols = []
    
    # Process YAML files
    yaml_files = glob.glob(os.path.join(PROTOCOLS_DIR, "*.yaml"))
    for file_path in yaml_files:
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    data['file_path'] = os.path.basename(file_path)
                    data['file_type'] = 'yaml'
                    protocols.append(data)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Process Markdown files with frontmatter
    md_files = glob.glob(os.path.join(PROTOCOLS_DIR, "*.md"))
    for file_path in md_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                frontmatter = extract_frontmatter(content)
                if frontmatter:
                    frontmatter['file_path'] = os.path.basename(file_path)
                    frontmatter['file_type'] = 'markdown'
                    protocols.append(frontmatter)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return protocols

def print_terminal_dashboard(protocols):
    """Display a simple terminal-based dashboard"""
    print("\n" + "="*80)
    print(f"LAB PROTOCOL DASHBOARD - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Count by type
    yaml_count = len([p for p in protocols if p.get('file_type') == 'yaml'])
    md_count = len([p for p in protocols if p.get('file_type') == 'markdown'])
    
    print(f"\nTotal Protocols: {len(protocols)}")
    print(f"YAML Files: {yaml_count}")
    print(f"Markdown with Frontmatter: {md_count}")
    
    # Sort protocols by ID
    protocols.sort(key=lambda x: str(x.get('id', 'ZZZZ')))
    
    # Print YAML protocols
    if yaml_count > 0:
        print("\n" + "-"*80)
        print("STANDALONE YAML PROTOCOLS")
        print("-"*80)
        for protocol in [p for p in protocols if p.get('file_type') == 'yaml']:
            print(f"\nID: {protocol.get('id', 'No ID')}")
            print(f"Name: {protocol.get('name', 'Unnamed')}")
            print(f"Version: {protocol.get('version', 'Unknown')}")
            print(f"File: {protocol.get('file_path')}")
            print(f"Description: {protocol.get('description', 'No description')}")
            if 'materials' in protocol and protocol['materials']:
                print(f"Materials: {len(protocol['materials'])} items")
            if 'steps' in protocol and protocol['steps']:
                print(f"Steps: {len(protocol['steps'])} steps")
    
    # Print Markdown protocols
    if md_count > 0:
        print("\n" + "-"*80)
        print("MARKDOWN PROTOCOLS WITH FRONTMATTER")
        print("-"*80)
        for protocol in [p for p in protocols if p.get('file_type') == 'markdown']:
            print(f"\nID: {protocol.get('id', 'No ID')}")
            print(f"Name: {protocol.get('name', 'Unnamed')}")
            print(f"Version: {protocol.get('version', 'Unknown')}")
            print(f"File: {protocol.get('file_path')}")
            print(f"Description: {protocol.get('description', 'No description')}")
            if 'materials' in protocol and protocol['materials']:
                print(f"Materials: {len(protocol['materials'])} items")
            if 'steps' in protocol and protocol['steps']:
                print(f"Steps: {len(protocol['steps'])} steps")
    
    print("\n" + "="*80)
    print("USAGE RECOMMENDATIONS:")
    print("="*80)
    print("- YAML Files: Great for machine processing and programmatic access")
    print("- Markdown+Frontmatter: Better for detailed protocols with rich formatting")
    print("- Both formats work well with the Lab Agent and can be used together")
    print("="*80 + "\n")

if __name__ == "__main__":
    protocols = load_protocol_files()
    print_terminal_dashboard(protocols)