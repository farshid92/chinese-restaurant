import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
def key(src):
    a = np.asarray(Image.open(src).convert('RGB')).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = np.maximum(r, b)
    alpha = 1 - np.clip((g - m - 25) / 95, 0, 1)
    g2 = np.minimum(g, m + 6)                       # despill
    out = np.dstack([r, np.where(alpha < 1, g2, g), b, alpha * 255]).astype('uint8')
    solid = alpha > 0.5
    lab, n = ndi.label(ndi.binary_dilation(solid, iterations=6))
    objs = [s for i, s in enumerate(ndi.find_objects(lab)) if (lab[s] == i + 1).sum() > 30000]
    objs.sort(key=lambda s: s[1].start)
    return Image.fromarray(out), objs
if __name__ == '__main__':
    for src, tag in ((sys.argv[1], 'box'), (sys.argv[2], 'cup')):
        im, objs = key(src); im.save(f'{tag}-keyed.png')
        print(tag, [(s[1].start, s[0].start, s[1].stop, s[0].stop) for s in objs])
        g = Image.new('RGB', im.size, '#1F7A5C'); g.paste(im, (0, 0), im)
        from PIL import ImageDraw
        d = ImageDraw.Draw(g)
        for v in range(0, 1254, 50):
            d.line((v, 0, v, 1254), fill='#ff00ff' if v % 100 == 0 else '#884488', width=1); d.line((0, v, 1254, v), fill='#ff00ff' if v % 100 == 0 else '#884488', width=1)
            if v % 100 == 0: d.text((v + 2, 2), str(v), fill='white'); d.text((2, v + 2), str(v), fill='white')
        g.crop((0, 200, 1254, 1050)).save(f'{tag}-grid.png')
