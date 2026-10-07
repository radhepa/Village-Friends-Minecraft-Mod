"""Bearskin Leggings: shaggy fur leggings bound with crossing hide thongs, over fur-lined boots with a pale turned cuff."""
from kit import SIDES, waistband
from kit_male import fur_face, leg_rings
from paint import fabric

META = {
    "name": "Bearskin Leggings",
    "gender": "male",
    "description": "Shaggy fur leggings bound at the shin with crossing hide thongs, over fur-lined boots with a pale turned cuff.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        fur_face(leg.strip, "L", 8111, 2, rows=range(0, 10))
        fur_face(leg.top, "L", 8111, 2)
        for y in range(3, 9):
            for x in range(pants.strip.w):
                if (x + y) % 6 == 0 or (x - y) % 6 == 0:
                    pants.strip.set(x, y, "L4")                            # crossing thongs
        fabric(leg.strip, "L", "leather", 8112, 1, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "L", "leather", 8113, 1, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
    waistband(g, "L", "leather", 8114, base=2)
    for ring in leg_rings(g, "boot_cuff", 9.0, "S", (5, 1, 5), 3, "plain", 8115, inflate=.12):
        for face in ring.faces:
            fur_face(face, "S", 8116, 3)
