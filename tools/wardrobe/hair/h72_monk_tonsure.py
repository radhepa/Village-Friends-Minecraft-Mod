"""Monk's Tonsure: the crown shaved in a wide circle, ringed by a soft band of short hair that falls
in small points round the brow, ears and nape; short hair below it."""
from anime_male import SIDES, combed_face, taper
from paint import hair_face, k

META = {"name": "Monk's Tonsure", "gender": "male",
        "description": "A wide shaved circle at the crown ringed by a soft band of short pointed hair."}

# The bald circle on the 8x8 crown (top face columns x, rows y).
BALD = {(x, y) for x in range(1, 7) for y in range(1, 7)} - {(1, 1), (6, 1), (1, 6), (6, 6)}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    hair_face(head.top, 7201, 2)
    for x, y in BALD:
        head.top.set(x, y, None)
    for face in (head.right, head.left, head.back):
        hair_face(face, 7203 + face.x0, 2, rows=range(7 if face is head.back else 6))
    head.front.hline(0, 7, 0, "H1")
    for y in range(8):
        for x in range(8):
            if (x, y) not in BALD and not (2 <= x <= 5 and 2 <= y <= 5):
                hat.top.set(x, y, k("H", 3 - (1 if (x + y) % 3 == 0 else 0)))
    for face in (hat.right, hat.left, hat.back):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 4, face.name)
        combed_face(sub, 7205 + face.x0, 2, sheen=0)
    hat.front.hline(0, 7, 0, "H2")
    # The ring: short soft points round the brow, the ears and the nape.
    for i, x in enumerate((-3.3, -1.65, 0, 1.65, 3.3)):
        taper(g, f"brow_{i}", (x, -8.45, -4.3), (-6, 0, 0), ((2, 1 + i % 2, 1), (1, 1, 1)), seed=7210 + i * 3, ring=0)
    for side, sign in SIDES:
        for j, z in enumerate((-2.6, .4, 3.2)):
            taper(g, f"{side}_{j}", (4.45 * sign, -8.3, z), (0, 0, -4 * sign), ((1, 3, 3), (1, 1, 1)), seed=7220 + j * 3 + (sign > 0) * 11,
                  ring=0)
    for i, x in enumerate((-2.6, 0, 2.6)):
        taper(g, f"back_{i}", (x, -8.3, 4.45), (4, 0, -x * 2), ((3, 3, 1), (1, 1, 1)), seed=7240 + i * 3, ring=0)
    # The rim of the ring standing just proud of the shaved circle.
    for i, (x, z, w, d) in enumerate(((0, -3.6, 8, 1), (0, 3.6, 8, 1), (-3.6, 0, 1, 6), (3.6, 0, 1, 6))):
        box = g.piece(f"rim_{i}", "HEAD", (-w / 2, -1, -d / 2), (w, 1, d), pivot=(x, -8.45, z))
        for f in box.faces:
            hair_face(f, 7260 + i, 2 + (f is box.top))
