"""Drawstring-Neck Linen Blouse: a full linen blouse gathered on a drawstring into a frilled neck, with frilled wrists, tucked in."""
from kit import SIDES, body
from kit_f10 import cord, frills
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Drawstring-Neck Linen Blouse",
    "gender": "female",
    "description": "A full linen blouse drawn up on a cord into a frilled neckline, its bead-tipped ends hanging free, with long gathered sleeves frilled at the wrist.",
    "tags": ["casual", "relaxed", "simple"],
    "tucked": True,
}


def build(g):
    b = body(g, "P", "weave", 60400, base=3)
    for face in (b.front, b.back):
        for x in range(face.w):
            if face.get(x, 1) and x % 2:
                face.set(x, 1, "P2")                                   # gathers under the drawstring
            if x % 3 == 1:
                face.vline(x, 3, 9, "P2")                              # soft folds falling from them
        face.hline(0, face.w - 1, 10, "P2")                            # the blouse pouching over the waist
    for face in (b.right, b.left):
        face.vline(1, 2, 9, "P2")
    # The frill round the drawn neckline, lying on the shoulders.
    frill = g.piece("neck_frill", "TORSO", (-4.5, .05, -2.5), (9, 1, 5), inflate=.06)
    solid(frill, "P", "plain", 60401, 3, edge=False)
    for face in frill.sides:
        for x in range(face.w):
            face.set(x, 0, k("P", 4 if x % 2 == 0 else 2))
    frill.top.fill("P2")
    for x, length, rot in ((-.5, 4, 5), (.5, 3, -5)):
        c = cord(g, f"drawstring_{'right' if x < 0 else 'left'}", (x, 1.1, -2.85), length, role="A", base=2,
                 end="L3", rotation=(0, 0, rot))
        c.bottom.fill("L2")
    # Long gathered sleeves, frilled where the cuff is drawn in.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 60402 + (side == "left"), 3, 0, 11)
        fabric(arm.top, "P", "weave", 60404, 4)
        for x in range(1, 16, 3):
            arm.strip.vline(x, 2, 8, "P2")
        arm.strip.hline(0, 15, 9, "P2")
    frills(g, "wrist_frill", 8.1, "P", 3)
