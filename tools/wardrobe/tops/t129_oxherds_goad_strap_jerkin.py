"""Oxherd's Goad-Strap Jerkin: a sleeved wool jerkin with a stitched leather shoulder yoke, a broad strap with a brass ring, and a long ox goad held across the back."""
from kit import belt, body, flaps, neckline, sleeves
from kit_m01 import rod
from kit_male import blk, shoulder_cape
from paint import k, line

META = {
    "name": "Oxherd's Goad-Strap Jerkin",
    "gender": "male",
    "description": "A sleeved wool jerkin under a stitched leather shoulder yoke, a broad strap with a brass ring across the chest, and a long iron-tipped ox goad with its plough-scraping spud held across the back.",
    "tags": ["work", "rugged", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 31575)
    neckline(b.front, "square", "P")
    b.front.vline(4, 2, 11, "P1")
    for y in (3, 5, 7):
        b.front.set(3, y, "L3")                                           # wooden buttons
    for face in (b.right, b.left):
        face.vline(1, 1, 11, "P1")
    sleeves(g, "P", "weave", 31576, rows=(0, 10), cuff="L2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "L3")
        for face in arm.sides:
            face.vline(1, 2, 8, "P1")
    # The leather yoke over both shoulders, its lower edge stitched and scalloped.
    yoke = shoulder_cape(g, "leather_yoke", "L", "leather", 31577, 2, length=2, width=10, depth=6, y=-.7)
    for face in yoke.sides:
        face.hline(0, face.w - 1, 0, "L3")
        for x in range(face.w):
            face.set(x, 1, "L1" if x % 3 == 2 else "L2")
    yoke.top.hline(0, yoke.top.w - 1, 2, "L3")
    # The goad strap: right shoulder to left hip in front, a brass ring on the chest; behind, it crosses the goad.
    jacket = g.part("jacket")
    for face, pts in ((jacket.front, (0, 1, 7, 9)), (jacket.back, (7, 1, 0, 9))):
        line(face, *pts, "L2")
        line(face, pts[0] + (1 if face is jacket.front else -1), pts[1], pts[2] + (1 if face is jacket.front else -1),
             pts[3], "L1")
    ring = blk(g, "strap_ring", (-1.0, 3.6, -2.6), (1, 1, 1), "M", 3, "smooth", 31578, edge=False, inflate=.1)
    ring.front.fill("M4")
    belt(g, "belt", 9.6, height=1, buckle="M")
    # The ox goad: a long ash pole with an iron prick at the top and the flat spud for scraping the share below.
    goad = rod(g, "ox_goad", (.3, 6.4, 3.4), 12, "L", 3, rotation=(0, 0, -30), seed=31579, end="M3")
    spud = blk(g, "goad_spud", (3.4, 11.3, 3.4), (2, 1, 1), "M", 2, "smooth", 31580, rotation=(0, 0, -30), edge=False)
    spud.back.set(0, 0, "M4"), spud.bottom.fill("M1")
    for i, (x, y) in enumerate(((-1.55, 3.2), (.8, 7.2))):                 # strap loops holding the goad
        loop = blk(g, f"goad_loop_{i}", (x, y, 3.4), (1, 1, 1), "L", 1, "leather", 31581 + i, inflate=.15,
                   edge=False)
        loop.back.set(0, 0, "L2")
    for face in flaps(g, "jerkin_skirt", 3, "P", "weave", 31583, top=10.8):
        for x in range(9):
            face.set(x, 2, k("P", 0) if x % 3 == 2 else k("P", 1))         # cut into square tabs
        face.vline(2, 1, 2, "P0"), face.vline(5, 1, 2, "P0")
