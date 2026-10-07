"""Sponge Coils: short springy coils standing all over the top in a loose staggered crop, the sides
cut close and faded."""
from anime_male import coil_face, fade, taper
from paint import curls_face

META = {"name": "Sponge Coils", "gender": "male",
        "description": "Short springy coils standing all over the top, over close faded sides."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    curls_face(head.top, 4401)
    for face, rows in ((head.right, 6), (head.left, 6), (head.back, 7)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows - 3, face.name)
        curls_face(sub, 4402 + face.x0, 1)
        fade(face, 4403 + face.x0, rows - 3, rows - 1, base=1, start=.75, end=.15)
    head.front.hline(0, 7, 0, "H1")
    curls_face(hat.top, 4404, 2)
    for face in (hat.right, hat.left, hat.back):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 2, face.name)
        curls_face(sub, 4405 + face.x0, 2)
    hat.front.hline(0, 7, 0, "H2")
    # Coils in a staggered grid, front ones leaning forward, outer ones leaning out.
    n = 0
    for row, z in enumerate((-3.2, -1.1, 1.0, 3.1)):
        xs = (-3.0, -1.0, 1.0, 3.0) if row % 2 == 0 else (-2.0, 0.0, 2.0)
        for x in xs:
            h = 2 + (n * 7 % 3 == 0)
            lean_x = 14 if z < -3 else -10 if z > 3 else (n * 5 % 9) - 4
            taper(g, f"coil_{n}", (x, -8.3, z), (lean_x, 0, -x * 4), ((2, h, 2),), seed=4410 + n * 3, up=True, painter=coil_face)
            n += 1
    for side, sign in (("right", -1), ("left", 1)):
        for j, z in enumerate((-2.0, 1.2)):
            taper(g, f"{side}_coil_{j}", (4.0 * sign, -7.9, z), (0, 0, -52 * sign), ((2, 2, 2),), seed=4480 + j + (sign > 0) * 5,
                  up=True, painter=coil_face)
