# Environment Setup Guide

This guide helps you set up your development environment correctly to avoid warnings about missing GitHub CLI and OpenAI API keys.

## GitHub CLI

GitHub CLI has been added to the Dockerfile and will be automatically installed when your container is built. If you're seeing warnings about GitHub CLI missing, you may need to:

1. Rebuild your container by running the command in VS Code:
   - Press `F1` and search for "Rebuild Container"
   - Or select "Dev Containers: Rebuild Container" from the command palette

2. After rebuilding, authenticate with GitHub:
   ```bash
   gh auth login
   ```

## OpenAI API Key

To permanently set up your OpenAI API key (required for Smart-Fill functionality):

### Option 1: GitHub Codespace Secrets (Recommended)

1. Go to [GitHub Codespace Secrets](https://github.com/settings/codespaces)
2. Click on "New secret"
3. Name: `OPENAI_API_KEY`
4. Value: Your OpenAI API key
5. Select the repositories where this secret should be available
6. Click "Add secret"
7. Rebuild your codespace for the changes to take effect

### Option 2: Environment Variable in .bashrc

Add the following to your `.bashrc` file in the container:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Option 3: Local .env File

1. Uncomment the `runArgs` section in the `.devcontainer/devcontainer.json` file
2. Create a `.env` file in the root of your repository with:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```
3. Add `.env` to your `.gitignore` to prevent accidentally committing your API key
4. Rebuild your container

## Environment Variables

### Setting up .env file

The development environment requires a `.env` file in the root directory of the repository. This file is not included in Git (it's gitignored) because it may contain sensitive information.

**Before starting a codespace:**

1. Create a `.env` file in the root directory
2. The file can be empty if you don't need any environment variables
3. If you need to use OpenAI API features, add your key like this:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

**Note:** Without a `.env` file (even an empty one), the codespace environment will fail to start.

## Verifying Your Setup

After completing these steps, you can verify your setup by running:

```bash
# Check GitHub CLI
gh --version

# Verify OpenAI API key is set
echo $OPENAI_API_KEY | grep -o "sk-..."
```

If properly configured, you should no longer see warnings about missing GitHub CLI or OpenAI API key when starting your environment. 