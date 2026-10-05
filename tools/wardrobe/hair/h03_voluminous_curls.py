"""Voluminous Curls: a big stepped dome of tight curl clumps with a soft curly fringe."""
from paint import curls_box, curls_face, k, scalp, shell

META = {"name": "Voluminous Curls", "description": "A rounded cloud of tight curls, full at the crown and sides."}


def build(g):
    scalp(g, 201, side_rows=5, back_rows=8, sideburn=2)
    shell(g, 202, side_rows=5, back_rows=8, front=[(0, 1), (0, 2), (0, 3), (7, 1), (7, 2), (7, 3), (1, 1), (6, 1), (3, 1), (4, 1)])
    hat = g.part("hat")
    for face in (hat.top, hat.back, hat.right, hat.left):
        rows = {"top": 8, "back": 8, "right": 5, "left": 5}[face.name]
        for y in range(rows):
            for x in range(face.w):
                if face.get(x, y):
                    face.set(x, y, None)
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows, face.name)
        curls_face(sub, 203 + face.x0)
    # Stepped dome: each tier a little smaller, so the silhouette reads round.
    tiers = [((-5.5, -9.0, -5.5), (11, 3, 11)), ((-4.5, -11.0, -4.5), (9, 2, 9)), ((-3, -12.0, -3), (6, 1, 6))]
    for i, (origin, size) in enumerate(tiers):
        tier = g.piece(f"dome_{i}", "HEAD", origin, size)
        curls_box(tier, 210 + i)
    for side, x in (("right", -5.6), ("left", 4.4)):
        puff = g.piece(f"{side}_puff", "HEAD", (0, 0, -4.5), (1, 4, 9), pivot=(x, -7.0, 0))
        curls_box(puff, 220 + (side == "left"))
    back = g.piece("back_puff", "HEAD", (-5, 0, 0), (10, 5, 1), pivot=(0, -7.0, 4.4))
    curls_box(back, 230)
    # A soft curly fringe that stops above the brows.
    fringe = g.piece("fringe", "HEAD", (-5, 0, -1), (10, 2, 2), pivot=(0, -9.2, -4.3))
    curls_box(fringe, 240)
    for i, x in enumerate((-4.2, 2.2)):
        curl = g.piece(f"fringe_curl_{i}", "HEAD", (0, 0, -1), (2, 2, 2), pivot=(x, -7.6, -4.3))
        curls_box(curl, 241 + i)
