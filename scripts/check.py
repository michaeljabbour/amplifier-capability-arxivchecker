#!/usr/bin/env python3
"""Check site links, canonical source fidelity, package contents and offline assets."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import capability
from build import reference_section, verification_date, writing_boundary


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.remote_runtime = []
        self.lang = ""
        self.h1 = 0
        self.skill = ""
        self.in_skill = False
        self.stages = []
        self.video = []
        self.video_depth = 0
        self.anchors = []
        self.tracks = []
        self.images_without_alt = []
        self.inputs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1 += 1
        if attrs.get("id") in self.ids:
            self.duplicates.append(attrs["id"])
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append(attrs[key])
                if tag in {"script", "img", "source", "track", "link"} and key != "href" or tag == "link" and attrs.get("rel") == "stylesheet":
                    if urlsplit(attrs[key]).scheme or urlsplit(attrs[key]).netloc:
                        self.remote_runtime.append(attrs[key])
        if tag == "textarea" and attrs.get("id") == "skill-text":
            self.in_skill = True
        if attrs.get("data-stage"):
            self.stages.append(attrs["data-stage"])
        if tag == "video":
            self.video.append(attrs)
            self.video_depth += 1
        if tag == "a" and attrs.get("href"):
            self.anchors.append((attrs["href"], self.video_depth > 0))
        if tag == "track":
            self.tracks.append(attrs)
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs.get("src"))
        if tag == "input":
            self.inputs.append(attrs)
    def handle_endtag(self, tag):
        if tag == "video":
            self.video_depth -= 1
        if tag == "textarea":
            self.in_skill = False
    def handle_data(self, data):
        if self.in_skill:
            self.skill += data


def check(output: Path) -> None:
    output = output.resolve()
    pages = {}
    for path in sorted(output.rglob("*.html")):
        page = Page()
        page.feed(path.read_text())
        assert not page.duplicates, f"Duplicate IDs in {path.name}: {page.duplicates}"
        assert page.lang == "en" and page.h1 == 1, f"Expected English and one h1 in {path.name}"
        assert not page.remote_runtime, f"External runtime dependency: {page.remote_runtime}"
        assert not page.images_without_alt, f"Missing image alternatives: {page.images_without_alt}"
        pages[path] = page
    assert set(pages) >= {output / "index.html", output / "guide.html"}
    links = 0
    for path, page in pages.items():
        for ref in page.links:
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc:
                assert parsed.scheme == "https", f"Unexpected external protocol {ref}"
                continue
            assert not parsed.path.startswith("/"), f"Root-relative link breaks subpath hosting: {ref}"
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            assert target.is_relative_to(output), f"Escaping link: {ref}"
            assert target.is_file(), f"Missing link in {path.name}: {ref}"
            if parsed.fragment and target.suffix == ".html":
                assert target in pages and unquote(parsed.fragment) in pages[target].ids, f"Missing anchor: {ref}"
            links += 1
    markdown_links = 0
    for path in output.rglob("*.md"):
        for ref in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", path.read_text()):
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            assert target.is_relative_to(output) and target.exists(), f"Missing Markdown target {path.relative_to(output)}: {ref}"
            markdown_links += 1
    data = capability.config()
    source = capability.file_map(data)
    guide_source = (output / "guide.html").read_text()
    assert pages[output / "guide.html"].skill == source["SKILL.md"].decode(), "Guide source differs from canonical skill"
    for identifier, filename in (("requirements-map", "references/requirements.md"), ("submission-map", "references/submission.md"), ("writing-style", "references/writing.md")):
        canonical = source[filename].decode()
        assert reference_section(identifier, filename, canonical) in guide_source, f"Rendered canonical map differs: {filename}"
        assert identifier in pages[output / "guide.html"].ids, f"Missing browser map anchor: {identifier}"
        official_links = [ref for ref in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", canonical) if urlsplit(ref).netloc == "info.arxiv.org"]
        assert official_links, f"Canonical map needs primary-source links: {filename}"
        assert all(ref in pages[output / "guide.html"].links for ref in official_links), f"Canonical map citations not linked in browser: {filename}"
    assert (output / "SKILL.md").read_bytes() == source["SKILL.md"], "Plain skill download differs"
    for name, content in source.items():
        assert (output / data["skill_path"] / name).read_bytes() == content, f"Source download differs: {name}"
    with ZipFile(output / "arxivchecker.zip") as archive:
        expected = [data["id"] + "/" + name for name in source]
        assert archive.namelist() == expected, "ZIP membership differs from installer package"
        assert archive.testzip() is None
        for name, content in source.items():
            assert archive.read(data["id"] + "/" + name) == content, f"ZIP source differs: {name}"
    digest = hashlib.sha256((output / "arxivchecker.zip").read_bytes()).hexdigest()
    assert (output / "arxivchecker.zip.sha256").read_text() == digest + "  arxivchecker.zip\n"
    workflow = json.loads(source["references/workflow.json"])
    assert pages[output / "index.html"].stages == [s["id"] for s in workflow["stages"]], "Site workflow order differs"
    for stage in workflow["stages"]:
        text = (output / "index.html").read_text()
        import html
        assert all(html.escape(str(stage[key]), quote=True) in text for key in ("title", "description", "output")), "Site workflow summary differs"
    assert len(pages[output / "index.html"].inputs) == 5, "Expected five review prompts"
    assert all("autoplay" not in v and "controls" in v for p in pages.values() for v in p.video), "Films must use explicit playback controls"
    for name in ("arxivchecker-film.mp4", "arxivchecker-film.webm", "arxivchecker-film-15s.mp4", "arxivchecker-film.vtt", "arxivchecker-film-15s.vtt", "arxivchecker-film-poster.jpg", "arxivchecker-film-transcript.txt", "arxivchecker-film-15s-transcript.txt", "arxivchecker-film-v2.mp4", "arxivchecker-film-v2.webm", "arxivchecker-film-v2-15s.mp4", "arxivchecker-film-v2.vtt", "arxivchecker-film-v2-15s.vtt", "arxivchecker-film-v2-poster.jpg", "arxivchecker-film-v2-transcript.txt", "arxivchecker-film-v2-15s-transcript.txt", "social-card.svg", "social-card.png", "favicon.svg"):
        assert (output / "assets" / name).is_file(), f"Missing asset: {name}"
    for name in ("arxivchecker-film.vtt", "arxivchecker-film-15s.vtt", "arxivchecker-film-v2.vtt", "arxivchecker-film-v2-15s.vtt"):
        assert (output / "assets" / name).read_text().startswith("WEBVTT\n"), f"Invalid caption header {name}"
    for name in ("family.css", "style.css"):
        css = (output / "assets" / name).read_text()
        assert not re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", css), "External CSS runtime asset"
    js = (output / "assets/site.js").read_text()
    assert not re.search(r"\b(?:fetch|XMLHttpRequest|WebSocket|localStorage|sessionStorage)\b", js), "Unexpected network or persistence code"
    raw = (output / "index.html").read_text()
    landing = pages[output / "index.html"]
    removed_film_links = {
        "assets/arxivchecker-film-v2-15s.mp4", "assets/arxivchecker-film-v2-transcript.txt",
        "assets/arxivchecker-film-v2-15s-transcript.txt", "assets/arxivchecker-film-v2.mp4",
        "assets/arxivchecker-film.mp4", "docs/VIDEO-UPDATE.md",
    }
    assert not any(ref in removed_film_links for ref, in_video in landing.anchors if not in_video), "Removed film links must not return as visible landing-page links"
    assert 'class="film-links"' not in raw, "Remove the auxiliary film-link row"
    assert any(t.get("kind") == "captions" and t.get("srclang") == "en" and "default" in t for t in landing.tracks), "Retain the default English caption track"
    assert "narrated explainer" in raw and "Sound on" in raw, "Player must describe the requested voiceover"
    assert not re.search(r"silent|audio-free|no narration", raw, re.I), "Stale silent-film description"
    assert "guide.html#writing-style" in pages[output / "index.html"].links, "Missing visible publishing-style guide"
    assert "https://info.arxiv.org/help/submit_latex_best_practices.html" in pages[output / "index.html"].links, "Missing official LaTeX recommendation link"
    assert writing_boundary(source["references/writing.md"].decode()) in raw, "Editorial-style boundary differs from canonical writing guide"
    assert all(label in raw for label in ("Official requirements", "LaTeX recommendations", "MJ’s publishing style")), "Publishing layers must remain distinct"
    family = json.loads((ROOT / "site/site.json").read_text())["theme"]
    family_css = (output / "assets/family.css").read_text()
    for token in ("paper", "ink", "muted", "line", "gold", "accent", "wash"):
        value = re.search(r"--" + token + r":\s*([^;]+);", family_css)
        assert value and value[1].strip() == family[token], f"Family token differs: {token}"
    assert "Skills for thoughtful work" in raw and 'class="masthead"' in raw, "Missing common family masthead"
    audio_checks = 0
    if shutil.which("ffprobe"):
        for name in ("arxivchecker-film.mp4", "arxivchecker-film.webm", "arxivchecker-film-15s.mp4", "arxivchecker-film-v2.mp4", "arxivchecker-film-v2.webm", "arxivchecker-film-v2-15s.mp4"):
            result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "json", str(output / "assets" / name)], capture_output=True, text=True, check=True, timeout=15)
            assert json.loads(result.stdout).get("streams"), f"Requested voiceover audio stream missing: {name}"
            audio_checks += 1
    for phrase in ("Fictional", "not a study result", "human review", "No arXiv endorsement", "connect-src 'none'", "default-src 'self'", "mandatory rules", "conditional requirements", "arXiv recommendations", "local profile", "does not certify arXiv acceptance", "does not by itself establish that arXiv would reject"):
        assert phrase in raw, f"Required scope label absent: {phrase}"
    assert "https://info.arxiv.org/help/policies/format_requirements.html" in pages[output / "index.html"].links, "Missing direct official-format link"
    assert "guide.html#requirements-map" in pages[output / "index.html"].links and "guide.html#submission-map" in pages[output / "index.html"].links, "Missing visible canonical-map links"
    assert "Primary-source review: " + verification_date(source["references/requirements.md"].decode()) in raw, "Site review date differs from canonical map"
    assert not re.search(r"@@[A-Z_]+@@", raw)
    source_skills = [p for p in ROOT.rglob("SKILL.md") if "_site" not in p.relative_to(ROOT).parts and ".git" not in p.relative_to(ROOT).parts]
    assert source_skills == [ROOT / data["skill_path"] / "SKILL.md"], "Keep exactly one canonical source SKILL.md"
    print(f"PASS: {len(pages)} HTML pages; {links} local links/assets/fragments; {markdown_links} Markdown destinations")
    print(f"PASS: {len(source)} portable files, exact guide source/downloads/ZIP and SHA-256")
    print("PASS: ten canonical workflow stages, offline runtime assets, accessible controls and explicit claim limits")
    print("PASS: canonical requirement/submission maps rendered in browser, primary citations linked and local-profile scope explicit")
    print("PASS: canonical publishing-style guide, three distinct publishing layers and shared family tokens/masthead")
    print(f"Voiceover audio-stream checks: {audio_checks} films inspected" if audio_checks else "Voiceover audio-stream checks: not run; ffprobe is unavailable")
    print("ZIP SHA-256: " + digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    check(args.output)
