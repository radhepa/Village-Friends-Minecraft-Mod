"""Sicilian Rope-Soled Trousers: drawstring trousers turned up at mid-calf over bare shins and canvas shoes on thick braided rope soles."""
from kit import SIDES, legs, waistband
from kit_casual import rolled_hems
from kit_male import leg_rings
from kit_m08 import tassel
from paint import fabric

META = {
    "name": "Sicilian Rope-Soled Trousers",
    "gender": "male",
    "description": "Loose drawstring trousers turned up at mid-calf over bare shins, and plain canvas shoes set on thick soles of braided rope.",
    "tags": ["casual", "relaxed"],
}


def build(g):
    legs(g, "P", "twill", 38341, rows=(0, 7), crease=False)
    body = waistband(g, "P", "twill", 38342)
    body.front.vline(4, 10, 11, "P1")
    rolled_hems(g, "P", base=3, y=6.4)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        fabric(leg.strip, "S", "weave", 38343, 3, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "S", "weave", 38344, 3, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 10, "S4")
        pants.front.set(1, 11, "S1"), pants.front.set(2, 11, "S1")         # the stitched toe seam
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
    for ring in leg_rings(g, "rope_sole", 11.0, "L", (5, 1, 5), 3, "plain", 38345, inflate=.02):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "L4" if x % 2 == 0 else "L2")               # the braided jute
        ring.top.fill("L3")
        ring.bottom.fill("L1")
    tassel(g, "waist_drawcord", (.4, 10.2, -2.45), "S", length=2, cord="S2")
