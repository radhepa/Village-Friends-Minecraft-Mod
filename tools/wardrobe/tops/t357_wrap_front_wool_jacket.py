"""Wrap-Front Wool Jacket: a short, thick wool jacket wrapped high across the chest to the left side, toggled down its slanting edge, with a rolled collar."""
from kit import SIDES, body, collar, flaps
from kit_m10 import arm_ring
from kit_male import blk
from paint import dark_seams, fabric, strip_fabric

META = {
    "name": "Wrap-Front Wool Jacket",
    "gender": "male",
    "description": "A short, thick wool jacket whose front wraps high across the chest to close on the left side, three horn toggles down the slanting edge, a high rolled collar against the wind and deep turned cuffs.",
    "tags": ["casual", "rugged", "sea"],
    "covers_waist": True,
}

EDGE = [(2, 0), (3, 1), (3, 2), (4, 3), (4, 4), (5, 5), (5, 6), (6, 7), (6, 8), (7, 9), (7, 10), (7, 11)]


def build(g):
    jacket = body(g, "P", "twill", 40540, base=2)
    f = jacket.front
    # The slanting edge of the wrap, lit on the overlapping side and shadowed beneath it.
    for x, y in EDGE:
        f.set(x, y, "P0")
        if x - 1 >= 0:
            f.set(x - 1, y, "P3")
        if x + 1 <= 7:
            f.set(x + 1, y, "P1")
    over = g.part("jacket")
    for x, y in EDGE[:9]:
        for xx in range(0, x):
            over.front.set(xx, y, "P2")                                     # the doubled overlap stands proud
        over.front.set(x - 1 if x else 0, y, "P3")
    # Horn toggles along the edge.
    for i, (x, y) in enumerate(((-.5, 2.6), (1.5, 5.6), (2.5, 8.6))):
        t = blk(g, f"wrap_toggle_{i}", (x, y, -2.45), (2, 1, 1), "S", 3, "smooth", 40541 + i, edge=False)
        t.front.set(0, 0, "S4"), t.front.set(1, 0, "S2")
    dark_seams(jacket, faces=("right", "left"))
    jacket.back.vline(4, 1, 11, "P1")
    # High rolled collar.
    roll = collar(g, "rolled_collar", "P", "twill", base=2, height=2, y=-1.4, inflate=.12)
    for face in roll.sides:
        face.hline(0, face.w - 1, 0, "P4")
        face.hline(0, face.w - 1, 1, "P2")
    roll.front.set(3, 1, "P0")
    # Sleeves with deep turned cuffs.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "twill", 40544 + (side == "left"), 2, 0, 10)
        fabric(arm.top, "P", "twill", 40544, 3)
        arm.front.vline(0, 1, 6, "P1")
        cuff = arm_ring(g, f"{side}_turned_cuff", side, 6.4, (5, 3, 5), "P", 3, "twill", 40546 + (side == "left"), out=.1)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "P4")
            face.hline(0, face.w - 1, 2, "P1")
    for face in flaps(g, "jacket_hem", 2, "P", "twill", 40548, top=11.2):
        face.hline(0, 8, 1, "P1")
