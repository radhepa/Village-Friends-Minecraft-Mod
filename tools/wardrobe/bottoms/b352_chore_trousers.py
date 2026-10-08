"""Chore Trousers: undyed canvas trousers with doubled knee panels, a work rag hanging from the side pocket, and laced ankle boots."""
from kit import SIDES, leg_bone
from kit_casual import leather_belt, shoes, trousers
from kit_m10 import outer
from paint import fabric, k, solid

META = {
    "name": "Chore Trousers",
    "gender": "male",
    "description": "Hard-wearing undyed canvas trousers with a second layer stitched over each knee, a work rag hanging from the side pocket and laced ankle boots.",
    "tags": ["casual", "simple", "work", "sturdy"],
}


def build(g):
    legs, body = trousers(g, "S", 2, "twill", 40360, end=8)
    for i, (side, leg) in enumerate(zip(SIDES, legs)):
        # The doubled knee: a second layer of canvas on the overlay, stitched round its edge.
        pants = g.part(f"{side}_pants")
        fabric(pants.front, "S", "twill", 40361 + i, 1, 0, 3, 4, 4)
        pants.front.hline(0, 3, 3, "S3")
        for y in (4, 6):
            pants.front.set(0, y, "S0"), pants.front.set(3, y, "S0")
        outer(leg, side).vline(2, 0, 8, "S1")
        # Back patch pocket.
        leg.back.hline(0, 2, 1, "S3"), leg.back.vline(0, 2, 3, "S1"), leg.back.vline(2, 2, 3, "S1")
    shoes(g, "boot", top=10)
    for side in SIDES:
        g.part(f"{side}_pants").strip.hline(0, 15, 8, "S1")              # hem resting on the boot tops
    leather_belt(g)
    # A work rag pushed into the right side pocket, hanging loose down the thigh.
    rag = g.piece("right_pocket_rag", leg_bone("right"), (-.5, 0, -1), (1, 4, 2), pivot=(-2.75, 1.4, .2),
                  rotation=(0, 0, 5))
    solid(rag, "A", "weave", 40363, 1)
    for face in rag.sides:
        face.hline(0, face.w - 1, 0, k("A", 2))
        face.set(face.w - 1, 3, k("A", 0))
    rag.right.set(0, 2, "A2"), rag.right.set(1, 1, "A0")
    leg = g.part("right_leg")
    leg.right.hline(0, 3, 1, "S0")                                        # the side pocket's mouth
