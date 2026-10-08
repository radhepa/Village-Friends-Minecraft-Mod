"""Quarryman's Wedge-Belt Trousers: heavy twill trousers whitened with stone dust, a broad belt hung with iron splitting wedges and a stone hammer at the hip."""
from kit import SIDES, belt, footwear, legs, waistband
from kit_m07 import dust, outer
from paint import solid

META = {
    "name": "Quarryman's Wedge-Belt Trousers",
    "gender": "male",
    "description": "Heavy twill trousers whitened with stone dust from the knee down, leather patches on the knees, and a broad belt hung with iron splitting wedges and a short stone hammer.",
    "tags": ["work", "sturdy", "rugged"],
}


def build(g):
    for i, leg in enumerate(legs(g, "S", "twill", 37430, base=1, rows=(0, 9), crease=False)):
        for face in leg.sides:
            dust(face, "S3", 37431 + i, 5, 9, d0=.03, d1=.22)
        leg.front.rect(0, 3, 4, 3, "L2")                                  # leather knee patch
        leg.front.hline(0, 3, 3, "L3")
        leg.front.set(0, 5, "L1"), leg.front.set(3, 5, "L1")
    waistband(g, "S", "twill", 37433, base=1)
    footwear(g, "boot", top=10, base=1, toe="M2")
    for side in SIDES:
        outer(g.part(f"{side}_leg"), side).vline(1, 0, 9, "S0")           # the outer seam
    belt(g, "waist_belt", 9.2, height=2)
    # Iron splitting wedges hung through the belt, points down, along the right hip.
    for n, x in enumerate((-4.1, -2.9, -1.7)):
        wedge = g.piece(f"waist_wedge_{n}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 11.0, -2.75),
                        rotation=(0, 0, 6 - 6 * n), motion="sway")
        solid(wedge, "M", "plain", 37434 + n, 2, edge=False)
        for face in wedge.sides:
            face.set(0, 0, "M4")                                            # struck, burred head
            face.set(0, 2, "M1")                                            # the thin cutting edge
    # A short stone hammer hanging head-down from a loop on the left hip.
    handle = g.piece("waist_hammer_handle", "TORSO", (-.5, 0, -.5), (1, 4, 1), pivot=(4.7, 10.6, .2), motion="sway")
    solid(handle, "L", "plain", 37437, 3, edge=False)
    head = g.piece("waist_hammer_head", "TORSO", (-1.5, 4, -1), (3, 2, 2), pivot=(4.7, 10.6, .2), motion="sway")
    solid(head, "M", "plain", 37438, 1)
    for face in head.sides:
        face.set(0, 0, "M3"), face.set(face.w - 1, 0, "M3")
