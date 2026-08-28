#!/usr/bin/env python3
"""harvest_tree.py — Static Data Covenant harvester for the app gallery.

index.html used to make an unauthenticated call to
  https://api.github.com/repos/kody-w/base/git/trees/main?recursive=1
from the visitor's browser to discover which HTML apps exist. That call now
reads a committed snapshot (data/api/tree.json) instead; this script is what
regenerates that snapshot. Run it in CI (or by hand) whenever the tree
changes.

Writes data/api/tree.json in the exact shape of the GitHub "get a tree"
API response ({sha, url, tree: [...], truncated}) so index.html's parsing
code did not need to change beyond the fetch URL.
"""

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "api" / "tree.json"
API_URL = "https://api.github.com/repos/kody-w/base/git/trees/main?recursive=1"


def main():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "static-data-covenant-harvester"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"✗ harvest failed: {e}", file=sys.stderr)
        return 1

    if data.get("truncated"):
        print("✗ GitHub API reported a truncated tree — snapshot would be incomplete, refusing to write", file=sys.stderr)
        return 2

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(f"✓ {OUT.relative_to(ROOT)} — {len(data.get('tree', []))} tree entries harvested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
