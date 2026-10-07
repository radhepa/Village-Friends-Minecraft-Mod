"""Spice Merchant's Sash Coat: a long coat wound with a fringed silk sash, accent cuffs and a filigree pomander on a cord."""
from kit import body, flaps, neckline, sleeves
from kit_male import blk, embroider, sash

META = {
    "name": "Spice Merchant's Sash Coat",
    "gender": "male",
    "description": "A travelling spice merchant's long coat wound with a fringed silk sash, broad embroidered cuffs and a filigree pomander.",
    "tags": ["fancy", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 6301)
    neckline(b.front, "v", "P")
    b.front.vline(4, 3, 11, "P0")
    sleeves(g, "P", "twill", 6302, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in (8, 9, 10):
            arm.strip.hline(0, arm.strip.w - 1, y, "A2")
        embroider(arm.strip, 8, "dots", "M3")
    sash(g, "silk_sash", "A", y=8.6, height=2, texture="smooth", seed=6303, tails=((-2.4, 6), (-1.6, -4)), tail_len=5)
    pomander = blk(g, "pomander", (2.8, 10.8, -2.8), (2, 2, 2), "M", 3, "smooth", 6306)
    for face in pomander.sides:
        face.set(0, 0, "M1"), face.set(1, 1, "M1")                       # filigree openings
    blk(g, "pomander_cord", (2.8, 10.0, -2.8), (1, 1, 1), "A", 1, "plain", 6307, edge=False)
    for face in flaps(g, "coat_skirt", 5, "P", "twill", 6308, top=10.8, slit=True):
        embroider(face, 3, "zig", "A3", "A1")
