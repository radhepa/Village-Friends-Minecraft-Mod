"""Braid-Frogged Trews: tight trews decorated with knotted accent braid on the thighs, and short boots with a braided cuff."""
from kit import SIDES, footwear, legs, waistband
from paint import grid

META = {
    "name": "Braid-Frogged Trews",
    "gender": "male",
    "description": "Tight trews decorated with knotted accent braid looping down each thigh, worn in short boots with a braided cuff.",
    "tags": ["fancy", "tailored"],
}

KNOT = ["a..a",
        ".aa.",
        "a..a"]


def build(g):
    legs(g, "P", "twill", 6811, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 6812)
    footwear(g, "boot", top=8, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        grid(leg.front, 0, 1, KNOT, {"a": "A3"})                           # the braid knot
        leg.front.vline(1 if side == "right" else 2, 4, 7, "A2")
        outer = leg.right if side == "right" else leg.left
        outer.vline(1, 0, 7, "A2")
        for face in pants.sides:
            for x in range(face.w):
                face.set(x, 8, "A3" if x % 2 else "A1")                    # braided cuff
