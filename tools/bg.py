import sys, random, math
sys.path.insert(0, '/home/claude/lucky')
import logo as L
PAPER, RED, JADE, GOLD, INK = L.PAPER, L.RED, L.JADE, L.GOLD, L.INK
A = '/home/claude/lucky/site/assets'
rnd = random.Random(8)
W, H = 2200, 1500
cj = {}
for ch in '福茶蒸包点心好吃香鲜':
    try: cj[ch] = L.load_cjk('ma-shan-zheng', ch)
    except SystemExit: pass
print('glyphs', ''.join(cj))
combos = [(RED, PAPER), (PAPER, RED), (GOLD, INK), (INK, GOLD), (JADE, PAPER), (PAPER, INK), (RED, GOLD), (PAPER, JADE)]

import base64, io
from PIL import Image
FOODS = [('siu-mai', 'SIU MAI'), ('char-siu-bao', 'CHAR SIU BAO'), ('egg-tart', 'EGG TARTS'), ('har-gow', 'HAR GOW'), ('spring-rolls', 'SPRING ROLLS'), ('jasmine', 'HOT TEA'), ('sesame-balls', 'SESAME BALLS'), ('soup-dumpling', 'SOUP DUMPLING'), ('mango-pudding', 'MANGO PUDDING'), ('bok-choy', 'FRESH GREENS')]
def food_poster(w, h, i):
    fid, cap = FOODS[i % len(FOODS)]
    im = Image.open(f'/home/claude/lucky/gen/cut/{fid}.png'); im.thumbnail((420, 420)); buf = io.BytesIO(); im.save(buf, 'PNG')
    bgc, fg, band = [(PAPER, INK, RED), (GOLD, INK, INK), ('#FBF5E6', INK, JADE)][i % 3]
    b = f'<rect width="{w}" height="{h}" fill="{bgc}"/>'
    for a in range(0, 360, 15):
        b += f'<path d="M{w/2},{h*.44} L{w/2+700*math.cos(math.radians(a-3)):.0f},{h*.44+700*math.sin(math.radians(a-3)):.0f} L{w/2+700*math.cos(math.radians(a+3)):.0f},{h*.44+700*math.sin(math.radians(a+3)):.0f}Z" fill="{fg}" opacity=".07"/>'
    sz = min(w * .7, h * .74)
    b += f'<image x="{(w-sz)/2}" y="{h*.44-sz/2}" width="{sz}" height="{sz}" href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/>'
    b += f'<rect y="{h-74}" width="{w}" height="74" fill="{band}"/>' + L.line(L.block, cap, 34, w / 2, h - 25, PAPER if band != GOLD else INK, ls=3)
    b += f'<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="none" stroke="{fg}" stroke-width="5"/>'
    return b

def poster(w, h, kind, bg, fg):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>'
    if kind == 'char':
        ch = rnd.choice(list(cj)); s = min(w, h) * 0.86
        p, adv = L.glyph(cj[ch], ch, s, (w - s) / 2, h / 2 + s * 0.36)
        b += f'<path d="{p}" fill="{fg}"/>'
    elif kind == 'two':
        chs = rnd.choice(['点心', '好吃', '香茶', '蒸包']); s = min(w / 2.1, h * 0.8)
        for i, ch in enumerate(chs):
            if ch in cj:
                p, _ = L.glyph(cj[ch], ch, s, w / 2 - s + i * s, h / 2 + s * 0.36); b += f'<path d="{p}" fill="{fg}"/>'
    elif kind == 'sun':
        for i in range(18):
            a0, a1 = math.radians(i * 20 - 5), math.radians(i * 20 + 5)
            b += f'<path d="M{w/2},{h/2} L{w/2+900*math.cos(a0):.0f},{h/2+900*math.sin(a0):.0f} L{w/2+900*math.cos(a1):.0f},{h/2+900*math.sin(a1):.0f}Z" fill="{fg}"/>'
        b += f'<circle cx="{w/2}" cy="{h/2}" r="{min(w,h)*0.26}" fill="{RED if bg != RED else INK}"/>'
    elif kind == 'stripe':
        for x in range(-int(h), int(w), 70):
            b += f'<path d="M{x},{h} L{x+h},0 L{x+h+35},0 L{x+35},{h}Z" fill="{fg}"/>'
    elif kind == 'text':
        t = rnd.choice([('DIM SUM', L.block), ('LUCKY LID', L.deco), ('YUM CHA', L.block), ('HOT TEA', L.deco), ('STEAMED', L.block), ('FRESH DAILY', L.deco)])
        s = 100
        s = s * (w * 0.84) / L.width(t[1], t[0], s, 4)
        s = min(s, h * 0.7)
        b += L.line(t[1], t[0], s, w / 2, h / 2 + s * 0.36, fg, ls=4)
        b += f'<rect x="14" y="14" width="{w-28}" height="{h-28}" fill="none" stroke="{fg}" stroke-width="6"/>'
    elif kind == 'check':
        c = 56
        for i in range(int(w / c) + 1):
            for j in range(int(h / c) + 1):
                if (i + j) % 2: b += f'<rect x="{i*c}" y="{j*c}" width="{c}" height="{c}" fill="{fg}"/>'
    elif kind == 'dots':
        for i in range(int(w / 26) + 1):
            for j in range(int(h / 26) + 1):
                b += f'<circle cx="{i*26+(j%2)*13}" cy="{j*26}" r="{4+7*i/(w/26):.1f}" fill="{fg}"/>'
    return b

s = f'<defs><filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0.1  0 0 0 0 0.09  0 0 0 0 0.08  0 0 0 -1.1 0.62"/></filter>'
s += f'<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="7"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter></defs>'
s += f'<rect width="{W}" height="{H}" fill="{JADE}"/>'
kinds = ['char', 'char', 'two', 'sun', 'stripe', 'text', 'text', 'check', 'dots', 'char', 'text']
cells = [(x, y) for y in range(-60, H, 300) for x in range(-80, W, 400)]
rnd.shuffle(cells)
cells.sort(key=lambda c: 0 if (c[0] < 330 or c[0] > 1500 or c[1] < 150 or c[1] > 1050) else -1)
n = 0
for x, y in cells:
    w, h = rnd.randint(380, 560), rnd.randint(300, 430)
    bgc, fg = rnd.choice(combos); k = kinds[n % len(kinds)]; n += 1
    edge = x < 330 or x > 1500 or y < 150 or y > 1050
    if edge and n % 2 == 0: k = 'food'
    cid = f'c{n}'
    s += f'<g transform="translate({x+rnd.randint(-40,40)},{y+rnd.randint(-30,30)}) rotate({rnd.uniform(-7,7):.1f} {w/2} {h/2})">'
    s += f'<rect x="8" y="12" width="{w}" height="{h}" fill="#000" opacity=".3"/>'
    s += f'<clipPath id="{cid}"><rect width="{w}" height="{h}"/></clipPath><g filter="url(#rough)"><g clip-path="url(#{cid})">{food_poster(w, h, n) if k == 'food' else poster(w, h, k, bgc, fg)}</g></g></g>'
s += f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".55"/>'
open('/home/claude/lucky/out/bg.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{s}</svg>')
# title + small marks
def title(fill, shadow, name):
    t = L.line(L.deco, 'LUCKY LID', 150, 500, 150, shadow, ls=6)
    b = f'<g transform="translate(7,8)">{t}</g>' + L.line(L.deco, 'LUCKY LID', 150, 500, 150, fill, ls=6) if shadow else L.line(L.deco, 'LUCKY LID', 150, 500, 150, fill, ls=6)
    open(f'{A}/{name}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 20 1000 160">{b}</svg>')
title(PAPER, INK, 'title'); title(INK, None, 'title-ink')
open(f'{A}/seal.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{L.seal(10, 10, 180)}</svg>')
