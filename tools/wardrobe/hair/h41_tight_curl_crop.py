"""Tight Curl Crop: short, tight curls hugging the head in small clusters, a crisp lined-up hairline
and a low fade at the sides and nape."""
from anime_male import fade
from paint import curls_box, curls_face

META = {"name": "Tight Curl Crop", "gender": "male",
        "description": "Short tight curls in small clusters, a crisp hairline and a low fade."}

TOP = [(-2.6, -2.6, 1), (0, -2.8, 1), (2.6, -2.6, 1), (-2.8, 0, 1), (0, 0, 2), (2.8, 0, 1), (-2.6, 2.6, 1), (0, 2.8, 1), (2.6, 2.6, 1)]


def build(g):
    head, hat = g.part("head"), g.part("hat")
    curls_face(head.top, 4101)
    for face, rows in ((head.right, 6), (head.left, 6), (head.back, 7)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows - 2, face.name)
        curls_face(sub, 4102 + face.x0)
        fade(face, 4103 + face.x0, rows - 2, rows - 1, base=1, start=.7, end=.2)
    head.front.hline(0, 7, 0, "H1")
    head.front.set(0, 1, "H1"), head.front.set(7, 1, "H1")
    curls_face(hat.top, 4104, 3)
    for face, rows in ((hat.right, 3), (hat.left, 3), (hat.back, 4)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows, face.name)
        curls_face(sub, 4105 + face.x0)
    hat.front.hline(0, 7, 0, "H1")
    # Curl clusters over the crown, the middle one sitting highest.
    for i, (x, z, h) in enumerate(TOP):
        box = g.piece(f"curls_{i}", "HEAD", (-1.5, -h, -1.5), (3, h, 3), pivot=(x, -8.25 - (i % 2) * .15, z), rotation=(0, (i * 23) % 30 - 15, 0))
        curls_box(box, 4110 + i * 3)
    # Smaller clusters round the edges soften the outline.
    edges = [(-2.4, -4.3, 0), (0, -4.4, 0), (2.4, -4.3, 0), (-4.3, -1.4, 90), (-4.3, 1.8, 90), (4.3, -1.4, 90), (4.3, 1.8, 90),
             (-2.2, 4.3, 0), (2.2, 4.3, 0)]
    for i, (x, z, ry) in enumerate(edges):
        box = g.piece(f"edge_{i}", "HEAD", (-1, -1, -.5), (2, 2, 1), pivot=(x, -8.1, z), rotation=(0, ry, 0))
        curls_box(box, 4150 + i * 3)
