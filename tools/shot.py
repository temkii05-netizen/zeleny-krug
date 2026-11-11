"""Скриншоты HTML-страниц через headless Chrome. usage: shot.py file.html out.png width [height|full]"""
import sys, asyncio
from playwright.async_api import async_playwright


async def main(html, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": w, "height": h if h else 900}, device_scale_factor=float(sys.argv[5]) if len(sys.argv) > 5 else 1)
        await pg.goto("file://" + html)
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=(h == 0))
        await b.close()

h = sys.argv[4]
asyncio.run(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), 0 if h == "full" else int(h)))
