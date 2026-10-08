"""Poacher's Quiet Soft Boots: dark close trousers in soft-soled moccasin boots thong-bound round the calf, ankle flaps folded down."""
from kit import SIDES, leg_bone, legs, waistband
from kit_m07 import outer
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Poacher's Quiet Soft Boots",
    "gender": "male",
    "description": "Dark close trousers tucked into soft-soled moccasin boots that make no sound on a leaf, thong-bound round the calf, a puckered seam over each toe and folded ankle flaps.",
    "tags": ["rugged", "simple", "slim"],
}


def build(g):
    legs(g, "S", "weave", 37260, base=1, rows=(0, 5), crease=False)
    waistband(g, "S", "weave", 37261, base=1)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "L", "leather", 37262 + i, 2, 6, 11)
        leg.bottom.fill("L1")
        for face in pants.sides:                                         # the soft boot shaft
            fabric(face, "L", "leather", 37264 + i, 2, 0, 6, face.w, 6)
        for y in (7, 9):
            pants.strip.hline(0, pants.strip.w - 1, y, "L3")             # thongs bound round calf and ankle
        o = outer(pants, side)
        o.set(1, 7, "L4"), o.set(2, 8, "L3"), o.set(1, 9, "L4")          # the knotted ends
        pants.strip.hline(0, pants.strip.w - 1, 6, "L1")                 # the soft top, gathered
        pants.strip.hline(0, pants.strip.w - 1, 11, "L1")                # thin sole, no heel
        pants.bottom.fill("L0")
        pants.front.hline(0, 3, 10, "L3")
        pants.front.set(1, 11, "L3"), pants.front.set(2, 11, "L3")       # the puckered vamp seam
        pants.front.set(0, 11, "L4"), pants.front.set(3, 11, "L4")
        # Ankle flaps folded down over each side of the boot.
        x = -2.3 if side == "right" else 2.3
        flap = g.piece(f"{side}_ankle_flap", leg_bone(side), (-.5, 0, -1.5), (1, 2, 3),
                       pivot=(x, 8.6, 0))
        solid(flap, "L", "leather", 37266 + i, 3, edge=False)
        fo = outer(flap, side)
        fo.hline(0, 2, 0, "L4"), fo.hline(0, 2, 1, "L2")
        for face in leg.sides:
            face.hline(0, face.w - 1, 5, k("S", 0))
