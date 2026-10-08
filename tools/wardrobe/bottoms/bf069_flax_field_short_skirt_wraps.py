"""Flax-Field Short Skirt and Wraps: a knee-length skirt slit up both sides over a pale underskirt, linen
leg wraps bound to the knee with a pair of winding leather thongs, and turnshoes."""
from kit import SIDES
from kit_female import shoes, skirt, wraps
from paint import k

META = {
    "name": "Flax-Field Short Skirt and Wraps",
    "gender": "female",
    "description": "A knee-length skirt slit up both sides over a pale underskirt, linen leg wraps bound to the knee with a pair of winding thongs, and turnshoes.",
    "tags": ["work", "rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 51340, top=9.8, length=7, flare=6)
    s.hem("P1")
    for box, face in ((s.right, s.right.right), (s.left, s.left.left)):
        for y in range(2, face.h):
            face.set(1, y, "P1"), face.set(2, y, "S3"), face.set(3, y, "P3")   # the slit and the underskirt
        face.set(2, face.h - 1, "S2")
    # Linen wraps from the ankle to the knee, bound with thongs.
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for face in leg.sides:
            wraps(face, 4, 10, "S", 3, step=4)
        for y in range(4, 11):
            for phase in (0, 8):
                x = (y * 2 + phase + (side == "left") * 4) % 16
                leg.strip.set(x, y, "L1"), leg.strip.set((x + 1) % 16, y, "L2")   # two thongs winding up the shin
        leg.strip.hline(0, leg.strip.w - 1, 4, k("S", 4))
    shoes(g, "turnshoe", "L", 2, top=11)
