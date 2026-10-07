"""Cooper's Pocket Bib Apron: a canvas bib apron with a deep belly pocket holding a mallet, and leather wrist guards."""
from kit import belt, body, neckline, sleeves
from kit_male import blk
from paint import fabric, line, solid

META = {
    "name": "Cooper's Pocket Bib Apron",
    "gender": "male",
    "description": "A barrel-maker's canvas bib apron with a deep belly pocket and mallet, straps crossed on the back, leather wrist guards.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 3501)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 3502, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_sleeve")
        fabric(arm.strip, "L", "leather", 3503, 2, 0, 7, arm.strip.w, 3)
        arm.strip.hline(0, arm.strip.w - 1, 7, "L3")
        arm.strip.hline(0, arm.strip.w - 1, 9, "L1")
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    fabric(jf, "S", "twill", 3504, 2, 1, 1, 6, 11)
    jf.hline(1, 6, 1, "S3"), jf.vline(1, 0, 0, "S2"), jf.vline(6, 0, 0, "S2")
    jf.vline(1, 2, 11, "S1"), jf.vline(6, 2, 11, "S1")
    for y in range(4):
        jacket.top.set(1, y, "S2"), jacket.top.set(6, y, "S2")
    line(jb, 1, 0, 6, 9, "S2"), line(jb, 6, 0, 1, 9, "S1")
    # Deep belly pocket with a mallet standing in it.
    pocket = blk(g, "belly_pocket", (0, 5.2, -2.55), (4, 3, 1), "S", 1, "twill", 3505)
    pocket.front.hline(0, 3, 0, "S3"), pocket.front.vline(2, 1, 2, "S0")
    handle = blk(g, "mallet_handle", (-.8, 3.4, -2.6), (1, 2, 1), "L", 3, "plain", 3506, edge=False)
    handle.front.set(0, 1, "L2")
    head = blk(g, "mallet_head", (-.8, 2.4, -2.6), (3, 1, 2), "L", 4, "plain", 3507, edge=False)
    head.front.set(0, 0, "L2"), head.front.set(2, 0, "L2")
    belt(g, "apron_tie", 9.6, role="S", base=1, height=1, buckle=None)
    skirt = g.piece("apron_skirt", "TORSO", (-4, 0, 0), (8, 6, 1), pivot=(0, 10.6, -2.85), motion="flap_front")
    solid(skirt, "S", "twill", 3508, 2)
    skirt.front.hline(0, 7, 5, "S1"), skirt.front.vline(0, 0, 5, "S1"), skirt.front.vline(7, 0, 5, "S1")
    skirt.front.hline(1, 2, 4, "S1"), skirt.front.set(5, 1, "S1")   # wear from bracing staves
