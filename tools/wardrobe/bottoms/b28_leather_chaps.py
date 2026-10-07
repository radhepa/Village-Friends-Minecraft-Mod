"""Leather Chaps: hard leather chaps buckled over canvas trousers, open at the inner leg."""
from kit import SIDES, belt, footwear, legs, waistband
from paint import fabric

META = {
    "name": "Leather Chaps",
    "gender": "male",
    "description": "Hard-wearing leather chaps buckled over canvas trousers, open at the inner leg.",
    "tags": ["rugged", "sturdy", "work"],
}


def build(g):
    legs(g, "S", "twill", 2801, rows=(0, 9))
    waistband(g, "S", "twill", 2802)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        inner = pants.left if side == "right" else pants.right
        for face in pants.sides:
            if face is inner:
                continue
            fabric(face, "L", "leather", 2803, 2, 0, 0, face.w, 9)
            face.hline(0, face.w - 1, 8, "L1")
        outer = pants.right if side == "right" else pants.left
        for y in range(1, 9, 2):
            outer.set(2 if side == "right" else 1, y, "L3")   # stitched outer seam
        pants.front.set(0 if side == "right" else 3, 3, "M3")
    belt(g, "waist_belt", 9.6)
    footwear(g, "boot", top=9)
