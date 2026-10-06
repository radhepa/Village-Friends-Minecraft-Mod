"""Undercut Curtains: clipped sides and nape under a long centre-parted top that falls as curtains."""
from anime import cel_box, lock
from paint import hair_face, rnd, scalp, shell

META = {"name": "Undercut Curtains", "gender": "male", "description": "A clipped undercut beneath long centre-parted curtains."}


def build(g):
    scalp(g, 2301, side_rows=5, back_rows=7, sideburn=1, part=3)
    head = g.part("head")
    for face in (head.right, head.left, head.back):
        for y in range(2 if face is not head.back else 4, 5 if face is not head.back else 7):
            for x in range(face.w):
                face.set(x, y, "H0" if rnd(x, y, 2302 + face.x0) < .5 else "H1")
    shell(g, 2303, side_rows=1, back_rows=3, front=[(2, 1), (5, 1)])
    for side, sign in (("right", -1), ("left", 1)):
        top = g.piece(f"{side}_top", "HEAD", (-2.1, -1, -4.4), (4, 1, 9), pivot=(2.0 * sign, -8.1, .1), rotation=(0, 0, 10 * sign))
        cel_box(top, 2310 + (sign > 0), ring=0)
        lock(g, f"{side}_curtain", (.4 * sign, -8.7, -4.35), (-8, 0, 50 * -sign), ((2, 4), (1, 1)), 1, 2320 + (sign > 0), ring=None)
        lock(g, f"{side}_tip", (4.15 * sign, -7.9, -3.9), (0, 0, -8 * sign), ((2, 3), (1, 1)), 1, 2325 + (sign > 0))
    back = g.piece("crown_back", "HEAD", (-3.5, -1, 0), (7, 2, 2), pivot=(0, -7.8, 3.6), rotation=(18, 0, 0))
    cel_box(back, 2330, ring=0)
