"""Summer Knee Breeches: loose linen breeches ending in open cuffs at the knee, bare shins and strapped low shoes."""
from kit import SIDES, waistband
from kit_m10 import leg_ring, outer, tie
from paint import fabric, k, strip_fabric

META = {
    "name": "Summer Knee Breeches",
    "gender": "male",
    "description": "Loose linen breeches ending in wide open cuffs just below the knee, bare summer shins and low shoes strapped at the ankle.",
    "tags": ["casual", "simple", "relaxed"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 40060 + i, 3, 0, 6)
        fabric(leg.top, "S", "weave", 40060, 3)
        strip_fabric(pants, "S", "weave", 40062 + i, 3, 0, 4)
        for face in pants.sides:
            face.vline(1, 1, 4, "S2")                                     # loose folds
        outer(leg, side).vline(2, 0, 6, "S2")
        # Low shoes with a strap round the ankle; shins left bare.
        strip_fabric(leg, "L", "smooth", 40064, 1, 10, 11)
        for face in pants.sides:
            fabric(face, "L", "smooth", 40065, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        pants.front.hline(0, 3, 10, "L3")
        pants.front.hline(0, 3, 11, "L3")
        leg.strip.hline(0, leg.strip.w - 1, 9, "L2")                      # ankle strap
        leg.front.set(1 if side == "right" else 2, 9, "M3")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
        ring = leg_ring(g, f"{side}_knee_cuff", side, 4.6, (5, 2, 5), "S", 3, "weave", 40066 + i)
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "S4")
            face.hline(0, face.w - 1, 1, "S2")
        tie(g, f"{side}_knee_tie", "RIGHT_LEG" if side == "right" else "LEFT_LEG",
            (-2.55 if side == "right" else 2.55, 5.6, -.5), "S", 2, 2, 40068 + i)
    body = waistband(g, "S", "weave", 40070, base=3)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "S2" if x % 2 else "S4")                       # drawstring gathers
    for i, x in enumerate((-.6, .6)):
        tie(g, f"waist_drawstring_{i}", "TORSO", (x, 9.8, -2.55), "S", 2, 2, 40071 + i, rotation=(0, 0, -12 + 24 * i))
