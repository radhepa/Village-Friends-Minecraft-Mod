"""Half-Up Tail: the top half combed back and tied in a short tail at the back of the crown, the rest
left loose to the neck in pointed layers, two strands framing the face."""
from anime import ring_shell
from anime_male import SIDES, combed_face, plate, taper, tie
from paint import scalp

META = {"name": "Half-Up Tail", "gender": "male",
        "description": "The top half tied back in a short tail, the rest loose to the neck."}


def build(g):
    scalp(g, 5601, side_rows=7, back_rows=8, sideburn=1)
    hat = ring_shell(g, 5602, side_rows=6, back_rows=8)
    combed_face(hat.top, 5603, 3)
    # The top half, combed back to the tie.
    for i, (x, w) in enumerate(((-2.4, 3), (.4, 3), (2.7, 2))):
        plate(g, f"combed_{i}", (x, -8.3 - (i % 2) * .15, -.2), (w, 1, 8), rotation=(-6, 0, -x * 3), seed=5610 + i, sheen=2)
    tie(g, "tie", (0, -7.6, 4.7), (2, 2, 1), seed=5620)
    taper(g, "tail", (0, -7.9, 5.0), (14, 0, 0), ((2, 3, 2), (2, 2, 1), (1, 1, 1)), seed=5625, ring=0, motion="sway")
    # The loose lower half.
    for side, sign in SIDES:
        taper(g, f"{side}_frame", (4.35 * sign, -7.8, -3.3), (-3, 0, -4 * sign), ((1, 5, 1), (1, 2, 1)), seed=5640 + (sign > 0), ring=1)
        for j, (z, length, tilt) in enumerate(((-.8, 6, 5), (1.9, 6, 8))):
            taper(g, f"{side}_layer_{j}", (4.45 * sign, -7.2, z), (0, 0, -tilt * sign), ((2, length, 2), (1, 2, 1)),
                  seed=5650 + j * 3 + (sign > 0) * 7, ring=1)
    for i, (x, length, rz) in enumerate(((-3.0, 6, 8), (-1.0, 7, 3), (1.0, 7, -3), (3.0, 6, -8))):
        taper(g, f"back_{i}", (x, -6.0, 4.45), (6, 0, rz), ((2, length, 1), (1, 2, 1)), seed=5670 + i * 3, ring=1)
