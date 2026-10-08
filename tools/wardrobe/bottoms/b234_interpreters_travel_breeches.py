"""Interpreter's Travel Breeches: wool knee breeches with a leather-lined seat and inner thighs, button-closed knee bands, ribbed stockings and strapped ankle boots."""
from kit import SIDES, footwear, waistband
from kit_male import leg_rings, ribbing
from paint import strip_fabric

META = {
    "name": "Interpreter's Travel Breeches",
    "gender": "male",
    "description": "Hard-wearing wool knee breeches lined with leather at the seat and inner thighs for long days in the saddle, closed below the knee by buttoned bands, over ribbed stockings and strapped ankle boots.",
    "tags": ["rugged", "sturdy", "casual"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "P", "twill", 35540 + (side == "left"), 2, 0, 5)
        leg.top.fill("P2")
        inner = leg.left if side == "right" else leg.right
        inner.rect(0, 0, 4, 5, "L2")                                        # leather inner-thigh lining
        inner.hline(0, 3, 0, "L3"), inner.vline(0 if side == "right" else 3, 0, 4, "L1")
        leg.back.rect(0, 0, 4, 2, "L2"), leg.back.hline(0, 3, 2, "L1")      # leather seat
        outer = leg.right if side == "right" else leg.left
        outer.vline(2, 0, 4, "P1")                                          # outer seam
        ribbing(leg.strip, "S", 3, rows=range(6, 9))                        # ribbed stockings
    waistband(g, "P", "twill", 35542)
    footwear(g, "boot", top=9, role="L", base=2, sole="K1")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L1")                             # ankle strap
        (pants.right if side == "right" else pants.left).set(2, 10, "M3")
    for i, band in enumerate(leg_rings(g, "knee_band", 5.0, "P", (5, 1, 5), 2, "twill", 35543, inflate=.1)):
        outer = band.right if i == 0 else band.left
        outer.set(1, 0, "M3"), outer.set(3, 0, "M3")                        # the buttons
        band.front.set(2, 0, "P3")
