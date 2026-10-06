"""Flower-Tucked Waves: shoulder-length waves, one side tucked behind the ear with a blossom slipped in."""
from anime import ring_shell
from anime_female import fall, flower, strand, wave_face, SIDES
from paint import scalp

META = {"name": "Flower-Tucked Waves", "gender": "female",
        "description": "Soft shoulder-length waves, one side tucked behind the ear with a flower tucked in."}

WAVE = ((2, 4), (2, 3, .5), (1, 2, -.2))


def build(g):
    scalp(g, 8401, side_rows=7, back_rows=8, sideburn=0, part=5)
    head = g.part("head")
    for y in range(3, 7):   # the tucked side shows the ear
        for x in range(0, 4):
            head.left.set(x, y, None)
    hat = ring_shell(g, 8402, side_rows=7, back_rows=8)
    for y in range(3, 7):
        for x in range(0, 4):
            hat.left.set(x, y, None)
    wave_face(hat.top, 8403, 3)
    strand(g, "sweep_0", (2.7, -8.7, -4.35), (-6, 0, 72), ((2, 5), (1, 1)), 1, 8410, ring=0, texture="wave")
    strand(g, "sweep_1", (1.1, -8.65, -4.35), (-6, 0, 60), ((2, 4), (1, 1)), 1, 8411, ring=0, texture="wave")
    # The open side: waves in front of and over the ear.
    strand(g, "right_front", (-4.35, -7.6, -3.1), (0, 0, 6), ((2, 4), (2, 3, -.5), (2, 2, .4), (1, 2)), 1, 8420, texture="wave")
    strand(g, "right_ear", (-4.45, -7.8, .4), (0, 0, 5), ((1, 7),), 4, 8421, texture="wave")
    # The tucked side: combed back over the ear, the flower in front of the tuck.
    strand(g, "left_tuck", (4.4, -7.8, 1.0), (24, 0, -3), ((2, 4), (2, 3, .4), (1, 2)), 1, 8422, texture="wave", motion="sway")
    strand(g, "left_top", (4.4, -7.9, -1.2), (0, 0, -2), ((1, 3),), 5, 8423, texture="wave", ring=0)
    flower(g, "blossom", (4.95, -6.6, -.6), facing="side")
    fall(g, "back", [(-3.0, -7.6, 4.3, WAVE + ((1, 1, .2),), 3, 6), (-1.0, -7.7, 4.75, ((3, 4), (3, 3, .6), (2, 3, -.3), (1, 1)), 4, 2),
                     (1.1, -7.6, 4.3, ((3, 4), (3, 3, -.5), (2, 3, .3), (1, 1)), 3, -2), (3.0, -7.7, 4.75, WAVE + ((1, 1, -.2),), 4, -6)],
         8430, motion="sway", texture="wave")
