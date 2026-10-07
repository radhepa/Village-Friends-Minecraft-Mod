"""Reindeer-Hide Shoe Bands: pale hide trousers in fur shoes, bright woven shoe bands wound round and round each ankle."""
from kit import SIDES, legs, waistband
from kit_male import fur_face, stripes, toe_pieces

META = {
    "name": "Reindeer-Hide Shoe Bands",
    "gender": "male",
    "description": "Pale reindeer-hide trousers worn in fur shoes, bright woven shoe bands wound round and round each ankle to keep out the snow.",
    "tags": ["rugged", "casual"],
}


def build(g):
    legs(g, "L", "leather", 9011, base=3, rows=(0, 7), crease=False)
    waistband(g, "L", "leather", 9012, base=3)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        fur_face(leg.strip, "S", 9013, 3, rows=range(10, 12))
        for face in pants.sides:
            stripes(face, ["A2", "S4", "A3", "M3"], rows=range(7, 10))     # the wound bands
            fur_face(face, "S", 9014, 3, rows=range(10, 12))
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
    for toe in toe_pieces(g, "fur_toe", (2, 1, 2), "S", base=3, texture="plain", y=10.9, z=-2.1):
        fur_face(toe.front, "S", 9015, 3)
