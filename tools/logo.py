import glob, math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

F = '/home/claude/lucky/fonts'
OUT = '/home/claude/lucky/out'
os.makedirs(OUT, exist_ok=True)
PAPER, RED, JADE, GOLD, INK = '#F3E6CC', '#D7332A', '#1F7A5C', '#E3A72F', '#1C1A17'


def load(name):
    return TTFont(glob.glob(f'{F}/fontsource-{name}-*/package/files/{name}-latin-400-normal.woff')[0])


def load_cjk(name, ch):
    for p in sorted(glob.glob(f'{F}/fontsource-{name}-*/package/files/*400-normal.woff')):
        f = TTFont(p)
        if ord(ch) in f.getBestCmap():
            return f
    raise SystemExit(f'no glyph {ch} in {name}')


def glyph(font, ch, size, tx=0, ty=0, rot=0):
    """Return (path d, advance) for one char; origin at baseline-left, rotated by rot degrees about origin then moved."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    g = cmap[ord(ch)]
    s = size / font['head'].unitsPerEm
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    # font units (y up) -> svg (y down), scale, rotate, translate
    t = (s * c, s * sn, s * sn, -s * c, tx, ty)
    pen = SVGPathPen(gs)
    gs[g].draw(TransformPen(pen, t))
    return pen.getCommands(), gs[g].width * s


def width(font, text, size, ls=0):
    return sum(glyph(font, ch, size)[1] + ls for ch in text) - ls


def line(font, text, size, x, y, fill, anchor='middle', ls=0):
    w = width(font, text, size, ls)
    cx = x - w / 2 if anchor == 'middle' else x - w if anchor == 'end' else x
    d = []
    for ch in text:
        p, adv = glyph(font, ch, size, cx, y)
        d.append(p)
        cx += adv + ls
    return f'<path fill="{fill}" d="{" ".join(d)}"/>'


def arc(font, text, size, cx, cy, r, fill, ls=0, bottom=False):
    w = width(font, text, size, ls)
    pos = -w / 2
    d = []
    for ch in text:
        adv = glyph(font, ch, size)[1]
        a = (pos + adv / 2) / r  # radians at glyph centre
        if bottom:
            x, y, rot = cx + r * math.sin(a), cy + r * math.cos(a), -math.degrees(a)
        else:
            x, y, rot = cx + r * math.sin(a), cy - r * math.cos(a), math.degrees(a)
        x -= adv / 2 * math.cos(math.radians(rot))
        y -= adv / 2 * math.sin(math.radians(rot))
        d.append(glyph(font, ch, size, x, y, rot)[0])
        pos += adv + ls
    return f'<path fill="{fill}" d="{" ".join(d)}"/>'


def steam(x, y, h, color, w=7):
    out = ''
    for dx, k in ((-34, 0.8), (0, 1.0), (34, 0.8)):
        hh = h * k
        out += (f'<path d="M{x+dx},{y} c-16,{-hh*0.25} 16,{-hh*0.45} 0,{-hh*0.7} c-10,{-hh*0.15} 4,{-hh*0.24} 6,{-hh*0.3}" '
                f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
    return out


def lid_top(cx, cy, r, weave, rim, base):
    """Bamboo steamer lid seen from above."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{rim}"/><circle cx="{cx}" cy="{cy}" r="{r*0.86}" fill="{base}"/>'
    s += f'<clipPath id="lc{cx}{cy}"><circle cx="{cx}" cy="{cy}" r="{r*0.86}"/></clipPath><g clip-path="url(#lc{cx}{cy})" stroke="{weave}" stroke-width="{r*0.035}">'
    step = r * 0.2
    n = int(r / step) + 1
    for i in range(-n, n + 1):
        s += f'<line x1="{cx+i*step}" y1="{cy-r}" x2="{cx+i*step}" y2="{cy+r}"/>'
        s += f'<line x1="{cx-r}" y1="{cy+i*step}" x2="{cx+r}" y2="{cy+i*step}" stroke-dasharray="{step} {step}" stroke-dashoffset="{(i%2)*step}"/>'
    s += '</g>'
    return s


def svg(name, w, h, body, bg=None):
    r = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{r}{body}</svg>'
    open(f'{OUT}/{name}.svg', 'w').write(s)
    return body


deco, slim, block = load('limelight'), load('poiret-one'), load('bungee')
fu = load_cjk('ma-shan-zheng', '福')
dim = load_cjk('ma-shan-zheng', '点')
xin = load_cjk('ma-shan-zheng', '心')


def seal(x, y, s, bg=RED, fg=PAPER):
    p, adv = glyph(fu, '福', s * 0.8, x + s * 0.1, y + s * 0.78)
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.12}" fill="{bg}"/><path fill="{fg}" d="{p}"/>'


# ---------- A: round seal badge ----------
def logo_a():
    c = 300
    b = f'<circle cx="{c}" cy="{c}" r="285" fill="{RED}"/>'
    b += f'<circle cx="{c}" cy="{c}" r="268" fill="none" stroke="{PAPER}" stroke-width="4"/>'
    b += f'<circle cx="{c}" cy="{c}" r="150" fill="none" stroke="{PAPER}" stroke-width="4"/>'
    b += arc(deco, 'LUCKY LID', 80, c, c, 182, PAPER, ls=6)
    b += arc(block, 'DIM SUM HOUSE', 30, c, c, 236, GOLD, ls=7, bottom=True)
    for sx in (-1, 1):
        b += f'<circle cx="{c+sx*212}" cy="{c+52}" r="9" fill="{GOLD}"/>'
    b += lid_top(c, c, 132, RED, GOLD, PAPER)
    b += f'<circle cx="{c}" cy="{c}" r="62" fill="{RED}"/><circle cx="{c}" cy="{c}" r="62" fill="none" stroke="{GOLD}" stroke-width="5"/>'
    p, _ = glyph(fu, '福', 92, c - 46, c + 32)
    b += f'<path fill="{PAPER}" d="{p}"/>'
    return svg('logo-a-seal', 600, 600, b)


# ---------- B: stacked wordmark with lifting lid ----------
def logo_b(ink=INK, name='logo-b-wordmark'):
    b = ''
    b += steam(300, 150, 120, JADE, 9)
    # lid (side view): dome + rim + knob
    b += f'<path d="M150,236 Q300,120 450,236 Z" fill="{RED}"/>'
    b += f'<rect x="138" y="232" width="324" height="20" rx="10" fill="{GOLD}"/>'
    b += f'<rect x="278" y="150" width="44" height="18" rx="9" fill="{GOLD}"/>'
    b += line(deco, 'LUCKY', 150, 300, 400, ink, ls=4)
    b += line(deco, 'LID', 150, 262, 540, ink, ls=10)
    b += seal(410, 432, 108)
    return svg(name, 600, 600, b)


# ---------- C: matchbox label ----------
def logo_c():
    W, H = 600, 760
    b = f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="26" fill="{PAPER}" stroke="{INK}" stroke-width="8"/>'
    b += f'<rect x="30" y="30" width="{W-60}" height="{H-60}" rx="14" fill="none" stroke="{RED}" stroke-width="4"/>'
    cx, cy = 300, 430
    b += f'<clipPath id="sun"><rect x="34" y="150" width="{W-68}" height="440"/></clipPath><g clip-path="url(#sun)">'
    for i in range(24):
        a0, a1 = math.radians(i * 15 - 3.2), math.radians(i * 15 + 3.2)
        b += (f'<path d="M{cx},{cy} L{cx+600*math.cos(a0):.1f},{cy+600*math.sin(a0):.1f} '
              f'L{cx+600*math.cos(a1):.1f},{cy+600*math.sin(a1):.1f} Z" fill="{GOLD}"/>')
    b += f'<circle cx="{cx}" cy="{cy}" r="150" fill="{RED}"/></g>'
    # banner
    b += f'<clipPath id="inner"><rect x="30" y="30" width="{W-60}" height="{H-60}" rx="14"/></clipPath>'
    b += f'<rect x="30" y="30" width="{W-60}" height="122" fill="{RED}" clip-path="url(#inner)"/>'
    b += line(deco, 'LUCKY LID', 86, 300, 122, PAPER, ls=4)
    # steamer: two tiers + lifted lid
    for i, y in enumerate((470, 410)):
        b += f'<rect x="190" y="{y}" width="220" height="58" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
        b += f'<line x1="190" y1="{y+20}" x2="410" y2="{y+20}" stroke="{INK}" stroke-width="5"/>'
        b += f'<line x1="190" y1="{y+38}" x2="410" y2="{y+38}" stroke="{INK}" stroke-width="5"/>'
        b += f'<rect x="286" y="{y+12}" width="28" height="34" rx="4" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'
    b += steam(300, 392, 86, PAPER, 9)
    b += f'<g transform="rotate(-10 300 300)"><path d="M186,318 Q300,236 414,318 Z" fill="{PAPER}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    b += f'<rect x="176" y="312" width="248" height="18" rx="9" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
    b += f'<rect x="282" y="252" width="36" height="16" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="5"/></g>'
    # side characters
    for ch, f, y in (('点', dim, 372), ('心', xin, 452)):
        for x in (62, 478):
            p, _ = glyph(f, ch, 60, x, y)
            b += f'<path fill="{INK}" d="{p}"/>'
    # footer
    b += f'<rect x="30" y="590" width="{W-60}" height="140" fill="{INK}" clip-path="url(#inner)"/>'
    b += line(block, 'DIM SUM HOUSE', 40, 300, 652, GOLD, ls=5)
    b += line(slim, 'STEAMED TO ORDER', 30, 300, 702, PAPER, ls=8)
    return svg('logo-c-matchbox', W, H, b)


a, bm, c = logo_a(), logo_b(), logo_c()
# small-size mark (favicon / stamp)
svg('mark-fu-seal', 200, 200, seal(10, 10, 180))
# comparison sheet
sheet = f'<rect width="1960" height="860" fill="#E9DCC0"/>'
sheet += f'<g transform="translate(40,130)">{a}</g>'
sheet += f'<g transform="translate(680,130)"><rect width="600" height="600" fill="{PAPER}" rx="20"/>{bm}</g>'
sheet += f'<g transform="translate(1320,50)">{c}</g>'
for i, t in enumerate(('A  SEAL', 'B  WORDMARK', 'C  MATCHBOX')):
    sheet += line(block, t, 34, 340 + i * 640, 840 if i < 2 else 845, INK, ls=3)
svg('logo-options', 1960, 860, sheet)
print(os.listdir(OUT))
