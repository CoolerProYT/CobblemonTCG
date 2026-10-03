"""
Original illustrations for the Base Set Trainer cards, one function per card number.
Stage is 160 x 100 units.
"""
import math

from .canvas import OUTLINE, Sprite, darker, lighter

WHITE = (246, 246, 250)
SKIN = (246, 206, 170)
BLACK = (40, 36, 42)
SILVER = (196, 200, 210)
RED = (222, 58, 52)
ENERGY_RED = (232, 104, 64)

DRAW = {}


def card(number):
    def wrap(fn):
        DRAW[number] = fn
        return fn
    return wrap


# ------------------------------------------------------------------ helpers

def person(s: Sprite, x, coat, pants, hair, hair_style="short", glasses=False, grin=False, holding=None, skirt=False, apron=None):
    """A simple standing person, head around y = 26, feet at y = 92."""
    s.shadow(x, 93, 18)
    with s.part():  # legs
        if skirt:
            s.tube([(x - 4, 74), (x - 5, 91)], 3, 2.6, SKIN)
            s.tube([(x + 4, 74), (x + 5, 91)], 3, 2.6, SKIN)
        else:
            s.tube([(x - 5, 66), (x - 6, 91)], 4, 3.6, pants)
            s.tube([(x + 5, 66), (x + 6, 91)], 4, 3.6, pants)
        s.ellipse(x - 7, 92, 5, 2.4, BLACK)
        s.ellipse(x + 7, 92, 5, 2.4, BLACK)
    with s.part():  # body
        if skirt:
            s.poly([(x - 10, 44), (x + 10, 44), (x + 16, 76), (x - 16, 76)], coat)
        else:
            s.poly([(x - 12, 42), (x + 12, 42), (x + 14, 76), (x - 14, 76)], coat)
            s.line([(x, 44), (x, 74)], darker(coat, 0.25), 0.8)
        if apron:
            s.poly([(x - 9, 52), (x + 9, 52), (x + 11, 76), (x - 11, 76)], apron)
    with s.part():  # arms
        s.tube([(x - 12, 46), (x - 16, 58), (x - 14, 68)], 3.4, 3, coat)
        s.tube([(x + 12, 46), (x + 18, 56), (x + 20, 60)], 3.4, 3, coat)
        s.circle(x - 14, 69, 2.6, SKIN)
        s.circle(x + 21, 61, 2.6, SKIN)
    if holding:
        holding(s, x + 23, 60)
    with s.part():  # head and hair
        if hair_style == "long":
            s.poly([(x - 11, 22), (x + 11, 22), (x + 12, 46), (x - 12, 46)], hair)
        s.ellipse(x, 28, 10, 11, SKIN)
        if hair_style == "spiky":
            s.poly([(x - 11, 26), (x - 12, 14), (x - 6, 18), (x - 2, 10), (x + 3, 17), (x + 9, 12), (x + 11, 26), (x + 6, 20), (x - 6, 20)], hair)
        else:
            s.ellipse(x, 20, 11, 7, hair)
            s.rect(x - 11, 20, x - 8, 30, hair)
            s.rect(x + 8, 20, x + 11, 30, hair)
        if glasses:
            s.rect(x - 8, 26, x - 1, 30, BLACK)
            s.rect(x + 1, 26, x + 8, 30, BLACK)
            s.line([(x - 1, 27), (x + 1, 27)], BLACK, 0.6)
        else:
            s.eye(x - 4, 28, 1.6, sclera=False)
            s.eye(x + 4, 28, 1.6, sclera=False)
        if grin:
            s.curve([(x - 5, 33), (x, 37), (x + 5, 33)], OUTLINE, 0.9)
        else:
            s.smile(x, 33, 3, depth=0.8)


def spray_bottle(s, cx, cy, body, cap, mist=True, scale=1.0):
    k = scale
    if mist:
        with s.part(outline=False, shade=False):
            for i in range(9):
                a = math.radians(-160 + i * 12)
                r = 16 + (i % 3) * 5
                s.circle(cx - 18 * k + r * math.cos(a) * k, cy - 26 * k + r * math.sin(a) * 0.6 * k, 1.6 + (i % 2), lighter(body, 0.5))
    with s.part():
        s.rect(cx - 10 * k, cy - 14 * k, cx + 10 * k, cy + 22 * k, body)
        s.ellipse(cx, cy + 22 * k, 10 * k, 3 * k, body)
        s.rect(cx - 6 * k, cy - 6 * k, cx + 6 * k, cy + 10 * k, WHITE)
    with s.part():
        s.rect(cx - 4 * k, cy - 22 * k, cx + 4 * k, cy - 14 * k, cap)
        s.poly([(cx - 4 * k, cy - 22 * k), (cx - 16 * k, cy - 26 * k), (cx - 16 * k, cy - 22 * k), (cx - 4 * k, cy - 18 * k)], cap)
        s.poly([(cx + 4 * k, cy - 16 * k), (cx + 10 * k, cy - 8 * k), (cx + 6 * k, cy - 6 * k)], cap)


def energy_orb(s, cx, cy, r, col, glyph="star"):
    with s.part():
        s.circle(cx, cy, r, col)
        s.circle(cx - r * 0.3, cy - r * 0.3, r * 0.35, lighter(col, 0.5))
        if glyph == "star":
            s.star(cx, cy, r * 0.6, r * 0.25, WHITE)


def big_x(s, cx, cy, r, col=RED):
    with s.part():
        s.line([(cx - r, cy - r), (cx + r, cy + r)], col, 5)
        s.line([(cx + r, cy - r), (cx - r, cy + r)], col, 5)


def arrows_circle(s, cx, cy, r, col):
    with s.part():
        for start in (20, 200):
            pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(start, start + 140, 6)]
            s.line(pts, col, 3)
            end = pts[-1]
            a = math.radians(start + 140)
            tip = (end[0] - 7 * math.sin(a), end[1] + 7 * math.cos(a))
            s.tri((end[0] + 6 * math.cos(a), end[1] + 6 * math.sin(a)), (end[0] - 6 * math.cos(a), end[1] - 6 * math.sin(a)), tip, col)


def capsule(s, cx, cy, r, top, bottom=WHITE):
    """A generic monster capsule: two coloured halves and a button."""
    with s.part():
        s.circle(cx, cy, r, bottom)
        s.poly([(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in range(0, 181, 6)], top)
    with s.part(outline=False, shade=False):
        s.line([(cx - r, cy), (cx + r, cy)], OUTLINE, 1.2)
        s.circle(cx, cy, r * 0.28, OUTLINE)
        s.circle(cx, cy, r * 0.18, WHITE)


# ------------------------------------------------------------------ rares

@card(70)  # Clefairy Doll
def clefairy_doll(s):
    pink = (236, 176, 186)
    s.shadow(80, 93, 22)
    with s.part():
        s.tri((64, 44), (56, 22), (74, 38), pink)
        s.tri((96, 44), (104, 22), (86, 38), pink)
    with s.part():
        s.ellipse(80, 66, 20, 24, pink)
        s.ellipse(68, 88, 6, 4, pink)
        s.ellipse(92, 88, 6, 4, pink)
    with s.part(outline=False, shade=False):
        for y in range(46, 88, 5):
            s.line([(80, y), (80, y + 2)], darker(pink, 0.4), 0.6)
        s.circle(73, 56, 2.6, BLACK)
        s.circle(87, 56, 2.6, BLACK)
        s.circle(72, 55, 0.8, WHITE)
        s.circle(86, 55, 0.8, WHITE)
        s.line([(77, 63), (83, 63)], darker(pink, 0.5), 0.7)
    with s.part():  # price tag
        s.poly([(98, 72), (112, 66), (116, 76), (102, 82)], (250, 240, 200))
        s.circle(101, 75, 1, BLACK)


@card(71)  # Computer Search
def computer_search(s):
    beige = (226, 220, 200)
    s.shadow(80, 93, 36)
    with s.part():
        s.poly([(50, 82), (110, 82), (118, 92), (42, 92)], beige)
        for i in range(5):
            s.line([(52 + i * 12, 87), (60 + i * 12, 87)], darker(beige, 0.3), 1)
    with s.part():
        s.rect(52, 22, 108, 74, beige)
        s.rect(58, 28, 102, 64, (40, 70, 90))
        s.rect(74, 74, 86, 82, beige)
    with s.part(outline=False, shade=False):
        for i, w in enumerate((30, 22, 34, 18)):
            s.line([(62, 34 + i * 7), (62 + w, 34 + i * 7)], (120, 240, 160), 1.2)
        s.circle(92, 56, 5, (120, 240, 160))
        s.line([(95, 59), (99, 63)], (120, 240, 160), 1.4)


@card(72)  # Devolution Spray
def devolution_spray(s):
    s.shadow(80, 93, 18)
    spray_bottle(s, 84, 58, (150, 90, 190), (90, 60, 120), scale=1.3)


@card(73)  # Impostor Professor Oak
def impostor_oak(s):
    person(s, 80, WHITE, (110, 110, 140), (60, 50, 60), glasses=True, grin=True)
    with s.part():  # false moustache
        s.ellipse(80, 31, 6, 1.8, (90, 70, 60))


@card(74)  # Item Finder
def item_finder(s):
    s.shadow(80, 93, 22)
    with s.part():
        s.line([(98, 36), (110, 14)], SILVER, 1.6)
        s.circle(110, 13, 2.6, RED)
    with s.part():
        s.rect(60, 34, 104, 84, (90, 150, 200))
        s.rect(66, 40, 98, 66, (30, 50, 40))
        s.circle(72, 76, 4, RED)
        s.circle(86, 76, 4, (250, 210, 60))
    with s.part(outline=False, shade=False):
        for r in (4, 8, 12):
            s.line([(82 + r * math.cos(math.radians(a)), 53 + r * 0.8 * math.sin(math.radians(a))) for a in range(0, 361, 10)], (100, 220, 130), 0.6)
        s.line([(82, 53), (92, 46)], (100, 220, 130), 1)
        s.circle(90, 58, 1.6, (250, 250, 120))


@card(75)  # Lass
def lass(s):
    person(s, 80, (240, 120, 150), (60, 60, 80), (120, 70, 40), hair_style="long", skirt=True)


@card(76)  # Pokemon Breeder
def breeder(s):
    def egg(s, x, y):
        with s.part():
            s.ellipse(x, y - 4, 7, 9, (250, 244, 220))
            s.circle(x - 2, y - 7, 1.6, (130, 200, 140))
            s.circle(x + 3, y - 2, 1.4, (130, 200, 140))
    person(s, 74, (120, 170, 120), (90, 80, 70), (90, 60, 40), apron=(250, 246, 230), holding=egg)


@card(77)  # Pokemon Trader
def trader(s):
    person(s, 52, (90, 120, 190), (60, 60, 80), (60, 40, 30), hair_style="spiky")
    capsule(s, 100, 46, 10, (70, 130, 220))
    capsule(s, 126, 66, 10, (90, 190, 110))
    with s.part():
        s.curve([(108, 40), (124, 40), (128, 52)], (250, 200, 60), 2)
        s.tri((124, 52), (132, 52), (128, 58), (250, 200, 60))
        s.curve([(118, 72), (102, 72), (98, 60)], (250, 200, 60), 2)
        s.tri((94, 60), (102, 60), (98, 54), (250, 200, 60))


@card(78)  # Scoop Up
def scoop_up(s):
    s.shadow(80, 93, 28)
    with s.part():
        s.line([(40, 30), (74, 60)], (160, 120, 70), 2.4)
    with s.part():
        s.ellipse(92, 70, 24, 14, (230, 230, 236), rot=-10)
    with s.part(outline=False, shade=False):
        for i in range(-3, 4):
            s.line([(92 + i * 6, 58), (92 + i * 5, 82)], (170, 170, 180), 0.6)
        for j in range(-2, 3):
            s.line([(70, 70 + j * 4), (114, 68 + j * 4)], (170, 170, 180), 0.6)
    capsule(s, 94, 68, 8, RED)


@card(79)  # Super Energy Removal
def super_energy_removal(s):
    energy_orb(s, 60, 54, 18, (240, 200, 70))
    energy_orb(s, 100, 54, 18, (100, 160, 230))
    big_x(s, 60, 54, 16)
    big_x(s, 100, 54, 16)


# ------------------------------------------------------------------ uncommons

@card(80)  # Defender
def defender(s):
    s.shadow(80, 93, 20)
    with s.part():
        s.poly([(80, 18), (106, 28), (102, 62), (80, 88), (58, 62), (54, 28)], (150, 170, 200))
        s.poly([(80, 26), (98, 34), (95, 60), (80, 78), (65, 60), (62, 34)], (90, 120, 180))
        s.star(80, 50, 10, 4, (250, 220, 90))


@card(81)  # Energy Retrieval
def energy_retrieval(s):
    arrows_circle(s, 80, 54, 30, (90, 180, 110))
    energy_orb(s, 80, 54, 14, (232, 104, 64))


@card(82)  # Full Heal
def full_heal(s):
    s.shadow(80, 93, 16)
    with s.part():
        s.rect(68, 40, 92, 88, (250, 230, 120))
        s.rect(72, 30, 88, 40, (230, 230, 240))
        s.rect(74, 22, 86, 30, (90, 160, 220))
    with s.part(outline=False, shade=False):
        s.rect(72, 54, 88, 76, WHITE)
        s.rect(78, 57, 82, 73, RED)
        s.rect(73, 63, 87, 67, RED)


@card(83)  # Maintenance
def maintenance(s):
    with s.part():
        s.line([(50, 80), (106, 30)], SILVER, 4)
        s.circle(108, 28, 8, SILVER)
        s.circle(112, 24, 4, (190, 220, 240))
    with s.part():
        s.line([(50, 30), (96, 74)], (230, 90, 60), 4.4)
        s.line([(96, 74), (110, 88)], SILVER, 1.6)


@card(84)  # PlusPower
def pluspower(s):
    s.shadow(80, 93, 20)
    with s.part():
        s.circle(80, 54, 26, (226, 60, 56))
        s.circle(80, 54, 20, (250, 200, 70))
        s.rect(76, 40, 84, 68, WHITE)
        s.rect(66, 50, 94, 58, WHITE)


@card(85)  # Pokemon Center
def center(s):
    s.shadow(80, 93, 50)
    with s.part():
        s.rect(36, 44, 124, 90, (246, 240, 230))
        s.poly([(30, 46), (80, 20), (130, 46)], (220, 60, 60))
    with s.part(outline=False, shade=False):
        s.rect(70, 66, 90, 90, (120, 180, 220))
        s.line([(80, 66), (80, 90)], OUTLINE, 0.6)
        for x in (44, 104):
            s.rect(x, 54, x + 12, 64, (120, 180, 220))
        s.circle(80, 36, 6, WHITE)
        s.rect(78, 32, 82, 40, RED)
        s.rect(76, 34, 84, 38, RED)


@card(86)  # Pokemon Flute
def flute(s):
    with s.part():
        s.line([(38, 70), (118, 40)], (226, 214, 180), 6)
    with s.part(outline=False, shade=False):
        for i in range(5):
            x = 54 + i * 12
            s.circle(x, 64 - i * 4.5, 1.6, (120, 90, 60))
    with s.part():
        for x, y in ((106, 24), (124, 30), (116, 12)):
            s.ellipse(x, y, 3.2, 2.4, BLACK, rot=-20)
            s.line([(x + 3, y), (x + 3, y - 10)], BLACK, 0.8)


@card(87)  # Pokedex
def pokedex(s):
    s.shadow(80, 93, 24)
    with s.part():
        s.rect(56, 26, 104, 86, (214, 50, 50))
        s.rect(62, 34, 98, 62, (200, 230, 200))
    with s.part(outline=False, shade=False):
        s.circle(64, 22, 5, (120, 200, 250))
        s.circle(72, 22, 2, (250, 90, 90))
        s.circle(78, 22, 2, (250, 220, 90))
        s.line([(66, 42), (90, 42)], (60, 120, 70), 1)
        s.line([(66, 48), (84, 48)], (60, 120, 70), 1)
        s.line([(66, 54), (92, 54)], (60, 120, 70), 1)
        s.rect(64, 70, 72, 78, (60, 40, 40))
        s.circle(90, 74, 3, (60, 40, 40))


@card(88)  # Professor Oak
def oak(s):
    person(s, 80, WHITE, (140, 110, 80), (196, 196, 200))


@card(89)  # Revive
def revive(s):
    s.shadow(80, 93, 18)
    with s.part():
        s.poly([(80, 22), (102, 54), (80, 86), (58, 54)], (250, 220, 80))
        s.poly([(80, 30), (94, 54), (80, 78), (66, 54)], (255, 244, 170))
    with s.part(outline=False, shade=False):
        s.star(106, 30, 5, 2, WHITE)
        s.star(56, 76, 4, 1.6, WHITE)


@card(90)  # Super Potion
def super_potion(s):
    s.shadow(80, 93, 18)
    spray_bottle(s, 84, 58, (250, 200, 70), (220, 90, 60), scale=1.3)


# ------------------------------------------------------------------ commons

@card(91)  # Bill
def bill(s):
    person(s, 80, (110, 150, 120), (90, 90, 110), (130, 80, 40), glasses=True)


@card(92)  # Energy Removal
def energy_removal(s):
    energy_orb(s, 80, 54, 22, (240, 200, 70))
    big_x(s, 80, 54, 20)


@card(93)  # Gust of Wind
def gust_of_wind(s):
    with s.part():
        for i, (y, w) in enumerate(((34, 70), (52, 90), (70, 60))):
            x0 = 30 + i * 10
            s.curve([(x0, y), (x0 + w * 0.6, y - 4), (x0 + w, y + 2), (x0 + w - 8, y + 10), (x0 + w - 18, y + 4)], (210, 236, 250), 2.6)
    with s.part():
        for x, y, a in ((112, 30, 30), (124, 58, -20), (96, 78, 60)):
            s.ellipse(x, y, 5, 2.4, (110, 180, 80), rot=a)


@card(94)  # Potion
def potion(s):
    s.shadow(80, 93, 18)
    spray_bottle(s, 84, 58, (150, 100, 200), (90, 160, 220), scale=1.3)


@card(95)  # Switch
def switch(s):
    with s.part():
        s.poly([(40, 40), (100, 40), (100, 30), (122, 48), (100, 66), (100, 56), (40, 56)], (250, 200, 60))
    with s.part():
        s.poly([(120, 62), (60, 62), (60, 52), (38, 70), (60, 88), (60, 78), (120, 78)], (100, 170, 230))
