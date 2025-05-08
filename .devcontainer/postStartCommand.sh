#!/bin/bash
# This script runs after the container is started but before the user gets access to it

echo "🚀 Running Lab Agent post-start setup..."

# Ensure Python dependencies are installed
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set up GitHub CLI if available
SETUP_NEEDED=false
if command -v gh &> /dev/null; then
    echo "🔧 GitHub CLI found, checking authentication..."
    # This won't authenticate, but will show status and prompt user if needed
    gh auth status || echo "⚠️  GitHub CLI needs authentication. Run 'gh auth login' to set up."
else
    echo "⚠️  GitHub CLI not found. Some features may not work properly."
    SETUP_NEEDED=true
fi

# Ensure directories exist
mkdir -p Data/chroma_index

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable not set. Smart-Fill will not work."
    echo "    Set it in your Codespace secrets or run 'export OPENAI_API_KEY=your-key'."
    SETUP_NEEDED=true
fi

# Check Jupyter installation and dashboard dependencies
echo "🔬 Setting up Jupyter environment and Protocol Dashboard..."
pip install -q jupyter notebook jupyterlab pandas matplotlib plotly pyyaml ipywidgets

# Create the welcome message for Jupyter
mkdir -p /workspaces/docs/Analysis
cat > /workspaces/docs/README.ipynb << EOL
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🧪 Welcome to the Lab Documentation System! 🧬\\n\\n",
    "## Quick Start\\n\\n",
    "This system provides interactive protocol dashboards to help manage your lab protocols.\\n\\n",
    "### Available Dashboards:\\n\\n",
    "- [**Protocol Dashboard**](/workspaces/docs/Analysis/protocol_dashboard.ipynb) - Browse and filter all protocols\\n\\n",
    "Click on any of the links above to get started!\\n\\n",
    "*No installation required - everything is pre-configured for you.*"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOL

# Create an empty .env file if it doesn't exist
if [ ! -f /workspaces/docs/.env ]; then
  echo "# Auto-generated .env file" > /workspaces/docs/.env
  echo "Creating empty .env file because none was found."
fi

# Display welcome message
echo ""
echo "🧪 LAB AGENT ENVIRONMENT READY 🧪"
echo "Start using the lab agent by typing in the VS Code Chat window."
echo "For a health check, run: python Agent/test_environment.py"
echo "To view the Protocol Dashboard, open Analysis/protocol_dashboard.ipynb"

# Point to setup guide if needed
if [ "$SETUP_NEEDED" = true ]; then
    echo ""
    echo "⚠️ Environment issues detected. Please see ENVIRONMENT_SETUP.md for instructions"
    echo "   on how to properly configure your environment."
fi
echo ""

# Exit with success
exit 0