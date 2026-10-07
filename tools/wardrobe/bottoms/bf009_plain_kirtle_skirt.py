"""Plain Kirtle Skirt: a plain above-the-ankle kirtle skirt with a darker guard band, white stockings and black shoes."""
from kit_female import shoes, skirt, stockings_row

META = {
    "name": "Plain Kirtle Skirt",
    "gender": "female",
    "description": "A plain kirtle skirt ending above the ankle, a deep guard band, white stockings and buckled black shoes.",
    "tags": ["simple", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 10911, top=9.8, length=10)
    s.band(2, "line", "P0", from_bottom=True)
    s.band(1, "line", "P1", from_bottom=True)
    s.band(0, "line", "P0", from_bottom=True)
    stockings_row(g, "S", 8, 9, base=4)
    shoes(g, "shoe", "K", 3)
    for side in ("right", "left"):
        g.part(f"{side}_pants").front.set(1, 10, "M3")
