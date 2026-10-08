"""Lady Sergeant's Splinted Boots and Skirt: a heavy calf-length wool skirt with a guarded hem over tall boots
strapped with steel splints down the shins."""
from kit import SIDES, leg_bone
from kit_female import shoes, skirt, waist_belt
from paint import solid

META = {
    "name": "Lady Sergeant's Splinted Boots and Skirt",
    "gender": "female",
    "description": "A heavy calf-length wool skirt with a guarded hem, over tall boots strapped with steel splints "
                   "down the shins.",
    "tags": ["martial", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 54101, top=9.8, length=8, flare=6)
    s.band(2, "double", "A2", from_bottom=True)
    s.hem("P1")
    shoes(g, "boot", "L", 2, top=4)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 4, "L3")
        for i, x in enumerate((-1.25, 1.25)):
            splint = g.piece(f"{side}_shin_splint_{i}", leg_bone(side), (-.5, 0, -1), (1, 6, 1), pivot=(x, 5.6, -2.25),
                             inflate=.05)
            solid(splint, "M", "smooth", 54102 + i, 2, edge=False)
            splint.front.vline(0, 0, 5, "M3"), splint.front.set(0, 0, "M4"), splint.front.set(0, 5, "M1")
        for j, y in enumerate((6.6, 9.4)):
            strap = g.piece(f"{side}_splint_strap_{j}", leg_bone(side), (-2.5, y, -2.5), (5, 1, 5), inflate=.12)
            solid(strap, "L", "leather", 54104 + j, 2, edge=False)
            strap.front.set(0 if side == "right" else 4, 0, "M3")
            (strap.right if side == "right" else strap.left).set(2, 0, "M4")    # buckle on the outer side
    waist_belt(g, "waist_belt", 9.4, height=1)
