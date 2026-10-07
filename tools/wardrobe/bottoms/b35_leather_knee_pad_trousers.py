"""Leather Knee-Pad Trousers: work trousers with stitched leather knee pads buckled round the leg, and low boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk

META = {
    "name": "Leather Knee-Pad Trousers",
    "gender": "male",
    "description": "Woollen work trousers with stitched leather knee pads strapped and buckled round each leg, over low boots.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 3511, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 3512)
    footwear(g, "boot", top=9, base=1)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        for y in (3, 6):
            pants.strip.hline(0, pants.strip.w - 1, y, "L1")          # straps
        outer = pants.right if side == "right" else pants.left
        outer.set(2, 3, "M3"), outer.set(2, 6, "M3")
        pad = leg_blk(g, f"{side}_knee_pad", side, 2.8, (4, 4, 1), "L", 2, "leather", 3513 + i, dz=-2.45)
        f = pad.front
        f.hline(0, 3, 0, "L3"), f.hline(0, 3, 3, "L1")
        f.vline(0, 1, 2, "L3"), f.vline(3, 1, 2, "L1")
        f.set(1, 1, "L3"), f.set(2, 2, "L3")                          # cross-stitched centre
