# Experiments Folder

This folder contains records of individual experiments or lab sessions as YAML files.

## How to Add a New Experiment
- Use the experiment_template.yaml in Templates/ as a starting point.
- Name your file with a unique ID or date, e.g., `2025-05-10_cell_staining_Alice.yaml`.
- Fill in all required fields: experiment_id, project, title, date, researcher, protocol, materials, parameters, results, status.
- Submit via the lab agent or manually, then commit to the repository.

## YAML Schema Reference
See `Templates/experiment_template.yaml` for the required structure.

## Example Experiment
See `2025-05-10_cell_staining_Alice.yaml` in this folder for a complete example of an experiment file. Use it as a reference when creating new experiments.

### Example Usage
To add a new experiment, you can:
1. Use the lab agent and describe your experiment in natural language (e.g., "Log a cell staining experiment for Alice on May 10, 2025").
2. The agent will generate a YAML file similar to `2025-05-10_cell_staining_Alice.yaml`.
3. Review and edit as needed, then commit the file.
