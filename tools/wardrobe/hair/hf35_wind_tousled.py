"""Wind-Tousled: shoulder-length hair caught by a gust, every lock streaming toward the wearer's left."""
from anime import ring_shell
from anime_female import curve, fall, paint, strand
from paint import scalp

META = {"name": "Wind-Tousled", "gender": "female",
        "description": "Shoulder-length hair caught in a gust, bangs and locks all streaming to one side."}


def build(g):
    scalp(g, 8501, side_rows=7, back_rows=8, sideburn=0, part=2)
    hat = ring_shell(g, 8502, side_rows=6, back_rows=8)
    hat.top.vline(2, 0, 7, "H1")
    for i, (x, z, rz) in enumerate(((-1.4, -1.6, -18), (1.6, .8, -26))):
        lift = g.piece(f"crown_lift_{i}", "HEAD", (-1.5, -1, -2.5), (3, 1, 5), pivot=(x, -8.4, z), rotation=(-6, 0, rz))
        paint(lift, "cel", 8505 + i, 2, ring=None)
    # Bangs blown across the brow; locks outside |x| < 3 may run longer.
    for i, (x, length, rz) in enumerate(((-3.0, 4, -64), (-1.4, 5, -72), (.4, 3, -56))):
        strand(g, f"bang_{i}", (x, -8.65, -4.35), (-8, 0, rz), ((2, length - 1), (1, 1)), 1, 8510 + i * 3, ring=None)
    # The windward side is pressed flat; the lee side streams out.
    strand(g, "right_flat", (-4.4, -7.8, .2), (8, 0, -6), ((1, 6),), 5, 8520)
    strand(g, "right_front", (-4.3, -7.6, -3.2), (0, 0, -10), ((2, 5), (1, 2)), 1, 8521)
    for j, (z, rz) in enumerate(((-2.8, -34), (-.4, -46), (2.0, -40))):
        curve(g, f"left_stream_{j}", (4.4, -7.4, z), ((2, 4, 0, -12), (2, 3, 4, rz), (1, 2, 8, rz - 14)), seed=8530 + j * 5,
              motion="sway")
    fall(g, "back", [(-3.0, -7.6, 4.4, ((3, 6), (2, 3), (1, 2)), 12, -18), (-1.0, -7.7, 4.8, ((3, 7), (2, 3), (1, 2)), 14, -24),
                     (1.0, -7.6, 4.4, ((3, 6), (2, 3), (1, 2)), 12, -30), (3.0, -7.7, 4.8, ((2, 5), (2, 3), (1, 2)), 14, -36)],
         8550, motion="sway")
