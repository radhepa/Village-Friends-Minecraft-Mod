"""Felt Slippers & Hose: dark study hose in thick felt slippers with turned-down cuffs, for long hours at the desk."""
from kit import SIDES, legs, waistband
from kit_male import leg_rings, toe_pieces
from paint import fabric

META = {
    "name": "Felt Slippers & Hose",
    "gender": "male",
    "description": "Dark woollen study hose in thick felt slippers with turned-down cuffs and rounded toes, for long hours at the desk.",
    "tags": ["scholarly", "slim", "casual"],
}


def build(g):
    legs(g, "P", "weave", 5411, base=1, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 5412, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        fabric(leg.strip, "A", "plain", 5413, 2, 0, 9, leg.strip.w, 3)
        for face in pants.sides:
            fabric(face, "A", "plain", 5414, 2, 0, 9, face.w, 3)
            face.hline(0, face.w - 1, 11, "A0")
        leg.bottom.fill("A0"), pants.bottom.fill("K1")
    for cuff in leg_rings(g, "felt_cuff", 8.4, "A", (5, 1, 5), 3, "plain", 5415, inflate=.1):
        cuff.front.set(2, 0, "A1")
    for toe in toe_pieces(g, "felt_toe", (4, 1, 1), "A", base=2, texture="plain", y=10.9, z=-2.15):
        toe.front.set(0, 0, "A1"), toe.front.set(3, 0, "A1")
