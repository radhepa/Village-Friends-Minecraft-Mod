"""Swept Undercut: clipped sides and a long top combed back into a lifted quiff."""
from paint import hair_box, k, rnd, scalp, shell

META = {"name": "Swept Undercut", "gender": "male", "description": "Close-clipped sides under a long top swept back into a quiff."}


def build(g):
    scalp(g, 601, side_rows=5, back_rows=7, sideburn=1)
    head = g.part("head")
    # Clipped sides and back: sparse, dark stubble texture rather than full hair.
    for face in (head.right, head.left, head.back):
        rows = 7 if face is head.back else 5
        for y in range(1 if face is not head.back else 3, rows):
            for x in range(face.w):
                face.set(x, y, "H0" if rnd(x, y, 602 + face.x0) < .5 else "H1")
    shell(g, 603, side_rows=1, back_rows=3, front=[(3, 1), (4, 1), (2, 1)])
    # Long top combed back: strands run front to back.
    top = g.piece("top_mass", "HEAD", (-3.5, -1, -4.2), (7, 1, 8), pivot=(0, -8.2, 0), rotation=(-5, 0, 0))
    hair_box(top, 610, 2, top_delta=1)
    for z in range(8):
        for x in range(7):
            top.top.set(x, z, k("H", 3 if x % 2 == 0 and (x + z) % 3 else 2))
    for f in top.sides:
        f.hline(0, f.w - 1, 0, "H3")
    # The quiff lifts at the front and rolls back.
    quiff = g.piece("quiff", "HEAD", (-3, -1, -1), (6, 1, 3), pivot=(.3, -9.0, -3.2), rotation=(26, 0, -4))
    hair_box(quiff, 620, 2, sheen_row=0, top_delta=2)
    for i, x in enumerate((-1.6, 1.6)):
        back = g.piece(f"swept_lock_{i}", "HEAD", (-1.5, -1, 0), (3, 1, 3), pivot=(x, -8.6, 1.4), rotation=(-16, 0, 6 if x < 0 else -6))
        hair_box(back, 640 + i, 2, top_delta=1)
    roll = g.piece("quiff_roll", "HEAD", (-2.5, -1, -1), (5, 1, 2), pivot=(.5, -9.9, -4.0), rotation=(46, 0, -6))
    hair_box(roll, 621, 3, top_delta=1)
