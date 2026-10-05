import math

from .trainers_base1 import RED, capsule

DRAW = {}


def card(number):
    def wrap(fn):
        DRAW[number] = fn
        return fn
    return wrap


@card(64)
def poke_ball(s):
    s.shadow(80, 93, 30)
    with s.part(outline=False, shade=False):
        s.circle(122, 24, 7, (244, 204, 70))
        s.circle(122, 24, 4.5, (228, 180, 50))
        for i in range(3):
            a = math.radians(200 + i * 20)
            s.line([(122 + 10 * math.cos(a), 24 + 10 * math.sin(a)), (122 + 14 * math.cos(a), 24 + 14 * math.sin(a))], (250, 230, 140), 0.8)
    capsule(s, 80, 60, 30, RED)
