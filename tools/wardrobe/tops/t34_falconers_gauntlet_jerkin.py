"""Falconer's Gauntlet Jerkin: a laced jerkin, a flared hawking gauntlet on the left arm, a lure pouch and hawk bells."""
from kit import belt, body, flaps, pouch, sleeves
from kit_male import arm_blk, blk, embroider, lacing
from paint import fabric, line

META = {
    "name": "Falconer's Gauntlet Jerkin",
    "gender": "male",
    "description": "A laced hunting jerkin, a flared hawking gauntlet on the left fist, a baldric of hawk bells and a feathered lure pouch.",
    "tags": ["rugged", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 3401, base=3)
    jacket = body(g, "P", "twill", 3402, layer="jacket")
    jf, jb = jacket.front, jacket.back
    for y in range(6):
        jf.clear(3, y), jf.clear(4, y)
    lacing(jf, 3, 1, 5, "L3", "L1")
    jf.vline(2, 0, 11, "P1"), jf.vline(5, 0, 11, "P3")
    sleeves(g, "S", "weave", 3403, base=3, rows=(0, 10), cuff="S2")
    for side in ("right", "left"):
        cap = g.part(f"{side}_sleeve")
        fabric(cap.strip, "P", "twill", 3404, 2, 0, 0, cap.strip.w, 3)
        cap.strip.hline(0, cap.strip.w - 1, 2, "P1")
    # The gauntlet: leather over the whole left forearm and fist, with an embroidered flared cuff.
    glove = g.part("left_sleeve")
    fabric(glove.strip, "L", "leather", 3405, 2, 0, 6, glove.strip.w, 6)
    glove.bottom.fill("L1")
    cuff = arm_blk(g, "gauntlet_cuff", "left", 3.6, (5, 3, 5), "L", 2, "leather", 3406, inflate=.18)
    for face in cuff.sides:
        embroider(face, 1, "dots", "A3")
        face.hline(0, face.w - 1, 0, "L3")
    # Baldric of hawk bells, right shoulder to left hip.
    line(jf, 0, 0, 7, 9, "L2"), line(jf, 0, 1, 6, 9, "L1")
    line(jb, 7, 0, 0, 9, "L2")
    for i, (x, y) in enumerate(((-1.6, 2.6), (1.4, 6.6))):
        bell = blk(g, f"hawk_bell_{i}", (x, y, -2.7), (1, 1, 1), "M", 3, "smooth", 3407 + i, edge=False)
        bell.bottom.fill("M1")
    belt(g, "belt", 9.6, height=1)
    lure = pouch(g, "lure_pouch", (-3.0, 10.0, -2.5), (2, 3, 2), flap="A2")
    lure.front.set(0, 2, "L1")
    feather = blk(g, "lure_feather", (-3.4, 8.2, -2.6), (1, 3, 1), "S", 4, seed=3409, rotation=(0, 0, 18))
    feather.strip.hline(0, feather.strip.w - 1, 0, "A2"), feather.strip.hline(0, feather.strip.w - 1, 2, "S2")
    for face in flaps(g, "skirt", 3, "P", "twill", 3410, top=10.6, slit=True):
        face.hline(0, 8, 2, "P1")
