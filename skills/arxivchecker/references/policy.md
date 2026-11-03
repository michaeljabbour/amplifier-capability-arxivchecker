# arXiv policy and project defaults

**Official-document review: 2026-11-03 (UTC).** Read the [requirements map](requirements.md) before asserting a rule or rejecting a submission path. It records scope, classification, official links, conflicts and local-check limits. This independent capability does not approve submissions or guarantee acceptance.

## Apply the right class of rule

The [format policy](https://info.arxiv.org/help/policies/format_requirements.html) specifies title/authorship, complete references, machine readability, public destinations for included code/data links, single spacing, 10–14 pt type and at least one-inch margins. Its excluded features include line numbering, obscuring watermarks, advertising, highlighting, editorial annotations, slides/posters in the article body and incompatible redistribution restrictions. It uses `should` wording and permits moderation to request individual corrections. Inspect the document; do not invent a page-number prohibition.

The [current TeX instructions](https://info.arxiv.org/help/submit_tex.html) and [TeX Live guide](https://info.arxiv.org/help/faq/texlive.html) define conditional processing requirements. Select the processor and bibliography route. Current arXiv processes `.bib` and accepts prepared `.bbl`; a `.bib`-only or literal-bibliography paper is not invalid because a local runner lacks that route. Keep required index/glossary and matching `minted` cache inputs. Match figures to the processor, include needed custom dependencies and inspect the server-rendered PDF.

[PDF-only submissions](https://info.arxiv.org/help/submit_pdf.html) have separate combined-file, readable-text, font and no-JavaScript conditions. Their no-mixed-file rule does not prohibit PDF figures in TeX source uploads. [Ancillary support](https://info.arxiv.org/help/ancillary_files.html) is route-specific. [Size help](https://info.arxiv.org/help/sizes.html) includes an image-pixel warning with exceptions, not a verified universal total-byte cap. Resolve unclear cases through current UI/support instead of inventing thresholds.

[Significant AI use](https://info.arxiv.org/help/moderation/index.html#policy-for-authors-use-of-generative-ai-language-tools) must be reported consistently with field methodology standards. Human authors remain responsible; tools are not authors. [Rights/coauthor consent](https://info.arxiv.org/help/policies/submission_agreement.html), [licence choice](https://info.arxiv.org/help/license/index.html) and [endorsement](https://info.arxiv.org/help/endorsement.html) remain human/account decisions. A paper need not use this capability's software licence.

## Keep local preferences visibly local

The starter's `article` class, Letter paper, 11 pt, newtx, microtype, booktabs, numeric natbib and dark-blue links are choices within applicable format requirements. No page numbers preserves the user's preference. Exact full names, balanced bylines, section order, vector-chart defaults, specific disclosure/limitations headings, crop previews and claim/reference ledgers are local method choices.

Manifest schema, resource caps, overwrite protection, runner profiles, exactly three build passes and optional PDF comparison are local checks. Missing executables, unsupported routes, dynamic dependencies, warnings and pending visual reviews retain their own meanings. They cannot become a generic arXiv eligibility failure. Record what ran, what remains unassessed and what needs responsible submitter review.
