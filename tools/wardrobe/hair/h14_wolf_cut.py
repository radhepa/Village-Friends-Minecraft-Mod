"""Wolf Cut: choppy pointed layers, flicked-out sides and a longer pointed nape."""
from anime import back_fan, bangs, lock, ring_shell, spike
from paint import scalp

META = {"name": "Wolf Cut", "description": "Shaggy pointed layers with outward flicks and a longer nape."}


def build(g):
    scalp(g, 1401, side_rows=6, back_rows=8, sideburn=2)
    ring_shell(g, 1402, side_rows=5, back_rows=8)
    bangs(g, "bang", [(-3.9, ((2, 3), (1, 2)), 12), (-1.6, ((2, 2), (1, 1)), 8), (0.6, ((3, 2), (1, 1)), -4), (2.6, ((2, 2), (1, 1)), -14)], 1410)
    for i, (x, z) in enumerate(((-2.0, -.8), (1.2, -1.2), (-.6, 1.6), (2.4, 1.4))):
        spike(g, f"crown_{i}", (x, -8.1, z), (-(z + 1) * 10 - 10, 0, x * 9), ((3, 1), (2, 1)), 2, 1420 + i)
    for side, sign in (("right", -1), ("left", 1)):
        for j, (y, z) in enumerate(((-5.5, -1.5), (-4.0, 1.0))):
            lock(g, f"{side}_flick_{j}", (4.3 * sign, y, z), (0, 0, -36 * sign), ((2, 2), (1, 2)), 2, 1440 + j + (sign > 0) * 3)
    back_fan(g, "mullet", [(-2.6, ((2, 6), (1, 2)), 14, 6), (0, ((3, 7), (2, 1), (1, 1)), 0, 4), (2.6, ((2, 6), (1, 2)), -14, 6)], 1460)
