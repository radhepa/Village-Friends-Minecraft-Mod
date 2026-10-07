"""Rawhide Cuarans & Breeks: hairy wool breeks to the knee, bare shins and pale rawhide cuarans thonged up the ankle."""
from kit import SIDES, legs, waistband
from kit_male import toe_pieces
from paint import line

META = {
    "name": "Rawhide Cuarans & Breeks",
    "gender": "male",
    "description": "Hairy undyed wool breeks to the knee, bare shins, and pale rawhide cuarans drawn up with thongs crossing at the ankle.",
    "tags": ["rugged", "simple"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "S", "tweed", 8311, base=2, rows=(0, 5), crease=False)
    waistband(g, "S", "tweed", 8312)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, leg.strip.w - 1, 5, "S1")
        for face in (leg.right, leg.front, leg.left, leg.back):
            face.hline(0, 3, 10, "L4"), face.hline(0, 3, 11, "L3")         # rawhide shoe
        leg.bottom.fill("L2")
        for face in pants.sides:
            line(face, 0, 8, 3, 9, "L2"), line(face, 3, 8, 0, 9, "L2")     # thongs crossing the ankle
            face.hline(0, face.w - 1, 10, "L4"), face.hline(0, face.w - 1, 11, "L2")
            face.set(1, 10, "L1")                                          # the thong holes
        pants.bottom.fill("L2")
    for toe in toe_pieces(g, "cuaran_toe", (4, 1, 1), "L", base=3, texture="plain", y=10.9, z=-2.1):
        toe.front.set(2, 0, "L1")
