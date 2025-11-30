#!/bin/bash
set -e

cd /Users/adilmubeen/Documents/test

echo "================================================"
echo "Cleaning and Pushing to GitHub"
echo "================================================"

# Initialize git if not already done
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Add remote if not exists
if ! git remote | grep -q "origin"; then
    echo "Adding remote origin..."
    git remote add origin https://github.com/AdilMubeen/deepResearchAI.git
fi

# Stage all files
echo "Staging files..."
git add .

# Commit
echo "Committing changes..."
git commit -m "Initial commit: Deep Research AI Agent with multi-LLM orchestration

- Multi-LLM agent using GPT-4, Claude, Gemini, and Perplexity
- LangGraph workflow for iterative research
- Flask web interface with tabbed navigation
- Pre-generated reports for Elizabeth Holmes, Sam Bankman-Fried, Martin Shkreli
- PDF download functionality
- Risk scoring across 6 categories
- Entity extraction and timeline analysis" || echo "No changes to commit"

# Set branch to main
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main --force

echo ""
echo "================================================"
echo "✅ Code pushed to GitHub successfully!"
echo "================================================"
echo ""
echo "Repository: https://github.com/AdilMubeen/deepResearchAI"
echo ""

