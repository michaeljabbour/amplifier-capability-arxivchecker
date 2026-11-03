#!/usr/bin/env python3
"""Build the dependency-free ArxivChecker site and exact portable skill download."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import capability

escape = lambda value: html.escape(str(value), quote=True)


def inline(text: str, prefix: str = "") -> str:
    """A small escaped Markdown subset; author HTML is never interpreted."""
    tokens = []
    def save(value):
        tokens.append(value)
        return "\x00" + str(len(tokens) - 1) + "\x00"
    text = re.sub(r"\x60([^\x60]+)\x60", lambda m: save("<code>" + escape(m[1]) + "</code>"), text)
    def link(match):
        label, destination = match[1], match[2]
        parsed = urlsplit(destination)
        if parsed.scheme and parsed.scheme not in {"https", "http"}:
            return escape(label)
        target = destination if parsed.scheme or parsed.netloc or destination.startswith("#") else prefix + destination
        return save('<a href="' + escape(target) + '">' + escape(label) + "</a>")
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    for i, token in enumerate(tokens):
        text = text.replace("\x00" + str(i) + "\x00", token)
    return text


def markdown(text: str, prefix: str = "", shift: int = 0) -> str:
    """Render headings, paragraphs, lists, fences and tables without dependencies."""
    if text.startswith("---\n"):
        text = text.split("---\n", 2)[2]
    lines = text.splitlines()
    result = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("\x60\x60\x60"):
            code = []
            index += 1
            while index < len(lines) and not lines[index].startswith("\x60\x60\x60"):
                code.append(lines[index])
                index += 1
            result.append("<pre><code>" + escape("\n".join(code)) + "</code></pre>")
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading:
            level = min(6, len(heading[1]) + shift)
            result.append(f"<h{level}>" + inline(heading[2], prefix) + f"</h{level}>")
            index += 1
            continue
        if "|" in line and index + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|", lines[index + 1]):
            rows = [line]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(lines[index])
                index += 1
            cells = lambda row: [c.strip() for c in row.strip().strip("|").split("|")]
            result.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Reference table; scroll horizontally to read all columns"><table><thead><tr>' + "".join("<th scope=\"col\">" + inline(c, prefix) + "</th>" for c in cells(rows[0])) + "</tr></thead><tbody>" + "".join("<tr>" + "".join("<td>" + inline(c, prefix) + "</td>" for c in cells(row)) + "</tr>" for row in rows[1:]) + "</tbody></table></div>")
            continue
        listing = re.match(r"^\s*(?:([-*])|(\d+)[.)])\s+(.*)", line)
        if listing:
            ordered = listing[2] is not None
            tag = "ol" if ordered else "ul"
            items = []
            while index < len(lines):
                current = re.match(r"^\s*(?:([-*])|(\d+)[.)])\s+(.*)", lines[index])
                if not current or (current[2] is not None) != ordered:
                    break
                value = current[3]
                index += 1
                while index < len(lines) and lines[index].startswith("  ") and not re.match(r"^\s*[-*]\s", lines[index]):
                    value += " " + lines[index].strip()
                    index += 1
                items.append("<li>" + inline(value, prefix) + "</li>")
            result.append("<" + tag + ">" + "".join(items) + "</" + tag + ">")
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip() and not re.match(r"^(?:#|\x60\x60\x60|[-*]\s|\d+[.)]\s)", lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        result.append("<p>" + inline(" ".join(paragraph), prefix) + "</p>")
    return "\n".join(result)


def verification_date(requirements: str) -> str:
    """Use the date stated by the canonical verification map, never site metadata."""
    for line in requirements.splitlines():
        found = re.search(r"\b\d{4}-\d{2}-\d{2}\b", line)
        if found and re.search(r"verif|check|review", line, re.I):
            return found[0]
    raise ValueError("The canonical requirements map needs a dated verification statement")


def reference_section(identifier: str, filename: str, source: str) -> str:
    return ('<section id="' + identifier + '" class="reference-map" data-canonical-source="'
            + escape(filename) + '">' + markdown(source, "skills/arxivchecker/references/", 1) + '</section>')


def writing_boundary(writing: str) -> str:
    """Keep the public editorial-style boundary tied to the installed method."""
    match = re.search(r"It is not an arXiv template[^.]+\.", writing)
    if not match:
        raise ValueError("The writing reference needs its explicit editorial-style boundary")
    return match[0]


def guide(skill: str, reference: str, policy: str, requirements: str, submission: str, writing: str) -> str:
    body = markdown(skill, "skills/arxivchecker/", 1)
    body += "<h2>The detailed workflow</h2>" + markdown(reference, "skills/arxivchecker/references/", 2)
    body += "<h2>Policy and project preferences</h2>" + markdown(policy, "skills/arxivchecker/references/", 2)
    body += reference_section("requirements-map", "references/requirements.md", requirements)
    body += reference_section("submission-map", "references/submission.md", submission)
    body += reference_section("writing-style", "references/writing.md", writing)
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>ArxivChecker complete playbook</title><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/family.css"><link rel="stylesheet" href="assets/style.css"></head><body><a class="skip" href="#guide">Skip to the guide</a><header class="masthead"><div class="wrap"><a class="brand" href="index.html" aria-label="ArxivChecker home"><span class="brand-mark" aria-hidden="true"></span><span><b>Amplifier</b><small>Skills for thoughtful work</small></span></a><nav class="nav" aria-label="Guide navigation"><a href="index.html#install">Get the capability</a><a href="SKILL.md" download>Download source</a></nav></div></header><main class="wrap guide" id="guide"><h1>The complete playbook</h1><p class="guide-intro">Built directly from the portable skill and canonical references, including the dated requirement and submission maps. The complete ZIP also carries tools and neutral templates.</p><nav class="guide-maps" aria-label="Official guidance maps"><a href="#requirements-map">Requirement and primary-citation map</a><a href="#submission-map">Submission-policy map</a><a href="#writing-style">MJ’s publishing style</a><a href="https://info.arxiv.org/help/policies/format_requirements.html">Official arXiv format requirements</a></nav>""" + body + '<details><summary>View the exact canonical skill source</summary><label class="sr-only" for="skill-text">Canonical SKILL.md source</label><textarea id="skill-text" readonly spellcheck="false">' + escape(skill) + '</textarea></details><p><a href="index.html#install">Get the complete capability</a></p></main></body></html>'


def build(output: Path) -> None:
    output = output.resolve()
    # A builder must never erase an arbitrary directory.
    if output != ROOT / "_site":
        raise ValueError("Build output must be this checkout's _site directory")
    if output.is_symlink():
        raise ValueError("Build output must not be a symlink")
    data = capability.config()
    portable = capability.file_map(data)
    config = json.loads((ROOT / "site/site.json").read_text())
    workflow = json.loads(portable["references/workflow.json"])
    stages = workflow["stages"]
    if len(stages) != 10 or len({s["id"] for s in stages}) != 10:
        raise ValueError("Expected ten distinct canonical workflow stages")
    example = config["claim_example"]
    replacements = {
        "NAME": escape(config["name"]),
        "DESCRIPTION": escape(config["description"]),
        "VERSION": escape(config["version"]),
        "STATUS": escape(config["status"]),
        "POLICY_DATE": escape(verification_date(portable["references/requirements.md"].decode())),
        "WRITING_BOUNDARY": escape(writing_boundary(portable["references/writing.md"].decode())),
        "WORKFLOW": "".join('<li data-stage="' + escape(s["id"]) + '"><div><h3>' + escape(s["title"]) + "</h3><p>" + escape(s["description"]) + '</p><p class="stage-output">Output: ' + escape(s["output"]) + "</p></div></li>" for s in stages),
        "CLAIM_LABEL": escape(example["label"]),
        "CLAIM_BEFORE": escape(example["before"]),
        "CLAIM_AFTER": escape(example["after"]),
        "CLAIM_CHECKS": "".join("<details" + (" open" if i == 0 else "") + "><summary>" + escape(c["title"]) + "</summary><p>" + escape(c["body"]) + "</p></details>" for i, c in enumerate(example["checks"])),
    }
    page = (ROOT / "site/template.html").read_text()
    for key, value in replacements.items():
        page = page.replace("@@" + key + "@@", value)
    if re.search(r"@@[A-Z_]+@@", page):
        raise ValueError("Unresolved site placeholder")
    if output.exists():
        shutil.rmtree(output)
    assets = output / "assets"
    assets.mkdir(parents=True)
    (output / "index.html").write_text(page, encoding="utf-8")
    for name, content in portable.items():
        # Preserve relative references from both the stable root download and
        # canonical source path; a lone root SKILL.md would strand its links.
        for target in (output / name, output / data["skill_path"] / name):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    (output / "guide.html").write_text(guide(portable["SKILL.md"].decode(), portable["references/workflow.md"].decode(), portable["references/policy.md"].decode(), portable["references/requirements.md"].decode(), portable["references/submission.md"].decode(), portable["references/writing.md"].decode()), encoding="utf-8")
    for name, target in (("site/theme/style.css", "family.css"), ("site/style.css", "style.css"), ("site/site.js", "site.js"), ("site/theme/LICENSE", "family-LICENSE.txt")):
        shutil.copy2(ROOT / name, assets / target)
    for path in sorted((ROOT / "site/assets").iterdir()):
        if path.is_symlink():
            raise ValueError("Site assets must not be symlinks")
        if path.is_file():
            shutil.copy2(path, assets / path.name)
    for name in ("README.md", "LICENSE", "CHANGELOG.md", "capability.json", "project.json", "bundle.md", "site/README.md", "site/theme/LICENSE"):
        source = ROOT / name
        if source.is_file():
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    for folder in ("docs", "behaviors", "modes", "recipes"):
        for source in sorted((ROOT / folder).rglob("*")):
            if source.is_symlink():
                raise ValueError("Documentation must not contain symlinks")
            if source.is_file() and not any(part.startswith(".") or part == "__pycache__" for part in source.relative_to(ROOT).parts):
                target = output / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    (output / ".nojekyll").touch()
    result = capability.export(data, output / "arxivchecker.zip")
    (output / "arxivchecker.zip.sha256").write_text(result["sha256"] + "  arxivchecker.zip\n")
    print(f"Built {output}: {len(stages)} canonical stages; {result['files']} portable files; ZIP sha256 {result['sha256']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    build(args.output)
