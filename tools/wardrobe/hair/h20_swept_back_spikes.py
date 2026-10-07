"""Swept-Back Spikes: hair raked back into backward-pointing spikes, two loose strands at the brow."""
from anime import lock, ring_shell, spike
from paint import scalp

META = {"name": "Swept-Back Spikes", "gender": "male", "description": "Hair raked back into tidy backward spikes, a couple of loose strands in front."}


def build(g):
    scalp(g, 2001, side_rows=4, back_rows=8, sideburn=2)
    ring_shell(g, 2002, side_rows=3, back_rows=7)
    for i, (x, z, length) in enumerate(((-2.4, -3.0, 3), (0, -3.4, 4), (2.4, -3.0, 3), (-1.2, -.6, 4), (1.2, -.6, 4), (-2.8, 1.8, 3),
                                        (0, 1.8, 3), (2.8, 1.8, 3))):
        segs = ((3, length - 2), (2, 1), (1, 1))
        spike(g, f"rake_{i}", (x, -8.0, z), (-62, 0, -x * 6), segs, 2, 2010 + i * 3)
    for side, sign in (("right", -1), ("left", 1)):
        spike(g, f"{side}_rake", (4.2 * sign, -7.0, -.5), (-60, 0, 20 * sign), ((2, 2), (1, 2)), 2, 2040 + (sign > 0))
    lock(g, "loose_strand_0", (-1.4, -8.6, -4.3), (-12, 0, 16), ((1, 2), (1, 1)), 1, 2050)
    lock(g, "loose_strand_1", (.6, -8.6, -4.3), (-12, 0, -10), ((1, 2),), 1, 2051)
