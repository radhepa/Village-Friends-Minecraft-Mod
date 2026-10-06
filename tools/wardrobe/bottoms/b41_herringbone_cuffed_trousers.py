"""Herringbone Cuffed Trousers: herringbone wool trousers with deep turned-up cuffs over ankle boots fastened by toggles."""
from kit import SIDES, footwear, waistband
from kit_male import herringbone, leg_rings, toggles

META = {
    "name": "Herringbone Cuffed Trousers",
    "gender": "male",
    "description": "Herringbone wool trousers with deep turned-up cuffs, over ankle boots fastened with wooden toggles.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        herringbone(leg.strip, "P", 2, ox=i * 2, rows=range(0, 10))
        herringbone(leg.top, "P", 2)
    waistband(g, "P", "twill", 4111)
    footwear(g, "boot", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        outer = pants.right if side == "right" else pants.left
        toggles(outer, 0, [10], "L4", "L1")
    for i, cuff in enumerate(leg_rings(g, "turned_cuff", 7.8, "P", (5, 2, 5), 2, "twill", 4112, inflate=.08)):
        for face in cuff.sides:
            herringbone(face, "P", 2, ox=i)
            face.hline(0, face.w - 1, 0, "P3")
