"""Goose Girl's Pinafore Bodice: a frill-shouldered pinafore over a long-sleeved chemise, a goose feather in
the strap and a willow switch in her hand for herding the flock."""
from kit_female import arm_rings, chemise
from kit_f01 import handle
from paint import fabric, k, solid

META = {
    "name": "Goose Girl's Pinafore Bodice",
    "gender": "female",
    "description": "A pinafore with ruffled shoulder frills and a bow at the back over a full chemise, a goose feather in the strap and a willow switch in hand.",
    "tags": ["casual", "simple", "whimsical"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51000, neckline="round", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2"), arm.strip.hline(0, 15, 10, "S4")
        for x in range(0, 16, 2):
            arm.strip.set(x, 11, "S2")                                # a little frill at the wrist
    j = g.part("jacket")
    # The pinafore: a full bib in front, two straps over the shoulders and a skirted back below the waist.
    fabric(j.front, "P", "weave", 51001, 2, 0, 2, 8, 10)
    for x in (1, 2, 5, 6):
        j.front.vline(x, 0, 1, "P2")
        j.top.vline(x, 0, 3, "P3")
    j.front.hline(0, 7, 2, "P3")
    for x in range(1, 7, 2):
        j.front.set(x, 3, "A2")                                       # stitched dots along the bib edge
    j.front.set(1, 2, "M3"), j.front.set(6, 2, "M3")                 # strap buttons
    j.front.vline(0, 2, 11, "P1"), j.front.vline(7, 2, 11, "P1")
    for x in (2, 5):
        j.front.vline(x, 8, 11, "P1")                                 # soft folds below the waist
    for x in (1, 2, 5, 6):
        j.back.vline(x, 0, 6, "P2")
    fabric(j.back, "P", "weave", 51002, 2, 0, 7, 8, 5)
    for face in (j.right, j.left):
        fabric(face, "P", "weave", 51003, 2, 0, 7, 4, 5)
    for face in j.sides:
        face.hline(0, face.w - 1, 7, "A2")                            # the waist tie
    # Ruffled frills over the shoulders, riding on the arms.
    for box in arm_rings(g, "pinafore_frill", -2.3, 2, 5, inflate=.06):
        solid(box, "P", "weave", 51004, 2, edge=False)
        fabric(box.top, "P", "weave", 51004, 3)
        for face in box.sides:
            for x in range(face.w):
                face.vline(x, 0, 1, k("P", 3 if x % 2 == 0 else 1))   # pleated ruffle
            face.hline(0, face.w - 1, 0, "P3")
        box.bottom.fill("P1")
    # The bow at the back and its two short tails.
    bow = g.piece("pinafore_bow", "TORSO", (-1.5, -.5, 0), (3, 1, 1), pivot=(0, 7.2, 2.3), inflate=.08)
    solid(bow, "A", "plain", 51005, 2, edge=False)
    bow.back.set(1, 0, "A1")
    for name, x in (("bow_tail_right", -.7), ("bow_tail_left", .7)):
        tail = g.piece(name, "TORSO", (-.5, 0, 0), (1, 3, 1), pivot=(x, 7.6, 2.35), rotation=(6, 0, 0), motion="sway")
        solid(tail, "A", "plain", 51006, 2)
    # A white goose feather tucked into the left strap.
    feather = g.piece("goose_feather", "TORSO", (-.5, -3, -.5), (1, 3, 1), pivot=(1.6, 2.4, -2.55), rotation=(0, 0, 18))
    solid(feather, "S", "plain", 51007, 4, edge=False)
    feather.front.set(0, 2, "S2"), feather.right.set(0, 0, "S3")
    # The willow switch held in her right hand, pointing down and ahead.
    handle(g, "willow_switch", "RIGHT_ARM", (-1, 8.8, -.6), 14, rotation=(-24, 0, 22), origin=(-.5, -1, -.5), base=2,
           seed=51008)
    twig = g.piece("switch_twig", "RIGHT_ARM", (-.5, 0, -.5), (1, 3, 1), pivot=(-3.7, 15.5, -3.8), rotation=(-30, 0, 55))
    solid(twig, "L", "smooth", 51009, 3, edge=False)
