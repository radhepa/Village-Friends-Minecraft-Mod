"""Messy Parted: a side part with a swooping fringe, tousled crown tufts and layered back locks."""
from paint import hair_box, hair_face, k, rnd

META = {"name": "Messy Parted", "gender": "male", "description": "Side-parted, tousled and swept across the brow."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    # Scalp layer: hairline, sideburns and back, with a part on the wearer's left.
    hair_face(head.top, 3, 2)
    head.top.vline(5, 0, 7, "H0")
    head.top.vline(6, 0, 7, "H3")
    hair_face(head.back, 4, 2, rows=range(7))
    for x in (0, 2, 3, 6):
        head.back.set(x, 7, "H1")
    hair_face(head.right, 5, 2, rows=range(4))
    hair_face(head.left, 6, 2, rows=range(3))
    head.right.vline(7, 4, 5, "H1"), head.left.vline(0, 3, 5, "H1")  # sideburns
    head.right.vline(6, 4, 4, "H1"), head.left.vline(1, 3, 3, "H1")
    head.front.hline(0, 7, 0, "H1")
    for x in range(8):
        head.front.set(x, 1, "X1")
    head.front.set(0, 1, "H1"), head.front.set(7, 1, "H0")

    # Hat layer: half a pixel of volume with ragged edges.
    hair_face(hat.top, 8, 3, sheen_row=None)
    hat.top.vline(5, 0, 7, "H1")
    for x in range(8):
        hat.top.set(x, 7 - (1 if x == 5 else 0), "H3")
    hair_face(hat.back, 9, 2, sheen_row=1, rows=range(6))
    for x in range(8):
        if rnd(x, 1, 9) < .55:
            hat.back.set(x, 6, "H1")
    hair_face(hat.right, 10, 2, sheen_row=1, rows=range(3))
    hair_face(hat.left, 11, 2, sheen_row=1, rows=range(2))
    for x in range(8):
        if rnd(x, 2, 10) < .5:
            hat.right.set(x, 3, "H1")
    hat.front.hline(0, 7, 0, "H2")
    for x, y in [(0, 1), (1, 1), (2, 1), (0, 2), (7, 1), (7, 2), (7, 3), (7, 4), (6, 1)]:
        hat.front.set(x, y, "H1" if y > 1 else "H2")

    # The swoop: a long fringe lock falling from the part toward the wearer's right brow.
    swoop = g.piece("fringe_swoop", "HEAD", (-6.2, 0, -1.2), (7, 2, 2), pivot=(1.6, -8.6, -4.0), rotation=(0, 0, -9))
    hair_box(swoop, 21, 2, sheen_row=0, clump=2)
    for x in range(7):
        swoop.front.set(x, 1, k("H", 1 if x % 3 == 0 else 2))
    tip = g.piece("fringe_tip", "HEAD", (-2, 0, -1), (2, 2, 2), pivot=(-4.1, -7.7, -4.1), rotation=(0, 0, -20))
    hair_box(tip, 22, 2)

    # Tousled crown tufts break the box silhouette.
    tufts = [((-1.5, -1.6, -1.5), (3, 2, 3), (-1.2, -8.2, -1.0), (8, 0, 14)),
             ((-1, -1.4, -1.5), (2, 2, 3), (2.0, -8.1, .6), (-10, 0, -22)),
             ((-1.5, -1.2, -1), (3, 2, 2), (-2.6, -8.0, 2.2), (14, 0, 26)),
             ((-1, -1.3, -1), (2, 2, 2), (.6, -8.1, 2.8), (20, 0, -6))]
    for i, (origin, size, pivot, rot) in enumerate(tufts):
        tuft = g.piece(f"crown_tuft_{i}", "HEAD", origin, size, pivot=pivot, rotation=rot)
        hair_box(tuft, 30 + i, 2, top_delta=1)

    # Fuller side over the wearer's right ear; the parted side lies flatter.
    side = g.piece("side_right", "HEAD", (-1, 0, -3), (1, 4, 6), pivot=(-4.15, -8.4, .4), rotation=(0, 0, 6))
    hair_box(side, 40, 2, clump=2)
    for x in range(6):
        if x % 2:
            side.left.set(x, 3, "H1")
            side.right.set(x, 3, "H1")
    side_l = g.piece("side_left", "HEAD", (0, 0, -2.5), (1, 3, 5), pivot=(4.1, -8.3, .6), rotation=(0, 0, -4))
    hair_box(side_l, 41, 2)

    # Layered back locks, staggered in length.
    for i, (x, length, rot) in enumerate([(-4.3, 6, 6), (-1.5, 7, -2), (1.4, 6, -7)]):
        lock = g.piece(f"back_lock_{i}", "HEAD", (0, 0, 0), (3, length, 1), pivot=(x, -8.0, 4.1), rotation=(8, 0, rot))
        hair_box(lock, 50 + i, 2, sheen_row=1)
        lock.back.set(1, length - 1, "H1")
