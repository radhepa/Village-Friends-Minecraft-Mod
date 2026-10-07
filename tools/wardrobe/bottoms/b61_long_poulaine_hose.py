"""Long Poulaine Hose: fine velvet hose ending in fashionably long pointed poulaines with upturned tips, and jewelled garters."""
from kit import SIDES, legs, waistband
from kit_male import toe_pieces
from paint import fabric

META = {
    "name": "Long Poulaine Hose",
    "gender": "male",
    "description": "Fine velvet hose with jewelled garters, ending in fashionably long pointed poulaine shoes with upturned tips.",
    "tags": ["fancy", "slim"],
}


def build(g):
    legs(g, "P", "velvet", 6111, rows=(0, 9), crease=False)
    waistband(g, "P", "velvet", 6112)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, leg.strip.w - 1, 5, "M2")
        leg.front.set(1 if side == "right" else 2, 5, "A3")                # garter jewel
        fabric(leg.strip, "K", "smooth", 6113, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "K", "smooth", 6114, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K0")
        leg.bottom.fill("K0"), pants.bottom.fill("K0")
    for toe in toe_pieces(g, "poulaine", (2, 1, 4), "K", base=2, y=11.0, z=-2.1):
        toe.top.fill("K3")
    for tip in toe_pieces(g, "poulaine_tip", (1, 1, 1), "K", base=3, y=10.5, z=-5.6, rotation=(-35, 0, 0)):
        tip.front.fill("K4")
