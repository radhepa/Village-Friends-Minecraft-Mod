"""Miner's Leather Knee Breeches: close leather breeches buttoned up the outside of each knee, worn pale at
the knees, over white stockings and laced ankle boots."""
from kit import SIDES, waistband
from kit_female import shoes
from paint import fabric, strip_fabric

META = {
    "name": "Miner's Leather Knee Breeches",
    "gender": "female",
    "description": "Close leather breeches buttoned up the outside of each knee and worn pale where she kneels, "
                   "over white wool stockings and laced ankle boots.",
    "tags": ["work", "sturdy", "rugged"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "L", "leather", 57821 + (side == "left"), 2, 0, 6)
        fabric(leg.top, "L", "leather", 57821, 2)
        for face in leg.sides:
            face.hline(0, face.w - 1, 6, "L1")
        fabric(leg.front, "L", "leather", 57823, 3, 0, 3, 4, 3)      # pale, rubbed knees
        leg.front.hline(0, 3, 3, "L2")
        outer = leg.right if side == "right" else leg.left
        x = 0 if side == "right" else 3
        for y in range(2, 7):
            outer.set(x, y, "L1")
        for y in (3, 5):
            outer.set(x, y, "M3")                                    # knee buttons
        for y in range(7, 10):
            leg.strip.hline(0, leg.strip.w - 1, y, "S4" if y % 2 else "S3")
    body = waistband(g, "L", "leather", 57824)
    body.front.vline(4, 9, 11, "L1"), body.front.set(3, 10, "M3")
    for face in (body.right, body.left):
        face.set(1, 10, "L1")
    shoes(g, "ankle", "L", 1, top=9)
