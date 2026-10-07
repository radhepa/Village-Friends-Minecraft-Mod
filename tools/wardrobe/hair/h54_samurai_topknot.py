"""Samurai Topknot: the pate shaved from the brow to the crown, the sides and back combed sleekly up,
tied at the crown, and the oiled queue folded forward along the shaved top."""
from anime_male import SIDES, chain, clump, combed_face, shave, tie
from paint import hair_face, k

META = {"name": "Samurai Topknot", "gender": "male",
        "description": "A shaved pate with the sides combed up, tied at the crown and the queue folded forward."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    # Shaved from the brow back to the crown; a rim of hair is left round the edges.
    hair_face(head.top, 5401, 2)
    shave(head.top, 5402, range(2, 8), cols=range(1, 7))
    for face in (head.right, head.left, head.back):
        combed_face(face, 5403 + face.x0, 2, sheen=1)
    shave(head.front, 5404, [0], cols=range(1, 7))
    head.front.set(0, 0, "H1"), head.front.set(7, 0, "H1")
    for face, rows in ((hat.right, 7), (hat.left, 7), (hat.back, 8)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows, face.name)
        combed_face(sub, 5405 + face.x0, 2, sheen=1)
    for y in range(8):
        hat.top.set(0, y, "H3"), hat.top.set(7, y, "H3")
    hat.top.hline(1, 6, 0, "H3"), hat.top.hline(1, 6, 1, "H2")
    # Sleek sides and back, combed up toward the knot.
    for side, sign in SIDES:
        for j, (z, length, tilt) in enumerate(((-1.2, 5, 2), (2.0, 6, 4))):
            wing = clump(g, f"{side}_side_{j}", (4.4 * sign + .1 * sign * j, -8.3, z), (1, length, 3), rotation=(0, 0, -tilt * sign),
                         seed=5410 + j * 3 + (sign > 0), ring=None)
            combed_face(wing.right if sign < 0 else wing.left, 5412 + j + (sign > 0), 2, sheen=0)
    for i, x in enumerate((-2.0, 2.0)):
        back = clump(g, f"back_{i}", (x, -8.4, 4.45), (4, 6, 1), seed=5415 + i, ring=None)
        combed_face(back.back, 5417 + i, 2, sheen=0)
    # The knot at the crown, its cord, and the queue folded forward over the pate.
    clump(g, "knot", (0, -8.2, 2.8), (3, 2, 3), origin=(-1.5, -2, -1.5), seed=5420, ring=0)
    tie(g, "cord", (0, -9.6, 2.5), (2, 1, 2), role="A", seed=5421)
    chain(g, "queue", (0, -9.9, 2.2), [(2, 4, 2, (-84, 0, 0)), (2, 2, 2, (-74, 0, 0)), (1, 2, 1, (-100, 0, 0))], seed=5425, ring=0)
