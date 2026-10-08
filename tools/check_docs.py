#!/usr/bin/env python3
"""Check local Markdown links and required documentation entry points."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
failures = []
documents = [p for p in ROOT.rglob("*.md") if not any(x in p.parts for x in [".venv",".git"])]
for path in documents:
    for target in re.findall(r"\]\(([^)]+)\)",path.read_text()):
        target = target.split()[0].strip("<>").split("#")[0]
        if not target or re.match(r"[a-z][a-z0-9+.-]*:",target): continue
        if not (path.parent/unquote(target)).exists():
            failures.append(f"{path.relative_to(ROOT)}: missing link target {target}")
for required in ["README.md","LICENSE","CONTRIBUTING.md","docs/README.md","examples/README.md","schemas/v0/README.md"]:
    if not (ROOT/required).is_file(): failures.append(f"Missing required project document: {required}")
for failure in failures: print(failure,file=sys.stderr)
print(f"Checked {len(documents)} Markdown documents; {len(failures)} failures")
sys.exit(bool(failures))
