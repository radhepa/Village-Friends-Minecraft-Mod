"""Side-Laced Gaiters: wool trousers tucked into stout leather gaiters laced up the outer shin, strapped under low shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_m10 import leg_ring, outer

META = {
    "name": "Side-Laced Gaiters",
    "gender": "male",
    "description": "Plain wool trousers tucked into stout leather gaiters that run from knee to instep, laced up the outer shin with a thong and strapped under low shoes.",
    "tags": ["casual", "sturdy", "rugged"],
}


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "weave", 40440, rows=(0, 9), crease=False)):
        outer(leg, side).vline(2, 1, 5, "P1")
    waistband(g, "P", "weave", 40441)
    footwear(g, "shoe", top=10, base=2)
    for i, side in enumerate(SIDES):
        gaiter = leg_ring(g, f"{side}_gaiter", side, 5.0, (5, 5, 5), "L", 2, "leather", 40442 + i)
        for face in gaiter.sides:
            face.hline(0, face.w - 1, 0, "L3")
            face.hline(0, face.w - 1, 4, "L1")
        o = outer(gaiter, side)
        for y in range(1, 4):
            o.set(1, y, "K1"), o.set(3, y, "K1")                         # eyelets either side of the opening
            o.set(2, y, "L4" if y % 2 else "S3")                         # the thong crossing over
        o.set(2, 4, "L0")
        gaiter.front.vline(2, 1, 3, "L1")                                # moulded shin seam
        # A strap passing under the shoe.
        pants = g.part(f"{side}_pants")
        for face in (pants.right, pants.left):
            face.set(1, 10, "L1"), face.set(2, 10, "L1")
