"""Noble Coiled Updo: a tall double coil pinned at the back of the crown, smooth rolls over the ears,
curled tendrils at the temples and a slim metal circlet set with one stone."""
from anime import ring_shell
from anime_female import bun, combed, strand, swept_sides, tie, wave_face, SIDES
from paint import k, scalp, solid

META = {"name": "Noble Coiled Updo", "gender": "female",
        "description": "A tall coiled updo pinned at the crown, smooth rolls over the ears, curled tendrils and a slim circlet."}


def build(g):
    scalp(g, 8701, side_rows=8, back_rows=8, sideburn=0, part=3)
    swept_sides(g, ear_from=5)
    head = g.part("head")
    combed(head.back, (1, 2, 5, 6))
    hat = ring_shell(g, 8702, side_rows=4, back_rows=6)
    hat.top.vline(3, 0, 7, "H1")
    for side, sign in SIDES:
        roll = g.piece(f"{side}_roll", "HEAD", (-.5, -1.5, -3.5), (1, 3, 7), pivot=(4.5 * sign, -5.6, .6), rotation=(-10, 0, 0))
        for f in roll.faces:
            wave_face(f, 8710 + (sign > 0), 2)
        strand(g, f"{side}_tendril", (4.3 * sign, -7.2, -3.4), (0, 0, -2 * sign), ((1, 3), (1, 2, .5 * sign), (1, 2, -.3 * sign)),
               1, 8715 + (sign > 0), texture="ringlet", ring=None)
        band = g.piece(f"{side}_circlet", "HEAD", (-.5, -.5, -4.5), (1, 1, 9), pivot=(4.6 * sign, -7.6, 0), inflate=.05)
        solid(band, "M", "smooth", 8720, 3, edge=False)
    front = g.piece("circlet_front", "HEAD", (-4.5, -.5, -.5), (9, 1, 1), pivot=(0, -7.6, -4.6), inflate=.05)
    solid(front, "M", "smooth", 8721, 3, edge=False)
    front.front.set(4, 0, k("M", 4))
    tie(g, "circlet_stone", (0, -7.6, -4.75), size=(1, 1, 1), y=-.5, role="A", base=3, inflate=.12)
    # Two coils stacked up and back from the crown, a long pin through both.
    bun(g, "lower_coil", (0, -8.5, 3.1), (-55, 0, 0), (6, 2, 5), seed=8730)
    bun(g, "upper_coil", (0, -9.9, 4.8), (-55, 0, 0), (4, 2, 3), seed=8735)
    pin = g.piece("pin", "HEAD", (-3.5, -.5, -.5), (7, 1, 1), pivot=(.2, -9.2, 4.3), rotation=(-20, 0, -24))
    solid(pin, "M", "smooth", 8740, 3, edge=False)
    pin.front.set(6, 0, k("M", 4))
