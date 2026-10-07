"""Studded Leather Trousers: hard leather trousers set with rows of iron studs down the thighs, and heavy boots."""
from kit import SIDES, footwear, waistband
from paint import fabric, strip_fabric

META = {
    "name": "Studded Leather Trousers",
    "gender": "male",
    "description": "Hard leather trousers set with rows of iron studs down the front of the thighs, worn with heavy cuffed boots.",
    "tags": ["martial", "rugged"],
}


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "L", "leather", 7711, 2, 0, 9)
        fabric(leg.top, "L", "leather", 7711, 2)
        for y in range(1, 7, 2):
            for x in (0, 2):
                leg.front.set(x + (y // 2) % 2, y, "M3")                    # staggered studs
        outer = leg.right if side == "right" else leg.left
        outer.vline(1, 0, 8, "L1")
    waistband(g, "L", "leather", 7712)
    footwear(g, "boot", top=8, base=1)
    for side in SIDES:
        for face in g.part(f"{side}_pants").sides:
            face.hline(0, face.w - 1, 8, "L3"), face.hline(0, face.w - 1, 9, "L1")
