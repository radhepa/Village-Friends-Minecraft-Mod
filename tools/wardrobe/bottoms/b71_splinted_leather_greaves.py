"""Splinted Leather Greaves: hose under leather greaves set with steel splints, small knee cops and buckled boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from paint import fabric

META = {
    "name": "Splinted Leather Greaves",
    "gender": "male",
    "description": "Wool hose under leather greaves set with vertical steel splints, small steel knee cops and buckled leather boots.",
    "tags": ["martial", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 7111, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 7112)
    footwear(g, "boot", top=9, base=1)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        inner = pants.left if side == "right" else pants.right
        for face in pants.sides:
            if face is inner:
                continue
            fabric(face, "L", "leather", 7113, 2, 0, 4, face.w, 5)
            for x in range(0, face.w, 2):
                face.vline(x, 4, 8, "M2")                                 # splints
            face.hline(0, face.w - 1, 4, "L3"), face.hline(0, face.w - 1, 8, "L1")
        outer = pants.right if side == "right" else pants.left
        outer.set(1, 10, "M3")
        cop = leg_blk(g, f"{side}_knee_cop", side, 2.6, (4, 2, 1), "M", 2, "smooth", 7114 + i, dz=-2.4)
        cop.front.hline(1, 2, 0, "M4"), cop.front.hline(0, 3, 1, "M1")
