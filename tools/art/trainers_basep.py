import math

from . import trainers_base1 as base1
from .canvas import OUTLINE, darker, lighter
from .trainers_base1 import BLACK, WHITE

DRAW = {}


def card(number):
    def wrap(fn):
        DRAW[number] = fn
        return fn
    return wrap


@card(16)
def computer_error(s):
    base1.computer_search(s)
    with s.part(outline=False, shade=False):
        s.rect(58, 28, 102, 64, (60, 20, 30))
        for i, w in enumerate((26, 34, 14)):
            s.line([(62, 34 + i * 7), (62 + w, 34 + i * 7)], (250, 90, 90), 1.2)
        s.poly([(80, 46), (90, 62), (70, 62)], (250, 210, 60))
        s.line([(80, 51), (80, 57)], BLACK, 1.2)
        s.circle(80, 60, 0.8, BLACK)
    with s.part(outline=False, shade=False):
        for x, y, r in ((40, 30, 3), (122, 20, 3.5), (126, 60, 2.6)):
            s.star(x, y, r, r * 0.3, (250, 120, 110), points=4, rot=45)


@card(40)
def pokemon_center(s):
    base1.center(s)


@card(41)
def lucky_stadium(s):
    gold, grass = (246, 206, 70), (96, 170, 70)
    s.shadow(80, 93, 60)
    with s.part():
        s.ellipse(80, 82, 64, 12, (176, 176, 186))
        s.ellipse(80, 80, 56, 9, grass)
    with s.part(outline=False, shade=False):
        s.ellipse(80, 80, 28, 4.5, lighter(grass, 0.25))
        s.line([(80, 71), (80, 89)], WHITE, 0.6)
    with s.part():
        for x in (30, 130):
            s.rect(x - 3, 30, x + 3, 80, (200, 200, 210))
            s.circle(x, 28, 6, (250, 240, 190))
    with s.part():
        s.circle(80, 40, 18, gold)
    with s.part(outline=False, shade=False):
        s.circle(80, 40, 13, lighter(gold, 0.35))
        for i in range(4):
            a = math.radians(45 + i * 90)
            s.ellipse(80 + math.cos(a) * 5, 40 + math.sin(a) * 5, 4.5, 4.5, (80, 160, 70))
        s.line([(80, 40), (84, 50)], darker((80, 160, 70), 0.2), 1.2)
    with s.part(outline=False, shade=False):
        for x, y in ((50, 16), (112, 20), (126, 50), (36, 52)):
            s.star(x, y, 4, 1.6, (255, 236, 130))


@card(42)
def pokemon_tower(s):
    stone, roof = (176, 168, 196), (110, 84, 150)
    s.shadow(80, 93, 30)
    with s.part(outline=False, shade=False):
        s.circle(122, 22, 9, (240, 236, 210))
        s.circle(126, 19, 8, (70, 52, 110))
    with s.part():
        s.rect(60, 50, 100, 90, stone)
        s.poly([(56, 52), (80, 40), (104, 52)], roof)
        s.rect(64, 26, 96, 42, stone)
        s.poly([(60, 28), (80, 16), (100, 28)], roof)
        s.rect(70, 6, 90, 18, stone)
        s.poly([(66, 8), (80, -2), (94, 8)], roof)
    with s.part(outline=False, shade=False):
        for y in (58, 72):
            for x in (66, 84):
                s.rect(x, y, x + 10, y + 8, (250, 220, 120))
        for x in (70, 84):
            s.rect(x, 30, x + 6, 38, (250, 220, 120))
        s.rect(76, 9, 84, 15, (250, 220, 120))
    with s.part(outline=False):
        for x, y, side in ((38, 46, 1), (124, 62, -1)):
            s.ellipse(x, y, 8, 10, (236, 236, 250))
            s.poly([(x - 8, y), (x - 8, y + 16), (x - 4, y + 12), (x, y + 16), (x + 4, y + 12), (x + 8, y + 16), (x + 8, y)], (236, 236, 250))
            s.circle(x - 3, y - 1, 1.4, OUTLINE)
            s.circle(x + 3, y - 1, 1.4, OUTLINE)
