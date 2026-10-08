"""Harbour Master's Buckled Boots: polished jackboots with stiff bucket tops standing off the knee, broad brass-
buckled straps across the instep, over close wool breeches."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Harbour Master's Buckled Boots",
    "gender": "male",
    "description": "Polished jackboots with stiff bucket tops standing off the knee and broad brass-buckled straps across "
                   "the instep, over close wool breeches.",
    "tags": ["tailored", "sturdy", "sea"],
}


def build(g):
    legs(g, "P", "twill", 33300, rows=(0, 4), crease=True)
    body = waistband(g, "P", "twill", 33301)
    body.front.vline(4, 9, 11, "P1"), body.front.set(4, 10, "M3")
    footwear(g, "boot", top=5, base=1, sole="K0")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.vline(1 if side == "right" else 2, 6, 9, "L3")       # the polish catching the light
        pants.front.set(1 if side == "right" else 2, 7, "L4")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L0")
    # Bucket tops: a stiff flared cup of leather round the knee.
    for ring in leg_rings(g, "boot_bucket", 3.0, "L", (5, 3, 5), 1, "smooth", 33302, inflate=.45):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3")
            face.hline(0, face.w - 1, 2, "L0")
        ring.front.set(1, 1, "L2"), ring.front.set(2, 1, "L3")
        ring.top.fill("K1")
    # Broad straps across the instep, closed with square brass buckles on the outside.
    for i, ring in enumerate(leg_rings(g, "instep_strap", 9.2, "L", (5, 1, 5), 2, "leather", 33304, inflate=.12)):
        outer = ring.right if i == 0 else ring.left
        outer.hline(1, 3, 0, "M4"), outer.set(2, 0, "M1")
        ring.front.hline(0, 4, 0, "L3")
