"""Forge Breeches & Hobnail Boots: twill breeches with leather knee patches over heavy hobnailed boots with steel toe caps."""
from kit import SIDES, legs, waistband
from kit_female import shoes, waist_belt
from paint import fabric

META = {
    "name": "Forge Breeches & Hobnail Boots",
    "gender": "female",
    "description": "Hard-wearing twill breeches patched with leather at the knee, over hobnailed boots with steel toe caps.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 14111, rows=(0, 8), crease=False)
    waistband(g, "P", "twill", 14112)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        fabric(pants.front, "L", "leather", 14113, 2, 0, 3, 4, 3)
        pants.front.hline(0, 3, 3, "L3"), pants.front.set(0, 5, "L1"), pants.front.set(3, 5, "L1")
    shoes(g, "boot", "L", 1, top=8)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(0, 3, 10, "M2"), pants.front.hline(0, 3, 11, "M1")
        for face in pants.sides:
            for x in range(0, face.w, 2):
                face.set(x, 11, "M3")                                # hobnails
    waist_belt(g, "waist_belt", 9.4, height=1)
