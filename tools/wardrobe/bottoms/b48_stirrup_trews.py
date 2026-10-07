"""Stirrup Trews: close twill trews with a strap under the instep, a seam down the shin, and low turnshoes."""
from kit import SIDES, waistband
from paint import fabric, strip_fabric

META = {
    "name": "Stirrup Trews",
    "gender": "male",
    "description": "Close twill trews cut with a strap under each instep and a seam down the shin, worn over low turnshoes.",
    "tags": ["casual", "slim"],
}


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "twill", 4811, 2, 0, 11)
        fabric(leg.top, "P", "twill", 4811, 2)
        c = 1 if side == "right" else 2
        leg.front.vline(c, 0, 9, "P3")                                     # shin seam
        leg.front.set(c, 4, "P1")
        leg.bottom.fill("L0")
        for face in pants.sides:
            fabric(face, "L", "smooth", 4812, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        for face in (pants.right, pants.left):
            face.vline(1, 10, 11, "P1"), face.vline(2, 10, 11, "P2")       # the stirrup under the arch
        pants.front.hline(0, 3, 10, "L3")
        pants.bottom.fill("K0")
    waistband(g, "P", "twill", 4813)
