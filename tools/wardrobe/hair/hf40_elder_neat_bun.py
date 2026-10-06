"""Elder's Neat Bun: centre-parted, set in soft combed waves over the temples and pinned in a small tidy bun."""
from anime import ring_shell
from anime_female import bun, combed, paint, swept_sides, wave_face, SIDES
from paint import k, scalp, solid

META = {"name": "Elder's Neat Bun", "gender": "female",
        "description": "A centre part, soft combed waves over the temples and a small, tidy pinned bun."}


def build(g):
    scalp(g, 9001, side_rows=8, back_rows=8, sideburn=0, part=3)
    swept_sides(g, ear_from=5, ear_depth=3)
    head = g.part("head")
    combed(head.back, (1, 3, 4, 6))
    hat = ring_shell(g, 9002, side_rows=5, back_rows=6)
    hat.top.vline(3, 0, 7, "H1")
    for f in (hat.right, hat.left):
        wave_face(type(f)(f.layer, f.x0, f.y0, f.w, 5, f.name), 9003, 2)
    for side, sign in SIDES:
        # A set wave falling from the part over each temple, then the side combed back over the ear.
        wave = g.piece(f"{side}_temple_wave", "HEAD", (-1.5, -1, -2.5), (3, 1, 5), pivot=(2.3 * sign, -8.15, -1.4),
                       rotation=(0, 0, 18 * sign))
        paint(wave, "wave", 9010 + (sign > 0), 2, ring=0)
        side_wave = g.piece(f"{side}_side_wave", "HEAD", (-.5, -2, -3), (1, 4, 6), pivot=(4.45 * sign, -5.8, .7), rotation=(-8, 0, 0))
        paint(side_wave, "wave", 9015 + (sign > 0), 2, ring=None)
    bun(g, "bun", (0, -5.2, 5.0), (-80, 0, 0), (4, 2, 4), seed=9020)
    pin = g.piece("pin", "HEAD", (-2.5, -.5, -.5), (5, 1, 1), pivot=(0, -5.0, 5.9), rotation=(0, 0, 30))
    solid(pin, "M", "smooth", 9030, 3, edge=False)
    pin.back.set(0, 0, k("M", 4))
