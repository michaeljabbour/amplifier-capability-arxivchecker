#!/usr/bin/env python3
"""Exercise local Amplifier integration without a provider or global install.

Run with a Python environment that already contains amplifier_foundation and
amplifier_app_cli. Official bundle includes are resolved only from local cache
checkouts. The test never creates an Amplifier session, invokes a model,
downloads dependencies, or changes host app configuration.
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def cached_repo(cache: Path, name: str, suffix: str = "") -> Path:
    candidates = [p for p in cache.glob(name + "-*") if p.is_dir() and (p / suffix).exists()]
    if not candidates:
        raise FileNotFoundError("No cached checkout for " + name + "/" + suffix)
    # Multiple snapshots can exist. Record the selected checkout and revision;
    # this is an observed local integration test, not a pin or remote update.
    return max(candidates, key=lambda p: (p.stat().st_mtime_ns, p.name))


def revision(path: Path) -> str | None:
    result = subprocess.run(["git", "--no-optional-locks", "-C", str(path), "-c", "core.fsmonitor=false", "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


async def smoke(checkout: Path, cache: Path) -> dict:
    from amplifier_foundation import BundleRegistry
    from amplifier_app_cli.lib.mention_loading.app_resolver import AppMentionResolver

    module_roots = {}
    for repo, suffix in (("amplifier-bundle-modes", "modules/hooks-mode"), ("amplifier-bundle-skills", "modules/tool-skills"), ("amplifier-bundle-recipes", "modules/tool-recipes")):
        selected = cached_repo(cache, repo, suffix)
        module_roots[repo] = selected
        sys.path.insert(0, str(selected / suffix))
    from amplifier_module_hooks_mode import ModeDiscovery
    from amplifier_module_tool_skills import SkillsTool
    from amplifier_module_tool_recipes import RecipesTool

    selected_includes = {}

    def local_include(uri: str) -> str | None:
        if not uri.startswith("git+"):
            return None
        parsed = urlsplit(uri[4:])
        if parsed.netloc != "github.com" or not parsed.path.startswith("/microsoft/"):
            raise ValueError("Only official Microsoft cached includes are admitted: " + uri)
        name = parsed.path.rstrip("/").split("/")[-1].split("@")[0].removesuffix(".git")
        suffix = parse_qs(parsed.fragment).get("subdirectory", [""])[0]
        if Path(suffix).is_absolute() or ".." in Path(suffix).parts:
            raise ValueError("Unsafe cached include suffix")
        source = cached_repo(cache, name, suffix)
        selected_includes[uri] = {"checkout": str(source), "revision": revision(source), "suffix": suffix}
        return (source / suffix).as_uri()

    class Coordinator:
        def __init__(self, resolver):
            self.resolver = resolver

        def get_capability(self, name):
            return self.resolver if name == "mention_resolver" else None

    records = []
    with tempfile.TemporaryDirectory(prefix="arxivchecker-amplifier-smoke-") as temp:
        for entry in ("bundle.md", "behaviors/arxivchecker.yaml"):
            registry = BundleRegistry(home=Path(temp), strict=True, persist=False, read_persisted=False, include_source_resolver=local_include)
            bundle = await registry.load((checkout / entry).as_uri(), auto_register=False)
            resolver = AppMentionResolver(bundle_mappings=bundle.source_base_paths)
            paths = {mention: resolver.resolve(mention) for mention in ("@arxivchecker:skills", "@arxivchecker:modes", "@arxivchecker:recipes/arxivchecker-paper.yaml")}
            if not all(p and p.exists() for p in paths.values()):
                raise ValueError("Namespace resolution failed: " + repr(paths))
            skills = SkillsTool(config={}, resolved_dirs=[paths["@arxivchecker:skills"]])
            loaded = await skills.execute({"skill_name": "arxivchecker"})
            if not loaded.success:
                raise ValueError("Skill discovery/load failed: " + repr(loaded))
            modes = ModeDiscovery(search_paths=[paths["@arxivchecker:modes"]], working_dir=Path(temp))
            mode_names = [item.name for item in modes.list_modes()]
            if "arxiv" not in mode_names:
                raise ValueError("/arxiv mode not discovered")
            recipes = RecipesTool(executor=None, session_manager=None, coordinator=Coordinator(resolver), config={})
            validation = await recipes.execute({"operation": "validate", "recipe_path": "@arxivchecker:recipes/arxivchecker-paper.yaml"})
            if not validation.success:
                raise ValueError("Recipe validation failed: " + repr(validation))
            records.append({"entry": entry, "loaded": True, "tools": [item["module"] for item in bundle.tools], "hooks": [item["module"] for item in bundle.hooks], "namespace_paths": {key: str(value) for key, value in paths.items()}, "skill_discovered_and_loaded": True, "modes": mode_names, "recipe_validation": validation.model_dump()})
    return {"status": "passed", "records": records,
            "cache_modules": {key: {"checkout": str(value), "revision": revision(value)} for key, value in module_roots.items()},
            "cached_includes": selected_includes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, default=ROOT)
    parser.add_argument("--cache-root", type=Path, default=Path.home() / ".amplifier/cache")
    parser.add_argument("--output", type=Path, help="Fresh JSON evidence path; otherwise print only")
    args = parser.parse_args()
    if args.output and (args.output.exists() or args.output.is_symlink()):
        parser.error("Evidence output already exists; choose a new path")
    record = {"schema": "arxivchecker-integration-smoke/v1", "observed_at": datetime.now(timezone.utc).isoformat(), "python": sys.executable,
              "scope": "Cached local bundle composition, namespace resolution, skill loading, mode discovery and recipe validation only. No provider/model/session execution, remote fetching, global install or app configuration mutation."}
    try:
        record.update(asyncio.run(smoke(args.checkout.expanduser().resolve(), args.cache_root.expanduser().resolve())))
    except Exception as error:
        record.update({"status": "failed", "error": type(error).__name__ + ": " + str(error)})
    encoded = json.dumps(record, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")
    return 0 if record["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
