# Multiblock Markdown Experiment Format

This new experiment format combines multiple YAML frontmatter blocks with rich Markdown sections to provide a more comprehensive lab notebook experience.

## Benefits of the Multiblock Format

- **Richer metadata organization** - Group related metadata in separate frontmatter blocks (experiment info, sample details, reagents)
- **Structured data collection** - Clear sections for raw data, analysis, interpretation, and next steps
- **Better data organization** - Automatic creation of data folders for raw data and figures
- **Task tracking integration** - Checkboxes in experiments can update TASKS.md
- **Team collaboration** - Discussion section for team comments and feedback

## Files Created in This Implementation

1. **New Template**
   - `Templates/experiment_multiblock.md`: The base template with placeholder sections

2. **Example Experiment**
   - `Experiments/EXP-0225-mRNA-stability-Huh7-HepG2-YBX1-knockdown.md`: Example for your mRNA stability assay
   
3. **Analysis Script**
   - `Analysis/EXP-0225_mRNA_stability_analysis.R`: R script template for analyzing mRNA stability data

4. **Data Directories**
   - `Data/EXP-0225/raw/`: For raw data files (qPCR data, RNA concentrations)
   - `Data/EXP-0225/figures/`: For plots and visualizations

5. **Code Integration**
   - `Agent/experiment_handler_patch.py`: Functions to add to `agent_runner.py` to handle the new format

## How to Use This Format

### Creating a New Experiment

In the chat, you can create a new experiment using:

```
Create a new multiblock experiment for [experiment type] using [cell lines] with the following conditions: [conditions]
```

The agent will:
1. Create the experiment file with appropriate frontmatter blocks
2. Set up data directories for raw data and figures
3. Generate a placeholder analysis script (if applicable)
4. Add tasks to TASKS.md

### Updating an Experiment

As you progress through the experiment, update specific sections:

```
Update experiment EXP-XXXX with Day 1 results: [results]
```

or

```
Mark task 2 as complete in experiment EXP-XXXX
```

### Tracking Progress

The experiment file contains a timeline with checkboxes for each step. When you check boxes in the "Next Steps" section, they can automatically update TASKS.md.

When you change the status to "completed", the system validates that all required sections are filled and opens an issue if something is missing.

### Adding Raw Data

Place your raw data files in the `Data/EXP-XXXX/raw/` directory and list them in the "Raw Data & Resources" section of the experiment file.

## Integration with Agent Runner

To integrate this functionality with your existing setup:

1. Add the functions from `Agent/experiment_handler_patch.py` to your `agent_runner.py` file
2. Update your function definition list to include the new multiblock experiment functions
3. Ensure proper imports (os, re, datetime) are at the top of your file

## Example Workflow

1. **Create experiment**: "Create a multiblock experiment for CRISPR knockout of gene X in HEK293T cells"
2. **Update progress**: "Update experiment EXP-0226 with Day 1 results: Transfection efficiency 85%"
3. **Check tasks**: "Mark tasks 1 and 2 as complete in experiment EXP-0226"
4. **Add data**: "Record that I've added qPCR data in Data/EXP-0226/raw/knockout_validation.xlsx"
5. **Complete experiment**: "Mark experiment EXP-0226 as completed with interpretation: Successful knockout with 95% efficiency"

## Customization

You can modify the template at `Templates/experiment_multiblock.md` to adjust the sections or add new ones specific to your lab's needs. 