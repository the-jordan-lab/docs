#!/usr/bin/env python3

import json
import os
import glob
import pandas as pd
import requests
import argparse

def extract_doc_id(gsheet_file_path):
    """Extract the document ID from a .gsheet file"""
    with open(gsheet_file_path, 'r') as file:
        content = json.load(file)
        return content.get("doc_id", "")

def download_as_excel(doc_id, output_path):
    """Download Google Sheet as Excel file using export URL"""
    # Google Sheets direct export URL
    export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=xlsx"
    
    print(f"Downloading from {export_url}")
    response = requests.get(export_url)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully saved {output_path}")
        return True
    else:
        print(f"Failed to download: HTTP {response.status_code}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert Google Sheets to Excel format')
    parser.add_argument('--dir', default='/workspaces/docs/Cell-prep-forms', 
                        help='Directory containing .gsheet files')
    args = parser.parse_args()
    
    # Find all .gsheet files
    gsheet_files = glob.glob(os.path.join(args.dir, '*.gsheet'))
    
    if not gsheet_files:
        print(f"No .gsheet files found in {args.dir}")
        return
    
    # Process each .gsheet file
    for gsheet_file in gsheet_files:
        file_name = os.path.basename(gsheet_file)
        base_name = os.path.splitext(file_name)[0]
        output_path = os.path.join(args.dir, f"{base_name}.xlsx")
        
        print(f"Converting {file_name} to {base_name}.xlsx...")
        
        # Extract document ID
        doc_id = extract_doc_id(gsheet_file)
        if not doc_id:
            print(f"Could not extract document ID from {file_name}")
            continue
        
        # Download as Excel
        download_as_excel(doc_id, output_path)

if __name__ == "__main__":
    main()