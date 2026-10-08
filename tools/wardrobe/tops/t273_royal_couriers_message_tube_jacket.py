"""Royal Courier's Message-Tube Jacket: a fitted livery riding jacket with a badge, and a capped message tube slung across the back."""
from kit import belt, body, collar, flaps, neckline, sleeves
from kit_m07 import baldric
from paint import grid, solid

META = {
    "name": "Royal Courier's Message-Tube Jacket",
    "gender": "male",
    "description": "A king's messenger's fitted riding jacket, buttoned close with a crowned livery badge on the breast and a capped leather message tube slung across his back.",
    "tags": ["tailored", "casual"],
    "covers_waist": True,
}

BADGE = ["m.m",
         "mmm",
         "aaa",
         "aba",
         ".a."]


def build(g):
    b = body(g, "P", "twill", 37080)
    neckline(b.front, "round", "P")
    b.front.vline(4, 1, 11, "P1")
    for y in range(2, 11, 2):
        b.front.set(3, y, "M3")                                          # a close row of buttons
    grid(b.front, 0, 2, BADGE, {"m": "M3", "a": "A2", "b": "M4"})       # crowned livery badge
    for face in (b.right, b.left):
        face.vline(1, 2, 11, "P1")                                       # fitted side seams
    sleeves(g, "P", "twill", 37081, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 8, "A3"), arm.strip.hline(0, 15, 9, "A2"), arm.strip.hline(0, 15, 10, "A1")
        for x in range(1, 16, 4):
            arm.strip.set(x, 9, "M3")                                    # cuff buttons
    stand = collar(g, "standing_collar", "A", "weave", base=2, height=1, y=-.6)
    stand.front.set(4, 0, "M3")
    jacket = g.part("jacket")
    baldric(jacket.front, jacket.back, from_left=True, key="L2", edge="L1")
    # The message tube: stiff leather, capped in metal at both ends, riding the strap.
    pivot, rot = (0, 5.0, 3.3), (0, 0, 40)
    tube = g.piece("message_tube", "TORSO", (-1, -4.5, -1), (2, 9, 2), pivot=pivot, rotation=rot)
    solid(tube, "L", "leather", 37082, 3, edge=False)
    for face in tube.sides:
        face.vline(0, 0, 8, "L2")
        face.hline(0, 1, 2, "M2"), face.hline(0, 1, 6, "M2")             # strap rings
    for name, oy in (("tube_cap_top", -5.5), ("tube_cap_end", 4.5)):
        cap = g.piece(name, "TORSO", (-1.5, oy, -1.5), (3, 1, 3), pivot=pivot, rotation=rot)
        solid(cap, "M", "smooth", 37083, 3, edge=False)
        for face in cap.sides:
            face.set(1, 0, "M4")
    seal = g.piece("tube_seal", "TORSO", (-.5, 5.5, -.5), (1, 2, 1), pivot=pivot, rotation=rot)
    solid(seal, "A", "plain", 37084, 2, edge=False)
    seal.strip.hline(0, 3, 1, "A1")
    belt(g, "belt", 9.4, height=1)
    for face in flaps(g, "peplum", 3, "P", "twill", 37085, hem="A2", top=10.6):
        face.vline(4, 0, 2, "P1")
