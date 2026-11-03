#!/usr/bin/env python3
"""Generate the original, silent ArxivChecker text films locally.

Optional production-only dependencies: Pillow and ffmpeg. Neither is needed to
build, view or use the website/capability. No network calls or generated speech.
Supply fonts explicitly on other platforms; the defaults are macOS system fonts.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

PAPER = '#f1f5f8'
INK = '#132d43'
MUTED = '#536879'
RED = '#a53839'
TEAL = '#175f66'
RULE = '#b9cbd7'
WHITE = '#ffffff'
WIDTH, HEIGHT = 1280, 720
SCALE = 2
SCENES = [
    ('Your study is done.\nThe paper is not.',
     'Start with the design, methods,\nraw results and draft.',
     'Inventory the study before writing.'),
    ('Every claim needs\na route to evidence.',
     'Keep the source, denominator,\nunit and cost coverage together.',
     'Trace every claim to evidence and keep its limits visible.'),
    ('Build the figure.\nThen look at it.',
     'Missing series should fail loudly.\nInspect labels, scales and panels.',
     'Rebuild figures from data, then inspect every figure.'),
    ('Tell the whole story.\nCheck every reference.',
     'Problem, design, harness, test,\nresults and limits—in that order.',
     'Explain the system and its test; verify reference details.'),
    ('Rebuild from the\nsubmission package.',
     'Check the build, fonts, filenames\nand all required source files.',
     'Test a clean build from the actual submission package.'),
    ('A person makes\nthe final call.',
     'Review authorship, AI use,\ncategory, licence and release.',
     'Human review remains essential. ArxivChecker does not guarantee acceptance.'),
]


def make_frame(index, serif, sans):
    image = Image.new('RGB', (WIDTH * SCALE, HEIGHT * SCALE), PAPER)
    d = ImageDraw.Draw(image)
    fonts = {}

    def font(size, family='sans'):
        key = (size, family)
        if key not in fonts:
            fonts[key] = ImageFont.truetype(str(serif if family == 'serif' else sans), size * SCALE)
        return fonts[key]

    def line(x1, y1, x2, y2, fill=RULE, width=2):
        d.line((x1*SCALE, y1*SCALE, x2*SCALE, y2*SCALE), fill=fill, width=width*SCALE)

    def rect(x1, y1, x2, y2, fill=WHITE, outline=RULE, width=2):
        d.rectangle((x1*SCALE, y1*SCALE, x2*SCALE, y2*SCALE), fill=fill, outline=outline, width=width*SCALE)

    def text(x, y, value, size=24, fill=INK, family='sans', spacing=12):
        d.multiline_text((x*SCALE, y*SCALE), value, font=font(size, family), fill=fill, spacing=spacing*SCALE)

    def ellipse(x1, y1, x2, y2, fill=None, outline=RED, width=3):
        d.ellipse((x1*SCALE, y1*SCALE, x2*SCALE, y2*SCALE), fill=fill, outline=outline, width=width*SCALE)

    def check(x, y):
        line(x, y+12, x+12, y+25, TEAL, 5)
        line(x+12, y+25, x+39, y-8, TEAL, 5)

    text(76, 42, 'ArxivChecker', 30, family='serif')
    text(940, 49, 'Study to paper', 21, fill=MUTED)
    line(76, 101, 1204, 101)
    for step in range(6):
        x = 76 + step * 190
        line(x, 101, min(x+174, 1204), 101, TEAL if step <= index else RULE, 5)
    title, description, _caption = SCENES[index]
    text(76, 190, title, 58, family='serif', spacing=9)
    text(80, 389, description, 27, fill=MUTED, spacing=14)
    line(76, 570, 1204, 570)
    text(80, 604, 'Trace. Rebuild. Review.', 23, fill=TEAL)
    text(930, 606, 'A silent text film', 20, fill=MUTED)

    # Each scene uses a different view of the manuscript's evidence trail.
    if index == 0:
        for x, y, title in [(840, 180, 'Design'), (890, 240, 'Methods'), (940, 300, 'Results')]:
            rect(x, y, x+226, y+174)
            text(x+20, y+18, title, 22, family='serif')
            for row in range(3):
                line(x+20, y+67+row*25, x+190-row*20, y+67+row*25)
        line(857, 490, 1150, 490, RED, 3)
        text(867, 506, 'Begin with the sources', 19, fill=RED)
    elif index == 1:
        rect(834, 172, 1184, 478)
        text(861, 192, 'Claim record', 28, family='serif')
        for row, label in enumerate(['Source', 'Denominator', 'Unit', 'Cost coverage']):
            y = 260 + row*47
            text(862, y, label, 21)
            check(1114, y)
        ellipse(845, 285, 1060, 331)
        text(862, 498, 'Keep the context attached', 19, fill=RED)
    elif index == 2:
        rect(834, 176, 1184, 489)
        text(861, 194, 'Figure review', 27, family='serif')
        line(880, 424, 880, 262, MUTED, 2)
        line(880, 424, 1140, 424, MUTED, 2)
        for x, h in [(917, 75), (978, 120), (1039, 98), (1100, 151)]:
            rect(x, 424-h, x+27, 424, TEAL, TEAL, 1)
        text(875, 447, 'Illustration, not study data', 17, fill=MUTED)
        ellipse(1065, 236, 1165, 309)
        line(1120, 306, 1145, 345, RED, 2)
    elif index == 3:
        rect(834, 164, 1184, 490)
        for row, label in enumerate(['Problem + design', 'Harness + test', 'Results + limits', 'Verified references']):
            text(860, 191+row*70, label, 23, family='serif')
            line(861, 230+row*70, 1125, 230+row*70)
        check(1123, 398)
    elif index == 4:
        rect(834, 174, 1184, 484)
        text(862, 193, 'Clean build', 29, family='serif')
        for row, label in enumerate(['Source files', 'Embedded fonts', 'Safe filenames', 'Package manifest']):
            text(864, 261+row*45, label, 20)
            check(1121, 260+row*45)
        text(868, 505, 'Test the package you will send', 17, fill=RED)
    else:
        rect(834, 174, 1184, 484)
        text(861, 197, 'Human review', 29, family='serif')
        for row, label in enumerate(['Names and responsibility', 'AI-use disclosure', 'Release decisions']):
            text(861, 273+row*58, label, 20)
        line(858, 463, 1159, 463, RED, 3)
        text(854, 503, 'No promise of arXiv acceptance', 18, fill=RED)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def write_vtt(path, scene_indices, duration):
    def timestamp(seconds):
        return f'00:{seconds//60:02d}:{seconds%60:02d}.000'
    lines = ['WEBVTT', '']
    for n, index in enumerate(scene_indices):
        lines.extend([f'{timestamp(n*duration)} --> {timestamp((n+1)*duration)}', SCENES[index][2], ''])
    path.write_text('\n'.join(lines), encoding='utf-8')


def encode(directory, scene_indices, duration, target, webm=False):
    concat = directory / ('webm.txt' if webm else target.stem+'.txt')
    lines = []
    for index in scene_indices:
        lines.extend([f"file '{(directory / f'frame-{index}.png').as_posix()}'", f'duration {duration}'])
    lines.append(f"file '{(directory / f'frame-{scene_indices[-1]}.png').as_posix()}'")
    concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    codec = ['-c:v', 'libvpx-vp9', '-crf', '37', '-b:v', '0'] if webm else ['-c:v', 'libx264', '-crf', '25', '-preset', 'slow', '-movflags', '+faststart']
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat), '-t', str(len(scene_indices)*duration), '-r', '24', '-an', *codec, '-pix_fmt', 'yuv420p', str(target)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serif-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Georgia.ttf'))
    parser.add_argument('--sans-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Arial.ttf'))
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets')
    parser.add_argument('--skip-webm', action='store_true')
    args = parser.parse_args()
    for font_path in [args.serif_font, args.sans_font]:
        if not font_path.is_file():
            parser.error(f'Font not found: {font_path}. Supply an installed font path.')
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='arxivchecker-film-') as tmp:
        directory = Path(tmp)
        for index in range(len(SCENES)):
            frame = make_frame(index, args.serif_font, args.sans_font)
            frame.save(directory / f'frame-{index}.png')
            if index == 0:
                frame.save(args.output / 'arxivchecker-film-poster.jpg', quality=93)
        encode(directory, list(range(6)), 8, args.output / 'arxivchecker-film.mp4')
        encode(directory, [0, 1, 5], 5, args.output / 'arxivchecker-film-15s.mp4')
        if not args.skip_webm:
            encode(directory, list(range(6)), 8, args.output / 'arxivchecker-film.webm', webm=True)
    write_vtt(args.output / 'arxivchecker-film.vtt', list(range(6)), 8)
    write_vtt(args.output / 'arxivchecker-film-15s.vtt', [0, 1, 5], 5)
    transcript = ['ArxivChecker: Trace. Rebuild. Review.', '', 'Silent text film. All meaning is conveyed by the on-screen text. No narration or music.', 'Figures are illustrations, not study results.', '']
    for title, description, caption in SCENES:
        transcript.extend([title.replace('\n', ' '), description.replace('\n', ' '), caption, ''])
    (args.output / 'arxivchecker-film-transcript.txt').write_text('\n'.join(transcript), encoding='utf-8')
    print('Generated original 48-second and 15-second silent films, poster, captions and transcript.')


if __name__ == '__main__':
    main()
