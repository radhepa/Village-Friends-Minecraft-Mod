"""Long Tucked: long straight hair parted in the centre, swept off the brow and tucked behind the ears,
falling well past the shoulders down the back."""
from anime import ring_shell
from anime_male import SIDES, clump, combed_face, taper
from paint import scalp

META = {"name": "Long Tucked", "gender": "male",
        "description": "Long straight hair parted in the centre and tucked behind the ears, past the shoulders."}


def build(g):
    scalp(g, 6101, side_rows=5, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 6102, side_rows=4, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    for side, sign in SIDES:
        # Swept from the part over the temple...
        taper(g, f"{side}_sweep", (.35 * sign, -8.75, -4.3), (-6, 0, -70 * sign), ((2, 4, 1), (1, 1, 1)), seed=6110 + (sign > 0), ring=0)
        # ...and back over the top of the ear, tucked behind it.
        tuck = clump(g, f"{side}_tuck", (4.45 * sign, -8.2, -.6), (1, 3, 6), rotation=(24, 0, -2 * sign), seed=6115 + (sign > 0))
        combed_face(tuck.right if sign < 0 else tuck.left, 6117 + (sign > 0), 2, sheen=0, across_y=True)
        taper(g, f"{side}_behind_ear", (4.45 * sign, -6.4, 2.9), (4, 0, -3 * sign), ((2, 8, 2), (1, 2, 1)), seed=6120 + (sign > 0), ring=1)
    for i, (x, length, rz) in enumerate(((-3.0, 11, 4), (-1.0, 12, 1), (1.0, 12, -1), (3.0, 11, -4))):
        taper(g, f"back_{i}", (x, -7.8, 4.45), (5, 0, rz), ((2, length, 1), (2, 2, 1), (1, 1, 1)), seed=6130 + i * 3, ring=1,
              motion="sway")
