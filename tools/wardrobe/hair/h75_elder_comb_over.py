"""Elder's Comb-Over: a bald crown with a few long strands grown out from a low side part and combed
carefully across it, the scalp showing between them, a short fringe of hair round the sides and back."""
from anime_male import SIDES, chain, clump
from anime import cel_face
from paint import hair_face

META = {"name": "Elder's Comb-Over", "gender": "male",
        "description": "A few long strands combed across a bald crown from a low side part."}

# (z, thickness, length across): thin strands with scalp between them.
STRANDS = [(-2.9, 1, 8), (-1.3, 1, 9), (.4, 1, 9), (2.1, 1, 8)]


def build(g):
    head, hat = g.part("head"), g.part("hat")
    for face, top in ((head.right, 2), (head.left, 1), (head.back, 1)):
        hair_face(face, 7501 + face.x0, 2, rows=range(top, 7))
    for face, top in ((hat.right, 3), (hat.left, 2), (hat.back, 2)):
        sub = type(face)(face.layer, face.x0, face.y0 + top, face.w, 4, face.name)
        cel_face(sub, 7502 + face.x0, 2, 0, tip_dark=False)
    # The low part sits just above the wearer's left ear; the strands are combed over to the right.
    for i, (z, thick, length) in enumerate(STRANDS):
        chain(g, f"strand_{i}", (4.3, -6.8 - (i % 2) * .1, z), [(thick, 2, 1, (0, 0, 152)), (thick, length, 1, (0, 0, 91)),
                                                                 (1, 1, 1, (0, 0, 40))], seed=7510 + i * 7, ring=1, overlap=.4)
    for side, sign in SIDES:
        clump(g, f"{side}_ear", (4.45 * sign, -6.0, 1.0), (1, 3, 4), rotation=(0, 0, -5 * sign), seed=7530 + (sign > 0), ring=0)
    for i, x in enumerate((-2.0, 2.0)):
        clump(g, f"back_{i}", (x, -6.6, 4.45), (4, 4, 1), rotation=(5, 0, 0), seed=7540 + i, ring=0)
