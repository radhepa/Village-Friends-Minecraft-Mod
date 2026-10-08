"""Orchard Ladder Breeches: full knee breeches with a buttoned fall front and buttoned knee bands for climbing
the ladders, ribbed stockings, buckled shoes and a hooked pruning knife at the hip."""
from kit import SIDES, legs, waistband
from kit_female import leg_rings, shoes
from paint import k, solid, strip_fabric

META = {
    "name": "Orchard Ladder Breeches",
    "gender": "female",
    "description": "Full knee breeches with a buttoned fall front and buttoned knee bands for the ladders, ribbed stockings, buckled shoes and a hooked pruning knife.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 51460, rows=(0, 6), crease=False)
    body = waistband(g, "P", "twill", 51461)
    # The fall front: a square flap buttoned at its two top corners.
    body.front.hline(1, 6, 9, "P1")
    body.front.set(1, 9, "M3"), body.front.set(6, 9, "M3")
    body.front.vline(1, 10, 11, "P1"), body.front.vline(6, 10, 11, "P1")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for f in pants.sides:
            for y in (3, 4):
                for x in range(f.w):
                    f.set(x, y, k("P", 2 if (x + y) % 3 else 1))
            f.hline(0, f.w - 1, 3, "P3")                               # the breeches blouse over the knee band
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "rib", 51462 + (side == "left"), 2, 7, 10)
    for side, box in zip(SIDES, leg_rings(g, "knee_band", 5.6, 2, 5, inflate=.06)):
        solid(box, "P", "twill", 51464, 1, edge=False)
        for f in box.sides:
            f.hline(0, f.w - 1, 0, "P2")
        outer = box.right if side == "right" else box.left
        outer.set(1, 0, "M3"), outer.set(3, 0, "M3"), outer.set(2, 1, "M3")
    shoes(g, "shoe", "L", 1, top=10)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 10, "M3"), pants.front.set(2, 10, "M4")
    # The pruning knife: a hooked blade in a leather frog at the right hip.
    frog = g.piece("waist_knife_frog", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-3.4, 10.0, -2.6), rotation=(0, 0, -10),
                   motion="flap_front")
    solid(frog, "L", "leather", 51465, 2)
    blade = g.piece("waist_pruning_hook", "TORSO", (-.5, 2.6, -.5), (2, 2, 1), pivot=(-3.4, 10.0, -2.6),
                    rotation=(0, 0, -10), motion="flap_front")
    solid(blade, "M", "smooth", 51466, 3, edge=False)
    blade.front.set(1, 0, "M1"), blade.front.set(0, 1, "M4")
