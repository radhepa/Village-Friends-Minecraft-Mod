"""Mutton-Chop Crop: a short crop combed forward and to one side, over bushy sideburns that broaden
down the cheeks to the jaw."""
from anime import ring_shell
from anime_male import SIDES, clump, combed_face, plate, taper
from paint import k, scalp

META = {"name": "Mutton-Chop Crop", "gender": "male",
        "description": "A short forward-combed crop over bushy sideburns that broaden down to the jaw."}


def build(g):
    scalp(g, 3901, side_rows=4, back_rows=7, sideburn=0)
    head, hat = g.part("head"), g.part("hat")
    # The chops on the scalp: the front columns of each side, widening toward the jaw.
    for y in range(4, 8):
        width = 2 if y < 6 else 3
        for i in range(width):
            head.right.set(7 - i, y, k("H", 2 - (1 if i == width - 1 else 0)))
            head.left.set(i, y, k("H", 2 - (1 if i == width - 1 else 0)))
    for y in (1, 2, 3, 5, 6, 7):
        head.front.set(0, y, "H1"), head.front.set(7, y, "H1")
    ring_shell(g, 3902, side_rows=3, back_rows=6)
    for y in range(3, 8):
        hat.right.set(7, y, "H2"), hat.left.set(0, y, "H2")
    # A short crop combed forward and a little to the wearer's right.
    for i, (x, z, ry) in enumerate(((-1.9, -1.6, 24), (1.9, -1.8, 18), (-1.6, 1.8, 14), (1.8, 1.6, 10))):
        plate(g, f"crop_{i}", (x, -8.3 - (i % 2) * .12, z), (4, 1, 4), rotation=(-5, ry, 0), seed=3910 + i, sheen=1)
    for i, (x, rz) in enumerate(((-2.8, 22), (-.6, 16), (1.6, 10))):
        taper(g, f"fringe_{i}", (x, -8.5, -4.3), (-10, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=3920 + i * 3, ring=0)
    # The chops themselves, bushy and broadening at the jaw.
    for side, sign in SIDES:
        chop = clump(g, f"{side}_chop", (4.3 * sign, -5.9, -2.5), (1, 4, 3), rotation=(0, 0, -4 * sign), seed=3930 + (sign > 0), ring=0)
        combed_face(chop.right if sign < 0 else chop.left, 3932 + (sign > 0), 2)
        clump(g, f"{side}_jaw", (4.4 * sign, -2.5, -2.7), (1, 2, 4), rotation=(0, 0, -12 * sign), seed=3934 + (sign > 0))
    for i, x in enumerate((-2.2, 2.2)):
        taper(g, f"nape_{i}", (x, -6.2, 4.35), (4, 0, -x * 2), ((3, 3, 1), (2, 1, 1)), seed=3940 + i * 3, ring=1)
