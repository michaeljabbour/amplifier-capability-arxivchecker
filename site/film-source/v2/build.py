#!/usr/bin/env python3
"""Build web/index.html from the source page, the audit hook and edit/edit.json."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
src = (ROOT / 'web/index.src.html').read_text()
hook = (ROOT / 'tools/audit-hook.js').read_text()
edit = json.loads((ROOT / 'edit/edit.json').read_text())
page = src.replace('/*AUDIT_HOOK*/', hook).replace('/*EDIT*/null', json.dumps(edit))
(ROOT / 'web/index.html').write_text(page)
print('built web/index.html')
