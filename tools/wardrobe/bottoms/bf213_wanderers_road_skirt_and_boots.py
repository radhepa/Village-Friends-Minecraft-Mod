"""Wanderer's Road Skirt and Boots: a mid-calf twill skirt hitched up at both sides on cords and toggles,
a double band at the hem, and tall boots strapped with two buckles each."""
from kit import SIDES
from kit_female import leg_rings, shoes, skirt, waist_belt
from paint import solid

META = {
    "name": "Wanderer's Road Skirt and Boots",
    "gender": "female",
    "description": "A mid-calf twill skirt hitched up at both hips on cords and wooden toggles, over tall walking "
                   "boots strapped with two buckles each.",
    "tags": ["rugged", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 57221, top=9.8, length=8, side_length=6, flare=7)
    s.band(2, "double", "A2", from_bottom=True)
    s.hem("P1")
    for box, face in ((s.right, s.right.right), (s.left, s.left.left)):
        # The hitched side: gathered up on a cord to a toggle at the hip.
        for y in range(1, face.h - 1):
            face.set(2, y, "L3" if y % 2 else "L2")
        face.set(1, 1, "L1"), face.set(2, 1, "L4"), face.set(3, 1, "L1")
        for x in range(face.w):
            face.set(x, face.h - 1, "P1" if x % 2 else "P3")
        face.set(1, face.h - 2, "P1"), face.set(3, face.h - 2, "P1")
    shoes(g, "boot", "L", 3, top=5)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 5, "L3")
    for i, y in enumerate((6.4, 9.0)):
        for box in leg_rings(g, f"boot_strap_{i}", y, 1, 5, inflate=.03):
            solid(box, "L", "leather", 57222 + i, 0, edge=False)
            box.front.set(3, 0, "M3"), box.front.set(2, 0, "M1")
    waist_belt(g, "waist_belt", 9.4, role="L", height=1)
