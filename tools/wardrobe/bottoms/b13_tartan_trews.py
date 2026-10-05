"""Tartan Trews: close-cut checked trousers in the outfit's colors, with plain ankle boots and a belt."""
from kit import SIDES, belt, footwear, waistband

META = {
    "name": "Tartan Trews",
    "description": "Close-cut tartan trews, a plain leather belt and sturdy ankle boots.",
    "tags": ["casual", "sturdy"],
}


def tartan(face, ox=0):
    for y in range(face.h):
        for x in range(face.w):
            gx, gy = (x + ox) % 6, y % 6
            band_x, band_y = gx in (0, 1), gy in (0, 1)
            key = "P0" if band_x and band_y else "P1" if band_x or band_y else "P2"
            if gx == 4 or gy == 4:
                key = "A2" if not (band_x or band_y) else key
            face.set(x, y, key)


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        tartan(leg.strip, 0 if side == "right" else 3)
        tartan(leg.top)
    body = waistband(g, "P", "twill", 1301)
    belt(g, "waist_belt", 9.6)
    footwear(g, "boot", top=9)
