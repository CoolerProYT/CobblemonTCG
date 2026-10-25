import math

from .canvas import darker, lighter
from .trainers_base1 import BLACK, RED, WHITE, arrows_circle, capsule, energy_orb, person

DRAW = {}

STONE = (186, 172, 150)


def card(number):
    def wrap(fn):
        DRAW[number] = fn
        return fn
    return wrap


@card(58)
def mr_fuji(s):
    def cane(s, x, y):
        with s.part():
            s.line([(x - 2, y - 4), (x + 2, 92)], (130, 90, 50), 1.6)
            s.curve([(x - 2, y - 4), (x - 2, y - 10), (x - 8, y - 9)], (130, 90, 50), 1.6)
    person(s, 72, (130, 110, 160), (90, 80, 100), (220, 220, 226), holding=cane)
    capsule(s, 120, 70, 9, RED)
    with s.part(outline=False, shade=False):
        for x, y in ((114, 50), (128, 46), (122, 36)):
            s.star(x, y, 3, 1, (255, 236, 160), points=4, rot=0)


@card(59)
def energy_search(s):
    for x, y, col in ((50, 66, (240, 90, 60)), (110, 66, (70, 140, 230)), (80, 74, (110, 190, 80))):
        energy_orb(s, x, y, 13, col)
    with s.part():
        s.circle(86, 34, 16, (210, 230, 246))
        s.line([(98, 46), (112, 60)], (120, 90, 60), 5)
    with s.part(outline=False, shade=False):
        s.circle(86, 34, 12, (236, 246, 252))
        s.circle(81, 29, 3.4, WHITE)


@card(60)
def gambler(s):
    person(s, 54, (200, 60, 60), (40, 40, 50), (60, 40, 30), hair_style="spiky", grin=True)
    with s.part():
        for i, (x, y, rot) in enumerate(((104, 48, -14), (120, 52, 4), (134, 60, 20))):
            a = math.radians(rot)
            pts = [(-9, -13), (9, -13), (9, 13), (-9, 13)]
            s.poly([(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts], WHITE)
    with s.part(outline=False, shade=False):
        for x, y, col in ((104, 48, RED), (120, 52, BLACK), (134, 60, RED)):
            s.star(x, y, 4, 1.8, col, points=4, rot=0)
    with s.part():
        s.circle(112, 82, 6, (246, 206, 80))
        s.circle(126, 86, 5, (246, 206, 80))
    with s.part(outline=False, shade=False):
        s.circle(112, 82, 3.6, lighter((246, 206, 80), 0.3))
        s.circle(126, 86, 3, lighter((246, 206, 80), 0.3))


@card(61)
def recycle(s):
    s.shadow(80, 93, 26)
    with s.part():
        s.poly([(56, 46), (104, 46), (98, 90), (62, 90)], (90, 150, 110))
        s.rect(52, 40, 108, 48, darker((90, 150, 110), 0.15))
    with s.part(outline=False, shade=False):
        for x in (68, 80, 92):
            s.line([(x, 52), (x - 1, 86)], darker((90, 150, 110), 0.25), 1)
    arrows_circle(s, 80, 24, 14, (110, 200, 120))


@card(62)
def mysterious_fossil(s):
    s.shadow(80, 93, 30)
    with s.part():
        s.poly([(48, 90), (44, 64), (58, 44), (86, 36), (110, 46), (118, 70), (112, 90)], STONE)
    with s.part(outline=False, shade=False):
        for y in (58, 70, 82):
            s.curve([(48, y), (80, y - 3), (114, y + 1)], darker(STONE, 0.12), 0.8)
        s.spiral(82, 64, 16, 2.6, (120, 100, 76), 2.2)
        s.circle(82, 64, 2.4, (120, 100, 76))
    with s.part(outline=False, shade=False):
        for x, y in ((50, 30), (118, 26), (128, 58)):
            s.star(x, y, 3.4, 1.2, (255, 232, 170), points=4, rot=0)
