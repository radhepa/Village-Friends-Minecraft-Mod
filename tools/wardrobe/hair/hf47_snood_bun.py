"""Snood Bun: centre-parted hair gathered at the nape into a netted snood of gold thread, held by a slim band."""
from anime import ring_shell
from anime_female import combed, strand, swept_sides, SIDES
from paint import k, rnd, scalp, solid

META = {"name": "Snood Bun", "gender": "female",
        "description": "Centre-parted hair gathered at the nape into a gold-thread snood, held by a slim band over the crown."}


def netted(box, seed, base=2):
    """Hair showing through a diamond lattice of metal thread, with a bead at each crossing."""
    for f in box.faces:
        for y in range(f.h):
            for x in range(f.w):
                xx = x + f.x0
                on = (xx + y) % 3 == 0 or (xx - y) % 3 == 0
                cross = (xx + y) % 3 == 0 and (xx - y) % 3 == 0
                hair = base + (1 if rnd(xx, y, seed) > .7 else 0) - (1 if y == f.h - 1 else 0)
                f.set(x, y, k("M", 4) if cross else k("M", 2) if on else k("H", hair))


def build(g):
    scalp(g, 9701, side_rows=8, back_rows=8, sideburn=0, part=3)
    swept_sides(g, ear_from=5)
    head = g.part("head")
    combed(head.back, (1, 2, 5, 6), rows=range(0, 5))
    hat = ring_shell(g, 9702, side_rows=4, back_rows=4)
    hat.top.vline(3, 0, 7, "H1")
    for side, sign in SIDES:
        strand(g, f"{side}_curtain", (.3 * sign, -8.75, -4.35), (-6, 0, 62 * -sign), ((2, 4), (1, 1)), 1, 9710 + (sign > 0), ring=None)
        strand(g, f"{side}_side", (4.45 * sign, -7.8, 1.2), (14, 0, -2 * sign), ((1, 5),), 5, 9712 + (sign > 0), ring=0)
        band = g.piece(f"{side}_band", "HEAD", (-.5, 0, -.5), (1, 4, 1), pivot=(4.6 * sign, -8.6, -.2), inflate=.05)
        solid(band, "M", "smooth", 9715, 3, edge=False)
    top = g.piece("band_top", "HEAD", (-4.5, -1, -.5), (9, 1, 1), pivot=(0, -8.45, -.2), inflate=.05)
    solid(top, "M", "smooth", 9716, 3, edge=False)
    # The snood: a full rounded bag of hair at the nape.
    for i, (size, centre) in enumerate((((7, 4, 3), (0, -2.6, 5.2)), ((5, 1, 3), (0, -5.0, 5.0)), ((5, 1, 2), (0, -.1, 5.3)),
                                        ((5, 3, 1), (0, -2.6, 7.0)))):
        w, h, d = size
        bag = g.piece(f"snood_{i}", "HEAD", (-w / 2, -h / 2, -d / 2), size, pivot=centre)
        netted(bag, 9720 + i)
