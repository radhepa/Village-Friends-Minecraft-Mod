"""Carpenter Pants: canvas work pants with a hammer loop, a rule pocket and a reinforced knee."""
from kit_casual import leather_belt, shoes, trousers
from paint import solid

META = {
    "name": "Carpenter Pants",
    "gender": "male",
    "description": "Canvas carpenter pants: hammer loop, rule pocket, reinforced knees and boots.",
    "tags": ["casual", "modern", "work"],
}


def build(g):
    legs, body = trousers(g, "S", 1, "twill", 11301)
    for leg in legs:
        leg.front.hline(0, 3, 4, "S2"), leg.front.hline(0, 3, 7, "S0")   # double-knee panel
        for y in (5, 6):
            leg.front.set(0, y, "S0"), leg.front.set(3, y, "S0")
    rule = legs[1].left   # rule pocket on the outer left thigh
    rule.vline(1, 1, 4, "S0"), rule.vline(2, 1, 4, "S2")
    loop = g.piece("right_hammer_loop", "RIGHT_LEG", (0, 0, -.5), (1, 3, 1), pivot=(-2.4, 2.4, 0))
    solid(loop, "S", "twill", 11302, 1)
    leather_belt(g)
    shoes(g, "boot")
