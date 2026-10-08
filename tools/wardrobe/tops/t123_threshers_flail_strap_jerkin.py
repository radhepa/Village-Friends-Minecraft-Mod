"""Thresher's Flail-Strap Jerkin: a channel-quilted jerkin over shirt sleeves, a threshing flail slung across the back on a chest strap."""
from kit import body, flaps, sleeves
from kit_m01 import rod
from kit_male import blk
from paint import k, line, strip_fabric

META = {
    "name": "Thresher's Flail-Strap Jerkin",
    "gender": "male",
    "description": "A sleeveless jerkin quilted in upright channels over linen shirt sleeves, with a threshing flail slung across the back on a broad strap over the chest.",
    "tags": ["work", "rugged", "sturdy"],
    "covers_waist": True,
}


def channels(face, ox=0, rows=None):
    """Upright quilted channels: a stitched seam every third texel, lit padding between."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            c = (x + ox) % 3
            face.set(x, y, "P1" if c == 0 else "P3" if c == 1 and y % 4 == 1 else "P2")


def build(g):
    b = body(g, "P", "weave", 31201)
    jacket = g.part("jacket")
    strip_fabric(jacket, "P", "weave", 31202, 2)
    for face in jacket.sides:
        channels(face, face.x0)
        face.hline(0, face.w - 1, 11, "P0")
    jacket.top.fill("P3")
    # Shirt showing at the throat; jerkin closed with wooden toggles.
    for face in (b.front, jacket.front):
        for x, y in ((3, 0), (4, 0), (3, 1), (4, 1)):
            face.set(x, y, "S3")
    jacket.front.set(3, 2, "P0"), jacket.front.set(4, 2, "P0")
    jacket.front.vline(4, 3, 11, "P0")
    for y in (4, 7, 10):
        jacket.front.set(3, y, "L3"), jacket.front.set(4, y, "L4")
    for face in (jacket.right, jacket.left):
        face.vline(1, 2, 11, "L1")                                        # side lacing
        for y in range(3, 11, 2):
            face.set(2, y, "L3")
    sleeves(g, "S", "weave", 31203, base=3, rows=(0, 10), cuff="S2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for face in arm.sides:
            face.vline(1, 2, 7, "S2")
        arm.strip.hline(0, arm.strip.w - 1, 9, "S4")
        arm.top.fill("P2")
        arm.strip.hline(0, arm.strip.w - 1, 0, "P1")                       # jerkin's shoulder edge
    # The flail's carrying strap: left shoulder to right hip, front and back.
    for face, pts in ((jacket.front, (6, 0, 0, 10)), (jacket.back, (1, 0, 7, 10))):
        line(face, *pts, "L2")
        line(face, pts[0] + (1 if face is jacket.front else -1), pts[1], pts[2] + (1 if face is jacket.front else -1),
             pts[3], "L1")
    jacket.top.vline(6, 0, 3, "L2")
    buckle = blk(g, "strap_buckle", (1.6, 4.6, -2.75), (1, 1, 1), "M", 3, "smooth", 31204, edge=False)
    buckle.front.set(0, 0, "M4")
    # The flail across the back: a long ash staff, a thong at the top and the stout swingle beside it.
    rod(g, "flail_staff", (0, 5.8, 3.1), 12, "L", 2, rotation=(0, 0, 36), seed=31205, end="L1")
    cap = blk(g, "flail_cap", (3.5, .4, 3.1), (1, 2, 1), "K", 2, "leather", 31206, rotation=(0, 0, 36))
    cap.strip.hline(0, cap.strip.w - 1, 0, "K3")
    # The swingle: a thicker, paler beater hanging from the cap, angled back across the shoulders.
    swingle = g.piece("flail_swingle", "TORSO", (-1, 0, -.5), (2, 6, 1), pivot=(2.6, 1.4, 4.1), rotation=(0, 0, 8))
    for face in swingle.faces:
        face.fill("L4")
    for face in swingle.sides:
        face.vline(0, 0, face.h - 1, "L3")
        face.hline(0, face.w - 1, 0, "K2"), face.hline(0, face.w - 1, face.h - 1, "L2")
        face.set(face.w - 1, 3, "L3")
    swingle.bottom.fill("L2")
    thong = blk(g, "flail_thong", (2.9, .7, 3.6), (1, 1, 2), "K", 2, "leather", 31207)
    thong.top.fill("K3")
    belt = g.piece("belt", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.32)
    for face in belt.faces:
        face.fill("L2")
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    belt.front.set(4, 0, "M3")
    for face in flaps(g, "jerkin_skirt", 3, "P", "weave", 31208, top=11.0):
        channels(face, 0, rows=range(1, 3))
        face.hline(0, 8, 2, k("P", 1))
