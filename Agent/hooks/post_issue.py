import sys
from pathlib import Path
from datetime import datetime

# Usage: python post_issue.py <issue_number> <issue_title> <issue_url>
if len(sys.argv) != 4:
    print("Usage: python post_issue.py <issue_number> <issue_title> <issue_url>")
    sys.exit(1)

issue_number = sys.argv[1]
issue_title = sys.argv[2]
issue_url = sys.argv[3]

entry = f"- [ ] [#{issue_number}]({issue_url}) {issue_title}  _(added {datetime.now().strftime('%Y-%m-%d %H:%M')})_\n"

# Append to TASKS.md
Path("TASKS.md").write_text(
    Path("TASKS.md").read_text() + entry if Path("TASKS.md").exists() else entry
)

# Append to ISSUES_LOG.md
Path("ISSUES_LOG.md").write_text(
    Path("ISSUES_LOG.md").read_text() + entry if Path("ISSUES_LOG.md").exists() else entry
) 