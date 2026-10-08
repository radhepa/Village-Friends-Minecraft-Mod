"""Lancer's Steel Cuisses and Sabatons: full leg harness of steel, winged poleyns and pointed laminated sabatons."""
from kit import SIDES, waistband
from kit_male import leg_blk, toe_pieces
from kit_m04 import lames, sides_of
from paint import cap, fabric, solid, strip_fabric

META = {
    "name": "Lancer's Steel Cuisses and Sabatons",
    "gender": "male",
    "description": "A full harness for the legs: ridged steel cuisses over the thighs, domed poleyns with fan-shaped side "
                   "wings, closed greaves and pointed sabatons built up of overlapping lames.",
    "tags": ["armor", "martial", "sturdy"],
    "requires": ["martial", "rugged"],
}

S = 34420


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "quilt", S + (side == "left"), 2, 0, 11)
        fabric(leg.top, "S", "quilt", S, 2)
        leg.bottom.fill("M1")
        for face in pants.sides:
            fabric(face, "M", "smooth", S + 2, 2, 0, 0, face.w, 12)
            face.hline(0, face.w - 1, 0, "M4")
            face.hline(0, face.w - 1, 4, "M1")                             # cuisse's lower edge
            face.hline(0, face.w - 1, 6, "M3")                             # greave's top
            lames(face, 9, 11, "M", 2, step=1)
            face.hline(0, face.w - 1, 9, "M4"), face.hline(0, face.w - 1, 10, "M2"), face.hline(0, face.w - 1, 11, "M0")
        ridge = 1 if side == "right" else 2
        pants.front.vline(ridge, 1, 3, "M4"), pants.front.vline(ridge, 7, 8, "M4")
        inner = getattr(pants, sides_of(side)[1])
        inner.vline(1, 7, 8, "L2")                                         # greave hinge strap
        pants.bottom.fill("M0")
    waistband(g, "S", "quilt", S + 3)
    for i, side in enumerate(SIDES):
        poleyn = g.piece(f"{side}_poleyn", "RIGHT_LEG" if side == "right" else "LEFT_LEG", (-2, 0, -1), (4, 3, 2),
                         pivot=(0, 4.0, -1.7), rotation=(-6, 0, 0))
        solid(poleyn, "M", "smooth", S + 4 + i, 2)
        cap(poleyn, "M", top_delta=2, bottom_delta=-1)
        poleyn.front.hline(1, 2, 0, "M4"), poleyn.front.set(1, 1, "M4"), poleyn.front.hline(0, 3, 2, "M1")
        wing = leg_blk(g, f"{side}_poleyn_wing", side, 3.6, (1, 3, 3), "M", 2, "smooth", S + 6 + i,
                       dx=-2.6 if side == "right" else 2.6, dz=-.6)
        outer = getattr(wing, sides_of(side)[0])
        outer.set(1, 0, "M4"), outer.set(0, 1, "M3"), outer.set(2, 1, "M3"), outer.set(1, 2, "M1")
    for toe in toe_pieces(g, "sabaton_toe", (2, 1, 3), "M", base=2, texture="smooth", seed=S + 8, y=11.0, z=-2.1):
        toe.top.set(0, 0, "M4"), toe.top.set(1, 1, "M4"), toe.top.hline(0, 1, 2, "M1")
        toe.front.fill("M1")
