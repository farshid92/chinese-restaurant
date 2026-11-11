"""Drive the page in headless Chrome at desktop and phone sizes and save screenshots to out/.
Usage: python3 tools/shot.py   (needs playwright and a Chrome binary; Google Fonts are served from tools' font cache if present)"""
import asyncio, glob, os
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = '/home/claude/lucky/fonts'
os.makedirs(f'{ROOT}/out', exist_ok=True)
def font(n):
    m = glob.glob(f'{FONTS}/fontsource-{n}-*/package/files/{n}-latin-400-normal.woff2'); return m[0] if m else None
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required'])
        for name, w, h, mob in (('desk', 1440, 820, False), ('phone', 390, 844, True)):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, has_touch=mob, is_mobile=mob)
            pg = await ctx.new_page(); errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
            css = ''.join(f"@font-face{{font-family:'{fam}';src:url(https://local.test/{n}.woff2)}}" for fam, n in (('Limelight', 'limelight'), ('Bungee', 'bungee'), ('DM Mono', 'dm-mono')))
            await pg.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(body=css, content_type='text/css'))
            await pg.route('**/local.test/*', lambda r: r.fulfill(path=font(r.request.url.split('/')[-1][:-6])) if font(r.request.url.split('/')[-1][:-6]) else r.abort())
            shot = lambda tag: pg.screenshot(path=f'{ROOT}/out/s_{name}_{tag}.png')
            async def tap(sel, n=0, wait=1300): await pg.locator(sel).nth(n).click(force=True); await pg.wait_for_timeout(wait)
            await pg.goto(f'file://{ROOT}/index.html'); await pg.wait_for_timeout(2600)
            await shot('0')
            await tap('.cat', 4, 1200)
            for k in range(4): await tap('.dish', 0, 60)          # four quick taps on the same sushi
            await pg.wait_for_timeout(350); await shot('fly'); await pg.wait_for_timeout(1600)
            await tap('.dish', 2)
            await tap('.cat', 0, 1200); await tap('.dish', 1); await tap('.cat', 1, 1200); await tap('.dish', 0)
            await tap('.cat', 6, 1200); await tap('.dish', 1, 2700); await tap('.dish', 1, 1200)
            await shot('1')
            if await pg.locator('#infoBtn').count():
                await tap('#infoBtn', 0, 600); await shot('info'); await tap('#infoClose', 0, 400)
            if mob: await tap('#barInfo', 0, 400); await shot('bill'); await pg.locator('.step button[data-d="1"]').nth(2).click(force=True); await pg.wait_for_timeout(300); await pg.mouse.click(10, 60); await pg.wait_for_timeout(400)
            else: await pg.locator('.step button[data-d="-1"]').nth(0).click(force=True); await pg.wait_for_timeout(500)
            await shot('2')
            await pg.locator('[data-pack]:visible').click(force=True); await pg.wait_for_timeout(2800)
            await pg.click('.go:visible'); await pg.wait_for_timeout(300); await shot('3')
            await pg.fill('#who', 'Mei Lin'); await pg.fill('#tel', '555 0142'); await pg.fill('#addr', '12 Jade Lane'); await pg.click('.go:visible'); await pg.wait_for_timeout(800)
            await shot('4')
            print(name, 'gsap', await pg.evaluate('!!window.gsap'), 'cart', await pg.evaluate('JSON.stringify(state.cart)'), 'errors:', errs[:5]); await ctx.close()
        await b.close()
asyncio.run(main())
