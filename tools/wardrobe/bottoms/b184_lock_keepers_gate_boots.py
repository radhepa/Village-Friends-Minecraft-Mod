"""Lock Keeper's Gate Boots: stout trousers in leather gaiters buttoned up the outside, over heavy hobnailed boots
with iron-plated toes for heaving the balance beams."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk, toe_pieces

META = {
    "name": "Lock Keeper's Gate Boots",
    "gender": "male",
    "description": "Stout trousers in leather gaiters buttoned up the outside, over heavy hobnailed boots with iron-plated "
                   "toes for heaving the balance beams.",
    "tags": ["work", "sturdy", "rugged"],
}


def build(g):
    legs(g, "P", "twill", 33540, rows=(0, 5), crease=True)
    waistband(g, "P", "twill", 33541)
    footwear(g, "boot", top=6, base=2, sole="K0")
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        outer = pants.right if side == "right" else pants.left
        for face in pants.sides:
            face.hline(0, face.w - 1, 6, "L3")                           # gaiter top
            face.hline(0, face.w - 1, 9, "L1")                           # gaiter's lower edge over the boot
            face.hline(0, face.w - 1, 10, "K2")
        outer.vline(2 if side == "right" else 1, 6, 9, "L1")              # the buttoned flap
        for y in (7, 9):
            outer.set(1 if side == "right" else 2, y, "M3")
        pants.front.hline(0, 3, 11, "K0")
        # A strap under the instep holds the gaiter down.
        strap = leg_blk(g, f"{side}_gaiter_strap", side, 9.6, (5, 1, 5), "L", 1, "leather", 33542 + i, inflate=.3)
        strap.front.hline(0, 4, 0, "L2")
    for toe in toe_pieces(g, "iron_toe", (4, 2, 1), "M", base=1, y=10.0, z=-2.1, inflate=.08):
        toe.front.hline(0, 3, 0, "M3")
        toe.front.set(0, 1, "M2"), toe.front.set(3, 1, "M2")
        toe.top.fill("M2")
