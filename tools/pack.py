import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
from key import key
A = '/home/claude/lucky/site/assets'
badge = Image.open('badge.png').convert('RGBA')

def coeffs(dst, src):  # perspective coefficients mapping dst quad -> src quad
    M = []
    for (x, y), (u, v) in zip(dst, src):
        M += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
    return np.linalg.solve(np.array(M, float), np.array(src, float).reshape(8))

def bil(q, u, v):
    tl, tr, br, bl = [np.array(p, float) for p in q]
    return tuple((tl * (1 - u) + tr * u) * (1 - v) + (bl * (1 - u) + br * u) * v)

def stamp(im, quad, keep_wire=True, strength=.9):
    """Multiply-print the badge onto im inside quad (TL,TR,BR,BL)."""
    w, h = badge.size
    warped = badge.transform(im.size, Image.PERSPECTIVE, coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)
    a = np.asarray(im).astype(float); l = np.asarray(warped).astype(float)
    m = l[..., 3:4] / 255 * strength
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; lum = (r + g + b) / 3
    ok = (lum > 105).astype(float)
    if keep_wire: ok *= 1 - ((r - b < 11) & (lum < 222)).astype(float)
    ok = ndi.gaussian_filter(ok, .7)[..., None]
    m = m * ok
    a[..., :3] = a[..., :3] * (1 - m) + (a[..., :3] * l[..., :3] / 255) * m
    return Image.fromarray(a.astype('uint8'))

def canvas(im, anchor, size, at):
    c = Image.new('RGBA', size, (0, 0, 0, 0)); c.paste(im, (at[0] - anchor[0], at[1] - anchor[1])); return c

# ---------------- boxes ----------------
sheet, objs = key('/mnt/user-data/uploads/960aa875-image.png')
arr = np.asarray(sheet).copy()
def obj(i):
    lab = np.zeros(arr.shape[:2], bool); s = objs[i]; lab[s] = True
    a = arr.copy(); a[~lab, 3] = 0; return Image.fromarray(a)
face_o = [(128, 640), (410, 655), (402, 975), (192, 885)]
face_c = [(697, 572), (1100, 690), (1052, 988), (783, 900)]
q = lambda f, u0, v0, u1, v1: [bil(f, u0, v0), bil(f, u1, v0), bil(f, u1, v1), bil(f, u0, v1)]
bo = stamp(obj(0), q(face_o, .2, .3, .8, .9)); bc = stamp(obj(1), q(face_c, .2, .2, .8, .86), keep_wire=False)
SZ, AT = (700, 740), (402, 730)
box_open = canvas(bo, (402, 975), SZ, AT); box_closed = canvas(bc, (1052, 988), SZ, AT)
# front overlay: everything below the front rim line (hides the bottom of the food)
poly = [(0, 488), (35, 498), (120, 520), (410, 655), (587, 497), (685, 440), (700, 430), (700, 1254), (0, 1254)]
poly = [(x, y - 245) for x, y in poly]
m = Image.new('L', SZ, 0); ImageDraw.Draw(m).polygon(poly, fill=255); m = m.filter(ImageFilter.GaussianBlur(.8))
front = box_open.copy(); front.putalpha(Image.fromarray((np.asarray(front)[..., 3].astype(float) * np.asarray(m) / 255).astype('uint8')))
for n, im in (('box-open', box_open), ('box-closed', box_closed), ('box-front', front)):
    im.save(f'{A}/{n}.webp', quality=88, method=6)

# ---------------- cups ----------------
sheet, objs = key('/mnt/user-data/uploads/fbb760b5-image.png')
arr = np.asarray(sheet).copy()
flat = lambda cx, cy, w, h: [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2 + 6), (cx + w / 2 - 6, cy + h / 2 + 4), (cx - w / 2 + 6, cy + h / 2 - 2)]
co = stamp(obj(0), flat(325, 792, 178, 170), keep_wire=False, strength=.82); cc = stamp(obj(1), flat(950, 794, 178, 170), keep_wire=False, strength=.82)
CS, CA = (560, 815), (280, 805)
cup_open = canvas(co, (322, 1012), CS, CA); cup_closed = canvas(cc, (950, 1013), CS, CA)
cup_open.save(f'{A}/cup-open.webp', quality=88, method=6); cup_closed.save(f'{A}/cup-closed.webp', quality=88, method=6)
# tea surface inside the open cup
yy, xx = np.mgrid[0:815, 0:560].astype(float)
ox, oy = 280 - 322, 805 - 1012
inner = ((xx - (323 + ox)) / 236) ** 2 + ((yy - (412 + oy)) / 167) ** 2 <= 1
liquid = ((xx - (323 + ox)) / 208) ** 2 + ((yy - (462 + oy)) / 126) ** 2 <= 1
mask = ndi.gaussian_filter((inner & liquid).astype(float), 1.2)[..., None]
base = np.asarray(cup_open).astype(float); lum = base[..., :3].mean(axis=2, keepdims=True) / 235
hl = np.exp(-(((xx - (250 + ox)) / 95) ** 2 + ((yy - (405 + oy)) / 16) ** 2))[..., None] * .55
for name, col in (('jasmine', (198, 204, 104)), ('pu-erh', (98, 38, 22)), ('oolong', (208, 136, 44)), ('chrysanthemum', (238, 210, 92))):
    tea = np.array(col, float) * (0.62 + 0.42 * np.clip(lum, 0, 1.05)); tea = tea + (255 - tea) * hl
    out = base.copy(); out[..., :3] = base[..., :3] * (1 - mask) + tea * mask
    Image.fromarray(np.clip(out, 0, 255).astype('uint8')).save(f'{A}/{name}.webp', quality=88, method=6)
# preview
P = Image.new('RGB', (700 * 3 + 560 * 3, 815), '#1F7A5C')
food = Image.open('cut/siu-mai.png').resize((410, 410))
demo = box_open.copy(); demo.alpha_composite(food, (355 - 205, 255 - 205)); demo.alpha_composite(front)
for i, im in enumerate((box_open, demo, box_closed)): P.paste(im, (i * 700, 40), im)
for i, n in enumerate(('jasmine', 'pu-erh')): im = Image.open(f'{A}/{n}.webp'); P.paste(im, (2100 + i * 560, 0), im)
P.paste(cup_closed, (2100 + 1120, 0), cup_closed); P.resize((P.width // 2, P.height // 2)).save('pack-preview.png')
