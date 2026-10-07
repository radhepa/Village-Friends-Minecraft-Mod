"""Horseshoe Balding: the crown bald and bare, a horseshoe of soft, slightly fluffy hair left round
the sides and back, a little fuller over the ears."""
from anime_male import SIDES, clump, taper
from anime import cel_face
from paint import hair_face

META = {"name": "Horseshoe Balding", "gender": "male",
        "description": "A bald crown with a horseshoe of soft hair round the sides and back."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    for face, top in ((head.right, 2), (head.left, 2), (head.back, 1)):
        hair_face(face, 7401 + face.x0, 2, rows=range(top, 7))
    for y in range(2, 5):   # no hair in front of the ears' tops at the temple
        head.right.set(7, y, None), head.left.set(0, y, None)
    for face, top in ((hat.right, 3), (hat.left, 3), (hat.back, 2)):
        sub = type(face)(face.layer, face.x0, face.y0 + top, face.w, 4, face.name)
        cel_face(sub, 7402 + face.x0, 2, 0, tip_dark=False)
    for y in range(3, 7):
        hat.right.set(7, y, None), hat.left.set(0, y, None)
    # Soft fullness over the ears and round the back.
    for side, sign in SIDES:
        for j, (z, h) in enumerate(((-.6, 4), (2.2, 4))):
            clump(g, f"{side}_tuft_{j}", (4.45 * sign, -6.4, z), (1, h, 3), rotation=(0, 0, -6 * sign), seed=7410 + j + (sign > 0) * 3,
                  ring=0)
    for i, x in enumerate((-2.6, 0, 2.6)):
        clump(g, f"back_{i}", (x, -6.9, 4.45), (3, 5, 1), rotation=(6, 0, -x * 2), seed=7430 + i * 3, ring=0)
    for i, x in enumerate((-1.3, 1.3)):
        taper(g, f"nape_{i}", (x, -2.4, 4.5), (6, 0, -x * 4), ((2, 2, 1), (1, 1, 1)), seed=7440 + i * 3, ring=None)
