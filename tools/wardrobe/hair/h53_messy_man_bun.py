"""Messy Man Bun: hair dragged back into a loose bun at the back of the crown, bound with a leather
tie, its ends poking out, strands escaping at the temples and the nape."""
from anime import ring_shell
from anime_male import SIDES, clump, combed_face, plate, taper, tie
from paint import scalp

META = {"name": "Messy Man Bun", "gender": "male",
        "description": "Dragged back into a loose bun at the back of the crown, with strands escaping."}


def build(g):
    scalp(g, 5301, side_rows=6, back_rows=8, sideburn=1)
    hat = ring_shell(g, 5302, side_rows=5, back_rows=7)
    combed_face(hat.top, 5303, 3)
    # Combed back toward the bun.
    for i, (x, w) in enumerate(((-2.4, 3), (.4, 3), (2.8, 2))):
        plate(g, f"swept_{i}", (x, -8.3 - (i % 2) * .15, -.4), (w, 1, 7), rotation=(-5, 0, -x * 2), seed=5310 + i, sheen=2)
    # The bun: a loose core with two loops and its ends poking out.
    tie(g, "tie", (0, -7.3, 4.75), (3, 3, 1), seed=5320)
    core = clump(g, "bun", (0, -7.4, 4.9), (4, 3, 2), origin=(-2, -1.5, 0), rotation=(-16, 0, 6), seed=5321, ring=0)
    core.top.set(1, 1, "H4")
    for i, (x, rz) in enumerate(((-1.7, -28), (1.6, 34))):
        clump(g, f"bun_loop_{i}", (x, -8.4, 5.6), (2, 2, 2), origin=(-1, -1, -1), rotation=(10, 0, rz), seed=5325 + i, ring=0)
    taper(g, "bun_end_0", (.8, -8.8, 5.8), (-30, 0, -24), ((2, 2, 1), (1, 1, 1)), seed=5330, up=True, ring=None)
    taper(g, "bun_end_1", (-1.0, -6.2, 6.3), (24, 0, 18), ((2, 2, 1), (1, 1, 1)), seed=5333, ring=None)
    # Strands that escaped the tie.
    for side, sign in SIDES:
        taper(g, f"{side}_temple", (4.35 * sign, -7.8, -3.3), (-4, 0, -5 * sign), ((1, 4, 1), (1, 1, 1)), seed=5340 + (sign > 0), ring=0)
    for i, (x, rz) in enumerate(((-1.8, 10), (1.6, -6))):
        taper(g, f"nape_{i}", (x, -4.2, 4.35), (6, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=5350 + i * 3, ring=1)
