"""Almoner's Sandals and Hose: plain darned hose, knee garters, and open sandals whose thongs criss-cross up the ankle to a knot in front."""
from kit import SIDES, waistband
from kit_male import leg_blk
from kit_m05 import hose

META = {
    "name": "Almoner's Sandals and Hose",
    "gender": "male",
    "description": "Plain woollen hose with a darn at the knee and narrow garters, worn in open leather sandals whose thongs criss-cross up the ankle and tie in a knot in front.",
    "tags": ["holy", "simple", "relaxed"],
    "rejects": ["armor"],
}


def build(g):
    hose(g, "P", 1, "weave", 35260, end=11)
    waistband(g, "P", "weave", 35261, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, leg.strip.w - 1, 4, "L1")                       # narrow garter below the knee
        leg.front.set(1 if side == "right" else 2, 4, "M3")
        leg.front.rect(1, 2, 2, 1, "P2")                                   # a darn over the knee
        leg.front.set(1 if side == "right" else 2, 2, "P3")
        for face in pants.sides:                                           # thongs criss-crossing the ankle
            for x, y in ((0, 7), (3, 7), (1, 8), (2, 8), (0, 9), (3, 9)):
                face.set(x, y, "L3" if y == 8 else "L2")
            face.hline(0, face.w - 1, 11, "L1")                            # the sole
        pants.front.hline(0, 3, 10, "L2")                                   # toe strap
        pants.front.set(0, 10, "L1"), pants.front.set(3, 10, "L1")
        for face in (pants.right, pants.left):
            face.set(3, 10, "L2"), face.set(0, 10, "L2")                    # heel strap
        leg.strip.hline(0, leg.strip.w - 1, 11, "P0")
        leg.bottom.fill("L0"), pants.bottom.fill("L0")
        knot = leg_blk(g, f"{side}_thong_knot", side, 6.8, (1, 1, 1), "L", 3, "plain", 35262, dz=-2.3)
        knot.top.fill("L4")
        for i, dx in enumerate((-.6, .6)):
            end = leg_blk(g, f"{side}_thong_end_{i}", side, 7.8, (1, 1, 1), "L", 2, "plain", 35263 + i, dx=dx, dz=-2.3)
            end.bottom.fill("L1")
