"""Rolled-Down Hose: loose linen braies puffing over hose rolled carelessly down below the knee, and scuffed turnshoes."""
from kit import SIDES, footwear, waistband
from kit_male import leg_rings
from paint import fabric, strip_fabric

META = {
    "name": "Rolled-Down Hose",
    "gender": "male",
    "description": "Loose linen braies puffing above hose rolled carelessly down below the knee in the heat, with scuffed turnshoes.",
    "tags": ["casual", "relaxed"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "weave", 6911, 3, 0, 4)
        fabric(leg.top, "S", "weave", 6911, 3)
        for x in range(leg.strip.w):
            leg.strip.set(x, 4, "S2" if x % 2 else "S3")                  # braies gathered at the knee
        strip_fabric(leg, "P", "weave", 6912, 2, 7, 9)                    # what is left of the hose
    waistband(g, "S", "weave", 6913, base=3)
    footwear(g, "turnshoe", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(0, 11, "L4"), pants.right.set(2, 10, "L1")
    for ring in leg_rings(g, "hose_roll", 5.2, "P", (5, 2, 5), 2, "weave", 6914, inflate=.08):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P3"), face.hline(0, face.w - 1, 1, "P1")
            face.set(1, 1, "P2")
