#!/usr/bin/env python3
"""
Test script to verify environment setup for Lab Agent.
Run this in your Codespace to diagnose issues.
"""
import os
import sys
import importlib
import subprocess

def check_dependency(module_name):
    """Check if a Python module is installed and can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def check_command(command):
    """Check if a shell command exists and can be executed."""
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔍 Lab Agent Environment Test")
    print("-----------------------------")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check required modules
    print("\n📦 Checking Python dependencies:")
    dependencies = [
        "openai", "yaml", "chromadb", "git", "Bio", "requests", 
        "langchain", "faiss", "json"
    ]
    
    for dep in dependencies:
        status = "✅" if check_dependency(dep) else "❌"
        print(f"{status} {dep}")
    
    # Check environment variables
    print("\n🔑 Checking environment variables:")
    env_vars = ["OPENAI_API_KEY", "GITHUB_TOKEN"]
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Hide actual key values
            display = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "****"
            print(f"✅ {var} = {display}")
        else:
            print(f"❌ {var} is not set")
    
    # Check file structure
    print("\n📁 Checking repository structure:")
    directories = ["Agent", "Protocols", "Experiments", "Data", "Templates"]
    for directory in directories:
        if os.path.isdir(directory):
            print(f"✅ {directory}/ exists")
        else:
            print(f"❌ {directory}/ is missing")
    
    # Check GitHub CLI
    print("\n🔧 Checking GitHub CLI:")
    if check_command("gh --version"):
        print("✅ GitHub CLI is installed")
        
        # Check if authenticated
        if check_command("gh auth status"):
            print("✅ GitHub CLI is authenticated")
        else:
            print("❌ GitHub CLI is not authenticated")
    else:
        print("❌ GitHub CLI is not installed")
    
    print("\n-----------------------------")
    print("If you see any ❌ errors above, they need to be fixed before the Lab Agent will work properly.")
    print("For GitHub authentication in Codespaces, try running 'gh auth status' and follow any prompts.")

if __name__ == "__main__":
    main() 