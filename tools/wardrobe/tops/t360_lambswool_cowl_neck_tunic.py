"""Lambswool Cowl-Neck Tunic: a soft undyed lambswool pullover tunic whose wide cowl neck slumps in heavy folds over the collarbones."""
from kit import SIDES, body, flaps, sleeves
from kit_male import blk, ribbing
from paint import k

META = {
    "name": "Lambswool Cowl-Neck Tunic",
    "gender": "male",
    "description": "A soft pullover tunic of undyed lambswool with a wide cowl neck slumping in heavy folds over the collarbones, ribbed cuffs and a ribbed hem at the hip.",
    "tags": ["casual", "simple", "knit"],
    "covers_waist": True,
}


def fleece(face, base=3, rows=None):
    """Lofty lambswool: soft knit stitches with a little lit nap scattered in calm diagonals."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            gx = x + face.x0
            s = base - 1 if gx % 3 == 2 and y % 2 == 0 else base + 1 if (gx + y) % 7 == 0 else base
            face.set(x, y, k("S", s))


def build(g):
    b = body(g, "S", "knit", 40660, base=3)
    for face in b.sides:
        fleece(face)
    sleeves(g, "S", "knit", 40661, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        fleece(arm.strip, rows=range(0, 8))
        ribbing(arm.strip, "S", 3, rows=range(8, 11))
    # The cowl: a deep ring of cloth round the neck, its front sagging into a fold.
    cowl = blk(g, "cowl_ring", (0, -.4, 0), (9, 2, 6), "S", 3, "knit", 40662, inflate=.08)
    for face in cowl.sides:
        face.hline(0, face.w - 1, 0, "S4")
        for x in range(0, face.w, 3):
            face.set(x, 1, "S2")                                          # heavy folds
    cowl.top.fill("S1")                                                   # looking down into the cowl
    drape = blk(g, "cowl_drape", (0, .9, -2.75), (8, 3, 1), "S", 3, "knit", 40663, rotation=(-22, 0, 0))
    df = drape.front
    df.hline(0, 7, 0, "S3")
    df.set(0, 1, "S2"), df.set(7, 1, "S2"), df.hline(1, 6, 1, "S4")       # the slumped fold catching light
    df.set(0, 2, "S1"), df.set(1, 2, "S2"), df.set(6, 2, "S2"), df.set(7, 2, "S1"), df.hline(2, 5, 2, "S2")
    # Ribbed hem at the hip.
    for face in flaps(g, "tunic_hem", 2, "S", "knit", 40664, base=3, top=11.2):
        ribbing(face, "S", 3)
