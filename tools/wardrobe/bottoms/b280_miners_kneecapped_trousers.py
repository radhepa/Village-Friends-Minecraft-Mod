"""Miner's Kneecapped Trousers: stout canvas trousers with domed leather kneecaps strapped behind the knee, tied at the ankle over iron-toed boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from kit_m07 import outer

META = {
    "name": "Miner's Kneecapped Trousers",
    "gender": "male",
    "description": "Stout canvas trousers worn dark at the seat, domed leather kneecaps strapped on behind the knee for crawling the low seams, tied at the ankle over iron-toed boots.",
    "tags": ["work", "sturdy", "rugged"],
}


def build(g):
    legs(g, "S", "twill", 37400, base=1, rows=(0, 9), crease=False)
    waistband(g, "S", "twill", 37401, base=1)
    footwear(g, "boot", top=10, base=1, toe="M3")
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.back.rect(0, 0, 4, 3, "S0")                                  # seat worn dark from sitting in the seams
        leg.strip.hline(0, leg.strip.w - 1, 5, "L1")                     # the kneecap strap round the leg
        leg.strip.hline(0, leg.strip.w - 1, 9, "L2")                     # ankle tie
        outer(leg, side).set(1, 9, "L4")
        pants.front.set(1, 10, "M2"), pants.front.set(2, 10, "M2")       # iron toe plate
        # The domed kneecap: a stiff leather plate with a raised boss.
        cap = leg_blk(g, f"{side}_kneecap", side, 3.2, (4, 4, 1), "L", 2, "leather", 37404 + i, dz=-2.45)
        cap.front.hline(0, 3, 0, "L3")
        for x, y in ((0, 0), (3, 0), (0, 3), (3, 3)):
            cap.front.set(x, y, "M3")                                    # rivets
        boss = leg_blk(g, f"{side}_kneecap_boss", side, 4.2, (2, 2, 1), "L", 3, "leather", 37406 + i, dz=-3.25)
        boss.front.set(0, 0, "L4")
