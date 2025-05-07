#!/usr/bin/env python3
"""
Initialize VS Code extensions and set up lab environment.
Run this with 'python -m Agent.init_extensions' or 'lab init-extensions'.
"""

import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("lab-init")

def run_command(cmd, desc=None):
    """Run a shell command and log the result"""
    if desc:
        logger.info(f"Running: {desc}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        if desc:
            logger.info(f"✓ {desc} completed successfully")
        return True
    else:
        if desc:
            logger.error(f"✗ {desc} failed: {result.stderr}")
        return False

def setup_extensions():
    """Set up VS Code extensions and GitHub CLI"""
    # Verify GitHub CLI is installed
    if run_command("gh --version", "Checking GitHub CLI"):
        logger.info("GitHub CLI is available")
    else:
        logger.error("GitHub CLI is not installed or not in PATH")
        return False
    
    # Verify GitHub authentication
    if run_command("gh auth status", "Checking GitHub authentication"):
        logger.info("GitHub CLI is authenticated")
    else:
        logger.warning("GitHub CLI is not authenticated - Some features may not work")
        logger.info("Use 'gh auth login' to authenticate")
    
    # Check if GitHub Issues extension is active
    if os.path.exists(os.path.expanduser("~/.vscode-server/extensions/github.vscode-pull-request-github-*")):
        logger.info("GitHub Pull Requests and Issues extension is installed")
    else:
        logger.warning("GitHub Pull Requests and Issues extension may not be installed")
        logger.info("Please check VS Code extensions")
    
    # Create SESSION_LOG.md if it doesn't exist
    if not os.path.exists("SESSION_LOG.md"):
        with open("SESSION_LOG.md", "w") as f:
            f.write("# Lab Session Log\n\n")
            f.write("This file tracks lab activities and completed experiments.\n\n")
        logger.info("Created SESSION_LOG.md")
    
    # Create Experiments directory if it doesn't exist
    os.makedirs("Experiments", exist_ok=True)
    logger.info("Verified Experiments directory exists")
    
    # Create Data directory if it doesn't exist  
    os.makedirs("Data", exist_ok=True)
    logger.info("Verified Data directory exists")
    
    return True

def main():
    """Main entry point"""
    logger.info("Initializing LabAgent environment...")
    if setup_extensions():
        logger.info("✅ LabAgent environment initialized")
        print("\nLabAgent is ready to use! Try asking:")
        print("  - Create a new siRNA screen experiment")
        print("  - Record data for experiment EXP-XXXXXX")
        print("  - What experiments are in progress?")
    else:
        logger.error("❌ Failed to initialize LabAgent environment")

if __name__ == "__main__":
    main() 