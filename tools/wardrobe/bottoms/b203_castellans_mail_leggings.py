"""Castellan's Mail Leggings: full mail leggings with fat quilted knee rolls and pointed leather shoes buckled at the ankle."""
from kit import SIDES, leg_ring, waistband
from kit_male import mail, toe_pieces
from kit_m04 import sides_of
from paint import fabric

META = {
    "name": "Castellan's Mail Leggings",
    "gender": "male",
    "description": "Riveted mail leggings from hip to ankle, a fat quilted roll padding each knee, and pointed leather "
                   "shoes buckled across the ankle.",
    "tags": ["armor", "martial", "sturdy"],
    "requires": ["martial", "rugged"],
}

S = 34300


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        mail(leg.strip, rows=range(0, 10), ox=1 if side == "left" else 0)
        mail(leg.top)
        leg.strip.hline(0, leg.strip.w - 1, 9, "M1")
        fabric(leg.strip, "L", "smooth", S, 2, 0, 10, leg.strip.w, 2)
        leg.strip.hline(0, leg.strip.w - 1, 11, "K1")
        for face in pants.sides:
            fabric(face, "L", "smooth", S + 1, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 10, "L3"), face.hline(0, face.w - 1, 11, "K1")
        getattr(pants, sides_of(side)[0]).set(1, 10, "M3")                # ankle buckle
        pants.front.hline(0, 3, 10, "L1")                                  # the ankle strap
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
    waistband(g, "S", "quilt", S + 2)
    for ring in leg_ring(g, "knee_roll", 4.2, "S", base=2, size=(5, 2, 5), texture="quilt", inflate=.16):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 1, "S1")
            for x in range(0, face.w, 2):
                face.set(x, 1, "S2")
        ring.front.set(2, 0, "A2"), ring.front.set(2, 1, "A1")             # a bound seam
    for toe in toe_pieces(g, "pointed_toe", (2, 1, 2), "L", base=2, seed=S + 4, y=11.0, z=-2.1):
        toe.front.fill("L1")
