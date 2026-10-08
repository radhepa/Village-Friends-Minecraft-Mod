"""Basque Wool Shepherd's Jacket: a short felted wool jacket open over a white shirt, a wound red sash and a leather wine bota on a strap."""
from kit import SIDES, body, sleeves
from kit_casual import collar_points
from kit_male import blk, sash
from paint import fabric, line, strip_fabric

META = {
    "name": "Basque Wool Shepherd's Jacket",
    "gender": "male",
    "description": "A short jacket of thick felted wool open over a white shirt, a long sash wound tight round the waist and a leather wine bota slung across the chest on a strap.",
    "tags": ["rugged", "work", "casual"],
    "covers_waist": True,
}


def build(g):
    shirt = body(g, "S", "weave", 38201, base=3)
    shirt.front.clear(3, 0), shirt.front.clear(4, 0)
    shirt.front.vline(4, 1, 3, "S1")
    jacket = g.part("jacket")
    strip_fabric(jacket, "P", "twill", 38202, 2)
    fabric(jacket.top, "P", "twill", 38202, 3)
    fabric(jacket.bottom, "P", "twill", 38203, 1)
    jf = jacket.front
    for y in range(12):
        jf.clear(3, y), jf.clear(4, y)                                    # the open front
        jf.set(2, y, "P3"), jf.set(5, y, "P3")                             # thick felted edges
        if y < 3:
            jf.set(1, y, "P1"), jf.set(6, y, "P1")                         # the lapels turned back
    line(jf, 0, 1, 7, 8, "L2")                                             # the bota strap across the chest
    line(jacket.back, 7, 1, 0, 8, "L2")
    sleeves(g, "P", "twill", 38204, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P3"), arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
        arm.front.vline(1, 2, 8, "P1")
    collar_points(g, "S", base=3, spread=14)
    band = sash(g, "gerriko_sash", "A", y=8.4, height=3, texture="weave", seed=38205, tails=((-3.0, 6),), tail_len=4)
    for face in band.sides:
        for x in range(face.w):
            if (x + 1) % 4 == 0:
                face.set(x, 1, "A1"), face.set(x - 1, 2, "A1")              # the turns of the wound sash
    bota = blk(g, "wine_bota", (2.6, 9.0, -3.25), (2, 3, 1), "L", 2, "leather", 38207)
    for face in bota.sides:
        face.set(0, face.h - 1, "L0"), face.set(face.w - 1, face.h - 1, "L0")    # rounded belly
    bota.front.set(0, 1, "L3"), bota.front.set(0, 0, "L3")
    neck = blk(g, "wine_bota_neck", (2.6, 8.0, -3.25), (1, 1, 1), "K", 2, "plain", 38208, edge=False)
    neck.top.fill("M3")
