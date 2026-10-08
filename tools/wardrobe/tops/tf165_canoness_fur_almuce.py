"""Canoness's Fur Almuce: a white pleated linen rochet with close sleeves and lace cuffs, under the
canoness's brown fur almuce: a shoulder cape with a little fur hood behind and two long lappets down the
front, their ends and the cape's back hem hung with dark-tipped marten tails."""
from kit import body, sleeves
from kit_female import hood_down, mantle, neck
from kit_f05 import dangle
from paint import k, solid

META = {
    "name": "Canoness's Fur Almuce",
    "gender": "female",
    "description": "A pleated white linen rochet under a brown fur almuce, its long front lappets and hem hung with little marten tails.",
    "tags": ["holy", "fancy", "scholarly"],
    "covers_waist": True,
}


def vair(face, seed=0):
    """Marten fur worked calm: rows of soft tufts, lit tips over shaded roots, each row offset."""
    for y in range(face.h):
        for x in range(face.w):
            gx = x + face.x0 + (2 if (y // 2) % 2 else 0)
            if y % 2 == 0:
                face.set(x, y, "L4" if gx % 8 == 0 else "L3")
            else:
                face.set(x, y, "L2" if gx % 4 == 2 else "L3")


def tail(box):
    """A little marten tail: brown fur darkening to a black tip."""
    for face in box.sides:
        face.hline(0, face.w - 1, 0, "L3")
        for y in range(1, face.h):
            face.hline(0, face.w - 1, y, "K1" if y == face.h - 1 else "L2" if y == face.h - 2 else "L3")
    box.top.fill("L3"), box.bottom.fill("K0")


def build(g):
    b = body(g, "S", "plain", 55161, base=4)
    neck(b.front, "round", "S", 4, edge="S3")
    for face in (b.front, b.back):
        for x in range(1, 8, 2):
            face.vline(x, 2, 11, "S3")                                # the rochet's fine pleats
    for arm in sleeves(g, "S", "plain", 55162, base=4, rows=(0, 11)):
        for x in range(1, 16, 4):
            arm.strip.vline(x, 1, 9, "S3")
        arm.strip.hline(0, 15, 10, "S3")
        for x in range(16):
            arm.strip.set(x, 11, "S2" if x % 2 else "S4")              # lace at the wrist
    # The cassock's dark collar shows above the rochet.
    j = g.part("jacket")
    j.front.hline(2, 5, 0, "P1"), j.back.hline(1, 6, 0, "P1")
    # The almuce: a fur shoulder cape.
    cape = mantle(g, "almuce", "L", "plain", 55163, 2, height=4, width=17, depth=6, y=-.7)
    for face in cape.faces:
        vair(face)
    for face in cape.sides:
        face.hline(0, face.w - 1, face.h - 1, "L1")
    # Two long lappets down the front, still on the breast.
    for side, x in (("right", -2.6), ("left", 2.6)):
        lap = g.piece(f"almuce_lappet_{side}", "TORSO", (-1.5, 0, 0), (3, 8, 1), pivot=(x, 1.2, -3.15))
        solid(lap, "L", "plain", 55164, 2)
        for face in lap.faces:
            vair(face)
        lap.front.hline(0, 2, 7, "L1")
        # Two tails at each lappet's end, riding the stride below the waist.
        for i, dx in enumerate((-1.0, 1.0)):
            t = dangle(g, f"tail_{side}_{i}", x + dx, .1, (1, 3, 1), "L", 2, "plain", top=9.2, seed=55165 + i)
            tail(t)
    # Three tails swing from the cape's back hem.
    for i, x in enumerate((-4.0, 0.0, 4.0)):
        t = g.piece(f"tail_back_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 3.3, 3.0), motion="sway")
        tail(t)
    # The fur hood lying behind the neck.
    hood = hood_down(g, "almuce_hood", "L", "plain", 55167, 2)
    for face in hood.faces:
        vair(face)
    hood.top.hline(0, 6, 0, k("L", 0)), hood.top.hline(1, 5, 1, k("L", 1))
