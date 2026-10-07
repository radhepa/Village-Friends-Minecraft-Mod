"""Norse Side Braids: two braids plaited flat along each side of the head over close-cut sides, the
long top combed back and falling down the back, the side braids hanging free behind the ears."""
from anime import cel_face
from anime_male import SIDES, clipped, cornrow, plait, plate, taper
from paint import hair_face

META = {"name": "Norse Side Braids", "gender": "male",
        "description": "Braids plaited flat along close-cut sides, the long top combed back down the back."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    hair_face(head.top, 7101, 2)
    for face in (head.right, head.left):
        clipped(face, 7102 + face.x0, 1, rows=range(7))
    hair_face(head.back, 7103, 2)
    head.front.hline(0, 7, 0, "H1")
    hair_face(hat.top, 7104, 3)
    sub = type(hat.back)(hat.layer, hat.back.x0, hat.back.y0, 8, 8, "back")
    cel_face(sub, 7105, 2, 1, tip_dark=False)
    hat.front.hline(1, 6, 0, "H2")
    # Two braids flat along each side, from the temple back toward the nape.
    for side, sign in SIDES:
        for j, (y, yaw) in enumerate(((-7.3, 0), (-5.6, -4))):
            cornrow(g, f"{side}_braid_{j}", (4.0 * sign, y, -3.4), 7, rotation=(0, yaw * sign, 90 * sign), width=1,
                    seed=7110 + j * 5 + (sign > 0) * 3, phase=j)
        plait(g, f"{side}_free", (3.6 * sign, -5.0, 4.4), 6, rotation=(6, 0, -4 * sign), width=1, depth=1, seed=7130 + (sign > 0) * 5,
              tie_role="M", tuft=2, motion="sway")
    # The long top, combed straight back and down.
    for i, x in enumerate((-2.0, 0, 2.0)):
        plate(g, f"top_{i}", (x, -8.3 - (i % 2) * .15, -.6), (2, 1, 7), rotation=(-6, 0, -x * 2), seed=7150 + i, sheen=2)
    for i, (x, length, rz) in enumerate(((-1.9, 10, 3), (0, 11, 0), (1.9, 10, -3))):
        taper(g, f"back_{i}", (x, -7.8, 4.55), (5, 0, rz), ((2, length, 1), (1, 2, 1)), seed=7160 + i * 3, ring=1, motion="sway")
