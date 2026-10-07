"""Laced Rawhide Shin Guards: pale rawhide guards wrapped over the shins and laced up the calf, with turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import lacing, leg_blk
from paint import fabric

META = {
    "name": "Laced Rawhide Shin Guards",
    "gender": "male",
    "description": "Twill trousers under stiff rawhide shin guards laced up the back of the calf, and soft turnshoes.",
    "tags": ["work", "rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 3611, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 3612)
    footwear(g, "turnshoe", top=10)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        for face in (pants.right, pants.front, pants.left):
            fabric(face, "L", "leather", 3613, 3, 0, 4, face.w, 6)
            face.hline(0, face.w - 1, 4, "L4"), face.hline(0, face.w - 1, 9, "L2")
            for x in range(0, face.w, 2):
                face.set(x, 6, "L1")                                  # stitch holes
        back = pants.back
        back.vline(0, 4, 9, "L3"), back.vline(3, 4, 9, "L3")
        lacing(back, 1, 4, 9, "L1", "L0")
        tail = leg_blk(g, f"{side}_lace_tail", side, 9.0, (1, 2, 1), "L", 1, "plain", 3614 + i, dz=2.5)
        tail.strip.hline(0, tail.strip.w - 1, 1, "L3")
