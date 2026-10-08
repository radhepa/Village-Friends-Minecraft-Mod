"""Mudlark's Rolled Rags: patched, outgrown trousers rolled unevenly, one leg to the knee and one to the shin, frayed
at the turn-ups, over bare feet black with river mud."""
from kit import SIDES, legs, waistband
from kit_male import leg_blk
from paint import grid

META = {
    "name": "Mudlark's Rolled Rags",
    "gender": "male",
    "description": "Patched, outgrown trousers rolled unevenly, one leg to the knee and one to the shin, frayed at the "
                   "turn-ups, over bare feet black with river mud.",
    "tags": ["simple", "relaxed"],
    "rejects": ["armor"],
}

PATCH = ["aaa",
         "a.a",
         "aaa"]
ROLL = {"right": (4, 4.0), "left": (7, 7.0)}     # last cloth row and roll height per leg: rolled unevenly


def build(g):
    for side in SIDES:
        last, _ = ROLL[side]
        legs(g, "P", "tweed", 33500 + (side == "left"), rows=(0, last), crease=False)
    waistband(g, "P", "tweed", 33502)
    # Clear the leg that was painted twice past its roll, then dirty the bare shins and feet.
    for side in SIDES:
        last, _ = ROLL[side]
        leg = g.part(f"{side}_leg")
        for y in range(last + 1, 12):
            leg.strip.hline(0, 15, y, None)
        for x in range(16):
            leg.strip.set(x, 11, "K1" if x % 3 else "K2")                  # mud-black soles of the feet
            leg.strip.set(x, 10, "K2" if (x + 1) % 3 else None)
            if x % 4 == 1:
                leg.strip.set(x, 9, "K2")
        leg.bottom.fill("K1")
    right, left = g.part("right_leg").front, g.part("left_leg").front
    right.rect(0, 1, 3, 3, "S2"), grid(right, 0, 1, PATCH, {"a": "S1"})    # patches
    left.rect(1, 3, 3, 3, "A2"), grid(left, 1, 3, PATCH, {"a": "A1"})
    g.part("left_leg").back.rect(1, 0, 2, 2, "L2")
    for i, side in enumerate(SIDES):
        _, y = ROLL[side]
        roll = leg_blk(g, f"{side}_rag_roll", side, y, (5, 1, 5), "P", 3, "tweed", 33503 + i, inflate=.12)
        for face in roll.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if (x + face.x0) % 2 else "P1")        # frayed threads at the turn-up
