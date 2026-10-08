"""Shipwright's Adze-Loop Apron: a heavy leather bib apron over a rolled-sleeve linen shirt, an adze hung head-up in
a leather loop at the hip and a pocket of wooden treenails on the apron skirt."""
from kit import body, neckline, roll, sleeves
from kit_male import blk
from paint import fabric, line, solid

META = {
    "name": "Shipwright's Adze-Loop Apron",
    "gender": "male",
    "description": "A heavy leather bib apron over a rolled-sleeve linen shirt, an adze hung head-up in a loop at the hip "
                   "and a pocket bristling with wooden treenails.",
    "tags": ["work", "sea", "rugged"],
    "covers_waist": True,
}

SKIRT = (0, 11.0, -3.15)     # the apron skirt's hinge; the pocket and treenails share it so they swing as one
ADZE = (2.3, 9.4, -3.65)     # the loop; the adze's head, blade and handle share it


def build(g):
    b = body(g, "S", "weave", 33120, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 33121, base=3, rows=(0, 7))
    roll(g, "S", 3.4, base=3)
    # The bib: thick leather from the chest down, with stitched edges and neck straps.
    f = b.front
    fabric(f, "L", "leather", 33122, 2, 1, 3, 6, 9)
    f.vline(1, 3, 11, "L3"), f.vline(6, 3, 11, "L1")
    f.hline(1, 6, 3, "L3")
    for y in range(4, 11, 2):                                            # saddle stitching down the edges
        f.set(1, y, "L4"), f.set(6, y, "L0")
    f.vline(1, 0, 2, "L2"), f.vline(6, 0, 2, "L2")                     # neck straps
    b.top.vline(1, 0, 3, "L2"), b.top.vline(6, 0, 3, "L2")
    b.back.vline(1, 0, 1, "L2"), b.back.vline(6, 0, 1, "L2")
    b.back.hline(1, 6, 1, "L1")
    line(b.back, 1, 6, 6, 11, "L2"), line(b.back, 1, 11, 6, 6, "L2")    # apron ties crossed at the back
    for face in (b.right, b.left):
        face.hline(0, 3, 9, "L2")
    # The apron skirt, lying over whatever is worn below.
    skirt = g.piece("apron_skirt", "TORSO", (-3.5, 0, 0), (7, 7, 1), pivot=SKIRT, motion="flap_front")
    solid(skirt, "L", "leather", 33123, 2)
    skirt.front.vline(0, 0, 6, "L3"), skirt.front.vline(6, 0, 6, "L1"), skirt.front.hline(0, 6, 6, "L0")
    for y in range(1, 6, 2):
        skirt.front.set(0, y, "L4"), skirt.front.set(6, y, "L0")
    pocket = blk(g, "treenail_pocket", SKIRT, (3, 2, 1), "L", 1, "leather", 33124, origin=(-3.2, 1.0, -1.0),
                 motion="flap_front")
    pocket.front.hline(0, 2, 0, "L3")
    for i, x in enumerate((-2.8, -1.5)):                                    # wooden treenails standing in the pocket
        peg = blk(g, f"treenail_{i}", SKIRT, (1, 1, 1), "L", 4, "plain", 33125 + i, origin=(x, 0, -.8),
                  motion="flap_front", edge=False)
        peg.top.fill("L3")
    # The adze: hung head-up through a leather loop at the left hip.
    loop = blk(g, "adze_loop", ADZE, (2, 1, 1), "L", 0, "leather", 33127, origin=(-1, 0, -.5), inflate=.12)
    loop.front.set(1, 0, "M3")
    handle = blk(g, "adze_handle", ADZE, (1, 6, 1), "L", 4, "plain", 33128, origin=(-.5, -1.0, -.5),
                 motion="flap_front")
    for y in range(0, 6, 2):
        handle.strip.hline(0, handle.strip.w - 1, y, "L3")              # the ash handle's grain
    handle.strip.hline(0, handle.strip.w - 1, 5, "L2")
    head = blk(g, "adze_head", ADZE, (3, 1, 1), "M", 1, "smooth", 33129, origin=(-1.5, -2.0, -.5),
               motion="flap_front", edge=False)
    head.top.fill("M3"), head.front.set(0, 0, "M0")
    blade = blk(g, "adze_blade", ADZE, (1, 2, 1), "M", 1, "smooth", 33130, origin=(.5, -1.0, -.7),
                motion="flap_front")
    blade.strip.hline(0, blade.strip.w - 1, 1, "M4")
