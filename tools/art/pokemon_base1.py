"""
Original drawings of the Base Set Pokemon, one function per card number.
Stage is 160 x 100 units, ground line around y = 92.
"""
import math
import random

from .canvas import OUTLINE, Sprite, darker, lighter

CREAM = (246, 226, 168)
WHITE = (246, 246, 250)
PINK = (244, 168, 186)
RED = (222, 58, 52)
BLACK = (40, 36, 42)
SILVER = (196, 200, 210)
BROWN = (150, 98, 58)

DRAW = {}


def card(number):
    def wrap(fn):
        DRAW[number] = fn
        return fn
    return wrap


# ------------------------------------------------------------------ shared builders

def biped_lizard(s: Sprite, body, belly, horn=False, flame=True, scale=1.0):
    """Charmander / Charmeleon."""
    k = scale
    s.shadow(80, 93, 26 * k)
    with s.part():  # tail
        s.tube([(92, 82), (112, 86), (122, 70)], 5 * k, 3 * k, body)
    if flame:
        with s.part():
            s.flame(123, 62, 12 * k, rot=10)
    with s.part():  # legs
        s.ellipse(70, 88, 8 * k, 5 * k, body)
        s.ellipse(90, 88, 8 * k, 5 * k, body)
    with s.part():
        s.ellipse(80, 70, 15 * k, 19 * k, body)
        s.ellipse(80, 74, 9 * k, 13 * k, belly)
    with s.part():  # arms
        s.tube([(68, 62), (60, 66), (58, 72)], 3.5 * k, 3 * k, body)
        s.tube([(92, 62), (100, 66), (102, 72)], 3.5 * k, 3 * k, body)
    with s.part():  # head
        if horn:
            s.tri((74, 30), (62, 22), (72, 38), body)
        s.ellipse(80, 40, 15 * k, 14 * k, body)
        s.ellipse(88, 46, 9 * k, 7 * k, body)
        s.eye(78, 38, 3.2 * k, look=(0.6, 0))
        s.eye(90, 38, 3.0 * k, look=(0.6, 0))
        s.smile(91, 48, 5)


def turtle(s: Sprite, skin, shell, rim, ears=False, cannons=False, size=1.0):
    k = size
    s.shadow(80, 93, 30 * k)
    if ears:
        with s.part():  # fluffy tail
            s.curve([(100, 80), (124, 84), (128, 66), (116, 64)], (228, 236, 250), 7)
    with s.part():  # shell back
        s.ellipse(82, 66, 24 * k, 24 * k, rim)
        s.ellipse(82, 66, 21 * k, 21 * k, shell)
    if cannons:
        with s.part():
            s.tube([(64, 52), (56, 40), (52, 32)], 5, 5, SILVER)
            s.tube([(98, 52), (106, 40), (110, 32)], 5, 5, SILVER)
            s.circle(52, 31, 3, (60, 60, 70))
            s.circle(110, 31, 3, (60, 60, 70))
    with s.part():  # legs
        s.ellipse(68, 88, 9 * k, 6 * k, skin)
        s.ellipse(92, 88, 9 * k, 6 * k, skin)
    with s.part():  # body front
        s.ellipse(80, 68, 17 * k, 20 * k, skin)
        s.ellipse(80, 71, 12 * k, 15 * k, CREAM)
        for y in (64, 71, 78):
            s.line([(70, y), (90, y)], darker(CREAM, 0.25), 0.8)
    with s.part():  # arms
        s.tube([(64, 60), (56, 68), (54, 76)], 4.5 * k, 4 * k, skin)
        s.tube([(96, 60), (104, 68), (106, 76)], 4.5 * k, 4 * k, skin)
    if ears:
        with s.part():
            s.curve([(68, 32), (56, 22), (58, 12), (66, 18)], (228, 236, 250), 5)
            s.curve([(92, 32), (104, 22), (102, 12), (94, 18)], (228, 236, 250), 5)
    with s.part():
        s.ellipse(80, 38, 15 * k, 14 * k, skin)
        if cannons:
            s.tri((68, 30), (64, 22), (72, 28), skin)
            s.tri((92, 30), (96, 22), (88, 28), skin)
        s.eyes(80, 37, 11 * k, 3.0 * k)
        s.smile(80, 45, 5)


def quadruped_dog(s: Sprite, fur, mane, stripes=True, big=True):
    k = 1.0 if big else 0.8
    s.shadow(84, 93, 32 * k)
    with s.part():  # tail
        s.ellipse(118, 54, 12 * k, 8 * k, mane, rot=-35)
    with s.part():  # back legs
        s.tube([(106, 66), (110, 80), (108, 90)], 5 * k, 4 * k, fur)
        s.tube([(66, 66), (64, 80), (62, 90)], 5 * k, 4 * k, darker(fur, 0.1))
    with s.part():
        s.ellipse(88, 64, 26 * k, 13 * k, fur)
        if stripes:
            for x in (78, 88, 98, 108):
                s.curve([(x, 54), (x + 3, 60), (x - 1, 66)], BLACK, 2)
    with s.part():  # front legs
        s.tube([(70, 68), (70, 82), (70, 91)], 5 * k, 4 * k, fur)
        s.tube([(98, 70), (100, 82), (100, 91)], 5 * k, 4 * k, fur)
    with s.part():  # mane
        s.ellipse(62, 56, 13 * k, 14 * k, mane)
    with s.part():  # head
        s.ellipse(54, 42, 12 * k, 11 * k, fur)
        s.ellipse(44, 47, 8 * k, 6 * k, fur)
        s.tri((56, 34), (64, 22), (64, 38), fur)
        s.ellipse(56, 31, 6 * k, 4 * k, mane)
        s.circle(37, 46, 2.2, BLACK)
        s.eye(52, 41, 2.6)
        s.curve([(38, 51), (44, 53), (48, 51)], OUTLINE, 0.8)


def quadruped_bulb(s: Sprite, skin, spots, back):
    """Bulbasaur / Ivysaur / Venusaur. back(s) draws what grows on the back."""
    s.shadow(80, 93, 34)
    with s.part():
        s.ellipse(90, 74, 26, 14, skin)
        for x, y in ((84, 68), (100, 72), (92, 78)):
            s.ellipse(x, y, 3.5, 2.5, spots)
    with s.part():  # legs
        for x in (70, 82, 98, 110):
            s.ellipse(x, 88, 6, 6, skin)
    back(s)
    with s.part():  # head
        s.ellipse(56, 62, 16, 13, skin)
        s.tri((46, 52), (42, 42), (52, 50), skin)
        s.tri((64, 50), (68, 42), (60, 50), skin)
        s.ellipse(52, 66, 3, 2.2, spots)
        s.eye(50, 60, 3.0, iris=(190, 40, 40))
        s.eye(62, 60, 3.0, iris=(190, 40, 40))
        s.curve([(46, 70), (56, 74), (66, 70)], OUTLINE, 0.8)


def mole(s, x, y, size=1.0):
    with s.part():
        s.ellipse(x, y, 9 * size, 13 * size, (162, 108, 72))
        s.ellipse(x, y + 2 * size, 5 * size, 3.5 * size, (238, 140, 160))
        s.ellipse(x - 3.2 * size, y - 5 * size, 1.1 * size, 1.9 * size, BLACK)
        s.ellipse(x + 3.2 * size, y - 5 * size, 1.1 * size, 1.9 * size, BLACK)


def magnemite(s, x, y, r=11):
    with s.part():  # magnets
        for side in (-1, 1):
            mx = x + side * (r + 5)
            s.tube([(mx, y - 6), (mx + side * 4, y), (mx, y + 6)], 2.6, 2.6, SILVER)
            s.circle(mx, y - 6, 2.6, (220, 60, 60))
            s.circle(mx, y + 6, 2.6, (70, 110, 220))
    with s.part():
        s.circle(x, y, r, SILVER)
        s.circle(x, y, r * 0.55, WHITE)
        s.circle(x, y, r * 0.24, BLACK)
        s.circle(x - r * 0.1, y - r * 0.12, r * 0.08, WHITE)
        for sx, sy in ((x - r * 0.6, y + r * 0.62), (x + r * 0.6, y + r * 0.62)):
            s.circle(sx, sy, r * 0.12, darker(SILVER, 0.2))
    with s.part():  # screw on top
        s.rect(x - 2, y - r - 6, x + 2, y - r + 1, (160, 164, 176))
        s.ellipse(x, y - r - 6, 4, 1.6, (190, 194, 204))


def split_ball(s, cx, cy, r, top, bottom, grin):
    """Voltorb / Electrode: a ball with a coloured top and bottom half and angry eyes."""
    with s.part():
        s.circle(cx, cy, r, bottom)
        s.poly([(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in range(0, 181, 5)], top)
    with s.part(outline=False, shade=False):
        s.line([(cx - r, cy), (cx + r, cy)], OUTLINE, 1)
        s.poly([(cx - r * 0.55, cy - r * 0.45), (cx - r * 0.12, cy - r * 0.2), (cx - r * 0.55, cy - r * 0.15)], BLACK)
        s.poly([(cx + r * 0.55, cy - r * 0.45), (cx + r * 0.12, cy - r * 0.2), (cx + r * 0.55, cy - r * 0.15)], BLACK)
        if grin:
            s.curve([(cx - r * 0.6, cy + r * 0.25), (cx, cy + r * 0.75), (cx + r * 0.6, cy + r * 0.25)], BLACK, 1.6)


def spiral_belly(s, cx, cy, r):
    s.circle(cx, cy, r, WHITE)
    s.spiral(cx, cy, r * 0.85, 2.2, BLACK, 1.1)


def serpent(s, path, r0, r1, body, belly, head_at, head_r, ears_col=WHITE, orbs=None):
    s.shadow(82, 93, 36)
    with s.part():
        s.tube(path, r0, r1, body, n=90)
    with s.part(outline=False):
        shifted = [(x + 1.5, y + r0 * 0.35) for x, y in path]
        s.tube(shifted, r0 * 0.45, r1 * 0.45, belly, n=90)
    if orbs:
        for (x, y) in orbs:
            with s.part():
                s.circle(x, y, 3.2, (40, 70, 200))
    hx, hy = head_at
    with s.part():
        s.tri((hx + 4, hy - 4), (hx + 16, hy - 14), (hx + 10, hy + 2), ears_col)
        s.tri((hx - 6, hy - 4), (hx - 14, hy - 16), (hx - 2, hy - 6), ears_col)
    with s.part():
        s.ellipse(hx, hy, head_r * 1.15, head_r, body)
        s.ellipse(hx - head_r * 0.7, hy + head_r * 0.3, head_r * 0.6, head_r * 0.45, body)
        s.eye(hx - 2, hy - 2, 2.6, iris=(60, 40, 120))
        s.curve([(hx - head_r * 1.2, hy + head_r * 0.45), (hx - head_r * 0.6, hy + head_r * 0.6)], OUTLINE, 0.7)


def humanoid_psychic(s, skin, armor, spoons=2, star=False, tail=False):
    s.shadow(80, 93, 22)
    if tail:
        with s.part():
            s.tube([(90, 80), (112, 86), (122, 72)], 4, 3, (200, 150, 70))
    with s.part():  # legs
        s.tube([(72, 72), (68, 84), (66, 91)], 4, 3.5, skin)
        s.tube([(88, 72), (92, 84), (94, 91)], 4, 3.5, skin)
    with s.part():
        s.ellipse(80, 62, 13, 15, armor)
        s.ellipse(80, 70, 9, 7, skin)
    with s.part():  # arms
        s.tube([(68, 52), (58, 58), (50, 62)], 3.4, 3, skin)
        s.tube([(92, 52), (102, 58), (110, 62)], 3.4, 3, skin)
    spoon_hands = [(50, 62), (110, 62)][:spoons]
    for hx, hy in spoon_hands:
        with s.part():
            s.line([(hx, hy), (hx - 2 if hx < 80 else hx + 2, hy - 18)], SILVER, 1.8)
            s.ellipse(hx - 2.5 if hx < 80 else hx + 2.5, hy - 22, 3.5, 5, SILVER)
    with s.part():
        s.ellipse(80, 50, 14, 6, armor)  # shoulder plates
    with s.part():  # head
        s.tri((70, 30), (60, 10), (76, 26), skin)
        s.tri((90, 30), (100, 10), (84, 26), skin)
        s.ellipse(80, 34, 12, 12, skin)
        s.ellipse(80, 40, 8, 5, skin)
        if star:
            s.star(80, 26, 3.5, 1.5, (220, 50, 50))
        s.line([(72, 33), (77, 35)], OUTLINE, 1.1)
        s.line([(88, 33), (83, 35)], OUTLINE, 1.1)
    with s.part():  # moustache
        s.curve([(77, 41), (68, 44), (64, 58)], (130, 90, 50), 1.8)
        s.curve([(83, 41), (92, 44), (96, 58)], (130, 90, 50), 1.8)


def muscle_man(s, skin, crest, briefs=True, four_arms=False, scale=1.0):
    k = scale
    s.shadow(80, 93, 26 * k)
    with s.part():
        s.tube([(72, 72), (68, 84), (66, 91)], 6 * k, 5 * k, skin)
        s.tube([(88, 72), (92, 84), (94, 91)], 6 * k, 5 * k, skin)
    if four_arms:
        with s.part():
            s.tube([(66, 60), (54, 66), (46, 74)], 5, 4.5, darker(skin, 0.08))
            s.tube([(94, 60), (106, 66), (114, 74)], 5, 4.5, darker(skin, 0.08))
            s.circle(45, 75, 5, darker(skin, 0.08))
            s.circle(115, 75, 5, darker(skin, 0.08))
    with s.part():
        s.ellipse(80, 58, 17 * k, 18 * k, skin)
        s.curve([(70, 52), (80, 56), (90, 52)], darker(skin, 0.3), 0.9)
        s.line([(80, 56), (80, 68)], darker(skin, 0.3), 0.8)
    if briefs:
        with s.part():
            s.poly([(66, 68), (94, 68), (92, 78), (80, 80), (68, 78)], BLACK)
            s.rect(66, 67, 94, 71, (240, 200, 60))
            s.rect(78, 66, 82, 72, (250, 220, 100))
    with s.part():
        s.tube([(64, 48), (52, 40), (46, 30)], 5.5 * k, 5 * k, skin)
        s.tube([(96, 48), (108, 40), (114, 30)], 5.5 * k, 5 * k, skin)
        s.circle(46, 28, 5.5 * k, skin)
        s.circle(114, 28, 5.5 * k, skin)
    with s.part():
        s.ellipse(80, 32, 10 * k, 10 * k, skin)
        for dx in (-5, 0, 5):
            s.ellipse(80 + dx, 21, 2, 5, crest)
        s.eye(76, 32, 2.2, iris=(200, 40, 40))
        s.eye(84, 32, 2.2, iris=(200, 40, 40))
        s.line([(76, 38), (84, 38)], OUTLINE, 0.9)


def bird(s, body, chest, wing, crest=None, flying=True, size=1.0):
    k = size
    s.shadow(80, 93, 22 * k)
    if flying:
        with s.part():  # far wing
            s.poly([(84, 52), (120, 22), (138, 30), (126, 44), (104, 60)], darker(wing, 0.1))
    with s.part():  # tail
        s.poly([(92, 66), (118, 80), (112, 86), (88, 74)], wing)
    with s.part():
        s.ellipse(80, 62, 16 * k, 13 * k, body)
        s.ellipse(74, 66, 10 * k, 8 * k, chest)
    if not flying:
        with s.part():
            s.line([(74, 74), (72, 90)], (230, 170, 80), 1.5)
            s.line([(84, 74), (86, 90)], (230, 170, 80), 1.5)
    with s.part():  # near wing
        if flying:
            s.poly([(76, 56), (40, 22), (24, 30), (40, 46), (70, 66)], wing)
            for i in range(3):
                s.line([(36 + i * 6, 32 + i * 4), (56 + i * 4, 52 + i * 2)], darker(wing, 0.25), 0.8)
        else:
            s.ellipse(86, 62, 11, 7, wing, rot=20)
    if crest:
        with s.part():
            for i, col in enumerate(crest):
                s.curve([(66, 40), (76 + i * 4, 30 - i * 3), (92 + i * 6, 28 - i * 2)], col, 3 - i * 0.5)
    with s.part():
        s.ellipse(64, 46, 10 * k, 9 * k, body)
        s.ellipse(62, 49, 7 * k, 5 * k, chest)
        s.tri((55, 46), (46, 49), (55, 51), (60, 54, 64))
        s.eye(62, 44, 2.4)


# ------------------------------------------------------------------ 1 - 16 holo rares

@card(1)  # Alakazam
def alakazam(s):
    humanoid_psychic(s, (232, 196, 96), (150, 98, 52), spoons=2)


@card(2)  # Blastoise
def blastoise(s):
    turtle(s, (92, 140, 210), (130, 94, 64), (232, 216, 170), cannons=True, size=1.05)


@card(3)  # Chansey
def chansey(s):
    s.shadow(80, 93, 24)
    with s.part():  # side tufts
        for side in (-1, 1):
            for i in range(3):
                y = 38 + i * 8
                s.tri((80 + side * 20, y - 3), (80 + side * 32, y - 2 + i), (80 + side * 21, y + 4), PINK)
    with s.part():
        s.ellipse(80, 62, 24, 30, PINK)
    with s.part():
        s.ellipse(70, 91, 7, 4, darker(PINK, 0.1))
        s.ellipse(90, 91, 7, 4, darker(PINK, 0.1))
    with s.part():  # pouch and egg
        s.ellipse(80, 76, 12, 8, (250, 214, 220))
        s.ellipse(80, 70, 6, 8, WHITE)
    with s.part():
        s.ellipse(64, 66, 4, 6, PINK, rot=-30)
        s.ellipse(96, 66, 4, 6, PINK, rot=30)
    with s.part(outline=False, shade=False):
        s.eye(73, 50, 2.8)
        s.eye(87, 50, 2.8)
        s.smile(80, 58, 4)
        s.ellipse(68, 56, 3, 1.6, (240, 130, 150))
        s.ellipse(92, 56, 3, 1.6, (240, 130, 150))


@card(4)  # Charizard
def charizard(s):
    orange, teal = (240, 130, 56), (64, 150, 160)
    s.shadow(80, 93, 30)
    with s.part():  # wings
        s.poly([(70, 52), (26, 16), (34, 34), (18, 44), (32, 50), (22, 62), (62, 66)], orange)
        s.poly([(90, 52), (134, 16), (126, 34), (142, 44), (128, 50), (138, 62), (98, 66)], orange)
    with s.part(outline=False):
        s.poly([(66, 54), (32, 24), (36, 36), (26, 45), (36, 50), (30, 58), (62, 63)], teal)
        s.poly([(94, 54), (128, 24), (124, 36), (134, 45), (124, 50), (130, 58), (98, 63)], teal)
    with s.part():
        s.tube([(94, 84), (118, 88), (128, 72)], 6, 3.5, orange)
    with s.part():
        s.flame(129, 63, 12, rot=8)
    with s.part():
        s.ellipse(70, 89, 9, 5, orange)
        s.ellipse(90, 89, 9, 5, orange)
    with s.part():
        s.ellipse(80, 70, 15, 20, orange)
        s.ellipse(80, 74, 10, 15, CREAM)
    with s.part():
        s.tube([(70, 60), (62, 66), (60, 72)], 3.5, 3, orange)
        s.tube([(90, 60), (98, 66), (100, 72)], 3.5, 3, orange)
    with s.part():  # neck and head
        s.tube([(80, 54), (80, 44), (78, 36)], 7, 6, orange)
    with s.part():
        s.tri((72, 26), (62, 14), (76, 22), orange)
        s.tri((84, 24), (82, 10), (88, 22), orange)
        s.ellipse(78, 30, 11, 9, orange)
        s.ellipse(68, 34, 8, 5.5, orange)
        s.eye(76, 28, 2.6, look=(-0.6, 0))
        s.curve([(61, 37), (68, 38), (74, 37)], OUTLINE, 0.8)


@card(5)  # Clefairy
def clefairy(s):
    s.shadow(80, 93, 20)
    with s.part():  # wings
        s.ellipse(60, 60, 6, 9, (252, 214, 222), rot=-30)
        s.ellipse(100, 60, 6, 9, (252, 214, 222), rot=30)
    with s.part():  # ears
        s.tri((64, 40), (54, 16), (74, 34), PINK)
        s.tri((96, 40), (106, 16), (86, 34), PINK)
        s.tri((56, 21), (54, 16), (60, 22), (110, 70, 60))
        s.tri((104, 21), (106, 16), (100, 22), (110, 70, 60))
    with s.part():
        s.ellipse(80, 64, 20, 26, PINK)
    with s.part():
        s.ellipse(70, 90, 6, 4, PINK)
        s.ellipse(90, 90, 6, 4, PINK)
        s.ellipse(62, 66, 4, 5, PINK)
        s.ellipse(98, 66, 4, 5, PINK)
    with s.part(outline=False, shade=False):
        s.curve([(80, 40), (74, 34), (80, 30), (84, 36)], (200, 120, 130), 1.6)
        s.eye(73, 52, 2.6)
        s.eye(87, 52, 2.6)
        s.smile(80, 59, 3)
        s.ellipse(67, 58, 2.5, 1.4, (240, 130, 150))
        s.ellipse(93, 58, 2.5, 1.4, (240, 130, 150))


@card(6)  # Gyarados
def gyarados(s):
    blue, belly = (54, 104, 200), (236, 222, 160)
    with s.part(outline=False, shade=False):  # water
        s.ellipse(100, 94, 50, 8, (180, 220, 250))
    with s.part():  # fin crest along the back
        for i, (x, y) in enumerate([(122, 70), (124, 56), (116, 44), (102, 34)]):
            s.tri((x - 3, y + 4), (x + 8, y - 6), (x + 3, y + 6), WHITE)
    with s.part():
        s.tube([(108, 96), (126, 72), (112, 44), (78, 34)], 11, 9, blue, n=90)
    with s.part(outline=False):
        s.tube([(104, 96), (120, 72), (108, 48), (82, 40)], 5, 4, belly, n=90)
    with s.part():  # crest
        s.tri((62, 22), (58, 4), (70, 18), (60, 110, 210))
        s.tri((70, 20), (74, 2), (78, 18), (60, 110, 210))
    with s.part():  # head
        s.ellipse(62, 32, 17, 13, blue)
        s.poly([(42, 30), (56, 38), (68, 46), (46, 46)], (160, 40, 50))
        s.tri((46, 32), (49, 38), (51, 32), WHITE)
        s.tri((52, 44), (55, 39), (58, 44), WHITE)
        s.eye(64, 26, 3.0, iris=(200, 40, 40))
        s.line([(60, 22), (68, 24)], OUTLINE, 1.2)
    with s.part():  # whiskers
        s.curve([(48, 36), (34, 34), (28, 42)], WHITE, 1.6)
        s.curve([(50, 40), (38, 48), (36, 58)], WHITE, 1.6)


@card(7)  # Hitmonchan
def hitmonchan(s):
    skin, tunic = (186, 140, 100), (150, 96, 170)
    s.shadow(80, 93, 22)
    with s.part():
        s.tube([(74, 72), (70, 84), (68, 91)], 4.5, 4, skin)
        s.tube([(86, 72), (90, 84), (92, 91)], 4.5, 4, skin)
    with s.part():
        s.ellipse(80, 60, 13, 16, skin)
        s.poly([(66, 60), (94, 60), (98, 78), (62, 78)], tunic)
    with s.part():
        s.tube([(68, 50), (58, 46), (52, 40)], 3.5, 3.5, skin)
        s.tube([(92, 50), (102, 52), (110, 48)], 3.5, 3.5, skin)
    with s.part():
        s.circle(50, 37, 8, (226, 46, 46))
        s.circle(114, 46, 8, (226, 46, 46))
    with s.part():
        s.ellipse(80, 34, 10, 11, skin)
        s.eye(76, 32, 2.2, iris=(80, 50, 30))
        s.eye(84, 32, 2.2, iris=(80, 50, 30))
        s.line([(72, 28), (78, 30)], OUTLINE, 1)
        s.line([(88, 28), (82, 30)], OUTLINE, 1)
        s.line([(76, 39), (84, 39)], OUTLINE, 0.8)


@card(8)  # Machamp
def machamp(s):
    muscle_man(s, (128, 148, 172), (226, 196, 140), four_arms=True, scale=1.05)


@card(9)  # Magneton
def magneton(s):
    s.shadow(80, 93, 30)
    magnemite(s, 80, 70, 11)
    magnemite(s, 58, 42, 11)
    magnemite(s, 102, 42, 11)


@card(10)  # Mewtwo
def mewtwo(s):
    pale, purple = (222, 210, 228), (152, 112, 176)
    s.shadow(80, 93, 22)
    with s.part():
        s.tube([(88, 74), (116, 84), (128, 70), (124, 56)], 6, 3.5, purple)
    with s.part():
        s.tube([(74, 70), (68, 82), (66, 91)], 6, 4, pale)
        s.tube([(86, 70), (92, 82), (94, 91)], 6, 4, pale)
    with s.part():
        s.ellipse(80, 56, 11, 15, pale)
        s.ellipse(80, 66, 9, 8, purple)
    with s.part():
        s.tube([(70, 48), (60, 56), (54, 62)], 3, 2.6, pale)
        s.tube([(90, 48), (100, 56), (106, 62)], 3, 2.6, pale)
        s.circle(53, 63, 3, pale)
        s.circle(107, 63, 3, pale)
    with s.part():  # tube from head to back
        s.curve([(88, 30), (98, 34), (90, 46)], pale, 2.4)
    with s.part():
        s.ellipse(80, 30, 9, 9, pale)
        s.ellipse(76, 34, 6, 4, pale)
        s.ellipse(74, 22, 2.4, 4, pale, rot=-20)
        s.ellipse(86, 22, 2.4, 4, pale, rot=20)
        s.eye(78, 29, 2.0, iris=(130, 60, 160))
        s.eye(85, 29, 2.0, iris=(130, 60, 160))


@card(11)  # Nidoking
def nidoking(s):
    body = (152, 92, 172)
    s.shadow(80, 93, 30)
    with s.part():
        s.tube([(94, 82), (120, 90), (134, 82)], 7, 4, body)
    with s.part():  # back spikes
        for i in range(4):
            s.tri((92 + i * 2, 42 + i * 10), (104 + i * 2, 40 + i * 10), (94 + i * 2, 50 + i * 10), darker(body, 0.2))
    with s.part():
        s.ellipse(70, 88, 9, 6, body)
        s.ellipse(92, 88, 9, 6, body)
    with s.part():
        s.ellipse(80, 64, 19, 23, body)
        s.ellipse(78, 70, 11, 15, CREAM)
    with s.part():
        s.tube([(66, 56), (56, 62), (54, 70)], 4.5, 4, body)
        s.tube([(94, 56), (102, 62), (104, 70)], 4.5, 4, body)
    with s.part():
        s.tri((70, 30), (62, 14), (76, 26), body)
        s.tri((88, 28), (96, 14), (84, 24), body)
        s.ellipse(76, 36, 12, 10, body)
        s.ellipse(68, 40, 8, 6, body)
        s.tri((72, 28), (70, 8), (78, 26), WHITE)
        s.eye(76, 34, 2.4, iris=(200, 40, 40))
        s.line([(62, 43), (70, 44)], OUTLINE, 0.8)


@card(12)  # Ninetales
def ninetales(s):
    fur, tip = (242, 218, 140), (240, 150, 70)
    s.shadow(80, 93, 32)
    for i in range(9):
        a = -150 + i * 15
        x = 102 + 22 * math.cos(math.radians(a + 90))
        y = 56 + 16 * math.sin(math.radians(a + 90)) - 10
        with s.part():
            s.ellipse(x, y, 13, 5, fur, rot=a + 60)
            s.ellipse(x + 9 * math.cos(math.radians(a + 60)), y + 9 * math.sin(math.radians(a + 60)), 4, 3, tip, rot=a + 60)
    with s.part():
        s.tube([(96, 70), (100, 82), (98, 91)], 3.5, 3, fur)
        s.tube([(66, 70), (64, 82), (62, 91)], 3.5, 3, darker(fur, 0.08))
    with s.part():
        s.ellipse(82, 66, 22, 11, fur)
    with s.part():
        s.tube([(72, 70), (72, 82), (72, 91)], 3.5, 3, fur)
        s.tube([(90, 70), (92, 82), (92, 91)], 3.5, 3, fur)
    with s.part():
        s.ellipse(58, 54, 8, 10, (250, 240, 200))
    with s.part():
        s.tri((52, 36), (50, 22), (58, 34), fur)
        s.tri((62, 36), (68, 24), (66, 38), fur)
        s.ellipse(56, 44, 9, 8, fur)
        s.ellipse(48, 48, 6, 4, fur)
        s.curve([(58, 36), (64, 30), (70, 34)], (250, 236, 190), 3)
        s.eye(56, 42, 2.2, iris=(200, 40, 40))
        s.circle(43, 47, 1.4, BLACK)


@card(13)  # Poliwrath
def poliwrath(s):
    blue = (70, 110, 196)
    s.shadow(80, 93, 26)
    with s.part():
        s.tube([(70, 80), (66, 88), (64, 92)], 6, 5, blue)
        s.tube([(90, 80), (94, 88), (96, 92)], 6, 5, blue)
    with s.part():
        s.circle(80, 58, 24, blue)
        spiral_belly(s, 80, 62, 15)
    with s.part():
        s.tube([(58, 52), (48, 44), (42, 36)], 6, 5.5, blue)
        s.tube([(102, 52), (112, 44), (118, 36)], 6, 5.5, blue)
        s.circle(41, 33, 6.5, WHITE)
        s.circle(119, 33, 6.5, WHITE)
    with s.part(outline=False, shade=False):
        s.eye(72, 40, 3.2)
        s.eye(88, 40, 3.2)
        s.line([(68, 35), (76, 37)], OUTLINE, 1.1)
        s.line([(92, 35), (84, 37)], OUTLINE, 1.1)


@card(14)  # Raichu
def raichu(s):
    orange, cream = (240, 150, 58), (250, 228, 170)
    s.shadow(80, 93, 22)
    with s.part():
        s.curve([(92, 82), (118, 86), (124, 60), (132, 40)], BLACK, 1.6)
        s.bolt(134, 34, 7, (248, 210, 70), rot=20)
    with s.part():
        s.ellipse(70, 90, 7, 4, (200, 120, 60))
        s.ellipse(90, 90, 7, 4, (200, 120, 60))
    with s.part():
        s.ellipse(80, 72, 15, 18, orange)
        s.ellipse(80, 76, 9, 12, cream)
    with s.part():
        s.tube([(68, 66), (60, 70), (60, 74)], 3, 2.5, orange)
        s.tube([(92, 66), (100, 70), (100, 74)], 3, 2.5, orange)
    with s.part():
        s.poly([(66, 42), (52, 14), (60, 30), (72, 38)], (176, 120, 70))
        s.poly([(94, 42), (108, 14), (100, 30), (88, 38)], (176, 120, 70))
    with s.part():
        s.ellipse(80, 46, 15, 13, orange)
        s.eye(74, 44, 2.6)
        s.eye(86, 44, 2.6)
        s.circle(80, 49, 1, BLACK)
        s.smile(80, 51, 3)
        s.circle(68, 50, 3, (250, 220, 80))
        s.circle(92, 50, 3, (250, 220, 80))


@card(15)  # Venusaur
def venusaur(s):
    def back(s):
        with s.part():  # leaves
            s.ellipse(70, 56, 20, 6, (60, 140, 70), rot=20)
            s.ellipse(112, 56, 20, 6, (60, 140, 70), rot=-20)
            s.rect(88, 50, 96, 62, (140, 96, 60))
        with s.part():  # flower
            for i in range(5):
                a = math.radians(-90 + i * 72)
                s.ellipse(92 + 13 * math.cos(a), 40 + 7 * math.sin(a), 11, 7, (240, 132, 150), rot=math.degrees(a))
            s.circle(92, 40, 5, (250, 200, 120))
            for i in range(5):
                a = math.radians(-90 + i * 72)
                s.circle(92 + 16 * math.cos(a), 40 + 9 * math.sin(a), 1.5, WHITE)
    quadruped_bulb(s, (98, 170, 156), (70, 130, 120), back)


@card(16)  # Zapdos
def zapdos(s):
    yellow = (250, 212, 58)
    s.shadow(80, 93, 30)

    def wing(side):
        pts = [(80, 50)]
        for i in range(6):
            x = 80 + side * (14 + i * 9)
            pts.append((x, 20 + i * 3))
            pts.append((x + side * 3, 30 + i * 4))
        pts.append((80 + side * 66, 52))
        pts.append((80 + side * 20, 62))
        return pts

    with s.part():
        s.poly(wing(-1), yellow)
        s.poly(wing(1), yellow)
    with s.part(outline=False):
        s.poly([(30, 40), (14, 50), (40, 52)], BLACK)
        s.poly([(130, 40), (146, 50), (120, 52)], BLACK)
    with s.part():  # tail
        s.poly([(74, 66), (66, 88), (76, 80), (80, 92), (84, 80), (94, 88), (86, 66)], yellow)
    with s.part():
        s.tube([(72, 84), (70, 90)], 1.5, 1.5, (230, 140, 50))
        s.tube([(88, 84), (90, 90)], 1.5, 1.5, (230, 140, 50))
        s.ellipse(80, 58, 12, 14, yellow)
    with s.part():
        for i in range(4):
            s.tri((74 + i * 3, 30), (66 + i * 6, 14 + (i % 2) * 4), (78 + i * 3, 28), yellow)
        s.ellipse(80, 38, 8, 8, yellow)
        s.tri((74, 40), (62, 44), (74, 44), (232, 140, 50))
        s.eye(80, 36, 2.2)


# ------------------------------------------------------------------ 17 - 22 rares

@card(17)  # Beedrill
def beedrill(s):
    yellow = (246, 206, 58)
    s.shadow(80, 93, 26)
    with s.part():  # wings
        s.ellipse(92, 30, 14, 7, (226, 240, 250), rot=-30)
        s.ellipse(102, 36, 12, 6, (226, 240, 250), rot=-10)
    with s.part():
        s.ellipse(102, 62, 13, 16, yellow, rot=-30)
        for t in (-6, 0, 6):
            s.ellipse(102 + t * 0.6, 62 + t, 12, 2.2, BLACK, rot=-30)
        s.tri((110, 74), (124, 88), (114, 72), WHITE)
    with s.part():
        s.ellipse(84, 50, 9, 8, yellow)
    with s.part():  # stinger arms
        s.tri((76, 54), (48, 50), (74, 60), WHITE)
        s.tri((84, 58), (60, 72), (84, 64), WHITE)
    with s.part():
        s.ellipse(72, 38, 9, 8, yellow)
        s.curve([(70, 32), (64, 22), (58, 20)], BLACK, 1)
        s.curve([(74, 31), (74, 20), (70, 16)], BLACK, 1)
        s.ellipse(66, 38, 4, 5, (220, 40, 40))
        s.ellipse(75, 37, 3, 4, (220, 40, 40))


@card(18)  # Dragonair
def dragonair(s):
    serpent(s, [(124, 90), (140, 70), (108, 66), (96, 84), (70, 82), (62, 46)], 6.5, 6, (110, 160, 232), WHITE,
            head_at=(60, 36), head_r=8, orbs=[(64, 50), (125, 89)])


@card(19)  # Dugtrio
def dugtrio(s):
    with s.part(shade=False):
        s.ellipse(80, 90, 54, 10, (150, 104, 70))
    mole(s, 54, 70, 1.45)
    mole(s, 106, 70, 1.45)
    mole(s, 80, 56, 1.65)
    with s.part(shade=False):
        s.ellipse(80, 91, 52, 7, (136, 92, 60))
        for x in (36, 66, 94, 124):
            s.ellipse(x, 86, 7, 4, (120, 82, 54))


@card(20)  # Electabuzz
def electabuzz(s):
    yellow = (246, 214, 70)
    s.shadow(80, 93, 22)
    with s.part():
        s.tube([(88, 80), (108, 86), (114, 78)], 3.5, 2.5, yellow)
    with s.part():
        s.tube([(74, 72), (70, 84), (68, 91)], 5, 4, yellow)
        s.tube([(86, 72), (90, 84), (92, 91)], 5, 4, yellow)
    with s.part():
        s.ellipse(80, 60, 14, 16, yellow)
        for y in (52, 60, 68):
            s.curve([(68, y), (74, y + 3), (80, y)], BLACK, 1.6)
    with s.part():
        s.tube([(68, 52), (56, 56), (50, 48)], 4, 3.5, yellow)
        s.tube([(92, 52), (104, 56), (110, 48)], 4, 3.5, yellow)
        s.line([(52, 54), (54, 50)], BLACK, 1.2)
        s.line([(108, 54), (106, 50)], BLACK, 1.2)
    with s.part():
        s.ellipse(80, 34, 11, 10, yellow)
        s.curve([(76, 25), (72, 14), (66, 12)], BLACK, 1.3)
        s.curve([(84, 25), (88, 14), (94, 12)], BLACK, 1.3)
        s.eye(76, 33, 2.2, iris=(60, 40, 30))
        s.eye(85, 33, 2.2, iris=(60, 40, 30))
        s.line([(74, 39), (86, 39)], OUTLINE, 0.9)


@card(21)  # Electrode
def electrode(s):
    s.shadow(80, 93, 24)
    split_ball(s, 80, 64, 26, top=WHITE, bottom=(228, 60, 56), grin=True)


@card(22)  # Pidgeotto
def pidgeotto(s):
    bird(s, (176, 120, 70), (240, 214, 160), (160, 104, 60), crest=[(228, 60, 50), (246, 200, 70)])


# ------------------------------------------------------------------ 23 - 42 uncommons

@card(23)  # Arcanine
def arcanine(s):
    quadruped_dog(s, (240, 140, 60), (246, 230, 180))


@card(24)  # Charmeleon
def charmeleon(s):
    biped_lizard(s, (226, 86, 60), CREAM, horn=True)


@card(25)  # Dewgong
def dewgong(s):
    white = (236, 242, 250)
    with s.part(outline=False, shade=False):
        s.ellipse(80, 92, 56, 7, (200, 230, 250))
    with s.part():
        s.poly([(116, 78), (140, 66), (136, 80), (144, 90), (118, 88)], white)
    with s.part():
        s.ellipse(86, 78, 32, 13, white)
        s.ellipse(70, 86, 9, 4, white, rot=20)
    with s.part():
        s.ellipse(56, 58, 13, 11, white)
        s.ellipse(48, 63, 8, 5, white)
        s.tri((56, 48), (52, 32), (60, 47), (220, 230, 240))
        s.eye(56, 56, 2.2)
        s.ellipse(44, 66, 3, 2, (230, 100, 120))


@card(26)  # Dratini
def dratini(s):
    serpent(s, [(126, 90), (128, 72), (100, 74), (82, 88), (60, 76), (58, 54)], 5, 4.5, (100, 150, 236), WHITE,
            head_at=(58, 46), head_r=8)


@card(27)  # Farfetch'd
def farfetchd(s):
    brown = (168, 120, 80)
    s.shadow(80, 93, 22)
    with s.part():
        s.line([(76, 76), (74, 90)], (230, 160, 70), 1.5)
        s.line([(86, 76), (88, 90)], (230, 160, 70), 1.5)
    with s.part():
        s.ellipse(82, 64, 17, 14, brown)
        s.ellipse(76, 68, 10, 8, (240, 222, 190))
        s.ellipse(92, 62, 10, 7, darker(brown, 0.15), rot=15)
    with s.part():  # leek
        s.line([(58, 80), (100, 30)], (90, 170, 80), 2.4)
        s.line([(58, 80), (64, 73)], WHITE, 2.6)
        s.ellipse(101, 28, 5, 2.5, (70, 150, 60), rot=-50)
    with s.part():
        s.ellipse(70, 44, 9, 8, brown)
        s.ellipse(60, 47, 7, 3, (230, 196, 90))
        s.eye(70, 42, 2.2)
        s.line([(66, 38), (73, 37)], OUTLINE, 1)


@card(28)  # Growlithe
def growlithe(s):
    fur, cream = (240, 140, 60), (246, 230, 180)
    s.shadow(80, 93, 26)
    with s.part():  # bushy tail
        s.ellipse(106, 74, 12, 9, cream, rot=-40)
    with s.part():  # sitting body
        s.ellipse(86, 72, 17, 18, fur)
        for y in (64, 72):
            s.curve([(96, y), (100, y + 4), (98, y + 8)], BLACK, 1.8)
        s.ellipse(96, 86, 9, 6, fur)
    with s.part():  # front legs
        s.tube([(74, 72), (72, 90)], 4, 3.6, fur)
        s.tube([(84, 74), (84, 90)], 4, 3.6, fur)
    with s.part():  # chest fluff
        s.ellipse(76, 64, 10, 11, cream)
    with s.part():
        s.tri((64, 40), (60, 26), (72, 36), fur)
        s.tri((84, 38), (92, 26), (90, 40), fur)
        s.ellipse(74, 46, 14, 12, fur)
        s.ellipse(64, 52, 8, 6, fur)
        s.ellipse(76, 34, 8, 5, cream)
        s.circle(57, 51, 2.2, BLACK)
        s.eye(72, 44, 2.8)
        s.eye(83, 44, 2.6)
        s.curve([(58, 56), (63, 58), (68, 56)], OUTLINE, 0.8)


@card(29)  # Haunter
def haunter(s):
    purple = (120, 82, 168)
    with s.part(outline=False, shade=False):
        s.ellipse(80, 60, 34, 30, (90, 60, 130))
    with s.part():
        pts = [(58, 40), (62, 26), (70, 34), (76, 22), (84, 34), (92, 24), (98, 40), (102, 64), (90, 80), (84, 72), (78, 84), (70, 74), (60, 70)]
        s.poly(pts, purple)
    with s.part():
        s.ellipse(44, 62, 7, 5, purple, rot=-20)
        s.ellipse(118, 54, 7, 5, purple, rot=20)
        for dx in (-3, 0, 3):
            s.ellipse(38 + dx, 58 + abs(dx), 2, 3.5, purple)
            s.ellipse(124 + dx, 50 + abs(dx), 2, 3.5, purple)
    with s.part(outline=False, shade=False):
        s.poly([(68, 46), (76, 42), (76, 50)], WHITE)
        s.poly([(92, 46), (84, 42), (84, 50)], WHITE)
        s.circle(73, 46, 1.6, (200, 40, 60))
        s.circle(87, 46, 1.6, (200, 40, 60))
        s.poly([(68, 56), (92, 56), (86, 66), (74, 66)], (80, 30, 50))
        s.ellipse(80, 64, 5, 3, (230, 100, 140))


@card(30)  # Ivysaur
def ivysaur(s):
    def back(s):
        with s.part():
            s.ellipse(76, 58, 14, 5, (60, 150, 80), rot=25)
            s.ellipse(108, 58, 14, 5, (60, 150, 80), rot=-25)
        with s.part():
            s.ellipse(92, 50, 9, 11, (232, 130, 160))
            s.ellipse(92, 42, 5, 6, (246, 170, 190))
            s.line([(92, 40), (92, 60)], darker((232, 130, 160), 0.3), 0.8)
    quadruped_bulb(s, (100, 170, 160), (70, 130, 120), back)


@card(31)  # Jynx
def jynx(s):
    face, hair, dress = (142, 96, 176), (250, 216, 90), (214, 50, 60)
    s.shadow(80, 93, 24)
    with s.part():  # hair
        s.poly([(64, 30), (96, 30), (106, 70), (54, 70)], hair)
    with s.part():  # dress
        s.poly([(68, 50), (92, 50), (104, 92), (56, 92)], dress)
        s.ellipse(80, 56, 10, 6, WHITE)
    with s.part():
        s.tube([(66, 56), (54, 66), (52, 74)], 3.4, 3, face)
        s.tube([(94, 56), (106, 66), (108, 74)], 3.4, 3, face)
    with s.part():
        s.ellipse(80, 36, 11, 12, face)
        s.ellipse(80, 26, 13, 7, hair)
        s.eye(75, 36, 2, iris=(30, 30, 30))
        s.eye(85, 36, 2, iris=(30, 30, 30))
        s.ellipse(80, 43, 5, 2.4, (238, 120, 150))


@card(32)  # Kadabra
def kadabra(s):
    humanoid_psychic(s, (232, 196, 96), (150, 98, 52), spoons=1, star=True, tail=True)


@card(33)  # Kakuna
def kakuna(s):
    yellow = (240, 210, 80)
    s.shadow(80, 93, 16)
    with s.part():
        s.poly([(70, 30), (92, 28), (98, 50), (92, 76), (80, 92), (70, 80), (64, 52)], yellow)
        for y in (46, 58, 70):
            s.curve([(66, y), (80, y + 3), (96, y)], darker(yellow, 0.3), 0.9)
    with s.part(outline=False, shade=False):
        s.poly([(70, 38), (78, 40), (70, 43)], BLACK)
        s.poly([(90, 38), (82, 40), (90, 43)], BLACK)
        s.ellipse(64, 52, 3, 5, yellow)
        s.ellipse(96, 52, 3, 5, yellow)


@card(34)  # Machoke
def machoke(s):
    muscle_man(s, (156, 150, 190), (220, 170, 170))


@card(35)  # Magikarp
def magikarp(s):
    red, fin = (234, 96, 56), (250, 230, 140)
    with s.part(outline=False, shade=False):
        s.ellipse(80, 92, 46, 6, (180, 220, 250))
        for x in (50, 110):
            s.ellipse(x, 84, 6, 9, (200, 232, 252))
    with s.part():
        s.poly([(110, 54), (132, 36), (128, 56), (134, 76)], fin)
        s.poly([(80, 34), (88, 22), (96, 36)], fin)
    with s.part():
        s.ellipse(80, 56, 30, 22, red, rot=-15)
        for i in range(3):
            s.curve([(84 + i * 8, 44), (88 + i * 8, 54), (84 + i * 8, 66)], darker(red, 0.2), 0.8)
    with s.part():
        s.ellipse(82, 72, 8, 4, fin, rot=20)
    with s.part(outline=False, shade=False):
        s.eye(64, 50, 4.2, look=(0, 0))
        s.ellipse(52, 62, 4, 5, (250, 220, 200))
        s.curve([(56, 58), (44, 52), (40, 58)], fin, 1.2)


@card(36)  # Magmar
def magmar(s):
    yellow, red = (248, 200, 70), (226, 70, 50)
    s.shadow(80, 93, 22)
    with s.part():
        s.tube([(90, 80), (112, 88), (122, 76)], 4, 3, yellow)
    with s.part():
        s.flame(124, 70, 9, rot=20)
    with s.part():
        s.tube([(74, 72), (70, 84), (68, 91)], 5, 4, yellow)
        s.tube([(86, 72), (90, 84), (92, 91)], 5, 4, yellow)
    with s.part():
        s.ellipse(80, 60, 14, 17, yellow)
        s.poly([(66, 52), (80, 58), (94, 52), (90, 70), (70, 70)], red)
    with s.part():
        s.tube([(68, 52), (58, 60), (54, 66)], 3.6, 3, yellow)
        s.tube([(92, 52), (102, 60), (106, 66)], 3.6, 3, yellow)
    with s.part():
        s.flame(80, 22, 9)
        s.ellipse(80, 34, 10, 9, yellow)
        s.ellipse(72, 38, 8, 4, (242, 180, 60))
        s.eye(80, 32, 2.2, iris=(200, 40, 40))


@card(37)  # Nidorino
def nidorino(s):
    body = (176, 116, 196)
    s.shadow(82, 93, 30)
    with s.part():
        for i in range(5):
            s.tri((80 + i * 7, 54), (84 + i * 7, 42), (88 + i * 7, 54), darker(body, 0.15))
    with s.part():
        s.ellipse(86, 66, 24, 13, body)
        for x, y in ((80, 62), (96, 66), (100, 60)):
            s.ellipse(x, y, 3, 2, darker(body, 0.25))
    with s.part():
        for x in (70, 80, 96, 106):
            s.tube([(x, 72), (x, 90)], 4, 3.5, body)
    with s.part():
        s.tri((54, 46), (46, 24), (62, 42), body)
        s.tri((66, 46), (74, 26), (70, 46), body)
        s.ellipse(58, 54, 12, 10, body)
        s.ellipse(48, 58, 7, 5, body)
        s.tri((56, 46), (52, 32), (60, 44), WHITE)
        s.eye(58, 52, 2.4, iris=(200, 40, 40))


@card(38)  # Poliwhirl
def poliwhirl(s):
    blue = (82, 130, 214)
    s.shadow(80, 93, 26)
    with s.part():
        s.tube([(70, 80), (66, 88), (64, 92)], 5, 4, blue)
        s.tube([(90, 80), (94, 88), (96, 92)], 5, 4, blue)
    with s.part():
        s.tube([(60, 56), (48, 58), (42, 50)], 3.4, 3, blue)
        s.tube([(100, 56), (112, 58), (118, 50)], 3.4, 3, blue)
        s.circle(41, 48, 5, WHITE)
        s.circle(119, 48, 5, WHITE)
    with s.part():
        s.circle(80, 60, 22, blue)
        spiral_belly(s, 80, 64, 14)
    with s.part(outline=False, shade=False):
        s.eye(71, 42, 3.4)
        s.eye(89, 42, 3.4)


@card(39)  # Porygon
def porygon(s):
    pink, blue = (240, 120, 150), (90, 190, 220)
    s.shadow(80, 93, 24)
    with s.part():
        s.poly([(92, 66), (118, 70), (112, 80), (92, 76)], blue)
    with s.part():
        s.poly([(66, 52), (96, 50), (102, 70), (74, 76), (62, 66)], pink)
        s.poly([(74, 76), (70, 90), (78, 90), (82, 74)], blue)
        s.poly([(90, 72), (92, 90), (100, 90), (98, 70)], blue)
    with s.part():
        s.poly([(48, 46), (66, 36), (76, 44), (70, 56), (52, 56)], pink)
        s.poly([(48, 46), (36, 50), (52, 56)], blue)
        s.poly([(66, 36), (70, 28), (76, 44)], blue)
        s.eye(64, 46, 2.4)


@card(40)  # Raticate
def raticate(s):
    fur = (186, 130, 82)
    s.shadow(80, 93, 30)
    with s.part():
        s.curve([(104, 76), (128, 84), (140, 70)], (150, 100, 70), 1.8)
    with s.part():
        s.ellipse(88, 70, 22, 15, fur)
        s.ellipse(82, 76, 12, 9, CREAM)
    with s.part():
        for x in (72, 104):
            s.ellipse(x, 88, 7, 4, (230, 190, 150))
    with s.part():
        s.ellipse(66, 44, 6, 7, fur, rot=-20)
        s.ellipse(80, 42, 6, 7, fur, rot=20)
        s.ellipse(70, 56, 13, 11, fur)
        s.ellipse(60, 62, 8, 6, CREAM)
        s.rect(56, 64, 62, 72, WHITE)
        s.eye(70, 52, 2.4)
        s.circle(53, 60, 1.8, BLACK)
        for dy in (-2, 2):
            s.line([(56, 62 + dy), (40, 60 + dy * 3)], OUTLINE, 0.5)


@card(41)  # Seel
def seel(s):
    white = (238, 244, 250)
    with s.part(outline=False, shade=False):
        s.ellipse(80, 92, 50, 7, (200, 230, 250))
    with s.part():
        s.poly([(110, 80), (132, 70), (130, 82), (138, 90), (112, 88)], white)
    with s.part():
        s.ellipse(86, 76, 26, 14, white)
        s.ellipse(70, 88, 8, 4, white, rot=20)
    with s.part():
        s.ellipse(62, 54, 14, 12, white)
        s.ellipse(62, 42, 3, 4, (220, 230, 240))
        s.eye(58, 52, 2.2, squint=True)
        s.eye(68, 52, 2.2, squint=True)
        s.ellipse(56, 62, 3, 3.5, (236, 110, 130))


@card(42)  # Wartortle
def wartortle(s):
    turtle(s, (120, 170, 230), (140, 98, 66), (232, 216, 170), ears=True)


# ------------------------------------------------------------------ 43 - 69 commons

@card(43)  # Abra
def abra(s):
    skin, armor = (232, 196, 96), (150, 98, 52)
    s.shadow(80, 93, 24)
    with s.part():
        s.tube([(94, 82), (114, 88), (118, 78)], 4, 3, skin)
    with s.part():
        s.ellipse(80, 72, 16, 16, armor)
        s.ellipse(72, 88, 8, 4, skin)
        s.ellipse(90, 88, 8, 4, skin)
    with s.part():
        s.tube([(68, 66), (64, 76)], 3.5, 3, skin)
        s.tube([(92, 66), (96, 76)], 3.5, 3, skin)
    with s.part():
        s.tri((68, 46), (60, 26), (76, 40), skin)
        s.tri((92, 46), (100, 26), (84, 40), skin)
        s.ellipse(80, 50, 13, 11, skin)
        s.line([(72, 50), (78, 51)], OUTLINE, 1)
        s.line([(88, 50), (82, 51)], OUTLINE, 1)


@card(44)  # Bulbasaur
def bulbasaur(s):
    def back(s):
        with s.part():
            s.ellipse(92, 56, 14, 13, (90, 170, 110))
            s.curve([(84, 46), (92, 52), (92, 66)], darker((90, 170, 110), 0.3), 0.8)
            s.curve([(100, 46), (94, 52), (94, 66)], darker((90, 170, 110), 0.3), 0.8)
    quadruped_bulb(s, (122, 196, 176), (80, 150, 130), back)


@card(45)  # Caterpie
def caterpie(s):
    green = (130, 196, 90)
    s.shadow(80, 93, 30)
    for i, (x, y) in enumerate([(116, 86), (104, 84), (92, 80), (80, 72)]):
        with s.part():
            s.circle(x, y, 9, green)
            s.circle(x, y + 3, 4, (240, 220, 140))
    with s.part():
        s.curve([(66, 44), (66, 32), (72, 26)], (230, 70, 60), 2.4)
    with s.part():
        s.circle(68, 56, 14, green)
        s.ellipse(58, 62, 6, 5, (240, 220, 140))
        s.eye(64, 52, 4, iris=(30, 30, 30))
        s.ellipse(64, 52, 1.8, 1.8, WHITE)


@card(46)  # Charmander
def charmander(s):
    biped_lizard(s, (242, 140, 66), CREAM, scale=0.95)


@card(47)  # Diglett
def diglett(s):
    with s.part(shade=False):
        s.ellipse(80, 90, 34, 9, (150, 104, 70))
    mole(s, 80, 62, 2.2)
    with s.part(shade=False):
        s.ellipse(80, 91, 30, 6, (136, 92, 60))
        for x in (56, 104):
            s.ellipse(x, 86, 7, 4, (120, 82, 54))


@card(48)  # Doduo
def doduo(s):
    brown, legs = (182, 132, 82), (224, 186, 120)
    s.shadow(80, 93, 22)
    with s.part():
        s.line([(74, 70), (70, 90)], legs, 1.6)
        s.line([(88, 70), (92, 90)], legs, 1.6)
    with s.part():
        s.ellipse(82, 62, 18, 13, brown)
    with s.part():
        s.curve([(74, 54), (66, 44), (62, 34)], darker(brown, 0.15), 2.2)
        s.curve([(88, 52), (94, 40), (100, 30)], darker(brown, 0.15), 2.2)
    for hx, d in ((60, -1), (102, 1)):
        with s.part():
            s.circle(hx, 28, 8, brown)
            s.poly([(hx + d * 6, 27), (hx + d * 16, 30), (hx + d * 6, 32)], (230, 200, 120))
            s.eye(hx + d * 2, 26, 1.8)


@card(49)  # Drowzee
def drowzee(s):
    yellow, brown = (240, 200, 80), (150, 104, 66)
    s.shadow(80, 93, 22)
    with s.part():
        s.tube([(74, 74), (70, 84), (68, 91)], 6, 5, brown)
        s.tube([(86, 74), (90, 84), (92, 91)], 6, 5, brown)
    with s.part():
        s.ellipse(80, 62, 16, 18, yellow)
        s.poly([(64, 68), (96, 68), (96, 80), (64, 80)], brown)
    with s.part():
        s.tube([(66, 54), (56, 60), (52, 66)], 4, 3.5, yellow)
        s.tube([(94, 54), (104, 60), (108, 66)], 4, 3.5, yellow)
    with s.part():
        s.ellipse(80, 36, 13, 11, yellow)
        s.tube([(80, 40), (80, 48), (76, 54)], 3, 2.5, yellow)
        s.line([(72, 34), (77, 35)], OUTLINE, 1)
        s.line([(88, 34), (83, 35)], OUTLINE, 1)


@card(50)  # Gastly
def gastly(s):
    with s.part(outline=False, shade=False):
        s.circle(80, 56, 32, (176, 120, 200))
        s.circle(80, 56, 26, (140, 90, 170))
    with s.part():
        s.circle(80, 56, 18, (50, 40, 60))
    with s.part(outline=False, shade=False):
        s.ellipse(73, 51, 5, 4, WHITE)
        s.ellipse(87, 51, 5, 4, WHITE)
        s.circle(74, 51, 1.6, BLACK)
        s.circle(86, 51, 1.6, BLACK)
        s.curve([(70, 62), (80, 68), (90, 62)], (230, 80, 120), 1.2)
        s.tri((73, 63), (75, 63), (74, 67), WHITE)
        s.tri((85, 63), (87, 63), (86, 67), WHITE)


@card(51)  # Koffing
def koffing(s):
    purple = (136, 100, 170)
    with s.part(outline=False, shade=False):
        for x, y, r in ((52, 40, 8), (110, 36, 9), (116, 70, 7), (46, 72, 6)):
            s.circle(x, y, r, (200, 196, 160))
    s.shadow(80, 93, 20)
    with s.part():
        s.circle(80, 56, 22, purple)
        for x, y in ((66, 42), (96, 46), (70, 70), (98, 66), (82, 38)):
            s.circle(x, y, 3.2, darker(purple, 0.2))
        s.circle(80, 66, 4, (230, 230, 220))
        s.line([(74, 61), (86, 71)], (230, 230, 220), 1.2)
        s.line([(86, 61), (74, 71)], (230, 230, 220), 1.2)
    with s.part(outline=False, shade=False):
        s.eye(72, 52, 2.4)
        s.eye(88, 52, 2.4)
        s.curve([(72, 58), (80, 60), (88, 58)], OUTLINE, 0.8)


@card(52)  # Machop
def machop(s):
    muscle_man(s, (150, 168, 196), (190, 180, 160), scale=0.85)


@card(53)  # Magnemite
def magnemite_card(s):
    s.shadow(80, 93, 18)
    magnemite(s, 80, 56, 15)


@card(54)  # Metapod
def metapod(s):
    green = (110, 176, 90)
    s.shadow(80, 93, 18)
    with s.part():
        s.poly([(66, 28), (90, 30), (98, 54), (92, 78), (78, 92), (70, 80), (78, 60), (68, 42)], green)
        for y in (46, 60, 74):
            s.curve([(72, y), (86, y + 2), (96, y)], darker(green, 0.25), 0.8)
    with s.part(outline=False, shade=False):
        s.poly([(72, 36), (82, 40), (72, 42)], BLACK)


@card(55)  # Nidoran male
def nidoran_m(s):
    body = (194, 130, 196)
    s.shadow(80, 93, 24)
    with s.part():
        for i in range(4):
            s.tri((84 + i * 6, 62), (88 + i * 6, 52), (92 + i * 6, 62), darker(body, 0.15))
    with s.part():
        s.ellipse(90, 72, 18, 11, body)
        for x, y in ((88, 66), (100, 72)):
            s.ellipse(x, y, 2.5, 1.6, darker(body, 0.3))
    with s.part():
        for x in (78, 86, 98, 106):
            s.tube([(x, 78), (x, 90)], 3, 2.6, body)
    with s.part():
        s.tri((58, 50), (40, 22), (66, 44), body)
        s.tri((72, 50), (80, 24), (76, 50), body)
        s.ellipse(64, 60, 11, 9, body)
        s.ellipse(56, 64, 6, 4, body)
        s.tri((62, 52), (60, 40), (66, 50), WHITE)
        s.eye(64, 58, 2.2, iris=(200, 40, 40))


@card(56)  # Onix
def onix(s):
    grey = (160, 160, 166)
    s.shadow(80, 93, 40)
    boulders = [(128, 86, 9), (112, 88, 10), (96, 84, 11), (88, 70, 12), (96, 56, 11), (108, 44, 10), (100, 30, 9)]
    for x, y, r in boulders:
        with s.part():
            s.ellipse(x, y, r * 1.1, r, grey)
            s.curve([(x - r * 0.5, y - r * 0.3), (x, y - r * 0.6), (x + r * 0.4, y - r * 0.2)], darker(grey, 0.25), 0.7)
    with s.part():
        s.tri((88, 18), (98, 4), (96, 18), grey)
        s.ellipse(82, 22, 14, 9, grey)
        s.eye(82, 20, 2.2, iris=(30, 30, 30))
        s.line([(70, 26), (80, 27)], OUTLINE, 0.8)


@card(57)  # Pidgey
def pidgey(s):
    bird(s, (182, 132, 82), (244, 222, 176), (168, 116, 70), flying=False, size=0.9)


@card(58)  # Pikachu
def pikachu(s):
    yellow = (250, 214, 60)
    s.shadow(80, 93, 22)
    with s.part():
        s.poly([(94, 80), (106, 70), (102, 62), (116, 54), (110, 46), (128, 34), (118, 52), (124, 56), (108, 66), (112, 72), (98, 84)], yellow)
        s.poly([(94, 80), (100, 76), (98, 84)], (160, 110, 60))
    with s.part():
        s.ellipse(72, 90, 6, 3.5, yellow)
        s.ellipse(88, 90, 6, 3.5, yellow)
    with s.part():
        s.ellipse(80, 74, 14, 16, yellow)
        s.line([(88, 70), (94, 68)], (160, 110, 60), 2)
        s.line([(88, 76), (94, 75)], (160, 110, 60), 2)
    with s.part():
        s.tube([(68, 70), (64, 76)], 3, 2.6, yellow)
        s.tube([(92, 70), (96, 76)], 3, 2.6, yellow)
    with s.part():  # ears
        s.poly([(68, 46), (50, 18), (74, 40)], yellow)
        s.poly([(92, 46), (110, 18), (86, 40)], yellow)
        s.poly([(53, 23), (50, 18), (58, 26)], BLACK)
        s.poly([(107, 23), (110, 18), (102, 26)], BLACK)
    with s.part():
        s.ellipse(80, 52, 15, 13, yellow)
        s.eye(74, 50, 2.6)
        s.eye(86, 50, 2.6)
        s.circle(80, 54, 0.9, BLACK)
        s.curve([(76, 57), (78, 59), (80, 57), (82, 59), (84, 57)], OUTLINE, 0.7)
        s.circle(69, 56, 3.4, (230, 70, 60))
        s.circle(91, 56, 3.4, (230, 70, 60))


@card(59)  # Poliwag
def poliwag(s):
    blue = (90, 140, 226)
    with s.part():
        s.ellipse(110, 70, 14, 6, (220, 230, 250), rot=-20)
    s.shadow(80, 93, 22)
    with s.part():
        s.ellipse(70, 90, 7, 3.5, blue)
        s.ellipse(90, 90, 7, 3.5, blue)
    with s.part():
        s.circle(80, 66, 20, blue)
        spiral_belly(s, 80, 70, 12)
    with s.part(outline=False, shade=False):
        s.eye(72, 50, 3.4)
        s.eye(88, 50, 3.4)
        s.ellipse(80, 56, 4, 2, (240, 160, 180))


@card(60)  # Ponyta
def ponyta(s):
    cream = (250, 236, 200)
    s.shadow(80, 93, 32)
    with s.part():
        s.flame(116, 56, 14, rot=60)
    with s.part():
        s.tube([(70, 70), (68, 90)], 3, 2.6, darker(cream, 0.08))
        s.tube([(100, 70), (104, 90)], 3, 2.6, darker(cream, 0.08))
    with s.part():
        s.ellipse(86, 64, 22, 11, cream)
    with s.part():
        s.tube([(76, 70), (76, 90)], 3, 2.6, cream)
        s.tube([(94, 70), (96, 90)], 3, 2.6, cream)
        for x in (76, 96):
            s.ellipse(x, 91, 3, 1.6, (150, 140, 130))
    with s.part():
        s.flame(76, 38, 13, rot=-30)
        s.flame(86, 44, 10, rot=-20)
    with s.part():
        s.tube([(70, 58), (62, 46)], 6, 5, cream)
        s.ellipse(56, 40, 9, 7, cream)
        s.ellipse(48, 44, 6, 4, cream)
        s.tri((58, 34), (60, 24), (64, 34), cream)
        s.eye(56, 38, 2.2, iris=(200, 60, 40))


@card(61)  # Rattata
def rattata(s):
    purple = (150, 106, 170)
    s.shadow(80, 93, 26)
    with s.part():
        s.spiral(122, 72, 7, 1.3, purple, 1.6)
        s.curve([(100, 80), (114, 80), (120, 72)], purple, 1.6)
    with s.part():
        s.ellipse(88, 74, 18, 13, purple)
        s.ellipse(80, 80, 9, 7, CREAM)
    with s.part():
        for x in (72, 100):
            s.ellipse(x, 89, 6, 3, (240, 214, 190))
    with s.part():
        s.ellipse(62, 46, 7, 8, purple, rot=-20)
        s.ellipse(80, 46, 7, 8, purple, rot=20)
        s.ellipse(70, 60, 12, 11, purple)
        s.ellipse(60, 64, 7, 6, CREAM)
        s.rect(57, 67, 63, 74, WHITE)
        s.eye(70, 56, 3, iris=(150, 40, 60))
        s.circle(53, 62, 1.6, (220, 120, 140))


@card(62)  # Sandshrew
def sandshrew(s):
    yellow, white = (226, 196, 110), (248, 240, 214)
    s.shadow(80, 93, 22)
    with s.part():
        s.tube([(90, 84), (106, 88), (110, 80)], 3, 2.4, yellow)
    with s.part():
        s.ellipse(72, 89, 7, 4, yellow)
        s.ellipse(90, 89, 7, 4, yellow)
    with s.part():
        s.ellipse(80, 70, 17, 18, yellow)
        s.ellipse(80, 74, 10, 12, white)
        for y in (60, 68):
            s.curve([(64, y), (70, y - 4), (76, y)], (176, 140, 70), 1)
    with s.part():
        s.tube([(66, 64), (58, 70)], 3.4, 3, yellow)
        s.tube([(94, 64), (102, 70)], 3.4, 3, yellow)
        for x in (56, 104):
            for d in (-2, 0, 2):
                s.tri((x + d, 70), (x + d - 1, 76), (x + d + 1, 72), WHITE)
    with s.part():
        s.ellipse(66, 34, 5, 7, yellow, rot=-30)
        s.ellipse(94, 34, 5, 7, yellow, rot=30)
        s.ellipse(80, 46, 15, 13, yellow)
        s.eye(74, 44, 2.4)
        s.eye(86, 44, 2.4)
        s.circle(80, 50, 1, BLACK)


@card(63)  # Squirtle
def squirtle(s):
    blue = (130, 190, 236)
    s.shadow(80, 93, 26)
    with s.part():
        s.spiral(114, 82, 6, 1.2, blue, 2.4)
    turtle_body(s, blue)


def turtle_body(s, blue):
    with s.part():
        s.ellipse(82, 70, 20, 20, (232, 216, 170))
        s.ellipse(82, 70, 17, 17, (176, 120, 70))
    with s.part():
        s.ellipse(70, 89, 7, 4.5, blue)
        s.ellipse(90, 89, 7, 4.5, blue)
    with s.part():
        s.ellipse(80, 72, 14, 16, blue)
        s.ellipse(80, 75, 9, 11, CREAM)
    with s.part():
        s.tube([(68, 66), (60, 72)], 3.4, 3, blue)
        s.tube([(92, 66), (100, 72)], 3.4, 3, blue)
    with s.part():
        s.ellipse(80, 46, 15, 13, blue)
        s.eye(74, 44, 3, iris=(140, 60, 40))
        s.eye(86, 44, 3, iris=(140, 60, 40))
        s.smile(80, 52, 4)


@card(64)  # Starmie
def starmie(s):
    purple, gold = (136, 100, 176), (240, 200, 90)
    s.shadow(80, 93, 26)
    with s.part():
        s.star(80, 56, 32, 13, darker(purple, 0.1), rot=-54)
    with s.part():
        s.star(80, 56, 32, 13, purple, rot=-90)
    with s.part():
        s.circle(80, 56, 9, gold)
        s.circle(80, 56, 6, (220, 50, 70))
        s.circle(78, 54, 2, (255, 200, 210))


@card(65)  # Staryu
def staryu(s):
    brown, gold = (200, 140, 80), (240, 200, 90)
    s.shadow(80, 93, 24)
    with s.part():
        s.star(80, 58, 30, 12, brown, rot=-90)
    with s.part():
        s.circle(80, 58, 8, gold)
        s.circle(80, 58, 5, (220, 50, 70))
        s.circle(78, 56, 1.7, (255, 200, 210))


@card(66)  # Tangela
def tangela(s):
    blue = (70, 110, 180)
    s.shadow(80, 93, 26)
    with s.part():
        s.ellipse(70, 89, 7, 4, (220, 70, 70))
        s.ellipse(90, 89, 7, 4, (220, 70, 70))
    with s.part():
        s.circle(80, 58, 26, blue)
        rng = random.Random(66)
        for _ in range(26):
            x, y = rng.uniform(58, 102), rng.uniform(36, 80)
            s.curve([(x, y), (x + rng.uniform(-8, 8), y + rng.uniform(-6, 6)), (x + rng.uniform(-10, 10), y + rng.uniform(-4, 8))], lighter(blue, 0.3), 1.2)
    with s.part(outline=False, shade=False):
        s.ellipse(80, 60, 14, 6, BLACK)
        s.eye(74, 60, 2.2)
        s.eye(86, 60, 2.2)


@card(67)  # Voltorb
def voltorb(s):
    s.shadow(80, 93, 22)
    split_ball(s, 80, 64, 22, top=(226, 60, 56), bottom=WHITE, grin=False)


@card(68)  # Vulpix
def vulpix(s):
    fur, tails = (196, 92, 60), (226, 120, 70)
    s.shadow(80, 93, 26)
    for i, (x, y) in enumerate([(112, 50), (120, 58), (116, 68), (106, 44), (124, 46), (110, 60)]):
        with s.part():
            s.ellipse(x, y, 7, 5, tails)
            s.spiral(x, y, 4, 1.2, (250, 196, 120), 1)
    with s.part():
        s.ellipse(92, 72, 16, 10, fur)
        s.ellipse(84, 76, 7, 6, (240, 210, 160))
    with s.part():
        for x in (80, 86, 100, 104):
            s.tube([(x, 76), (x, 90)], 2.6, 2.2, fur)
    with s.part():
        s.tri((58, 48), (54, 32), (66, 46), fur)
        s.tri((72, 48), (78, 32), (70, 50), fur)
        s.ellipse(66, 56, 11, 9, fur)
        s.ellipse(58, 60, 6, 4, (240, 210, 160))
        s.spiral(68, 46, 4, 1.3, (230, 120, 70), 1.4)
        s.eye(66, 54, 2.4, iris=(120, 60, 30))
        s.circle(53, 59, 1.4, BLACK)


@card(69)  # Weedle
def weedle(s):
    body = (220, 150, 80)
    s.shadow(80, 93, 30)
    with s.part():
        s.tri((122, 82), (138, 86), (124, 90), WHITE)
    for x, y in [(116, 86), (104, 84), (94, 80), (84, 74)]:
        with s.part():
            s.circle(x, y, 8, body)
    with s.part():
        s.tri((70, 44), (68, 28), (76, 44), WHITE)
        s.circle(72, 58, 13, body)
        s.circle(62, 62, 4, (236, 130, 150))
        s.eye(70, 54, 2.4)
