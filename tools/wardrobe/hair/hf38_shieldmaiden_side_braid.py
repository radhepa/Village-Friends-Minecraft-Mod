"""Shieldmaiden Side Braid: one side shaved close, the long top swept over to the other side, where a braid runs
back along the head and down behind the shoulder to a metal bead."""
from anime import ring_shell
from anime_female import fall, paint, plait_along, stubble, strand, tie
from paint import scalp

META = {"name": "Shieldmaiden Side Braid", "gender": "female",
        "description": "One side shaved, the long top swept over, and a braid along the other side ending in a metal bead."}

BRAID = [(4.75, -7.6, -2.8), (5.15, -6.8, -.4), (5.05, -5.6, 2.0), (4.3, -3.8, 4.1), (3.7, -.8, 4.9), (3.5, 2.4, 4.8)]


def build(g):
    scalp(g, 8801, side_rows=8, back_rows=8, sideburn=0, part=2)
    head = g.part("head")
    stubble(head.right, 8802, range(0, 8))
    for x in range(0, 3):   # the shave runs round to the back of the right side
        for y in range(2, 8):
            head.back.set(7 - x, y, None if (x + y) % 3 == 0 else "H0")
    hat = ring_shell(g, 8803, side_rows=6, back_rows=8)
    for y in range(8):
        for x in range(8):
            hat.right.set(x, y, None)
    for y in range(0, 8):
        for x in range(0, 3):
            hat.back.set(7 - x, y, None)
    for x in range(0, 3):
        hat.top.vline(x, 0, 7, None)
    hat.top.vline(2, 0, 7, "H1")
    # The long top, swept over from the edge of the shave toward the braided side.
    for i, (x, rz) in enumerate(((-1.4, -8), (.8, -16), (2.8, -26))):
        top = g.piece(f"top_{i}", "HEAD", (-1.5, -1, -4), (3, 1, 8), pivot=(x, -8.3, .3), rotation=(-2, 0, rz))
        paint(top, "cel", 8810 + i * 3, 2, ring=None)
    strand(g, "sweep_0", (-2.6, -8.7, -4.35), (-6, 0, -70), ((2, 5), (1, 1)), 1, 8820, ring=None)
    strand(g, "sweep_1", (-.9, -8.65, -4.35), (-6, 0, -58), ((2, 4), (1, 1)), 1, 8821, ring=None)
    strand(g, "left_cover", (4.45, -7.8, 1.0), (0, 0, -3), ((1, 5),), 5, 8822)
    plait_along(g, "side_braid", BRAID, spacing=1.8, seed=8830)
    tie(g, "bead", (3.5, 3.4, 4.8), size=(2, 2, 2), y=-1, role="M", base=3, inflate=.05)
    strand(g, "braid_end", (3.5, 4.3, 4.8), (0, 0, 0), ((2, 1), (1, 2)), 2, 8840, ring=None)
    fall(g, "back", [(-1.4, -7.6, 4.4, ((3, 9), (2, 2), (1, 2)), -3, -2), (.8, -7.7, 4.75, ((3, 10), (2, 2), (1, 2)), -4, -5),
                     (2.6, -7.6, 4.4, ((2, 8), (1, 2)), -3, -8)], 8850, motion="sway")
