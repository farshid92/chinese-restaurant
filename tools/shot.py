import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--allow-file-access-from-files'])
        for name, w, h, mob in (('desk',1440,820,False),('phone',390,844,True)):
            ctx = await b.new_context(viewport={'width':w,'height':h}, device_scale_factor=1, has_touch=mob, is_mobile=mob)
            pg = await ctx.new_page(); errs=[]
            pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
            
            import glob
            def font(n): return glob.glob(f'fonts/fontsource-{n}-*/package/files/{n}-latin-400-normal.woff2')[0]
            css=''.join(f"@font-face{{font-family:'{fam}';src:url(https://local.test/{n}.woff2)}}" for fam,n in (('Limelight','limelight'),('Bungee','bungee'),('DM Mono','dm-mono')))
            await pg.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(body=css, content_type='text/css'))
            await pg.route('**/local.test/*', lambda r: r.fulfill(path=font(r.request.url.split('/')[-1][:-6])))
            await pg.goto('file:///home/claude/lucky/site/index.html'); await pg.wait_for_timeout(1500)
            print(name, 'gsap', await pg.evaluate('!!window.gsap'))
            await pg.screenshot(path=f'out/s_{name}_0.png')
            async def tap(sel, n=0, wait=1400): await pg.locator(sel).nth(n).click(force=True); await pg.wait_for_timeout(wait)
            await tap('.cat', 4, 1200)                      # sushi only, several of the same
            for k in range(3): await tap('.dish', 0)
            await tap('.dish', 2); await tap('.dish', 2)
            await pg.screenshot(path=f'out/s_{name}_1.png')
            await tap('.cat', 0, 1200); await tap('.dish', 1); await tap('.cat', 1, 1200); await tap('.dish', 0)
            await tap('.cat', 6, 1200); await tap('.dish', 1, 2700); await tap('.dish', 1, 2700)
            if not mob: await pg.locator('.step button[data-d="-1"]').nth(0).click(force=True); await pg.wait_for_timeout(500)
            else:
                await pg.click('#barInfo'); await pg.wait_for_timeout(400); await pg.screenshot(path=f'out/s_{name}_bill.png'); await pg.locator('.step button[data-d="1"]').nth(2).click(force=True); await pg.wait_for_timeout(300); await pg.mouse.click(10, 60); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'out/s_{name}_2.png')
            await pg.locator('[data-pack]:visible').click(force=True); await pg.wait_for_timeout(2600)
            await pg.screenshot(path=f'out/s_{name}_3.png')
            await pg.fill('#addr','12 Jade Lane'); await pg.click('.go:visible'); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f'out/s_{name}_4.png')
            print(name, 'errors:', errs[:5]); await ctx.close()
        await b.close()
asyncio.run(main())
