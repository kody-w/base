#!/bin/bash

# Update Existing Repository Script for kody-w/base
# Run this in the root of your existing base repository

echo "================================================"
echo "Updating kody-w/base for GitHub Pages"
echo "================================================"
echo ""

# Ensure we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository. Please run this from your base repo root."
    exit 1
fi

echo "Current directory: $(pwd)"
read -p "Is this your base repository? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "Exiting. Please run from your base repository root."
    exit 1
fi

# Create directory structure if it doesn't exist
echo "Creating/updating directory structure..."

mkdir -p apps/games
mkdir -p apps/productivity
mkdir -p apps/business
mkdir -p apps/development
mkdir -p apps/media
mkdir -p apps/education
mkdir -p apps/ai-tools
mkdir -p apps/health
mkdir -p apps/utilities
mkdir -p data/config
mkdir -p data/games
mkdir -p assets/css
mkdir -p assets/js
mkdir -p assets/images
mkdir -p docs/api
mkdir -p docs/guides
mkdir -p archive

# Create .nojekyll if it doesn't exist (required for GitHub Pages)
if [ ! -f ".nojekyll" ]; then
    echo "Creating .nojekyll file..."
    touch .nojekyll
fi

# Check if we need to move existing HTML files
echo ""
echo "Checking for existing HTML files to organize..."

# Count HTML files in root (excluding index.html)
HTML_COUNT=$(find . -maxdepth 1 -name "*.html" ! -name "index.html" ! -name "404.html" -type f | wc -l)

if [ $HTML_COUNT -gt 0 ]; then
    echo "Found $HTML_COUNT HTML files in root directory."
    echo ""
    echo "Please move these files to appropriate category folders:"
    echo "  - Games → apps/games/"
    echo "  - Productivity tools → apps/productivity/"
    echo "  - Development tools → apps/development/"
    echo "  - etc."
    echo ""
    echo "Example commands:"
    echo "  mv gameboy-emulator.html apps/games/"
    echo "  mv task-manager.html apps/productivity/"
    echo ""
fi

# Update or create robots.txt
echo "Updating robots.txt..."
cat > robots.txt << 'EOF'
User-agent: *
Allow: /
Sitemap: https://kody-w.github.io/base/sitemap.xml
EOF

# Create or update .gitignore
echo "Updating .gitignore..."
cat > .gitignore << 'EOF'
# OS files
.DS_Store
Thumbs.db
desktop.ini

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~
*.sublime-*

# Logs
*.log
npm-debug.log*

# Dependencies (if any)
node_modules/
bower_components/

# Build output
dist/
build/
*.min.js
*.min.css

# Environment files
.env
.env.local
.env.*.local

# Temporary files
*.tmp
*.temp
.tmp/
.temp/

# Cache
.cache/
*.cache

# Local data (don't commit user data)
data/local/
*.local.json
EOF

echo ""
echo "================================================"
echo "Setup complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Move your existing HTML files to appropriate category folders"
echo ""
echo "2. Run the create-pages script to generate index pages:"
echo "   ./create-index-pages.sh"
echo ""
echo "3. Commit and push changes:"
echo "   git add ."
echo "   git commit -m 'Reorganize for GitHub Pages structure'"
echo "   git push origin main"
echo ""
echo "4. Enable GitHub Pages (if not already enabled):"
echo "   - Go to Settings → Pages"
echo "   - Source: Deploy from branch"
echo "   - Branch: main"
echo "   - Folder: / (root)"
echo ""
echo "Your site will be available at:"
echo "https://kody-w.github.io/base/"
echo ""
