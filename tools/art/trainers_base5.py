from .canvas import OUTLINE, darker, lighter
from .trainers_base1 import BLACK, RED, WHITE, capsule, person

DRAW = {}

ROCKET = (52, 48, 58)


def card(*numbers):
    def wrap(fn):
        for number in numbers:
            DRAW[number] = fn
        return fn
    return wrap


def r_badge(s, cx, cy, r):
    with s.part():
        s.circle(cx, cy, r, WHITE)
    with s.part(outline=False, shade=False):
        k = r / 10
        s.line([(cx - 4 * k, cy + 6 * k), (cx - 4 * k, cy - 6 * k), (cx + 1 * k, cy - 6 * k)], RED, 2.2 * k)
        s.curve([(cx + 1 * k, cy - 6 * k), (cx + 6 * k, cy - 3 * k), (cx + 1 * k, cy)], RED, 2.2 * k)
        s.line([(cx - 4 * k, cy), (cx + 1 * k, cy), (cx + 5 * k, cy + 6 * k)], RED, 2.2 * k)


def grunt(s, x, hair, skirt=False, holding=None):
    person(s, x, (238, 238, 242), ROCKET if not skirt else (238, 238, 242), hair, hair_style="long" if skirt else "spiky",
           grin=True, skirt=skirt, holding=holding)
    r_badge(s, x, 54, 5)


@card(15, 71)
def here_comes_team_rocket(s):
    with s.part(outline=False, shade=False):
        for x, a in ((20, 30), (140, -30)):
            s.poly([(x, 0), (80 + a, 100), (80 + a * 2, 100)], (250, 246, 200))
    grunt(s, 56, (200, 60, 90), skirt=True)
    grunt(s, 104, (90, 110, 200))
    with s.part(outline=False, shade=False):
        for x, y in ((80, 14), (30, 60), (130, 60)):
            s.star(x, y, 4, 1.4, (255, 236, 140), points=4, rot=0)


@card(16, 72)
def rockets_sneak_attack(s):
    s.shadow(80, 93, 30)
    with s.part():
        s.ellipse(80, 60, 26, 30, ROCKET)
        s.tri((60, 40), (54, 22), (70, 34), ROCKET)
        s.tri((100, 40), (106, 22), (90, 34), ROCKET)
    with s.part(outline=False, shade=False):
        s.ellipse(70, 48, 5, 2.4, (250, 230, 90), rot=12)
        s.ellipse(90, 48, 5, 2.4, (250, 230, 90), rot=-12)
    r_badge(s, 80, 74, 8)
    with s.part():
        for i in range(5):
            x = 30 + i * 6
            s.rect(x, 74 - i * 6, x + 18, 76 - i * 6, (200, 200, 210))


@card(73)
def bosss_way(s):
    with s.part(outline=False, shade=False):
        s.rect(20, 10, 140, 100, (110, 40, 50))
    with s.part():
        s.poly([(48, 92), (52, 54), (108, 54), (112, 92)], (90, 64, 50))
        s.ellipse(80, 46, 24, 14, (120, 84, 64))
    with s.part():
        s.ellipse(80, 66, 18, 22, (60, 60, 70))
    with s.part():
        s.ellipse(80, 38, 10, 11, (40, 36, 46))
    with s.part():
        s.ellipse(100, 74, 9, 7, (236, 220, 180))
        s.tri((94, 70), (92, 62), (98, 68), (236, 220, 180))
        s.tri((106, 70), (108, 62), (102, 68), (236, 220, 180))
        s.circle(100, 72, 2, (250, 200, 60))
    r_badge(s, 80, 18, 6)


@card(74)
def challenge(s):
    person(s, 46, (60, 120, 210), (60, 60, 80), (70, 50, 30), hair_style="spiky")
    person(s, 116, (238, 238, 242), ROCKET, (200, 60, 90), hair_style="long", grin=True)
    r_badge(s, 116, 54, 5)
    with s.part():
        s.poly([(74, 26), (84, 36), (76, 40), (88, 54), (72, 44), (80, 40)], (250, 210, 60))


@card(75)
def digger(s):
    soil = (150, 104, 66)
    with s.part(outline=False, shade=False):
        s.rect(0, 70, 160, 100, soil)
        s.ellipse(80, 76, 30, 8, darker(soil, 0.4))
    with s.part():
        s.ellipse(52, 70, 14, 6, lighter(soil, 0.1))
        s.ellipse(110, 72, 12, 5, lighter(soil, 0.1))
    with s.part():
        s.line([(100, 20), (82, 64)], (150, 110, 70), 2.4)
        s.poly([(76, 60), (88, 66), (84, 80), (72, 74)], (176, 180, 196))


@card(76)
def imposter_oaks_revenge(s):
    person(s, 80, WHITE, (140, 110, 80), (196, 196, 200), grin=True)
    with s.part(outline=False, shade=False):
        s.rect(68, 25, 92, 30, BLACK)
        s.line([(72, 22), (77, 24)], OUTLINE, 1)
        s.line([(88, 22), (83, 24)], OUTLINE, 1)
    for x, y in ((30, 34), (130, 30)):
        with s.part():
            s.poly([(x - 8, y - 10), (x + 8, y - 10), (x + 8, y + 10), (x - 8, y + 10)], WHITE)
        with s.part(outline=False, shade=False):
            s.line([(x - 4, y - 4), (x + 4, y + 4)], RED, 1.6)
            s.line([(x + 4, y - 4), (x - 4, y + 4)], RED, 1.6)


@card(77)
def nightly_garbage_run(s):
    with s.part(outline=False, shade=False):
        s.circle(126, 20, 10, (244, 240, 210))
        s.circle(130, 17, 9, (52, 44, 80))
    s.shadow(70, 93, 26)
    with s.part():
        s.poly([(48, 46), (92, 46), (88, 90), (52, 90)], (150, 156, 168))
        s.ellipse(70, 44, 24, 6, (170, 176, 188))
    with s.part(outline=False, shade=False):
        for x in (60, 70, 80):
            s.line([(x, 52), (x, 86)], darker((150, 156, 168), 0.25), 1)
    with s.part():
        s.ellipse(110, 86, 12, 6, (90, 160, 90))
        s.ellipse(124, 88, 6, 3, (230, 220, 160))
        s.circle(100, 30, 6, (240, 90, 60))


@card(78)
def goop_gas_attack(s):
    with s.part(outline=False):
        for x, y, r in ((50, 50, 20), (80, 40, 24), (110, 54, 20), (78, 66, 18), (40, 74, 12), (120, 78, 14)):
            s.circle(x, y, r, (170, 120, 200))
    with s.part(outline=False, shade=False):
        for x, y, r in ((70, 34, 6), (100, 48, 5), (52, 60, 4)):
            s.circle(x, y, r, (210, 180, 230))
        s.circle(80, 52, 3, (80, 50, 100))
        s.circle(92, 52, 3, (80, 50, 100))
        s.smile(86, 60, 5, (80, 50, 100), 1.2)


@card(79)
def sleep(s):
    s.shadow(80, 93, 28)
    capsule(s, 80, 68, 20, (110, 90, 200))
    with s.part(outline=False, shade=False):
        for i, (x, y, k) in enumerate(((100, 40, 4), (112, 26, 5.5), (126, 12, 7))):
            s.line([(x - k, y - k), (x + k, y - k), (x - k, y + k), (x + k, y + k)], (240, 240, 255), 1.4 + i * 0.3)
