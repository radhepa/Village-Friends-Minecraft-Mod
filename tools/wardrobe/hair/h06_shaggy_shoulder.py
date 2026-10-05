"""Shaggy Shoulder-Length: choppy layered locks falling to the shoulders, bangs swept off-centre."""
from paint import hair_box, rnd, scalp, shell

META = {"name": "Shaggy Shoulder-Length", "description": "Choppy layers falling to the shoulders with face-framing locks."}


def ragged(box, seed):
    """Notch the lowest row so each lock ends in uneven points."""
    for f in box.sides:
        for x in range(f.w):
            if rnd(x, 0, seed) < .45:
                f.set(x, f.h - 1, "H0")


def build(g):
    scalp(g, 501, side_rows=6, back_rows=8, sideburn=2, part=2)
    shell(g, 502, side_rows=6, back_rows=8, front=[(0, 1), (0, 2), (0, 3), (0, 4), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
                                                       (4, 1), (5, 1), (6, 1), (1, 1)])
    for i, (x, z, rx, rz) in enumerate(((-2.2, -1.8, 10, 12), (1.4, -2.2, 6, -10), (-1.6, 1.4, -10, 8), (2.0, 1.8, -8, -14))):
        lock = g.piece(f"crown_lock_{i}", "HEAD", (-1.5, -1, -1.5), (3, 2, 3), pivot=(x, -8.0, z), rotation=(rx, 0, rz))
        hair_box(lock, 510 + i, 2, top_delta=1)
    # Three locks per side, each a different length and angle.
    for side, sign in (("right", -1), ("left", 1)):
        for j, (z, length, tilt) in enumerate(((-1.7, 7, 4), (.3, 8, 7), (2.4, 7, 5))):
            lock = g.piece(f"{side}_lock_{j}", "HEAD", (-.5, 0, -1), (1, length, 2),
                           pivot=(4.25 * sign + .1 * sign * j, -7.7, z), rotation=(0, 0, -tilt * sign))
            hair_box(lock, 520 + j + (sign > 0) * 5, 2, sheen_row=1)
            ragged(lock, 530 + j)
        frame = g.piece(f"{side}_frame", "HEAD", (-.5, 0, -.5), (1, 6, 1), pivot=(4.2 * sign, -7.2, -3.6), rotation=(0, 0, -3 * sign))
        hair_box(frame, 535 + (sign > 0), 2, sheen_row=0)
    # Back: a row of long locks, a shorter layer on top.
    for i, (x, length, rz) in enumerate(((-3.0, 9, 6), (0, 10, 0), (3.0, 9, -6))):
        lock = g.piece(f"back_lock_{i}", "HEAD", (-1.5, 0, 0), (3, length, 1), pivot=(x, -7.8, 4.15), rotation=(5, 0, rz))
        hair_box(lock, 540 + i, 2, sheen_row=2)
        ragged(lock, 545 + i)
    for i, (x, rz) in enumerate(((-1.6, 8), (1.6, -8))):
        layer = g.piece(f"back_layer_{i}", "HEAD", (-1.5, 0, 0), (3, 6, 1), pivot=(x, -7.0, 5.1), rotation=(10, 0, rz))
        hair_box(layer, 550 + i, 2, sheen_row=1)
        ragged(layer, 555 + i)
    for i, (x, w, rz) in enumerate(((-1.0, 3, -10), (2.0, 3, -16))):
        bang = g.piece(f"bang_{i}", "HEAD", (-w / 2, 0, -1), (w, 2, 1), pivot=(x, -8.6, -4.3), rotation=(-10, 0, rz))
        hair_box(bang, 560 + i, 2, sheen_row=0)
