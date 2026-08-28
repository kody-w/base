#!/usr/bin/env python3
"""harvest_agent_browser_data.py — Static Data Covenant harvester for
apps/ai-tools/agent-browser.html.

That page used to call, from the visitor's browser:
  https://api.github.com/repos/kody-w/Copilot-Agent-365/contents/agents?ref=main
  https://api.github.com/repos/kody-w/Copilot-Agent-365/commits?path=<file>&per_page=1

Both now read committed snapshots instead
(apps/ai-tools/data/agents-listing.json, apps/ai-tools/data/agents-commits.json).

NOTE (as of this migration): kody-w/Copilot-Agent-365 returns 404 from the
GitHub API — the source repo does not exist (renamed, deleted, or never
public). The API calls this page made were already silently dead for every
visitor before this migration. This script writes empty snapshots ([] / {})
so the page's existing empty-state UI renders instead of a network error, and
re-harvests real data automatically if the source repo ever reappears. No
scheduled workflow is wired for this one — see migration flags.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "apps" / "ai-tools" / "data"
REPO = "kody-w/Copilot-Agent-365"
AGENTS_PATH = "agents"
BRANCH = "main"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "static-data-covenant-harvester"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    listing_url = f"https://api.github.com/repos/{REPO}/contents/{AGENTS_PATH}?ref={BRANCH}"
    try:
        files = get_json(listing_url)
    except urllib.error.HTTPError as e:
        print(f"! {REPO} contents/{AGENTS_PATH} -> HTTP {e.code} (source repo likely gone); writing empty snapshots")
        files = []
    except Exception as e:
        print(f"✗ harvest failed: {e}", file=sys.stderr)
        return 1

    py_files = [f for f in files if isinstance(f, dict) and f.get("name", "").endswith(".py")]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "agents-listing.json").write_text(json.dumps(py_files, indent=1) + "\n")

    commits_by_path = {}
    for f in py_files:
        path = f["path"]
        commits_url = f"https://api.github.com/repos/{REPO}/commits?path={path}&per_page=1"
        try:
            commits_by_path[path] = get_json(commits_url)
        except Exception as e:
            print(f"! commits fetch failed for {path}: {e}")

    (OUT_DIR / "agents-commits.json").write_text(json.dumps(commits_by_path, indent=1) + "\n")
    print(f"✓ {len(py_files)} agents, {len(commits_by_path)} commit records harvested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
