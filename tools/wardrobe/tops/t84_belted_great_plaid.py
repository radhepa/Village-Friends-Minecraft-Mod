"""Belted Great Plaid: the upper fold of a great kilted plaid thrown over the left shoulder and pinned, over a linen shirt."""
from kit import body, neckline, sleeves
from kit_male import blk, tartan

META = {
    "name": "Belted Great Plaid",
    "gender": "male",
    "description": "The upper fold of a great kilted plaid drawn over the left shoulder and down the back, pinned with a round brooch over a linen shirt.",
    "tags": ["casual", "kilt", "rugged"],
    "locked_to": "b84_great_plaid_kilt_and_hose",
    "covers_waist": True,
}


def plaid_key(x, y):
    gx, gy = x % 6, y % 6
    bx, by = gx < 2, gy < 2
    if (gx == 4 or gy == 4) and not (bx or by):
        return "A2"
    return "P0" if bx and by else "P1" if bx or by else "P2"


def build(g):
    b = body(g, "S", "weave", 8401, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 8402, base=3, rows=(0, 10), cuff="S2")
    jacket = g.part("jacket")
    # The plaid crosses from the right hip up over the left shoulder, front and back, and wraps the waist.
    for face, covered in ((jacket.front, lambda x, y: x >= 6 - y * 2 // 3),
                          (jacket.back, lambda x, y: x <= 1 + y * 2 // 3)):
        for y in range(12):
            for x in range(8):
                if covered(x, y) or y >= 9:
                    face.set(x, y, plaid_key(x + face.x0, y))
        face.hline(0, 7, 8, "P0")
    tartan(jacket.left, ox=1)
    for y in range(9, 12):
        for x in range(4):
            jacket.right.set(x, y, plaid_key(x, y))
    shoulder = blk(g, "plaid_shoulder", (3.0, -.9, 0), (3, 2, 6), "P", 2, "weave", 8403)
    for face in shoulder.faces:
        tartan(face, ox=face.x0)
    drape = g.piece("plaid_drape", "TORSO", (-2, 0, 0), (5, 9, 1), pivot=(1.4, .6, 2.7), rotation=(4, 0, -8))
    for face in drape.faces:
        tartan(face, ox=face.x0)
    brooch = blk(g, "plaid_brooch", (2.4, .6, -2.85), (2, 2, 1), "M", 3, "smooth", 8404, edge=False)
    brooch.front.set(0, 0, "M4"), brooch.front.set(1, 1, "A2")
