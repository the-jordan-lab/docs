#!/usr/bin/env python3
"""
Protocol Format Checker
This script checks which YAML protocol files have been updated with the consistent professional format
and which ones still need to be fixed.
"""

import os
import yaml
import sys

def check_protocol_format(protocol_path):
    """Check if a protocol file has the expected professional format sections."""
    try:
        with open(protocol_path, 'r') as f:
            content = f.read()
            
        # If file is empty or very small, it's probably not formatted properly
        if len(content) < 100:
            return False
            
        # Check for key sections that indicate our professional format
        required_sections = [
            "# Protocol metadata",
            "# Materials required",
            "# Equipment required",
            "# Protocol steps",
            "# Critical parameters",
            "last_updated:",
            "category:",
        ]
        
        # Check for numbered steps format
        step_format = "step: "
        
        # Count how many required sections are present
        section_count = 0
        has_step_format = False
        
        for section in required_sections:
            if section in content:
                section_count += 1
        
        if step_format in content:
            has_step_format = True
            
        # If it has most of the sections and the step format, consider it updated
        return section_count >= 5 and has_step_format
        
    except Exception as e:
        print(f"Error checking {protocol_path}: {e}")
        return False

def main():
    """Main function to check all protocol files."""
    protocol_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all YAML files in the protocols directory
    protocol_files = []
    for root, _, files in os.walk(protocol_dir):
        for file in files:
            if file.endswith('.yaml'):
                protocol_files.append(os.path.join(root, file))
    
    # Check each protocol file
    updated = []
    need_update = []
    
    for protocol in protocol_files:
        is_updated = check_protocol_format(protocol)
        file_name = os.path.basename(protocol)
        
        if is_updated:
            updated.append(file_name)
        else:
            need_update.append(file_name)
    
    # Print results as a checklist
    print("\n===== PROTOCOL FORMATTING CHECKLIST =====")
    print(f"Total protocols: {len(protocol_files)}")
    print(f"Updated protocols: {len(updated)} ✓")
    print(f"Protocols needing update: {len(need_update)} ✗\n")
    
    print("UPDATED PROTOCOLS:")
    for i, protocol in enumerate(sorted(updated), 1):
        print(f"  ✓ {i}. {protocol}")
    
    print("\nPROTOCOLS NEEDING UPDATE:")
    for i, protocol in enumerate(sorted(need_update), 1):
        print(f"  ✗ {i}. {protocol}")

if __name__ == "__main__":
    main()