"""Fisher's Oilskin Waders: stiff oiled waders to the hip, strapped at the thigh, shining wet over heavy sea boots."""
from kit import SIDES, waistband
from kit_male import leg_rings
from paint import fabric, rnd

META = {
    "name": "Fisher's Oilskin Waders",
    "gender": "male",
    "description": "Stiff oiled waders reaching to the hip and strapped at the thigh, shining wet, over heavy black-soled sea boots.",
    "tags": ["sea", "work"],
    "locked_to": "t85_fishers_oilskin_smock",
}


def sheen(face, seed=0, rows=None):
    """Oilskin: smooth stiff cloth, a few bright glints of wet and one stiff crease."""
    for y in range(face.h) if rows is None else rows:
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, 8500 + seed)
            face.set(x, y, "P4" if r < .05 else "P3" if r < .12 else "P2")
        if y % 6 == 4:
            face.hline(0, face.w - 1, y, "P1")


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        sheen(leg.strip, rows=range(0, 10))
        sheen(leg.top)
        for face in pants.sides:
            sheen(face, 2, rows=range(6, 10))
            fabric(face, "K", "smooth", 8511, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K0")
        fabric(leg.strip, "K", "smooth", 8512, 2, 0, 10, leg.strip.w, 2)
        leg.bottom.fill("K0"), pants.bottom.fill("K0")
    body = waistband(g, "P", "smooth", 8513)
    for face in body.sides:
        sheen(face, 1, rows=range(9, 12))
    for ring in leg_rings(g, "wader_strap", 1.0, "L", (5, 1, 5), 2, "leather", 8514, inflate=.08):
        ring.front.set(2, 0, "M3")
