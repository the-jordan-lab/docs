#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Histidine Interface Visualization Script for VS Code
===================================================
This script visualizes histidine-mediated cation-π and π-π interactions
in protein structures. It uses py3Dmol for visualization.

Adapted from the Jupyter notebook version for use in VS Code.

Usage:
    python his-interface-visualization.py path/to/pdb/folder

Notes:
    - Requires py3Dmol and biopython
    - Creates HTML files that can be opened in a web browser
    - Uses the same identification strategy for His-π and His-cation interactions
    - Creates separate HTML files for each anchor protein to prevent browser crashes
"""

import py3Dmol
import os
import time
import tempfile
import webbrowser
import argparse
import sys
import re
from pathlib import Path
from Bio import PDB
from datetime import datetime

# ------------------------------------------------------------------------------
# COLOR CONSTANTS
# ------------------------------------------------------------------------------
# Chain A Surfaces/Ribbons
CHAIN_A_SURFACE = '#4e79a7'    # Darker blue
# Chain A sidechain STICK color (lighter shade of blue)
CHAIN_A_STICK = '#85b0d5'

CHAIN_A_LABEL = '#2c4e6f'      # Dark blue for label text

# Chain B Surfaces/Ribbons/Sticks
CHAIN_B_SURFACE = '#f2be2b'    # Gold
CHAIN_B_STICK   = '#f2be2b'    # Same as surface, or pick a slight variant
CHAIN_B_LABEL   = '#8B4513'    # Dark brown for better contrast on gold

# ------------------------------------------------------------------------------
# HELPER CONSTANTS / FUNCTIONS
# ------------------------------------------------------------------------------
ONE_LETTER_MAP = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLN': 'Q', 'GLU': 'E', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

def three_to_one(resn):
    return ONE_LETTER_MAP.get(resn, 'X')

# Sets of residue types considered cationic or aromatic
CATION_RES = {'ARG', 'LYS'}
AROMATIC_RES = {'PHE', 'TYR', 'TRP', 'HIS'}

def extract_anchor_protein(filename):
    """
    Extract the anchor protein (Chain A) name from a filename.
    For example:
    - NDUFS7_Q123_PARTNER_Q456... would return "NDUFS7"
    - fold_2025_03_16_23_33_acad9_acat1_model_0.cif would return "ACAD9"
    """
    filename = os.path.basename(filename).lower()
    
    # Hardcoded normalization - if acad appears anywhere in the filename, return ACAD9
    if "acad" in filename and not "acad9" in filename:
        return "ACAD9"
    
    # Special case for fold pattern with date
    # fold_2025_03_16_23_33_acad9_acat1_model_0.cif
    fold_date_pattern = r'fold_\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_([a-z0-9]+)_'
    fold_date_match = re.search(fold_date_pattern, filename)
    if fold_date_match:
        protein = fold_date_match.group(1).upper()
        return protein
    
    # For names like NDUFS7_Q123_PARTNER
    underscore_pattern = r'^([a-z0-9]+)_'
    underscore_match = re.match(underscore_pattern, filename)
    if underscore_match:
        protein = underscore_match.group(1).upper()
        return protein
    
    # Last resort: split on underscore or dot and take first part
    parts = re.split(r'[_\.]', filename)
    if len(parts) > 1:
        # If first part is fold, use next non-numeric part
        if parts[0] == "fold":
            for part in parts[1:]:
                if not part.isdigit() and len(part) > 1 and part != "model":
                    return part.upper()
        # Otherwise use first part
        return parts[0].upper()
    
    # Fallback
    return filename[:10].upper()

def convert_cif_to_pdb(cif_file):
    """Convert a CIF file to PDB format using BioPython."""
    try:
        # Create a temporary file for the PDB output
        fd, temp_pdb = tempfile.mkstemp(suffix=".pdb")
        os.close(fd)

        # Parse the CIF file
        parser = PDB.MMCIFParser(QUIET=True)
        structure = parser.get_structure("structure", cif_file)

        # Write as PDB
        io = PDB.PDBIO()
        io.set_structure(structure)
        io.save(temp_pdb)

        return temp_pdb
    except Exception as e:
        print(f"Error converting {cif_file} to PDB: {e}")
        return None

def get_sidechain_top_atom(residue):
    """
    Returns the sidechain atom with the highest (max Z) position,
    excluding backbone atoms (N, CA, C, O).
    """
    top_atom = None
    max_z = float('-inf')
    for atom in residue:
        if atom.get_name() in ['N','CA','C','O']:
            continue
        z_val = atom.coord[2]
        if z_val > max_z:
            max_z = z_val
            top_atom = atom
    return top_atom

def find_histidine_pairs(chain_a, chain_b, distance_cutoff=5.0):
    """
    Identify cation–π or π–π interactions with at least one HIS residue.
    We do a naive check of all heavy-atom distances < distance_cutoff.
    Returns a list of (resA, resB, interaction_type),
    where interaction_type is '+:π' or 'π:π'.
    """
    pairs = []
    for residue_a in chain_a:
        resn_a = residue_a.get_resname()
        for residue_b in chain_b:
            resn_b = residue_b.get_resname()
            # One must be HIS, the other cationic or aromatic
            is_a_HIS = (resn_a == 'HIS')
            is_b_HIS = (resn_b == 'HIS')
            is_a_cation_or_aromatic = (resn_a in CATION_RES or resn_a in AROMATIC_RES)
            is_b_cation_or_aromatic = (resn_b in CATION_RES or resn_b in AROMATIC_RES)

            if (is_a_HIS and is_b_cation_or_aromatic) or (is_b_HIS and is_a_cation_or_aromatic):
                # Check distance
                for atom_a in residue_a:
                    for atom_b in residue_b:
                        try:
                            if (atom_a - atom_b) < distance_cutoff:
                                # Distinguish cation–π vs π–π
                                if (is_a_HIS and resn_b in CATION_RES) or (is_b_HIS and resn_a in CATION_RES):
                                    itype = '+:π'  # cation–π
                                else:
                                    itype = 'π:π'  # π–π
                                pairs.append((residue_a, residue_b, itype))
                                break
                        except Exception:
                            # Skip if distance calculation fails
                            continue
                    else:
                        continue
                    break
    return pairs

# ------------------------------------------------------------------------------
# HTML TEMPLATE FUNCTIONS
# ------------------------------------------------------------------------------
def create_html_header(title="Histidine Interface Visualization"):
    """Create the HTML header with required JavaScript libraries"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://3dmol.org/build/3Dmol-min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .viewer-container {{
            margin-bottom: 30px;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
        }}
        .view-title {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .viewer {{
            width: 600px;
            height: 400px;
            position: relative;
        }}
        .divider {{
            border-top: 1px solid #ccc;
            margin: 30px 0;
        }}
        button {{
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
            margin-right: 5px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        h2 {{
            margin-top: 30px;
        }}
        .index-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }}
        .protein-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            width: 200px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .protein-card:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .protein-card h3 {{
            margin-top: 0;
            color: #2c4e6f;
        }}
        .protein-card p {{
            color: #666;
            margin-bottom: 10px;
        }}
        .protein-card a {{
            display: inline-block;
            background: #4e79a7;
            color: white;
            padding: 8px 12px;
            text-decoration: none;
            border-radius: 4px;
        }}
        .protein-card a:hover {{
            background: #3d6491;
        }}
        .page-controls {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
            gap: 10px;
        }}
        .page-info {{
            display: inline-block;
            padding: 8px 16px;
            background-color: #f1f1f1;
            border-radius: 4px;
            margin: 0 10px;
        }}
        .model-page {{
            display: none;
        }}
        .model-page.active {{
            display: block;
        }}
        /* Light Mode Toggle Switch Styling */
        .toggle-label {{
            margin-right: 10px;
            font-weight: bold;
        }}
        .switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            vertical-align: middle;
        }}
        .switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}
        .slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
        }}
        .slider:before {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
        }}
        input:checked + .slider {{
            background-color: #2196F3;
        }}
        input:focus + .slider {{
            box-shadow: 0 0 1px #2196F3;
        }}
        input:checked + .slider:before {{
            transform: translateX(26px);
        }}
        .slider.round {{
            border-radius: 34px;
        }}
        .slider.round:before {{
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p>This visualization shows histidine-mediated cation-π and π-π interactions in protein structures.</p>
"""

def create_html_footer():
    """Create the HTML footer"""
    return """
</body>
</html>
"""

def create_index_html(output_dir, protein_files):
    """
    Create an index.html file that links to individual protein HTML files
    
    Parameters:
    - output_dir: Directory where the HTML files are stored
    - protein_files: Dictionary mapping protein names to file paths
    
    Returns:
    - Path to the index.html file
    """
    index_path = os.path.join(output_dir, "index.html")
    
    with open(index_path, 'w') as f:
        f.write(create_html_header("Histidine Interface Visualization - Index"))
        
        f.write("<h2>Protein Structures</h2>")
        
        # Add manuscript button at the top
        f.write("""
        <div style="margin: 20px 0;">
            <a href="manuscript.html" style="display: inline-block; background: #4CAF50; color: white; 
                                           padding: 10px 20px; text-decoration: none; border-radius: 4px;
                                           font-weight: bold; font-size: 16px;">
                Manuscript Figure Builder
            </a>
            <p>Create publication-ready figures with optimized layouts and visualization settings</p>
        </div>
        """)
        
        f.write("<p>Click on a protein to view its histidine interfaces:</p>")
        
        f.write("<div class='index-container'>")
        for protein, details in protein_files.items():
            html_file = os.path.basename(details['html_file'])
            file_count = details['file_count']
            
            f.write(f"""
            <div class='protein-card'>
                <h3>{protein}</h3>
                <p>{file_count} structure{"s" if file_count > 1 else ""}</p>
                <a href='{html_file}'>View Structures</a>
            </div>
            """)
        f.write("</div>")
        
        f.write(create_html_footer())
    
    return index_path

def create_viewer_div(file_path, view_counter, viewer_id, pdb_data, viewer_type, histidine_pairs=None):
    """
    Create a div for a py3Dmol viewer with its JavaScript
    
    Parameters:
    - file_path: Path to the original file
    - view_counter: Counter for this view
    - viewer_id: ID for the viewer div
    - pdb_data: PDB data as a string
    - viewer_type: 'ribbon' or 'label'
    - histidine_pairs: List of histidine pair tuples (only needed for 'label' viewer)
    
    Returns:
    - HTML string for the viewer div with embedded JavaScript
    """
    file_name = os.path.basename(file_path)
    
    title = f"<h2>File #{view_counter}: {file_name}</h2>"
    
    if viewer_type == 'ribbon':
        view_description = "<div class='view-title'>View 1: Surface + Ribbon (no labels)</div>"
    else:
        view_description = "<div class='view-title'>View 2: Surface only + labeled cation-π/π-π</div>"
    
    div = f"""
    <div class="viewer-container">
        {view_description}
        <div id="{viewer_id}" class="viewer"></div>
        <button id="save-{viewer_id}">Save Image</button>
    </div>
    
    <script>
        $(document).ready(function() {{
            // Setup viewer
            let viewer = $3Dmol.createViewer($("#{viewer_id}"), {{
                backgroundColor: "#f0f0f0",
                outline: true
            }});
            
            // Add PDB data
            let pdbData = `{pdb_data.replace('`', '\\`')}`;
            viewer.addModel(pdbData, "pdb");
            
            // Set view style
            viewer.setViewStyle({{
                style: 'outline',
                color: 'gray',
                width: 0.01
            }});
            
            // Add surfaces
            viewer.addSurface($3Dmol.SAS, {{opacity: 0.6, color: '{CHAIN_A_SURFACE}'}}, {{chain: 'A'}});
            viewer.addSurface($3Dmol.SAS, {{opacity: 0.6, color: '{CHAIN_B_SURFACE}'}}, {{chain: 'B'}});
    """
    
    if viewer_type == 'ribbon':
        # Add ribbon-specific JavaScript
        div += f"""
            // Ribbon (cartoon)
            viewer.setStyle({{chain: 'A'}}, {{cartoon: {{color: '{CHAIN_A_SURFACE}', opacity: 1.0}}}});
            viewer.setStyle({{chain: 'B'}}, {{cartoon: {{color: '{CHAIN_B_SURFACE}', opacity: 1.0}}}});
        """
    else:
        # Add label-specific JavaScript with histidine pairs highlighting
        div += """
            // Hide cartoon
            viewer.setStyle({model: -1}, {cartoon: {hidden: true}});
            
            // Track chain A and B data for labels
            let chainAData = {};
            let chainBData = {};
        """
        
        # Now add the histidine pairs
        if histidine_pairs:
            for i, (resA, resB, itype) in enumerate(histidine_pairs):
                chainA_id = resA.get_parent().id
                chainB_id = resB.get_parent().id
                resA_id = resA.get_id()[1]
                resB_id = resB.get_id()[1]
                
                colorA = CHAIN_A_STICK if chainA_id == 'A' else CHAIN_B_STICK
                colorB = CHAIN_A_STICK if chainB_id == 'A' else CHAIN_B_STICK
                
                div += f"""
                // Highlight pair {i+1}
                viewer.setStyle({{chain: '{chainA_id}', resi: {resA_id}}}, 
                               {{stick: {{color: '{colorA}', radius: 0.3}}}});
                viewer.setStyle({{chain: '{chainB_id}', resi: {resB_id}}}, 
                               {{stick: {{color: '{colorB}', radius: 0.3}}}});
                """
                
                # Add dotted line if we have the atom coordinates
                topA = get_sidechain_top_atom(resA)
                topB = get_sidechain_top_atom(resB)
                if topA and topB:
                    x1, y1, z1 = topA.coord
                    x2, y2, z2 = topB.coord
                    div += f"""
                    // Add dotted line for pair {i+1}
                    viewer.addLine({{
                        start: {{x: {float(x1)}, y: {float(y1)}, z: {float(z1)}}},
                        end: {{x: {float(x2)}, y: {float(y2)}, z: {float(z2)}}},
                        color: 'blue',
                        linewidth: 4,
                        dashed: true,
                        dashLength: 0.4,
                        gapLength: 0.2
                    }});
                    """
                
                # Store data for chain A labels
                if chainA_id == 'A':
                    resn_a = three_to_one(resA.get_resname())
                    div += f"""
                    // Store chain A data for residue {resA_id}
                    if (!chainAData['{resA_id}']) {{
                        chainAData['{resA_id}'] = {{
                            chain: '{chainA_id}',
                            resn: '{resn_a}',
                            types: []
                        }};
                    }}
                    if (!chainAData['{resA_id}'].types.includes('{itype}')) {{
                        chainAData['{resA_id}'].types.push('{itype}');
                    }}
                    """
                
                if chainB_id == 'A':
                    resn_b = three_to_one(resB.get_resname())
                    div += f"""
                    // Store chain A data for residue {resB_id}
                    if (!chainAData['{resB_id}']) {{
                        chainAData['{resB_id}'] = {{
                            chain: '{chainB_id}',
                            resn: '{resn_b}',
                            types: []
                        }};
                    }}
                    if (!chainAData['{resB_id}'].types.includes('{itype}')) {{
                        chainAData['{resB_id}'].types.push('{itype}');
                    }}
                    """
            
            # Now add code to add labels for cation-π or π-π interactions
            div += """
                // Add labels for interacting residues in Chain A
                for (const resnum in chainAData) {
                    const data = chainAData[resnum];
                    const labelText = `${data.resn}${resnum}`;
                    
                    viewer.addLabel(labelText, {
                        fontColor: 'black',
                        backgroundColor: 'rgba(255,255,255,0.7)',
                        backgroundOpacity: 0.7,
                        fontSize: 14,
                        fontWeight: 'bold',
                        inFront: true,
                        padding: 2
                    }, {chain: data.chain, resi: resnum, atom: 'CA'});
                }
            """
    
    # Common JavaScript for both viewer types
    div += f"""
            viewer.zoomTo();
            viewer.render();
            
            // Save button functionality
            $("#save-{viewer_id}").click(function() {{
                let png = viewer.pngURI();
                let a = document.createElement('a');
                a.href = png;
                a.download = '{os.path.basename(file_path)[:-4]}_{viewer_type}_view_{view_counter}.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }});
        }});
    </script>
    """
    
    return title + div

def create_manuscript_html_header(title="Manuscript Figure Builder"):
    """Create the HTML header for manuscript-friendly visualization page"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://3dmol.org/build/3Dmol-min.js"></script>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .manuscript-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .figure-panel {{
            border: 1px solid #ccc;
            padding: 15px;
            border-radius: 5px;
            background-color: white;
        }}
        .figure-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }}
        .figure-cell {{
            border: 1px dashed #ccc;
            padding: 5px;
            position: relative;
        }}
        .viewer {{
            width: 100%;
            height: auto;
            position: relative;
        }}
        h2, h3 {{
            margin-top: 20px;
        }}
        button {{
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
            margin-right: 5px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        .controls {{
            margin: 20px 0;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
        .inset-controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        .inset-controls label {{
            margin-right: 5px;
        }}
        .panel-label {{
            position: absolute;
            top: 0;
            left: 0;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 2px 6px;
            font-weight: bold;
            border-bottom-right-radius: 5px;
            z-index: 100;
        }}
        .figure-title {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .label-settings {{
            margin-top: 15px;
            border-top: 1px solid #ddd;
            padding-top: 15px;
        }}
        .color-picker {{
            display: inline-block;
            width: 30px;
            height: 20px;
            border: 1px solid #ccc;
            margin-right: 5px;
            vertical-align: middle;
        }}
        /* Light Mode Toggle Switch Styling */
        .toggle-label {{
            margin-right: 10px;
            font-weight: bold;
        }}
        .switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            vertical-align: middle;
        }}
        .switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}
        .slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
        }}
        .slider:before {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
        }}
        input:checked + .slider {{
            background-color: #2196F3;
        }}
        input:focus + .slider {{
            box-shadow: 0 0 1px #2196F3;
        }}
        input:checked + .slider:before {{
            transform: translateX(26px);
        }}
        .slider.round {{
            border-radius: 34px;
        }}
        .slider.round:before {{
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Create optimized views for manuscript figures. Group structures, create insets, and export ready-to-use figures.</p>
    <p><a href="index.html">← Back to Main Index</a></p>
    
    <div class="controls">
        <h3>Figure Settings</h3>
        <div>
            <button id="add-row-btn">Add Row</button>
            <button id="add-2col-btn">Add 2-Column Row</button>
            <button id="add-3col-btn">Add 3-Column Row</button>
            <button id="capture-figure-btn">Export Figure as PNG</button>
        </div>
        
        <div class="label-settings">
            <h4>Global Label Settings</h4>
            <div>
                <label>Font Size:</label>
                <select id="global-font-size">
                    <option value="20">Small (20px)</option>
                    <option value="28" selected>Medium (28px)</option>
                    <option value="36">Large (36px)</option>
                </select>
                
                <label style="margin-left:15px">Font Weight:</label>
                <select id="global-font-weight">
                    <option value="normal">Normal</option>
                    <option value="bold" selected>Bold</option>
                </select>
                
                <label style="margin-left:15px">Background:</label>
                <select id="global-background">
                    <option value="false">None</option>
                    <option value="true" selected>Show</option>
                </select>
            </div>
            <div style="margin-top:10px">
                <label>Chain A Label Color:</label>
                <input type="color" id="chain-a-color" value="#2c4e6f" class="color-picker">
                
                <label style="margin-left:15px">Chain B Label Color:</label>
                <input type="color" id="chain-b-color" value="#8B4513" class="color-picker">
                
                <label style="margin-left:15px">Stroke Width:</label>
                <select id="global-stroke-width">
                    <option value="2">Thin (2px)</option>
                    <option value="3" selected>Medium (3px)</option>
                    <option value="4">Thick (4px)</option>
                </select>
            </div>
        </div>
    </div>
    
    <div id="manuscript-container" class="manuscript-container">
        <!-- Rows and viewers will be added here -->
    </div>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# MAIN VISUALIZATION FUNCTIONS
# ------------------------------------------------------------------------------
def visualize_pdb(pdb_file, view_counter, output_html, page_num=0, total_pages=1):
    """Process a PDB file and add its visualizations to the HTML file"""
    try:
        # Parse structure
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure('model', pdb_file)

        # Check for chain A & B
        try:
            chain_a = structure[0]['A']
            chain_b = structure[0]['B']
        except KeyError:
            print(f"[SKIP] Could not find chain A or B in: {pdb_file}")
            return False

        # Find cation–π or π–π pairs with a cutoff of 5Å
        histidine_pairs = find_histidine_pairs(chain_a, chain_b, distance_cutoff=5.0)

        # Read PDB data into a string for py3Dmol
        with open(pdb_file, 'r') as fh:
            pdb_data = fh.read()

        # Determine if this view should be visible initially
        is_active = (page_num == 0)
        page_class = "model-page active" if is_active else "model-page"
        
        # Start a new page div
        page_html = f'<div class="{page_class}" data-page="{page_num}">\n'

        # Create HTML for first viewer (ribbons, no labels)
        ribbon_viewer_id = f"viewer1_{view_counter}"
        ribbon_html = create_viewer_div(pdb_file, view_counter, ribbon_viewer_id, 
                                         pdb_data, 'ribbon')
        
        # Create HTML for second viewer (no ribbons, with labels)
        label_viewer_id = f"viewer2_{view_counter}"
        label_html = create_viewer_div(pdb_file, view_counter, label_viewer_id, 
                                        pdb_data, 'label', histidine_pairs)
        
        # Add a divider between file sets
        divider = '<div class="divider"></div>'
        
        # Add light mode toggle controls if they don't exist yet
        light_mode_toggle = """
        <div style="margin: 20px 0; background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
            <span class="toggle-label">Light Mode:</span>
            <label class="switch">
                <input type="checkbox" id="light-mode-toggle" checked>
                <span class="slider round"></span>
            </label>
        </div>
        
        <script>
            // Light mode toggle functionality
            const lightModeToggle = document.getElementById('light-mode-toggle');
            let lightModeEnabled = true; // Default to light mode
            
            // Function to update all viewers based on light mode setting
            function updateViewers(isLightMode) {
                // Get all viewer divs on the page
                const viewerDivs = document.querySelectorAll('[id^="viewer"]');
                
                viewerDivs.forEach(viewerDiv => {
                    const viewerId = viewerDiv.id;
                    try {
                        // Create a new viewer with the appropriate background color
                        let viewer = $3Dmol.createViewer($(`#${viewerId}`), {
                            backgroundColor: isLightMode ? "#f0f0f0" : "black",
                            outline: true
                        });
                        
                        // Check what kind of viewer this is (ribbon or label)
                        const viewType = viewerId.includes('viewer1_') ? 'ribbon' : 'label';
                        
                        // Get the PDB data from the original viewer's model
                        const pdbData = pdbDataStore[viewerId];
                        if (!pdbData) return;
                        
                        // Add the model
                        viewer.addModel(pdbData, "pdb");
                        
                        // Add base styling
                        viewer.setViewStyle({
                            style: 'outline',
                            color: 'gray',
                            width: 0.01
                        });
                        
                        // Add surfaces with appropriate opacity for light/dark mode
                        const opacity = isLightMode ? 0.6 : 0.3;
                        viewer.addSurface($3Dmol.SAS, {opacity: opacity, color: '{CHAIN_A_SURFACE}'}, {chain: 'A'});
                        viewer.addSurface($3Dmol.SAS, {opacity: opacity, color: '{CHAIN_B_SURFACE}'}, {chain: 'B'});
                        
                        // Add viewer-specific styling
                        if (viewType === 'ribbon') {
                            // Ribbon view
                            viewer.setStyle({chain: 'A'}, {cartoon: {color: '{CHAIN_A_SURFACE}', opacity: 1.0}});
                            viewer.setStyle({chain: 'B'}, {cartoon: {color: '{CHAIN_B_SURFACE}', opacity: 1.0}});
                        } else {
                            // Label view
                            viewer.setStyle({model: -1}, {cartoon: {hidden: true}});
                            
                            // Get histidine pairs for this viewer
                            const histidinePairs = histidinePairsStore[viewerId];
                            if (histidinePairs) {
                                // Apply the histidine pairs highlighting and labels
                                for (const pair of histidinePairs) {
                                    viewer.setStyle({chain: pair.chainA, resi: pair.resA}, 
                                                  {stick: {color: pair.colorA, radius: 0.3}});
                                    viewer.setStyle({chain: pair.chainB, resi: pair.resB}, 
                                                  {stick: {color: pair.colorB, radius: 0.3}});
                                    
                                    // Add dotted line if coordinates are available
                                    if (pair.coordsA && pair.coordsB) {
                                        viewer.addLine({
                                            start: pair.coordsA,
                                            end: pair.coordsB,
                                            color: 'blue',
                                            linewidth: 4,
                                            dashed: true,
                                            dashLength: 0.4,
                                            gapLength: 0.2
                                        });
                                    }
                                }
                                
                                // Add labels for Chain A residues
                                for (const data of pair.chainALabels) {
                                    const labelText = `${data.resn}${data.resnum}`;
                                    
                                    viewer.addLabel(labelText, {
                                        fontColor: isLightMode ? 'black' : 'white',
                                        strokeColor: isLightMode ? 'white' : 'black',
                                        strokeWidth: 3,
                                        fontSize: 28,
                                        fontWeight: 'bold',
                                        showBackground: true,
                                        backgroundColor: 'rgba(255,255,255,0.5)',
                                        backgroundOpacity: 0.5,
                                        inFront: true
                                    }, {chain: 'A', resi: data.resnum, atom: 'CA'});
                                }
                            }
                        }
                        
                        // Finish setup
                        viewer.zoomTo();
                        viewer.render();
                    } catch (e) {
                        console.error(`Error updating viewer ${viewerId}:`, e);
                        // If there's an error, don't stop the whole process
                    }
                });
            }
            
            // Add the event listener with try-catch to prevent crashes
            if (lightModeToggle) {
                lightModeToggle.addEventListener('change', function() {
                    lightModeEnabled = this.checked;
                    try {
                        updateViewers(lightModeEnabled);
                    } catch (e) {
                        console.error('Error updating viewers on light mode toggle:', e);
                    }
                });
            }
            
            // Store PDB data and histidine pairs for light mode toggle
            const pdbDataStore = {};
            const histidinePairsStore = {};
        </script>
        """
        
        # Add the light mode toggle after the first viewer if this is the first structure
        if page_num == 0 and view_counter == 1:
            page_html += light_mode_toggle
        
        # End the page div
        page_html += ribbon_html + label_html + divider + '</div>\n'
        
        # Append to HTML file
        with open(output_html, 'a') as html_file:
            html_file.write(page_html)
            
        print(f"Added visualizations for: {os.path.basename(pdb_file)}")
        return True
        
    except Exception as e:
        print(f"Error processing {pdb_file}: {e}")
        return False

def visualize_cif(cif_file, view_counter, output_html, page_num=0, total_pages=1):
    """Process a CIF file and add its visualizations to the HTML file"""
    # Convert CIF to PDB temporarily
    temp_pdb = None
    try:
        temp_pdb = convert_cif_to_pdb(cif_file)
        if not temp_pdb:
            print(f"[SKIP] Could not convert CIF to PDB: {cif_file}")
            return False
            
        # Now process the temporary PDB
        result = visualize_pdb(temp_pdb, view_counter, output_html, page_num, total_pages)
        
        # If successful, add a note that this was from a CIF
        if result:
            print(f"Processed CIF file: {os.path.basename(cif_file)}")
            
        return result
        
    except Exception as e:
        print(f"Error processing CIF {cif_file}: {e}")
        return False
        
    finally:
        # Clean up temporary PDB file
        if temp_pdb and os.path.exists(temp_pdb):
            os.remove(temp_pdb)

def create_manuscript_page(output_dir, protein_files):
    """
    Create a manuscript figure builder page that allows creating optimized
    publication-ready figures from the protein visualizations
    
    Parameters:
    - output_dir: Directory where the HTML files are stored
    - protein_files: Dictionary mapping protein names to file paths
    
    Returns:
    - Path to the manuscript.html file
    """
    manuscript_path = os.path.join(output_dir, "manuscript.html")
    
    # Create a dictionary to hold PDB data for each individual file
    file_data = {}
    file_counter = 0
    
    # For each protein, process all its files
    for protein, details in protein_files.items():
        for file_info in details['files']:
            file_path = file_info['path']
            file_name = os.path.basename(file_path)
            is_cif = file_info['is_cif']
            
            # Limit to 10 files per protein to prevent memory issues
            file_counter += 1
            if file_counter > 10 and protein in file_data and len(file_data[protein]) >= 3:
                continue
            
            try:
                # Get PDB data either directly from PDB or by converting CIF
                if is_cif:
                    temp_pdb = convert_cif_to_pdb(file_path)
                    if temp_pdb:
                        with open(temp_pdb, 'r') as f:
                            pdb_data = f.read()
                        # Clean up temp file
                        os.remove(temp_pdb)
                else:
                    with open(file_path, 'r') as f:
                        pdb_data = f.read()
                
                # Parse the structure to find histidine pairs
                parser = PDB.PDBParser(QUIET=True)
                structure = None
                
                if is_cif:
                    temp_pdb = convert_cif_to_pdb(file_path)
                    if temp_pdb:
                        structure = parser.get_structure('model', temp_pdb)
                        os.remove(temp_pdb)
                else:
                    structure = parser.get_structure('model', file_path)
                
                histidine_pairs = []
                if structure:
                    try:
                        chain_a = structure[0]['A']
                        chain_b = structure[0]['B']
                        histidine_pairs = find_histidine_pairs(chain_a, chain_b, distance_cutoff=5.0)
                    except (KeyError, Exception) as e:
                        print(f"Warning: Could not analyze chains in {file_path}: {e}")
                
                # Store the PDB data and histidine pairs
                pairs_with_coords = []
                for pair in histidine_pairs:
                    resA, resB, itype = pair
                    
                    # Get top sidechain atoms
                    topA = get_sidechain_top_atom(resA)
                    topB = get_sidechain_top_atom(resB)
                    
                    # Create pair data
                    pair_data = {
                        'chainA': resA.get_parent().id,
                        'resA': resA.get_id()[1],
                        'resnA': three_to_one(resA.get_resname()),
                        'chainB': resB.get_parent().id,
                        'resB': resB.get_id()[1],
                        'resnB': three_to_one(resB.get_resname()),
                        'type': itype
                    }
                    
                    # Add coordinates if available
                    if topA:
                        pair_data['coordsA'] = {
                            'x': float(topA.coord[0]),
                            'y': float(topA.coord[1]),
                            'z': float(topA.coord[2])
                        }
                    
                    if topB:
                        pair_data['coordsB'] = {
                            'x': float(topB.coord[0]),
                            'y': float(topB.coord[1]),
                            'z': float(topB.coord[2])
                        }
                    
                    pairs_with_coords.append(pair_data)
                
                # Initialize the protein entry if it doesn't exist
                if protein not in file_data:
                    file_data[protein] = {}
                
                # Add this file's data
                file_data[protein][file_name] = {
                    'pdb_data': pdb_data,
                    'histidine_pairs': pairs_with_coords,
                    'file_path': file_path,
                    'is_cif': is_cif
                }
                
                print(f"Extracted data for {file_name} ({protein})")
                
            except Exception as e:
                print(f"Error extracting data for {file_name}: {e}")
    
    with open(manuscript_path, 'w') as f:
        f.write(create_manuscript_html_header())
        
        # Add JavaScript to populate the available files
        f.write("<script>\n")
        f.write("// Available protein structures with PDB data\n")
        f.write("const availableFiles = {\n")
        
        for protein, files in file_data.items():
            f.write(f"    '{protein}': {{\n")
            
            for file_name, data in files.items():
                escaped_file = file_name.replace('\\', '\\\\').replace('`', '\\`').replace("'", "\\'")
                escaped_pdb = data['pdb_data'].replace('\\', '\\\\').replace('`', '\\`').replace("'", "\\'")
                
                f.write(f"        '{escaped_file}': {{\n")
                f.write(f"            id: '{escaped_file}',\n")
                f.write(f"            name: '{escaped_file}',\n")
                f.write(f"            protein: '{protein}',\n")
                f.write(f"            pdbData: `{escaped_pdb}`,\n")
                f.write(f"            histidinePairs: {str(data['histidine_pairs']).replace("'", '"')},\n")
                f.write(f"        }},\n")
            
            f.write(f"    }},\n")
        
        f.write("};\n\n")
        
        # Add the manuscript builder JavaScript
        f.write("""
// Global settings that will be applied to new viewers
const globalSettings = {
    fontSize: 28,
    fontWeight: 'bold',
    showBackground: true,
    chainAColor: '#2c4e6f',
    chainBColor: '#8B4513',
    strokeWidth: 3
};

// Organize files by protein for the dropdown
const proteinGroups = {};
for (const protein in availableFiles) {
    const files = availableFiles[protein];
    proteinGroups[protein] = Object.keys(files);
}

// Load and display a protein structure with specified options
function loadStructure(protein, fileName, viewerId, viewType) {
    if (!protein || !fileName || !availableFiles[protein] || !availableFiles[protein][fileName]) {
        console.error(`File not found: ${protein}/${fileName}`);
        return;
    }
    
    const fileData = availableFiles[protein][fileName];
    if (!fileData.pdbData) {
        console.error(`No PDB data available for ${fileName}`);
        return;
    }
    
    try {
        // Create viewer
        let viewer = $3Dmol.createViewer($(`#${viewerId}`), {
            backgroundColor: "#f0f0f0"
        });
        
        // Add the PDB data
        viewer.addModel(fileData.pdbData, "pdb");
        
        // Set basic view style
        viewer.setViewStyle({
            style: 'outline',
            color: 'gray',
            width: 0.01
        });
        
        // Add surfaces
        viewer.addSurface($3Dmol.SAS, {opacity: 0.6, color: '#4e79a7'}, {chain: 'A'});
        viewer.addSurface($3Dmol.SAS, {opacity: 0.6, color: '#f2be2b'}, {chain: 'B'});
        
        if (viewType === 'ribbon') {
            // Ribbon view - add cartoon representation
            viewer.setStyle({chain: 'A'}, {cartoon: {color: '#4e79a7', opacity: 1.0}});
            viewer.setStyle({chain: 'B'}, {cartoon: {color: '#f2be2b', opacity: 1.0}});
        } else {
            // Label view - show sticks and labels for histidine interactions
            viewer.setStyle({model: -1}, {cartoon: {hidden: true}});
            
            // Create data structures for labels
            let chainAData = {};
            let chainBData = {};
            
            // Process histidine pairs
            for (const pair of fileData.histidinePairs) {
                // Set sticks for the residues
                const colorA = pair.chainA === 'A' ? '#85b0d5' : '#f2be2b';
                const colorB = pair.chainB === 'A' ? '#85b0d5' : '#f2be2b';
                
                viewer.setStyle({chain: pair.chainA, resi: pair.resA}, 
                                {stick: {color: colorA, radius: 0.3}});
                viewer.setStyle({chain: pair.chainB, resi: pair.resB}, 
                                {stick: {color: colorB, radius: 0.3}});
                
                // Add dotted line if coordinates are available
                if (pair.coordsA && pair.coordsB) {
                    viewer.addLine({
                        start: pair.coordsA,
                        end: pair.coordsB,
                        color: 'blue',
                        linewidth: 4,
                        dashed: true,
                        dashLength: 0.4,
                        gapLength: 0.2
                    });
                }
                
                // Add interaction data for Chain A
                if (pair.chainA === 'A') {
                    if (!chainAData[pair.resA]) {
                        chainAData[pair.resA] = {
                            chain: 'A',
                            resn: pair.resnA,
                            types: []
                        };
                    }
                    if (!chainAData[pair.resA].types.includes(pair.type)) {
                        chainAData[pair.resA].types.push(pair.type);
                    }
                }
                
                if (pair.chainB === 'A') {
                    if (!chainAData[pair.resB]) {
                        chainAData[pair.resB] = {
                            chain: 'A',
                            resn: pair.resnB,
                            types: []
                        };
                    }
                    if (!chainAData[pair.resB].types.includes(pair.type)) {
                        chainAData[pair.resB].types.push(pair.type);
                    }
                }
                
                // Add data for Chain B
                if (pair.chainA === 'B') {
                    chainBData[pair.resA] = {
                        chain: 'B',
                        resn: pair.resnA
                    };
                }
                
                if (pair.chainB === 'B') {
                    chainBData[pair.resB] = {
                        chain: 'B',
                        resn: pair.resnB
                    };
                }
            }
            
            // Add labels for Chain A
            for (const resnum in chainAData) {
                const data = chainAData[resnum];
                const labelText = `${data.resn}${resnum}`;
                
                viewer.addLabel(labelText, {
                    fontColor: globalSettings.chainAColor,
                    strokeColor: 'white',
                    strokeWidth: globalSettings.strokeWidth,
                    fontSize: globalSettings.fontSize,
                    fontWeight: globalSettings.fontWeight,
                    showBackground: globalSettings.showBackground,
                    backgroundColor: 'rgba(255,255,255,0.5)',
                    backgroundOpacity: 0.5,
                    inFront: true
                }, {chain: data.chain, resi: resnum, atom: 'CA'});
            }
            
            // Add labels for Chain B
            for (const resnum in chainBData) {
                const data = chainBData[resnum];
                const labelText = `${data.resn}${resnum}`;
                
                viewer.addLabel(labelText, {
                    fontColor: globalSettings.chainBColor,
                    strokeColor: 'black',
                    strokeWidth: globalSettings.strokeWidth,
                    fontSize: globalSettings.fontSize,
                    fontWeight: globalSettings.fontWeight,
                    showBackground: globalSettings.showBackground,
                    backgroundColor: 'rgba(255,255,255,0.5)',
                    backgroundOpacity: 0.5,
                    inFront: true
                }, {chain: data.chain, resi: resnum, atom: 'CA'});
            }
        }
        
        viewer.zoomTo();
        viewer.render();
        console.log(`Successfully loaded ${fileName} in ${viewType} view`);
    } catch (e) {
        console.error(`Error loading structure ${fileName}:`, e);
    }
}

// Add a new row to the figure
function addRow(numCols = 1) {
    const container = document.getElementById('manuscript-container');
    const rowIndex = container.children.length + 1;
    
    const row = document.createElement('div');
    row.className = 'figure-row';
    row.id = `row-${rowIndex}`;
    
    for (let i = 1; i <= numCols; i++) {
        const cell = document.createElement('div');
        cell.className = 'figure-cell';
        
        const cellControls = document.createElement('div');
        cellControls.innerHTML = `
            <div style="margin-bottom:10px">
                <select class="protein-select" data-row="${rowIndex}" data-col="${i}">
                    <option value="">Select protein...</option>
                    ${Object.keys(proteinGroups).map(p => `<option value="${p}">${p}</option>`).join('')}
                </select>
                
                <select class="file-select" data-row="${rowIndex}" data-col="${i}" disabled>
                    <option value="">Select file...</option>
                </select>
                
                <select class="view-type" data-row="${rowIndex}" data-col="${i}">
                    <option value="ribbon">Ribbon view</option>
                    <option value="label">Labeled view</option>
                </select>
            </div>
            <div class="viewer-container">
                <div class="panel-label">${String.fromCharCode(64 + rowIndex)}${i}</div>
                <div id="viewer-${rowIndex}-${i}" class="viewer"></div>
            </div>
        `;
        
        cell.appendChild(cellControls);
        row.appendChild(cell);
    }
    
    container.appendChild(row);
    
    // Add event listeners to the new selects
    row.querySelectorAll('.protein-select').forEach(select => {
        select.addEventListener('change', function() {
            const row = this.dataset.row;
            const col = this.dataset.col;
            const protein = this.value;
            const fileSelect = document.querySelector(`.file-select[data-row="${row}"][data-col="${col}"]`);
            
            // Clear and update the file select
            fileSelect.innerHTML = '<option value="">Select file...</option>';
            fileSelect.disabled = !protein;
            
            if (protein && proteinGroups[protein]) {
                proteinGroups[protein].forEach(fileName => {
                    const option = document.createElement('option');
                    option.value = fileName;
                    option.textContent = fileName;
                    fileSelect.appendChild(option);
                });
            }
        });
    });
    
    row.querySelectorAll('.file-select').forEach(select => {
        select.addEventListener('change', function() {
            const row = this.dataset.row;
            const col = this.dataset.col;
            const protein = document.querySelector(`.protein-select[data-row="${row}"][data-col="${col}"]`).value;
            const fileName = this.value;
            const viewType = document.querySelector(`.view-type[data-row="${row}"][data-col="${col}"]`).value;
            const viewerId = `viewer-${row}-${col}`;
            
            if (protein && fileName) {
                loadStructure(protein, fileName, viewerId, viewType);
            }
        });
    });
    
    row.querySelectorAll('.view-type').forEach(select => {
        select.addEventListener('change', function() {
            const row = this.dataset.row;
            const col = this.dataset.col;
            const protein = document.querySelector(`.protein-select[data-row="${row}"][data-col="${col}"]`).value;
            const fileName = document.querySelector(`.file-select[data-row="${row}"][data-col="${col}"]`).value;
            const viewerId = `viewer-${row}-${col}`;
            
            if (protein && fileName) {
                loadStructure(protein, fileName, viewerId, this.value);
            }
        });
    });
}

// Capture the figure as an image
function captureFigure() {
    html2canvas(document.getElementById('manuscript-container')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'manuscript-figure.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
}

// Event listeners for the control buttons
document.getElementById('add-row-btn').addEventListener('click', () => addRow(1));
document.getElementById('add-2col-btn').addEventListener('click', () => addRow(2));
document.getElementById('add-3col-btn').addEventListener('click', () => addRow(3));
document.getElementById('capture-figure-btn').addEventListener('click', captureFigure);

// Update global settings when controls change
document.getElementById('global-font-size').addEventListener('change', function() {
    globalSettings.fontSize = parseInt(this.value);
});

document.getElementById('global-font-weight').addEventListener('change', function() {
    globalSettings.fontWeight = this.value;
});

document.getElementById('global-background').addEventListener('change', function() {
    globalSettings.showBackground = this.value === 'true';
});

document.getElementById('chain-a-color').addEventListener('change', function() {
    globalSettings.chainAColor = this.value;
});

document.getElementById('chain-b-color').addEventListener('change', function() {
    globalSettings.chainBColor = this.value;
});

document.getElementById('global-stroke-width').addEventListener('change', function() {
    globalSettings.strokeWidth = parseInt(this.value);
});
</script>
</body>
</html>
""")
    
    return manuscript_path

def visualize_folder(folder_path, output_dir=None):
    """
    Process all PDB and CIF files in a folder and create HTML visualizations.
    Groups files by anchor protein (Chain A) and creates separate HTML files
    for each protein to avoid browser crashes.
    
    Parameters:
    - folder_path: Path to folder containing PDB and/or CIF files
    - output_dir: Directory for output HTML (defaults to same as folder_path)
    
    Returns:
    - Path to the index.html file that links to individual protein HTML files
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        return None
        
    if not output_dir:
        output_dir = folder_path
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Group files by anchor protein
    protein_files = {}
    all_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in sorted(files):
            file_lower = file.lower()
            file_path = os.path.join(root, file)
            
            if file_lower.endswith('.pdb') or file_lower.endswith('.cif'):
                protein = extract_anchor_protein(file)
                
                if protein not in protein_files:
                    protein_files[protein] = {
                        'files': [],
                        'file_count': 0,
                        'html_file': None
                    }
                
                protein_files[protein]['files'].append({
                    'path': file_path,
                    'is_cif': file_lower.endswith('.cif')
                })
                protein_files[protein]['file_count'] += 1
                all_files.append(file_path)
    
    # Create HTML file for each protein
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for protein, details in protein_files.items():
        # Create an HTML file for this protein
        html_filename = f"histidine_{protein.lower()}_{timestamp}.html"
        html_path = os.path.join(output_dir, html_filename)
        protein_files[protein]['html_file'] = html_path
        
        # Initialize the HTML file with header
        with open(html_path, 'w') as html_file:
            html_file.write(create_html_header(f"Histidine Interface - {protein}"))
            html_file.write(f"<p><a href='index.html'>← Back to Index</a> | <a href='manuscript.html'>Manuscript Figure Builder</a></p>")
        
        # Process all files for this protein in paginated groups of 3
        view_counter = 1
        file_count = 0
        max_models_per_page = 3
        total_files = len(details['files'])
        total_pages = (total_files + max_models_per_page - 1) // max_models_per_page
        
        # Add navigation controls at the top
        with open(html_path, 'a') as html_file:
            html_file.write(f"""
            <div class="page-controls">
                <button id="prev-page" disabled>← Previous</button>
                <span class="page-info">Page <span id="current-page">1</span> of {total_pages}</span>
                <button id="next-page" {'' if total_pages > 1 else 'disabled'}>Next →</button>
            </div>
            """)
        
        # Process files in groups of max_models_per_page
        current_page = 0
        for i, file_info in enumerate(details['files']):
            file_path = file_info['path']
            is_cif = file_info['is_cif']
            page_num = i // max_models_per_page
            
            success = False
            if is_cif:
                success = visualize_cif(file_path, view_counter, html_path, page_num, total_pages)
            else:
                success = visualize_pdb(file_path, view_counter, html_path, page_num, total_pages)
                
            if success:
                view_counter += 1
                file_count += 1
        
        # Add pagination JavaScript
        with open(html_path, 'a') as html_file:
            html_file.write("""
            <script>
                // Pagination functionality
                document.addEventListener('DOMContentLoaded', function() {
                    const pages = document.querySelectorAll('.model-page');
                    const prevButton = document.getElementById('prev-page');
                    const nextButton = document.getElementById('next-page');
                    const currentPageSpan = document.getElementById('current-page');
                    
                    let currentPage = 0;
                    const totalPages = pages.length;
                    
                    // Function to show the current page and hide others
                    function showPage(pageIndex) {
                        pages.forEach((page, index) => {
                            page.classList.toggle('active', index === pageIndex);
                        });
                        
                        // Update current page indicator
                        currentPageSpan.textContent = pageIndex + 1;
                        
                        // Update button states
                        prevButton.disabled = pageIndex === 0;
                        nextButton.disabled = pageIndex === totalPages - 1;
                    }
                    
                    // Set up event listeners for navigation buttons
                    prevButton.addEventListener('click', function() {
                        if (currentPage > 0) {
                            currentPage--;
                            showPage(currentPage);
                        }
                    });
                    
                    nextButton.addEventListener('click', function() {
                        if (currentPage < totalPages - 1) {
                            currentPage++;
                            showPage(currentPage);
                        }
                    });
                    
                    // Initialize with the first page
                    showPage(0);
                });
            </script>
            """)
        
        # Finalize the HTML file
        with open(html_path, 'a') as html_file:
            html_file.write(create_html_footer())
        
        protein_files[protein]['file_count'] = file_count
        print(f"Created HTML for {protein} with {file_count} files: {html_filename}")
    
    # Create index.html with links to all protein HTML files
    index_path = create_index_html(output_dir, protein_files)
    
    # Create manuscript figure builder page
    manuscript_path = create_manuscript_page(output_dir, protein_files)
    print(f"Created manuscript figure builder page: {os.path.basename(manuscript_path)}")
    
    print(f"Processed {len(all_files)} files. Index page saved to: {index_path}")
    
    return index_path

# ------------------------------------------------------------------------------
# COMMAND LINE INTERFACE
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualize histidine interfaces in protein structures')
    parser.add_argument('folder', type=str, help='Path to folder containing PDB/CIF files')
    parser.add_argument('--output', '-o', type=str, help='Output directory for HTML files', default=None)
    parser.add_argument('--open', '-p', action='store_true', help='Open HTML in browser when done')
    
    args = parser.parse_args()
    
    # Check for required dependencies
    try:
        import py3Dmol
    except ImportError:
        print("Error: py3Dmol is required but not installed.")
        print("Please install it with: pip install py3Dmol")
        sys.exit(1)
    
    try:
        from Bio import PDB
    except ImportError:
        print("Error: Biopython is required but not installed.")
        print("Please install it with: pip install biopython")
        sys.exit(1)
    
    # Process the folder
    index_html = visualize_folder(args.folder, args.output)
    
    # Open in browser if requested
    if args.open and index_html:
        print(f"Opening HTML in browser: {index_html}")
        webbrowser.open('file://' + os.path.abspath(index_html))

if __name__ == "__main__":
    main() 