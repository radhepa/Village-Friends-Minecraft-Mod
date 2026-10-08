"""Bohemian Embroidered Shirt: a full linen shirt with puffed sleeves, broad embroidered cuffs and yoke, frilled wrists and a fringed sash."""
from kit import SIDES, body, sleeves
from kit_male import arm_blk, embroider, sash, sleeve_shapes
from kit_m08 import fringe

META = {
    "name": "Bohemian Embroidered Shirt",
    "gender": "male",
    "description": "A full linen shirt with puffed sleeves, broad bands of bright embroidery at the cuffs, shoulders and slit neck, frilled wrists and a fringed sash.",
    "tags": ["casual", "fancy"],
    "tucked": True,
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 38441, base=3)
    f = b.front
    f.clear(3, 0), f.clear(4, 0), f.clear(4, 1)
    for y in range(1, 5):                                                  # embroidery round the neck slit
        f.set(3, y, "A3" if y % 2 else "A1")
        f.set(5, y, "A3" if y % 2 else "A1")
    f.set(2, 0, "A2"), f.set(5, 0, "A2")
    b.back.hline(1, 6, 0, "A2")
    embroider(b.back, 1, "dots", "A3", x0=1, x1=6)
    for x in (1, 6):
        f.vline(x, 5, 11, "S2")                                            # soft folds
    sleeves(g, "S", "weave", 38442, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for y in (7, 8, 9, 10):
            arm.strip.hline(0, arm.strip.w - 1, y, "A2")
        embroider(arm.strip, 7, "diamond", "A4", "M3")                     # broad embroidered cuff
        arm.strip.hline(0, arm.strip.w - 1, 10, "A1")
        sl = g.part(f"{side}_sleeve")                                      # embroidered shoulder band
        embroider(sl.strip, 0, "zig", "A3", "A1")
        embroider(sl.top, 0, "zig", "A3", "A1")
    for puff in sleeve_shapes(g, "puff_sleeve", "S", 1.4, (5, 5, 5), "weave", 38443, inflate=.1):
        for face in puff.sides:
            face.hline(0, face.w - 1, 0, "S4")
            face.vline(1, 1, 4, "S2"), face.vline(3, 1, 4, "S2")             # gathers
            face.hline(0, face.w - 1, 4, "S1")
        puff.bottom.fill("S1")
    for side in SIDES:
        frill = arm_blk(g, f"{side}_wrist_frill", side, 8.9, (5, 1, 5), "S", 4, "plain", 38444, inflate=.05)
        for face in frill.sides:
            for x in range(face.w):
                face.set(x, 0, "S4" if x % 2 else "S2")
    band = sash(g, "sash", "A", y=8.8, height=2, texture="weave", seed=38445, tails=((2.6, -5), (3.4, 4)), tail_len=5)
    for face in band.sides:
        face.hline(0, face.w - 1, 1, "A1")
