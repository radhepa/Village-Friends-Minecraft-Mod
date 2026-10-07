"""Starry-Cuffed Soft Boots: night-dark hose in soft pointed boots whose wide turned-down cuffs are sewn with little stars."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings, toe_pieces

META = {
    "name": "Starry-Cuffed Soft Boots",
    "gender": "male",
    "description": "Night-dark hose in soft pointed boots whose wide turned-down cuffs are sewn with little pale stars.",
    "tags": ["scholarly", "whimsical"],
}


def build(g):
    legs(g, "P", "velvet", 9911, base=1, rows=(0, 6), crease=False)
    waistband(g, "P", "velvet", 9912, base=1)
    footwear(g, "boot", top=6, base=2)
    for side in SIDES:
        for face in g.part(f"{side}_pants").sides:
            face.vline(0, 7, 10, "L1")
    for ring in leg_rings(g, "star_cuff", 5.0, "P", (5, 3, 5), 1, "velvet", 9913, inflate=.12):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "M2")
            face.set(1, 1, "S4"), face.set(3, 2, "S4")                    # stitched stars
    for toe in toe_pieces(g, "pointed_toe", (2, 1, 2), "L", base=2, y=11.0, z=-2.1):
        toe.top.fill("L3")
