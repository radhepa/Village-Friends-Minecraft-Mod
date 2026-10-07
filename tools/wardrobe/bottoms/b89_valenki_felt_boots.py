"""Valenki Felt Boots: wool trousers stuffed into thick, seamless pale felt boots to the knee, a stitched band at the ankle."""
from kit import SIDES, legs, waistband
from kit_male import leg_rings, toe_pieces
from paint import fabric

META = {
    "name": "Valenki Felt Boots",
    "gender": "male",
    "description": "Wool trousers stuffed into thick, seamless pale felt boots reaching the knee, with a stitched band round the ankle.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 8911, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 8912)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        fabric(leg.strip, "S", "plain", 8913, 2, 0, 4, leg.strip.w, 8)
        for face in pants.sides:
            fabric(face, "S", "plain", 8914, 2, 0, 4, face.w, 8)
            face.hline(0, face.w - 1, 4, "S3")
            face.hline(0, face.w - 1, 9, "A2")                             # stitched ankle band
            face.hline(0, face.w - 1, 11, "S0")
        leg.bottom.fill("S0"), pants.bottom.fill("S0")
    for ring in leg_rings(g, "felt_top", 3.0, "S", (5, 2, 5), 2, "plain", 8915, inflate=.18):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 1, "S1")
    for toe in toe_pieces(g, "felt_toe", (4, 2, 1), "S", base=2, texture="plain", y=9.9, z=-2.15, inflate=.1):
        toe.front.set(0, 1, "S1"), toe.front.set(3, 1, "S1")
