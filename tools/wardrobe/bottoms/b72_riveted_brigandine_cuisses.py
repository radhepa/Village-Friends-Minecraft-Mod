"""Riveted Brigandine Cuisses: cloth-covered thigh plates studded with rivets over quilted hose, with tall riding boots."""
from kit import SIDES, footwear, waistband
from kit_male import leg_blk
from paint import fabric, rivets, strip_fabric

META = {
    "name": "Riveted Brigandine Cuisses",
    "gender": "male",
    "description": "Cloth-covered thigh plates studded with rows of rivets, strapped over quilted hose, with tall riding boots.",
    "tags": ["armor", "sturdy", "martial"],
    "requires": ["martial", "rugged"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "quilt", 7211, 2, 0, 9)
        fabric(leg.top, "S", "quilt", 7211, 2)
    waistband(g, "S", "quilt", 7212)
    footwear(g, "boot", top=6, base=2)
    for i, side in enumerate(SIDES):
        cuisse = leg_blk(g, f"{side}_cuisse", side, .2, (5, 5, 5), "P", 2, "velvet", 7213 + i, inflate=.08)
        for face in cuisse.sides:
            for y in (1, 3):
                rivets(face, y, start=y % 2 + 0, step=2)
            face.hline(0, face.w - 1, 4, "L2")                            # strap below the plates
            face.hline(0, face.w - 1, 0, "P3")
        cuisse.top.fill("P3")
