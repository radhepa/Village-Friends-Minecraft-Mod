"""Hobelar's Light Riding Jack: a fitted leather jack split for the saddle, a buckler hung on the sword hilt."""
from kit import SIDES, body, sleeves
from kit_male import arm_blk, blk, lacing
from kit_m04 import hanging, sides_of, split_flaps

META = {
    "name": "Hobelar's Light Riding Jack",
    "gender": "male",
    "description": "A light horseman's fitted leather jack over quilted cloth sleeves, laced up the side and split front and "
                   "back for the saddle, with flared riding cuffs and a small buckler hung over the sword hilt at his left hip.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}

S = 34120


def build(g):
    b = body(g, "L", "leather", S, base=2)
    for face in (b.front, b.back):
        face.vline(1, 1, 11, "L1"), face.vline(6, 1, 11, "L1")           # fitted panel seams
        face.hline(0, 7, 11, "L1")
    b.front.vline(2, 1, 10, "L3")
    lacing(b.right, 1, 2, 10, "S3", "L0")                                # laced up the right side
    jacket = g.part("jacket")
    for face in jacket.sides:                                              # padded cloth showing at the armholes
        face.hline(0, face.w - 1, 0, "S2")
    jacket.top.fill("S3")
    jacket.front.rect(2, 0, 4, 1, None)
    sleeves(g, "S", "quilt", S + 1, rows=(0, 10))
    for i, side in enumerate(SIDES):
        cuff = arm_blk(g, f"{side}_riding_cuff", side, 7.0, (5, 2, 5), "L", 2, "leather", S + 2 + i, inflate=.2)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 1, "L1")
        getattr(cuff, sides_of(side)[0]).set(2, 1, "M3")
    belt = blk(g, "belt", (0, 9.6, 0), (9, 1, 5), "L", 1, "leather", S + 4, inflate=.07, edge=False)
    belt.front.set(3, 0, "M3")
    # Sword hilt rising at the left hip, the buckler hung over it by its grip.
    hilt = hanging(g, "sword_grip", 3.0, 8.4, (1, 2, 1), "L", 1, "plain", S + 5, top=10.4, dz=.2)
    hilt.front.set(0, 0, "M3")
    hanging(g, "sword_guard", 3.0, 10.0, (3, 1, 1), "M", 3, "smooth", S + 6, top=10.4, dz=.2)
    buckler = hanging(g, "buckler", 2.0, 10.2, (4, 4, 1), "M", 2, "smooth", S + 7, top=10.4, dz=-.9)
    f = buckler.front
    for x, y in ((0, 0), (3, 0), (0, 3), (3, 3)):
        f.set(x, y, "L1")                                                  # rounded off by its leather rim
    f.hline(1, 2, 0, "M4"), f.vline(0, 1, 2, "M3"), f.vline(3, 1, 2, "M1"), f.hline(1, 2, 3, "M1")
    boss = hanging(g, "buckler_boss", 2.0, 11.2, (2, 2, 1), "M", 3, "smooth", S + 8, top=10.4, dz=-1.9)
    boss.front.set(0, 0, "M4"), boss.front.set(1, 1, "M1")
    for face in split_flaps(g, "riding_skirt", 4, "L", "leather", S + 9, top=10.6, half=4, gap=.6):
        face.vline(0, 1, 3, "L1"), face.hline(0, 3, 3, "L1")             # stitched edge
        face.set(2, 2, "L3")
