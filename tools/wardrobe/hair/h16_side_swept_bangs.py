"""Side-Swept Bangs: long bangs swept across the brow to one side, short pointed layers behind."""
from anime import back_fan, lock, ring_shell, sidelocks
from paint import scalp

META = {"name": "Side-Swept Bangs", "gender": "male", "description": "Long pointed bangs swept across the brow, short pointed layers behind."}


def build(g):
    scalp(g, 1601, side_rows=5, back_rows=8, sideburn=1, part=5)
    ring_shell(g, 1602, side_rows=4, back_rows=7)
    # Sweeping locks from the part on the wearer's left across toward the right temple.
    for i, (x, length, rz) in enumerate(((2.6, 6, 72), (1.0, 5, 64), (3.6, 4, 58))):
        lock(g, f"sweep_{i}", (x, -8.75, -4.35), (-6, 0, rz), ((2, length - 1), (1, 1)), 1, 1610 + i * 7, ring=None)
    lock(g, "sweep_fall", (-4.2, -7.4, -3.6), (0, 0, 8), ((2, 5), (1, 2)), 1, 1630)
    lock(g, "left_temple", (4.25, -7.6, -3.4), (0, 0, -4), ((1, 4), (1, 1)), 1, 1631)
    back_fan(g, "nape", [(-3.0, ((2, 4), (1, 2)), 8, 12), (-1.0, ((3, 4), (1, 2)), 2, 10), (1.0, ((3, 4), (1, 2)), -2, 10), (3.0, ((2, 4), (1, 2)), -8, 12)], 1640)
