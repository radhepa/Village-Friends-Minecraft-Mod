"""Village Mullet: short and textured on top, cropped close at the sides with long sideburns, and a
long straight fall at the back reaching the shoulders."""
from anime_male import clump, clipped, fade, taper
from paint import hair_face, k, scalp

META = {"name": "Village Mullet", "gender": "male",
        "description": "Short and textured on top, cropped sides, and a long straight fall to the shoulders behind."}


def build(g):
    scalp(g, 6401, side_rows=6, back_rows=8, sideburn=2)
    head, hat = g.part("head"), g.part("hat")
    for face in (head.right, head.left):
        fade(face, 6402 + face.x0, 3, 5, base=1, start=.9, end=.5)
    hair_face(hat.top, 6403, 3)
    for face in (hat.right, hat.left):
        clipped(face, 6404 + face.x0, 2, rows=[0, 1])
    sub = type(hat.back)(hat.layer, hat.back.x0, hat.back.y0, 8, 8, "back")
    hair_face(sub, 6405, 2, sheen_row=1)
    hat.front.hline(0, 7, 0, "H2")
    # Short textured tufts on top.
    for i, (x, z, rx, rz) in enumerate(((-2.3, -2.2, 10, 12), (.3, -2.6, 14, -6), (2.6, -1.8, 8, -14), (-1.4, .8, -8, 10), (1.6, 1.0, -10, -8))):
        clump(g, f"tuft_{i}", (x, -8.35, z), (3, 1, 3), rotation=(rx, 0, rz), origin=(-1.5, -1, -1.5), seed=6410 + i, top_delta=2)
    for i, (x, rz) in enumerate(((-2.2, 8), (0, -2), (2.2, -10))):
        taper(g, f"fringe_{i}", (x, -8.5, -4.3), (-12, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=6420 + i * 3, ring=0)
    # The long fall at the back.
    back = clump(g, "fall_root", (0, -7.6, 4.45), (8, 4, 1), origin=(-4, 0, -.5), seed=6430, ring=1)
    for x in range(8):
        back.back.set(x, 3, k("H", 1 + (x % 2)))
    for i, (x, length, rz) in enumerate(((-3.0, 7, 4), (-1.0, 8, 1), (1.0, 8, -1), (3.0, 7, -4))):
        taper(g, f"fall_{i}", (x, -4.2, 4.55), (5, 0, rz), ((2, length, 1), (1, 2, 1)), seed=6440 + i * 3, ring=None, motion="sway")
