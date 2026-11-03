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
- `assets/`: original favicon, SVG/PNG social card, narrated films, captions, poster and full/short transcripts.
- `film-source/`: optional film regeneration source and instructions. `film-source/v2/` holds the historical v2 production archive. The main player uses the supplied v3 finished film (`assets/arxivchecker-film-v3*`), with corrected visible page numbers, updated captions and transcript; v1/v2 films and cuts remain in `assets/`. The v3 production project was not supplied, so a reproducible production rebuild is not claimed. See [v3 verification](../docs/VIDEO-V3.md).

The check validates local links/fragments, exact workflow and source fidelity,
ZIP membership and contents, SHA-256, local runtime assets, explicit claim limits,
video controls, captions, image alternatives and one canonical skill source.
It also verifies complete rendered requirement/submission map fidelity, their
primary-source links, the visible canonical verification date and the explicit
separation of official rules from the helper's local profile.
Visual inspection and interaction checks remain separate from these structural checks.

## Design

The layout follows the actual family pages: a slim attribution band, the common
Amplifier masthead, a large product name and pedagogical tagline on the left, and
plain benefits, actions and limits on the right. Proof marks stay in the claim
audit and original artwork. Shared family paper `#f6f4ee`, charcoal ink `#252823`, muted text
`#64685e`, rules `#d8d8cc`, gold `#80642f`, sage accent `#486b61` and
wash `#e9ede5`. Product proof marks use `#8c473d`.
Georgia headings and Arial body use system fonts; no remote font requests.

The full and short films include voiceover, English captions and separate
transcripts. The player announces sound and waits for a click.
The landing page presents the main player and its caption control without an
always-visible row of film links. Supporting cuts, transcripts, notes and prior
media remain in the project; a transcript link remains inside the player's
browser fallback.

Visible page numbers are the house default, with author or venue exceptions.
This is a local editorial choice, not an arXiv requirement.

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

## Concrete family comparison

Reviewed on 2026-11-03. These comparisons use the actual checked-out source files,
not a newly invented palette. Live Right Shape and Taste pages were also inspected
in the browser during this revision; the other URLs below are documented entry
points and are not claimed as separately verified live renders here.

| Reference | Source inspected | Documented page / observed convention |
| --- | --- | --- |
| Right Shape | `amplifier-skill-right-shape/site/theme/style.css`, `site/style.css`, `site/template.html` | [Live Right Shape](https://michaeljabbour.github.io/amplifier-skill-right-shape/): paper/charcoal, slim top band, Amplifier masthead, large two-line product title left and plain explanation right. Indigo is its product accent, not a new base palette. |
| Taste × Elegance | `amplifier-skill-taste/site/theme/style.css`, `site/style.css`, `site/template.html`, README | [Live Taste](https://michaeljabbour.github.io/amplifier-skill-taste/): same base, sage accent, Georgia display, Arial body and narrated player with captions. |
| Decisioncraft | `amplifier-smart-tool-decisioncraft/site/theme/style.css`, `site/README.md`, README | [Documented Decisioncraft page](https://michaeljabbour.github.io/amplifier-smart-tool-decisioncraft/): versioned Amplifier Smart Tools family theme; static source and labelled fictional examples. |
| Unfold | `amplifier-smart-tool-unfold/site/theme/style.css`, `site/README.md`, README | [Documented Unfold fork page](https://robotdad.github.io/amplifier-smart-tool-unfold/): shared paper, gold details, typography and navigation. This is the documented robotdad fork, not an MJ-owned page. |
| Project Handoff | `amplifier-skill-project-handoff/site/theme/style.css`, `site/style.css`, `site/template.html` | Local source comparison: common Amplifier masthead, product-name hero, two-column explanation, fine rules and portable-skill handoff. No live-page verification is claimed. |

The common base declares `--paper:#f6f4ee`, `--ink:#252823`,
`--muted:#64685e`, `--line:#d8d8cc`, `--gold:#80642f`,
`--accent:#486b61`, `--wash:#e9ede5`, Georgia/Times serif and Arial/Helvetica
sans. Its content wrapper is 1180 px with 80 px total desktop inset; the hero uses
1.2fr/1fr columns, and primary actions use charcoal on paper. Product overrides
vary accents and display scale while keeping that baseline.

Source-theme SHA-256 for Right Shape, Taste, Decisioncraft and Project Handoff:
`794600af68c7fc2af0340a5acc13051886441aca4f58870e7d4d110168638d20`.
Unfold's theme hash is
`9f87606ad071c908917c0e0620343f432e9fae27fbe66d994effc4369bdc969b`;
its declared base tokens match, but its complete theme has other changes.

Browser-computed values recorded for live Right Shape were body background
`rgb(246,244,238)`, ink `rgb(37,40,35)`, Arial body, Georgia title at 94.72 px
in the inspected desktop viewport, and the same paper/ink/line/gold/wash tokens.
Taste's live page confirmed the same shared baseline. Viewport-dependent title
size is evidence from that view, not a universal fixed value.

ArxivChecker keeps the theme's MIT notice and does not copy institutional
attribution or imply endorsement. The publication section distinguishes official
requirements, LaTeX markup recommendations and the owner's publishing style.
The full writing guide is rendered from the canonical installed reference.
