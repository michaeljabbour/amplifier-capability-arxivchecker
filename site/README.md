# ArxivChecker website

A dependency-free static site in the Amplifier family. It explains the capability,
shows the ten canonical workflow stages, teaches claim scoping with an explicitly
fictional example, and offers the complete portable skill ZIP.

## Build and preview

From the repository root with Python 3.11+:

~~~sh
python3 scripts/build.py
python3 scripts/check.py
node --check site/site.js
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
~~~

Open http://127.0.0.1:8000. The build uses only Python's standard library. The optional
Node command checks browser-script syntax; Node is not a site dependency.

The builder only writes this checkout's generated `_site/` directory. It refuses
a symlink or a different output path. All paths in the output support repository
subpath hosting.

## Source ownership

- `site.json`: page metadata and one explicitly fictional claim illustration.
- `template.html`: semantic landing-page content.
- `style.css`: product styles; `site.js`: copy feedback and an in-memory checklist.
- `../skills/arxivchecker/references/workflow.json`: canonical stage summaries,
  rendered directly into the page. Do not fork this list.
- `../skills/arxivchecker/SKILL.md` and workflow/policy references: directly rendered
  into `guide.html`. The canonical `requirements.md` and `submission.md` maps are
  also rendered in full, with stable browser anchors and direct primary citations.
  The exact sources remain available as downloads. The visible verification date
  comes from the canonical requirements map, never separate site metadata.
- `../scripts/capability.py`: the builder imports the installer’s package enumerator
  and exporter. The site and installer ship precisely the same skill folder.
- `assets/`: original favicon, SVG/PNG social card, silent films, captions, poster and transcript.
- `film-source/`: optional film regeneration source and instructions.

The check validates local links/fragments, exact workflow and source fidelity,
ZIP membership and contents, SHA-256, local runtime assets, explicit claim limits,
video controls, captions, image alternatives and one canonical skill source.
It also verifies complete rendered requirement/submission map fidelity, their
primary-source links, the visible canonical verification date and the explicit
separation of official rules from the helper's local profile.
Visual inspection and interaction checks remain separate from these structural checks.

## Design

The characteristic element is a manuscript with proof marks and a visible route
from claim to source. Cool paper `#f1f5f8`, navy ink `#132d43`, muted text
`#4b6172`, teal evidence `#175f66` and red proof marks `#a53839`.
Georgia headings and Arial body use system fonts; no remote font requests.

No automatic playback or animation, tracking, study upload, browser persistence
or backend. The review checklist resets on reload and makes no readiness claim.
Native details, labelled controls, keyboard focus, reduced-motion handling and
no-JavaScript reading/download paths are included.

## Provenance and publication

`theme/style.css` is the unchanged Amplifier Smart Tools family v0.1.0 snapshot
copied through Right Shape. Its Microsoft MIT notice is retained in
[theme/LICENSE](theme/LICENSE). Product content, illustration and interaction are
new. No arXiv endorsement is implied.

The manual GitHub Pages workflow is provided for an owner to run after establishing
an authorized repository and Pages environment. Creating these files did not
publish or deploy the site. There is no canonical hosted URL asserted in metadata.
