"""Single Temple Braid: a short, side-swept crop with one thin braid left long at the right temple,
falling to the jaw and finished with a metal bead."""
from anime import ring_shell
from anime_male import fade, plait, plate, taper
from paint import scalp

META = {"name": "Single Temple Braid", "gender": "male",
        "description": "A short side-swept crop with one thin bead-tied braid at the temple."}


def build(g):
    scalp(g, 7701, side_rows=5, back_rows=7, sideburn=1)
    head = g.part("head")
    for face, rows in ((head.right, 5), (head.left, 5), (head.back, 7)):
        fade(face, 7702 + face.x0, rows - 2, rows - 1, base=1, start=.9, end=.45)
    ring_shell(g, 7703, side_rows=2, back_rows=5)
    # A short crop swept toward the wearer's left.
    for i, (x, z, ry) in enumerate(((-2.0, -1.9, -18), (1.4, -2.2, -22), (-1.8, 1.4, -10), (1.8, 1.6, -14), (0, 3.4, -6))):
        plate(g, f"crop_{i}", (x, -8.3 - (i % 2) * .12, z), (3, 1, 4), rotation=(-4, ry, 0), seed=7710 + i, sheen=1)
    for i, (x, rz) in enumerate(((-1.8, -26), (.6, -32))):
        taper(g, f"fringe_{i}", (x, -8.55, -4.3), (-10, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=7720 + i * 3, ring=0)
    for i, (x, rz) in enumerate(((-2.0, 6), (2.0, -6))):
        taper(g, f"nape_{i}", (x, -6.4, 4.4), (4, 0, rz), ((3, 2, 1), (1, 1, 1)), seed=7730 + i * 3, ring=1)
    # The braid, left long at the right temple.
    plait(g, "temple_braid", (-4.45, -7.4, -3.2), 6, rotation=(-3, 0, 3), width=1, depth=1, seed=7740, tie_role="M", tuft=2,
          motion="sway")
