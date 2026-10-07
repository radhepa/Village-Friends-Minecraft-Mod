"""Floppy Fringe: short back and sides under a long top that flops forward over the front of the
head in heavy locks, the fringe stopping at the brows."""
from anime_male import chain, clipped, clipped_scalp, combed_face
from paint import hair_face

META = {"name": "Floppy Fringe", "gender": "male",
        "description": "Short back and sides under a long top flopping forward in heavy locks to the brows."}

# (x, root z, width, side lean)
LOCKS = [(-2.9, -.6, 2, 8), (-1.0, -1.2, 3, 3), (1.1, -.8, 3, -4), (3.0, -.2, 2, -9), (0, 1.6, 3, 0)]


def build(g):
    clipped_scalp(g, 7901, base=1, side_rows=6, back_rows=7, fade_rows=3, sideburn=1)
    head, hat = g.part("head"), g.part("hat")
    hair_face(head.top, 7902, 2)
    hair_face(hat.top, 7903, 3)
    for face in (hat.right, hat.left, hat.back):
        clipped(face, 7904 + face.x0, 2, rows=[0])
    hat.front.hline(0, 7, 0, "H2")
    # Locks from the crown, lying forward over the top and flopping down at the brow.
    for i, (x, z, w, lean) in enumerate(LOCKS):
        last = (1, 2, 1, (-12, 0, lean)) if i < 4 else (2, 1, 1, (-30, 0, lean))
        chain(g, f"flop_{i}", (x, -9.3 - (i % 2) * .2, z + .8),
              [(w, 4 if i < 4 else 2, 2, (-95, lean * .5, 0)), (w, 2, 1, (-38, 0, lean)), last],
              seed=7910 + i * 7, ring=1, overlap=.5)
    # The back of the crown, combed down to the short nape.
    back = g.piece("crown_back", "HEAD", (-3.5, -1, -1), (7, 2, 3), pivot=(0, -8.2, 2.6), rotation=(14, 0, 0))
    for f in back.faces:
        combed_face(f, 7950, 2 + (f is back.top))
