"""Sleeveless Pinafore over Blouse: a square-bibbed pinafore with frilled shoulder straps over a long-sleeved blouse, a spoon in its pocket."""
from kit_female import chemise
from paint import fabric, k, solid

META = {
    "name": "Sleeveless Pinafore over Blouse",
    "gender": "female",
    "description": "A square-bibbed pinafore on wide straps frilled over the shoulders, worn over a long-sleeved blouse, with a wooden spoon tucked in the bib pocket.",
    "tags": ["casual", "work", "apron"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 60520, neckline="round", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2"), arm.strip.hline(0, 15, 10, "S4")
        arm.front.vline(1, 1, 8, "S2")
    j = g.part("jacket")
    f = j.front
    fabric(f, "P", "weave", 60521, 2, 1, 3, 6, 9)                      # the square bib
    for x in (0, 1, 6, 7):
        f.vline(x, 0, 2, "P2")                                         # wide straps
    f.hline(1, 6, 3, "P3")                                             # the bib's top edge
    for x, y in ((0, 2), (7, 2)):
        f.set(x, y, "P1")
    for y in range(3, 12):
        f.set(0, y, "P1"), f.set(7, y, "P1")
    fabric(f, "P", "weave", 60522, 1, 0, 3, 1, 9)
    fabric(f, "P", "weave", 60522, 1, 7, 3, 1, 9)
    fabric(j.back, "P", "weave", 60523, 2, 0, 6, 8, 6)
    for x in (0, 1, 6, 7):
        j.back.vline(x, 0, 5, "P2")
    j.back.hline(0, 7, 6, "P3")
    for face in (j.right, j.left):
        fabric(face, "P", "weave", 60524, 2, 0, 6, 4, 6)
        face.hline(0, 3, 6, "P3")
    for x in (0, 1, 6, 7):
        j.top.vline(x, 0, 3, "P3")
    # The bib pocket, a wooden spoon tucked into it.
    pocket = g.piece("bib_pocket", "TORSO", (-1.5, 0, -.5), (3, 3, 1), pivot=(-1.0, 6.4, -2.45))
    solid(pocket, "P", "weave", 60525, 2, edge=False)
    pocket.front.hline(0, 2, 0, "P3"), pocket.front.hline(0, 2, 2, "P1")
    handle = g.piece("spoon_handle", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-1.4, 4.4, -2.3))
    solid(handle, "L", "smooth", 60526, 3, edge=False)
    bowl = g.piece("spoon_bowl", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(-1.4, 2.6, -2.35))
    solid(bowl, "L", "smooth", 60527, 3, edge=False)
    bowl.front.set(0, 0, "L4"), bowl.front.set(1, 1, "L2")
    # Frills along the straps where they cross the shoulders.
    for side, x in (("right", -4.9), ("left", 2.9)):
        frill = g.piece(f"{side}_strap_frill", "TORSO", (x, -.9, -2.5), (2, 1, 5), inflate=.08)
        solid(frill, "P", "plain", 60528, 3, edge=False)
        for face in frill.sides:
            for xx in range(face.w):
                face.set(xx, 0, k("P", 4 if xx % 2 == 0 else 2))
