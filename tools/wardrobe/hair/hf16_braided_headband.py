"""Braided Headband: a plait laid over the crown from ear to ear like a headband, the rest worn long and loose."""
import math

from anime import ring_shell
from anime_female import fall, paint, points, strand, SIDES
from paint import scalp

META = {"name": "Braided Headband", "gender": "female",
        "description": "A plait laid over the crown from ear to ear, wispy bangs in front and long loose hair behind."}


def build(g):
    scalp(g, 6601, side_rows=7, back_rows=8, sideburn=0)
    ring_shell(g, 6602, side_rows=7, back_rows=8)
    # The plait follows an arc over the head, each lobe turned along it and nudged in or out in turn.
    for i, theta in enumerate((-80, -57, -34, -11, 11, 34, 57, 80)):
        t = math.radians(theta)
        r = 4.95 + (.25 if i % 2 else 0)
        lobe = g.piece(f"crown_braid_{i}", "HEAD", (-1, -1.1, -1), (2, 2, 2), pivot=(r * math.sin(t), -3.9 - r * math.cos(t), -2.5),
                       rotation=(0, 0, theta - 90 + (8 if i % 2 else -8)))
        paint(lobe, "plait", 6610 + i, 3, flip=bool(i % 2))
    points(g, "bang", [(-2.4, 3, 2, 2, 8), (0, 2, 2, 2, 0), (2.3, 3, 2, 2, -8)], 6620)
    for side, sign in SIDES:
        strand(g, f"{side}_wisp", (4.35 * sign, -6.6, -3.5), (0, 0, -3 * sign), ((1, 5), (1, 2)), 1, 6630 + (sign > 0))
        strand(g, f"{side}_side", (4.45 * sign, -7.0, 1.4), (0, 0, -3 * sign), ((1, 7),), 4, 6633 + (sign > 0))
    fall(g, "back", [(-3.3, -7.6, 4.3, ((3, 12), (2, 2), (1, 2)), -2, 4), (-1.1, -7.7, 4.65, ((3, 14), (2, 2), (1, 2)), -3, 1),
                     (1.1, -7.7, 4.3, ((3, 13), (2, 3), (1, 2)), -3, -1), (3.3, -7.6, 4.65, ((3, 11), (2, 2), (1, 2)), -2, -4)],
         6640, motion="sway")
