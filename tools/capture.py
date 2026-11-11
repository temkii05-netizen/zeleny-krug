"""Покадровый захват video.html. usage: capture.py html outdir fps duration [only_times]"""
import sys, asyncio, os
from playwright.async_api import async_playwright


async def main(html, out, fps, dur, only):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto("file://" + html)
        # прогреть кадры талисмана
        await pg.evaluate("""()=>Promise.all([...Array(24).keys()].map(i=>new Promise(r=>{const im=new Image();im.onload=r;im.onerror=r;im.src='assets/'+String(i).padStart(3,'0')+'.png'})))""")
        await pg.wait_for_timeout(400)
        times = only if only else [i / fps for i in range(int(fps * dur))]
        for i, t in enumerate(times):
            await pg.evaluate(f"seek({t})")
            if "m3" and 9 <= t < 14.6:
                await pg.evaluate("()=>new Promise(r=>{const im=document.getElementById('m3');if(im.complete)r();else im.onload=r;})")
            name = f"{out}/f{i:04d}.jpg" if not only else f"{out}/t{t:05.2f}.jpg"
            await pg.screenshot(path=name, type="jpeg", quality=92)
        await b.close()

only = [float(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else None
asyncio.run(main(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), only))
