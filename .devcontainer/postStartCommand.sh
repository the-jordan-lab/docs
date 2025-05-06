#!/bin/bash
# This script runs after the container is started but before the user gets access to it

echo "🚀 Running Lab Agent post-start setup..."

# Ensure Python dependencies are installed
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set up GitHub CLI if available
if command -v gh &> /dev/null; then
    echo "🔧 GitHub CLI found, checking authentication..."
    # This won't authenticate, but will show status and prompt user if needed
    gh auth status || echo "⚠️  GitHub CLI needs authentication. Run 'gh auth login' to set up."
else
    echo "⚠️  GitHub CLI not found. Some features may not work properly."
fi

# Ensure directories exist
mkdir -p Data/chroma_index

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable not set. Smart-Fill will not work."
    echo "    Set it in your Codespace secrets or run 'export OPENAI_API_KEY=your-key'."
fi

# Display welcome message
echo ""
echo "🧪 LAB AGENT ENVIRONMENT READY 🧪"
echo "Start using the lab agent by typing in the VS Code Chat window."
echo "For a health check, run: python Agent/test_environment.py"
echo ""

# Exit with success
exit 0 