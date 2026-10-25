import math

from . import pokemon_base1 as base1
from . import pokemon_base2 as base2
from .canvas import OUTLINE, Sprite, darker
from .pokemon_base1 import BLACK, RED, WHITE, quadruped_dog

DRAW = {}

YELLOW = (250, 214, 60)
SPARK = (255, 236, 120)


def card(*numbers):
    def wrap(fn):
        for number in numbers:
            DRAW[number] = fn
        return fn
    return wrap


def sparkles(s: Sprite, spots, col=SPARK):
    with s.part(outline=False, shade=False):
        for x, y, r in spots:
            s.star(x, y, r, r * 0.35, col, points=4, rot=0)


@card(1, 4, 27)
def pikachu(s):
    base1.pikachu(s)


@card(26)
def pikachu_sparks(s):
    base2.pikachu(s)


@card(2, 46)
def electabuzz(s):
    base1.electabuzz(s)


@card(3, 12, 14)
def mewtwo(s):
    with s.part(outline=False, shade=False):
        s.circle(122, 40, 9, (190, 150, 230))
        s.circle(122, 40, 6, (236, 214, 250))
    base1.mewtwo(s)


@card(5)
def dragonite(s):
    orange, belly, wing = (240, 168, 74), (248, 226, 160), (96, 168, 150)
    s.shadow(80, 93, 30)
    with s.part():
        s.poly([(92, 50), (130, 26), (136, 36), (124, 40), (128, 50), (104, 60)], wing)
        s.poly([(68, 50), (30, 26), (24, 36), (36, 40), (32, 50), (56, 60)], darker(wing, 0.1))
    with s.part():
        s.tube([(96, 82), (118, 88), (136, 80)], 8, 3, orange)
    with s.part():
        s.ellipse(72, 89, 8, 4, orange)
        s.ellipse(92, 89, 8, 4, orange)
    with s.part():
        s.ellipse(82, 68, 22, 22, orange)
        s.ellipse(80, 72, 14, 17, belly)
        for y in (62, 70, 78):
            s.curve([(68, y), (80, y + 2), (92, y)], darker(belly, 0.15), 0.6)
    with s.part():
        s.tube([(64, 60), (56, 68), (58, 74)], 4, 3.4, orange)
        s.tube([(98, 60), (104, 68), (100, 74)], 4, 3.4, orange)
    with s.part():
        s.curve([(70, 30), (64, 16), (56, 12)], orange, 1.2)
        s.curve([(80, 28), (82, 14), (88, 10)], orange, 1.2)
    with s.part():
        s.ellipse(76, 38, 13, 12, orange)
        s.ellipse(66, 43, 8, 6, orange)
        s.tri((80, 28), (86, 22), (86, 32), belly)
        s.eye(72, 36, 2.4, iris=(40, 30, 30))
        s.circle(60, 42, 0.9, OUTLINE)
        s.smile(66, 47, 3)


def mew_body(s, cx=80, cy=50, flip=1):
    pink = (246, 182, 204)
    with s.part(outline=False, shade=False):
        s.circle(cx, cy + 4, 34, (252, 220, 240))
    with s.part():
        s.tube([(cx + 10 * flip, cy + 12), (cx + 34 * flip, cy + 30), (cx + 54 * flip, cy + 10), (cx + 46 * flip, cy - 20)], 2, 1.4, pink)
        s.ellipse(cx + 46 * flip, cy - 22, 4, 6, pink, rot=20 * flip)
    with s.part():
        s.tube([(cx - 4, cy + 16), (cx - 10, cy + 26)], 3, 2.6, pink)
        s.tube([(cx + 6, cy + 16), (cx + 12, cy + 26)], 3, 2.6, pink)
    with s.part():
        s.ellipse(cx + 1, cy + 6, 10, 13, pink)
    with s.part():
        s.tube([(cx - 6, cy + 2), (cx - 14, cy + 6)], 2.2, 2, pink)
        s.tube([(cx + 8, cy + 2), (cx + 16, cy + 6)], 2.2, 2, pink)
    with s.part():
        s.tri((cx - 12, cy - 16), (cx - 18, cy - 30), (cx - 4, cy - 22), pink)
        s.tri((cx + 10, cy - 18), (cx + 18, cy - 30), (cx + 14, cy - 12), pink)
    with s.part():
        s.ellipse(cx, cy - 12, 15, 13, pink)
        s.eye(cx - 6, cy - 12, 3.4, iris=(70, 120, 220))
        s.eye(cx + 6, cy - 12, 3.4, iris=(70, 120, 220))
        s.smile(cx, cy - 5, 2.2)


@card(8, 9, 47)
def mew(s):
    s.shadow(80, 93, 16)
    mew_body(s)
    sparkles(s, [(36, 22, 4), (124, 70, 3.5), (44, 76, 3), (132, 20, 2.6)], (255, 240, 250))


@card(6)
def arcanine(s):
    base1.arcanine(s)


@card(7)
def jigglypuff(s):
    base2.jigglypuff(s)


@card(10)
def meowth(s):
    base2.meowth(s)


@card(18)
def rocket_meowth(s):
    base2.meowth(s)
    with s.part():
        s.circle(128, 28, 11, (250, 250, 250))
    with s.part(outline=False, shade=False):
        s.line([(124, 34), (124, 22), (130, 22)], RED, 2)
        s.curve([(130, 22), (135, 25), (130, 28)], RED, 2)
        s.line([(126, 28), (133, 34)], RED, 2)


@card(11)
def eevee(s):
    base2.eevee(s)


@card(13)
def venusaur(s):
    base1.venusaur(s)


@card(15)
def cool_porygon(s):
    with s.part(outline=False, shade=False):
        for i in range(6):
            y = 18 + i * 13
            s.line([(18, y), (40, y)], (120, 220, 250), 1)
            s.line([(120, y + 6), (144, y + 6)], (250, 140, 190), 1)
    base1.porygon(s)
    sparkles(s, [(122, 22, 4), (36, 70, 3)], (220, 250, 255))


@card(17)
def dark_persian(s):
    base2.persian(s)
    sparkles(s, [(30, 24, 4), (132, 20, 3.5), (126, 70, 3), (26, 66, 2.6)], (190, 140, 230))


@card(19)
def sabrina_abra(s):
    with s.part(outline=False, shade=False):
        for r, col in ((36, (220, 190, 240)), (26, (236, 214, 250))):
            s.circle(80, 56, r, col)
    base1.abra(s)


@card(20)
def psyduck(s):
    yellow, bill = (250, 214, 90), (246, 226, 176)
    s.shadow(80, 93, 20)
    with s.part():
        s.ellipse(72, 90, 7, 3, bill)
        s.ellipse(90, 90, 7, 3, bill)
    with s.part():
        s.ellipse(80, 74, 16, 16, yellow)
    with s.part():
        s.tube([(66, 70), (58, 60), (62, 50)], 3, 2.6, yellow)
        s.tube([(94, 70), (102, 60), (98, 50)], 3, 2.6, yellow)
    with s.part():
        for x in (76, 80, 84):
            s.curve([(80, 30), (x, 22), (x + 2, 18)], OUTLINE, 0.8)
    with s.part():
        s.ellipse(80, 44, 17, 15, yellow)
        s.eye(73, 42, 3.4, iris=(30, 30, 30))
        s.eye(87, 42, 3.4, iris=(30, 30, 30))
    with s.part():
        s.ellipse(80, 54, 9, 4.5, bill)
        s.line([(73, 54), (87, 54)], darker(bill, 0.3), 0.6)
    with s.part(outline=False, shade=False):
        for x, y in ((52, 30), (108, 30)):
            s.circle(x, y, 2, (150, 110, 220))
            s.circle(x, y, 4, (190, 160, 240))


def legend_bird(s, body, wing, tip, crest, tail, tail_tip=None):
    s.shadow(80, 93, 30)

    def wing_pts(side):
        pts = [(80, 52)]
        for i in range(5):
            x = 80 + side * (16 + i * 11)
            pts.append((x, 24 - i * 2))
            pts.append((x + side * 4, 34 - i))
        pts.append((80 + side * 72, 40))
        pts.append((80 + side * 22, 62))
        return pts

    with s.part():
        s.tube([(84, 66), (100, 82), (120, 90), (140, 86)], 5, 2, tail)
        if tail_tip:
            s.tube([(120, 90), (140, 86)], 3, 2, tail_tip)
    with s.part():
        s.poly(wing_pts(-1), wing)
        s.poly(wing_pts(1), wing)
    with s.part(outline=False):
        s.poly([(8, 40), (24, 26), (34, 38), (22, 46)], tip)
        s.poly([(152, 40), (136, 26), (126, 38), (138, 46)], tip)
    with s.part():
        s.tube([(76, 70), (74, 86)], 1.5, 1.5, (130, 130, 150))
        s.tube([(86, 70), (88, 86)], 1.5, 1.5, (130, 130, 150))
    with s.part():
        s.ellipse(80, 58, 11, 14, body)
    with s.part():
        crest(s)
    with s.part():
        s.tube([(80, 48), (74, 36)], 4, 3.5, body)
        s.ellipse(72, 32, 7, 6, body)
        s.tri((66, 31), (58, 34), (66, 35), (200, 170, 90))
        s.eye(70, 30, 1.8, iris=(40, 30, 30))


@card(21)
def moltres(s):
    orange, fire = (246, 178, 70), (240, 100, 40)

    def crest(s):
        s.flame(76, 22, 9, rot=-20)

    legend_bird(s, orange, orange, fire, crest, orange)
    with s.part(outline=False, shade=False):
        for x, y in ((14, 38), (30, 30), (146, 38), (130, 30)):
            s.flame(x, y, 8)
        s.flame(140, 82, 9, rot=70)


@card(22, 48)
def articuno(s):
    blue, ice = (110, 180, 236), (210, 236, 252)

    def crest(s):
        for i in range(3):
            s.curve([(72, 28), (74 + i * 3, 18 - i * 2), (82 + i * 4, 14 - i)], ice, 2.4 - i * 0.5)

    legend_bird(s, blue, blue, ice, crest, blue, ice)
    with s.part(outline=False, shade=False):
        for x, y in ((40, 16), (118, 14), (130, 66), (30, 66)):
            s.star(x, y, 4, 1.2, (240, 250, 255), points=6, rot=0)


@card(23)
def zapdos(s):
    base1.zapdos(s)


@card(24)
def birthday_pikachu(s):
    with s.part(outline=False, shade=False):
        for x, y, col in ((28, 22, (240, 90, 120)), (40, 40, (90, 170, 240)), (130, 30, (250, 200, 70)), (122, 60, (140, 210, 110))):
            s.rect(x - 1.6, y - 1.6, x + 1.6, y + 1.6, col)
    base1.pikachu(s)
    with s.part():
        s.poly([(70, 42), (82, 14), (90, 40)], (90, 160, 240))
    with s.part(outline=False, shade=False):
        for t in (0.35, 0.65):
            s.line([(70 + 6 * t, 42 - 28 * t), (90 - 4 * t, 40 - 26 * t)], (250, 230, 110), 1.2)
        s.circle(82, 14, 2.6, (250, 90, 110))


@card(25)
def flying_pikachu(s):
    with s.part(outline=False, shade=False):
        for x in (60, 80, 100):
            s.line([(80, 52), (x, 18)], (240, 240, 250), 0.5)
    with s.part():
        s.ellipse(60, 12, 9, 11, (240, 80, 90))
        s.ellipse(100, 12, 9, 11, (90, 160, 240))
        s.ellipse(80, 8, 9, 11, (250, 210, 70))
    with s.part(outline=False, shade=False):
        for x in (57, 77, 97):
            s.ellipse(x, 8, 2, 3.5, (255, 255, 255))
    base1.pikachu(s)


@card(28)
def surfing_pikachu(s):
    sea = (60, 140, 220)
    with s.part(outline=False, shade=False):
        s.poly([(0, 84), (20, 78), (40, 84), (60, 78), (80, 84), (100, 78), (120, 84), (140, 78), (160, 84), (160, 100), (0, 100)], sea)
        for x in (20, 60, 100, 140):
            s.curve([(x - 10, 80), (x, 76), (x + 8, 80)], (220, 240, 255), 1)
    base1.pikachu(s)
    with s.part():
        s.ellipse(80, 92, 40, 4, (250, 200, 70))
    with s.part(outline=False, shade=False):
        s.line([(44, 92), (116, 92)], (230, 90, 60), 1.2)


@card(29)
def marill(s):
    blue, cream = (84, 150, 232), (240, 236, 220)
    s.shadow(80, 93, 22)
    with s.part():
        s.curve([(98, 80), (114, 86), (122, 74)], OUTLINE, 1)
        s.circle(124, 68, 7, blue)
    with s.part():
        s.ellipse(80, 72, 21, 20, blue)
        s.ellipse(80, 80, 12, 10, cream)
    with s.part():
        s.ellipse(70, 91, 6, 3, blue)
        s.ellipse(90, 91, 6, 3, blue)
    with s.part():
        s.circle(64, 42, 9, blue)
        s.circle(96, 42, 9, blue)
    with s.part(outline=False):
        s.circle(64, 42, 5, darker(blue, 0.2))
        s.circle(96, 42, 5, darker(blue, 0.2))
    with s.part(outline=False, shade=False):
        s.eye(72, 64, 2.8, iris=(30, 30, 40))
        s.eye(88, 64, 2.8, iris=(30, 30, 40))
        s.ellipse(80, 70, 3, 2, (250, 140, 160))
        s.smile(80, 73, 2.6)


@card(30)
def togepi(s):
    shell, skin = (250, 248, 240), (250, 232, 170)
    s.shadow(80, 93, 18)
    with s.part():
        s.ellipse(72, 90, 5, 3, skin)
        s.ellipse(88, 90, 5, 3, skin)
    with s.part():
        s.ellipse(80, 72, 17, 18, shell)
    with s.part(outline=False, shade=False):
        for x, y, r, col in ((72, 78, 4, (220, 70, 70)), (88, 74, 4.5, (70, 120, 220)), (80, 86, 3, (220, 70, 70)), (92, 84, 3, (70, 120, 220))):
            s.poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], col)
    with s.part():
        s.tube([(64, 66), (58, 60)], 2.6, 2.2, skin)
        s.tube([(96, 66), (102, 60)], 2.6, 2.2, skin)
    with s.part():
        s.poly([(62, 58), (66, 52), (70, 58), (74, 52), (78, 58), (82, 52), (86, 58), (90, 52), (94, 58), (98, 52), (98, 60), (62, 60)], shell)
    with s.part():
        s.ellipse(80, 46, 15, 12, skin)
        for x in (72, 80, 88):
            s.tri((x - 3, 37), (x, 28), (x + 3, 37), skin)
        s.eye(74, 46, 2, iris=(30, 30, 30), sclera=False)
        s.eye(86, 46, 2, iris=(30, 30, 30), sclera=False)
        s.smile(80, 50, 2.4)


@card(31)
def cleffa(s):
    pink = (246, 180, 194)
    s.shadow(80, 93, 18)
    with s.part():
        s.ellipse(73, 90, 5, 3, pink)
        s.ellipse(87, 90, 5, 3, pink)
    with s.part():
        s.ellipse(80, 82, 9, 8, pink)
    with s.part():
        s.tri((60, 56), (52, 40), (68, 48), pink)
        s.tri((100, 56), (108, 40), (92, 48), pink)
        s.tri((58, 54), (54, 44), (64, 50), (90, 60, 70))
        s.tri((102, 54), (106, 44), (96, 50), (90, 60, 70))
    with s.part():
        s.ellipse(80, 60, 22, 18, pink)
    with s.part(outline=False):
        s.spiral(80, 42, 4, 1.4, pink, 2.2)
    with s.part(outline=False, shade=False):
        s.eye(72, 60, 2, iris=(30, 30, 40), sclera=False)
        s.eye(88, 60, 2, iris=(30, 30, 40), sclera=False)
        s.circle(66, 66, 2.6, (250, 140, 160))
        s.circle(94, 66, 2.6, (250, 140, 160))
        s.smile(80, 66, 2)
    sparkles(s, [(126, 24, 4), (36, 30, 3)])


@card(32)
def smeargle(s):
    cream, brown = (240, 230, 200), (140, 108, 70)
    s.shadow(80, 93, 22)
    with s.part(outline=False, shade=False):
        for x, y, col in ((30, 80, (240, 90, 90)), (40, 86, (90, 160, 240)), (120, 86, (250, 210, 70))):
            s.ellipse(x, y, 8, 3, col)
    with s.part():
        s.tube([(94, 70), (110, 60), (120, 40), (116, 26)], 3, 2.2, cream)
        s.ellipse(116, 22, 4, 6, (110, 200, 110))
    with s.part():
        s.tube([(74, 76), (72, 91)], 3.6, 3, cream)
        s.tube([(86, 76), (88, 91)], 3.6, 3, cream)
    with s.part():
        s.ellipse(80, 66, 12, 14, cream)
        s.ellipse(80, 54, 9, 5, brown)
    with s.part():
        s.tube([(70, 60), (62, 68)], 2.6, 2.2, cream)
        s.tube([(90, 60), (98, 66)], 2.6, 2.2, cream)
    with s.part():
        s.tri((70, 30), (62, 14), (76, 26), cream)
        s.tri((90, 30), (96, 14), (84, 26), cream)
    with s.part():
        s.ellipse(80, 38, 13, 12, cream)
        s.ellipse(80, 28, 13, 5, brown)
        s.eye(75, 38, 2.2, iris=(30, 30, 30), sclera=False)
        s.eye(86, 38, 2.2, iris=(30, 30, 30), sclera=False)
        s.smile(80, 44, 2)


@card(33)
def scizor(s):
    red, grey = (214, 54, 50), (120, 120, 132)
    s.shadow(80, 93, 26)
    with s.part():
        s.ellipse(100, 48, 16, 6, (236, 240, 248), rot=-30)
        s.ellipse(104, 56, 14, 5, (236, 240, 248), rot=-5)
    with s.part():
        s.tube([(88, 74), (96, 84), (94, 91)], 3, 2.6, grey)
        s.tube([(76, 74), (72, 84), (70, 91)], 3, 2.6, grey)
    with s.part():
        s.ellipse(92, 70, 12, 8, red, rot=30)
        s.line([(86, 64), (98, 76)], grey, 1.2)
    with s.part():
        s.ellipse(78, 58, 9, 13, red)
        s.line([(72, 58), (84, 58)], grey, 1.4)
    with s.part():
        s.tube([(72, 52), (60, 52), (50, 46)], 3, 3, red)
        s.tube([(84, 52), (96, 46), (104, 36)], 3, 3, red)
    with s.part():
        for cx, cy, rot in ((42, 40, -30), (110, 26, 30)):
            s.ellipse(cx, cy, 12, 9, red, rot=rot)
    with s.part(outline=False, shade=False):
        for cx, cy, rot in ((42, 40, -30), (110, 26, 30)):
            a = math.radians(rot)
            s.line([(cx - 10 * math.cos(a), cy - 10 * math.sin(a)), (cx - 2 * math.cos(a), cy - 2 * math.sin(a))], OUTLINE, 1)
            for dx in (-4, 4):
                s.circle(cx + dx * math.sin(a) * 0.9 + 2, cy - dx * math.cos(a) * 0.9 + 2, 1.4, (40, 30, 40))
    with s.part():
        s.ellipse(74, 36, 9, 8, red)
        s.tri((76, 28), (88, 20), (82, 32), red)
        s.ellipse(73, 35, 3.6, 2.4, (240, 220, 80), rot=-20)


@card(34)
def entei(s):
    brown, mane, grey = (164, 104, 62), (236, 226, 208), (150, 150, 160)
    with s.part(outline=False, shade=False):
        s.flame(122, 30, 12)
        s.flame(30, 36, 10)
    quadruped_dog(s, brown, mane, stripes=False)
    with s.part():
        s.poly([(48, 32), (40, 14), (56, 26), (60, 10), (66, 28), (74, 18), (70, 36)], grey)
    with s.part(outline=False, shade=False):
        s.poly([(44, 46), (36, 48), (44, 50)], grey)
        s.line([(50, 38), (58, 36)], (250, 210, 80), 0.8)


@card(35)
def pichu(s):
    yellow = (250, 222, 90)
    s.shadow(80, 93, 16)
    with s.part():
        s.poly([(92, 82), (104, 74), (100, 70), (110, 64)], yellow)
        s.line([(92, 82), (104, 74), (100, 70), (110, 64)], darker(yellow, 0.4), 0.6)
    with s.part():
        s.ellipse(74, 90, 4.5, 3, yellow)
        s.ellipse(86, 90, 4.5, 3, yellow)
    with s.part():
        s.ellipse(80, 78, 10, 12, yellow)
    with s.part():
        s.poly([(66, 50), (44, 30), (52, 54)], yellow)
        s.poly([(94, 50), (116, 30), (108, 54)], yellow)
        s.poly([(44, 30), (50, 34), (46, 40)], BLACK)
        s.poly([(116, 30), (110, 34), (114, 40)], BLACK)
    with s.part():
        s.ellipse(80, 58, 15, 13, yellow)
        s.eye(74, 56, 2.4)
        s.eye(86, 56, 2.4)
        s.circle(80, 60, 0.8, BLACK)
        s.smile(80, 62, 2)
        s.circle(69, 62, 3, (250, 130, 140))
        s.circle(91, 62, 3, (250, 130, 140))
    with s.part(outline=False, shade=False):
        s.bolt(40, 70, 6, SPARK, rot=-15)
        s.bolt(124, 46, 5, SPARK, rot=20)


@card(36)
def igglybuff(s):
    base2.puff(s, 18, cy=70, ears=0.7)


@card(37)
def hitmontop(s):
    brown, blue, white = (170, 120, 80), (70, 110, 190), (240, 240, 244)
    with s.part(outline=False, shade=False):
        for r in (28, 22):
            s.ellipse(80, 88, r, r * 0.22, (220, 220, 230))
    s.shadow(80, 93, 20)
    with s.part():
        s.tube([(70, 56), (52, 80), (46, 88)], 3.6, 3, brown)
        s.tube([(90, 56), (110, 76), (118, 82)], 3.6, 3, brown)
    with s.part():
        s.ellipse(80, 62, 14, 12, blue)
        s.ellipse(80, 66, 9, 6, white)
    with s.part():
        s.tube([(70, 54), (54, 46)], 3, 2.6, brown)
        s.tube([(90, 54), (104, 44)], 3, 2.6, brown)
        s.circle(52, 46, 3.6, white)
        s.circle(106, 44, 3.6, white)
    with s.part():
        s.ellipse(80, 40, 11, 10, brown)
        s.tri((76, 30), (80, 16), (84, 30), brown)
        s.eye(76, 40, 2, iris=(40, 30, 30), sclera=False)
        s.eye(84, 40, 2, iris=(40, 30, 30), sclera=False)
        s.line([(74, 37), (79, 38)], OUTLINE, 0.7)
        s.line([(86, 37), (81, 38)], OUTLINE, 0.7)


@card(38)
def unown(s):
    black = (50, 48, 58)
    s.shadow(80, 93, 12)
    with s.part(outline=False, shade=False):
        for r, col in ((34, (210, 190, 240)), (24, (234, 222, 250))):
            s.circle(80, 50, r, col)
    with s.part():
        s.tube([(92, 22), (92, 64), (88, 76), (76, 78), (68, 70)], 4, 4, black)
        s.tube([(84, 22), (100, 22)], 3, 3, black)
    with s.part(outline=False):
        s.circle(88, 76, 7, WHITE)
        s.circle(88, 76, 3, black)
        s.circle(87, 75, 1, WHITE)


@card(39)
def misdreavus(s):
    teal, red = (92, 110, 152), (200, 60, 110)
    with s.part(outline=False, shade=False):
        s.circle(80, 50, 34, (196, 170, 220))
    with s.part():
        s.poly([(58, 54), (48, 76), (60, 70), (66, 82), (72, 70), (80, 84), (88, 70), (94, 82), (100, 70), (112, 76), (102, 54)], teal)
    with s.part():
        s.ellipse(80, 50, 20, 18, teal)
    with s.part():
        for x in (68, 80, 92):
            s.circle(x, 68, 3.6, red)
    with s.part(outline=False, shade=False):
        s.eye(73, 48, 3.6, iris=(200, 40, 60))
        s.eye(87, 48, 3.6, iris=(200, 40, 60))
        s.curve([(74, 58), (80, 60), (86, 58)], OUTLINE, 0.7)


@card(43)
def machamp(s):
    base1.machamp(s)


@card(44)
def magmar(s):
    base1.magmar(s)


@card(45)
def scyther(s):
    base2.scyther(s)


@card(49)
def snorlax(s):
    base2.snorlax(s)


@card(50)
def celebi(s):
    green, eye = (150, 214, 110), (60, 150, 220)
    with s.part(outline=False, shade=False):
        s.circle(80, 48, 32, (220, 246, 200))
    with s.part():
        s.ellipse(104, 40, 16, 7, (236, 252, 240), rot=-30)
        s.ellipse(56, 40, 16, 7, (236, 252, 240), rot=30)
    with s.part():
        s.tube([(76, 64), (74, 76)], 2.4, 2, green)
        s.tube([(84, 64), (86, 76)], 2.4, 2, green)
    with s.part():
        s.ellipse(80, 56, 8, 10, green)
    with s.part():
        s.tube([(74, 52), (64, 58)], 2, 1.8, green)
        s.tube([(86, 52), (96, 58)], 2, 1.8, green)
    with s.part():
        s.tri((70, 30), (58, 14), (76, 24), green)
        s.tri((90, 30), (102, 14), (84, 24), green)
    with s.part():
        s.ellipse(80, 36, 13, 11, green)
        s.ellipse(73, 36, 4, 5, (30, 30, 40))
        s.ellipse(87, 36, 4, 5, (30, 30, 40))
        s.ellipse(73, 37, 3, 3.6, eye)
        s.ellipse(87, 37, 3, 3.6, eye)
        s.circle(72, 35, 1, WHITE)
        s.circle(86, 35, 1, WHITE)
        s.smile(80, 42, 1.8)
    sparkles(s, [(34, 70, 3), (128, 66, 3.5), (122, 18, 2.6)], (240, 255, 220))


@card(51)
def rapidash(s):
    base2.rapidash(s)


@card(52)
def ho_oh(s):
    red, gold, green = (214, 60, 50), (250, 200, 70), (90, 180, 110)

    def crest(s):
        s.curve([(72, 28), (78, 16), (90, 12)], gold, 2.4)
        s.curve([(72, 28), (80, 20), (94, 20)], gold, 1.8)

    legend_bird(s, red, red, gold, crest, green, gold)
    with s.part(outline=False, shade=False):
        for side in (-1, 1):
            for i in range(4):
                x = 80 + side * (24 + i * 12)
                s.line([(x, 36 - i), (x + side * 4, 50 - i)], gold, 1.4)
        s.ellipse(80, 64, 7, 9, (246, 230, 190))
    sparkles(s, [(30, 76, 4), (130, 70, 3), (80, 6, 3)], (255, 220, 120))


@card(53)
def suicune(s):
    blue, ribbon, crest = (110, 196, 230), (240, 240, 250), (176, 120, 200)
    with s.part(outline=False, shade=False):
        for x, y in ((24, 30), (136, 24), (130, 60)):
            s.circle(x, y, 4, (220, 246, 255))
            s.circle(x, y, 2, (255, 255, 255))
    s.shadow(84, 93, 32)
    with s.part():
        s.curve([(110, 56), (134, 44), (146, 60)], ribbon, 3)
        s.curve([(110, 60), (136, 64), (144, 80)], ribbon, 3)
    with s.part():
        s.tube([(106, 66), (110, 80), (108, 90)], 4.5, 3.6, blue)
        s.tube([(66, 66), (64, 80), (62, 90)], 4.5, 3.6, darker(blue, 0.1))
    with s.part():
        s.ellipse(88, 62, 25, 12, blue)
    with s.part(outline=False, shade=False):
        for x in (80, 92, 104):
            s.poly([(x - 4, 56), (x, 60), (x + 4, 56), (x, 64)], ribbon)
    with s.part():
        s.tube([(70, 68), (70, 82), (70, 91)], 4.5, 3.6, blue)
        s.tube([(98, 70), (100, 82), (100, 91)], 4.5, 3.6, blue)
    with s.part():
        s.curve([(66, 42), (90, 30), (110, 40)], crest, 6)
    with s.part():
        s.ellipse(56, 44, 11, 10, blue)
        s.ellipse(46, 48, 7, 5, blue)
        s.poly([(56, 34), (62, 18), (66, 36)], ribbon)
        s.ellipse(60, 36, 8, 4, ribbon)
        s.circle(40, 47, 1.6, BLACK)
        s.eye(52, 42, 2.4, iris=(170, 40, 60))
        s.curve([(41, 52), (46, 54), (50, 52)], OUTLINE, 0.7)
