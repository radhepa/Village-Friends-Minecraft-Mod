"""Scorched Leather Leggings: stiff leather leggings pocked with burn holes from the furnace, over iron-shod wooden-soled boots."""
from kit import SIDES, footwear, waistband
from paint import fabric, strip_fabric

META = {
    "name": "Scorched Leather Leggings",
    "gender": "male",
    "description": "Stiff leather leggings pocked with burn holes from the furnace, over boots with thick wooden soles shod in iron.",
    "tags": ["work", "sturdy"],
}

BURNS = ((1, 2), (6, 5), (10, 3), (13, 7), (3, 8))


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "L", "leather", 10011, 3, 0, 9)
        fabric(leg.top, "L", "leather", 10011, 3)
        for x, y in BURNS:
            leg.strip.set(x, y, "K2"), leg.strip.set(x + 1, y, "L1"), leg.strip.set(x, y + 1, "L1")
    waistband(g, "L", "leather", 10012, base=3)
    footwear(g, "boot", top=9, base=1, sole="M2")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L4")                          # the thick wooden sole
        pants.bottom.fill("M1")
