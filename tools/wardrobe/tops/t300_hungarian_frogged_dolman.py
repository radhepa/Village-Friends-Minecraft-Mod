"""Hungarian Frogged Dolman: a short fitted dolman barred across the chest with braid frogging, and a fur-collared mente slung over the left shoulder."""
from kit import SIDES, body, collar, sleeves
from kit_male import fur_face
from paint import grid, solid

META = {
    "name": "Hungarian Frogged Dolman",
    "gender": "male",
    "description": "A short fitted dolman barred across the chest with rows of looped braid frogging and knotted cuffs, a fur-collared mente slung over the left shoulder.",
    "tags": ["fancy", "martial", "tailored"],
}

CUFF_KNOT = [".a..",
             "a.a.",
             ".a..",
             ".a.."]


def frog_bar(face, y, buttons=True):
    face.hline(1, 6, y, "A3")
    face.set(0, y, "A2"), face.set(7, y, "A2")                            # the loops at each end
    face.hline(1, 6, y + 1, "X1")
    if buttons:
        face.set(3, y, "M4"), face.set(4, y, "M3")


def build(g):
    b = body(g, "P", "velvet", 38161)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.vline(3, 1, 11, "P1")
    b.strip.hline(0, b.strip.w - 1, 11, "A2")                             # braided hem
    jacket = g.part("jacket")
    for y in (2, 4, 6, 8):
        frog_bar(jacket.front, y)
    stand = collar(g, "stand_collar", "A", "plain", base=2, height=1, y=-.5)
    for face in stand.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "A3")
    sleeves(g, "P", "velvet", 38162, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "A2"), arm.strip.hline(0, arm.strip.w - 1, 10, "A1")
        outer = arm.right if side == "right" else arm.left
        grid(outer, 0, 5, CUFF_KNOT, {"a": "A3"})                            # the braid knot above the cuff
        grid(arm.front, 0, 5, CUFF_KNOT, {"a": "A3"})
    # The mente: a second, fur-collared jacket slung off the left shoulder and hanging down the back.
    mente = g.piece("slung_mente", "TORSO", (-2.5, 0, 0), (5, 11, 1), pivot=(1.3, .2, 2.3), rotation=(5, 0, 0))
    solid(mente, "S", "velvet", 38163, 2)
    for y in (2, 4, 6, 8):
        mente.back.hline(1, 4, y, "A3"), mente.back.set(2, y, "M3"), mente.back.hline(1, 4, y + 1, "S1")
    mente.back.vline(3, 1, 9, "S1")
    for face in (mente.back, mente.left):                                   # fur down the outer edge and round the hem
        fur_face(face, "L", 38164, 3, rows=range(9, 11))
    for y in range(11):
        mente.back.set(0, y, "L4" if y % 3 == 0 else "L3")
        mente.left.set(0, y, "L3")
    fur = g.piece("mente_fur", "TORSO", (-2, 0, -2.5), (4, 2, 5), pivot=(2.0, -.9, .2))
    for face in fur.faces:
        fur_face(face, "L", 38165, 3)
    cord = g.piece("mente_cord", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(2.6, .9, -2.4))
    solid(cord, "M", "plain", 38166, 3, edge=False)
    cord.front.set(0, 2, "M4")
