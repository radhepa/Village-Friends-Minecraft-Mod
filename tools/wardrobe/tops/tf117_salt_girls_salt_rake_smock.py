"""Salt Girl's Salt-Rake Smock: a loose drawstring linen smock to the knee, its hem stiff with a white crust
of salt, with the long wooden salt-rake carried crosswise behind her shoulders under two loops."""
from kit_female import chemise, over_flaps
from paint import fabric, k, rnd, solid

META = {
    "name": "Salt Girl's Salt-Rake Smock",
    "gender": "female",
    "description": "A loose drawstring linen smock to the knee, its hem crusted white with salt, and a long salt-rake carried across her back.",
    "tags": ["sea", "work", "relaxed"],
    "covers_waist": True,
}

SEED = 53210


def crust(face, seed, rows=2):
    """Salt dried white along the hem, a damp shadow just above it."""
    for x in range(face.w):
        face.set(x, face.h - rows - 1, "S2")
        for y in range(face.h - rows, face.h):
            face.set(x, y, "S4" if rnd(x + face.x0, y, seed) < .7 else "S3")


def build(g):
    chemise(g, "S", 3, "weave", SEED, neckline="round", sleeve_rows=(0, 7), gather=False)
    j = g.part("jacket")
    for face in j.sides:
        fabric(face, "S", "weave", SEED + 1, 3)
        for x in range(face.w):                                      # gathered under the drawstring
            if x % 2:
                face.set(x, 1, "S2")
    fabric(j.top, "S", "weave", SEED + 1, 4)
    for x in range(2, 6):
        j.front.clear(x, 0)
    for x in (2, 5):
        j.front.set(x, 1, "A2")                                      # the drawstring
    j.front.set(3, 1, "A3"), j.front.set(3, 2, "A2"), j.front.set(4, 2, "A1")
    for face in (j.front, j.back):
        face.vline(2, 3, 11, "S2"), face.vline(5, 4, 11, "S2")       # long loose folds
    for side in ("right", "left"):
        sleeve = g.part(f"{side}_sleeve")
        for face in sleeve.sides:
            fabric(face, "S", "weave", SEED + 2, 3, 0, 0, face.w, 7)
            face.hline(0, face.w - 1, 6, "S2")
            for x in range(0, face.w, 2):
                face.set(x, 7, "S2")                                 # the loose sleeve end
        fabric(sleeve.top, "S", "weave", SEED + 2, 4)
    f, b = over_flaps(g, "smock", 5, "S", "weave", SEED + 3, base=3, width=9, top=9.0)
    for face in (f, b):
        face.vline(2, 1, 2, "S2"), face.vline(6, 1, 3, "S2")
        crust(face, SEED + 4)
    f.vline(8, 0, 4, "S2"), b.vline(0, 0, 4, "S2")                  # side slits
    # The salt-rake: a long handle held crosswise behind the shoulders, its flat board at her left.
    handle = g.piece("salt_rake_handle", "TORSO", (-9, 0, 0), (18, 1, 1), pivot=(0, 3.4, 3.3))
    solid(handle, "L", "smooth", SEED + 5, 3)
    for face in handle.sides:
        face.set(0, 0, "L2"), face.set(face.w - 1, 0, "L2")
    board = g.piece("salt_rake_board", "TORSO", (-1, -3, -.5), (2, 7, 1), pivot=(9.6, 3.9, 3.8))
    solid(board, "L", "smooth", SEED + 6, 2)
    for face in board.sides:
        face.hline(0, face.w - 1, 0, "L3")
    board.back.vline(0, 1, 6, "L1"), board.back.vline(1, 0, 6, "L3")
    board.bottom.fill("S4"), board.back.set(0, 6, "S4"), board.back.set(1, 6, "S4")   # salt caked on the blade edge
    for i, x in enumerate((-2.6, 2.6)):                              # two loops from the smock's back
        loop = g.piece(f"salt_rake_loop_{i}", "TORSO", (-.5, -.5, 0), (1, 2, 2), pivot=(x, 3.4, 2.2), inflate=.05)
        solid(loop, "L", "leather", SEED + 7 + i, 1, edge=False)
        loop.back.fill(k("L", 2))
