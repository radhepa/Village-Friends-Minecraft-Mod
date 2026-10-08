"""Dairymaid's Pattens and Petticoat: a warm petticoat stitched in horizontal channels with a scalloped
hem, grey stockings and wooden pattens with leather toe straps for the wet dairy floor."""
from kit import SIDES, leg_bone
from kit_female import shoes, skirt, stockings_row, trim
from paint import k, solid

META = {
    "name": "Dairymaid's Pattens and Petticoat",
    "gender": "female",
    "description": "A warm calf-length petticoat stitched in horizontal channels with a scalloped hem, grey stockings and strapped wooden pattens for the wet dairy floor.",
    "tags": ["work", "simple", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 51220, top=9.8, length=10, flare=6, folds=False)
    for face in s.faces:
        for y in range(3, face.h - 2, 2):
            for x in range(face.w):
                face.set(x, y, k("P", 1) if x % 3 else k("P", 2))     # channel stitching between puffed rows
        for y in range(2, face.h - 2, 2):
            face.hline(0, face.w - 1, y, "P3")
        trim(face, face.h - 2, "scallop", "A2", "A1")
    for box in (s.right, s.left):
        for face in (box.front, box.back):
            for y in range(3, face.h - 2, 2):
                face.set(0, y, "P1")
    stockings_row(g, "S", 8, 10, base=1)
    for side in SIDES:
        g.part(f"{side}_leg").front.vline(1 if side == "right" else 2, 8, 10, "S0")   # the stocking seam
    shoes(g, "turnshoe", "L", 1, top=11)
    # Pattens: a wooden sole on two cross-bars, held on by a broad leather toe strap.
    for side in SIDES:
        sole = g.piece(f"{side}_patten_sole", leg_bone(side), (-2, 0, -2.2), (4, 1, 5), pivot=(0, 11.5, 0), inflate=.1)
        solid(sole, "L", "smooth", 51221, 3, edge=False)
        for f in sole.sides:
            f.hline(0, f.w - 1, 0, "L4")
        sole.bottom.fill("L0")
        strap = g.piece(f"{side}_patten_strap", leg_bone(side), (-2, 0, -2.2), (4, 1, 2), pivot=(0, 10.5, 0), inflate=.16)
        solid(strap, "L", "leather", 51222, 1, edge=False)
        strap.front.set(1, 0, "M3"), strap.front.set(2, 0, "M3")
