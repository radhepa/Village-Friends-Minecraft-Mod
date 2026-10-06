"""Desert Sirwal & Sandals: billowing light trousers with embroidered ankle cuffs, a fringed hip scarf and sandals."""
from kit import SIDES, leg_bone, legs, waistband
from kit_female import shoes, trim
from paint import solid

META = {
    "name": "Desert Sirwal & Sandals",
    "gender": "female",
    "description": "Billowing linen sirwal trousers with embroidered ankle cuffs, a fringed hip scarf and flat sandals.",
    "tags": ["relaxed", "casual"],
}


def build(g):
    legs(g, "S", "weave", 13611, base=4, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 13612, base=4)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        trim(leg.strip, 8, "zigzag", "A2", "M3")
        leg.strip.hline(0, 15, 7, "A1")
        for y in range(1, 6, 2):
            leg.front.set(1 if side == "right" else 2, y, "S3")
        puff = g.piece(f"{side}_billow", leg_bone(side), (-2.6, 3.6, -2.6), (5, 4, 5), inflate=.12)
        solid(puff, "S", "weave", 13613, 4)
        for face in puff.sides:
            for x in range(1, face.w, 2):
                face.vline(x, 1, 3, "S3")
            face.hline(0, face.w - 1, 3, "S3")
    shoes(g, "sandal", "L", 2)
    scarf = g.piece("waist_hip_scarf", "TORSO", (-4, 0, 0), (8, 3, 1), pivot=(0, 9.4, -3.05), motion="flap_front")
    solid(scarf, "A", "weave", 13614, 2)
    for x in range(8):
        scarf.front.set(x, 2, "S3" if x % 2 else "A1")
    scarf.front.hline(2, 5, 2, "A2"), scarf.front.set(3, 2, "A1"), scarf.front.set(4, 2, "A1")
    knot = g.piece("waist_scarf_knot", "TORSO", (-1, 0, -1), (2, 2, 2), pivot=(4.6, 9.4, -1.2))
    solid(knot, "A", "weave", 13615, 2)
