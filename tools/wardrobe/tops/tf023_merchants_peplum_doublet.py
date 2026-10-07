"""Merchant's Peplum Doublet: a tailored velvet doublet-bodice with a flared peplum, slashed shoulder puffs and a coin purse."""
from kit import sleeves
from kit_female import buttons, girdle, neck, over_flaps, puffs
from paint import fabric, solid, strip_fabric

META = {
    "name": "Merchant's Peplum Doublet",
    "gender": "female",
    "description": "A tailored velvet doublet with a flared peplum, slashed shoulder puffs, gilt buttons and a coin purse.",
    "tags": ["fancy", "tailored"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "velvet", 12301, 2)
    fabric(b.top, "P", "velvet", 12301, 3), fabric(b.bottom, "P", "velvet", 12301, 1)
    neck(b.front, "square", "P", 2, edge="S4")
    buttons(b.front, 3, 2, 9, "M3", step=1, placket=None)
    for y in range(2, 10):
        b.front.set(4, y, "P1" if y % 2 else "M4")
    for face in (b.front, b.back):
        face.vline(1, 3, 9, "P1"), face.vline(6, 3, 9, "P1")
    sleeves(g, "P", "velvet", 12302, rows=(0, 11))
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 11, "S4")
    puffs(g, "P", "velvet", 12303, base=2, y=-2.4, h=3, slash="A2")
    girdle(g, "girdle", 8.2, role="M", base=3, height=1, buckle=None, texture="smooth", wide=True)
    f, bk = over_flaps(g, "peplum", 2, "P", "velvet", 12304, width=11, top=9.0)
    for face in (f, bk):
        for x in range(0, face.w, 2):
            face.vline(x, 0, 1, "P1")
        face.hline(0, face.w - 1, 1, "A2")
    purse = g.piece("purse", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(2.6, 7.0, -3.4))
    solid(purse, "A", "velvet", 12305, 2)
    purse.front.set(0, 0, "M3"), purse.front.set(1, 0, "M3"), purse.front.set(1, 1, "M4")
