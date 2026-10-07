"""Padded Chausses & Knee Guards: chausses quilted in vertical channels, domed boiled-leather knee guards and laced shoes."""
from kit import SIDES, footwear, waistband
from kit_male import lacing, leg_blk

META = {
    "name": "Padded Chausses & Knee Guards",
    "gender": "male",
    "description": "Chausses padded in vertical quilted channels, domed boiled-leather knee guards strapped on, and laced leather shoes.",
    "tags": ["martial", "sturdy"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(10):
            for x in range(leg.strip.w):
                leg.strip.set(x, y, "P1" if x % 2 else "P2")
        for x in range(leg.top.w):
            for y in range(leg.top.h):
                leg.top.set(x, y, "P2")
        leg.strip.hline(0, leg.strip.w - 1, 0, "P3")
    waistband(g, "P", "quilt", 5911)
    footwear(g, "shoe", top=10, base=2)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        lacing(pants.front, 1, 10, 11, "L4", "L1")
        pants.strip.hline(0, pants.strip.w - 1, 5, "L1")                   # guard strap
        guard = leg_blk(g, f"{side}_knee_guard", side, 2.4, (4, 3, 1), "L", 2, "smooth", 5912 + i, dz=-2.45)
        guard.front.hline(1, 2, 0, "L4"), guard.front.set(1, 1, "L3"), guard.front.hline(0, 3, 2, "L1")
        guard.top.fill("L3")
