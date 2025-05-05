# Histidine Interface Visualization Project - Progress Log

Date: April 15, 2024

## Project Overview

We've been adapting a Jupyter notebook script for visualizing histidine-mediated cation-π and π-π interactions into a standalone Python script (his-interface-visualization.py) that works in VS Code with py3Dmol visualization.

## Completed Improvements

1. **Separate HTML Files for Different Proteins**
   - Created individual HTML files for each anchor protein (Chain A) to prevent browser crashes
   - Added an index page with links to each protein's visualization page
   - Added manuscript figure builder tool for publication-ready figures

2. **CIF Filename Parsing**
   - Fixed the extraction of anchor protein names from CIF filenames
   - Added logic to parse patterns like `fold_2025_03_16_23_33_acad_acat1_model_0.cif` to extract "ACAD"
   - Added safeguards to prevent returning "FOLD" as an anchor protein name
   - Still seeing some files grouped under "FOLD" that need better parsing

3. **Label Visibility Improvements**
   - Increased font size from 20px to 28px for better readability
   - Changed Chain B label color from gold to dark brown (#8B4513) for better contrast against gold surface
   - Added semi-transparent white backgrounds behind labels
   - Increased stroke width around text from 2px to 3px
   - Changed Chain B stroke color from white to black for better visibility
   - Added comments in code to document these styling improvements

4. **Manuscript Figure Builder**
   - Created a new tool for building publication figures with multiple panels
   - Added ability to select different proteins and view types for each panel
   - Implemented global label settings for customizing appearance
   - Added size control for individual viewers (small, medium, large)
   - Added export to PNG functionality
   - Uses iframe approach to extract data from individual protein pages

5. **Code Organization**
   - Moved from Jupyter notebook to standalone Python script
   - Added proper command-line argument handling
   - Added documentation and docstrings
   - Improved error handling and messaging

## Remaining Issues

1. **Regex Pattern Escaping**
   - SyntaxWarning: invalid escape sequence '\(' in JavaScript regex
   - Need to properly escape backslashes in JavaScript regex patterns

2. **Some CIF Files Still Under "FOLD"**
   - Some CIF files are still being grouped under a "FOLD" category
   - Need to improve filename parsing for more variants

3. **Browser Stability**
   - While greatly improved, very large files might still cause slowness
   - Consider adding pagination for proteins with many structures

4. **JavaScript Integration**
   - The manuscript figure builder's dynamic loading of protein structures could be enhanced
   - Consider adding a loading indicator while structures load

## Usage Instructions

```bash
# Basic usage
python his-interface-visualization.py path/to/pdb/folder

# With output directory specified
python his-interface-visualization.py path/to/pdb/folder --output output_dir

# Auto-open in browser
python his-interface-visualization.py path/to/pdb/folder --open
```

## Next Steps

1. Fix the JavaScript regex escape warnings
2. Further refine the CIF filename parsing to reduce "FOLD" grouping
3. Enhance the manuscript figure builder UI for easier use
4. Add configuration options for colors and styling
5. Consider adding more export formats beyond PNG
6. Add option to modify distance cutoff via command line

## Dependencies

- py3Dmol
- Biopython
- jQuery (web interface)
- html2canvas (for PNG export) 