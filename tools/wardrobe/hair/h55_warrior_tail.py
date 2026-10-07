"""Wrapped Warrior Tail: the sides shaved high, the top dragged back into a tail tied high on the
crown and bound down its length with three leather wraps."""
from anime import cel_box
from anime_male import combed_face, plate, shave, tie
from paint import hair_face

META = {"name": "Wrapped Warrior Tail", "gender": "male",
        "description": "Shaved sides and a high tail bound down its length with leather wraps."}

# The tail, top to tip, all sharing one pivot so it swings as one: (width, height, depth) or a wrap.
TAIL = [(3, 2, 3), "wrap", (2, 3, 2), "wrap", (2, 3, 2), "wrap", (2, 3, 2), (1, 2, 1)]


def build(g):
    head, hat = g.part("head"), g.part("hat")
    hair_face(head.top, 5501, 2)
    for face in (head.right, head.left):
        hair_face(face, 5502 + face.x0, 2, rows=range(2))
        shave(face, 5503, range(2, 7))
    hair_face(head.back, 5504, 2, rows=range(3))
    shave(head.back, 5505, range(3, 7))
    head.front.hline(0, 7, 0, "H1")
    combed_face(hat.top, 5506, 3)
    for face in (hat.right, hat.left, hat.back):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 2, face.name)
        combed_face(sub, 5507 + face.x0, 2, across_y=True)
    hat.front.hline(0, 7, 0, "H2")
    # Dragged straight back over the crown.
    for i, (x, w) in enumerate(((-3.0, 2), (-1.0, 2), (1.0, 2), (3.0, 2))):
        plate(g, f"dragged_{i}", (x, -8.3 - (i % 2) * .15, -.6), (w, 1, 7), rotation=(-8, 0, -x * 3), seed=5510 + i, sheen=2)
    # The tail, tied high and wrapped.
    pivot, rotation, y = (0, -9.0, 4.0), (7, 0, 0), 0.0
    for i, part in enumerate(TAIL):
        if part == "wrap":
            tie(g, f"wrap_{i}", pivot, (2, 1, 2), rotation=rotation, origin=(-1, y, -1), inflate=.2, motion="sway", seed=5520 + i)
            y += 1
            continue
        w, h, d = part
        box = g.piece(f"tail_{i}", "HEAD", (-w / 2, y, -d / 2), part, pivot=pivot, rotation=rotation, motion="sway")
        cel_box(box, 5530 + i * 5, 2, 0 if i == 0 else None, top_delta=1 if i == 0 else 0)
        y += h
