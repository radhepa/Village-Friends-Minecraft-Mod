"""Novgorod Boot-Tucked Trousers: full trousers tucked into tall boots and bloused over the tops, with stacked heels and sewn toe caps."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk, leg_rings, toe_pieces

META = {
    "name": "Novgorod Boot-Tucked Trousers",
    "gender": "male",
    "description": "Full trousers stuffed into tall boots and bloused in heavy folds over the boot tops, the boots with stacked leather heels and sewn toe caps.",
    "tags": ["sturdy", "casual", "rugged"],
}


def build(g):
    legs(g, "P", "weave", 38501, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 38502)
    footwear(g, "boot", top=4, role="L", base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        pants.front.hline(0, 3, 8, "L1")                                    # the sewn toe cap
        pants.front.set(1, 9, "L3"), pants.front.set(2, 9, "L3")
        for face in pants.sides:
            face.set(0, 6, "L1"), face.set(face.w - 1, 7, "L1")             # creases at the ankle
        heel = leg_blk(g, f"{side}_stacked_heel", side, 10.0, (3, 2, 1), "L", 1, "leather", 38503 + i, dz=2.15)
        for face in heel.sides:
            face.hline(0, face.w - 1, 0, "L2"), face.hline(0, face.w - 1, 1, "K1")
    for ring in leg_rings(g, "trouser_blouse", 2.4, "P", (5, 3, 5), 2, "weave", 38505, inflate=.2):
        for face in ring.sides:
            for x in range(face.w):
                if x % 2 == 0:
                    face.vline(x, 0, 1, "P1")                             # folds sagging over the boot
            face.hline(0, face.w - 1, 2, "P0")
            face.hline(0, face.w - 1, 0, "P3")
        ring.bottom.fill("P0")
    for toe in toe_pieces(g, "boot_toe", (3, 1, 1), "L", base=2, y=11.0, z=-2.0, seed=38507):
        toe.top.fill("L3")
