"""Fur-Topped Winter Boots: wool trousers tucked into tall boots with thick fur cuffs."""
from kit import footwear, leg_ring, legs, waistband
from paint import rnd

META = {
    "name": "Fur-Topped Winter Boots",
    "gender": "male",
    "description": "Wool trousers tucked into tall winter boots with thick fur cuffs.",
    "tags": ["rugged", "sturdy", "casual"],
}


def build(g):
    legs(g, "P", "weave", 2101, rows=(0, 5))
    waistband(g, "P", "weave", 2102)
    footwear(g, "boot", top=6)
    for ring in leg_ring(g, "fur_cuff", 4.4, "S", base=3, size=(6, 3, 6)):
        for face in ring.faces:
            for y in range(face.h):
                for x in range(face.w):
                    r = rnd(x, y, 2103 + face.x0)
                    face.set(x, y, "S4" if r > .65 else "S2" if r < .2 else "S3")
