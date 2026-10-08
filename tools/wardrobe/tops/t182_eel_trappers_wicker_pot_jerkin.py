"""Eel Trapper's Wicker-Pot Jerkin: a short toggled leather jerkin over a linen shirt, marsh mud on its hem, and a
long tapering wicker eel trap carried on the back on rope straps."""
from kit import body, flaps, sleeves
from kit_male import blk, toggles
from paint import fabric, k

META = {
    "name": "Eel Trapper's Wicker-Pot Jerkin",
    "gender": "male",
    "description": "A short toggled leather jerkin over a linen shirt, fen mud dried on its hem, and a long tapering "
                   "wicker eel trap carried on the back on rope straps.",
    "tags": ["rugged", "work", "sea"],
}

TRAP = (0.3, .4, 3.0)        # the trap's mouth rests between the shoulder blades; all three sections share it


def wicker(face, base=3):
    """Woven willow: stakes running the length, weavers crossing them in alternating rows."""
    for y in range(face.h):
        for x in range(face.w):
            over = (x + y) % 2 == 0
            face.set(x, y, k("L", base if over else base - 1))
        if y % 3 == 2:
            face.hline(0, face.w - 1, y, k("L", base - 2))               # a binding round


def build(g):
    b = body(g, "S", "weave", 33440, base=3)
    sleeves(g, "S", "weave", 33441, base=3, rows=(0, 10), cuff="S1")
    # The jerkin: leather over the shirt, open at the neck, toggled down the front.
    for face in b.sides:
        fabric(face, "L", "leather", 33442, 2, 0, 0, face.w, 12)
    f = b.front
    for x, y in ((3, 0), (4, 0), (3, 1), (4, 1)):
        f.set(x, y, "S3")
    f.vline(3, 2, 11, "L1"), f.vline(4, 2, 11, "L3")
    toggles(f, 3, (3, 6, 9), "L4", "L0")
    for face in b.sides:
        for x in range(face.w):
            face.set(x, 11, "K2" if (x + face.x0) % 3 else "L1")       # fen mud on the hem
    fabric(b.top, "L", "leather", 33443, 3)
    # Rope straps over both shoulders to the trap.
    for x in (1, 6):
        f.vline(x, 0, 6, "S2"), f.set(x, 6, "S1")
        b.back.vline(x, 0, 2, "S2")
        b.top.vline(x, 0, 3, "S2")
    # The eel trap: a wide mouth with its funnel, tapering to a stoppered tail at the small of the back.
    mouth = blk(g, "eel_trap_mouth", TRAP, (5, 4, 3), "L", 3, "plain", 33444, origin=(-2.5, 0, -.5),
                rotation=(0, 0, 8))
    for face in mouth.sides:
        wicker(face)
    mouth.top.fill("L1")
    for x in range(1, 4):
        mouth.top.set(x, 1, "K1")                                        # the funnel's dark throat
    mouth.top.hline(0, 4, 0, "L4")
    mid = blk(g, "eel_trap_body", TRAP, (4, 4, 2), "L", 3, "plain", 33445, origin=(-2.0, 4.0, 0), rotation=(0, 0, 8))
    for face in mid.sides:
        wicker(face)
    tail = blk(g, "eel_trap_tail", TRAP, (2, 3, 2), "L", 3, "plain", 33446, origin=(-1.0, 8.0, 0), rotation=(0, 0, 8))
    for face in tail.sides:
        wicker(face)
    stopper = blk(g, "eel_trap_stopper", TRAP, (1, 1, 1), "S", 2, "plain", 33447, origin=(-.5, 11.0, .5),
                  rotation=(0, 0, 8), edge=False)
    stopper.bottom.fill("S1")
    for face in flaps(g, "jerkin_skirt", 2, "L", "leather", 33448, top=11.2):
        for x in range(9):
            face.set(x, 1, "K2" if x % 3 else "L1")
