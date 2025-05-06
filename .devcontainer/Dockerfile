FROM mcr.microsoft.com/devcontainers/python:3.10

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /workspaces/lab-docs

# (Optional) Install additional tools or dependencies here 