"""Wool Carder's Fleece-Dusted Bodice: a side-hooked bodice and chemise dusted with clinging tufts of fleece,
a pair of toothed wool cards hung at the girdle and a soft rolag tucked behind them."""
from kit_female import OVER_FRONT, bodice, chemise, girdle
from paint import k, solid

META = {
    "name": "Wool Carder's Fleece-Dusted Bodice",
    "gender": "female",
    "description": "A bodice and chemise dusted with clinging tufts of fleece, a pair of toothed wooden wool cards hung at the girdle and a soft rolag beside them.",
    "tags": ["work", "casual"],
}

TUFTS = {"front": [(1, 3), (5, 6), (2, 8)], "back": [(5, 3), (1, 7)], "right": [(1, 4)], "left": [(2, 6)]}


def tuft(face, x, y):
    """A wisp of fleece caught on the cloth."""
    face.set(x, y, "S4"), face.set(x + 1, y, "S3"), face.set(x, y + 1, "S3")


def card(g, pid, x, tilt, dz=0.0):
    """A wool card: a square wooden back with rows of fine wire teeth, and its handle."""
    pivot = (x, 8.2, OVER_FRONT - .1)
    board = g.piece(pid, "TORSO", (-1.5, 1.2, -1.0 + dz), (3, 3, 1), pivot=pivot, rotation=(0, 0, tilt), motion="flap_front")
    solid(board, "L", "smooth", 51362, 3, edge=False)
    for y in range(3):
        for xx in range(3):
            board.front.set(xx, y, "M3" if (xx + y) % 2 == 0 else "K1")
    board.front.hline(0, 2, 0, "L3")
    grip = g.piece(f"{pid}_handle", "TORSO", (-.5, -.4, -1.0 + dz), (1, 2, 1), pivot=pivot, rotation=(0, 0, tilt),
                   motion="flap_front")
    solid(grip, "L", "smooth", 51363, 2, edge=False)
    grip.top.fill("L3")


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51360, neckline="square", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 10, "S2"), arm.strip.hline(0, 15, 11, "S4")
        for x, y in ((3, 4), (10, 7), (14, 2)):
            tuft(arm.strip, x, y)
    b = bodice(g, "P", "twill", 51361, rows=(2, 9), neckline="square", edge="P3", seams=False)
    for face in (b.right, b.left):
        for y in range(3, 10, 2):
            face.set(1, y, "M3")                                      # hooked up the sides
        face.vline(2, 2, 9, "P1")
    b.front.vline(2, 3, 9, "P1"), b.front.vline(5, 3, 9, "P1")
    for name, spots in TUFTS.items():
        for x, y in spots:
            tuft(getattr(b, name), x, y)
    girdle(g, "girdle", 7.8, role="L", height=1)
    card(g, "wool_card_back", 2.5, 10, dz=.6)
    card(g, "wool_card_front", 1.1, -8)
    # A rolag of carded wool, rolled ready for the wheel, tucked into the girdle.
    rolag = g.piece("rolag", "TORSO", (-2, -.5, -.5), (4, 1, 1), pivot=(-2.0, 8.6, OVER_FRONT - .3), inflate=.2,
                    motion="flap_front")
    solid(rolag, "S", "plain", 51364, 4, edge=False)
    for f in rolag.sides:
        for xx in range(f.w):
            f.set(xx, 0, k("S", 4 if xx % 2 else 3))
