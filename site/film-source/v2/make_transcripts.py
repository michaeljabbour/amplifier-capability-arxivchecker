#!/usr/bin/env python3
"""Full and 15 s transcripts (narration plus on-screen text), from edit/edit.json. Usage: make_transcripts.py OUTDIR"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
E = json.loads((ROOT / 'edit/edit.json').read_text()); SC = E['SC']; out = Path(sys.argv[1])
VO = {v['id']: v['text'] for v in E['vo']}
FZ, SH = E.get('freeze', [1e9, 0])
ts = lambda x: (lambda y: f'{int(y // 60):02d}:{y % 60:06.3f}')(x if x < FZ else x + SH)
SCENES = [
    ('s1', 'One result becomes a sentence', ['L1a', 'L1b'], 'Your study is done. / The system saved half the cost. (a gold thread hangs loose from the full stop) / Half of what? (in silence) / Fictional example'),
    ('s2', 'The turn', ['L2'], 'The thread pulls taut; the camera follows it down into a file card labelled results.json. Wordmark: ArxivChecker'),
    ('s3', 'The sentence gains its limits', ['L3'], 'A fictional results.json with task_set "held-out", compare "baseline", cost_scope "priced model calls" and excluded ["setup", "unpriced calls", "human review"]. Each line lights as its phrase arrives: On this held-out task set, priced model calls cost half as much as the baseline. Setup, unpriced calls and human review are excluded.'),
    ('s4', 'Draw it from the data', ['L4'], 'Rows A, B, C and D stream into bars. Row D is renamed D2 in the file ("Renamed in the file"), so its bar never arrives: "D is missing. Build stopped." D is restored, then: Then look at it. A magnifier passes over the labels. Illustration, not study data.'),
    ('s5', 'The story in order', ['L5'], 'Problem · What we built · How we tested it · What happened · Limits, each landing in a page.'),
    ('s6', 'Set it, and sort the rules', ['L6a', 'L6b', 'L6c', 'L6d'], 'LaTeX source types and compiles into a page. ARXIV POLICY: Margins of at least 1 inch (the thread measures 1 in). ARXIV RECOMMENDS: Describe each figure (the page figure is marked ALT). HOUSE STYLE: No page numbers (a page number appears, then is left off).'),
    ('s7', 'Rebuild from what you’ll send', ['L7'], 'main.tex, figures/ and references.bib are checked; drafts/ and private-data/ are struck out. An empty folder opens, the three files go in, and the paper rebuilds. LOCAL CHECK: A local check, not arXiv’s decision.'),
    ('s8', 'Hand-over', ['L8'], 'A cover sheet slides across the desk: BEFORE YOU SUBMIT. You decide. Authors and affiliations · How you disclose AI use (ARXIV POLICY) · License · Final claims, each with an empty box. A blank signature line. No promise of acceptance.'),
    ('s9', 'The takeaway', [], 'A stronger claim has clearer limits. (type only)'),
    ('s10', 'End card', [], 'ArxivChecker · Trace. Rebuild. Review. · › Use ArxivChecker on this study folder. (typed; no voice)'),
]
head = ['ArxivChecker: Trace. Rebuild. Review.', '',
        f'{E["duration"]:.0f}-second narrated launch film (v2). Voice: Veda Sky (ElevenLabs, US English, synthetic). Original score and sound effects generated with ElevenLabs.',
        'Every file, number and chart is fictional or an illustration, not a study result. ArxivChecker prepares a paper for human review; it does not submit it or promise acceptance.', '']
lines = list(head)
for k, title, ids, screen in SCENES:
    lines += [f'{ts(SC[k])}  {title}', f'On screen: {screen}']
    if ids: lines.append('Narration: ' + ' '.join(VO[i] for i in ids))
    lines.append('')
lines.append('The narrator says ArxivChecker as “Archive Checker” and arXiv as “archive”.')
(out / 'arxivchecker-film-v2-transcript.txt').write_text('\n'.join(lines) + '\n')
short = ['ArxivChecker: Trace. Rebuild. Review.', '', '14.5-second cut of the v2 launch film. Fictional example; not a study result.', '',
         '00:00  On screen: The system saved half the cost. A gold thread hangs loose from the full stop.', f'       Narration: {VO["L1b"]}',
         '00:03  On screen: The thread pulls taut into results.json. Wordmark: ArxivChecker.', '       Narration: starts with the evidence, not the old draft’s numbers.',
         '00:06  On screen: The sentence rebuilds as: On this held-out task set, priced model calls cost half as much as the baseline. Setup, unpriced calls and human review are excluded.', f'       Narration: {VO["L3"]}',
         '00:12  On screen: ArxivChecker · Trace. Rebuild. Review. (no voice)', '']
(out / 'arxivchecker-film-v2-15s-transcript.txt').write_text('\n'.join(short).rstrip() + '\n')
print('transcripts written')
