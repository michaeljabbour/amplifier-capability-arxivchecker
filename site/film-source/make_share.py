#!/usr/bin/env python3
"""Draw the raster companion of site/assets/social-card.svg with local Pillow.

No external services or bundled fonts. Font paths can be supplied for other OSes.
Pillow is an optional asset-production dependency, not a site-build dependency.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCALE = 2
PAPER, INK, MUTED = '#f1f5f8', '#132d43', '#4b6172'
RED, TEAL, RULE, SHADOW = '#a53839', '#175f66', '#c6d3de', '#dbe5ed'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serif-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Georgia.ttf'))
    parser.add_argument('--sans-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Arial.ttf'))
    parser.add_argument('--bold-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/social-card.png')
    args = parser.parse_args()
    for value in (args.serif_font, args.sans_font, args.bold_font):
        if not value.is_file():
            parser.error(f'Font not found: {value}; supply an installed font path.')
    image = Image.new('RGB', (1200*SCALE, 630*SCALE), PAPER)
    draw = ImageDraw.Draw(image)

    def text(target, x, y, content, size, fill=INK, family='sans'):
        path = {'sans': args.sans_font, 'serif': args.serif_font, 'bold': args.bold_font}[family]
        target.text((x*SCALE, y*SCALE), content, font=ImageFont.truetype(str(path), size*SCALE), fill=fill, anchor='ls')

    text(draw, 75, 88, 'ArxivChecker', 25, family='bold')
    text(draw, 75, 246, 'Every claim needs', 69, family='serif')
    text(draw, 75, 325, 'a way back.', 69, family='serif')
    text(draw, 78, 435, 'Turn a finished study into a paper', 26, MUTED)
    text(draw, 78, 474, 'you can trace, rebuild and review.', 26, MUTED)
    text(draw, 78, 575, 'An independent Amplifier-compatible capability', 18, MUTED)
    panel = Image.new('RGBA', (280*SCALE, 380*SCALE), (0, 0, 0, 0))
    p = ImageDraw.Draw(panel)

    def rect(x1, y1, x2, y2, fill, outline=None):
        p.rectangle(tuple(v*SCALE for v in (x1,y1,x2,y2)), fill=fill, outline=outline, width=SCALE)

    def line(points, fill, width):
        p.line([(x*SCALE, y*SCALE) for x,y in points], fill=fill, width=width*SCALE)

    rect(5, 7, 265, 367, SHADOW)
    rect(0, 0, 260, 360, 'white', RULE)
    text(p, 28, 59, 'Claim', 28, family='serif')
    line([(30,73),(143,73)], RED, 3)
    for y, end in [(110,217),(124,217),(138,154)]:
        line([(32,y),(end,y)], SHADOW, 5)
    text(p, 30, 200, 'Metric + denominator', 19, TEAL)
    line([(130,217),(130,250)], TEAL, 2)
    line([(123,242),(130,250),(137,242)], TEAL, 2)
    text(p, 30, 285, 'Source + command', 19, TEAL)
    line([(180,320),(191,331),(219,299)], RED, 5)
    rotated = panel.rotate(-4, resample=Image.Resampling.BICUBIC, expand=True)
    image.paste(rotated, (820*SCALE, 110*SCALE), rotated)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.resize((1200,630), Image.Resampling.LANCZOS).save(args.output, optimize=True)
    print('Created 1200 x 630 original social-card.png raster companion.')


if __name__ == '__main__':
    main()
