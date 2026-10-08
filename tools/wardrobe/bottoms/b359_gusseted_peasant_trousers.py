"""Gusseted Peasant Trousers: loose square-cut trousers with diamond gussets at hip and knee, rolled once at the ankle, over thonged turnshoes."""
from kit import SIDES, footwear, waistband
from kit_casual import rolled_hems
from kit_m10 import outer
from paint import fabric, strip_fabric

META = {
    "name": "Gusseted Peasant Trousers",
    "gender": "male",
    "description": "Loose trousers cut from plain squares, with contrast diamond gussets let in at the hips and the outer knees for bending in the field, rolled once at the ankle over thonged turnshoes.",
    "tags": ["casual", "simple", "relaxed"],
}

DIAMOND = [".ab.",
           "abba",
           ".ab."]


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "weave", 40640 + i, 2, 0, 9)
        fabric(leg.top, "P", "weave", 40640, 2)
        strip_fabric(pants, "P", "weave", 40642 + i, 2, 0, 7)           # roomy, standing off the leg
        o = outer(pants, side)
        # Knee gusset on the outer side, a hip gusset above it.
        for gy in (0, 4):
            for dy, row in enumerate(DIAMOND):
                for dx, ch in enumerate(row):
                    if ch != ".":
                        o.set(dx, gy + dy, "S1" if ch == "a" else "S2")
        for face in (pants.front, pants.back):
            face.vline(1 if side == "right" else 2, 1, 6, "P1")
        pants.strip.hline(0, pants.strip.w - 1, 7, "P1")
    body = waistband(g, "P", "weave", 40644)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "P1" if x % 2 else "P3")
    rolled_hems(g, "P", base=3, y=8.4, texture="weave")
    footwear(g, "turnshoe", top=10, base=2)
    for side in SIDES:
        g.part(f"{side}_pants").front.hline(1, 2, 10, "L4")                # the thong over the instep
