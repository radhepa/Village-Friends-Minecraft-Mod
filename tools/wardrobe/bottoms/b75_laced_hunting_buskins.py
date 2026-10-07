"""Laced Hunting Buskins: hose in soft knee-high buskins laced all the way up the front, their tops folded over."""
from kit import SIDES, footwear, legs, waistband
from kit_male import lacing, leg_rings

META = {
    "name": "Laced Hunting Buskins",
    "gender": "male",
    "description": "Close hose in soft knee-high hunting buskins laced all the way up the shin with thongs, their tops folded over.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    legs(g, "S", "twill", 7511, base=2, rows=(0, 4), crease=False)
    waistband(g, "S", "twill", 7512)
    footwear(g, "boot", top=4, base=3)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.vline(0, 5, 10, "L2"), pants.front.vline(3, 5, 10, "L2")
        lacing(pants.front, 1, 5, 10, "L1", "L0")
    for ring in leg_rings(g, "buskin_fold", 3.0, "L", (5, 2, 5), 3, "leather", 7513, inflate=.1):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 1, "L2")
        ring.front.set(2, 1, "L1")
