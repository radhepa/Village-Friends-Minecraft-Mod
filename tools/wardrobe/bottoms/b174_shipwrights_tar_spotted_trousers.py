"""Shipwright's Tar-Spotted Trousers: loose sailcloth trousers spattered with shiny black tar, a long rule pocket down
the right thigh with a boxwood folding rule standing in it, over plain shoes."""
from kit import SIDES, leg_bone
from kit_casual import trousers
from kit_m03 import low_shoes
from paint import grid, solid

META = {
    "name": "Shipwright's Tar-Spotted Trousers",
    "gender": "male",
    "description": "Loose sailcloth trousers spattered with shiny black tar, a long rule pocket down the right thigh "
                   "holding a boxwood folding rule, over plain shoes.",
    "tags": ["work", "sturdy", "sea"],
}

SPLAT = ["kk",
         "gk",
         ".k"]
DROP = ["k",
        "g",
        "k"]
# (side, face, x, y, stamp): the spatter falls where a man bends over hot tar.
SPOTS = [("right", "front", 1, 3, SPLAT), ("right", "front", 2, 7, DROP), ("left", "front", 1, 1, DROP),
         ("left", "front", 0, 6, SPLAT), ("left", "left", 1, 2, SPLAT), ("right", "back", 1, 6, SPLAT)]


def build(g):
    _, body = trousers(g, "P", 2, "twill", 33140, end=9, loops=True, overlay=True)
    grid(body.front, 2, 10, ["k"], {"k": "K1"})
    for side, face, x, y, stamp in SPOTS:
        grid(getattr(g.part(f"{side}_pants"), face), x, y, stamp, {"k": "K1", "g": "K3"})
    low_shoes(g, "L", 2, top=10, seed=33142)
    for side in SIDES:
        g.part(f"{side}_leg").strip.hline(0, 15, 9, "P1")
        g.part(f"{side}_pants").strip.hline(0, 15, 9, "P1")
    # The rule pocket: a long narrow pocket on the outer right thigh, the folding rule standing proud of it.
    pocket = g.piece("right_rule_pocket", leg_bone("right"), (0, 0, -1), (1, 5, 2), pivot=(-2.55, 2.5, -.2))
    solid(pocket, "P", "twill", 33143, 1)
    pocket.right.hline(0, 1, 0, "P3")
    pocket.right.vline(0, 1, 4, "P2")
    rule = g.piece("right_folding_rule", leg_bone("right"), (0, -2, 0), (1, 2, 1), pivot=(-2.45, 2.5, -.6))
    solid(rule, "L", "smooth", 33144, 4, edge=False)
    for face in rule.sides:
        face.set(0, 0, "K2")                                               # the inch marks
    rule.right.set(0, 1, "M3")                                             # brass hinge
