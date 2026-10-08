"""Carrier's Parcel-Strapped Jerkin: a cloth jerkin crossed by carrying straps, a stack of corded parcels on the back."""
from kit import belt, body, flaps, neckline, pouch, roll, sleeves
from kit_male import blk
from paint import fabric, k, line, solid, strip_fabric

META = {
    "name": "Carrier's Parcel-Strapped Jerkin",
    "gender": "male",
    "description": "A common carrier's twill jerkin crossed by two carrying straps, a waybill tucked at the crossing and a stack of corded, wax-sealed parcels on his back.",
    "tags": ["casual", "work", "sturdy"],
    "covers_waist": True,
}


def twine(box, key="L1"):
    """Parcel cord: once round each way, crossing on top."""
    for face in box.sides:
        face.vline(face.w // 2, 0, face.h - 1, key)
        face.hline(0, face.w - 1, face.h // 2, key)
    box.top.vline(box.top.w // 2, 0, box.top.h - 1, key), box.top.hline(0, box.top.w - 1, box.top.h // 2, key)


def build(g):
    b = body(g, "S", "weave", 37040)                                    # the shirt
    neckline(b.front, "laced", "S")
    sleeves(g, "S", "weave", 37041, rows=(0, 5))
    roll(g, "S", 2.6, base=3)
    jacket = g.part("jacket")                                           # the jerkin over it
    strip_fabric(jacket, "P", "twill", 37042, 2, 0, 11)
    fabric(jacket.top, "P", "twill", 37042, 3)
    fabric(jacket.bottom, "P", "twill", 37043, 1)
    for x, y in ((2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2)):
        jacket.front.clear(x, y)
    jacket.front.set(2, 1, "P3"), jacket.front.set(5, 1, "P1")
    jacket.front.vline(4, 3, 11, "P0")
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "P1")
    # Two carrying straps cross on the chest and run straight down the back.
    line(jacket.front, 0, 0, 7, 9, "L1"), line(jacket.front, 7, 0, 0, 9, "L1")
    jacket.front.rect(3, 4, 2, 2, "M2"), jacket.front.set(3, 4, "M4")  # ring where they cross
    for x in (1, 6):
        jacket.back.vline(x, 0, 11, "L2"), jacket.back.vline(x + (1 if x == 1 else -1), 0, 11, "L1")
    for y in range(2):
        jacket.top.set(1, y, "L2"), jacket.top.set(6, y, "L2")
    tag = g.piece("waybill", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(-.8, 3.6, -2.7), rotation=(0, 0, 18))
    solid(tag, "S", "plain", 37044, 4, edge=False)
    tag.front.set(0, 1, "K2")
    belt(g, "belt", 9.4, height=1)
    pouch(g, "fee_pouch", (-2.6, 9.6, -2.9), (2, 2, 1), flap="M3")
    # The parcels: a long cloth bale at the bottom, a leather-cased box on it, a small bundle on top.
    bale = blk(g, "parcel_bale", (0, 5.4, 3.9), (8, 4, 3), "S", 3, "weave", 37045)
    twine(bale)
    bale.back.set(6, 1, "A2"), bale.back.set(6, 2, "A1")              # wax seal
    box = blk(g, "parcel_box", (-.8, 1.9, 3.8), (5, 4, 3), "L", 2, "leather", 37046, rotation=(0, 6, 0))
    for face in box.sides:                                              # a strapped leather case
        face.hline(0, face.w - 1, 0, "L3")
        face.vline(face.w // 2, 0, 3, "S3")
    box.top.vline(2, 0, 2, "S3")
    box.back.set(2, 2, "M3")
    bundle = blk(g, "parcel_bundle", (1.6, .2, 3.6), (4, 2, 2), "A", 2, "weave", 37047, rotation=(0, -10, 0))
    twine(bundle, "L1")
    bundle.top.set(1, 0, "A4")
    for face in flaps(g, "jerkin_hem", 2, "P", "twill", 37048, top=10.8):
        face.hline(0, 8, 1, k("P", 1))
