"""Linen Calf Braies: very loose linen braies blousing over a bound band at mid-calf, a drawstring waist, bare ankles and soft turnshoes."""
from kit import SIDES, footwear, leg_bone, waistband
from kit_m10 import leg_ring, outer, tie
from paint import fabric, strip_fabric

META = {
    "name": "Linen Calf Braies",
    "gender": "male",
    "description": "Very loose linen braies that blouse over a narrow band wound round each mid-calf, a drawstring at the waist, bare ankles and soft turnshoes.",
    "tags": ["casual", "simple", "relaxed"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 40400 + i, 3, 0, 8)
        fabric(leg.top, "S", "weave", 40400, 3)
        strip_fabric(pants, "S", "weave", 40402 + i, 3, 0, 5)           # roomy legs standing off
        for face in pants.sides:
            for x in (0, 2):
                face.vline(x, 1, 5, "S2")                                # long soft folds
        outer(leg, side).vline(1, 0, 8, "S2")
        # The cloth blousing over the calf band.
        puff = leg_ring(g, f"{side}_braies_blouse", side, 5.4, (5, 2, 5), "S", 3, "weave", 40404 + i, inflate=.2)
        for face in puff.sides:
            for x in range(face.w):
                face.set(x, 0, "S3" if x % 2 else "S4")
                face.set(x, 1, "S2" if x % 2 else "S1")
        # The band wound round the calf.
        band = leg_ring(g, f"{side}_calf_band", side, 7.3, (5, 2, 5), "P", 2, "weave", 40406 + i, open_bottom=False)
        for face in band.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 1, "P1")
            face.set(1, 0, "P2"), face.set(3, 1, "P2")                   # the wound overlap
        tie(g, f"{side}_calf_tie", leg_bone(side), (-2.65 if side == "right" else 2.65, 8.8, .4), "P", 2, 2, 40408 + i)
    body = waistband(g, "S", "weave", 40410, base=3)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "S2" if x % 2 else "S4")                       # gathered on the drawstring
    for j, x in enumerate((-.5, .5)):
        tie(g, f"waist_drawstring_{j}", "TORSO", (x, 10.0, -2.5), "P", 2, 2, 40411 + j, rotation=(0, 0, 10 - 20 * j))
    footwear(g, "turnshoe", top=10, base=2)
