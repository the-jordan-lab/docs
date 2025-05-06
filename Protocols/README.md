# Protocols Folder

This folder contains standard operating procedures and experimental protocols as YAML files.

## How to Add a New Protocol
- Use the protocol_template.yaml in Templates/ as a starting point.
- Name your file descriptively, e.g., `cell_staining_v1.yaml`.
- Fill in all required fields: name, id, description, author, created, version, materials, steps, notes.
- Submit via the lab agent or manually, then commit to the repository.

## YAML Schema Reference
See `Templates/protocol_template.yaml` for the required structure.

## Example Protocol
See `cell_staining_v1.yaml` in this folder for a complete example of a protocol file. Use it as a reference when creating new protocols.

### Example Usage
To add a new protocol, you can:
1. Use the lab agent and describe your protocol in natural language (e.g., "Create a protocol for cell lysis").
2. The agent will generate a YAML file similar to `cell_staining_v1.yaml`.
3. Review and edit as needed, then commit the file.

---
