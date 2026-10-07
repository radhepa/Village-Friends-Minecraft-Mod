"""Brow Cord: long, loose, centre-parted hair held off the face by a thin leather cord tied round the
head at the brow, knotted at the side with its ends hanging."""
from anime import ring_shell
from anime_male import SIDES, plate, taper, tie
from paint import scalp, solid

META = {"name": "Brow Cord", "gender": "male",
        "description": "Long loose hair held off the face by a thin leather cord knotted round the brow."}


def build(g):
    scalp(g, 7001, side_rows=8, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 7002, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    # Combed back from the part, under the cord.
    for side, sign in SIDES:
        plate(g, f"{side}_crown", (1.9 * sign, -8.3, -.4), (4, 1, 8), rotation=(-4, 0, 10 * sign), seed=7010 + (sign > 0), sheen=2)
    # The cord round the head at the brow, its knot and two ends at the wearer's left.
    cord = g.piece("cord", "HEAD", (-4.5, 0, -4.5), (9, 1, 9), pivot=(0, -7.0, 0), inflate=.08)
    solid(cord, "L", "leather", 7020, 2, edge=False)
    for face in cord.sides:
        face.hline(0, face.w - 1, 0, "L3")
    tie(g, "cord_knot", (4.75, -6.5, -1.6), (1, 2, 2), seed=7021)
    for i, (z, rx) in enumerate(((-2.0, -8), (-1.2, 10))):
        cord_end = g.piece(f"cord_end_{i}", "HEAD", (-.5, 0, -.5), (1, 4, 1), pivot=(4.9, -5.6, z), rotation=(rx, 0, -6 - i * 4), motion="sway")
        solid(cord_end, "L", "leather", 7022 + i, 2)
    # Long loose hair falling below the cord.
    for side, sign in SIDES:
        for j, (z, length, tilt) in enumerate(((-3.2, 9, 3), (-.4, 6, 5), (2.9, 10, 4))):
            taper(g, f"{side}_lock_{j}", (4.55 * sign, -6.6, z), (j * 3, 0, -tilt * sign), ((2, length, 2), (1, 2, 1)),
                  seed=7030 + j * 5 + (sign > 0) * 17, ring=1)
    for i, (x, rz) in enumerate(((-2.9, 4), (-1.0, 1), (1.0, -1), (2.9, -4))):
        taper(g, f"back_{i}", (x, -7.6, 4.6), (5, 0, rz), ((2, 11 + (i % 2), 1), (1, 2, 1)), seed=7060 + i * 5, ring=1, motion="sway")
