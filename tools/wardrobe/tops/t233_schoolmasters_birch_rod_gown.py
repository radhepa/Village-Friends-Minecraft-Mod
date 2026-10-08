"""Schoolmaster's Birch-Rod Gown: a threadbare open gown patched at the elbows over a plain tunic, a birch rod thrust through the belt and a hornbook hanging at the hip."""
from kit import belt, body, sleeves
from paint import fabric, solid

META = {
    "name": "Schoolmaster's Birch-Rod Gown",
    "gender": "male",
    "description": "A village schoolmaster's threadbare open gown, patched at both elbows, over a plain tunic, a bundle of birch twigs thrust through his belt and a hornbook of letters swinging at his hip.",
    "tags": ["scholarly", "simple"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 35480, base=2)                             # the tunic beneath
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.set(3, 1, "S1"), b.front.set(4, 1, "S1")
    gown = g.part("jacket")
    for face in gown.sides:
        fabric(face, "P", "twill", 35481, 2)
    fabric(gown.top, "P", "twill", 35481, 3)
    for y in range(12):                                                  # open front: the tunic shows between the edges
        for x in (2, 3, 4, 5):
            gown.front.clear(x, y)
    gown.front.vline(1, 0, 11, "P3"), gown.front.vline(6, 0, 11, "P1")
    gown.back.vline(3, 1, 11, "P1"), gown.back.vline(4, 2, 11, "P3")
    gown.back.rect(5, 6, 2, 2, "P1"), gown.back.set(5, 6, "S2"), gown.back.set(6, 7, "S2")   # a stitched patch
    sleeves(g, "P", "twill", 35482, rows=(0, 10), cuff="P0")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.back.rect(0, 4, 4, 3, "L2")                                  # leather elbow patch
        arm.back.set(0, 4, "L3"), arm.back.set(3, 6, "L1")
        for x in range(0, 4, 2):
            arm.back.set(x, 4, "S2")                                     # tacking stitches
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")                    # tunic cuff peeping out
    belt(g, "belt", 9.6, height=1)
    # The birch rod: a bound bundle of pale twigs thrust up through the belt.
    rod = g.piece("birch_rod", "TORSO", (-.5, 0, -.5), (1, 7, 1), pivot=(2.4, 4.0, -2.75), rotation=(0, 0, -12))
    solid(rod, "S", "plain", 35483, 3, edge=False)
    for y in (1, 4):
        rod.strip.hline(0, rod.strip.w - 1, y, "K2")                     # birch bark marks
    rod.strip.hline(0, rod.strip.w - 1, 6, "L2")                         # the binding
    for i, rz in enumerate((-32, -12, 10)):
        twig = g.piece(f"birch_twig_{i}", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(2.4, 4.0, -2.75), rotation=(0, 0, rz))
        solid(twig, "L", "plain", 35484 + i, 3, edge=False)
        twig.top.fill("L1")
    # The hornbook: a little wooden paddle with its lettered sheet under horn.
    piv = (-2.6, 10.0, -3.0)
    board = g.piece("hornbook", "TORSO", (-1, 1, -.5), (2, 3, 1), pivot=piv, motion="flap_front")
    solid(board, "L", "plain", 35487, 2, edge=False)
    board.front.set(0, 0, "S4"), board.front.set(1, 0, "K2"), board.front.set(0, 1, "K2"), board.front.set(1, 1, "S4")
    board.front.set(0, 2, "S3"), board.front.set(1, 2, "K2")
    grip = g.piece("hornbook_handle", "TORSO", (-.5, 4, -.5), (1, 1, 1), pivot=piv, motion="flap_front")
    solid(grip, "L", "plain", 35488, 3, edge=False)
    cord = g.piece("hornbook_cord", "TORSO", (-.5, 0, -.5), (1, 1, 1), pivot=piv, motion="flap_front")
    solid(cord, "L", "plain", 35489, 1, edge=False)
    # Tunic hem in the middle, the gown's open fronts either side, its long back.
    tunic = g.piece("tunic_hem", "TORSO", (-2, 0, 0), (4, 4, 1), pivot=(0, 11.4, -2.75), motion="flap_front")
    solid(tunic, "S", "weave", 35490, 2)
    for name, x in (("gown_front_right", -3.0), ("gown_front_left", 3.0)):
        panel = g.piece(name, "TORSO", (-1.5, 0, 0), (3, 8, 1), pivot=(x, 10.6, -2.85), motion="flap_front")
        solid(panel, "P", "twill", 35491, 2)
        panel.front.vline(2 if x < 0 else 0, 0, 7, "P3" if x < 0 else "P1")
        panel.front.set(1, 7, "P0"), panel.front.set(0 if x < 0 else 2, 6, "P1")   # frayed hem
    back = g.piece("gown_back", "TORSO", (-4.5, 0, 0), (9, 8, 1), pivot=(0, 10.6, 1.85), motion="flap_back")
    solid(back, "P", "twill", 35492, 2)
    for x in (3, 6):
        back.back.vline(x, 0, 6, "P1")
    for x in range(0, 9, 3):
        back.back.set(x, 7, "P0")
