# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **static HTML gallery repository** ("Vibe Coding Gallery") showcasing self-contained web applications. The repository is deployed via GitHub Pages at `https://kody-w.github.io/base/`.

Key characteristics:
- Each application is a **single, self-contained HTML file** with embedded CSS and JavaScript
- **No external dependencies** - all code is inline (no npm, no build process)
- Applications are organized by category in the `apps/` directory
- The main gallery (`index.html`) auto-discovers and displays all apps using the GitHub API

## Repository Structure

```
/
├── index.html              # Main gallery page with animated UI
├── apps/                   # Categorized applications
│   ├── ai-tools/          # AI and ML tools
│   ├── games/             # Interactive games
│   ├── development/       # Developer tools
│   ├── productivity/      # Productivity apps
│   ├── business/          # Business applications
│   ├── media/             # Media and audio/video tools
│   ├── utilities/         # Utility applications
│   └── health/            # Health and wellness apps
├── data/                  # Configuration and data files
├── assets/                # Shared assets (minimal)
└── docs/                  # Documentation
```

## Self-Contained HTML Architecture

**Critical Pattern:** Every application must be a single HTML file containing:
1. All HTML structure in `<body>`
2. All CSS in `<style>` tags in `<head>`
3. All JavaScript in `<script>` tags before `</body>`
4. No external CSS or JS file references
5. No npm dependencies or build steps

Example structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Name</title>
    <style>
        /* All CSS here */
    </style>
</head>
<body>
    <!-- All HTML here -->

    <script>
        // All JavaScript here
    </script>
</body>
</html>
```

## Gallery System

The `index.html` gallery page:
- Auto-discovers HTML files via GitHub API
- Categorizes apps based on their `apps/` subdirectory
- Generates metadata (title, description, icon) from filenames
- Supports pinning, voting, and search features
- Includes a 3D gallery mode using Three.js (loaded via CDN)

File discovery pattern:
```javascript
// Files are found at: apps/{category}/{filename}.html
// Title is generated from filename: "my-cool-app.html" → "My Cool App"
// Icon is assigned deterministically based on filename hash
```

## GitHub Pages Deployment

The repository uses GitHub Pages with:
- `.nojekyll` file to bypass Jekyll processing
- `robots.txt` for SEO
- Direct file serving from `main` branch root
- No build or deployment process required

URL patterns:
- Local: `file:///path/to/app.html`
- Production: `https://kody-w.github.io/base/apps/category/app.html`

## File Organization Script

The `update-existing-repo.sh` script:
- Creates the standard directory structure
- Sets up `.nojekyll` and `.gitignore`
- Provides guidance for organizing existing HTML files
- No automation of file moves (manual categorization required)

## Development Workflow

When adding new applications:

1. **Create a self-contained HTML file** in the appropriate `apps/` subdirectory
2. **Follow naming conventions**: Use kebab-case (e.g., `task-manager.html`)
3. **Embed everything**: All styles, scripts, and assets inline
4. **Test locally**: Open the HTML file directly in a browser
5. **Commit and push**: The gallery will auto-discover the new app

When handling external libraries:
- Prefer vanilla JavaScript when possible
- If a library is needed, use CDN links (e.g., Three.js from cdnjs)
- Keep external dependencies to an absolute minimum

## Gallery Index Behavior

The main `index.html`:
- Detects local vs production environment
- Uses GitHub API for file discovery
- Falls back to local config if running locally
- Supports search/filter across all apps
- Maintains pinned tools and voting in localStorage
- Provides both 2D grid and 3D gallery views

## Key Technical Decisions

1. **No build process** - Enables instant deployment and maximum simplicity
2. **Self-contained files** - Each app is portable and independent
3. **GitHub API discovery** - No manual manifest maintenance required
4. **Category-based organization** - Clear structure for growing collection
5. **Local storage for state** - Pins, votes, and preferences stored client-side

## Common Tasks

**Add a new application:**
```bash
# Create the file in the appropriate category
touch apps/games/new-game.html
# Edit the file with self-contained HTML/CSS/JS
# Commit and push - the gallery will auto-discover it
```

**Reorganize files:**
```bash
# Move files between categories
mv apps/utilities/tool.html apps/productivity/tool.html
# The gallery will automatically recategorize it
```

**Update the gallery UI:**
```bash
# Edit index.html directly
# All gallery logic is in the embedded <script> tag
```

## Personal Project Context

This is Kody Wildfeuer's personal creative coding playground. Content represents personal experiments and creative explorations, not associated with any employer. The gallery includes a disclaimer to this effect.
