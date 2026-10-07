"""Buckled Leather Spats: pressed wool trousers over low shoes, leather spats buckled up the outside of each ankle."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from paint import fabric

META = {
    "name": "Buckled Leather Spats",
    "gender": "male",
    "description": "Pressed wool trousers over low shoes, guarded by stiff leather spats buckled twice up the outside of each ankle.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 4211, rows=(0, 9))
    waistband(g, "P", "weave", 4212)
    footwear(g, "shoe", top=10, base=1)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            fabric(face, "L", "leather", 4213, 2, 0, 7, face.w, 4)
            face.hline(0, face.w - 1, 7, "L3"), face.hline(0, face.w - 1, 10, "L1")
        outer = pants.right if side == "right" else pants.left
        outer.set(1, 8, "M3"), outer.set(1, 9, "M3")
        buckle = leg_blk(g, f"{side}_spat_buckle", side, 8.0, (1, 2, 1), "M", 2, "smooth", 4214 + i,
                         dx=-2.25 if side == "right" else 2.25, dz=-.4)
        buckle.strip.hline(0, buckle.strip.w - 1, 0, "M4")
