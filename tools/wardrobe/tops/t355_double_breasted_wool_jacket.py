"""Double-Breasted Wool Jacket: a hip-length wool jacket lapped wide across the chest, two rows of brass buttons and a piped stand collar."""
from kit import SIDES, body, collar, flaps
from paint import dark_seams, fabric, strip_fabric

META = {
    "name": "Double-Breasted Wool Jacket",
    "gender": "male",
    "description": "A smart hip-length wool jacket lapped wide across the chest and closed with two rows of brass buttons, a stand collar piped in a bright cord, and buttoned cuffs.",
    "tags": ["casual", "tailored"],
    "covers_waist": True,
}


def build(g):
    shirt = body(g, "S", "weave", 40460, base=3)
    jacket = body(g, "P", "weave", 40461, layer="jacket")
    f, bk = jacket.front, jacket.back
    f.clear(3, 0), f.clear(4, 0)
    shirt.front.set(3, 0, "S4"), shirt.front.set(4, 0, "S2")
    # The wide lap: the left forepart crosses to the right, its edge running down from the collar.
    f.set(2, 0, "P3"), f.set(1, 1, "P3")
    f.vline(1, 2, 11, "P0"), f.vline(2, 1, 11, "P3")
    f.set(5, 0, "P1"), f.set(6, 1, "P1")                                 # the lapel folds at the neck
    for x in (3, 6):
        for y in (3, 5, 7):
            f.set(x, y, "M3")
            f.set(x, y + 1, "P1")                                         # each button's small shadow
    f.hline(4, 6, 9, "P1")                                                # pocket welt
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "A2")                               # piped hem
    bk.vline(3, 2, 11, "P1"), bk.vline(4, 2, 11, "P3")                   # centre-back seam
    dark_seams(jacket, faces=("right", "left"))
    # Stand collar piped along its top edge.
    stand = collar(g, "stand_collar", "P", "weave", base=2, height=2, y=-1.2)
    for face in stand.sides:
        face.hline(0, face.w - 1, 0, "A3")
    stand.front.vline(4, 1, 1, "P0")
    # Sleeves with a two-button cuff.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 40462 + (side == "left"), 2, 0, 10)
        fabric(arm.top, "P", "weave", 40462, 3)
        arm.strip.hline(0, arm.strip.w - 1, 8, "P3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
        o = arm.right if side == "right" else arm.left
        o.set(1, 9, "M3"), o.set(2, 9, "M3")
        arm.front.vline(0, 1, 7, "P1")
    for face in flaps(g, "jacket_skirt", 3, "P", "weave", 40464, top=11.2):
        face.hline(0, 8, 2, "A2")
        face.hline(0, 8, 1, "P1")
