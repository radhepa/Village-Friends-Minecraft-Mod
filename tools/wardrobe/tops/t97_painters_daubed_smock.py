"""Painter's Daubed Smock: a loose smock dabbed with colour, brushes standing in the breast pocket and a palette board at the hip."""
from kit import body, flaps, neckline, sleeves
from kit_male import blk

META = {
    "name": "Painter's Daubed Smock",
    "gender": "male",
    "description": "A loose painter's smock dabbed with every colour of the workshop, brushes standing in the breast pocket and a palette board.",
    "tags": ["casual", "work", "whimsical"],
    "covers_waist": True,
}

DAUBS = ((1, 4, "A2"), (5, 7, "P1"), (2, 9, "M3"), (6, 2, "A3"), (3, 6, "K3"), (0, 10, "P2"))


def daub(face, flip=False):
    for x, y, key in DAUBS:
        x = face.w - 1 - x if flip else x
        if face.inside(x, y):
            face.set(x, y, key)
            if face.inside(x + 1, y):
                face.set(x + 1, y, key)


def build(g):
    b = body(g, "S", "weave", 9701, base=3)
    neckline(b.front, "v", "S", base=3)
    daub(b.front), daub(b.back, True)
    b.front.rect(5, 2, 2, 2, "S1")                                        # breast pocket
    sleeves(g, "S", "weave", 9702, base=3, rows=(0, 10), cuff="S1")
    for side in ("right", "left"):
        daub(g.part(f"{side}_arm").strip, side == "left")
    for i, (x, key) in enumerate(((1.6, "A"), (2.4, "P"), (3.0, "M"))):
        brush = blk(g, f"pocket_brush_{i}", (x, .2 + i * .3, -2.5), (1, 2, 1), "L", 3, "plain", 9703 + i)
        brush.strip.hline(0, brush.strip.w - 1, 0, f"{key}3")
    palette = blk(g, "palette_board", (-2.8, 10.6, -2.9), (3, 2, 1), "L", 4, "plain", 9706, rotation=(0, 0, 10))
    palette.front.set(0, 0, "A2"), palette.front.set(1, 1, "P2"), palette.front.set(2, 0, "M3")
    for face in flaps(g, "smock_hem", 4, "S", "weave", 9707, base=3, top=10.6):
        daub(face, face.name == "back")
