#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Histidine Interface Visualization for Single Files
==================================================
This version of the visualization script is adapted for processing 
single files interactively in Jupyter notebooks.

Usage in a notebook:
    import his_viz_single as hvs
    hvs.list_available_files("ndufs-7-acot-9-mm-af2-models")
    hvs.visualize_single_file("ndufs-7-acot-9-mm-af2-models/your_file.pdb")
"""

import py3Dmol
import os
import tempfile
import glob
from Bio import PDB
from datetime import datetime
from IPython.display import HTML

# Import functions from the main script
try:
    from his_interface_visualization import (
        create_html_header, 
        create_html_footer, 
        visualize_pdb, 
        visualize_cif,
        ONE_LETTER_MAP,
        CATION_RES,
        AROMATIC_RES,
        extract_anchor_protein,
        convert_cif_to_pdb,
        get_sidechain_top_atom,
        find_histidine_pairs
    )
except ImportError:
    # If we can't import directly, try using runpy
    import runpy
    hisvis = runpy.run_path('his-interface-visualization.py')
    
    # Extract the functions we need
    create_html_header = hisvis['create_html_header']
    create_html_footer = hisvis['create_html_footer']
    visualize_pdb = hisvis['visualize_pdb']
    visualize_cif = hisvis['visualize_cif']
    ONE_LETTER_MAP = hisvis['ONE_LETTER_MAP']
    CATION_RES = hisvis['CATION_RES']
    AROMATIC_RES = hisvis['AROMATIC_RES']
    extract_anchor_protein = hisvis['extract_anchor_protein']
    convert_cif_to_pdb = hisvis['convert_cif_to_pdb']
    get_sidechain_top_atom = hisvis['get_sidechain_top_atom']
    find_histidine_pairs = hisvis['find_histidine_pairs']

# Output directory for generated HTML files
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def list_available_files(folder_path):
    """List all PDB and CIF files in the specified folder."""
    pdb_files = glob.glob(os.path.join(folder_path, '*.pdb'))
    cif_files = glob.glob(os.path.join(folder_path, '*.cif'))
    all_files = sorted(pdb_files + cif_files)
    
    print(f"Found {len(all_files)} PDB/CIF files in {folder_path}:")
    for i, file in enumerate(all_files):
        protein = extract_anchor_protein(file)
        print(f"{i+1}. {os.path.basename(file)} ({protein})")
    
    return all_files

def visualize_single_file(file_path, output_dir=OUTPUT_DIR):
    """
    Visualize a single PDB or CIF file and create an HTML visualization.
    
    Parameters:
    - file_path: Path to the PDB or CIF file
    - output_dir: Directory to save the HTML output
    
    Returns:
    - HTML display object with link to the visualization, or None if failed
    """
    file_name = os.path.basename(file_path)
    is_cif = file_name.lower().endswith('.cif')
    
    # Create HTML file for this structure
    output_html = os.path.join(output_dir, f"single_{file_name.replace('.', '_')}.html")
    
    # Initialize HTML with header
    with open(output_html, 'w') as f:
        f.write(create_html_header(f"Single View - {file_name}"))
    
    # Process the file
    if is_cif:
        success = visualize_cif(file_path, 1, output_html)
    else:
        success = visualize_pdb(file_path, 1, output_html)
    
    # Finalize HTML
    with open(output_html, 'a') as f:
        f.write(create_html_footer())
    
    if success:
        print(f"Successfully visualized {file_name}")
        print(f"HTML saved to: {output_html}")
        return HTML(f"<a href='{output_html}' target='_blank'>Open {file_name} Visualization</a>")
    else:
        print(f"Failed to visualize {file_name}")
        return None

def process_by_index(folder_path, file_index, output_dir=OUTPUT_DIR):
    """
    Process a file by its index in the folder's file list.
    
    Parameters:
    - folder_path: Path to folder containing PDB/CIF files
    - file_index: 1-based index of the file to process
    - output_dir: Directory to save HTML output
    
    Returns:
    - HTML display object with link to visualization, or None if failed
    """
    all_files = list_available_files(folder_path)
    
    if 1 <= file_index <= len(all_files):
        selected_file = all_files[file_index - 1]
        print(f"Processing: {os.path.basename(selected_file)}")
        return visualize_single_file(selected_file, output_dir)
    else:
        print(f"Invalid file index. Please choose between 1 and {len(all_files)}")
        return None

def process_by_name(folder_path, file_name, output_dir=OUTPUT_DIR):
    """
    Process a file by its name within the folder.
    
    Parameters:
    - folder_path: Path to folder containing PDB/CIF files
    - file_name: Name of the file to process (e.g., "model_1.pdb")
    - output_dir: Directory to save HTML output
    
    Returns:
    - HTML display object with link to visualization, or None if failed
    """
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        return visualize_single_file(file_path, output_dir)
    else:
        print(f"File not found: {file_path}")
        return None

# Example usage when run as a script
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize a single protein structure file')
    parser.add_argument('file_path', type=str, help='Path to PDB or CIF file')
    parser.add_argument('--output', '-o', type=str, default=OUTPUT_DIR, 
                        help='Output directory for HTML files')
    args = parser.parse_args()
    
    visualize_single_file(args.file_path, args.output) 