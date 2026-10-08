"""Coracle Man's Wading Breeks: heavy wool breeks to the knee, laced open at the outer knee and soaked dark at the
hem, over bare calves and soft rawhide shoes with thongs crossed round the ankle."""
from kit import SIDES, legs, waistband
from kit_m03 import soak
from kit_male import leg_blk
from paint import fabric

META = {
    "name": "Coracle Man's Wading Breeks",
    "gender": "male",
    "description": "Heavy wool breeks to the knee, laced open at the outer knee and soaked dark at the hem, over bare "
                   "calves and soft rawhide shoes with thongs crossed round the ankle.",
    "tags": ["sea", "relaxed", "simple"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "P", "weave", 33580, rows=(0, 6), crease=False)
    waistband(g, "P", "weave", 33581)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        soak(leg.strip, "P", range(4, 7), seed=33582 + i)
        outer = leg.right if side == "right" else leg.left
        for y in range(3, 7):                                            # the laced slit at the outer knee
            outer.set(1, y, "K2" if y % 2 else "L3"), outer.set(2, y, "L3" if y % 2 else "K2")
        # Rawhide shoes: pale hide gathered round the foot, thongs crossing up the ankle.
        fabric(leg.strip, "L", "leather", 33584 + i, 3, 0, 10, 16, 2)
        leg.strip.hline(0, 15, 11, "L2")
        for x in range(16):
            leg.strip.set(x, 9, "L1" if x % 4 in (0, 3) else None)
            if x % 4 == 1:
                leg.strip.set(x, 8, "L1")
        for face in pants.sides:
            fabric(face, "L", "leather", 33586 + i, 3, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "L1")
            face.set(1, 10, "L4")
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
        # The breek hem stands a little off the leg, heavy with water.
        hem = leg_blk(g, f"{side}_breek_hem", side, 5.6, (5, 1, 5), "P", 1, "weave", 33588 + i, inflate=.1)
        for face in hem.sides:
            for x in range(face.w):
                face.set(x, 0, "P0" if (x + face.x0) % 3 else "P2")
