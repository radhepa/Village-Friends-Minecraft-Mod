"""Thorn-Proof Leather Leggings: heavy hide leggings lapped in overlapping bands like shingles, stiff shin shields strapped on, and a hawthorn twig caught in a strap."""
from kit import SIDES, footwear, leg_bone, waistband
from kit_m01 import outer
from kit_male import blk, leg_blk
from paint import k, solid, strip_fabric

META = {
    "name": "Thorn-Proof Leather Leggings",
    "gender": "male",
    "description": "Heavy hide leggings lapped in overlapping bands like roof shingles, stiff stitched shin shields strapped over them and a hawthorn twig still caught in a strap.",
    "tags": ["work", "rugged", "sturdy"],
}


def lapped(face, rows, ox=0):
    """Overlapping leather bands: a lit lip at the top of each band, a dark shadow under it."""
    for y in rows:
        for x in range(face.w):
            p = y % 3
            key = "L3" if p == 0 else "L1" if p == 2 else "L2"
            if p == 1 and (x + ox) % 4 == 0:
                key = "L1"                                                # stitches holding each band
            face.set(x, y, key)


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "L", "leather", 31421 + i, 2, 0, 9)
        lapped(leg.strip, range(0, 9), i)
        leg.top.fill("L2")
        strip_fabric(pants, "L", "leather", 31423 + i, 2, 0, 8)
        lapped(pants.strip, range(0, 8), i + 2)
        outer(pants, side).vline(1 if side == "right" else 2, 0, 7, "L0")      # outer seam, laced shut
        for y in range(1, 8, 2):
            outer(pants, side).set(2 if side == "right" else 1, y, "S3")
    waistband(g, "L", "leather", 31425)
    body = g.part("body")
    body.front.set(4, 9, "M3"), body.front.vline(4, 10, 11, "L0")
    footwear(g, "boot", top=8, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 8, "L3")
    # Shin shields: stiff stitched hide on the front of each shin, two buckled straps behind.
    for i, side in enumerate(SIDES):
        shield = g.piece(f"{side}_shin_shield", leg_bone(side), (-2, 0, -1), (4, 6, 1), pivot=(0, 3.4, -2.3))
        solid(shield, "L", "leather", 31427 + i, 3)
        f = shield.front
        f.hline(0, 3, 0, "L4")
        for y in range(1, 5):
            f.set(0, y, "L1" if y % 2 else "L2"), f.set(3, y, "L1" if y % 2 else "L2")   # running stitch
        f.vline(1 if side == "right" else 2, 1, 4, "L2")                         # moulded ridge
        f.set(2 if side == "right" else 1, 2, "L4")
        f.hline(0, 3, 5, "L0")
        for j, y in enumerate((4.2, 7.6)):
            strap = leg_blk(g, f"{side}_shield_strap_{j}", side, y, (5, 1, 5), "L", 1, "leather", 31429 + 2 * i + j,
                            inflate=.06)
            o = outer(strap, side)
            o.set(2, 0, "M3"), o.set(1, 0, "M1")
    # A hawthorn twig snagged in the right upper strap, a red haw still on it.
    twig = blk(g, "hawthorn_twig", (-2.2, 3.4, -1.2), (1, 3, 1), "L", 1, "plain", 31435, bone="RIGHT_LEG",
               rotation=(0, 0, 34), edge=False)
    twig.strip.set(0, 1, "L3")
    thorn = blk(g, "hawthorn_thorn", (-2.9, 4.2, -1.2), (1, 1, 1), "L", 3, "plain", 31436, bone="RIGHT_LEG",
                edge=False)
    thorn.top.fill(k("L", 4))
    haw = blk(g, "hawthorn_haw", (-3.1, 3.0, -1.2), (1, 1, 1), "A", 2, "plain", 31437, bone="RIGHT_LEG", edge=False)
    haw.top.fill("A4"), haw.front.fill("A3")
