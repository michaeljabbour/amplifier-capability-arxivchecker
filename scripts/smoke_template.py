#!/usr/bin/env python3
"""Build a fictional fixture from the actual starter and measure rendered text bounds.

Requires existing pdflatex and Poppler tools. No network or scientific/policy approval.
Text bounds do not measure diagrams, rules or every PDF object; inspect the renders.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='new fixture/evidence directory')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error('Choose a new output directory; evidence is never overwritten')
    for name in ('pdflatex', 'pdffonts', 'pdfinfo', 'pdftotext', 'pdftoppm'):
        if not shutil.which(name):
            parser.error('Missing local tool: ' + name)
    output.mkdir(parents=True)
    study = output / 'study'
    study.mkdir()
    template = (ROOT / 'skills/arxivchecker/templates/main.tex').read_text()
    source = template.replace('REPLACE_ME', 'Fixture')
    source = source.replace('Fixture study title', 'Fictional typesetting fixture')
    source = source.replace('Fixture exact full author name(s)', 'Example Researcher')
    source = source.replace('Fixture exact affiliation(s)', 'Fictional Laboratory')
    source = source.replace('Fixture fixed month and year', 'November 2026')
    source = source.replace('\\section{Methods}', '\\section{Methods}\n'
        'This is a software fixture, not a scientific study. A test runner'
        '\\footnote{A program that executes the checks and records the results.}'
        ' checks the template.\\cite{fixture}\n')
    source = source.replace('Fixture write from the extracted evidence ledger. Report counts with denominators and units.',
        'Fixture write from the extracted evidence ledger. Report counts with denominators and units.\n'
        '\\begin{figure}[htbp]\\centering\n'
        '\\fbox{\\parbox{0.8\\linewidth}{\\centering Study files $\\rightarrow$ '
        'checked values $\\rightarrow$ reviewable paper}}\n'
        '\\caption{An illustrative workflow, not study data. Each step needs its own evidence and review.}'
        '\\end{figure}\n')
    (study / 'main.tex').write_text(source)
    (study / 'references.bib').write_text('@misc{fixture,title={Fictional software fixture},'
        'author={{Example Researcher}},year={2026},note={No actual research publication}}\n')
    (study / 'main.bbl').write_text('\\begin{thebibliography}{1}\n\\bibitem{fixture}'
        ' Example Researcher. Fictional software fixture. Test only, 2026.\n\\end{thebibliography}\n')
    manifest = {'schema_version': 1, 'main_tex': 'main.tex', 'engine': 'pdflatex',
                'files': ['main.tex', 'references.bib', 'main.bbl'],
                'authors': [{'name': 'Example Researcher', 'affiliation': 'Fictional Laboratory'}],
                'human_review': ['Fictional software fixture only; inspect actual paper and policies separately.']}
    (study / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    spec = importlib.util.spec_from_file_location('arxivcheck', ROOT / 'skills/arxivchecker/scripts/arxivcheck.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    report = checker.preflight(study, manifest, output / 'build')
    if report['errors']:
        raise SystemExit('Template preflight failed; inspect the build/report.json evidence')
    pdf = output / 'build/source/main.pdf'
    result = subprocess.run(['pdftotext', '-bbox', str(pdf), '-'], check=True, capture_output=True, text=True)
    (output / 'text-bounds.xhtml').write_text(result.stdout)
    doc = ET.fromstring(result.stdout)
    pages = []
    for index, page in enumerate(doc.findall('.//{*}page'), 1):
        words = page.findall('.//{*}word')
        if not words:
            raise SystemExit('No extractable words on fixture page')
        width, height = float(page.attrib['width']), float(page.attrib['height'])
        margins = {'left': min(float(w.attrib['xMin']) for w in words),
                   'right': width - max(float(w.attrib['xMax']) for w in words),
                   'top': min(float(w.attrib['yMin']) for w in words),
                   'bottom': height - max(float(w.attrib['yMax']) for w in words)}
        pages.append({'page': index, 'size_pt': [width, height],
                      'word_bounds_margins_pt': {k: round(v, 3) for k, v in margins.items()},
                      'within_local_72pt_text_envelope_with_1pt_tolerance': min(margins.values()) >= 71})
    subprocess.run(['pdftoppm', '-scale-to', '1100', '-png', str(pdf), str(output / 'page')], check=True, capture_output=True)
    record = {'schema_version': 1, 'status': 'local-template-build-and-bounds-measured',
              'arxiv_eligibility': 'not-assessed', 'pages': pages,
              'footnote_profile': 'Starter selects 10pt/12pt leading for footnotes as a house readability choice.',
              'limits': 'Word bounds only, with a local rounding/ink-overhang tolerance; not every PDF object, policy compliance, accessibility, science or final arXiv output. Inspect every rendered page.'}
    (output / 'layout-review.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
