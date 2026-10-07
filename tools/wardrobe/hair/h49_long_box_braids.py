"""Long Box Braids: many slim braids from a sectioned, centre-parted crown, falling past the shoulders
in front and behind, a few finished with metal beads."""
from anime_male import SIDES, plait_face, taper, tie
from paint import k

META = {"name": "Long Box Braids", "gender": "male",
        "description": "Many slim braids from a centre-parted crown falling past the shoulders, some with beads."}


def sections(face, base=2, rows=8):
    for y in range(rows):
        for x in range(face.w):
            face.set(x, y, k("H", base - (1 if x % 3 == 2 or y % 3 == 2 else 0)))


def braid(g, pid, pivot, length, rotation, seed, bead=False, motion="none", tip=True):
    segs = ((2, length, 1), (1, 1, 1)) if tip else ((2, length, 1),)
    boxes = taper(g, pid, pivot, rotation, segs, seed=seed, painter=plait_face, motion=motion)
    if bead:
        tie(g, f"{pid}_bead", pivot, (1, 1, 1), rotation=rotation, origin=(-.5, length - .9, -.5), role="M", inflate=.25,
            motion=motion, seed=seed + 1)
    return boxes


def build(g):
    head, hat = g.part("head"), g.part("hat")
    sections(head.top)
    head.top.vline(3, 0, 7, "H0"), head.top.vline(4, 0, 7, "H0")
    for face in (head.right, head.left, head.back):
        sections(face, rows=8 if face is head.back else 7)
    head.front.hline(0, 7, 0, "H1")
    sections(hat.top, 3)
    hat.top.vline(3, 0, 7, "H1"), hat.top.vline(4, 0, 7, "H1")
    for face in (hat.right, hat.left, hat.back):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 6, face.name)
        sections(sub, rows=6)
    hat.front.hline(0, 7, 0, "H2")
    # Braids falling in front of the shoulders, framing the face from outside the cheeks.
    for side, sign in SIDES:
        for j, (z, length) in enumerate(((-3.6, 11), (-2.3, 12))):
            braid(g, f"{side}_front_{j}", (4.45 * sign, -7.8, z), length, (-4, 0, -(2 + j * 3) * sign), 4910 + j * 3 + (sign > 0) * 7,
                  bead=j == 0)
        for j, (z, length) in enumerate(((-.8, 12), (.8, 13), (2.4, 12))):
            braid(g, f"{side}_braid_{j}", (4.5 * sign, -7.8, z), length, ((j - 1) * 4 + 4, 0, -(4 + j * 2) * sign),
                  4930 + j * 3 + (sign > 0) * 7)
    for i, x in enumerate((-3.4, -2.0, -.7, .7, 2.0, 3.4)):
        braid(g, f"back_braid_{i}", (x, -7.6, 4.5), 13 + (i % 2), (8 + (i % 3) * 3, 0, -x * 1.6), 4960 + i * 3,
              bead=i in (1, 4), motion="sway", tip=False)
