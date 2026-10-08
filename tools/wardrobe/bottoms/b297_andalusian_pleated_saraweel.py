"""Andalusian Pleated Saraweel and Slippers: finely pleated linen saraweel gathered at the calf, a tasselled drawcord and leather slippers."""
from kit import SIDES, waistband
from kit_male import leg_rings, toe_pieces
from kit_m08 import pleats, tassel
from paint import fabric

META = {
    "name": "Andalusian Pleated Saraweel and Slippers",
    "gender": "male",
    "description": "Pale linen saraweel falling in fine pleats and gathered into a band at the calf, a tasselled drawcord, bare ankles and pointed leather slippers embroidered on the vamp.",
    "tags": ["fancy", "relaxed"],
    "rejects": ["armor"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        pleats(leg.strip, "S", 3, rows=range(0, 9), ox=i)
        fabric(leg.top, "S", "weave", 38061, 3)
        pleats(pants.strip, "S", 3, rows=range(0, 7), ox=i + 1)           # roomy legs stand off the shin
        pants.strip.hline(0, pants.strip.w - 1, 6, "S1")
        # Slippers: two rows of soft leather, an embroidered vamp and a thin leather sole.
        fabric(leg.strip, "L", "smooth", 38062, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "L", "smooth", 38063, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 10, "L3")
            face.hline(0, face.w - 1, 11, "K1")
        pants.front.set(1, 10, "A3"), pants.front.set(2, 10, "A2")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
    body = waistband(g, "S", "weave", 38064, base=3)
    body.front.vline(4, 10, 11, "S1")
    for ring in leg_rings(g, "calf_band", 7.4, "A", (5, 1, 5), 2, "weave", 38065, inflate=.06):
        for face in ring.sides:
            for x in range(0, face.w, 2):
                face.set(x, 0, "A3")
        ring.bottom.fill("S1")
    tassel(g, "waist_cord_tassel", (.8, 10.4, -2.45), "A", length=3, cord="S2")
    for toe in toe_pieces(g, "slipper_toe", (2, 1, 2), "L", base=2, y=11.0, z=-1.9, seed=38067):
        toe.top.set(0, 1, "A3"), toe.top.set(1, 1, "A3")
    for tip in toe_pieces(g, "slipper_tip", (1, 1, 1), "L", base=3, y=11.0, z=-3.8, seed=38069):
        tip.top.fill("L4")
