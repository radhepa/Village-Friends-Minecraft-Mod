"""Straw Mummer's Leg Bundles: wool trousers bound at thigh and shin with sheaves of straw tied by ribbons, over turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Straw Mummer's Leg Bundles",
    "gender": "male",
    "description": "Wool trousers bound at the thigh and the shin with sheaves of straw tied on with ribbons, over plain turnshoes.",
    "tags": ["whimsical", "rugged"],
    "locked_to": "t92_straw_mummers_cape",
}


def straw(face):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, ("S2", "S3", "S4", "S3")[(x + face.x0 + y // 2) % 4])


def build(g):
    legs(g, "P", "weave", 9211, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 9212)
    footwear(g, "turnshoe", top=10, base=2)
    for prefix, y, size, key in (("thigh_straw", .4, (5, 4, 5), "A2"), ("shin_straw", 6.0, (5, 4, 5), "P1")):
        for ring in leg_rings(g, prefix, y, "S", size, 3, "plain", 9213, inflate=.16):
            for face in ring.faces:
                straw(face)
            for face in ring.sides:
                face.hline(0, face.w - 1, 1, key)                           # ribbon tie
            ring.bottom.fill("S1")
