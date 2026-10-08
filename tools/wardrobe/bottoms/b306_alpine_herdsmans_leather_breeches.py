"""Alpine Herdsman's Leather Breeches: buckskin knee breeches with an embroidered fall-front flap, horn-buttoned knee bands, turned-down knitted stockings and stout shoes."""
from kit import SIDES, footwear, waistband
from kit_male import leg_rings
from paint import fabric, strip_fabric

META = {
    "name": "Alpine Herdsman's Leather Breeches",
    "gender": "male",
    "description": "Buckskin knee breeches with an embroidered fall-front flap and horn-buttoned knee bands, thick knitted stockings turned down at the top, and stout shoes.",
    "tags": ["rugged", "sturdy", "work"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "L", "leather", 38421 + i, 2, 0, 5)
        fabric(leg.top, "L", "leather", 38421, 2)
        leg.strip.hline(0, leg.strip.w - 1, 5, "L1")                       # knee band
        outer = leg.right if side == "right" else leg.left
        outer.set(1, 5, "L4"), outer.set(2, 5, "L4")                       # horn buttons
        outer.vline(2, 0, 4, "L1")                                         # side seam
        leg.front.vline(1 if side == "right" else 2, 1, 4, "L3")            # buckskin worn pale at the thigh
        fabric(leg.strip, "S", "knit", 38423 + i, 2, 0, 6, leg.strip.w, 4)  # knitted stockings
    body = waistband(g, "L", "leather", 38425)
    f = body.front                                                         # the fall-front flap
    f.hline(1, 6, 9, "L0"), f.vline(1, 9, 11, "L0"), f.vline(6, 9, 11, "L0")
    f.set(2, 10, "A3"), f.set(3, 11, "A2"), f.set(4, 11, "A2"), f.set(5, 10, "A3"), f.set(3, 10, "A1"), f.set(4, 10, "A1")
    f.set(1, 9, "L4"), f.set(6, 9, "L4")
    footwear(g, "shoe", top=10, role="L", base=2)
    for ring in leg_rings(g, "stocking_turn", 5.8, "S", (5, 1, 5), 3, "knit", 38426, inflate=.06):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "S3" if x % 2 else "S2")                    # ribbed turn-down
