"""Chandler's Wax Apron: a long apron streaked with wax drips, a bundle of tallow candles hanging from the tie."""
from kit import belt, body, neckline, sleeves
from kit_male import blk
from paint import fabric, solid

META = {
    "name": "Chandler's Wax Apron",
    "gender": "male",
    "description": "A candle-maker's bib apron streaked with wax drips, sleeves cuffed, a bundle of tallow candles swinging from the tie.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}

DRIPS = ((1, 2, 3), (3, 1, 2), (4, 4, 4), (6, 2, 3))   # (column, first row, length)


def drips(face, top, rows):
    for x, y, n in DRIPS:
        for dy in range(n):
            if top + y + dy < rows:
                face.set(x, top + y + dy, "S4" if dy < n - 1 else "S3")


def build(g):
    b = body(g, "P", "weave", 4001)
    neckline(b.front, "square", "P")
    sleeves(g, "P", "weave", 4002, rows=(0, 10), cuff="S3")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "S2")
    jacket = g.part("jacket")
    fabric(jacket.front, "S", "smooth", 4003, 2, 1, 2, 6, 10)
    jacket.front.hline(1, 6, 2, "S3")
    jacket.front.set(1, 1, "S2"), jacket.front.set(6, 1, "S2"), jacket.front.set(1, 0, "S2"), jacket.front.set(6, 0, "S2")
    drips(jacket.front, 2, 12)
    for face in (jacket.back,):
        face.hline(0, 7, 9, "S2")
    belt(g, "apron_tie", 9.4, role="S", base=2, height=1, buckle=None)
    skirt = g.piece("apron_skirt", "TORSO", (-3.5, 0, 0), (7, 6, 1), pivot=(0, 10.4, -2.85), motion="flap_front")
    solid(skirt, "S", "smooth", 4004, 2)
    drips(skirt.front, 0, 6)
    skirt.front.hline(0, 6, 5, "S1")
    # Tallow candles hung by their wicks from the apron tie.
    for i, (x, y) in enumerate(((2.4, 10.6), (3.2, 10.9), (4.0, 10.5))):
        c = blk(g, f"candle_{i}", (x, y, -2.85), (1, 3, 1), "S", 4 - (i == 1), "plain", 4005 + i, motion="sway")
        c.strip.hline(0, c.strip.w - 1, 0, "K2")
