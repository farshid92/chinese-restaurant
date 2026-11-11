import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
src, names, outdir = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
DIL = int(sys.argv[4]) if len(sys.argv) > 4 else 14
OPN = int(sys.argv[5]) if len(sys.argv) > 5 else 2
WT = float(sys.argv[6]) if len(sys.argv) > 6 else 251.5
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int)
# background = near-white pixels connected to the image border
white = (a.min(axis=2) > 236) & ((a.max(axis=2) - a.min(axis=2)) < 14)
lab, n = ndi.label(white)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
idx = range(1, n + 1)
wsz = ndi.sum(np.ones_like(lab), lab, idx); wmean = ndi.mean(a.min(axis=2), lab, idx)
bg = np.isin(lab, list(border | {i + 1 for i, (z, m) in enumerate(zip(wsz, wmean)) if z > 150 and m > WT}))
fg = ndi.binary_opening(~bg, iterations=OPN)
holes, hn = ndi.label(ndi.binary_fill_holes(fg) & ~fg)
sizes = ndi.sum(np.ones_like(holes), holes, range(1, hn + 1))
fg = fg | np.isin(holes, [i + 1 for i, z in enumerate(sizes) if z < 150])
fg = ndi.binary_erosion(fg, iterations=1)
# group blobs into dishes: dilate so pieces of one dish merge
grp, k = ndi.label(ndi.binary_dilation(fg, iterations=DIL))
boxes = [s for i, s in enumerate(ndi.find_objects(grp)) if (grp[s] == i + 1).sum() > 20000]
boxes.sort(key=lambda s: (round(s[0].start / (a.shape[0] / 2)), s[1].start))
alpha = Image.fromarray((fg * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
rgba = im.copy(); rgba.putalpha(alpha)
for name, s in zip(names, boxes):
    pad = 4
    box = (max(s[1].start - pad, 0), max(s[0].start - pad, 0), s[1].stop + pad, s[0].stop + pad)
    c = rgba.crop(box); side = max(c.size)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.paste(c, ((side - c.width) // 2, (side - c.height) // 2))
    sq.save(f'{outdir}/{name}.png'); print(name, c.size)
print(len(boxes), 'dishes found')
