#!/bin/bash

# Windsurf extension authentication setup script
# This script securely sets up the authentication for the Windsurf extension
# without exposing credentials in plaintext

echo "🌊 Setting up Windsurf authentication..."

# Create the windsurf config directory if it doesn't exist
mkdir -p ~/.windsurf

# Write the authentication config
cat > ~/.windsurf/auth.json << EOL
{
  "authToken": "$WINDSURF_AUTH_TOKEN",
  "configTimestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "lastLogin": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOL

# Set correct permissions
chmod 600 ~/.windsurf/auth.json

echo "✅ Windsurf authentication setup complete"