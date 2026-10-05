"""Pointed Layers: short-to-medium hair in rings of pointed locks all around, a classic shonen look."""
from anime import back_fan, bangs, lock, ring_shell, spike
from paint import scalp

META = {"name": "Pointed Layers", "description": "Layered hair ending in points all the way around the head."}


def build(g):
    scalp(g, 1901, side_rows=6, back_rows=8, sideburn=2)
    ring_shell(g, 1902, side_rows=5, back_rows=8)
    bangs(g, "bang", [(-4.0, ((2, 3), (1, 2)), 14), (-2.0, ((2, 2), (1, 1)), 8), (0, ((2, 2), (1, 1)), 0), (2.0, ((2, 2), (1, 1)), -8),
                      (4.0, ((2, 3), (1, 2)), -14)], 1910)
    for side, sign in (("right", -1), ("left", 1)):
        for j, z in enumerate((-2.0, 0.4, 2.6)):
            lock(g, f"{side}_layer_{j}", (4.3 * sign, -7.4, z), (0, 0, -(5 + j * 2) * sign), ((2, 3), (1, 2)), 1, 1920 + j + (sign > 0) * 4)
    back_fan(g, "back", [(-3.2, ((2, 4), (1, 2)), 14, 12), (-1.1, ((2, 5), (1, 2)), 5, 10), (1.1, ((2, 5), (1, 2)), -5, 10),
                         (3.2, ((2, 4), (1, 2)), -14, 12)], 1940)
    for i, (x, z) in enumerate(((-1.8, 0), (1.8, 0), (0, 2.0))):
        spike(g, f"crown_{i}", (x, -8.1, z), (-12 - z * 8, 0, x * 8), ((3, 1), (2, 1)), 2, 1960 + i)
