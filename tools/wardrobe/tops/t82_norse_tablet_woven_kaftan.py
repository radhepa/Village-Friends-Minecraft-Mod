"""Norse Tablet-Woven Kaftan: a wrap-front kaftan edged with tablet-woven bands and pinned at the shoulder with a ring brooch."""
from kit import belt, body, flaps, sleeves
from kit_male import blk, embroider

META = {
    "name": "Norse Tablet-Woven Kaftan",
    "gender": "male",
    "description": "A northern wrap-front kaftan crossing to the hip, every edge bound with tablet-woven bands, pinned with a ring brooch.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}


def band(face, x, y0, y1):
    for y in range(y0, y1 + 1):
        face.set(x, y, "A3" if y % 2 else "M3")
        face.set(x + 1, y, "A1" if y % 2 else "A2")


def build(g):
    b = body(g, "P", "twill", 8201)
    jacket = g.part("jacket")
    jf = jacket.front
    # The wrap: the left panel crosses to the right hip along a stepped tablet-woven edge.
    for y in range(12):
        edge = max(0, 5 - y // 2)
        band(jf, edge, y, y)
    jf.clear(3, 0), jf.clear(4, 0), jf.clear(4, 1)
    sleeves(g, "P", "twill", 8202, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        embroider(arm.strip, 8, "step", "A3", "M3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "A1")
    pin = blk(g, "ring_brooch", (-2.6, 1.2, -2.75), (2, 2, 1), "M", 3, "smooth", 8203, edge=False)
    pin.front.set(1, 1, "M0"), pin.front.set(0, 0, "M4")
    belt(g, "belt", 9.4, height=1)
    for face in flaps(g, "kaftan_skirt", 5, "P", "twill", 8204, top=10.6, slit=True):
        embroider(face, 3, "step", "A3", "M3")
