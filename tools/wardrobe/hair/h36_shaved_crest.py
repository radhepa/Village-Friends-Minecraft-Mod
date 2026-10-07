"""Shaved-Side Crest: sides and nape shaved to stubble, a strip of hair down the middle laid back in
long locks that arc over the crown and fall to points at the nape."""
from anime import cel_face
from anime_male import chain, shave, taper
from paint import hair_face, k

META = {"name": "Shaved-Side Crest", "gender": "male",
        "description": "Shaved sides under a strip of long locks laid back over the crown to points at the nape."}

# (x, width, drop): the middle lock rides highest.
CREST = [(0, 3, 0.0), (-1.9, 2, .35), (1.9, 2, .35)]


def build(g):
    head, hat = g.part("head"), g.part("hat")
    shave(head.top, 3601, range(8))
    for face in (head.right, head.left):
        shave(face, 3602 + face.x0, range(7))
    shave(head.back, 3604, range(7))
    shave(head.front, 3605, [0], cols=[0, 1, 6, 7])
    # The crest strip on the scalp and the hat layer.
    hair_face(head.top, 3606, 2, cols=range(2, 6))
    hair_face(head.back, 3607, 2, cols=range(2, 6), rows=range(7))
    head.front.hline(2, 5, 0, "H1")
    for y in range(8):
        for x in range(2, 6):
            hat.top.set(x, y, k("H", 3 - (1 if (x + y) % 3 == 0 else 0)))
    strip = type(hat.back)(hat.layer, hat.back.x0 + 2, hat.back.y0, 4, 7, "back")
    cel_face(strip, 3608, 2, 1, tip_dark=False)
    hat.front.hline(2, 5, 0, "H2")
    # Long locks lifting off the hairline, laid back over the crown and down the back of the head.
    for i, (x, w, drop) in enumerate(CREST):
        segs = [(w, 3, 2, (100, 0, 0)), (w, 4, 2, (90, 0, 0)), (w, 3, 2, (48, 0, 0)), (w, 3, 2, (10, 0, 0)),
                (max(1, w - 1), 3, 1, (2, 0, 0))]
        chain(g, f"crest_{i}", (x, -8.85 + drop, -4.1), segs, seed=3610 + i * 11, ring=1)
    # Short layers shingled along the top break up the ridge.
    for i, (z, rx) in enumerate(((-.9, -78), (1.6, -82))):
        taper(g, f"layer_{i}", (0, -10.3, z), (rx, 0, 0), ((3, 2, 1), (1, 1, 1)), seed=3660 + i * 3, ring=0, up=True)
