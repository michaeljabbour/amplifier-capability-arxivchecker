#!/usr/bin/env python3
"""Evidence extraction and conservative local LaTeX checks; Python standard library only.

This is not an arXiv acceptance or scientific-validity checker. Compile trusted TeX only.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath

SAFE = re.compile(r"^[A-Za-z0-9_+=,./-]+$")
IGNORED = {".git", ".venv", "venv", "node_modules", "__pycache__", ".DS_Store"}
FORBIDDEN = {".env", "credentials", "id_rsa", "id_ed25519"}


def fail(message):
    raise ValueError(message)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            fail(f"duplicate JSON key: {k}")
        result[k] = v
    return result


def read_json(path):
    return parse_json(path.read_bytes())


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_pairs,
                      parse_constant=lambda x: fail(f"nonfinite JSON value: {x}"))


def root_dir(value):
    root = Path(value).absolute()
    if root.is_symlink() or not root.is_dir():
        fail(f"study must be an existing nonsymlink directory: {root}")
    return root.resolve()


def local_file(root, value, safe=False):
    if not isinstance(value, str) or not value or "\\" in value:
        fail(f"invalid relative path: {value!r}")
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in {"", ".", ".."} for x in value.split("/")):
        fail(f"path must stay inside study: {value}")
    if any(x.startswith(".") or x in IGNORED or x in FORBIDDEN for x in p.parts):
        fail(f"hidden, cache or credential path excluded: {value}")
    if safe and not SAFE.fullmatch(value):
        fail(f"filename outside this local portable profile: {value}")
    result = root
    for part in p.parts:
        result /= part
        if result.is_symlink():
            fail(f"symlinks are excluded: {value}")
    if not result.is_file() or not result.resolve().is_relative_to(root):
        fail(f"missing local file: {value}")
    return result


def write_json(value, output=None):
    text = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if output:
        with Path(output).open("x", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text, end="")


def pointer(data, address):
    if not isinstance(address, str) or (address and not address.startswith("/")):
        fail(f"invalid JSON pointer: {address!r}")
    value = data
    if address == "":
        return value
    for raw in address[1:].split("/"):
        if re.search(r"~(?![01])", raw):
            fail(f"invalid JSON pointer escape: {address}")
        key = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", key):
                fail(f"invalid list index at {address}")
            try:
                value = value[int(key)]
            except IndexError:
                fail(f"missing data at {address}")
        elif isinstance(value, dict) and key in value:
            value = value[key]
        else:
            fail(f"missing data at {address}")
    return value


def number(value, label):
    try:
        valid = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        fail(f"{label} must be a finite number")
    return value


def extract(root, spec):
    if not isinstance(spec, dict) or spec.get("schema_version") != 1:
        fail("extraction spec requires schema_version: 1")
    metrics = spec.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        fail("spec requires a nonempty metrics list")
    seen, result, cache = set(), [], {}
    for m in metrics:
        if not isinstance(m, dict):
            fail("each metric must be an object")
        mid = m.get("id")
        if not isinstance(mid, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", mid) or mid in seen:
            fail(f"invalid or duplicate metric id: {mid!r}")
        seen.add(mid)
        source = m.get("source")
        f = local_file(root, source)
        if source not in cache:
            content = f.read_bytes()
            cache[source] = (parse_json(content), hashlib.sha256(content).hexdigest())
        data, digest = cache[source]
        unit, kind = m.get("unit"), m.get("kind")
        if not isinstance(unit, str) or not unit.strip():
            fail(f"{mid}: explicit unit required")
        if kind not in {"number", "proportion"}:
            fail(f"{mid}: kind must be number or proportion")
        value = number(pointer(data, m.get("pointer")), mid)
        item = {"id": mid, "kind": kind, "source": source, "source_sha256": digest,
                "pointer": m["pointer"], "unit": unit, "value": value}
        if "cost_scope" in m:
            if not isinstance(m["cost_scope"], str) or not m["cost_scope"].strip():
                fail(f"{mid}: cost_scope must describe inclusions/exclusions")
            item["cost_scope"] = m["cost_scope"]
        if kind == "proportion":
            address = m.get("denominator_pointer")
            denominator = number(pointer(data, address), f"{mid} denominator")
            if (not isinstance(value, int) or not isinstance(denominator, int)
                    or denominator <= 0 or not 0 <= value <= denominator):
                fail(f"{mid}: binomial counts must be integers, 0 <= numerator <= denominator, n > 0")
            if denominator > 2 ** 53:
                fail(f"{mid}: counts exceed this helper's exact floating-point integer range (2**53)")
            p, z = value / denominator, 1.959963984540054
            scale = 1 + z * z / denominator
            centre = (p + z * z / (2 * denominator)) / scale
            half = z * math.sqrt(p * (1 - p) / denominator + z * z / (4 * denominator**2)) / scale
            item.update(denominator=denominator, denominator_pointer=address, rate=p,
                        wilson95=[max(0, centre - half), min(1, centre + half)])
        result.append(item)
    return {"schema_version": 1, "metrics": result,
            "limits": "Pointer extraction and binomial intervals only. Cohort choice, independence, units and cost scope need human review."}


def inventory(root):
    files, excluded = [], []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(x.startswith(".") or x in IGNORED or x in FORBIDDEN for x in rel.parts):
            continue
        if p.is_symlink():
            excluded.append({"path": rel.as_posix(), "reason": "symlink"})
        elif p.is_file():
            files.append({"path": rel.as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)})
    return {"schema_version": 1, "files": files, "excluded": excluded,
            "limits": "File inventory only; hidden files, credentials and caches excluded. No contents or scientific claims evaluated."}


def load_manifest(root, manifest):
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        fail("manifest requires schema_version: 1")
    if not isinstance(manifest.get("engine"), str) or not manifest["engine"].strip():
        fail("local manifest must record the chosen engine; this does not establish arXiv support")
    files = manifest.get("files")
    if not isinstance(files, list) or not files or len(files) > 1000:
        fail("files must be an explicit nonempty allowlist of at most 1000 files")
    paths = {}
    total = 0
    for name in files:
        p = local_file(root, name, safe=True)
        if name in paths:
            fail(f"duplicate manifest path: {name}")
        total += p.stat().st_size
        paths[name] = p
    if total > 100 * 1024 * 1024:
        fail("local package limit is 100 MiB; review asset sizes")
    main = manifest.get("main_tex")
    if main not in paths or not main.endswith(".tex"):
        fail("main_tex must name an allowlisted .tex file")
    generated = {".aux", ".log", ".fls", ".toc", ".out", ".fdb_latexmk", ".synctex", ".ps", ".dvi", ".pdf", ".lot", ".lof"}
    generated_names = set()
    for name in paths:
        if name.endswith(".tex"):
            for ext in generated:
                generated_names.add(str(PurePosixPath(name).with_suffix(ext)))
    # This runner writes the top-level job's outputs into compile cwd even for nested main source.
    generated_names.update(Path(main).stem + ext for ext in generated)
    for name in paths:
        if name in generated_names:
            fail(f"generated build artifact excluded from source allowlist: {name}")
    authors = manifest.get("authors")
    if not isinstance(authors, list) or not authors:
        fail("local manifest must record author-provided names")
    for a in authors:
        if not isinstance(a, dict) or not isinstance(a.get("name"), str) or not a["name"].strip():
            fail("each local author record needs an author-provided name")
        if "affiliation" in a and not isinstance(a["affiliation"], str):
            fail("affiliation, when provided, must be a string; never invent one")
    reviews = manifest.get("human_review")
    if not isinstance(reviews, list) or not reviews or any(not isinstance(x, str) or not x.strip() for x in reviews):
        fail("human_review must list the remaining human decisions")
    return paths


def uncomment(tex):
    return re.sub(r"(?<!\\)%[^\n]*", "", tex)


def check(root, manifest):
    import posixpath
    paths = load_manifest(root, manifest)
    errors, warnings = [], []
    bbl = Path(manifest["main_tex"]).stem + ".bbl"
    for name, p in paths.items():
        if p.suffix != ".tex":
            continue
        text = uncomment(p.read_text(encoding="utf-8"))
        if re.search(r"\\(?:write18|immediate\s*\\write18)\b|\\(?:input|include)(?![A-Za-z])\s*[^{\s]", text):
            warnings.append(f"{name}: shell command or nonliteral input needs manual review; local preflight disables shell escape")
        if re.search(r"(?:REPLACE_ME|AUTHOR_NAME|STUDY_TITLE)", text):
            errors.append(f"{name}: explicit local template placeholders remain; this is not an arXiv policy verdict")
        if re.search(r"\b(?:TODO|FIXME)\b", text):
            warnings.append(f"{name}: possible editing marker; review context rather than treating prose as ineligible")
        custom_graphics = bool(re.search(r"\\(?:graphicspath|DeclareGraphicsExtensions)\b", text))
        for kind, value in re.findall(r"\\(input|include|includegraphics|bibliography|addbibresource)\*?(?:\[[^\]]*\])?\s*\{([^}]+)\}", text):
            for ref in value.split(",") if kind == "bibliography" else [value]:
                ref = ref.strip()
                if "\\" in ref or "#" in ref:
                    warnings.append(f"{name}: dynamic dependency needs manual allowlist review: {ref}")
                    continue
                if kind in {"bibliography", "addbibresource"} and bbl in paths:
                    continue  # An uploaded compatible .bbl can replace the .bib source.
                ref = posixpath.normpath(ref)
                extensions = {"input": ["", ".tex"], "include": ["", ".tex"],
                              "includegraphics": ["", ".pdf", ".png", ".jpg", ".jpeg", ".eps", ".ps"],
                              "bibliography": ["", ".bib"], "addbibresource": [""]}[kind]
                # TeX normally resolves relative to compile cwd, not the included file.
                if not any(ref + ext in paths for ext in extensions):
                    if kind == "includegraphics" and custom_graphics:
                        warnings.append(f"{name}: graphics search paths/extensions need manual resolution: {ref}")
                    else:
                        errors.append(f"{name}: literal dependency missing from local allowlist: {ref}; review TeX search paths before changing source")
        if re.search(r"\\(?:graphicspath|usepackage|bibliographystyle)\b", text):
            warnings.append(f"{name}: static scan cannot resolve all class/package/macro dependencies; inspect clean-build recorder")
        if re.search(r"\\(?:bibliography|addbibresource)(?![A-Za-z])", text) and bbl not in paths:
            warnings.append(f"{name}: .bib processing is valid on arXiv; this local no-bibliography-engine preflight needs a prepared {bbl} or a separately tested bibliography workflow")
    if manifest["engine"] != "pdflatex":
        warnings.append("Chosen engine is outside this helper's pdflatex preflight profile; use and test its supported arXiv route separately")
    warnings.extend(["Author spelling/affiliations, reference metadata and claim accuracy require human verification.",
                     "No figure or page has been visually inspected by this checker.",
                     "This local policy does not certify current arXiv acceptance or licensing."])
    return {"schema_version": 1, "status": "fail" if errors else "static-checks-pass",
            "scope": "Local manifest safety and limited static heuristics. Findings are not arXiv eligibility decisions. See references/requirements.md and references/submission.md, verified 2026-11-03; recheck official sources before submission.",
            "arxiv_eligibility": "not-assessed",
            "errors": errors, "warnings": warnings, "human_review": manifest["human_review"],
            "files": [{"path": n, "sha256": sha256(p)} for n, p in sorted(paths.items())]}


def run(command, cwd):
    import os
    env = dict(os.environ, openin_any="p", openout_any="p")
    try:
        p = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        fail(f"command timed out after 120s: {command[0]}")
    return p


def snapshot(paths, report):
    expected = {item["path"]: item["sha256"] for item in report["files"]}
    result = {}
    for name, path in sorted(paths.items()):
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected[name]:
            fail(f"source changed during checks: {name}; rerun against stable evidence")
        result[name] = data
    return result


def preflight(root, manifest, output, reference_pdf=None):
    report = check(root, manifest)
    if report["errors"]:
        return report
    bbl = Path(manifest["main_tex"]).stem + ".bbl"
    uses_bibliography = any(re.search(r"\\(?:bibliography|addbibresource)(?![A-Za-z])", uncomment(p.read_text(encoding="utf-8")))
                            for p in load_manifest(root, manifest).values() if p.suffix == ".tex")
    if manifest["engine"] != "pdflatex" or (uses_bibliography and bbl not in manifest["files"]):
        report.update(status="not-run-unsupported-local-profile",
                      reason="This helper executes only three pdflatex passes with a prebuilt bibliography when used. Other supported arXiv engines and .bib-processing routes need a separate build; no eligibility decision was made.")
        return report
    needed = ["pdflatex", "pdffonts", "pdfinfo", "pdftotext"]
    missing = [x for x in needed if not shutil.which(x)]
    if missing:
        fail("preflight unavailable; missing tools: " + ", ".join(missing))
    out = Path(output).resolve()
    if out.exists() or out.is_relative_to(root):
        fail("preflight output must be a new directory outside the study")
    reference = Path(reference_pdf).resolve() if reference_pdf else None
    if reference and not reference.is_file():
        fail("reference PDF does not exist")
    contents = snapshot(load_manifest(root, manifest), report)
    out.mkdir(parents=True)
    source = out / "source"
    source.mkdir()
    for name, data in contents.items():
        dest = source / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    main = manifest["main_tex"]
    stem = Path(main).stem
    for index in range(1, 4):
        p = run(["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", "-recorder", main], source)
        (out / f"pass-{index}.txt").write_text(p.stdout + p.stderr, encoding="utf-8")
        if p.returncode:
            report["errors"].append(f"pdflatex pass {index} failed; inspect pass-{index}.txt")
            break
    pdf = source / f"{stem}.pdf"
    log = (source / f"{stem}.log")
    text = log.read_text(errors="replace") if log.exists() else ""
    for pattern, label in [(r"(?im)^!", "TeX error"),
                           (r"(?i)undefined control sequence|(?:reference|citation)[^\n]*undefined|undefined (?:references|citations)|rerun to get|labels? may have changed", "unresolved reference or rerun request"),
                           (r"Overfull \\[hv]box", "overfull box"),
                           (r"(?i)Package hyperref Warning", "hyperref warning")]:
        if re.search(pattern, text):
            report["errors"].append(label)
    if not pdf.exists():
        report["errors"].append("compiled PDF is missing")
    elif not report["errors"]:
        font = run(["pdffonts", str(pdf)], source)
        (out / "fonts.txt").write_text(font.stdout + font.stderr, encoding="utf-8")
        rows = [r.split() for r in font.stdout.splitlines()[2:] if r.strip()]
        if font.returncode or not rows:
            report["errors"].append("font inspection failed or reported no fonts")
        for row in rows:
            if len(row) < 8 or "Type 3" in " ".join(row) or row[-5] != "yes":
                report["errors"].append("nonembedded, Type 3 or unrecognized font row: " + " ".join(row))
        info = run(["pdfinfo", str(pdf)], source)
        (out / "pdfinfo.txt").write_text(info.stdout + info.stderr, encoding="utf-8")
        if info.returncode:
            report["errors"].append("pdfinfo failed")
        pages = re.search(r"(?m)^Pages:\s+(\d+)", info.stdout)
        report["pages"] = int(pages[1]) if pages else None
        extracted = run(["pdftotext", "-layout", str(pdf), "-"], source)
        if extracted.returncode:
            report["errors"].append("text extraction failed")
        report["pdf_sha256"] = sha256(pdf)
        report["text_sha256"] = hashlib.sha256(extracted.stdout.encode()).hexdigest()
        if reference:
            original = run(["pdftotext", "-layout", str(reference), "-"], source)
            match = original.returncode == 0 and original.stdout == extracted.stdout
            report["reference_text_matches"] = match
            if not match:
                report["errors"].append("clean-build PDF text differs from reference PDF (or extraction failed)")
            original_info = run(["pdfinfo", str(reference)], source)
            original_pages = re.search(r"(?m)^Pages:\s+(\d+)", original_info.stdout)
            report["reference_pages_match"] = bool(original_info.returncode == 0 and original_pages
                                                     and int(original_pages[1]) == report["pages"])
            if not report["reference_pages_match"]:
                report["errors"].append("reference PDF page count differs or could not be read")
    report["status"] = "fail" if report["errors"] else "local-preflight-pass"
    report["build_policy"] = "Three pdflatex passes, no shell escape, no bibliography engine. Supply .bbl when needed; this is a conservative local policy, not an arXiv requirement. Compile trusted source only; this is not an OS sandbox."
    write_json(report, out / "report.json")
    return report


def package(root, manifest, output):
    report = check(root, manifest)
    if report["errors"]:
        return report
    out = Path(output)
    if out.exists() or Path(str(out) + ".manifest.json").exists():
        fail("package or sidecar already exists; choose a new output")
    contents = snapshot(load_manifest(root, manifest), report)
    import gzip
    with out.open("xb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for name, data in contents.items():
                    info = tarfile.TarInfo(name)
                    info.size, info.mtime, info.mode = len(data), 0, 0o644
                    archive.addfile(info, io.BytesIO(data))
    report.update(status="packaged-unreviewed", archive_sha256=sha256(out),
                  limits="Packaging does not run preflight or confer human approval. Review local-preflight report, visuals, references, permissions and current arXiv guidance separately.")
    write_json(report, str(out) + ".manifest.json")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ["inventory", "extract", "check", "preflight", "package"]:
        sub = subs.add_parser(command)
        sub.add_argument("study", help="existing study directory")
        if command == "extract":
            sub.add_argument("--spec", required=True)
        if command in {"check", "preflight", "package"}:
            sub.add_argument("--manifest", required=True)
        sub.add_argument("--output", required=command in {"preflight", "package"})
        if command == "preflight":
            sub.add_argument("--reference-pdf")
    args = parser.parse_args(argv)
    try:
        root = root_dir(args.study)
        if args.command == "inventory":
            result = inventory(root)
        elif args.command == "extract":
            result = extract(root, read_json(Path(args.spec)))
        else:
            manifest = read_json(Path(args.manifest))
            if args.command == "check":
                result = check(root, manifest)
            elif args.command == "preflight":
                result = preflight(root, manifest, args.output, args.reference_pdf)
            else:
                result = package(root, manifest, args.output)
        write_json(result, args.output if args.command in {"inventory", "extract", "check"} else None)
        return 1 if result.get("errors") else 2 if result.get("status", "").startswith("not-run") else 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"arxivcheck: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
