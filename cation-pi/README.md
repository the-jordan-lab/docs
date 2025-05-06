# Histidine Interface Visualization

This repository contains tools for visualizing histidine-mediated cation-π and π-π interactions in protein structures.

## Project Summary

- **Purpose**: Visualize histidine interfaces in protein structures, particularly for NDUFS7/ACOT9 interactions
- **Visualization Output**: Interactive HTML files with 3D molecular visualizations using py3Dmol
- **Analysis**: Identifies cation-π and π-π interactions involving histidine residues

## Files

- `his-interface-visualization.py`: Main script with complete functionality for batch processing
- `his_viz_single.py`: Helper module for processing single files interactively
- `ndufs7_vis_notebook.ipynb`: Jupyter notebook for interactive visualization of single structures

## Usage

### Prerequisites

```bash
pip install py3Dmol biopython jupyter notebook
```

### Interactive Visualization (Single Files)

1. Open the Jupyter notebook:
   ```bash
   jupyter notebook ndufs7_vis_notebook.ipynb
   ```
   
2. Or in VS Code:
   - Open the notebook file
   - Run each cell sequentially
   - Change `file_index` value to process different files

3. The notebook allows:
   - Listing all PDB/CIF files in the folder
   - Processing files one at a time
   - Visualizing specific files by name or index

### Batch Processing

For processing multiple files at once:

```bash
python his-interface-visualization.py ndufs-7-acot-9-mm-af2-models
```

## Visualization Features

- Surface representations of both chains
- Ribbon/cartoon view of protein backbone
- Highlighted histidine-mediated interfaces
- Labeled cation-π and π-π interactions
- Dotted lines showing interaction distances

## Output Files

- Individual HTML files for each structure
- Index page linking to all visualizations
- Manuscript figure builder for publication-ready figures

## Technical Notes

- Uses BioPython for structure parsing and manipulation
- Interactive 3D visualization with py3Dmol
- Detects histidine interactions using distance cutoffs (5Å)
- Groups output by anchor protein to prevent browser crashes 