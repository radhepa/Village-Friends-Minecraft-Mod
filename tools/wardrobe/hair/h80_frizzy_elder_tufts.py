"""Frizzy Elder Tufts: a bald crown with a few stray hairs on top, and big frizzy puffs of hair
springing out over the ears and round the back."""
from anime_male import SIDES, taper
from paint import curls_box, curls_face

META = {"name": "Frizzy Elder Tufts", "gender": "male",
        "description": "A bald crown with stray hairs and big frizzy puffs springing out over the ears."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    for face, top in ((head.right, 2), (head.left, 2), (head.back, 2)):
        sub = type(face)(face.layer, face.x0, face.y0 + top, face.w, 7 - top, face.name)
        curls_face(sub, 8001 + face.x0, 2)
    for y in range(2, 5):
        head.right.set(7, y, None), head.left.set(0, y, None)
    for face, top in ((hat.right, 2), (hat.left, 2), (hat.back, 2)):
        sub = type(face)(face.layer, face.x0, face.y0 + top, face.w, 5, face.name)
        curls_face(sub, 8002 + face.x0, 2)
    # The puffs over the ears, springing out and up.
    for side, sign in SIDES:
        puffs = ((-6.8, -.9, (2, 3, 3), 20), (-7.6, 1.4, (3, 2, 3), 32), (-5.0, .8, (2, 2, 3), 8), (-6.2, 3.2, (2, 3, 2), 24))
        for j, (y, z, size, rz) in enumerate(puffs):
            w, h, d = size
            box = g.piece(f"{side}_puff_{j}", "HEAD", (0 if sign > 0 else -w, -h / 2, -d / 2), size, pivot=(4.1 * sign, y, z),
                          rotation=(0, 0, -rz * sign))
            curls_box(box, 8010 + j * 3 + (sign > 0) * 11)
    for i, x in enumerate((-2.2, 2.2)):
        box = g.piece(f"back_puff_{i}", "HEAD", (-2, -1.5, 0), (4, 3, 2), pivot=(x, -5.4, 4.1), rotation=(-12, 0, x * 5))
        curls_box(box, 8040 + i * 3)
    # A few stray hairs still standing on the crown.
    for i, (x, z, rx, rz) in enumerate(((-.8, -.6, -30, 40), (.6, .2, 34, -46), (0, 1.8, 50, 10))):
        taper(g, f"stray_{i}", (x, -8.0, z), (rx, 0, rz), ((1, 1, 1), (1, 1, 1)), seed=8050 + i * 3, ring=None, up=True)
