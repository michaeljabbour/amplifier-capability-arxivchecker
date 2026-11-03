# Publication privacy review

Reviewed on 2026-11-03 before the initial public-source commit. This record covers the intended code, documentation, templates, workflow configuration, fixtures, media and rebuilt website. It is a review of this version, not a guarantee about later changes.

## Coverage and findings

Three independent read-only reviews examined all 82 initial Git candidates (72 text/structured files and 10 binary assets), generated-site text, all 18 portable ZIP members, both fixture PDFs and media metadata. Visual review covered the six film scenes, poster, social card and fictional figure/crop fixtures. No credentials, personal email addresses, private-paper names/results/visuals or unrelated confidential content were found. The public account identity and copyright notice are intentional.

Two machine-specific disclosures were found: an absolute home-directory URI in the install guide and 40 runtime/cache/checkout paths in the integration evidence. Original records were retained privately outside the repository. The guide now uses an explicit generic path; the public JSON replaces machine prefixes with documented aliases while preserving revisions and test outcomes. Generated copies were rebuilt. A subsequent scan of 169 text/archive blobs found no home paths, private temp paths, personal emails, private-key markers or token-shaped strings.

The quality workflow added afterward contains only source checkout and local tests/build checks. It has no deployment job. The separate Pages workflow remains manual-only. Review the final staged snapshot and commit metadata before pushing; use a public GitHub no-reply identity rather than a personal email address.

## Scope

The source paper and original installed skill remain private and unchanged. Only generic method adaptations, neutral templates and explicitly fictional fixtures are included. Media metadata is generic; browser code has no network/storage calls, and no external runtime assets are loaded.

[Validation](VALIDATION.md) records local tests and their limits. [Provenance](PROVENANCE.md) records the adaptation. Publication does not establish arXiv acceptance or scientific approval, and the website must be deployed separately from a source push.

## Revision review — 2026-11-03

An independent read-only audit covered 62 changed/new files relative to `67c670e`, 190 text/generated blobs, all 19 portable ZIP members and media metadata. It found no private machine paths, personal email addresses, credentials/secrets, private Library identifiers or transplanted study results in the reviewed revision. The supplied secondary guidance is represented only by independently verified official-source conclusions; no raw attachment is included.

This supplements the initial review above. It covers the local revision only; no publication, push or deployment was performed as part of this revision audit.

The coordinator subsequently inspected the fictional layout fixture's source,
PDF, page renders, build summary and font evidence, plus the browser-review JSON
and final 50-test log. These additions contain generic names, illustrative
content and local-check results. A final scan of 210 source/generated text files and all 19 ZIP members found no
private paths, attachment identifiers, personal emails or credential patterns.
The original source skill remains outside the repository.

## Supplied v2 film update — 2026-11-03

Reviewed the owner's 29 prepared candidates, related generated files, media
metadata and sampled frames. No credentials, personal contact details, private
study material or private media metadata were found. Internal production flow
identifiers, cloud workspace paths and unrelated project references in source
notes were omitted from public copies; originals were preserved privately. The
exact supplied MP4 has the same encoded/decoded picture and sound as the
prepared local v2. All v1 asset bytes remain unchanged. See [video integration
and independent review](VIDEO-UPDATE.md) for verification scope, rights and
listening limitations. The final independent recheck covered 42 candidates, 152 generated files and all 19 ZIP members, with no privacy blockers. Subsequent test/browser records contain only generic local-check observations; the staged snapshot is scanned again before commit.
