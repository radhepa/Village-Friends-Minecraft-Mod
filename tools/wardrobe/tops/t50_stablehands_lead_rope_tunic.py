"""Stablehand's Lead-Rope Tunic: a tunic with a twisted lead rope across the chest, coiled at the hip, a curry comb and brush."""
from kit import belt, body, neckline, sleeves
from kit_male import blk
from paint import line

META = {
    "name": "Stablehand's Lead-Rope Tunic",
    "gender": "male",
    "description": "A stable lad's tunic with a twisted lead rope worn across the chest and coiled at the hip, a curry comb and a brush.",
    "tags": ["casual", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 5001)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 5002, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.rect(5, 6, 2, 2, "P1")                               # elbow patches
    jacket = g.part("jacket")
    for i, key in enumerate(("S3", "S1")):
        line(jacket.front, 0, i, 7, 8 + i, key)
        line(jacket.back, 7, i, 0, 8 + i, key)
    jacket.top.vline(0, 0, 3, "S2")
    belt(g, "belt", 9.6)
    coil = blk(g, "rope_coil", (3.4, 8.8, -.2), (2, 3, 4), "S", 2, "plain", 5003)
    for face in coil.sides:
        for y in range(face.h):
            face.hline(0, face.w - 1, y, "S3" if y % 2 == 0 else "S1")
    comb = blk(g, "curry_comb", (-3.0, 10.6, -2.75), (3, 2, 1), "M", 2, "smooth", 5004)
    for x in range(3):
        comb.front.set(x, 1, "M3" if x % 2 == 0 else "M0")             # teeth
    comb.front.hline(0, 2, 0, "L2")
    brush = blk(g, "body_brush", (-1.0, 10.6, -2.75), (2, 1, 1), "L", 3, "plain", 5005, edge=False)
    blk(g, "body_brush_bristles", (-1.0, 11.6, -2.75), (2, 1, 1), "K", 3, "plain", 5006, edge=False)
