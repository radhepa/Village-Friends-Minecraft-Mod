"""Knitted Wool Waistcoat: a V-necked knitted waistcoat with two cables, a ribbed hem and wooden buttons over a linen shirt."""
from kit import SIDES, body, sleeves
from kit_m10 import cable
from kit_male import blk, ribbing

META = {
    "name": "Knitted Wool Waistcoat",
    "gender": "male",
    "description": "A snug hand-knitted wool waistcoat with a deep ribbed V neck, a twisting cable either side, wooden buttons and a thick ribbed hem, over a full linen shirt.",
    "tags": ["casual", "simple", "knit"],
    "covers_waist": True,
}


def build(g):
    shirt = body(g, "S", "weave", 40140, base=3)
    shirt.front.vline(3, 1, 4, "S2")                                     # the shirt's slit in the V
    vest = body(g, "P", "plain", 40141, layer="jacket")
    f, bk = vest.front, vest.back
    # Deep V neck edged with a ribbed band.
    for y in range(0, 5):
        for x in range(2 + y // 2, 6 - y // 2):
            f.clear(x, y)
    for y in range(0, 5):
        f.set(1 + y // 2, y, "P3"), f.set(6 - y // 2, y, "P1")
    f.set(3, 5, "P1"), f.set(4, 5, "P3")
    # Cables up both fronts and the back.
    cable(f, 1, 6, 9, "P", 2)
    cable(f, 5, 6, 9, "P", 2)
    cable(bk, 3, 1, 9, "P", 2)
    # Wooden buttons down the front.
    for y in (6, 8):
        f.set(4, y, "L3")
    # Ribbed hem band.
    ribbing(f, "P", 2, rows=range(10, 12))
    ribbing(bk, "P", 2, rows=range(10, 12))
    for face in (vest.right, vest.left):
        ribbing(face, "P", 2, rows=range(10, 12))
        face.vline(0 if face is vest.right else 3, 0, 9, "P1")
    # Armholes: the knit ends at the shoulder, shirt sleeves below.
    sleeves(g, "S", "weave", 40142, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for y in (7, 8):
            for x in range(arm.strip.w):
                arm.strip.set(x, y, "S2" if x % 2 else "S3")                # gathered into the cuff
        arm.strip.hline(0, arm.strip.w - 1, 9, "S4")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")
    # A thick ribbed hem standing off the hips.
    hem = blk(g, "knit_hem", (0, 10.0, 0), (9, 2, 5), "P", 2, "rib", 40144, inflate=.12, edge=False)
    for face in hem.sides:
        ribbing(face, "P", 2)
    hem.bottom.fill("P0")
