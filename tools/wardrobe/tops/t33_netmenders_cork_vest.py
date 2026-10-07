"""Net-Mender's Cork Vest: a knitted vest over a linen shirt, a fishing net over one shoulder hung with cork floats."""
from kit import body, sleeves
from kit_male import blk, ribbing
from paint import fabric

META = {
    "name": "Net-Mender's Cork Vest",
    "gender": "male",
    "description": "A knitted vest over a linen shirt, a mended fishing net slung over the shoulder with cork floats and a netting needle.",
    "tags": ["casual", "sea"],
}


def build(g):
    b = body(g, "S", "weave", 3301, base=3)
    sleeves(g, "S", "weave", 3302, base=3, rows=(0, 10), cuff="S2")
    # Knitted vest on the body, open down the front over the shirt.
    for face in b.sides:
        fabric(face, "P", "knit", 3303, 2)
        ribbing(face, "P", 2, rows=range(10, 12))
    fabric(b.top, "P", "knit", 3303, 3)
    fabric(b.front, "S", "weave", 3304, 3, 3, 0, 2, 10)
    b.front.vline(2, 0, 9, "P1"), b.front.vline(5, 0, 9, "P3")
    b.front.clear(3, 0), b.front.clear(4, 0)
    # The net: a cord mesh on the jacket layer over the left shoulder, front and back.
    jacket = g.part("jacket")
    mesh = lambda x, y: (x + y) % 4 == 0 or (x - y) % 4 == 0
    for face, cols in ((jacket.front, lambda y: range(4 + y // 4, 8)), (jacket.back, lambda y: range(0, 4 - y // 4))):
        for y in range(9):
            for x in cols(y):
                if mesh(x, y):
                    face.set(x, y, "S4")
    for y in range(9):
        for x in range(4):
            if mesh(x, y):
                jacket.left.set(x, y, "S4")
    for y in range(4):
        for x in range(5, 8):
            if mesh(x, y):
                jacket.top.set(x, y, "S4")
    # Cork floats along the net's edge, a bundle of spare net at the back, the netting needle.
    for i, (x, y) in enumerate(((.6, 2.6), (1.4, 5.4), (2.4, 8.2))):
        cork = blk(g, f"cork_{i}", (x, y, -2.7), (2, 1, 1), "L", 3, "plain", 3305 + i, edge=False)
        cork.front.set(0, 0, "L4")
    bundle = blk(g, "net_bundle", (2.6, .6, 2.8), (3, 4, 2), "S", 3, "plain", 3310)
    for face in bundle.sides:
        for y in range(face.h):
            face.hline(0, face.w - 1, y, "S3" if y % 2 == 0 else "S1")   # the coiled net
    needle = blk(g, "netting_needle", (-2.3, 2.6, -2.6), (1, 3, 1), "L", 3, "plain", 3311)
    needle.front.set(0, 0, "S4")
