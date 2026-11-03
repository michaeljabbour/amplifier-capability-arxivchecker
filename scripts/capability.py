#!/usr/bin/env python3
"""Inspect, export, and install the complete portable ArxivChecker method.

Python 3.11+; standard library only. No host registration, network or model calls.
Adapted from Right Shape's MIT-licensed capability release tooling.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DATE = (2026, 1, 1, 0, 0, 0)
OMIT = {".git", "__pycache__", ".DS_Store", ".pytest_cache", ".ruff_cache"}


def config() -> dict:
    data = json.loads((ROOT / "capability.json").read_text(encoding="utf-8"))
    for key in ("id", "display_name", "kind", "promise", "skill_path"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise ValueError("Missing capability field: " + key)
    if not re.fullmatch(r"[a-z][a-z0-9-]*", data["id"]):
        raise ValueError("Capability id is not a safe folder name")
    return data


def within(path: Path, parent: Path) -> Path:
    target = path.resolve()
    if not target.is_relative_to(parent.resolve()):
        raise ValueError("Path escapes its package: " + str(path))
    return target


def skill_root(data: dict) -> Path:
    source = ROOT / data["skill_path"]
    if source.is_symlink():
        raise ValueError("Portable skill root must not be a symlink")
    source = within(source, ROOT)
    if source == ROOT:
        raise ValueError("Portable skill must live in its own folder")
    return source


def portable_files(data: dict) -> list[Path]:
    source = skill_root(data)
    files = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part in OMIT for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("Portable package contains a symlink: " + str(relative))
        if not path.is_file():
            continue
        if any(part.startswith(".env") or part in {".secrets", "credentials.json"} for part in relative.parts):
            raise ValueError("Environment or credential file in portable package: " + str(relative))
        files.append(path)
    if [p.relative_to(source).as_posix() for p in files if p.name == "SKILL.md"] != ["SKILL.md"]:
        raise ValueError("The portable package needs exactly one canonical SKILL.md at its root")
    if not any(p.name.upper().startswith("LICENSE") for p in files):
        raise ValueError("The portable package must carry its license")
    for path in files:
        if path.suffix != ".md":
            continue
        for ref in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            uri = urlsplit(ref)
            if uri.scheme or uri.netloc or not uri.path:
                continue
            target = within(path.parent / unquote(uri.path), source)
            if not target.exists():
                raise ValueError("Missing installed reference: " + str(target.relative_to(source)))
    return files


def package_name(data: dict) -> str:
    return data["id"]


def file_map(data: dict) -> dict[str, bytes]:
    source = skill_root(data)
    return {p.relative_to(source).as_posix(): p.read_bytes() for p in portable_files(data)}


def export(data: dict, destination: Path) -> dict:
    files = file_map(data)
    destination = destination.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("Export destination already exists; choose a fresh archive path")
    destination = destination.resolve()
    destination = destination.resolve()
    if destination.is_relative_to(skill_root(data)):
        raise ValueError("Export destination must be outside the portable source")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(destination, "x", zipfile.ZIP_DEFLATED) as archive:
            for name, content in files.items():
                info = zipfile.ZipInfo(package_name(data) + "/" + name, ARCHIVE_DATE)
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, content)
    except BaseException:
        if destination.is_file():
            destination.unlink()
        raise
    return {"exported": str(destination), "files": len(files), "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}


def installed_map(target: Path) -> dict[str, bytes] | None:
    if not target.is_dir():
        return None
    result = {}
    for path in target.rglob("*"):
        if path.is_symlink():
            return None
        if path.is_file():
            relative = path.relative_to(target)
            if not any(part in OMIT for part in relative.parts):
                result[relative.as_posix()] = path.read_bytes()
    return result


def install(data: dict, destination: Path, replace: bool = False) -> dict:
    files = file_map(data)
    parent = destination.expanduser().resolve()
    target = parent / package_name(data)
    if target.is_symlink():
        raise ValueError("Refusing a symlink skill destination")
    source = skill_root(data)
    if target == source or target.is_relative_to(source) or source.is_relative_to(target):
        raise ValueError("Installation must not overlap the source skill")
    identical = target.is_dir() and installed_map(target) == files
    if identical:
        return {"installed": str(target), "files": len(files), "unchanged": True}
    backup = None
    if target.exists() and not replace:
        raise ValueError("Existing skill differs. Review it, or use --replace to retain a dated backup")
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".arxivchecker-install-", dir=parent) as temp:
        staging = Path(temp) / package_name(data)
        staging.mkdir()
        for name, content in files.items():
            dest = staging / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
        if target.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = target.with_name(target.name + ".backup-" + stamp)
            target.rename(backup)
        try:
            staging.rename(target)
        except BaseException:
            if backup is not None and not target.exists():
                backup.rename(target)
            raise
    return {"installed": str(target), "files": len(files), "unchanged": False, "backup": str(backup) if backup else None}


def doctor(data: dict) -> dict:
    files = portable_files(data)
    return {"capability": data["id"], "portable_method": "valid", "portable_files": len(files),
            "runtime_tools": {name: shutil.which(name) is not None for name in ("python3", "latexmk", "pdflatex", "pdffonts", "pdftoppm", "pdftotext")},
            "runtime_verified": False,
            "scope": "Packaging and tool availability only; no host load, model behavior, paper correctness or arXiv acceptance is established"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("doctor", help="Check portable method integrity and report tool availability")
    create = sub.add_parser("export", help="Create a deterministic complete skill ZIP")
    create.add_argument("--output", required=True, type=Path)
    add = sub.add_parser("install", help="Copy the complete skill to a host's discovery parent folder")
    add.add_argument("--dest", required=True, type=Path)
    add.add_argument("--replace", action="store_true", help="Back up a differing existing copy before replacing it")
    args = parser.parse_args()
    try:
        data = config()
        result = doctor(data) if args.operation == "doctor" else export(data, args.output) if args.operation == "export" else install(data, args.dest, args.replace)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
