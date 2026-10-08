"""Gate Warden's Hobnail Gaiters: stout trousers under stiff leather shin gaiters, over shoes studded with hobnails."""
from kit import SIDES, footwear, leg_ring, legs, waistband
from kit_m04 import sides_of

META = {
    "name": "Gate Warden's Hobnail Gaiters",
    "gender": "male",
    "description": "Stout wool trousers under stiff boiled-leather gaiters that stand off the shin, seamed up the front and "
                   "strapped at the back, over low shoes whose soles bristle with iron hobnails.",
    "tags": ["martial", "rugged", "sturdy"],
}

S = 34340


def build(g):
    legs(g, "P", "weave", S, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", S + 2)
    footwear(g, "shoe", top=10, base=2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.front.vline(1 if side == "right" else 2, 1, 5, "P1")
        for face in pants.sides:                                           # hobnails round the sole edge
            for x in range(face.w):
                face.set(x, 11, "M3" if x % 2 == 0 else "K1")
        for x in range(4):
            for y in range(4):
                pants.bottom.set(x, y, "M2" if (x + y) % 2 == 0 else "K0")
        getattr(pants, sides_of(side)[0]).set(2, 10, "M3")
    for i, ring in enumerate(leg_ring(g, "gaiter", 5.8, "L", base=2, size=(5, 4, 5), texture="leather", inflate=.12)):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 3, "L1")
        ring.front.vline(2, 0, 3, "L1"), ring.front.set(2, 0, "L3")         # front seam
        for y in (1, 2):
            ring.back.hline(0, 4, y, "L0" if y == 1 else "L2")              # back strap
        ring.back.set(2, 1, "M3")
        outer = getattr(ring, sides_of("right" if i == 0 else "left")[0])
        outer.set(2, 1, "L3"), outer.set(2, 2, "L1")
