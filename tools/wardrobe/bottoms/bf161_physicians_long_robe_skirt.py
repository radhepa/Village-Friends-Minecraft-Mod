"""Physician's Long Robe Skirt: a floor-length robe skirt vented at both sides over lined gores, with a
bound hem and dark pointed shoes."""
from kit_female import shoes, skirt
from paint import fabric

META = {
    "name": "Physician's Long Robe Skirt",
    "gender": "female",
    "description": "A sober floor-length robe skirt vented at the sides over pale lined gores, with a bound hem and pointed shoes.",
    "tags": ["scholarly", "robe", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 55021, base=1, top=9.8, length=12, back_length=13, folds=False, gather=False)
    for face in s.wide_faces:
        face.hline(0, face.w - 1, 0, "P2")
        for x in (0, face.w - 1):
            face.vline(x, 3, face.h - 2, "S3")                       # the lining showing at each vent
        face.vline(1, 3, face.h - 2, "P0"), face.vline(face.w - 2, 3, face.h - 2, "P0")
        for x in (3, 6):
            face.vline(x, 2, face.h - 3, "P0")
        face.vline(4, 4, face.h - 3, "P2")
        face.hline(0, face.w - 1, face.h - 1, "L1")                  # bound hem
    for box in (s.right, s.left):
        outer = box.right if box is s.right else box.left
        fabric(outer, "S", "weave", 55022, 2, 0, 3, outer.w, outer.h - 3)
        for x in range(0, outer.w, 2):
            outer.vline(x, 3, outer.h - 2, "S1")                     # the gore's own fine pleats
        outer.hline(0, outer.w - 1, 2, "P0")
        outer.hline(0, outer.w - 1, outer.h - 1, "L1")
        for face in (box.front, box.back):
            face.vline(0, 3, face.h - 1, "S2")
    for side in ("right", "left"):
        g.part(f"{side}_leg").strip.hline(0, 15, 10, "P0")
    shoes(g, "pointed", "K", 2)
