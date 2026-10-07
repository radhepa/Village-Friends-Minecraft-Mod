"""Low Chignon: swept back over the ears into a smooth, wide bun at the nape held with a long metal pin."""
from anime import ring_shell
from anime_female import bun, combed, pointed, strand, swept_sides, SIDES
from paint import k, scalp, solid

META = {"name": "Low Chignon", "gender": "female",
        "description": "Smooth hair swept back over the ears into a low bun at the nape, pinned with a long hairpin."}


def build(g):
    scalp(g, 6901, side_rows=8, back_rows=8, sideburn=0, part=5)
    swept_sides(g, ear_from=4)
    head = g.part("head")
    combed(head.back, (1, 3, 4, 6))
    hat = ring_shell(g, 6902, side_rows=3, back_rows=5)
    hat.top.vline(5, 0, 7, "H1")
    strand(g, "sweep_0", (2.7, -8.65, -4.35), (-6, 0, 72), ((2, 5), (1, 1)), 1, 6910, ring=None)
    strand(g, "sweep_1", (1.1, -8.6, -4.35), (-6, 0, 62), ((2, 4), (1, 1)), 1, 6911, ring=None)
    pointed(g, "right_frame", (-4.3, -7.4, -3.4), (0, 0, 6), 2, 5, 2, seed=6915)
    for side, sign in SIDES:
        # A smooth roll of hair swept back over the top of each ear toward the bun.
        roll = g.piece(f"{side}_roll", "HEAD", (-.5, -1, -3.5), (1, 2, 7), pivot=(4.45 * sign, -5.3, .9), rotation=(-14, 0, 0))
        strand_paint = (2, 3)
        for f in roll.sides:
            for y in range(f.h):
                for x in range(f.w):
                    f.set(x, y, k("H", strand_paint[0] + (1 if y == 0 else 0) - (1 if (x + y) % 4 == 3 else 0)))
        roll.top.fill(k("H", 3)), roll.bottom.fill(k("H", 1))
    bun(g, "chignon", (0, -2.5, 5.2), (-90, 0, 0), (5, 2, 4), seed=6920)
    pin = g.piece("hairpin", "HEAD", (-3.5, -.5, -.5), (7, 1, 1), pivot=(0, -2.6, 6.0), rotation=(0, 0, 18))
    solid(pin, "M", "smooth", 6930, 3, edge=False)
    pin.front.set(0, 0, k("M", 4)), pin.back.set(6, 0, k("M", 4))
    for i, (x, rz) in enumerate(((-1.6, 8), (1.9, -10))):
        strand(g, f"nape_wisp_{i}", (x, -1.4, 4.3), (6, 0, rz), ((1, 2), (1, 1)), 1, 6940 + i, ring=None)
