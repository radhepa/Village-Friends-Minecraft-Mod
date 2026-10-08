"""Grape-Stained Rolled Trousers: trousers rolled thick to mid-calf for the treading vat, wine-dark stains climbing to the knee, bare shins and wooden-soled sandals."""
from kit import SIDES, leg_bone, legs, waistband
from kit_m01 import mud, stains
from kit_male import leg_blk
from paint import solid

META = {
    "name": "Grape-Stained Rolled Trousers",
    "gender": "male",
    "description": "Linen trousers rolled thick to mid-calf for the treading vat, wine-dark stains climbing up to the knee, bare shins and wooden-soled sandals.",
    "tags": ["work", "relaxed", "simple"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "S", "weave", 31321, base=3, rows=(0, 6), crease=False)
    waistband(g, "S", "weave", 31322, base=3)
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        for face in leg.sides:
            face.vline(1, 0, 5, "S2")
        mud(leg.strip, 31323 + i, 5, role="K", base=3, rows=range(0, 7), splash=.12)          # wine-dark tide line from the vat
        # The thick double roll at mid-calf.
        for j, (y, base) in enumerate(((6.0, 3), (7.0, 2))):
            roll = leg_blk(g, f"{side}_trouser_roll_{j}", side, y, (5, 1, 5), "S", base, "weave", 31327 + 2 * i + j,
                           inflate=.08 - .04 * j)
            for face in roll.sides:
                face.hline(0, face.w - 1, 0, "S4" if j == 0 else "S2")
            stains(roll.front, "K2", 31331 + i + j, .12, cell=2)
        # Sandals: a wooden sole, a toe strap and an ankle thong; the foot itself bare.
        sole = leg_blk(g, f"{side}_sandal_sole", side, 11.1, (4, 1, 5), "L", 3, "plain", 31333 + i, dz=-.4,
                       inflate=.12)
        for face in sole.sides:
            face.hline(0, face.w - 1, 0, "L3")
        sole.bottom.fill("L1")
        for name, y, z, size in (("toe", 10.4, -2.15, (4, 1, 1)), ("ankle", 9.4, 0, (5, 1, 5))):
            strap = g.piece(f"{side}_sandal_{name}_strap", leg_bone(side), (-size[0] / 2, 0, -size[2] / 2), size,
                            pivot=(0, y, z), inflate=.04)
            solid(strap, "L", "leather", 31335 + i, 2, edge=False)
            strap.front.set(1, 0, "L3")
