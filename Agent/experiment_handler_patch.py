"""
Code snippet to be added to agent_runner.py to handle creating experiments with multiblock markdown templates.
This would extend the existing functionality to support the richer experiment format.
"""

def handle_create_multiblock_experiment(self, args: Dict[str, Any]):
    """
    Handle creation of a new experiment using the multiblock markdown template.
    This creates a structured markdown file with multiple YAML frontmatter blocks
    and placeholder sections for data, analysis, and next steps.
    
    Args should include:
        title (str): Experiment title
        researchers (list): List of researchers involved
        protocol_id (str): Protocol ID (e.g., PROT-XXXX)
        protocol_name (str): Protocol name
        project (str): Project name
        aim (str): Brief description of experimental aim
        cell_lines (list): List of cell lines used
        plate_format (str): Plate format (e.g., 24-well)
        condition_map (str): Map of conditions in the plate
        additional_metadata (dict): Any additional metadata fields
    """
    # Load the multiblock template
    template_path = os.path.join("Templates", "experiment_multiblock.md")
    with open(template_path, "r") as f:
        template = f.read()
    
    # Generate experiment ID if not provided
    if not args.get("experiment_id"):
        # Generate unique ID with date-based prefix
        date_prefix = datetime.now().strftime("%Y%m%d")
        existing_ids = [f for f in os.listdir("Experiments") if f.startswith("EXP-")]
        existing_nums = [int(f.split("-")[1].split("_")[0]) 
                         for f in existing_ids if re.match(r"EXP-\d+", f)]
        next_num = max(existing_nums) + 1 if existing_nums else 1
        args["experiment_id"] = f"EXP-{next_num:04d}"
    
    # Current date if not provided
    if not args.get("date"):
        args["date"] = datetime.now().strftime("%Y-%m-%d")
    
    # Fill template with args
    # This is a simple placeholder - in a real implementation, we'd handle the
    # multiple frontmatter blocks more carefully
    for key, value in args.items():
        if isinstance(value, (str, int, float)):
            template = template.replace(f"{{{{{key}}}}}", str(value))
    
    # Generate filename with experiment ID and title
    experiment_id = args.get("experiment_id")
    title = args.get("title", "untitled").lower().replace(" ", "-")
    filename = f"{experiment_id}-{title}.md"
    out_path = os.path.join("Experiments", filename)
    
    # Ensure unique filename if exists
    i = 1
    base_filename = filename
    while os.path.exists(out_path):
        filename = f"{experiment_id}-{title}-{i}.md"
        out_path = os.path.join("Experiments", filename)
        i += 1
    
    # Create data directories for the experiment
    data_dir = os.path.join("Data", experiment_id)
    os.makedirs(os.path.join(data_dir, "raw"), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "figures"), exist_ok=True)
    
    # Create analysis script placeholder if needed
    analysis_dir = "Analysis"
    os.makedirs(analysis_dir, exist_ok=True)
    
    # Script path based on experiment type
    if args.get("analysis_type") == "mRNA_stability":
        script_path = os.path.join(analysis_dir, f"{experiment_id}_mRNA_stability_analysis.R")
        # Here we would create a placeholder R script tailored to mRNA stability analysis
    elif args.get("analysis_type") == "qPCR":
        script_path = os.path.join(analysis_dir, f"{experiment_id}_qPCR_analysis.R")
        # Create a placeholder qPCR analysis script
    
    # Write the experiment file
    with open(out_path, "w") as f:
        f.write(template)
    
    # Log the action
    self.logger.info(f"Created multiblock experiment: {out_path}")
    self.logger.info(f"Created data directories: {data_dir}/raw and {data_dir}/figures")
    
    # Update user profile
    for researcher in args.get("researchers", []):
        researcher_id = researcher.replace(" ", "_").lower()
        self._update_user_profile(researcher_id, "recent_experiments", experiment_id)
        for cell_line in args.get("cell_lines", []):
            if isinstance(cell_line, dict) and "name" in cell_line:
                self._update_user_profile(researcher_id, "frequent_cell_lines", cell_line["name"])
            elif isinstance(cell_line, str):
                self._update_user_profile(researcher_id, "frequent_cell_lines", cell_line)
    
    # Append to CHANGELOG.md
    self.append_changelog(f"Created new multiblock experiment {experiment_id}: {args.get('title')}")
    
    # Check if there are any experiment tasks to add to TASKS.md
    if args.get("next_steps"):
        self.add_experiment_tasks_to_tasklist(experiment_id, args.get("next_steps"))
    
    return {
        "experiment_id": experiment_id,
        "path": out_path,
        "data_dir": data_dir,
        "analysis_script": script_path if "script_path" in locals() else None
    }

def handle_update_multiblock_experiment(self, args: Dict[str, Any]):
    """
    Handle updating an existing multiblock experiment markdown file.
    
    Args should include:
        experiment_id (str): Experiment ID to update
        section (str): Section to update (metadata, sample_metadata, results, interpretation, etc.)
        content (dict or str): Content to update in the section
        next_steps (list, optional): Updated next steps list
        status (str, optional): New experiment status
    """
    experiment_id = args.get("experiment_id")
    if not experiment_id:
        self.logger.error("Missing experiment_id for update_multiblock_experiment.")
        return
    
    # Find experiment file
    exp_dir = "Experiments"
    exp_file = None
    for fname in os.listdir(exp_dir):
        if experiment_id in fname and fname.endswith(".md"):
            exp_file = os.path.join(exp_dir, fname)
            break
    
    if not exp_file or not os.path.exists(exp_file):
        self.logger.error(f"Experiment file not found for id: {experiment_id}")
        return
    
    # Read the current file content
    with open(exp_file, "r") as f:
        content = f.read()
    
    # Process updates - this is a simplified example
    # A real implementation would parse the Markdown and YAML blocks properly
    
    section = args.get("section")
    section_content = args.get("content")
    
    # Handle status updates
    if args.get("status"):
        new_status = args.get("status")
        # Update status in the YAML frontmatter
        status_pattern = r"status: .*"
        content = re.sub(status_pattern, f"status: {new_status}", content)
    
    # Handle next steps updates
    if args.get("next_steps"):
        # Locate the Next Steps section and replace it
        next_steps_pattern = r"# 5️⃣ Next Steps ✅.*?(?=# 6️⃣|$)"
        next_steps_content = "# 5️⃣ Next Steps ✅\n_Check boxes when complete. These can auto-update TASKS.md._\n\n"
        for step in args.get("next_steps"):
            checked = "x" if step.get("completed") else " "
            next_steps_content += f"- [{checked}] {step.get('description')}\n"
        content = re.sub(next_steps_pattern, next_steps_content, content, flags=re.DOTALL)
        
        # Update TASKS.md based on checked items
        self.update_tasks_from_experiment(experiment_id, args.get("next_steps"))
    
    # Handle section-specific updates
    if section and section_content:
        if section.lower() in ["metadata", "sample_metadata", "reagents"]:
            # Update YAML frontmatter blocks
            # This would require more sophisticated YAML parsing in a real implementation
            pass
        elif section.lower() in ["results", "interpretation", "discussion"]:
            # Update markdown sections
            section_pattern = rf"## {section.title()}.*?(?=##|$)"
            new_section = f"## {section.title()}\n{section_content}\n\n"
            content = re.sub(section_pattern, new_section, content, flags=re.DOTALL)
    
    # Write updated content back to file
    with open(exp_file, "w") as f:
        f.write(content)
    
    # Log the update
    self.logger.info(f"Updated multiblock experiment: {exp_file}")
    
    # Append to CHANGELOG.md
    self.append_changelog(f"Updated experiment {experiment_id}: {section if section else 'various sections'}")
    
    # If experiment is completed, verify all required fields are present
    if args.get("status") == "completed":
        self.validate_experiment_completion(experiment_id, exp_file)
    
    return {
        "experiment_id": experiment_id,
        "path": exp_file,
        "updated_section": section
    }

def validate_experiment_completion(self, experiment_id, file_path):
    """Validate that a completed experiment has all required fields."""
    with open(file_path, "r") as f:
        content = f.read()
    
    required_sections = [
        "# 3️⃣ Results & Analysis",
        "# 4️⃣ Interpretation"
    ]
    
    missing = []
    for section in required_sections:
        if section not in content or re.search(rf"{section}.*?_[^_]*_", content, re.DOTALL):
            # Section missing or only contains placeholder text
            missing.append(section.replace("#", "").strip())
    
    if missing:
        issue_title = f"Experiment {experiment_id} missing required sections"
        issue_body = f"The following required sections need to be completed: {', '.join(missing)}. Please update the experiment record."
        self.handle_open_issue({"title": issue_title, "body": issue_body})
        return False
    
    # Mark related tasks as complete in TASKS.md
    self.mark_experiment_complete_in_tasks(experiment_id)
    return True

def update_tasks_from_experiment(self, experiment_id, next_steps):
    """Update TASKS.md based on experiment next steps."""
    if not os.path.exists("TASKS.md"):
        return
    
    with open("TASKS.md", "r") as f:
        tasks_content = f.readlines()
    
    # Find experiment section in TASKS.md or create it
    exp_section_idx = -1
    for i, line in enumerate(tasks_content):
        if experiment_id in line and "##" in line:
            exp_section_idx = i
            break
    
    if exp_section_idx == -1:
        # Section not found, append at the end of Lab Tasks
        lab_tasks_idx = -1
        for i, line in enumerate(tasks_content):
            if "## Lab Tasks" in line:
                lab_tasks_idx = i
                break
        
        if lab_tasks_idx != -1:
            # Create new section
            tasks_content.insert(lab_tasks_idx + 1, f"### {experiment_id} Tasks\n")
            exp_section_idx = lab_tasks_idx + 1
        else:
            # Create Lab Tasks section and experiment section
            tasks_content.append("\n## Lab Tasks\n")
            tasks_content.append(f"### {experiment_id} Tasks\n")
            exp_section_idx = len(tasks_content) - 1
    
    # Update or add tasks under this section
    updated_tasks = []
    for step in next_steps:
        checked = "x" if step.get("completed") else " "
        updated_tasks.append(f"- [{checked}] {step.get('description')}\n")
    
    # Find the end of the section
    end_idx = len(tasks_content)
    for i in range(exp_section_idx + 1, len(tasks_content)):
        if tasks_content[i].startswith("##"):
            end_idx = i
            break
    
    # Replace the tasks in this section
    new_content = tasks_content[:exp_section_idx + 1] + updated_tasks + tasks_content[end_idx:]
    
    with open("TASKS.md", "w") as f:
        f.writelines(new_content)
    
    self.logger.info(f"Updated {experiment_id} tasks in TASKS.md")

def mark_experiment_complete_in_tasks(self, experiment_id):
    """Mark all tasks for an experiment as complete in TASKS.md when the experiment is completed."""
    if not os.path.exists("TASKS.md"):
        return
    
    with open("TASKS.md", "r") as f:
        tasks_content = f.readlines()
    
    updated = False
    in_experiment_section = False
    
    for i, line in enumerate(tasks_content):
        if experiment_id in line and "##" in line:
            in_experiment_section = True
            continue
        
        if in_experiment_section:
            if line.startswith("##"):
                # End of section
                in_experiment_section = False
            elif line.strip().startswith("- [ ]"):
                # Unchecked task in this experiment, mark as done
                tasks_content[i] = line.replace("- [ ]", "- [x]", 1)
                updated = True
    
    if updated:
        with open("TASKS.md", "w") as f:
            f.writelines(tasks_content)
        
        self.logger.info(f"Marked all tasks for {experiment_id} as complete in TASKS.md")

def add_experiment_tasks_to_tasklist(self, experiment_id, tasks):
    """Add tasks from experiment next steps to TASKS.md."""
    if not os.path.exists("TASKS.md"):
        with open("TASKS.md", "w") as f:
            f.write("# Lab Task List\n\n## Lab Tasks\n")
    
    with open("TASKS.md", "r") as f:
        content = f.read()
    
    # Check if Lab Tasks section exists
    if "## Lab Tasks" not in content:
        content += "\n## Lab Tasks\n"
    
    # Check if this experiment already has a section
    if f"### {experiment_id}" in content:
        # Will be handled by update_tasks_from_experiment
        return
    
    # Add new section for this experiment
    new_section = f"\n### {experiment_id} Tasks\n"
    for task in tasks:
        new_section += f"- [ ] {task.get('description')}\n"
    
    # Insert after Lab Tasks header
    lab_tasks_idx = content.find("## Lab Tasks")
    if lab_tasks_idx != -1:
        insert_idx = lab_tasks_idx + len("## Lab Tasks") + 1
        content = content[:insert_idx] + new_section + content[insert_idx:]
    else:
        content += new_section
    
    with open("TASKS.md", "w") as f:
        f.write(content)
    
    self.logger.info(f"Added {experiment_id} tasks to TASKS.md") 