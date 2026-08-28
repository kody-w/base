#!/usr/bin/env python3
"""harvest_deployment_agents.py — Static Data Covenant harvester for
apps/ai-tools/agent-deployment-prototype.html.

That page used to call, from the visitor's browser:
  https://api.github.com/repos/kody-w/AI-Agent-Library/contents/agents

It now reads a committed snapshot instead
(apps/ai-tools/data/deployment-agents-listing.json).

NOTE (as of this migration): kody-w/AI-Agent-Library returns 404 from the
GitHub API — the source repo does not exist. The page already has a
mock-data fallback for a non-ok/empty response, so an empty snapshot renders
the same mock-data experience visitors already got. No scheduled workflow is
wired for this one — see migration flags.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "apps" / "ai-tools" / "data" / "deployment-agents-listing.json"
REPO = "kody-w/AI-Agent-Library"


def main():
    url = f"https://api.github.com/repos/{REPO}/contents/agents"
    req = urllib.request.Request(url, headers={"User-Agent": "static-data-covenant-harvester"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            files = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"! {REPO} contents/agents -> HTTP {e.code} (source repo likely gone); writing empty snapshot")
        files = []
    except Exception as e:
        print(f"✗ harvest failed: {e}", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(files, indent=1) + "\n")
    print(f"✓ {OUT.relative_to(ROOT)} — {len(files)} entries harvested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
