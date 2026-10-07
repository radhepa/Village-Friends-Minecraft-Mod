"""Short Locs: thick rounded locs to the chin, a few tipped over the brow, every one its own length."""
from anime import ring_shell
from anime_female import paint, strand, SIDES
from paint import scalp

META = {"name": "Short Locs", "gender": "female",
        "description": "Chin-length locs, thick and rounded, a few falling over the brow, each its own length and lean."}


def build(g):
    scalp(g, 8101, side_rows=8, back_rows=8, sideburn=0)
    ring_shell(g, 8103, side_rows=6, back_rows=7)
    # Locs over the crown lying back; three tip forward over the brow.
    for i, (x, z, rz) in enumerate(((-2.2, -.2, 14), (2.2, .2, -14), (0, 2.4, 2))):
        top = g.piece(f"crown_loc_{i}", "HEAD", (-1, -1, -3), (2, 2, 6), pivot=(x, -8.6, z), rotation=(-8, 0, rz))
        paint(top, "loc", 8115 + i, 2)
    for i, (x, rz) in enumerate(((-2.4, 12), (-.2, 2), (2.1, -10))):
        strand(g, f"brow_loc_{i}", (x, -8.9, -3.7), (-24, 0, rz), ((2, 3, 0, 2),), 1, 8110 + i, ring=None, texture="loc")
    for side, sign in SIDES:
        for j, (z, n, tilt) in enumerate(((-2.8, 6, 6), (-.6, 7, 10), (1.6, 6, 12), (3.4, 7, 8))):
            strand(g, f"{side}_loc_{j}", (4.6 * sign, -7.4, z), (0, 0, -tilt * sign), ((2, n, 0, 2), (1, 1, 0, 1)), 1,
                   8120 + j * 3 + (sign > 0), ring=None, texture="loc", motion="sway")
    for i, (x, z, rz, n) in enumerate(((-2.7, 4.6, 9, 7), (-.9, 5.0, 3, 8), (.9, 4.6, -3, 8), (2.7, 5.0, -9, 6))):
        strand(g, f"back_loc_{i}", (x, -7.4, z), (6, 0, rz), ((2, n, 0, 2), (1, 1, 0, 1)), 1, 8150 + i, ring=None, texture="loc",
               motion="sway")
