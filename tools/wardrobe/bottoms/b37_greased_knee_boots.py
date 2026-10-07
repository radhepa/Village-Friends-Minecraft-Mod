"""Greased Knee Boots: tall boots shining with tallow grease, trousers bloused in soft gathers over their tops."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Greased Knee Boots",
    "gender": "male",
    "description": "Tall knee boots shining with tallow grease against the wet, wool trousers bloused in soft gathers over their tops.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 3711, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 3712)
    footwear(g, "boot", top=4, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        c = 1 if side == "right" else 2
        pants.front.vline(c, 5, 9, "L3")
        pants.front.set(c, 6, "L4"), pants.front.set(c, 7, "L4")      # greasy sheen
        pants.back.vline(2, 4, 10, "L0")                              # back seam
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L3")                       # welt stitching
    for ring in leg_rings(g, "blouse", 2.8, "P", (5, 2, 5), 2, "weave", 3713, inflate=.12):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if x % 2 else "P2")
                face.set(x, 1, "P1" if x % 2 else "P2")
