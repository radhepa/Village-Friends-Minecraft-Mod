"""Long Wolf Cut: heavy choppy layers at the crown and sides, wispy bangs and long pointed layers down the nape."""
from anime import ring_shell
from anime_female import fall, points, strand, SIDES
from paint import scalp

META = {"name": "Long Wolf Cut", "gender": "female",
        "description": "Choppy, shaggy crown and side layers, wispy bangs and long pointed layers falling down the nape."}


def build(g):
    scalp(g, 9201, side_rows=8, back_rows=8, sideburn=0)
    ring_shell(g, 9202, side_rows=7, back_rows=8)
    points(g, "bang", [(-3.0, 2, 2, 2, 12), (-1.0, 2, 2, 2, 4), (1.0, 2, 2, 2, -6), (3.1, 2, 2, 2, -14)], 9210)
    # Crown layers lying back and down, so their points flick out over the back of the head.
    for i, (x, z, rz) in enumerate(((-2.2, .6, 14), (.2, 1.0, -2), (2.4, .4, -16))):
        strand(g, f"crown_{i}", (x, -8.6, z), (64, 0, rz), ((3, 3), (1, 2)), 1, 9230 + i * 4, ring=0)
    for side, sign in SIDES:
        for j, (y, z, n) in enumerate(((-7.6, -2.8, 5), (-7.4, -.2, 6))):
            strand(g, f"{side}_layer_{j}", (4.4 * sign, y, z), (0, 0, -(12 + j * 10) * sign), ((2, n), (1, 2)), 1,
                   9250 + j * 3 + (sign > 0), motion="sway" if j else "none")
        strand(g, f"{side}_flick", (4.5 * sign, -4.4, 2.0), (6, 0, -38 * sign), ((2, 3), (1, 2)), 1, 9258 + (sign > 0), ring=None)
    fall(g, "nape", [(-2.7, -6.0, 4.5, ((2, 10), (1, 3)), -2, 6), (-.9, -6.2, 4.85, ((3, 12), (2, 2), (1, 2)), -3, 2),
                     (.9, -6.2, 4.5, ((3, 11), (2, 2), (1, 2)), -3, -2), (2.7, -6.0, 4.85, ((2, 9), (1, 3)), -2, -6)], 9270,
         motion="sway")
