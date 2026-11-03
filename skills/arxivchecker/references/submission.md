# arXiv submission grounding

Official documentation checked on **2026-11-03**. ArxivChecker prepares a local
paper and review package; it does not certify eligibility or acceptance. Recheck
the linked pages before a real submission. This is an independent capability,
not an arXiv service or endorsement. The portable method's
[policy reference](policy.md) travels with the
installed skill.

## Policy-to-workflow map

| Topic and official source | Consequence for ArxivChecker | Exception or boundary |
| --- | --- | --- |
| [Submission overview](https://info.arxiv.org/help/submit/index.html) | Prepare a self-contained scholarly work, preserve its required figures and check the uploaded files, selected processor, top-level source, metadata and generated PDF. | A local build cannot reproduce the actual submission system. Passing local checks does not make a paper eligible or accepted. |
| [Content moderation](https://info.arxiv.org/help/moderation/index.html) | Keep claims, references and presentation accurate; assess whether the work serves a community arXiv covers. | Moderation is not peer review. Prior journal publication does not guarantee acceptance. Moderators may reclassify or decline a work. |
| [Format requirements](https://info.arxiv.org/help/policies/format_requirements.html) | Review title/authorship, complete references, machine readability, single spacing, 10–14 point type and margins of at least one inch. Resolve public code/data links included in the paper. Check the official list of unwanted content. | The neutral template's exact 11 point size and 1.05-inch geometry are local choices within that guidance; the extra space is a rendered-ink buffer. Letter paper, newtx, natbib and omission of page numbers are local preferences. |
| [Authorship metadata](https://info.arxiv.org/help/prep.html#authors-required) | Obtain correct names, order and affiliations from the responsible authors. Check the submission-form metadata separately from the PDF. | arXiv permits first/middle initials; this project's full-name preference is not an arXiv requirement. Named collaborations have special metadata rules, while the paper must contain the full author/affiliation list. |
| [Identity and affiliation](https://info.arxiv.org/help/policies/identity_and_affiliation.html), [registration](https://info.arxiv.org/help/registerhelp.html) | Never infer an affiliation or claim institutional approval. The submitter handles an accurate account and identity. | An institution is not a prerequisite for authorship: registration explicitly accommodates independent researchers. ORCID linkage is recommended, not a substitute for author confirmation. |
| [Submittal agreement](https://info.arxiv.org/help/policies/submission_agreement.html) | Leave a visible decision for all-author consent, submitter authority and rights to distribute the work and third-party material. | A local manifest's author list or review checklist does not establish consent, authority or rights. Permission to prepare a paper is not permission to bind its authors to the agreement. |
| [Significant AI use](https://info.arxiv.org/help/moderation/index.html#policy-for-authors-use-of-generative-ai-language-tools) | Describe significant sophisticated-tool use, including generative text tools, in a way consistent with the subject's methodology standards. Human authors review and take responsibility for all content. | arXiv does not prescribe this template's section title or a universal sentence. Do not invent a declaration of completed review. AI tools must not be listed as authors. |
| [License information](https://info.arxiv.org/help/license/index.html) | The responsible submitter chooses an appropriate available license after checking rights, funder and publisher constraints. Record the actual choice and decision owner. | The choice for an announced version is irrevocable; later versions may have different licenses. The capability's MIT license does not choose or relicense the research paper, figures or data. |
| [Category taxonomy](https://arxiv.org/category_taxonomy), [cross-listing](https://info.arxiv.org/help/cross.html) | Propose categories from the paper's substantive content and the current category descriptions; have the author decide. Justify any cross-list. | Do not default every AI-related study to `cs.AI`. Cross-lists should address a direct reader interest; moderators can remove inappropriate ones. |
| [Endorsement](https://info.arxiv.org/help/endorsement.html) | Have the submitter check the endorsement status required for the intended category in their account. Record any outstanding step. | Endorsement is account/category dependent and can be obtained through different routes. An affiliation, local build or existing paper does not by itself prove this submitter is currently endorsed. |
| [Third-party submission](https://info.arxiv.org/help/third_party_submission.html) | Prefer author-controlled submission. Any proxy path must satisfy arXiv's approval and author-validation conditions. | A general-purpose assistant or this recipe is not automatically an approved proxy. This capability neither requests endorsement from people nor uploads a paper. |
| [Archive creation](https://info.arxiv.org/help/tar.html), [ancillary files](https://info.arxiv.org/help/ancillary_files.html) | Use an explicit source allowlist and inspect archive contents. Keep optional ancillary material in root `anc/`, with release permission and a clear purpose. | `.tar.gz` and ZIP are supported routes; the helper's `.tar.gz` choice is not the only option. Ancillary files currently require TeX/PDFLaTeX source submissions; TeX sources do not belong in `anc/`. |

## Content-type and account checks

The following official sources were checked directly on **2026-11-03**. These conditions concern moderation and submitter status, not the manuscript's local compilation result.

| Topic and official source | Verified scope | ArxivChecker action and limits |
| --- | --- | --- |
| [Scholarly interest](https://info.arxiv.org/help/moderation/index.html#scholarly-interest), [content types](https://info.arxiv.org/help/policies/content-types.html) | Work should be substantive, self-contained and relevant to a served research community; lack of originality, novelty or significance may lead to decline. | Ask what contribution is original and what evidence supports it. Editing or adding a polished layout does not establish novelty or scientific merit. |
| [CS review/position-paper practice, 2025-10-31](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/) | CS review/survey and position papers must have prior journal/conference acceptance and documentation of completed successful peer review for consideration. Workshop review generally does not suffice. Original scientific research is not subject to this particular practice. | Identify content type before choosing a route; obtain real acceptance/review evidence when applicable. Do not generalize this into prior-peer-review requirements for every original study or category. Acceptance still is not guaranteed. |
| [Rate-policy FAQ, effective 2026-10-01](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/), [current summary](https://info.arxiv.org/help/moderation/index.html#submission-rate) | Up to two new submissions per calendar month and at most three active submissions. The detailed FAQ applies accounting across categories to the submitter, not automatically to each coauthor; rejected submissions count. | Have the responsible submitter check actual account capacity. A prepared archive proves neither a free slot nor permission to submit. |
| [Rate-policy exceptions](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/), [replacement instructions](https://info.arxiv.org/help/replace.html#to-replace-an-article) | Prior-month on-hold work remains active but does not consume the next month's monthly allotment. Deletion before announcement removes that submission from monthly/active counts. Replacements have separate weekly guidance, enforced after version 5. | Preserve the distinction among new submissions, active work and replacements. The reviewed FAQ does not explicitly settle every replacement/active-quota interaction; confirm unclear cases rather than inventing a blanket exemption. |

Two source details require care. First, the moderation summary uses “author” in its quota sentence, whereas the linked detailed FAQ specifically limits accounting to the submitter. Use the FAQ's precise scope. Second, the CS practice announcement requests peer-reviewed reference/DOI metadata, while [metadata instructions](https://info.arxiv.org/help/prep.html#journal-ref) reserve `Journal-ref` for published works. If a paper is accepted but unpublished, supply genuine acceptance/review documentation and confirm the appropriate current field/support path; never fabricate publication details or a DOI to satisfy a form.

The owner supplied a secondary policy summary. Its relevant claims were independently checked against these official sources; the private summary is not redistributed. A compact evidence record is in the repository's `docs/ATTACHMENT-VERIFICATION.md`. The canonical requirements and this submission map remain the authority for the installed workflow.

## Details a successful compile does not check

The official format guidance says line numbers, margin notes, highlighted text,
referee remarks, advertisements and text-obstructing watermarks should not be
present. It directs slides and posters out of the article body and into
ancillary material. Preserve explanatory design figures where appropriate;
do not automatically insert entire presentation artboards as article pages.
Copyright statements are evaluated for whether they impair redistribution,
not banned categorically. Permitted publisher notices may be required on the
first page. See [format requirements](https://info.arxiv.org/help/policies/format_requirements.html)
and [copyright notices](https://info.arxiv.org/help/license/index.html#copyright-notices).

Submission metadata needs its own review. The current preparation page
specifies title, authors and abstract, ASCII/TeX-accent handling, author-list
formatting and an abstract limit of 1,920 characters. Do not paste PDF ligatures
or infer that a valid LaTeX byline is valid form input. See
[metadata preparation](https://info.arxiv.org/help/prep.html).

Semantic source deserves a separate check. arXiv's [LaTeX markup best practices](https://info.arxiv.org/help/submit_latex_best_practices.html) recommend structural commands, standard frontmatter, supported conversion packages and image alternatives. These improve accessible HTML; they do not impose one class, column count, heading arrangement or blanket acceptance gate. See the [source/typesetting map](requirements.md#latex-source-and-typesetting-recommendations).

Do not refer to `anc/` as a build-input dependency. Ancillary material is stored
with an article version, and it cannot be changed independently. PDFs containing
embedded JavaScript fail arXiv processing. A full study kit may contain useful
review material that should never be included in the submission archive. See
[ancillary-file instructions](https://info.arxiv.org/help/ancillary_files.html).

## Local checking profile and exceptions

`arxivcheck.py` implements a deliberately bounded portability profile: explicit
files, portable paths, a `pdflatex` engine, a prepared bibliography when needed,
three clean passes, font inspection and optional extracted-text/page-count
comparison. Its file-count/size caps, explicit-template marker checks, editorial font gate and
`human_review` record are local checks. They do not enumerate arXiv's complete
requirements. Consult [tooling](tooling.md)
for the exact interface. The repository’s `docs/VALIDATION.md` records observed
tests; an installed skill does not carry the repository’s local test evidence.

A local profile failure means that this profile failed. It does not prove that
arXiv will reject another supported engine, bibliography workflow, valid author
format or submission route. Conversely, a local profile pass can miss semantic
TeX dependencies, policy issues, inaccurate citations or a scientific defect.
Record the particular failed or skipped check and test an alternative route
explicitly; never relabel an untested route as passing.

## Decisions still owned by people

Before any actual submission, the responsible authors must resolve scientific
and label review; accurate authorship, affiliations and consent; significant
AI-use wording; third-party/data/privacy/release rights; the selected paper
license; category and cross-list choices; account/endorsement or approved proxy
status; public code/data claims; and the final metadata and arXiv-generated PDF.
Keep unresolved items visible with an owner and next action. The current recipe
ends with a local handoff and never treats an archive as author approval.
