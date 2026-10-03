"""
Small vector drawing kit for card illustrations.

Shapes are drawn in "units" on a 160 x 100 stage (x right, y down) at 4x resolution and
downscaled at the end, which gives smooth, painted-looking edges. Shapes are grouped in parts;
each part gets its own dark outline and soft top-left lighting, so overlapping limbs stay readable.
"""
import math
from contextlib import contextmanager

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

STAGE_W, STAGE_H = 160, 100
SS = 4
OUTLINE = (34, 26, 30)


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def lighter(c, t=0.35):
    return mix(c, (255, 255, 255), t)


def darker(c, t=0.35):
    return mix(c, (0, 0, 0), t)


def bezier(points, n=40):
    """Points along a Bezier curve of any degree."""
    out = []
    for i in range(n + 1):
        t = i / n
        pts = list(points)
        while len(pts) > 1:
            pts = [(pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t) for j in range(len(pts) - 1)]
        out.append(pts[0])
    return out


class Sprite:
    def __init__(self, width_px, height_px):
        self.w, self.h = width_px * SS, height_px * SS
        self.k = min(self.w / STAGE_W, self.h / STAGE_H)
        self.ox = (self.w - STAGE_W * self.k) / 2
        self.oy = (self.h - STAGE_H * self.k) / 2
        self.out_size = (width_px, height_px)
        self.parts = []
        self._current = None
        self._new_part(outline=True, shade=True)

    # ------------------------------------------------------------ parts

    def _new_part(self, outline, shade):
        layer = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        self._current = {"img": layer, "draw": ImageDraw.Draw(layer), "outline": outline, "shade": shade}
        self.parts.append(self._current)

    @contextmanager
    def part(self, outline=True, shade=True):
        self._new_part(outline, shade)
        yield self
        self._new_part(True, True)

    # ------------------------------------------------------------ coordinates

    def P(self, x, y):
        return (self.ox + x * self.k, self.oy + y * self.k)

    def S(self, v):
        return v * self.k

    @property
    def d(self):
        return self._current["draw"]

    # ------------------------------------------------------------ shapes

    def ellipse(self, cx, cy, rx, ry, col, rot=0.0):
        if rot == 0:
            x0, y0 = self.P(cx - rx, cy - ry)
            x1, y1 = self.P(cx + rx, cy + ry)
            self.d.ellipse((x0, y0, x1, y1), fill=(*col, 255))
            return
        a = math.radians(rot)
        pts = []
        for i in range(64):
            t = i / 64 * math.tau
            x, y = rx * math.cos(t), ry * math.sin(t)
            pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
        self.poly(pts, col)

    def circle(self, cx, cy, r, col):
        self.ellipse(cx, cy, r, r, col)

    def poly(self, pts, col):
        self.d.polygon([self.P(x, y) for x, y in pts], fill=(*col, 255))

    def rect(self, x0, y0, x1, y1, col):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)

    def line(self, pts, col, w=1.0):
        px = [self.P(x, y) for x, y in pts]
        width = max(1, round(self.S(w)))
        self.d.line(px, fill=(*col, 255), width=width, joint="curve")
        r = width / 2
        for x, y in (px[0], px[-1]):
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=(*col, 255))

    def curve(self, ctrl, col, w=1.0):
        self.line(bezier(ctrl), col, w)

    def tube(self, ctrl, r0, r1, col, n=60):
        """A thick body along a curve, tapering from r0 to r1 (tails, serpents, necks)."""
        pts = bezier(ctrl, n)
        for i, (x, y) in enumerate(pts):
            r = r0 + (r1 - r0) * i / n
            self.circle(x, y, r, col)

    def tri(self, a, b, c, col):
        self.poly([a, b, c], col)

    def spiral(self, cx, cy, r, turns, col, w=1.0):
        pts = []
        steps = int(60 * turns)
        for i in range(steps + 1):
            t = i / steps
            ang = t * turns * math.tau
            rr = r * t
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        self.line(pts, col, w)

    def star(self, cx, cy, r_out, r_in, col, points=5, rot=-90.0):
        pts = []
        for i in range(points * 2):
            r = r_out if i % 2 == 0 else r_in
            a = math.radians(rot + i * 180 / points)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.poly(pts, col)

    def bolt(self, x, y, size, col, rot=0.0):
        base = [(0, -1), (0.45, -1), (0.15, -0.15), (0.55, -0.15), (-0.1, 1), (0.08, 0.1), (-0.35, 0.1)]
        a = math.radians(rot)
        pts = [(x + size * (px * math.cos(a) - py * math.sin(a)), y + size * (px * math.sin(a) + py * math.cos(a))) for px, py in base]
        self.poly(pts, col)

    def flame(self, cx, cy, size, rot=0.0):
        """A three-tone flame, tip pointing up (rot rotates it)."""
        a = math.radians(rot)

        def tear(scale, col):
            # round bottom, pointed tip at the top
            local = [(0.0, -scale)]
            for deg in range(-25, 206, 10):
                t = math.radians(deg)
                local.append((0.48 * scale * math.cos(t), 0.2 * scale + 0.48 * scale * math.sin(t)))
            pts = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in local]
            self.poly(pts, col)

        tear(size, (230, 70, 40))
        tear(size * 0.72, (250, 150, 40))
        tear(size * 0.42, (255, 230, 110))

    def eye(self, cx, cy, r=2.6, iris=(25, 20, 30), sclera=True, look=(0.0, 0.0), squint=False):
        if squint:
            self.line([(cx - r, cy), (cx, cy - r * 0.5), (cx + r, cy)], OUTLINE, 0.9)
            return
        if sclera:
            self.ellipse(cx, cy, r, r * 1.15, (250, 250, 250))
            self.ellipse(cx + look[0] * r * 0.4, cy + look[1] * r * 0.4, r * 0.62, r * 0.78, iris)
        else:
            self.ellipse(cx, cy, r * 0.7, r * 0.85, iris)
        self.circle(cx - r * 0.25, cy - r * 0.35, r * 0.25, (255, 255, 255))

    def eyes(self, cx, cy, gap, r=2.6, **kw):
        self.eye(cx - gap / 2, cy, r, **kw)
        self.eye(cx + gap / 2, cy, r, **kw)

    def smile(self, cx, cy, w, col=OUTLINE, lw=0.8, depth=1.5):
        self.curve([(cx - w, cy), (cx, cy + depth * 2), (cx + w, cy)], col, lw)

    def shadow(self, cx, cy, rx, ry=None):
        with self.part(outline=False, shade=False):
            x0, y0 = self.P(cx - rx, cy - (ry or rx * 0.18))
            x1, y1 = self.P(cx + rx, cy + (ry or rx * 0.18))
            self.d.ellipse((x0, y0, x1, y1), fill=(0, 0, 0, 90))

    # ------------------------------------------------------------ render

    def render(self) -> Image.Image:
        out = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        outline_px = max(3, round(self.k * 1.1))
        for part in self.parts:
            img = part["img"]
            alpha = img.getchannel("A")
            if alpha.getbbox() is None:
                continue
            if part["shade"]:
                img = _shade(img)
            if part["outline"]:
                grown = alpha.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(outline_px * 2 + 1))
                ring = Image.new("RGBA", img.size, (*OUTLINE, 0))
                ring.putalpha(grown)
                out.alpha_composite(ring)
            out.alpha_composite(img)
        return out.resize(self.out_size, Image.LANCZOS)


def _shade(img: Image.Image) -> Image.Image:
    """Soft light from the top left, shadow towards the bottom right, inside the part's own bounds."""
    arr = np.asarray(img).astype(np.float32)
    alpha = arr[..., 3]
    ys, xs = np.nonzero(alpha > 0)
    if len(xs) == 0:
        return img
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    h, w = alpha.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = np.clip((xx - x0) / max(x1 - x0, 1), 0, 1)
    v = np.clip((yy - y0) / max(y1 - y0, 1), 0, 1)
    t = (u * 0.35 + v * 0.65)              # 0 at top left, 1 at bottom right
    light = np.clip(0.22 - t * 0.55, -0.30, 0.22)[..., None]
    rgb = arr[..., :3]
    rgb = np.where(light > 0, rgb + (255 - rgb) * light, rgb * (1 + light))
    arr[..., :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")
