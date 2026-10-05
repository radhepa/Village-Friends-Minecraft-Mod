"""Side-Laced Leather Trousers: supple leather trousers laced up the outer seam, with tall boots."""
from kit import SIDES, footwear, legs, waistband

META = {
    "name": "Side-Laced Leather Trousers",
    "description": "Supple leather trousers laced up the outer seam with pale cord, over tall boots.",
    "tags": ["rugged", "sturdy", "casual"],
}


def build(g):
    for leg in legs(g, "L", "leather", 1701, base=3, rows=(0, 7), crease=False):
        leg.front.set(1, 4, "L2"), leg.front.set(2, 5, "L2")
    waistband(g, "L", "leather", 1702, base=3)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        outer = leg.right if side == "right" else leg.left
        for y in range(1, 8):
            outer.set(1, y, "S3" if y % 2 else "L1")
            outer.set(2, y, "L1" if y % 2 else "S3")
    footwear(g, "boot", top=7, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 7, "L2")
