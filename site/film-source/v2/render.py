#!/usr/bin/env python3
"""Render web/index.html frame by frame into a lossless-ish H.264 picture track (Sizzle 7)."""
import sys, json, base64, asyncio, subprocess
from playwright.async_api import async_playwright
out, f0, f1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
async def main():
    ff = subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate','30','-c:v','png','-i','-',
        '-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','slow','-crf','15','-g','60',
        '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709', out], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1920,'height':1080})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8771/index.html')
        for f in range(f0, f1):
            url = await pg.evaluate(f'window.renderAt({f/30})')
            ff.stdin.write(base64.b64decode(url.split(',',1)[1]))
        await b.close()
    ff.stdin.close(); ff.wait(); print('rendered', out, f0, f1, 'errors', errs[:3])
asyncio.run(main())
