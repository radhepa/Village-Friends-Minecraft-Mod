"""Afro Puff Fade: a rounded cushion of afro-textured hair on top, built from springy curl
clusters, over a high fade at the sides and nape and a crisp lined-up hairline."""
from anime_male import fade
from paint import curls_box, curls_face

META = {"name": "Afro Puff Fade", "gender": "male",
        "description": "A rounded afro-textured puff on top over a high fade and a crisp hairline."}

# (x, z, height): the centre rises highest so the cushion reads round.
PUFF = [(-2.6, -2.6, 3), (0, -2.8, 4), (2.6, -2.6, 3), (-2.8, 0, 4), (0, 0, 5), (2.8, 0, 4), (-2.6, 2.6, 3), (0, 2.8, 4), (2.6, 2.6, 3)]
RIM = [(0, -4.0, 0), (-4.0, 0, 90), (4.0, 0, 90), (0, 4.0, 0)]


def build(g):
    head, hat = g.part("head"), g.part("hat")
    curls_face(head.top, 4301)
    for face, rows in ((head.right, 5), (head.left, 5), (head.back, 6)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 2, face.name)
        curls_face(sub, 4302 + face.x0, 1)
        fade(face, 4303 + face.x0, 2, rows - 1, base=1, start=.7, end=.1)
    head.front.hline(0, 7, 0, "H1")
    head.front.set(0, 1, "H1"), head.front.set(7, 1, "H1")
    curls_face(hat.top, 4304, 3)
    for face in (hat.right, hat.left, hat.back, hat.front):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 1, face.name)
        curls_face(sub, 4305 + face.x0)
    for i, (x, z, h) in enumerate(PUFF):
        box = g.piece(f"puff_{i}", "HEAD", (-2, -h, -2), (4, h, 4), pivot=(x, -8.3, z), rotation=(0, (i * 17) % 24 - 12, 0))
        curls_box(box, 4310 + i * 3)
    for i, (x, z, ry) in enumerate(RIM):
        box = g.piece(f"rim_{i}", "HEAD", (-2, -3, -1), (4, 3, 2), pivot=(x, -8.2, z), rotation=(0, ry, 0))
        curls_box(box, 4350 + i * 3)
