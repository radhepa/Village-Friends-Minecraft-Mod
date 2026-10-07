"""Bridegroom's Ribboned Hose: pale wedding hose gartered in accent ribbon, with ribbon rosettes on pale low shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import toe_pieces

META = {
    "name": "Bridegroom's Ribboned Hose",
    "gender": "male",
    "description": "Pale wedding hose gartered below the knee in accent ribbon, with ribbon rosettes on pale low shoes.",
    "tags": ["fancy", "slim"],
    "locked_to": "t94_bridegrooms_wedding_doublet",
}


def build(g):
    legs(g, "S", "velvet", 9411, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "velvet", 9412, base=3)
    footwear(g, "shoe", top=10, role="S", base=4, sole="L1")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, leg.strip.w - 1, 5, "A2")
        leg.strip.hline(0, leg.strip.w - 1, 6, "A1")
        outer = leg.right if side == "right" else leg.left
        outer.vline(1, 6, 8, "A3")                                       # garter ribbon ends
    for rose in toe_pieces(g, "shoe_rosette", (2, 2, 1), "A", base=3, texture="plain", y=9.7, z=-2.2):
        rose.front.set(0, 0, "A4"), rose.front.set(1, 1, "A1")
