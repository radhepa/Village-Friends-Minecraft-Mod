"""Watchman's Lantern Coat: a town watch coat with a pewter badge, a horn lantern glowing at the hip and a wooden rattle."""
from kit import belt, body, collar, flaps, sleeves
from kit_male import blk, buttons

META = {
    "name": "Watchman's Lantern Coat",
    "gender": "male",
    "description": "A night watchman's warm coat with a turned collar and pewter badge, a horn lantern glowing at the hip and a wooden rattle.",
    "tags": ["martial", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 7701)
    b.front.vline(4, 0, 11, "P0")
    buttons(b.front, 3, 2, 8, 3, "L3")
    b.front.rect(5, 2, 2, 2, "M3"), b.front.set(5, 2, "M4")              # watch badge
    sleeves(g, "P", "weave", 7702, rows=(0, 10), cuff="P1")
    turned = collar(g, "turned_collar", "P", "weave", base=1, height=2, y=-1.0)
    turned.front.vline(4, 0, 1, "P0")
    belt(g, "belt", 9.4)
    frame = blk(g, "lantern", (-3.0, 10.6, -2.85), (2, 3, 2), "A", 3, "plain", 7703)
    for face in frame.sides:
        face.vline(0, 0, 2, "M1"), face.set(1, 1, "A4")                  # horn panes glowing
    frame.top.fill("M2"), frame.bottom.fill("M1")
    blk(g, "lantern_ring", (-3.0, 9.8, -2.85), (1, 1, 1), "M", 2, "smooth", 7704, edge=False)
    rattle = blk(g, "watch_rattle", (3.0, 10.0, -2.8), (1, 4, 1), "L", 3, "plain", 7705)
    rattle.strip.hline(0, rattle.strip.w - 1, 0, "L1")
    for face in flaps(g, "coat_skirt", 4, "P", "weave", 7706, top=10.8, slit=True):
        face.hline(0, 8, 3, "P1")
