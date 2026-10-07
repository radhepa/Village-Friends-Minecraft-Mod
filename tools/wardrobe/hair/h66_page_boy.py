"""Scholar's Page-Boy: a rounded, jaw-length cut parted in the centre into two short curtains, the
ends rolled neatly under all the way round."""
from anime import ring_shell
from anime_male import SIDES, chain, clump
from paint import scalp

META = {"name": "Scholar's Page-Boy", "gender": "male",
        "description": "A rounded jaw-length cut, centre-parted curtains and the ends rolled neatly under."}


def build(g):
    scalp(g, 6601, side_rows=8, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 6602, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1"), hat.top.vline(4, 0, 7, "H1")
    # Centre-parted curtains arching from the part out to each temple, well above the brows.
    for side, sign in SIDES:
        chain(g, f"{side}_curtain", (.2 * sign, -8.5, -4.35), [(2, 3, 1, (0, 0, -82 * sign)), (2, 3, 1, (0, 0, -36 * sign)),
                                                               (1, 1, 1, (0, 0, -18 * sign))], seed=6610 + (sign > 0) * 7, ring=0)
    # Smooth panels round the sides and back, each rolled under at the jaw.
    for side, sign in SIDES:
        for j, z in enumerate((-2.4, .8)):
            chain(g, f"{side}_panel_{j}", (4.5 * sign, -8.1, z), [(1, 6, 3, (0, 0, -2 * sign)), (1, 2, 3, (0, 0, 55 * sign))],
                  seed=6620 + j * 7 + (sign > 0) * 17, ring=1, overlap=.5)
        clump(g, f"{side}_tuck", (4.5 * sign, -8.1, 3.4), (1, 7, 2), seed=6640 + (sign > 0), ring=1)
    for i, x in enumerate((-2.7, 0, 2.7)):
        chain(g, f"back_{i}", (x, -8.1, 4.55), [(3, 6, 1, (2, 0, 0)), (3, 2, 1, (-55, 0, 0))], seed=6650 + i * 7, ring=1, overlap=.5)
