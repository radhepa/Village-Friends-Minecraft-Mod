"""Tall Riding Boots: slim trousers with thigh-high riding boots folded down at the top."""
from kit import SIDES, footwear, leg_ring, legs, waistband

META = {
    "name": "Tall Riding Boots",
    "description": "Slim trousers and thigh-high riding boots with folded-down tops.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    legs(g, "S", "twill", 2201, rows=(0, 3))
    waistband(g, "S", "twill", 2202)
    footwear(g, "boot", top=3, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.vline(1 if side == "right" else 2, 4, 9, "L2")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L0")
    for ring in leg_ring(g, "boot_fold", 2.2, "L", base=3, size=(5, 2, 5), texture="leather"):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 1, "L2")
