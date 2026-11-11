import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
from key import key
A = '/home/claude/lucky/site/assets'
badge = Image.open('badge.png').convert('RGBA')
def coeffs(dst, src):
    M = []
    for (x, y), (u, v) in zip(dst, src):
        M += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
    return np.linalg.solve(np.array(M, float), np.array(src, float).reshape(8))
def bil(q, u, v):
    tl, tr, br, bl = [np.array(p, float) for p in q]
    return tuple((tl * (1 - u) + tr * u) * (1 - v) + (bl * (1 - u) + br * u) * v)
def stamp(im, quad, strength=.9):
    w, h = badge.size
    warped = badge.transform(im.size, Image.PERSPECTIVE, coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)
    a = np.asarray(im).astype(float); l = np.asarray(warped).astype(float)
    m = l[..., 3:4] / 255 * strength * ndi.gaussian_filter((a[..., :3].mean(axis=2) > 105).astype(float), .7)[..., None]
    a[..., :3] = a[..., :3] * (1 - m) + (a[..., :3] * l[..., :3] / 255) * m
    return Image.fromarray(a.astype('uint8'))
sheet, objs = key('/mnt/user-data/uploads/a48bb885-image.png'); arr = np.asarray(sheet).copy()
LAB, _ = ndi.label(arr[..., 3] > 100)
def obj(i):
    ids = np.bincount(LAB[objs[i]].ravel()); ids[0] = 0; keep = ndi.binary_dilation(LAB == ids.argmax(), iterations=2)
    a = arr.copy(); a[~keep, 3] = 0; return Image.fromarray(a)
q = lambda f, u0, v0, u1, v1: [bil(f, u0, v0), bil(f, u1, v0), bil(f, u1, v1), bil(f, u0, v1)]
top_o = [(428, 262), (665, 330), (468, 590), (197, 495)]; top_c = [(968, 297), (1222, 368), (968, 730), (668, 617)]
to = stamp(obj(0), q(top_o, .16, .2, .84, .72)); tc = stamp(obj(1), q(top_c, .15, .27, .85, .7))
SZ = (700, 740)
def canvas(im, centre):
    c = Image.new('RGBA', SZ, (0, 0, 0, 0)); c.paste(im, (350 - centre[0], 385 - centre[1])); return c
o_c, c_c = (349, 595), (945, 588)
t_open, t_closed = canvas(to, o_c), canvas(tc, c_c)
sh = lambda pts: [(x + 350 - o_c[0], y + 385 - o_c[1]) for x, y in pts]
m = Image.new('L', SZ, 0); d = ImageDraw.Draw(m)
d.polygon(sh([(0, 663), (38, 678), (303, 785), (465, 592), (520, 527), (700, 527), (700, 1254), (0, 1254)]), fill=255)   # front + right walls of the tray
d.polygon(sh([(150, 479), (197, 495), (468, 590), (520, 527), (700, 527), (700, 0), (150, 0)]), fill=255)             # the sleeve, which the food slides under
m = m.filter(ImageFilter.GaussianBlur(.8))
front = t_open.copy(); front.putalpha(Image.fromarray((np.asarray(front)[..., 3].astype(float) * np.asarray(m) / 255).astype('uint8')))
for n, im in (('tray-open', t_open), ('tray-closed', t_closed), ('tray-front', front)): im.save(f'{A}/{n}.webp', quality=88, method=6)
P = Image.new('RGB', (2100, 740), '#1F7A5C')
food = Image.open('cut/salmon-nigiri.png').resize((300, 300)); demo = t_open.copy(); demo.alpha_composite(food, (236 - 150, 445 - 150)); demo.alpha_composite(front)
for i, im in enumerate((t_open, demo, t_closed)): P.paste(im, (i * 700, 0), im)
P.resize((1050, 370)).save('tray-preview.png')
