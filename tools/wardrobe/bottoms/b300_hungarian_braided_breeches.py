"""Hungarian Braided Breeches: tight breeches with a braided knot on each thigh and a double seam braid, in notched csizma boots with tassels."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m08 import tassel
from paint import grid

META = {
    "name": "Hungarian Braided Breeches",
    "gender": "male",
    "description": "Tight riding breeches with a looped braid knot high on each thigh and a double braid down the outer seam, in soft csizma boots notched at the front with a swinging tassel.",
    "tags": ["slim", "fancy", "sturdy"],
}

THIGH_KNOT = ["aaa.",
              "a.a.",
              ".aaa",
              "..a."]


def build(g):
    legs(g, "P", "twill", 38181, rows=(0, 6), crease=False)
    waistband(g, "P", "twill", 38182)
    footwear(g, "boot", top=6, role="L", base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        knot = THIGH_KNOT if side == "right" else [r[::-1] for r in THIGH_KNOT]
        grid(leg.front, 0, 0, knot, {"a": "A3"})
        outer = leg.right if side == "right" else leg.left
        outer.vline(1, 0, 6, "A2"), outer.vline(2, 0, 6, "A3")              # double braid down the seam
        for face in (leg.front, pants.front):                              # the heart notch of the csizma
            face.set(1, 6, "P2"), face.set(2, 6, "P2")
            face.set(1, 7, "L2"), face.set(2, 7, "L2")
        outer_p = pants.right if side == "right" else pants.left
        outer_p.vline(1, 7, 10, "L0")
        tassel(g, f"{side}_csizma_tassel", (0, 6.6, -2.4), "A", length=2, bone=leg_bone(side))
