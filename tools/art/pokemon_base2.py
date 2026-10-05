import math

from . import pokemon_base1 as base1
from .canvas import OUTLINE, Sprite, darker, lighter
from .pokemon_base1 import BLACK, CREAM, PINK, WHITE, bird, split_ball

DRAW = {}

PURPLE = (150, 104, 184)
LEAF = (78, 160, 72)
BONE = (236, 230, 210)


def card(*numbers):
    def wrap(fn):
        for number in numbers:
            DRAW[number] = fn
        return fn
    return wrap


def fox(s: Sprite, fur, ruff, tail, ears=(1.0, 1.0)):
    s.shadow(82, 93, 30)
    tail(s)
    with s.part():
        s.ellipse(102, 86, 10, 7, darker(fur, 0.06))
    with s.part():
        s.ellipse(92, 72, 20, 15, fur)
    with s.part():
        s.tube([(72, 74), (70, 90)], 4, 3.6, fur)
        s.tube([(82, 76), (82, 90)], 4, 3.6, fur)
    ruff(s)
    with s.part():
        s.tri((56, 38), (44 - 4 * ears[0], 14 - 10 * ears[0]), (64, 32), fur)
        s.tri((70, 34), (80 + 2 * ears[1], 10 - 8 * ears[1]), (76, 40), fur)
        s.tri((54, 34), (46 - 3 * ears[0], 18 - 9 * ears[0]), (60, 32), darker(fur, 0.3))
    with s.part():
        s.ellipse(64, 46, 13, 12, fur)
        s.ellipse(54, 52, 8, 6, fur)
        s.eye(58, 44, 2.8, iris=(70, 40, 30))
        s.eye(68, 44, 2.6, iris=(70, 40, 30))
        s.circle(47, 51, 1.3, BLACK)
        s.curve([(48, 56), (52, 58), (56, 56)], OUTLINE, 0.7)


def puff(s: Sprite, r, cx=80, cy=None, ears=1.0, tuft=True, eyes_blue=True):
    cy = cy or 92 - r
    s.shadow(cx, 93, r * 0.9)
    with s.part():
        s.ellipse(cx - r * 0.45, 91, r * 0.3, r * 0.15, PINK)
        s.ellipse(cx + r * 0.45, 91, r * 0.3, r * 0.15, PINK)
    with s.part():
        e = r * 0.55 * ears
        s.tri((cx - r * 0.75, cy - r * 0.45), (cx - r * 0.75 - e * 0.4, cy - r - e), (cx - r * 0.2, cy - r * 0.85), PINK)
        s.tri((cx + r * 0.75, cy - r * 0.45), (cx + r * 0.75 + e * 0.4, cy - r - e), (cx + r * 0.2, cy - r * 0.85), PINK)
        s.tri((cx - r * 0.72, cy - r * 0.6), (cx - r * 0.75 - e * 0.3, cy - r - e * 0.7), (cx - r * 0.4, cy - r * 0.8), (70, 40, 50))
        s.tri((cx + r * 0.72, cy - r * 0.6), (cx + r * 0.75 + e * 0.3, cy - r - e * 0.7), (cx + r * 0.4, cy - r * 0.8), (70, 40, 50))
    with s.part():
        s.ellipse(cx, cy, r, r * 0.95, PINK)
    with s.part():
        s.ellipse(cx - r * 0.95, cy + r * 0.15, r * 0.18, r * 0.26, PINK, rot=-30)
        s.ellipse(cx + r * 0.95, cy + r * 0.15, r * 0.18, r * 0.26, PINK, rot=30)
    if tuft:
        with s.part(outline=False):
            s.curve([(cx - r * 0.1, cy - r * 0.9), (cx - r * 0.35, cy - r * 0.55), (cx + r * 0.05, cy - r * 0.45), (cx + r * 0.1, cy - r * 0.7)],
                    darker(PINK, 0.15), r * 0.12)
    with s.part(outline=False, shade=False):
        iris = (60, 120, 210) if eyes_blue else (40, 30, 40)
        s.eye(cx - r * 0.35, cy - r * 0.05, r * 0.22, iris=iris)
        s.eye(cx + r * 0.35, cy - r * 0.05, r * 0.22, iris=iris)
        s.smile(cx, cy + r * 0.38, r * 0.15)


def fish(s: Sprite, body, fins, marks, size=1.0):
    k = size
    with s.part(outline=False, shade=False):
        s.ellipse(80, 92, 58, 6, (184, 222, 250))
        for x in (50, 100, 122):
            s.circle(x, 30 + (x % 7) * 3, 2.2, (200, 232, 252))
    with s.part():
        s.poly([(80 + 26 * k, 56), (80 + 52 * k, 34), (80 + 46 * k, 56), (80 + 54 * k, 80)], fins)
        s.poly([(80 + 30 * k, 56), (80 + 48 * k, 42), (80 + 44 * k, 56), (80 + 50 * k, 72)], lighter(fins, 0.35))
    with s.part():
        s.poly([(70, 56 - 16 * k), (92, 56 - 30 * k), (96, 56 - 12 * k)], fins)
    with s.part():
        s.ellipse(78, 56, 30 * k, 18 * k, body)
    with s.part(outline=False):
        s.ellipse(86, 50, 10 * k, 8 * k, marks, rot=20)
        s.ellipse(72, 64, 9 * k, 6 * k, marks, rot=-10)
    with s.part():
        s.poly([(74, 62), (66, 80 * k + 4), (84, 70)], fins)
    with s.part():
        s.tri((54, 48), (32 - 6 * k, 34), (56, 42), (246, 240, 226))
    with s.part(outline=False, shade=False):
        s.eye(60, 50, 3.4 * k, iris=(60, 50, 60))
        s.ellipse(50, 60, 4, 2, (240, 140, 160))


def bell_plant(s: Sprite, cx=80, cy=40, r=12, stem=True):
    yellow = (236, 218, 86)
    if stem:
        s.shadow(cx, 93, 16)
        with s.part():
            s.curve([(cx, 86), (cx - 10, 90), (cx - 14, 92)], (220, 140, 110), 2)
            s.curve([(cx, 86), (cx + 10, 90), (cx + 14, 92)], (220, 140, 110), 2)
        with s.part():
            s.curve([(cx, 86), (cx + 6, 70), (cx - 4, 56), (cx, cy + r * 0.8)], LEAF, 2)
        with s.part():
            s.ellipse(cx - 12, 68, 11, 4, LEAF, rot=20)
            s.ellipse(cx + 14, 62, 11, 4, LEAF, rot=-25)
    with s.part():
        s.ellipse(cx, cy, r, r * 1.05, yellow)
        s.ellipse(cx - r * 0.9, cy + r * 0.25, r * 0.7, r * 0.5, yellow)
        s.ellipse(cx - r * 1.2, cy + r * 0.3, r * 0.35, r * 0.28, (200, 90, 110))
        s.eye(cx - r * 0.25, cy - r * 0.2, r * 0.2, sclera=False)


def mushroom_bug(s: Sprite, cx, cy, size, caps):
    k = size
    body = (240, 150, 70)
    s.shadow(cx, 93, 26 * k)
    with s.part():
        for i in range(3):
            x = cx - 14 * k + i * 14 * k
            s.tube([(x, cy + 6 * k), (x - 4 * k, cy + 14 * k), (x - 2 * k, 92)], 2.4 * k, 2 * k, darker(body, 0.08))
    with s.part():
        s.ellipse(cx, cy, 22 * k, 12 * k, body)
    for dx, dy, r in caps:
        with s.part():
            s.ellipse(cx + dx * k, cy + dy * k, r * k, r * 0.62 * k, (220, 66, 54))
            for sx, sy in ((-0.4, -0.2), (0.3, -0.35), (0.1, 0.1), (-0.05, -0.45), (0.55, 0.0)):
                s.circle(cx + (dx + sx * r) * k, cy + (dy + sy * r * 0.62) * k, r * 0.12 * k, (250, 222, 120))
    with s.part():
        s.tube([(cx - 18 * k, cy + 2 * k), (cx - 28 * k, cy + 4 * k), (cx - 30 * k, cy + 12 * k)], 2.8 * k, 2.2 * k, WHITE)
    with s.part(outline=False, shade=False):
        s.eye(cx - 14 * k, cy - 1 * k, 2.4 * k, iris=(250, 250, 250), sclera=False)


def monkey(s: Sprite, size=1.0, angry=False):
    k = size
    fur, limbs = (238, 220, 186), (150, 100, 70)
    cy = 92 - 26 * k
    s.shadow(80, 93, 24 * k)
    with s.part():
        s.curve([(80 + 18 * k, cy + 10 * k), (80 + 34 * k, cy + 8 * k), (80 + 36 * k, cy - 8 * k), (80 + 28 * k, cy - 12 * k)], fur, 3 * k)
    with s.part():
        s.tube([(80 - 10 * k, cy + 16 * k), (80 - 14 * k, 90)], 4 * k, 4 * k, fur)
        s.tube([(80 + 10 * k, cy + 16 * k), (80 + 14 * k, 90)], 4 * k, 4 * k, fur)
        s.ellipse(80 - 15 * k, 91, 6 * k, 3 * k, limbs)
        s.ellipse(80 + 15 * k, 91, 6 * k, 3 * k, limbs)
    with s.part():
        for i in range(14):
            a = math.radians(i * 360 / 14)
            s.circle(80 + 20 * k * math.cos(a), cy + 18 * k * math.sin(a), 6 * k, fur)
        s.ellipse(80, cy, 21 * k, 19 * k, fur)
    with s.part():
        s.tube([(80 - 18 * k, cy), (80 - 30 * k, cy - 10 * k), (80 - 32 * k, cy - 22 * k)], 3.6 * k, 3.2 * k, fur)
        s.tube([(80 + 18 * k, cy), (80 + 30 * k, cy - 8 * k), (80 + 34 * k, cy - 18 * k)], 3.6 * k, 3.2 * k, fur)
        s.circle(80 - 32 * k, cy - 24 * k, 4.5 * k, limbs)
        s.circle(80 + 34 * k, cy - 20 * k, 4.5 * k, limbs)
    with s.part():
        s.circle(80 - 18 * k, cy - 14 * k, 5 * k, fur)
        s.circle(80 + 18 * k, cy - 14 * k, 5 * k, fur)
    with s.part():
        s.ellipse(80, cy + 4 * k, 8 * k, 6 * k, (242, 180, 160))
        s.ellipse(78, cy + 4 * k, 1.2 * k, 1.8 * k, BLACK)
        s.ellipse(82, cy + 4 * k, 1.2 * k, 1.8 * k, BLACK)
    with s.part(outline=False, shade=False):
        s.eye(80 - 7 * k, cy - 6 * k, 2.4 * k)
        s.eye(80 + 7 * k, cy - 6 * k, 2.4 * k)
        brow = 2 if angry else 0
        s.line([(80 - 12 * k, cy - 11 * k - brow), (80 - 3 * k, cy - 8 * k)], OUTLINE, 1.2 * k)
        s.line([(80 + 12 * k, cy - 11 * k - brow), (80 + 3 * k, cy - 8 * k)], OUTLINE, 1.2 * k)
        s.curve([(80 - 6 * k, cy + 13 * k), (80, cy + 11 * k), (80 + 6 * k, cy + 13 * k)], OUTLINE, 0.9)


def nido(s: Sprite, body, belly, size=1.0, upright=True, spikes=True):
    k = size
    s.shadow(80, 93, 26 * k)
    with s.part():
        s.tube([(92, 80), (112, 84), (122 + 6 * k, 74)], 5 * k, 3 * k, body)
    if spikes:
        with s.part():
            for i in range(4):
                y = 46 + i * 8
                s.tri((92 + i * 2, y), (102 + i * 3, y - 6), (96 + i * 2, y + 6), darker(body, 0.25))
    if upright:
        with s.part():
            s.ellipse(70, 88, 9 * k, 6 * k, body)
            s.ellipse(92, 88, 9 * k, 6 * k, body)
        with s.part():
            s.ellipse(80, 66, 18 * k, 22 * k, body)
            s.ellipse(78, 72, 11 * k, 14 * k, belly)
            for y in (66, 74, 82):
                s.line([(72, y), (84, y)], darker(belly, 0.2), 0.7)
        with s.part():
            s.tube([(66, 58), (56, 64), (54, 72)], 4.5 * k, 4 * k, body)
            s.tube([(94, 58), (102, 64), (104, 72)], 4.5 * k, 4 * k, body)
        head = (76, 38)
    else:
        with s.part():
            for x in (62, 74, 92, 104):
                s.tube([(x, 72), (x, 90)], 4.5 * k, 4 * k, body)
        with s.part():
            s.ellipse(84, 68, 26 * k, 14 * k, body)
            for x, y in ((90, 62), (102, 66), (80, 60)):
                s.ellipse(x, y, 3, 2, darker(body, 0.3))
        head = (56, 54)
    hx, hy = head
    with s.part():
        s.ellipse(hx - 9 * k, hy - 12 * k, 5 * k, 9 * k, body, rot=-25)
        s.ellipse(hx + 9 * k, hy - 12 * k, 5 * k, 9 * k, body, rot=25)
        s.ellipse(hx - 9 * k, hy - 12 * k, 2.5 * k, 6 * k, (240, 240, 250), rot=-25)
        s.ellipse(hx + 9 * k, hy - 12 * k, 2.5 * k, 6 * k, (240, 240, 250), rot=25)
    with s.part():
        s.ellipse(hx, hy, 12 * k, 10 * k, body)
        s.ellipse(hx - 6 * k, hy + 4 * k, 7 * k, 5 * k, body)
        s.tri((hx - 2, hy - 9 * k), (hx, hy - 15 * k), (hx + 3, hy - 9 * k), WHITE)
        s.eye(hx - 3 * k, hy - 2 * k, 2.4, iris=(200, 40, 40))
        s.eye(hx + 5 * k, hy - 2 * k, 2.2, iris=(200, 40, 40))
        s.tri((hx - 10 * k, hy + 6 * k), (hx - 8 * k, hy + 9 * k), (hx - 6 * k, hy + 6 * k), WHITE)


def skull_kid(s: Sprite, size=1.0, club=False):
    k = size
    skin, belly = (180, 132, 90), (238, 222, 180)
    s.shadow(80, 93, 22 * k)
    with s.part():
        s.tube([(88, 82), (100, 86), (104, 80)], 3 * k, 2 * k, skin)
    with s.part():
        s.ellipse(72, 89, 7 * k, 4.5 * k, skin)
        s.ellipse(88, 89, 7 * k, 4.5 * k, skin)
    with s.part():
        s.ellipse(80, 74, 14 * k, 15 * k, skin)
        s.ellipse(80, 78, 9 * k, 10 * k, belly)
    with s.part():
        bx = 108 if club else 104
        s.line([(bx - 4, 82), (bx + 6, 38)], BONE, 3 * k)
        for ex, ey in ((bx - 4, 82), (bx + 6, 38)):
            s.circle(ex - 2, ey, 2.6 * k, BONE)
            s.circle(ex + 2, ey, 2.6 * k, BONE)
    with s.part():
        s.tube([(68, 66), (62, 72), (62, 78)], 3.4 * k, 3 * k, skin)
        s.tube([(92, 66), (100, 64), (104, 62)], 3.4 * k, 3 * k, skin)
    with s.part():
        s.ellipse(80, 50, 12 * k, 10 * k, skin)
        s.eye(76, 50, 2.2 * k)
        s.eye(85, 50, 2.2 * k)
    with s.part():
        s.ellipse(80, 40, 15 * k, 11 * k, BONE)
        s.tri((68, 36), (60, 22 if club else 26), (72, 32), BONE)
        s.tri((92, 36), (100, 22 if club else 26), (88, 32), BONE)
        s.ellipse(74, 42, 3.5, 2.6, (90, 80, 70))
        s.ellipse(86, 42, 3.5, 2.6, (90, 80, 70))
        s.line([(70, 48), (90, 48)], darker(BONE, 0.3), 0.8)


def drill_rhino(s: Sprite, upright=False):
    grey = (166, 160, 170)
    s.shadow(80, 93, 32)
    if upright:
        with s.part():
            s.tube([(96, 80), (120, 88), (134, 80)], 7, 4, grey)
        with s.part():
            s.ellipse(70, 88, 10, 6, grey)
            s.ellipse(92, 88, 10, 6, grey)
        with s.part():
            s.ellipse(80, 64, 18, 22, grey)
            s.ellipse(78, 70, 12, 14, (226, 220, 210))
            for y in (64, 72):
                s.line([(70, y), (86, y)], darker(grey, 0.3), 0.8)
        with s.part():
            s.tube([(64, 54), (54, 62), (50, 70)], 5, 4.5, grey)
            s.tube([(96, 54), (104, 62), (106, 70)], 5, 4.5, grey)
        with s.part():
            s.tri((80, 30), (92, 20), (88, 34), grey)
            s.ellipse(76, 36, 12, 10, grey)
            s.ellipse(64, 40, 9, 6, grey)
            s.tri((58, 34), (52, 20), (62, 32), WHITE)
            for i in range(3):
                s.line([(54 + i * 2, 24 + i * 3), (60 + i, 26 + i * 3)], darker(WHITE, 0.3), 0.6)
            s.eye(74, 34, 2.2, iris=(200, 40, 40))
            s.line([(56, 44), (64, 44)], OUTLINE, 0.8)
        return
    with s.part():
        for x in (62, 74, 98, 110):
            s.tube([(x, 72), (x, 90)], 6, 5.5, darker(grey, 0.05))
    with s.part():
        s.ellipse(88, 64, 30, 18, grey)
        for i in range(4):
            s.tri((80 + i * 9, 48), (86 + i * 9, 38), (90 + i * 9, 50), darker(grey, 0.15))
        for x in (78, 90, 102):
            s.curve([(x, 66), (x + 4, 72), (x, 78)], darker(grey, 0.3), 0.8)
    with s.part():
        s.ellipse(52, 62, 16, 12, grey)
        s.ellipse(38, 66, 9, 7, grey)
        s.tri((32, 60), (26, 44), (38, 58), WHITE)
        s.tri((46, 54), (44, 46), (50, 54), WHITE)
        s.eye(52, 60, 2.2, iris=(200, 40, 40))
        s.line([(30, 70), (40, 70)], OUTLINE, 0.8)


@card(1, 17)
def clefable(s):
    s.shadow(80, 93, 24)
    with s.part():
        s.ellipse(56, 54, 9, 14, (252, 214, 222), rot=-40)
        s.ellipse(104, 54, 9, 14, (252, 214, 222), rot=40)
        s.line([(54, 48), (60, 60)], darker(PINK, 0.2), 0.6)
        s.line([(106, 48), (100, 60)], darker(PINK, 0.2), 0.6)
    with s.part():
        s.curve([(96, 84), (110, 86), (112, 74), (104, 72)], PINK, 3)
    with s.part():
        s.tri((66, 36), (58, 8), (78, 30), PINK)
        s.tri((94, 36), (102, 8), (82, 30), PINK)
        s.tri((60, 14), (58, 8), (64, 16), (110, 70, 60))
        s.tri((100, 14), (102, 8), (96, 16), (110, 70, 60))
    with s.part():
        s.ellipse(80, 64, 22, 26, PINK)
    with s.part():
        s.ellipse(70, 90, 7, 4, PINK)
        s.ellipse(90, 90, 7, 4, PINK)
        s.tube([(60, 60), (54, 68), (54, 74)], 4, 3.6, PINK)
        s.tube([(100, 60), (106, 68), (106, 74)], 4, 3.6, PINK)
    with s.part(outline=False, shade=False):
        s.curve([(80, 40), (72, 34), (78, 28), (84, 34)], (200, 120, 130), 1.6)
        s.eye(73, 50, 2.4, squint=True)
        s.eye(87, 50, 2.4, squint=True)
        s.smile(80, 57, 3)
        s.ellipse(66, 56, 2.5, 1.4, (240, 130, 150))
        s.ellipse(94, 56, 2.5, 1.4, (240, 130, 150))


@card(2, 18)
def electrode(s):
    s.shadow(80, 93, 28)
    with s.part(outline=False, shade=False):
        for x, y, rot in ((40, 30, -30), (122, 28, 30), (128, 64, 70), (34, 66, -70)):
            s.bolt(x, y, 7, (250, 220, 70), rot=rot)
    split_ball(s, 80, 62, 29, top=(228, 60, 56), bottom=WHITE, grin=True)


def _flareon_ruff(s):
    with s.part():
        for i in range(7):
            a = math.radians(-30 + i * 30)
            s.circle(70 + 12 * math.cos(a), 60 + 10 * math.sin(a), 6, (252, 230, 150))
        s.ellipse(70, 62, 11, 10, (252, 230, 150))
        s.circle(64, 34, 5, (252, 230, 150))


def _flareon_tail(s):
    with s.part():
        s.ellipse(118, 54, 13, 17, (252, 230, 150), rot=-30)
        s.circle(124, 44, 8, (252, 230, 150))


@card(3, 19)
def flareon(s):
    fox(s, (238, 120, 56), _flareon_ruff, _flareon_tail)


def _jolteon_ruff(s):
    with s.part():
        for i in range(7):
            a = math.radians(-60 + i * 30)
            cx, cy = 70 + 6 * math.cos(a), 62 + 6 * math.sin(a)
            s.tri((cx - 4, cy), (cx + 12 * math.cos(a), cy + 12 * math.sin(a)), (cx + 4, cy), (246, 246, 240))
        s.ellipse(70, 62, 9, 8, (246, 246, 240))


def _jolteon_tail(s):
    with s.part():
        for i in range(5):
            a = math.radians(-80 + i * 20)
            s.tri((108, 70), (110 + 24 * math.cos(a), 66 + 24 * math.sin(a)), (114, 74), (250, 214, 60))
    with s.part(outline=False):
        for x in (84, 94, 104):
            s.tri((x - 4, 60), (x, 50), (x + 4, 60), (250, 214, 60))


@card(4, 20)
def jolteon(s):
    fox(s, (250, 214, 60), _jolteon_ruff, _jolteon_tail, ears=(1.4, 1.4))
    with s.part(outline=False, shade=False):
        s.bolt(130, 30, 8, (255, 246, 160), rot=15)
        s.bolt(34, 30, 6, (255, 246, 160), rot=-20)


@card(5, 21)
def kangaskhan(s):
    brown, belly = (150, 110, 80), (232, 212, 160)
    s.shadow(80, 93, 30)
    with s.part():
        s.tube([(94, 84), (122, 90), (136, 84)], 8, 4, brown)
    with s.part():
        s.ellipse(68, 88, 11, 6, brown)
        s.ellipse(94, 88, 11, 6, brown)
    with s.part():
        s.ellipse(80, 60, 22, 28, brown)
        s.ellipse(78, 68, 15, 18, belly)
    with s.part():
        s.ellipse(78, 74, 11, 8, darker(belly, 0.12))
    with s.part():
        s.ellipse(78, 66, 6, 5, brown)
        s.eye(76, 65, 1.5)
        s.eye(81, 65, 1.5)
    with s.part():
        s.ellipse(78, 75, 12, 5, belly)
    with s.part():
        s.tube([(62, 50), (52, 58), (50, 68)], 5, 4.5, brown)
        s.tube([(98, 50), (106, 58), (108, 68)], 5, 4.5, brown)
    with s.part():
        s.ellipse(70, 28, 4, 7, brown, rot=-20)
        s.ellipse(86, 26, 4, 7, brown, rot=20)
        s.ellipse(76, 36, 13, 11, brown)
        s.ellipse(66, 40, 8, 6, brown)
        s.ellipse(76, 34, 10, 4, (90, 70, 56))
        s.eye(76, 34, 2.2)
        s.circle(60, 39, 1.3, BLACK)


@card(6, 22)
def mr_mime(s):
    skin, pink, blue = (246, 236, 236), (240, 140, 160), (90, 130, 220)
    s.shadow(80, 93, 22)
    with s.part(outline=False, shade=False):
        s.rect(34, 18, 46, 86, (200, 230, 250))
    with s.part():
        s.tube([(74, 72), (70, 84), (68, 90)], 3, 2.6, skin)
        s.tube([(86, 72), (90, 84), (92, 90)], 3, 2.6, skin)
        s.ellipse(66, 91, 6, 3, blue)
        s.ellipse(94, 91, 6, 3, blue)
    with s.part():
        s.ellipse(80, 62, 14, 14, skin)
        s.circle(80, 64, 6, pink)
    with s.part():
        s.circle(66, 52, 5, pink)
        s.circle(94, 52, 5, pink)
    with s.part():
        s.tube([(66, 52), (56, 46), (50, 40)], 2.6, 2.4, skin)
        s.tube([(94, 52), (104, 58), (110, 66)], 2.6, 2.4, skin)
        for x, y in ((48, 38), (112, 68)):
            s.circle(x, y, 5, WHITE)
            for i in range(4):
                a = math.radians(-90 + i * 40 - (0 if x < 80 else 60))
                s.circle(x + 5 * math.cos(a), y + 5 * math.sin(a), 1.8, WHITE)
    with s.part():
        s.circle(70, 24, 6, blue)
        s.circle(90, 24, 6, blue)
    with s.part():
        s.circle(80, 34, 12, skin)
        s.circle(70, 40, 3, pink)
        s.circle(90, 40, 3, pink)
        s.eye(76, 32, 2.2)
        s.eye(84, 32, 2.2)
        s.ellipse(80, 40, 3, 1.6, (200, 70, 90))


@card(7, 23)
def nidoqueen(s):
    nido(s, (96, 150, 190), (236, 222, 180), size=1.1)


@card(8, 24)
def pidgeot(s):
    bird(s, (178, 124, 72), (244, 222, 172), (166, 112, 66), crest=[(230, 62, 50), (246, 196, 70), (230, 62, 50)], size=1.1)


@card(9, 25)
def pinsir(s):
    brown = (176, 140, 110)
    s.shadow(80, 93, 26)
    with s.part():
        for side in (-1, 1):
            pts = [(80 + side * 6, 40), (80 + side * 22, 26), (80 + side * 26, 8), (80 + side * 18, 4), (80 + side * 16, 18), (80 + side * 4, 30)]
            s.poly(pts, (232, 228, 214))
            for i in range(3):
                y = 10 + i * 6
                s.tri((80 + side * 17, y), (80 + side * 12, y + 2), (80 + side * 17, y + 4), (232, 228, 214))
    with s.part():
        s.ellipse(70, 89, 7, 4, brown)
        s.ellipse(90, 89, 7, 4, brown)
        s.tube([(74, 76), (70, 88)], 4, 3.5, brown)
        s.tube([(86, 76), (90, 88)], 4, 3.5, brown)
    with s.part():
        s.ellipse(80, 62, 17, 20, brown)
        for y in (56, 64, 72):
            s.line([(66, y), (94, y)], darker(brown, 0.3), 0.8)
    with s.part():
        s.tube([(64, 54), (54, 62), (52, 70)], 3.6, 3.2, brown)
        s.tube([(96, 54), (106, 62), (108, 70)], 3.6, 3.2, brown)
    with s.part():
        s.ellipse(80, 42, 12, 10, brown)
        s.line([(72, 38), (78, 41)], OUTLINE, 1.2)
        s.line([(88, 38), (82, 41)], OUTLINE, 1.2)
        s.circle(75, 42, 1.4, BLACK)
        s.circle(85, 42, 1.4, BLACK)
        for i in range(5):
            s.line([(74 + i * 3, 48), (74 + i * 3, 51)], WHITE, 0.8)


@card(10, 26)
def scyther(s):
    green, cream = (106, 186, 92), (238, 232, 190)
    s.shadow(80, 93, 26)
    with s.part():
        s.ellipse(100, 44, 20, 8, (236, 244, 250), rot=-30)
        s.ellipse(106, 54, 18, 7, (236, 244, 250), rot=-5)
    with s.part():
        s.tube([(88, 74), (98, 84), (96, 91)], 3.5, 3, green)
        s.tube([(78, 74), (74, 84), (72, 91)], 3.5, 3, green)
    with s.part():
        s.ellipse(96, 70, 16, 10, green, rot=30)
        for t in (-6, 0, 6):
            s.line([(96 + t - 3, 62 + t * 0.6), (96 + t + 3, 76 + t * 0.6)], cream, 1)
    with s.part():
        s.ellipse(78, 58, 10, 13, green)
        s.ellipse(76, 60, 6, 9, cream)
    with s.part():
        s.tube([(72, 52), (60, 56), (52, 50)], 3, 3, green)
        s.poly([(52, 50), (30, 30), (24, 36), (40, 48), (50, 56)], (236, 240, 244))
        s.tube([(84, 52), (96, 46), (104, 36)], 3, 3, green)
        s.poly([(104, 36), (124, 14), (130, 18), (116, 34), (106, 42)], (236, 240, 244))
    with s.part():
        s.ellipse(74, 36, 10, 9, green)
        s.ellipse(66, 40, 6, 5, green)
        s.tri((76, 28), (88, 18), (82, 30), green)
        s.ellipse(74, 34, 3.5, 2.6, (40, 40, 40), rot=-20)
        s.circle(73, 33, 0.9, WHITE)
        s.line([(62, 42), (68, 43)], OUTLINE, 0.7)


@card(11, 27)
def snorlax(s):
    teal, cream = (60, 100, 120), (240, 226, 190)
    s.shadow(80, 93, 40)
    with s.part():
        s.ellipse(56, 86, 12, 8, cream)
        s.ellipse(104, 86, 12, 8, cream)
        s.ellipse(56, 86, 6, 4, darker(cream, 0.12))
        s.ellipse(104, 86, 6, 4, darker(cream, 0.12))
    with s.part():
        s.ellipse(80, 62, 36, 30, teal)
        s.ellipse(80, 66, 26, 24, cream)
    with s.part():
        s.ellipse(46, 62, 8, 14, teal, rot=20)
        s.ellipse(114, 62, 8, 14, teal, rot=-20)
    with s.part():
        s.tri((62, 26), (58, 14), (70, 22), teal)
        s.tri((98, 26), (102, 14), (90, 22), teal)
        s.ellipse(80, 34, 22, 16, teal)
        s.ellipse(80, 38, 16, 11, cream)
    with s.part(outline=False, shade=False):
        s.line([(70, 34), (76, 34)], OUTLINE, 1.1)
        s.line([(84, 34), (90, 34)], OUTLINE, 1.1)
        s.curve([(72, 42), (80, 46), (88, 42)], OUTLINE, 0.9)
        s.tri((75, 43), (77, 46), (79, 43), WHITE)
        s.tri((81, 43), (83, 46), (85, 43), WHITE)
    with s.part(outline=False, shade=False):
        for i, (x, y) in enumerate(((108, 26), (116, 18), (126, 10))):
            r = 2.5 + i
            s.line([(x - r, y - r), (x + r, y - r), (x - r, y + r), (x + r, y + r)], (240, 244, 255), 0.9)


def _vaporeon_ruff(s):
    with s.part():
        for i in range(5):
            a = math.radians(-50 + i * 25)
            s.ellipse(70 + 10 * math.cos(a), 62 + 9 * math.sin(a), 7, 4, (246, 246, 232), rot=math.degrees(a))
        s.ellipse(70, 62, 9, 8, (246, 246, 232))
    with s.part():
        s.poly([(62, 34), (72, 16), (82, 22), (76, 38)], (246, 246, 232))


def _vaporeon_tail(s):
    with s.part():
        s.tube([(104, 72), (122, 70), (128, 54), (122, 40)], 6, 4, (110, 180, 220))
        s.poly([(122, 42), (110, 22), (124, 32), (138, 20), (128, 42)], (70, 120, 200))
    with s.part(outline=False):
        s.poly([(86, 58), (96, 46), (106, 60)], (70, 120, 200))


@card(12, 28)
def vaporeon(s):
    with s.part(outline=False, shade=False):
        s.ellipse(84, 93, 50, 6, (184, 222, 250))
    fox(s, (110, 180, 220), _vaporeon_ruff, _vaporeon_tail, ears=(0.6, 0.6))


@card(13, 29)
def venomoth(s):
    wing = (222, 206, 236)
    s.shadow(80, 93, 22)
    with s.part():
        s.poly([(80, 52), (36, 14), (22, 26), (30, 46), (70, 60)], wing)
        s.poly([(80, 52), (124, 14), (138, 26), (130, 46), (90, 60)], wing)
        s.poly([(78, 60), (44, 66), (40, 80), (74, 70)], lighter(wing, 0.2))
        s.poly([(82, 60), (116, 66), (120, 80), (86, 70)], lighter(wing, 0.2))
    with s.part(outline=False):
        for x, y in ((40, 28), (52, 36), (120, 28), (108, 36), (54, 72), (106, 72)):
            s.circle(x, y, 2.6, (190, 150, 220))
    with s.part():
        s.ellipse(80, 66, 7, 14, PURPLE)
        for y in (62, 68, 74):
            s.line([(74, y), (86, y)], darker(PURPLE, 0.3), 0.7)
    with s.part():
        s.curve([(76, 40), (70, 28), (64, 26)], PURPLE, 1)
        s.curve([(84, 40), (90, 28), (96, 26)], PURPLE, 1)
        s.circle(80, 46, 9, PURPLE)
        s.circle(75, 46, 3.6, (90, 140, 230))
        s.circle(85, 46, 3.6, (90, 140, 230))
        s.circle(74, 45, 1, WHITE)
        s.circle(84, 45, 1, WHITE)


@card(14, 30)
def victreebel(s):
    yellow, green = (230, 214, 84), (90, 170, 80)
    s.shadow(80, 93, 26)
    with s.part():
        s.curve([(98, 34), (124, 30), (132, 52), (118, 70)], (130, 100, 70), 2)
    with s.part():
        s.ellipse(56, 74, 16, 6, green, rot=30)
        s.ellipse(104, 74, 16, 6, green, rot=-30)
    with s.part():
        s.poly([(56, 44), (62, 80), (80, 92), (98, 80), (104, 44)], yellow)
        s.ellipse(80, 82, 18, 10, yellow)
    with s.part(outline=False):
        for x in (66, 74, 86, 94):
            s.circle(x, 70 - (x % 3), 1.8, (176, 160, 60))
    with s.part():
        s.ellipse(80, 44, 24, 10, (232, 140, 160))
        s.ellipse(80, 46, 18, 6, (140, 50, 70))
    with s.part():
        s.poly([(98, 36), (118, 14), (124, 24), (106, 40)], green)
        s.line([(100, 36), (120, 18)], darker(green, 0.3), 0.8)
    with s.part(outline=False, shade=False):
        s.eye(66, 54, 2.4)
        s.eye(94, 54, 2.4)
        s.tri((70, 41), (72, 46), (74, 41), WHITE)
        s.tri((86, 41), (88, 46), (90, 41), WHITE)


@card(15, 31)
def vileplume(s):
    blue, red = (70, 92, 170), (214, 60, 56)
    s.shadow(80, 93, 26)
    with s.part():
        s.ellipse(70, 89, 7, 4, blue)
        s.ellipse(90, 89, 7, 4, blue)
    with s.part():
        s.ellipse(80, 74, 14, 15, blue)
    with s.part():
        s.ellipse(64, 72, 4, 6, blue, rot=-20)
        s.ellipse(96, 72, 4, 6, blue, rot=20)
    with s.part(outline=False, shade=False):
        s.eye(75, 70, 2.2, iris=(200, 40, 40))
        s.eye(85, 70, 2.2, iris=(200, 40, 40))
        s.smile(80, 77, 3)
    with s.part():
        for i in range(5):
            a = math.radians(-90 + i * 72 + 36)
            s.ellipse(80 + 24 * math.cos(a), 44 + 10 * math.sin(a), 22, 12, red, rot=math.degrees(a))
        s.ellipse(80, 44, 14, 6, (110, 70, 140))
    with s.part(outline=False):
        for i in range(5):
            a = math.radians(-90 + i * 72 + 36)
            for t in (0.6, 1.15):
                s.circle(80 + 26 * t * math.cos(a), 44 + 11 * t * math.sin(a), 2.4, (250, 236, 220))


@card(16, 32)
def wigglytuff(s):
    pink = PINK
    s.shadow(80, 93, 26)
    with s.part():
        s.ellipse(68, 89, 8, 5, pink)
        s.ellipse(92, 89, 8, 5, pink)
    with s.part():
        s.tri((58, 34), (52, 6), (72, 24), pink)
        s.tri((102, 34), (108, 6), (88, 24), pink)
        s.tri((58, 26), (54, 10), (66, 22), (70, 40, 50))
        s.tri((102, 26), (106, 10), (94, 22), (70, 40, 50))
    with s.part():
        s.ellipse(80, 60, 28, 30, pink)
        s.ellipse(80, 72, 16, 13, WHITE)
    with s.part():
        s.ellipse(52, 66, 6, 9, pink, rot=-30)
        s.ellipse(108, 66, 6, 9, pink, rot=30)
    with s.part():
        s.circle(80, 32, 7, WHITE)
        s.circle(72, 34, 5, WHITE)
        s.circle(88, 34, 5, WHITE)
    with s.part(outline=False, shade=False):
        s.eye(70, 50, 4, iris=(60, 120, 210))
        s.eye(90, 50, 4, iris=(60, 120, 210))
        s.smile(80, 60, 4)


@card(33)
def butterfree(s):
    s.shadow(80, 93, 20)
    with s.part():
        s.poly([(80, 50), (40, 18), (26, 30), (34, 50), (72, 58)], WHITE)
        s.poly([(80, 50), (120, 18), (134, 30), (126, 50), (88, 58)], WHITE)
        s.poly([(78, 58), (46, 64), (44, 80), (74, 68)], WHITE)
        s.poly([(82, 58), (114, 64), (116, 80), (86, 68)], WHITE)
    with s.part(outline=False):
        s.poly([(40, 18), (26, 30), (32, 38), (44, 24)], BLACK)
        s.poly([(120, 18), (134, 30), (128, 38), (116, 24)], BLACK)
        s.poly([(46, 64), (44, 80), (50, 76)], BLACK)
        s.poly([(114, 64), (116, 80), (110, 76)], BLACK)
    with s.part():
        s.ellipse(80, 62, 7, 12, (90, 90, 170))
        s.ellipse(74, 76, 3, 4, (90, 90, 170))
        s.ellipse(86, 76, 3, 4, (90, 90, 170))
    with s.part():
        s.curve([(76, 36), (70, 24), (66, 22)], BLACK, 1)
        s.curve([(84, 36), (90, 24), (94, 22)], BLACK, 1)
        s.circle(80, 44, 9, (90, 90, 170))
        s.circle(75, 43, 4, (220, 50, 60))
        s.circle(85, 43, 4, (220, 50, 60))
        s.circle(74, 42, 1.2, WHITE)
        s.circle(84, 42, 1.2, WHITE)
        s.tri((78, 50), (80, 53), (82, 50), WHITE)


@card(34)
def dodrio(s):
    brown, neck = (170, 120, 76), (186, 140, 96)
    s.shadow(80, 93, 26)
    with s.part():
        s.line([(74, 72), (70, 90)], (230, 170, 80), 1.8)
        s.line([(88, 72), (92, 90)], (230, 170, 80), 1.8)
    with s.part():
        s.poly([(98, 62), (120, 52), (116, 62), (124, 66), (98, 70)], BLACK)
    with s.part():
        s.ellipse(82, 64, 20, 13, brown)
    for (hx, hy), (nx, ny) in (((56, 22), (74, 54)), ((80, 14), (82, 52)), ((104, 24), (90, 54))):
        with s.part():
            s.tube([(nx, ny), ((nx + hx) / 2, (ny + hy) / 2 + 4), (hx, hy + 6)], 3.4, 3, neck)
        with s.part():
            s.ellipse(hx, hy, 7, 6.5, neck)
            s.tri((hx - 4, hy - 4), (hx - 2, hy - 12), (hx + 1, hy - 5), BLACK)
            s.tri((hx - 5, hy - 1), (hx - 15, hy + 1), (hx - 5, hy + 3), (236, 214, 150))
            s.eye(hx, hy - 1, 1.8)


@card(35)
def exeggutor(s):
    trunk, belly = (196, 160, 100), (240, 222, 176)
    egg = (246, 236, 180)
    s.shadow(80, 93, 26)
    with s.part():
        s.ellipse(70, 89, 9, 5, trunk)
        s.ellipse(90, 89, 9, 5, trunk)
        s.tube([(80, 86), (80, 54)], 12, 10, trunk)
        s.ellipse(80, 72, 8, 12, belly)
    with s.part():
        for a in (-160, -125, -55, -20, -90):
            r = math.radians(a)
            s.ellipse(80 + 22 * math.cos(r), 34 + 14 * math.sin(r), 20, 5, (70, 160, 70), rot=a)
    for x, y in ((66, 38), (80, 32), (94, 38)):
        with s.part():
            s.ellipse(x, y, 9, 8, egg)
        with s.part(outline=False, shade=False):
            s.eye(x - 3, y - 1, 1.6)
            s.eye(x + 3, y - 1, 1.6)
            s.smile(x, y + 3, 2)
    with s.part():
        s.tube([(70, 62), (60, 70), (58, 76)], 4, 3.5, trunk)
        s.tube([(90, 62), (100, 70), (102, 76)], 4, 3.5, trunk)


@card(36)
def fearow(s):
    brown, cream = (168, 112, 70), (238, 214, 170)
    s.shadow(80, 93, 26)
    with s.part():
        s.poly([(78, 52), (30, 26), (22, 36), (34, 44), (24, 50), (66, 64)], brown)
        s.poly([(90, 52), (134, 22), (142, 32), (130, 40), (138, 48), (98, 64)], darker(brown, 0.1))
    with s.part():
        s.poly([(92, 66), (114, 80), (108, 86), (88, 74)], brown)
        s.ellipse(84, 62, 15, 12, brown)
        s.ellipse(80, 66, 9, 7, cream)
    with s.part():
        s.tube([(80, 56), (72, 44), (64, 36)], 5, 4.5, cream)
    with s.part():
        s.ellipse(62, 32, 8, 7, brown)
        for i in range(3):
            s.tri((66, 28), (70 + i * 4, 16 + i * 2), (70, 30), (220, 60, 50))
        s.tri((56, 30), (30, 34), (56, 36), (236, 196, 110))
        s.eye(62, 30, 2.2)
        s.line([(58, 26), (66, 28)], OUTLINE, 1)


@card(37)
def gloom(s):
    blue, leaf = (80, 100, 170), (176, 80, 50)
    s.shadow(80, 93, 22)
    with s.part():
        s.ellipse(70, 89, 7, 4, blue)
        s.ellipse(90, 89, 7, 4, blue)
    with s.part():
        s.ellipse(80, 70, 17, 18, blue)
    with s.part():
        s.ellipse(62, 70, 4, 6, blue, rot=-20)
        s.ellipse(98, 70, 4, 6, blue, rot=20)
    with s.part():
        for i, a in enumerate((-160, -120, -60, -20)):
            r = math.radians(a)
            s.ellipse(80 + 16 * math.cos(r), 50 + 10 * math.sin(r), 16, 8, leaf, rot=a + (20 if a < -90 else -20))
        s.ellipse(80, 46, 9, 6, (220, 120, 80))
    with s.part(outline=False, shade=False):
        s.eye(73, 66, 2.2, squint=True)
        s.eye(87, 66, 2.2, squint=True)
        s.ellipse(80, 76, 4, 3, (110, 50, 60))
        s.tube([(84, 78), (85, 86)], 1.2, 1.8, (180, 220, 250))


@card(38)
def lickitung(s):
    pink, cream = (236, 158, 170), (246, 226, 200)
    s.shadow(80, 93, 28)
    with s.part():
        s.tube([(98, 84), (116, 88), (124, 80)], 6, 3, pink)
    with s.part():
        s.ellipse(68, 88, 10, 6, pink)
        s.ellipse(92, 88, 10, 6, pink)
    with s.part():
        s.ellipse(82, 62, 22, 26, pink)
        s.ellipse(82, 72, 13, 13, cream)
        for y in (68, 74):
            s.line([(74, y), (90, y)], darker(cream, 0.2), 0.7)
    with s.part():
        s.tube([(62, 58), (52, 66), (52, 74)], 4.5, 4, pink)
        s.tube([(102, 58), (110, 66), (110, 74)], 4.5, 4, pink)
    with s.part():
        s.tube([(70, 50), (50, 52), (36, 64), (34, 80), (44, 84)], 4, 3.4, (226, 100, 130))
    with s.part(outline=False, shade=False):
        s.eye(78, 40, 2.6)
        s.eye(90, 40, 2.6)
        s.curve([(66, 50), (78, 54), (92, 50)], OUTLINE, 0.9)


@card(39)
def marowak(s):
    skull_kid(s, 1.15, club=True)


@card(40)
def nidorina(s):
    nido(s, (130, 190, 220), (236, 236, 240), size=0.95, upright=False)


@card(41)
def parasect(s):
    mushroom_bug(s, 84, 70, 1.15, [(4, -14, 28)])


@card(42)
def persian(s):
    cream = (240, 222, 180)
    s.shadow(84, 93, 34)
    with s.part():
        s.curve([(108, 68), (130, 64), (136, 44), (128, 34)], cream, 2.4)
    with s.part():
        s.tube([(104, 70), (110, 82), (108, 91)], 4, 3.6, darker(cream, 0.06))
        s.tube([(66, 70), (64, 82), (62, 91)], 4, 3.6, darker(cream, 0.06))
    with s.part():
        s.ellipse(86, 66, 26, 11, cream)
    with s.part():
        s.tube([(72, 70), (72, 91)], 4, 3.6, cream)
        s.tube([(96, 72), (98, 91)], 4, 3.6, cream)
    with s.part():
        s.tri((46, 44), (40, 26), (54, 38), cream)
        s.tri((62, 40), (68, 24), (70, 40), cream)
        s.tri((47, 40), (43, 30), (52, 38), (60, 60, 70))
        s.tri((63, 37), (67, 29), (68, 39), (60, 60, 70))
    with s.part():
        s.ellipse(56, 52, 13, 11, cream)
        s.circle(56, 42, 3, (220, 50, 60))
        s.ellipse(52, 52, 2.6, 2, (190, 40, 40), rot=-20)
        s.ellipse(62, 52, 2.6, 2, (190, 40, 40), rot=20)
        s.circle(57, 57, 1, BLACK)
    with s.part(outline=False, shade=False):
        s.curve([(46, 56), (36, 54), (28, 48)], OUTLINE, 0.6)
        s.curve([(66, 56), (76, 54), (82, 48)], OUTLINE, 0.6)


@card(43)
def primeape(s):
    monkey(s, 1.15, angry=True)


@card(44)
def rapidash(s):
    cream = (250, 236, 200)
    s.shadow(80, 93, 34)
    with s.part():
        s.flame(122, 52, 18, rot=60)
        s.flame(116, 42, 12, rot=40)
    with s.part():
        s.tube([(104, 64), (112, 78), (114, 90)], 3.6, 3, darker(cream, 0.06))
        s.tube([(70, 64), (64, 78), (62, 90)], 3.6, 3, darker(cream, 0.06))
    with s.part():
        s.ellipse(88, 58, 24, 12, cream)
    with s.part():
        s.tube([(76, 62), (76, 76), (74, 90)], 3.6, 3, cream)
        s.tube([(100, 62), (102, 76), (104, 90)], 3.6, 3, cream)
        for x in (74, 104, 114, 62):
            s.ellipse(x, 91, 3, 1.6, (90, 80, 80))
    with s.part():
        for i in range(4):
            s.flame(66 + i * 7, 36 + i * 5, 14 - i, rot=50)
    with s.part():
        s.tube([(76, 54), (62, 38)], 7, 6, cream)
        s.ellipse(54, 32, 11, 8, cream, rot=-15)
        s.tri((54, 26), (50, 8), (58, 24), (232, 228, 214))
        s.tri((58, 26), (62, 20), (62, 28), cream)
        s.eye(54, 30, 2.4, iris=(200, 40, 40))
        s.circle(44, 34, 1, BLACK)


@card(45)
def rhydon(s):
    drill_rhino(s, upright=True)


@card(46)
def seaking(s):
    fish(s, WHITE, (236, 112, 50), (236, 112, 50), size=1.15)


@card(47)
def tauros(s):
    brown, mane = (186, 140, 90), (110, 80, 60)
    s.shadow(82, 93, 34)
    with s.part():
        for i in range(3):
            s.curve([(108, 60), (120, 54 + i * 8), (126, 44 + i * 12)], mane, 1.8)
            s.circle(126, 44 + i * 12, 2.6, mane)
    with s.part():
        s.tube([(104, 66), (108, 80), (106, 91)], 5, 4.5, darker(brown, 0.08))
        s.tube([(68, 66), (64, 80), (62, 91)], 5, 4.5, darker(brown, 0.08))
    with s.part():
        s.ellipse(88, 62, 24, 14, brown)
    with s.part():
        s.tube([(76, 66), (76, 91)], 5, 4.5, brown)
        s.tube([(98, 68), (100, 91)], 5, 4.5, brown)
    with s.part():
        s.ellipse(64, 56, 14, 14, mane)
    with s.part():
        s.curve([(48, 40), (40, 30), (44, 20)], WHITE, 3)
        s.curve([(62, 38), (70, 28), (66, 18)], WHITE, 3)
        s.ellipse(54, 48, 11, 10, brown)
        s.ellipse(48, 54, 8, 6, brown)
        s.eye(52, 46, 2.2)
        s.line([(48, 42), (56, 44)], OUTLINE, 1)
        s.circle(44, 55, 1, BLACK)


@card(48)
def weepinbell(s):
    yellow, green = (232, 214, 86), (80, 166, 72)
    s.shadow(80, 93, 22)
    with s.part():
        s.curve([(80, 30), (88, 22), (90, 12)], (120, 100, 60), 2)
    with s.part():
        s.ellipse(56, 66, 14, 5, green, rot=30)
        s.ellipse(104, 66, 14, 5, green, rot=-30)
    with s.part():
        s.ellipse(80, 54, 22, 26, yellow)
    with s.part(outline=False):
        for x, y in ((72, 70), (88, 72), (80, 76)):
            s.circle(x, y, 1.8, (176, 160, 60))
    with s.part():
        s.ellipse(80, 52, 14, 5, (232, 140, 160))
    with s.part(outline=False, shade=False):
        s.eye(70, 42, 2.4)
        s.eye(90, 42, 2.4)
        s.tri((74, 50), (76, 54), (78, 50), WHITE)
        s.tri((82, 50), (84, 54), (86, 50), WHITE)


@card(49)
def bellsprout(s):
    bell_plant(s, 76, 38, 11)


@card(50)
def cubone(s):
    skull_kid(s, 0.9)


@card(51)
def eevee(s):
    def ruff(s):
        with s.part():
            for i in range(6):
                a = math.radians(-20 + i * 30)
                s.circle(70 + 10 * math.cos(a), 62 + 8 * math.sin(a), 5, (246, 232, 196))
            s.ellipse(70, 62, 9, 8, (246, 232, 196))

    def tail(s):
        with s.part():
            s.ellipse(116, 56, 11, 16, (176, 120, 72), rot=-30)
            s.ellipse(122, 46, 6, 7, (246, 232, 196), rot=-30)

    fox(s, (176, 120, 72), ruff, tail, ears=(1.1, 1.1))


@card(52)
def exeggcute(s):
    egg, cracked = (244, 196, 200), (220, 170, 120)
    s.shadow(80, 93, 34)
    for i, (x, y) in enumerate(((58, 78), (80, 80), (102, 78), (68, 60), (92, 60), (80, 42))):
        with s.part():
            s.ellipse(x, y, 11, 12, egg)
            if i == 4:
                s.line([(x - 8, y - 6), (x - 4, y - 9), (x, y - 5), (x + 4, y - 9), (x + 8, y - 6)], cracked, 0.9)
        with s.part(outline=False, shade=False):
            s.eye(x - 4, y - 1, 1.8)
            s.eye(x + 4, y - 1, 1.8)
            s.smile(x, y + 4, 2.4)


@card(53)
def goldeen(s):
    fish(s, WHITE, (236, 112, 50), (236, 112, 50), size=0.85)


@card(54)
def jigglypuff(s):
    puff(s, 26)
    with s.part(outline=False, shade=False):
        for x, y in ((120, 30), (130, 44), (34, 34)):
            s.circle(x, y, 2.4, (60, 60, 80))
            s.line([(x + 2, y), (x + 2, y - 9), (x + 6, y - 7)], (60, 60, 80), 0.8)


@card(55)
def mankey(s):
    monkey(s, 0.9)


@card(56)
def meowth(s):
    cream, brown = (240, 224, 186), (150, 106, 70)
    s.shadow(80, 93, 20)
    with s.part():
        s.curve([(90, 82), (110, 84), (118, 66), (110, 58)], cream, 2)
        s.circle(110, 58, 2.6, brown)
    with s.part():
        s.ellipse(72, 90, 6, 3, brown)
        s.ellipse(88, 90, 6, 3, brown)
        s.tube([(74, 78), (72, 89)], 3.4, 3, cream)
        s.tube([(86, 78), (88, 89)], 3.4, 3, cream)
    with s.part():
        s.ellipse(80, 70, 11, 12, cream)
    with s.part():
        s.tube([(70, 66), (62, 62), (58, 56)], 3, 2.6, cream)
        s.tube([(90, 66), (98, 70), (102, 72)], 3, 2.6, cream)
    with s.part():
        s.circle(58, 52, 6, (244, 204, 70))
        s.circle(58, 52, 3.6, (228, 180, 50))
    with s.part():
        s.tri((66, 40), (62, 22), (74, 34), cream)
        s.tri((94, 40), (98, 22), (86, 34), cream)
        s.tri((66, 36), (63, 26), (71, 34), BLACK)
        s.tri((94, 36), (97, 26), (89, 34), BLACK)
    with s.part():
        s.ellipse(80, 46, 15, 13, cream)
        s.ellipse(80, 36, 4, 3, (244, 204, 70))
        s.eye(74, 46, 2.4)
        s.eye(86, 46, 2.4)
        s.curve([(76, 53), (78, 55), (80, 53), (82, 55), (84, 53)], OUTLINE, 0.7)
    with s.part(outline=False, shade=False):
        s.line([(66, 50), (56, 48)], OUTLINE, 0.6)
        s.line([(94, 50), (104, 48)], OUTLINE, 0.6)


@card(57)
def nidoran_f(s):
    nido(s, (140, 196, 226), (236, 236, 240), size=0.8, upright=False, spikes=False)


@card(58)
def oddish(s):
    blue, green = (80, 104, 180), (80, 170, 76)
    s.shadow(80, 93, 18)
    with s.part():
        s.ellipse(72, 90, 6, 3.5, blue)
        s.ellipse(88, 90, 6, 3.5, blue)
    with s.part():
        for a in (-150, -115, -90, -65, -30):
            r = math.radians(a)
            s.ellipse(80 + 18 * math.cos(r), 50 + 18 * math.sin(r), 16, 5.5, green, rot=a)
    with s.part(outline=False):
        for a in (-150, -115, -90, -65, -30):
            r = math.radians(a)
            s.line([(80 + 6 * math.cos(r), 50 + 6 * math.sin(r)), (80 + 30 * math.cos(r), 50 + 30 * math.sin(r))], darker(green, 0.3), 0.6)
    with s.part():
        s.ellipse(80, 70, 18, 17, blue)
    with s.part(outline=False, shade=False):
        s.eye(74, 68, 2.4, iris=(200, 40, 40))
        s.eye(86, 68, 2.4, iris=(200, 40, 40))
        s.smile(80, 75, 2.6)


@card(59)
def paras(s):
    mushroom_bug(s, 80, 76, 0.85, [(-6, -12, 12), (10, -12, 12)])


@card(60)
def pikachu(s):
    with s.part(outline=False, shade=False):
        s.bolt(36, 30, 7, (255, 236, 120), rot=-15)
        s.bolt(134, 70, 6, (255, 236, 120), rot=25)
    base1.pikachu(s)


@card(61)
def rhyhorn(s):
    drill_rhino(s)


@card(62)
def spearow(s):
    brown, red = (170, 116, 76), (200, 70, 56)
    s.shadow(80, 93, 20)
    with s.part():
        s.line([(76, 76), (74, 90)], (230, 170, 100), 1.4)
        s.line([(86, 76), (88, 90)], (230, 170, 100), 1.4)
    with s.part():
        s.poly([(84, 58), (110, 32), (122, 38), (100, 62)], red)
        s.poly([(74, 58), (46, 34), (38, 42), (64, 64)], darker(red, 0.1))
    with s.part():
        s.poly([(92, 70), (112, 78), (106, 84), (88, 76)], brown)
        s.ellipse(80, 66, 14, 12, brown)
        s.ellipse(76, 70, 8, 6, (240, 220, 180))
    with s.part():
        for i in range(3):
            s.tri((70, 42), (74 + i * 4, 30 + i * 2), (76, 44), red)
        s.ellipse(68, 50, 9, 8, brown)
        s.tri((60, 48), (50, 52), (60, 54), (236, 196, 120))
        s.eye(68, 48, 2.2)
        s.line([(64, 44), (71, 45)], OUTLINE, 1)


@card(63)
def venonat(s):
    fur = (140, 100, 170)
    s.shadow(80, 93, 22)
    with s.part():
        s.ellipse(70, 90, 7, 4, (220, 210, 230))
        s.ellipse(90, 90, 7, 4, (220, 210, 230))
    with s.part():
        s.curve([(72, 44), (66, 30), (60, 26)], fur, 1.2)
        s.curve([(88, 44), (94, 30), (100, 26)], fur, 1.2)
        s.circle(60, 26, 2.4, fur)
        s.circle(100, 26, 2.4, fur)
    with s.part():
        for i in range(16):
            a = math.radians(i * 360 / 16)
            s.circle(80 + 21 * math.cos(a), 66 + 20 * math.sin(a), 4.5, fur)
        s.circle(80, 66, 22, fur)
    with s.part():
        s.ellipse(58, 72, 4, 6, fur, rot=-20)
        s.ellipse(102, 72, 4, 6, fur, rot=20)
    with s.part():
        for x in (71, 89):
            s.circle(x, 60, 7, (220, 50, 60))
    with s.part(outline=False, shade=False):
        for x in (71, 89):
            for dx, dy in ((-2, -2), (2, -2), (0, 1), (-3, 2), (3, 2)):
                s.circle(x + dx, 60 + dy, 0.9, (250, 140, 140))
        s.tri((77, 76), (80, 80), (83, 76), WHITE)
