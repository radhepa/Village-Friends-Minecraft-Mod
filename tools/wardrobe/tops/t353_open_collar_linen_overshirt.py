"""Open-Collar Linen Overshirt: a loose dyed-linen overshirt worn untucked, its broad collar spread open over a bare throat."""
from kit import SIDES, arm_bone, body, flaps, sleeves
from kit_m10 import arm_ring
from paint import dark_seams, solid

META = {
    "name": "Open-Collar Linen Overshirt",
    "gender": "male",
    "description": "A loose dyed-linen overshirt worn untucked, its broad flat collar spread wide over an open throat, roomy sleeves ending in unbuttoned cuffs and curved shirt tails.",
    "tags": ["casual", "simple", "relaxed"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 40380, base=3)
    f = b.front
    # The open neck: a deep V of bare throat.
    for y in range(0, 4):
        for x in range(2 + y, 6 - y) if y < 2 else (3, 4) if y == 2 else (4,):
            f.clear(x, y)
    for x, y in ((1, 0), (2, 1), (3, 2), (3, 3)):
        f.set(x, y, "P4")
    for x, y in ((6, 0), (5, 1), (4, 2)):
        f.set(x, y, "P1")
    f.vline(4, 4, 11, "P2"), f.vline(3, 4, 11, "P4")                  # button stand
    f.set(3, 5, "S4"), f.set(3, 8, "S4")
    b.back.hline(0, 7, 2, "P2")                                        # yoke seam
    b.back.set(3, 3, "P2"), b.back.set(4, 3, "P4")                     # a little pleat under it
    dark_seams(b, faces=("right", "left"))
    # Broad collar points lying open on the chest and shoulders.
    for side, x, rz in (("right", -2.6, 32), ("left", 2.6, -32)):
        tab = g.piece(f"{side}_open_collar", "TORSO", (-1.5, 0, -.5), (3, 2, 1), pivot=(x, -.2, -2.3), rotation=(0, 0, rz))
        solid(tab, "P", "weave", 40381, 4, edge=False)
        tab.front.hline(0, 2, 1, "P2")
        tab.front.set(0 if side == "right" else 2, 0, "P3")
    collar_back = g.piece("collar_back", "TORSO", (-4, 0, 0), (8, 2, 1), pivot=(0, -.6, 2.05), rotation=(-10, 0, 0))
    solid(collar_back, "P", "weave", 40382, 4, edge=False)
    collar_back.back.hline(0, 7, 1, "P2")
    # Roomy sleeves, cuffs left unbuttoned.
    sleeves(g, "P", "weave", 40383, base=3, rows=(0, 9))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        (arm.right if side == "right" else arm.left).vline(1, 1, 8, "P2")
        cuff = arm_ring(g, f"{side}_open_cuff", side, 6.6, (5, 2, 5), "P", 3, "weave", 40384 + (side == "left"), out=.1)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "P4")
        (cuff.front if side == "right" else cuff.front).set(1, 1, "S4")
    # Curved shirt tails hanging out, vented at the sides.
    for face in flaps(g, "shirt_tail", 3, "P", "weave", 40386, base=3, top=11.2):
        face.set(0, 2, "P1"), face.set(8, 2, "P1")
        face.hline(1, 7, 2, "P2")
