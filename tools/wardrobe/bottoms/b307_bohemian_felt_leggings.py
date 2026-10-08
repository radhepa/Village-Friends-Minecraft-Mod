"""Bohemian Felt Leggings: close felted leggings with cut-felt tulips on the thighs and a scalloped seam braid, in soft shoes strapped round the ankle."""
from kit import SIDES, footwear, legs, waistband
from paint import grid

META = {
    "name": "Bohemian Felt Leggings",
    "gender": "male",
    "description": "Close felted wool leggings with cut-felt tulips stitched on the thighs and a scalloped braid down each outer seam, worn in soft leather shoes strapped round the ankle.",
    "tags": ["casual", "slim"],
}

TULIP = ["a..a",
         "aaaa",
         ".aa.",
         ".bb.",
         "b..."]


def build(g):
    legs(g, "P", "plain", 38461, rows=(0, 9), crease=False)
    waistband(g, "P", "plain", 38462)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        tulip = TULIP if side == "right" else [r[::-1] for r in TULIP]
        grid(leg.front, 0, 1, tulip, {"a": "A3", "b": "S2"})
        grid(leg.back, 0, 2, tulip, {"a": "A2", "b": "S1"})
        outer = leg.right if side == "right" else leg.left
        for y in range(0, 9):
            outer.set(1 + y % 2, y, "A2")                                 # scalloped seam braid
            outer.set(2 - y % 2, y, "A1" if y % 2 else outer.get(2 - y % 2, y))
    footwear(g, "turnshoe", top=9, role="L", base=2)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        for x in range(pants.strip.w):                                     # the ankle straps
            if (x + i) % 4 in (0, 1):
                pants.strip.set(x, 9, "L1")
            if (x + i) % 4 in (2, 3):
                pants.strip.set(x, 10, "L1")
