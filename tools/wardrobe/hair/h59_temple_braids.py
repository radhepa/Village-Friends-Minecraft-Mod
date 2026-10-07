"""Temple Braids: centre-parted, shoulder-length straight hair with a thin braid at each temple,
tied off with a metal bead and hanging in front of the ears."""
from anime import ring_shell
from anime_male import SIDES, plait, taper
from paint import scalp

META = {"name": "Temple Braids", "gender": "male",
        "description": "Centre-parted shoulder-length hair with a thin bead-tied braid at each temple."}


def build(g):
    scalp(g, 5901, side_rows=7, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 5902, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    # Short centre-parted bangs sweeping off the brow.
    for side, sign in SIDES:
        taper(g, f"{side}_bang", (.3 * sign, -8.75, -4.3), (-8, 0, -44 * sign), ((2, 3, 1), (1, 1, 1)), seed=5910 + (sign > 0), ring=0)
        plait(g, f"{side}_braid", (4.45 * sign, -7.4, -3.3), 7, rotation=(-2, 0, -3 * sign), width=1, depth=1,
              seed=5915 + (sign > 0) * 5, tie_role="M", tuft=2)
        for j, (z, length, tilt) in enumerate(((-1.4, 8, 4), (1.4, 8, 6))):
            taper(g, f"{side}_lock_{j}", (4.45 * sign, -7.7, z), (j * 4, 0, -tilt * sign), ((2, length, 2), (1, 2, 1)),
                  seed=5930 + j * 3 + (sign > 0) * 7, ring=1)
    for i, (x, length, rz) in enumerate(((-3.0, 9, 6), (-1.0, 10, 2), (1.0, 10, -2), (3.0, 9, -6))):
        taper(g, f"back_{i}", (x, -7.6, 4.45), (5, 0, rz), ((2, length, 1), (1, 2, 1)), seed=5950 + i * 3, ring=1)
