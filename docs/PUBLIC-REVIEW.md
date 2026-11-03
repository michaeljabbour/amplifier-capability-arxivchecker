# Publication privacy review

Reviewed on 2026-11-03 before the initial public-source commit. This record covers the intended code, documentation, templates, workflow configuration, fixtures, media and rebuilt website. It is a review of this version, not a guarantee about later changes.

## Coverage and findings

Three independent read-only reviews examined all 82 initial Git candidates (72 text/structured files and 10 binary assets), generated-site text, all 18 portable ZIP members, both fixture PDFs and media metadata. Visual review covered the six film scenes, poster, social card and fictional figure/crop fixtures. No credentials, personal email addresses, private-paper names/results/visuals or unrelated confidential content were found. The public account identity and copyright notice are intentional.

Two machine-specific disclosures were found: an absolute home-directory URI in the install guide and 40 runtime/cache/checkout paths in the integration evidence. Original records were retained privately outside the repository. The guide now uses an explicit generic path; the public JSON replaces machine prefixes with documented aliases while preserving revisions and test outcomes. Generated copies were rebuilt. A subsequent scan of 169 text/archive blobs found no home paths, private temp paths, personal emails, private-key markers or token-shaped strings.

The quality workflow added afterward contains only source checkout and local tests/build checks. It has no deployment job. The separate Pages workflow remains manual-only. Review the final staged snapshot and commit metadata before pushing; use a public GitHub no-reply identity rather than a personal email address.

## Scope

The source paper and original installed skill remain private and unchanged. Only generic method adaptations, neutral templates and explicitly fictional fixtures are included. Media metadata is generic; browser code has no network/storage calls, and no external runtime assets are loaded.

[Validation](VALIDATION.md) records local tests and their limits. [Provenance](PROVENANCE.md) records the adaptation. Publication does not establish arXiv acceptance or scientific approval, and the website must be deployed separately from a source push.
