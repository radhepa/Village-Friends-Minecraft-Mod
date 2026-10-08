"""Horse Archer's Riding Trousers: full trousers bloused over soft high boots with stitched felt tops, leather
grip patches on the inner knees."""
from kit import SIDES, legs, waistband
from kit_female import leg_rings, shoes, trim, waist_belt
from paint import solid

META = {
    "name": "Horse Archer's Riding Trousers",
    "gender": "female",
    "description": "Full riding trousers bloused over soft high boots with stitched felt tops, and leather grip "
                   "patches on the inner knees.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 54141, rows=(0, 6), crease=False)
    body = waistband(g, "P", "twill", 54142)
    body.front.vline(3, 9, 11, "P1")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        inner = pants.left if side == "right" else pants.right
        for y in range(2, 6):
            inner.hline(0, inner.w - 1, y, "L2")                     # grip patch on the inside of the knee
        inner.hline(0, inner.w - 1, 2, "L3")
        for x in range(0, 16, 3):
            leg.strip.vline(x, 1, 4, "P1")                            # loose folds
    shoes(g, "boot", "L", 2, top=7)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.vline(face.w // 2, 8, 10, "L3")                     # soft boot seams
    for ring in leg_rings(g, "blousing", 4.6, 2, 5, inflate=.12):
        solid(ring, "P", "twill", 54143, 2, edge=False)
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if x % 2 else "P2")
                face.set(x, 1, "P1" if x % 2 else "P2")
    for ring in leg_rings(g, "felt_top", 6.6, 2, 5, inflate=.08):
        solid(ring, "S", "plain", 54144, 3, edge=False)
        for face in ring.sides:
            trim(face, 0, "zigzag", "A2")
            face.hline(0, face.w - 1, 1, "A1")
    waist_belt(g, "waist_sash", 9.4, role="A", height=1, buckle=None, texture="plain")
