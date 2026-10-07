"""Velvet Court Bodice: a noblewoman's pearl-edged velvet bodice with a jeweled stomacher and trumpet sleeves."""
from kit import body, sleeves
from kit_female import bells, girdle, hanging, lacing, neck, trim
from paint import k

META = {
    "name": "Velvet Court Bodice",
    "gender": "female",
    "description": "A pearl-edged velvet bodice with a jeweled stomacher, trumpet sleeves lined in silk and a jeweled girdle.",
    "tags": ["fancy", "gown"],
    "locked_to": "bf010_velvet_court_skirt",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 11001)
    neck(b.front, "square", "P", 2)
    for x in range(1, 7):
        b.front.set(x, 2, "M4" if x % 2 else "S4")                  # pearls along the neckline
    for y in (0, 1):
        b.front.set(1, y, "M4" if y % 2 else "S4"), b.front.set(6, y, "S4" if y % 2 else "M4")
    for y in range(3, 12):
        for x in range(2, 6):
            b.front.set(x, y, "A2")                                   # the stomacher
    for y in range(3, 12, 3):
        b.front.set(3, y + 1, "M3"), b.front.set(4, y + 1, "M4")
        b.front.set(2, y, "A3"), b.front.set(5, y + 2, "A1")
    b.front.vline(1, 3, 11, "M2"), b.front.vline(6, 3, 11, "M2")
    lacing(b.back, 3, 1, 9, "x", lace="A3", under="P0", eyelet="M3")
    sleeves(g, "P", "velvet", 11002, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 1, "M3")
        for x in range(0, 16, 2):
            arm.strip.set(x, 2, "S4")
    for box in bells(g, "P", "velvet", 11003, base=2, y=5.0, h=5, size=6, lining="A1"):
        for face in box.sides:
            face.hline(0, face.w - 1, 4, "A2")
            face.hline(0, face.w - 1, 3, "M3")
    belt = girdle(g, "jeweled_girdle", 7.8, role="M", base=3, height=1, buckle=None, texture="smooth")
    for face in belt.sides:
        for x in range(0, face.w, 3):
            face.set(x, 0, "A2")
    drop = hanging(g, "girdle_drop", 0.0, 10, role="M", base=3, top=8.8)
    for y in range(0, 10, 2):
        drop.front.set(0, y, "M4")
    drop.front.set(0, 9, "A2")
