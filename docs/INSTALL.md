# Install and use ArxivChecker

For current submission-policy boundaries and human decisions, read the dated
[official arXiv source map](ARXIV-SUBMISSION.md). Installing this capability is
separate from registering, obtaining endorsement or submitting a paper.

This is a local, unpublished capability. The commands below use your existing
checkout. No hosted repository or website is required. Python 3.11 or later is
needed for packaging and the standard-library checking helpers.

## Portable skill

From the capability checkout:

```sh
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

`--dest` is the parent discovery directory supported by your host. For Claude
Code, use `--dest ~/.claude/skills`. The resulting folder is `arxivchecker/`.
The existing `arxiv-paper-from-study` installation is a separate source skill;
this installer does not replace or remove it. Avoid invoking both methods at
once. Start a new host session if discovery happens only at startup.

Ask:

> Use ArxivChecker on this completed study. Read its data, design, harness and
> methods before drafting. Put deliverables in a new paper-output folder. Show
> which claims and references are verified, inspect all figures and pages, and
> report the remaining human decisions. Do not submit it.

Keep `SKILL.md`, `references/`, `scripts/`, `templates/` and the license together.
The skill is a method applied by the host's model; it is not a background
service. Actual paper preparation needs the study files, exact author metadata,
rights decisions, a capable host and its usual file/command/browser tools.

### Inspect an install before changing it

The installer is idempotent when the complete installed copy matches. It
refuses a differing copy, extra non-cache files, or a symlink destination.
Review local changes before deliberately replacing a copy:

```sh
python3 scripts/capability.py install --dest /path/to/skills-parent --replace
```

`--replace` retains a dated sibling backup and reports its path. Restore that
folder if needed after moving the new install aside. This is a file copy, not
proof that the host discovered the skill or that a model followed it correctly.

### Export without installing

```sh
python3 scripts/capability.py export --output /tmp/arxivchecker-skill.zip
```

Choose a fresh path: existing exports are not overwritten. Extract the ZIP into
the host's skills parent, yielding `arxivchecker/SKILL.md` alongside all helpers
and references. The site build also creates a complete portable download. A
single `SKILL.md` download is for reading; it does not carry the full method.

## Amplifier

Add the behavior from the final checkout, using an absolute local URI:

```sh
amplifier bundle add "file:///absolute/path/to/amplifier-capability-arxivchecker/behaviors/arxivchecker.yaml" --app
```

Replace that path for another checkout. This deliberately changes the host's
app configuration; run it when you choose to enable the capability. The thin
root `bundle.md` is also available for hosts that load a bundle directly. The
behavior obtains Amplifier's modes, skills and recipes modules from their
official Microsoft source repositories, so first resolution may need network
access and the host's existing provider configuration. The portable skill and
standard-library helpers do not require these Amplifier modules.

Start a new Amplifier session:

- Ask for `arxivchecker` by name or use `/arxivchecker` where skill shortcuts are supported.
- `/arxiv` enables the working mode. `/mode off` leaves it.
- Run the optional staged recipe through the `recipes` tool:

```text
recipes(operation="validate", recipe_path="@arxivchecker:recipes/arxivchecker-paper.yaml")
recipes(operation="execute", recipe_path="@arxivchecker:recipes/arxivchecker-paper.yaml",
        context={"study_dir":"/absolute/path/to/study",
                 "output_dir":"/absolute/path/to/new-paper-output",
                 "author_details":"Exact names, author order and affiliations"})
```

The recipe first reads and returns a concrete evidence plan, then pauses for
approval. Approve with corrections using the `recipes` tool's `approve`
operation for stage `evidence`, then `resume` the session. Deny to stop before
paper preparation. Execution uses `agent: self`, so the calling session must
have this behavior and file/command/web tools available. Validation checks
structure; actual execution and scientific judgment need their own evidence.

Remove the behavior with:

```sh
amplifier bundle remove arxivchecker-behavior --app
```

When an explicit `tool-skills` source is configured, some Amplifier hosts no
longer scan their default skills directories. Preserve other desired sources in
your host configuration. Do not install a competing hand-copied ArxivChecker
folder into another Amplifier skill source.

## Optional paper tools

The site and portable installer have no third-party Python dependencies. The
method's paper workflow can use an existing TeX Live/MacTeX installation
(`latexmk`, `pdflatex`, BibTeX and required LaTeX packages), Poppler utilities
(`pdfinfo`, `pdffonts`, `pdftoppm`, `pdftotext`, `pdfimages`) and appropriate
figure tooling. Figure and crop templates document their optional Python
dependencies. Do not install a tool silently or claim a skipped check passed.

Use `doctor` to report available commands. It does not compile a paper, check
credentials, contact arXiv, validate references, establish host discovery, or
prove scientific correctness. See [validation](VALIDATION.md) for what was
actually tested in this delivery.

## Deterministic helper commands

From an installed skill folder, use relative paths as below. From the repository,
prefix `scripts/arxivcheck.py` with `skills/arxivchecker/`. Read the canonical
method and template manifests before configuring a real study.

```sh
python3 scripts/arxivcheck.py inventory /path/to/study --output /tmp/inventory.json
python3 scripts/arxivcheck.py extract /path/to/study --spec /path/to/extraction-spec.json --output /tmp/claims.json
python3 scripts/arxivcheck.py check /path/to/study --manifest /path/to/manifest.json --output /tmp/static-check.json
python3 scripts/arxivcheck.py preflight /path/to/study --manifest /path/to/manifest.json --output /tmp/new-preflight
python3 scripts/arxivcheck.py package /path/to/study --manifest /path/to/manifest.json --output /tmp/new-submission.tar.gz
```

Outputs must be fresh paths; the preflight folder must be outside the study.
These commands do not invent study-specific extraction rules or establish
reference accuracy. Static checks, local preflight and packaging have separate
statuses. A package remains unreviewed until the recorded human checks are done.
The three-pass `pdflatex` build is a conservative portability policy used by this
capability; it is not a claim that arXiv universally requires that exact route.
A local-profile failure does not establish that arXiv would reject a different
supported engine or bibliography workflow. Record and test that route separately.

Optional figure helpers use `scripts/make_figures.py --input metrics.json
--series condition-a --series condition-b --output /tmp/new-figure.pdf` and
`scripts/crop_artboards.py --input design-image.png --boxes boxes.json --output
/tmp/new-crops`. They require their documented third-party Python libraries.
Names, series IDs, input records and crop boxes must come from the current study.

## Local website

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:8000`. The site is static and local; building it does not
publish or deploy it. Stop the server with Ctrl+C. Rebuild after source changes.
