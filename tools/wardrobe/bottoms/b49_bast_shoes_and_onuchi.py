"""Bast Shoes & Onuchi: pale linen foot wraps bound with crossing cords up to the knee, in plaited bast-bark shoes."""
from kit import SIDES, legs, waistband
from kit_male import toe_pieces
from paint import strip_fabric

META = {
    "name": "Bast Shoes & Onuchi",
    "gender": "male",
    "description": "Pale linen foot wraps bound to the knee with crossing cords, worn in shoes plaited from strips of bast bark.",
    "tags": ["simple", "rugged"],
}


def build(g):
    legs(g, "P", "weave", 4911, rows=(0, 3), crease=False)
    waistband(g, "P", "weave", 4912)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 4913, 3, 4, 9)
        for x in range(leg.strip.w):
            leg.strip.set(x, 3, "P3" if x % 2 else "P1")                   # trousers gathered into the wraps
        for y in range(4, 10):
            for x in range(pants.strip.w):
                if (x + y) % 6 == 0 or (x - y) % 6 == 0:
                    pants.strip.set(x, y, "L1")                            # cords crossing round the leg
        # Plaited bast shoes.
        strip_fabric(leg, "L", "plain", 4914, 3, 10, 11)
        for face in pants.sides:
            for x in range(face.w):
                face.set(x, 10, "L4" if (x + face.x0) % 3 == 0 else "L3")
                face.set(x, 11, "L2" if (x + face.x0) % 3 == 1 else "L1")
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
    for toe in toe_pieces(g, "bast_toe", (4, 1, 1), "L", base=3, texture="plain", y=10.9, z=-2.1):
        toe.front.set(1, 0, "L4"), toe.front.set(2, 0, "L2")
