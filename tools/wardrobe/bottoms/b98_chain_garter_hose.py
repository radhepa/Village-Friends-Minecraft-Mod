"""Chain-Garter Hose: fine velvet hose held below the knee by garters of linked metal, over slender buckled shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Chain-Garter Hose",
    "gender": "male",
    "description": "Fine velvet hose held below the knee by garters of linked metal, over slender shoes with bright buckles.",
    "tags": ["fancy", "slim"],
}


def build(g):
    legs(g, "P", "velvet", 9811, rows=(0, 9), crease=False)
    waistband(g, "P", "velvet", 9812)
    footwear(g, "shoe", top=10, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 10, "M4"), pants.front.set(2, 10, "M3")
    for ring in leg_rings(g, "chain_garter", 4.8, "M", (5, 1, 5), 2, "smooth", 9813, inflate=.06):
        for face in ring.faces:
            for x in range(face.w):
                for y in range(face.h):
                    face.set(x, y, "M4" if (x + y) % 2 else "M1")         # linked chain
