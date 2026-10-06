"""Flipped Shoulder Layers: smooth, side-parted layers falling to the shoulders, every end flicking
outward, a short side-swept fringe above the brow."""
from anime import ring_shell
from anime_male import SIDES, chain, taper
from paint import scalp

META = {"name": "Flipped Shoulder Layers", "gender": "male",
        "description": "Smooth shoulder-length layers with every end flicking outward, a short swept fringe."}


def build(g):
    scalp(g, 6301, side_rows=8, back_rows=8, sideburn=0, part=2)
    hat = ring_shell(g, 6302, side_rows=7, back_rows=8)
    hat.top.vline(2, 0, 7, "H1")
    for i, (x, rz) in enumerate(((-2.4, -32), (-.2, -40))):
        taper(g, f"fringe_{i}", (x, -8.6, -4.3), (-8, 0, rz), ((2, 3, 1), (1, 1, 1)), seed=6310 + i * 3, ring=0)
    # Sides: straight down, then a flick out at the ends.
    for side, sign in SIDES:
        for j, (z, length) in enumerate(((-3.0, 6), (-.4, 6), (2.8, 7))):
            flick = [(2, length, 2, (j * 3, 0, -3 * sign)), (2, 2, 1, (0, 0, -34 * sign)), (1, 1, 1, (0, 0, -48 * sign))]
            chain(g, f"{side}_layer_{j}", (4.5 * sign, -7.7, z), flick, seed=6320 + j * 7 + (sign > 0) * 23, ring=1)
    # Back: the same, flicking out behind.
    for i, x in enumerate((-2.9, -1.0, 1.0, 2.9)):
        flick = [(2, 7 + (i % 2), 1, (4, 0, -x * 1.5)), (2, 2, 1, (32, 0, -x * 4)), (1, 1, 1, (46, 0, -x * 5))]
        chain(g, f"back_{i}", (x, -7.6, 4.55), flick, seed=6360 + i * 7, ring=1)
