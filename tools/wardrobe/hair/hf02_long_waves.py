"""Long Waves: side-parted hair in soft waves to mid-back, a wavy swept fringe and rippling side locks."""
from anime import ring_shell
from anime_female import fall, strand, wave_face, SIDES
from paint import scalp

META = {"name": "Long Waves", "gender": "female",
        "description": "Soft side-parted waves to mid-back, with a wavy fringe swept across the brow."}


def build(g):
    scalp(g, 5201, side_rows=7, back_rows=8, sideburn=0, part=5)
    hat = ring_shell(g, 5202, side_rows=7, back_rows=8)
    wave_face(hat.top, 5203, 3)
    hat.top.vline(5, 0, 7, "H1")
    # The fringe sweeps from the part toward the wearer's right temple.
    strand(g, "sweep_0", (2.6, -8.7, -4.35), (-6, 0, 70), ((2, 5), (1, 1)), 1, 5210, ring=0, texture="wave")
    strand(g, "sweep_1", (1.0, -8.65, -4.35), (-6, 0, 58), ((2, 4), (1, 1)), 1, 5211, ring=0, texture="wave")
    for side, sign in SIDES:
        # In front of the shoulder, over the ear, and behind the shoulder: each wave a different length.
        strand(g, f"{side}_front", (4.35 * sign, -7.6, -3.0), (0, 0, -(6 if sign < 0 else 3) * sign),
               ((2, 5), (2, 4, .6 * sign), (1, 3, -.3 * sign)), 1, 5220 + (sign > 0), texture="wave")
        strand(g, f"{side}_ear", (4.4 * sign, -7.8, .4), (0, 0, -4 * sign), ((1, 7),), 4, 5224 + (sign > 0), texture="wave")
        strand(g, f"{side}_rear", (4.0 * sign, -7.6, 3.0), (3, 0, -7 * sign),
               ((2, 6), (2, 4, -.6 * sign), (1, 3, .3 * sign)), 1, 5226 + (sign > 0), motion="sway", texture="wave")
    fall(g, "back", [(-2.6, -7.6, 4.3, ((3, 6), (3, 5, .7), (1, 3, -.3)), 5, 5),
                     (-.6, -7.7, 4.8, ((3, 7), (2, 5, -.6), (1, 3, .2)), 7, 1),
                     (1.4, -7.6, 4.35, ((3, 7), (3, 4, .6), (1, 3, -.2)), 4, -2),
                     (3.0, -7.7, 4.85, ((2, 6), (2, 5, -.7), (1, 2, .3)), 6, -6)], 5240, motion="sway", texture="wave")
