"""Verderer's Bracken Boots: knee breeches in tall soft boots tooled with bracken fronds, a sprig of fern tucked in each boot top."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m07 import outer
from paint import solid

META = {
    "name": "Verderer's Bracken Boots",
    "gender": "male",
    "description": "Wool knee breeches tucked into tall soft riding boots tooled up the outside with curling bracken fronds, a fresh sprig of fern tucked into each boot top.",
    "tags": ["rugged", "sturdy"],
}


def frond(face, x: int, y0: int, y1: int, stem: str, leaf: str):
    """A bracken frond: a stem up the middle, leaflets alternating out to each side, a curled tip."""
    for y in range(y0, y1 + 1):
        face.set(x, y, stem)
        if (y - y0) % 2 == 1:
            face.set(x - 1, y, leaf)
        elif y > y0:
            face.set(x + 1, y, leaf)
    face.set(x + 1, y0, stem)                                            # the fiddlehead curl


def build(g):
    legs(g, "P", "weave", 37180, rows=(0, 3), crease=False)
    waistband(g, "P", "weave", 37181)
    footwear(g, "boot", top=4, base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 4, "L3")                           # the soft rolled boot top
            face.hline(0, face.w - 1, 5, "L1")
        frond(outer(pants, side), 1, 6, 10, "L1", "L3")
        pants.front.vline(1 if side == "right" else 2, 6, 10, "L1")      # the boot's front seam
        leg.strip.hline(0, leg.strip.w - 1, 3, "P1")                     # the breeches' knee band
        # A sprig of bracken tucked into the boot top on the outer side.
        x = -1.9 if side == "right" else 1.9
        sprig = g.piece(f"{side}_bracken_sprig", leg_bone(side), (-.5, -3, -.5), (1, 3, 1), pivot=(x, 4.4, .6),
                        rotation=(0, 0, -14 if side == "right" else 14))
        solid(sprig, "P", "plain", 37182 + i, 3, edge=False)
        for face in sprig.sides:
            face.set(0, 0, "P4"), face.set(0, 1, "P2"), face.set(0, 2, "L2")
