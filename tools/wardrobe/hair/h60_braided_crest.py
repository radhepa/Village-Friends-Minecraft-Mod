"""Braided Crest: the sides shaved, the strip of hair down the middle plaited into one thick braid
that runs from the brow over the crown and hangs down the back as a tied tail."""
from anime import cel_face
from anime_male import chain, plait, plait_face, shave, taper
from paint import hair_face, k

META = {"name": "Braided Crest", "gender": "male",
        "description": "Shaved sides and one thick braid running from the brow over the crown to a tail."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    shave(head.top, 6001, range(8))
    for face in (head.right, head.left):
        shave(face, 6002 + face.x0, range(7))
    shave(head.back, 6004, range(7))
    shave(head.front, 6005, [0], cols=[0, 1, 6, 7])
    hair_face(head.top, 6006, 1, cols=range(2, 6))
    hair_face(head.back, 6007, 1, cols=range(2, 6), rows=range(6))
    head.front.hline(2, 5, 0, "H1")
    for y in range(8):
        for x in range(2, 6):
            hat.top.set(x, y, k("H", 2 - (1 if (x + y) % 2 == 0 else 0)))
    strip = type(hat.back)(hat.layer, hat.back.x0 + 2, hat.back.y0, 4, 6, "back")
    cel_face(strip, 6008, 2, None, tip_dark=False)
    # A wisp left loose where the braid begins at the hairline.
    taper(g, "wisp", (-.6, -8.6, -4.3), (-10, 0, 12), ((2, 2, 1), (1, 1, 1)), seed=6010, ring=0)
    # The braid over the crown, hugging the head round the back corner.
    chain(g, "braid", (0, -9.1, -3.9),
          [(3, 3, 2, (98, 0, 0)), (3, 3, 2, (90, 0, 0)), (3, 3, 2, (68, 0, 0)), (3, 2, 2, (32, 0, 0)), (3, 3, 2, (8, 0, 0))],
          seed=6020, painter=plait_face, overlap=.45)
    plait(g, "tail", (0, -2.3, 5.0), 4, rotation=(6, 0, 0), width=2, depth=2, seed=6040, tie_role="L", tuft=2, motion="sway")
