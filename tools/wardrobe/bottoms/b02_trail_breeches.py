"""Trail Breeches: canvas breeches, knee-high turn-down boots, belt with a hip pouch."""
from paint import cap, fabric, grid, k, solid, strip_fabric

META = {
    "name": "Trail Breeches",
    "description": "Canvas breeches with side buttons, tall cuffed boots, a belt and a hip pouch.",
    "tags": ["rugged", "sturdy", "casual"],
}


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "twill", 71 if side == "right" else 72, 2, 0, 6)
        fabric(leg.top, "S", "twill", 7, 2)
        outer = leg.right if side == "right" else leg.left
        for y in (1, 3, 5):
            outer.set(1 if side == "right" else 2, y, "M3")
        leg.front.set(0 if side == "right" else 3, 4, "S1"), leg.front.set(1 if side == "right" else 2, 5, "S1")
        # Tall boots: base layer under a chunkier overlay shaft.
        strip_fabric(leg, "L", "leather", 73, 2, 6, 11)
        strip_fabric(pants, "L", "leather", 74, 2, 6, 11)
        for face in pants.sides:
            face.hline(0, face.w - 1, 11, "K1")
            face.hline(0, face.w - 1, 10, "L1")
        pants.front.hline(0, 3, 10, "L3")
        pants.front.set(1 if side == "right" else 2, 8, "L3")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
        # Turned-down cuff ring at the top of the boot.
        bone = "RIGHT_LEG" if side == "right" else "LEFT_LEG"
        cuff = g.piece(f"{side}_boot_cuff", bone, (-2.5, 5.2, -2.5), (5, 2, 5))
        solid(cuff, "L", "leather", 75, 3)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "L4")
            face.hline(0, face.w - 1, 1, "L2")

    body = g.part("body")
    strip_fabric(body, "S", "twill", 76, 2, 9, 11)
    fabric(body.bottom, "S", "twill", 8, 1)
    belt = g.piece("waist_belt", "TORSO", (-4.6, 9.6, -2.6), (9, 2, 5), inflate=.04)
    solid(belt, "L", "leather", 77, 2)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    grid(belt.front, 3, 0, ["MMM", "MLM"], {"M": "M3", "L": "L0"})
    pouch = g.piece("waist_pouch", "TORSO", (-1, 0, -1.5), (2, 3, 3), pivot=(-4.7, 10.4, 0))
    solid(pouch, "L", "leather", 78, 2)
    for face in pouch.sides:
        face.hline(0, face.w - 1, 0, "L3")
    pouch.right.set(1, 1, "M3")
    cap(pouch, "L", top_delta=1)
