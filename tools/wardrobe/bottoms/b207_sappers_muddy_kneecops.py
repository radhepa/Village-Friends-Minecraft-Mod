"""Sapper's Muddy Kneecops: trench-muddied trousers with fat domed leather kneecops and mud-caked boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from kit_m04 import mud, sides_of

META = {
    "name": "Sapper's Muddy Kneecops",
    "gender": "male",
    "description": "Wool trousers caked with tunnel mud from the knee down, fat domed leather kneecops strapped behind the "
                   "knee for crawling the saps, and boots wearing thick rings of clay.",
    "tags": ["rugged", "sturdy", "work"],
}

S = 34460


def build(g):
    legs(g, "P", "weave", S, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", S + 2)
    footwear(g, "boot", top=8, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        mud(leg.strip, S + 3, range(4, 8), "L1", "L0", .1, .4)
        leg.back.hline(0, 3, 4, "L1")                                      # strap behind the knee
        for face in pants.sides:
            mud(face, S + 4, range(8, 12), "L1", "L0", .25, .6)
    for i, side in enumerate(SIDES):
        cop = leg_blk(g, f"{side}_kneecop", side, 2.4, (4, 3, 2), "L", 2, "leather", S + 5 + i, dz=-2.3)
        cop.front.hline(1, 2, 0, "L4"), cop.front.set(1, 1, "L3"), cop.front.hline(0, 3, 2, "L1")
        cop.front.set(3, 1, "L0"), cop.front.set(0, 2, "L0")              # caked mud
        cop.top.fill("L3")
        outer = getattr(cop, sides_of(side)[0])
        outer.set(1, 1, "M3")
        clod = leg_blk(g, f"{side}_clay_ring", side, 10.4, (5, 1, 5), "L", 1, "plain", S + 7 + i, inflate=.1)
        for face in clod.sides:
            for x in range(face.w):
                face.set(x, 0, "L0" if (x + i) % 3 == 0 else "L1")
        clod.top.fill("L1")
