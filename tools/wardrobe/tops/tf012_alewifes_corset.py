"""Alewife's Corset: a boned, ribbon-laced corset over a full-sleeved chemise, a bar towel and a ring of cellar keys."""
from kit_female import bodice, chemise, hanging, lacing
from paint import solid

META = {
    "name": "Alewife's Corset",
    "gender": "female",
    "description": "A boned corset laced with ribbon over a billowing chemise, a striped bar towel and the cellar keys.",
    "tags": ["casual", "tailored"],
    "covers_waist": True,
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 11201, neckline="wide", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 4, "A2")                              # ribbon bands at the elbow
        arm.strip.hline(0, 15, 9, "S2")
        arm.strip.hline(0, 15, 10, "S4")
        for x in range(1, 16, 4):
            arm.strip.vline(x, 0, 3, "S2")
            arm.strip.vline(x, 5, 8, "S2")
    b = bodice(g, "P", "weave", 11202, rows=(3, 10), straps=False)
    b.front.clear(3, 3), b.front.clear(4, 3)                         # a sweetheart dip
    b.front.set(2, 3, "P3"), b.front.set(5, 3, "P3")
    for x in (1, 6):
        b.front.vline(x, 4, 10, "P1")                                # boning channels
    for x in range(0, 8, 2):
        b.back.vline(x, 4, 10, "P1")
    for face in (b.right, b.left):
        face.vline(1, 4, 10, "P1")
    lacing(b.front, 3, 4, 9, "spiral", lace="A3", under="S3", eyelet="M3")
    towel = hanging(g, "bar_towel", -3.0, 5, role="S", base=4, width=2, top=9.0, texture="weave")
    for y in (1, 3):
        towel.front.hline(0, 1, y, "A2")
    ring = hanging(g, "key_cord", 3.2, 3, role="L", base=2, top=9.0)
    keys = g.piece("keys", "TORSO", (-1, 3, -.1), (2, 2, 1), pivot=(3.2, 9.0, -3.25), motion="flap_front")
    solid(keys, "M", "smooth", 11203, 3)
    keys.front.set(0, 1, "M1"), keys.front.set(1, 0, "M4")
