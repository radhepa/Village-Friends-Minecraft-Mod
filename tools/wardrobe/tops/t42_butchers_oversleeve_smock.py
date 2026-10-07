"""Butcher's Oversleeve Smock: a twill smock with tied linen oversleeves, a striped half-apron and a steel on a chain."""
from kit import belt, body, neckline, sleeves
from kit_male import arm_blk, blk, stripes
from paint import fabric, solid

META = {
    "name": "Butcher's Oversleeve Smock",
    "gender": "male",
    "description": "A shambles smock with linen oversleeves tied at elbow and wrist, a striped half-apron and a sharpening steel on a chain.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 4201)
    neckline(b.front, "keyhole", "P")
    b.front.hline(0, 7, 0, "P3")
    sleeves(g, "P", "twill", 4202, rows=(0, 10))
    for i, side in enumerate(("right", "left")):
        over = g.part(f"{side}_sleeve")
        fabric(over.strip, "S", "weave", 4203, 3, 0, 4, over.strip.w, 7)
        for y in (4, 10):
            for x in range(over.strip.w):
                over.strip.set(x, y, "S1" if x % 2 else "S2")       # gathered ties
        tie = arm_blk(g, f"{side}_oversleeve_tie", side, 2.2, (1, 2, 1), "S", 2, "plain", 4204 + i,
                      dx=-2.3 if side == "right" else 2.3)
        tie.strip.hline(0, tie.strip.w - 1, 1, "S1")
    apron = g.piece("half_apron", "TORSO", (-4, 0, 0), (8, 6, 1), pivot=(0, 9.8, -2.85), motion="flap_front")
    solid(apron, "S", "weave", 4206, 3)
    stripes(apron.front, ["S3", "S3", "A2"], vertical=True, rows=range(1, 6))
    apron.front.hline(0, 7, 0, "S4"), apron.front.hline(0, 7, 5, "S1")
    belt(g, "apron_tie", 9.4, role="S", base=3, height=1, buckle=None)
    steel = blk(g, "sharpening_steel", (3.1, 10.0, -2.75), (1, 6, 1), "M", 3, "smooth", 4207, motion="sway")
    steel.strip.hline(0, steel.strip.w - 1, 0, "L3"), steel.strip.hline(0, steel.strip.w - 1, 1, "L2")
    steel.strip.hline(0, steel.strip.w - 1, 2, "M2")
