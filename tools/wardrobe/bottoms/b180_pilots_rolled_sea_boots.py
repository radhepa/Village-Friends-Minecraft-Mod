"""Pilot's Rolled Sea Boots: full wool trousers bloused into soft calf boots whose tops are rolled down twice, a
seaman's knife riding in the right roll."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import leg_rings
from paint import solid

META = {
    "name": "Pilot's Rolled Sea Boots",
    "gender": "male",
    "description": "Full wool trousers bloused into soft calf boots whose tops are rolled down twice, a seaman's knife "
                   "riding in the right-hand roll.",
    "tags": ["sea", "sturdy", "casual"],
}


def build(g):
    legs(g, "P", "weave", 33380, rows=(0, 5), crease=False)
    body = waistband(g, "P", "weave", 33381)
    body.front.vline(4, 10, 11, "P1")
    footwear(g, "boot", top=6, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:                                        # soft leather creasing at the ankle
            face.set(1, 8, "L1"), face.set(2, 9, "L1")
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, 15, 5, "P1")
    # The bloused trouser leg spilling over the boot.
    for ring in leg_rings(g, "trouser_blouse", 3.4, "P", (5, 2, 5), 2, "weave", 33382, inflate=.36):
        for face in ring.sides:
            face.hline(0, face.w - 1, 1, "P1")
            face.set(1, 0, "P3"), face.set(3, 0, "P1")
    # Two rolls of boot top: the lower one tight, the upper one fatter and lighter where the flesh side shows.
    for ring in leg_rings(g, "boot_roll_low", 6.2, "L", (5, 1, 5), 2, "leather", 33384, inflate=.22):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3")
    for ring in leg_rings(g, "boot_roll_high", 5.2, "L", (5, 1, 5), 3, "leather", 33386, inflate=.34):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "L4" if (x + face.x0) % 3 == 0 else "L3")
        ring.bottom.fill("L1")
    # The seaman's knife: its wooden grip standing out of the right boot roll on the outside.
    grip = g.piece("right_boot_knife", leg_bone("right"), (0, 0, 0), (1, 2, 1), pivot=(-2.75, 4.0, -.5))
    solid(grip, "L", "plain", 33388, 3)
    grip.top.fill("M3")
    grip.strip.hline(0, grip.strip.w - 1, 1, "M2")
