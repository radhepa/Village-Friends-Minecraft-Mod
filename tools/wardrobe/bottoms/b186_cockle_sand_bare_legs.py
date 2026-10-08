"""Cockle-Sand Bare Legs: short breeches hitched high and knotted at each thigh with a twist of cloth, bare legs and
feet crusted with wet sand from the cockle flats."""
from kit import SIDES, legs, waistband
from kit_male import blk, leg_rings
from paint import rnd

META = {
    "name": "Cockle-Sand Bare Legs",
    "gender": "male",
    "description": "Short breeches hitched high and knotted at each thigh with a twist of cloth, bare legs and feet "
                   "crusted with wet sand from the cockle flats.",
    "tags": ["relaxed", "simple", "sea"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "P", "weave", 33620, rows=(0, 2), crease=False)
    waistband(g, "P", "weave", 33621)
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg").strip
        # Sand: thick and wet about the feet, thinning up the shins to a few grains at the knee.
        for y in range(5, 12):
            for x in range(16):
                r = rnd(x, y, 33622 + i)
                density = (y - 4) / 7
                if y >= 10:
                    leg.set(x, y, "S3" if r < .55 else "S2")
                elif r < density * .45:
                    leg.set(x, y, "S4" if r < density * .2 else "S3")
        g.part(f"{side}_leg").bottom.fill("S2")
    # The hitched legs: a twist of cloth knotted round each thigh, its ends hanging at the outside.
    for ring in leg_rings(g, "thigh_knot", 2.2, "S", (5, 1, 5), 2, "weave", 33624, inflate=.16):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "S3" if (x + face.x0) % 2 else "S1")
    for i, side in enumerate(SIDES):
        x = -2.6 if side == "right" else 2.6
        bone = "RIGHT_LEG" if side == "right" else "LEFT_LEG"
        end = blk(g, f"{side}_thigh_knot_end", (x, 2.6, -1.0), (1, 2, 1), "S", 2, "weave", 33626 + i, bone=bone)
        end.strip.hline(0, end.strip.w - 1, 1, "S1")
    for ring in leg_rings(g, "breech_hem", 1.6, "P", (5, 1, 5), 2, "weave", 33628, inflate=.1):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P1")
