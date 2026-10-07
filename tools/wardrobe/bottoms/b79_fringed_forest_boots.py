"""Fringed Forest Boots: soft hide leggings in calf boots whose turned-down tops are cut into a hanging fringe."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Fringed Forest Boots",
    "gender": "male",
    "description": "Soft hide leggings worn in quiet calf boots whose turned-down tops are cut into a hanging leather fringe.",
    "tags": ["rugged", "casual"],
}


def build(g):
    legs(g, "L", "leather", 7911, base=3, rows=(0, 6), crease=False)
    waistband(g, "L", "leather", 7912, base=3)
    footwear(g, "boot", top=6, base=1)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        outer = leg.right if side == "right" else leg.left
        outer.vline(1, 0, 5, "L2")                                         # seam
    for ring in leg_rings(g, "fringe", 4.6, "L", (5, 3, 5), 2, "leather", 7913, inflate=.12):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3")
            for x in range(face.w):
                face.set(x, 1, "L2" if x % 2 else "L1")
                face.set(x, 2, "L2" if x % 2 else "L0")                    # the cut fringe
