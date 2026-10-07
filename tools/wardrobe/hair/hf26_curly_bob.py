"""Curly Bob: a chin-length bob of springy curls, a curly crown and short curled bangs."""
from anime import ring_shell
from anime_female import bubble_face, fringe, paint, strand, SIDES
from paint import scalp

META = {"name": "Curly Bob", "gender": "female",
        "description": "A chin-length bob of springy curls with a rounded curly crown and short curled bangs."}


def curl(sign, length):
    """A short corkscrew: segments stepping out and back."""
    return (2, length, 0, 2), (2, 2, .5 * sign, 2), (1, 2, -.2 * sign, 1)


def build(g):
    scalp(g, 7601, side_rows=8, back_rows=8, sideburn=0)
    hat = ring_shell(g, 7602, side_rows=7, back_rows=8)
    bubble_face(hat.top, 7603, 3)
    for i, (x, z, rz) in enumerate(((-2.4, -1.4, 14), (2.4, -1.2, -14), (0, 1.6, 0))):
        crown = g.piece(f"crown_{i}", "HEAD", (-2, -1.5, -2), (4, 2, 4), pivot=(x, -8.3, z), rotation=(-6, 0, rz))
        paint(crown, "bubble", 7605 + i, 2, top_delta=1)
    fringe(g, "bang", [(-2.6, ((3, 2),), 10), (-.2, ((3, 2),), -2), (2.3, ((3, 2),), -12)], 7610, texture="ringlet")
    for side, sign in SIDES:
        for j, (z, n, tilt) in enumerate(((-2.7, 4, 10), (-.3, 5, 14), (2.2, 4, 12))):
            strand(g, f"{side}_curl_{j}", (4.6 * sign, -7.4, z), (0, 0, -tilt * sign), curl(sign, n), 1, 7620 + j * 5 + (sign > 0),
                   texture="ringlet")
    for i, (x, z, rz, n) in enumerate(((-3.2, 4.4, 14, 4), (-1.1, 4.9, 4, 5), (1.1, 4.4, -4, 5), (3.2, 4.9, -14, 4))):
        strand(g, f"back_curl_{i}", (x, -7.4, z), (6, 0, rz), curl(1 if i % 2 else -1, n), 1, 7650 + i * 3, texture="ringlet")
