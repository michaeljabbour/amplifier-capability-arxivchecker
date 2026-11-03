# MJ's publishing style

This is the owner's editorial style, layered on top of the applicable arXiv requirements in [the requirements map](requirements.md). It is not an arXiv template, required section order or acceptance rule. Adapt it to the audience and field while preserving the study's evidence.

## Teach the reader the study

Start with the problem in ordinary language, then explain what was built and why that design was chosen. Introduce the test setup before reporting its results. A reader should be able to follow the question, system, experiment, answer and limitations without already knowing the project's internal names.

Use a short overview to give the reader a route through the argument. Let each section answer a question raised by the previous one. Explain why a comparison, measurement or design choice matters before presenting a dense table of its values. Keep the distinction between observations and interpretation visible.

## Spend jargon carefully

Remove specialized words that add no precision. Prefer “the program that runs the tests” to an unexplained “harness,” for example. When a technical term matters, define it at first use in the sentence, with a small example if useful. Use the standard term after the reader understands it.

A brief footnote can hold a necessary technical definition or secondary detail when it would interrupt the main explanation. Do not put the main conclusion, a material limitation, the reporting unit or an essential method in a footnote. Footnotes must remain legible and compatible with the applicable format guidance; inspect their rendered size and placement. Do not treat an abbreviation list as a substitute for explaining the idea.

## Make visuals do explanatory work

Choose each visual for a reader question: what was built, how the test ran, how the methods differ, what changed, or where the uncertainty lies. Introduce the visual where that question arises and explain its takeaway in the surrounding text. A design diagram can make the experiment intelligible before a results chart asks the reader to judge it.

Prefer direct labels, consistent units and category colors, readable type and captions that explain the population, denominator, comparison and uncertainty. Make diagrams understandable without relying on color alone. Supply meaningful text alternatives where the toolchain supports them, following arXiv's [LaTeX markup recommendations](https://info.arxiv.org/help/submit_latex_best_practices.html). Those recommendations support accessibility; a useful picture still needs accurate data and human inspection.

Preserve all required series and relevant context. Do not crop away a footnote or qualification. A visual should clarify the evidence, not make an unsupported finding look stronger. Whole slide decks/posters are different from explanatory article figures; follow the route-specific official guidance.

## Write precise, readable results

Lead with the answer to the research question, then the evidence needed to assess it. Give counts with denominators and units, and state what an estimated cost includes. Keep preregistered decisions, later exploration, negative findings and unresolved questions distinct. Readability is never a reason to hide an inconvenient result or uncertainty.

For an illustrative structure, not a research finding: “We built [system] to address [problem]. We tested it using [design and comparison]. We observed [measured answer], with [important limit].” Fill those slots from this study's evidence, not a template's invented example.

## Keep page references useful

Show visible page numbers on the first and subsequent pages by default so readers can refer to a passage during review. This is MJ’s preference, not an arXiv rule. Follow a different treatment when an author or venue requests it, and record that choice. Keep the page number and all other footer ink inside the applicable margins; inspect the rendered pages.

## Review the explanation

Before handoff, check that a reader can explain what was built, why it was tested, what the result means and what remains unknown. Check every unnecessary acronym, undefined term, decorative visual and paragraph that lists statistics without developing the argument. Keep the prose pedagogical without talking down to the reader.

Scientific review, the cited arXiv policies and MJ's editorial review remain separate. A local build or style checklist cannot certify any of them.
