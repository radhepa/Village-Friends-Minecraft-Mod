"""Steppe Loops: a shaved crown with a small forelock, the hair left long behind the ears and
plaited into a looped braid on each side, a short braid hanging at the nape."""
from anime import cel_face
from anime_male import SIDES, chain, clump, plait, plait_face, shave, taper, tie
from paint import hair_face

META = {"name": "Steppe Loops", "gender": "male",
        "description": "A shaved crown and forelock, with the hair behind the ears plaited into a loop on each side."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    shave(head.top, 4001, range(8))
    hair_face(head.top, 4002, 2, rows=range(5, 8), cols=range(3, 5))
    shave(head.front, 4003, [0], cols=[0, 1, 2, 5, 6, 7])
    head.front.hline(3, 4, 0, "H1")
    # Long behind the ears and across the back; shaved above and in front of the ears.
    shave(head.right, 4004, range(8), cols=range(3, 8))
    shave(head.left, 4005, range(8), cols=range(0, 5))
    shave(head.right, 4006, range(3), cols=range(0, 3))
    shave(head.left, 4007, range(3), cols=range(5, 8))
    shave(head.back, 4008, range(3))
    hair_face(head.right, 4009, 2, rows=range(3, 8), cols=range(0, 3))
    hair_face(head.left, 4010, 2, rows=range(3, 8), cols=range(5, 8))
    hair_face(head.back, 4011, 2, rows=range(3, 8))
    for name, cols in (("right", range(0, 3)), ("left", range(5, 8)), ("back", range(8))):
        face = getattr(hat, name)
        sub = type(face)(face.layer, face.x0 + cols[0], face.y0 + 3, len(cols), 4, name)
        cel_face(sub, 4012 + face.x0, 2, 0, tip_dark=False)
    # The forelock: one small lock left at the hairline.
    taper(g, "forelock", (0, -8.4, -4.3), (-8, 0, 4), ((2, 2, 1), (1, 1, 1)), seed=4020, ring=0)
    # Each side is plaited and the braid looped back up on itself, bound where it meets.
    for side, sign in SIDES:
        clump(g, f"{side}_root", (4.4 * sign, -5.6, 2.3), (1, 2, 4), seed=4030 + (sign > 0), ring=0)
        chain(g, f"{side}_loop", (4.75 * sign, -5.2, 1.4),
              [(2, 6, 1, (0, 0, 0)), (2, 3, 1, (90, 0, 0)), (2, 5, 1, (180, 0, 0))], seed=4040 + (sign > 0) * 9,
              painter=plait_face, overlap=.5)
        tie(g, f"{side}_loop_tie", (4.75 * sign, -3.7, 3.4), (2, 1, 1), seed=4060 + (sign > 0))
    # A short braid at the nape.
    clump(g, "nape", (0, -5.0, 4.35), (6, 3, 1), seed=4070, ring=0)
    plait(g, "nape_braid", (0, -2.6, 4.7), 4, rotation=(6, 0, 0), seed=4075, motion="sway")
