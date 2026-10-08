"""Turned-Down Mud Boots: hemp trousers bloused into calf boots whose floppy tops are turned down to show the rough lining, the feet caked in wet ditch mud."""
from kit import SIDES, footwear, legs, waistband
from kit_m01 import mud
from kit_male import leg_blk, toe_pieces

META = {
    "name": "Turned-Down Mud Boots",
    "gender": "male",
    "description": "Hemp trousers bloused into calf boots whose floppy tops are turned down to show the rough flesh-side lining, the feet caked to the ankle in wet ditch mud.",
    "tags": ["work", "rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 31515, rows=(0, 5), crease=False)
    waistband(g, "P", "twill", 31516)
    footwear(g, "boot", top=5, base=3)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in leg.sides:
            face.vline(1, 0, 3, "P1"), face.set(2, 4, "P1")              # bloused over the boot
        for face in pants.sides:
            face.vline(1, 6, 8, "L2")                                    # a soft crease in the shaft
            mud(face, 31517 + i + face.x0, 9, role="L", base=1, splash=.06)
        mud(leg.strip, 31519 + i, 9, role="L", base=1, rows=range(8, 12), splash=.06)
        pants.bottom.fill("L0")
        # The turned-down top: the floppy fold shows the rough flesh side, a scalloped lower edge.
        fold = leg_blk(g, f"{side}_boot_fold", side, 4.3, (5, 2, 5), "L", 4, "leather", 31521 + i, inflate=.22)
        for face in fold.sides:
            face.hline(0, face.w - 1, 0, "L3")
            for x in range(face.w):
                face.set(x, 1, "L2" if x % 2 else "L3")
        fold.top.fill("L1")                                               # the dark mouth of the boot
        fold.bottom.fill("L2")
    for toe in toe_pieces(g, "mud_clump", (4, 1, 1), "L", base=1, texture="plain", seed=31523, y=10.9, z=-2.1,
                          inflate=.05):
        toe.front.set(1, 0, "L2"), toe.front.set(3, 0, "L0")
        toe.top.fill("L2")
