"""Wavy Crop: a short wavy top combed back from a lifted front wave, each lock rippling from side to
side, over neat short sides."""
from anime_male import SIDES, chain, clump, fade, hat_ring, taper, wave_face
from paint import scalp

META = {"name": "Wavy Crop", "gender": "male",
        "description": "A short wavy top rippling back from a lifted front wave, over neat short sides."}

LOCKS = [(-3.1, 0, 3), (-1.5, 1, 2), (.1, 0, 3), (1.7, 1, 2), (3.2, 0, 2)]


def build(g):
    scalp(g, 3801, side_rows=5, back_rows=7, sideburn=1)
    head = g.part("head")
    for face, rows in ((head.right, 5), (head.left, 5), (head.back, 7)):
        fade(face, 3802 + face.x0, rows - 2, rows - 1, base=1, start=.9, end=.5)
    hat = hat_ring(g, 3803, rows={"back": 5, "right": 3, "left": 3})
    wave_face(hat.top, 3804, 3)
    hat.front.hline(0, 7, 0, "H2")
    # Wave locks lying back over the crown, swinging side to side as they go.
    for i, (x, phase, w) in enumerate(LOCKS):
        swing = 14 if phase else -14
        chain(g, f"wave_{i}", (x, -9.0, -4.0),
              [(w, 3, 2, (122, swing, 0)), (w, 3, 1, (90, -swing, 0)), (w, 3, 1, (68, swing * .8, 0))],
              seed=3810 + i * 9, ring=1, painter=wave_face)
    for side, sign in SIDES:
        side_box = clump(g, f"{side}_side", (4.4 * sign, -8.3, .6), (1, 3, 6), seed=3850 + (sign > 0))
        wave_face(side_box.right if sign < 0 else side_box.left, 3852 + (sign > 0), 2)
    for i, (x, rz) in enumerate(((-2.4, 8), (0, 0), (2.4, -8))):
        taper(g, f"nape_{i}", (x, -6.4, 4.3), (4, 0, rz), ((2, 3, 1), (1, 1, 1)), seed=3860 + i * 3, ring=1, painter=wave_face)
