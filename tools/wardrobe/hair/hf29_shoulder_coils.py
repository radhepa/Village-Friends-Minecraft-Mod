"""Shoulder Coils: defined springy coils all around, falling to the shoulders, fuller at the crown."""
from anime import ring_shell
from anime_female import coil_face, paint, strand, SIDES
from paint import scalp

META = {"name": "Shoulder Coils", "gender": "female",
        "description": "Defined, springy coils falling to the shoulders, full at the crown with short coils at the brow."}


def coil(sign, n):
    """A thin coil that zigzags as it springs down."""
    return (1, n, 0, 2), (1, 3, .45 * sign, 2), (1, 2, -.35 * sign, 1)


def build(g):
    scalp(g, 7901, side_rows=8, back_rows=8, sideburn=0)
    head = g.part("head")
    for face in (head.top, head.back, head.right, head.left):
        coil_face(face, 7902 + face.x0, 2)
    for x in range(1, 7):
        head.front.set(x, 1, "X1")
    hat = ring_shell(g, 7903, side_rows=7, back_rows=8)
    coil_face(hat.top, 7904, 3)
    for i, (x, z, rz) in enumerate(((-2.0, -1.2, 12), (2.0, -1.0, -12), (0, 1.8, 0))):
        crown = g.piece(f"crown_{i}", "HEAD", (-2, -1.5, -2), (4, 2, 4), pivot=(x, -8.4, z), rotation=(-4, 0, rz))
        paint(crown, "coil", 7905 + i * 3, 2, top_delta=1)
    for i, (x, rz) in enumerate(((-2.2, 8), (.1, -2), (2.4, -10))):
        strand(g, f"brow_coil_{i}", (x, -8.6, -4.4), (-12, 0, rz), ((2, 2, 0, 2),), 1, 7910 + i, ring=None, texture="ringlet")
    # Side and back coils, each its own length and lean.
    for side, sign in SIDES:
        for j, (z, n, tilt) in enumerate(((-2.8, 3, 8), (-.2, 4, 13), (2.5, 4, 10))):
            strand(g, f"{side}_coil_{j}", (4.7 * sign, -7.2, z), (0, 0, -tilt * sign), coil(sign, n), 1,
                   7920 + j * 5 + (sign > 0), texture="ringlet", motion="sway" if j else "none")
    for i, (x, z, rz) in enumerate(((-3.0, 4.6, 10), (-1.0, 5.1, 3), (1.0, 4.6, -3), (3.0, 5.1, -10))):
        strand(g, f"back_coil_{i}", (x, -7.2, z), (6, 0, rz), coil(1 if i % 2 else -1, 4), 1, 7960 + i * 3, texture="ringlet",
               motion="sway")
