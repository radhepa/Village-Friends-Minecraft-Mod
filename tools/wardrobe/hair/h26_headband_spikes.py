"""Headband Spikes: spiky hair bursting over a cloth headband whose tails flutter behind."""
from anime import back_fan, lock, ring_shell, spike
from paint import scalp, solid

META = {"name": "Headband Spikes", "gender": "male", "description": "Spiky hair over a cloth headband, its knotted tails trailing behind."}


def build(g):
    scalp(g, 2601, side_rows=5, back_rows=8, sideburn=2)
    ring_shell(g, 2602, side_rows=4, back_rows=7)
    band = g.piece("headband", "HEAD", (-4.5, 0, -4.5), (9, 1, 9), pivot=(0, -7.7, 0), inflate=.12)
    solid(band, "A", "plain", 2610, 2, edge=False)
    for face in band.sides:
        face.hline(0, face.w - 1, 0, "A3")
    knot = g.piece("headband_knot", "HEAD", (-1, -1, -.5), (2, 2, 1), pivot=(0, -7.2, 4.9))
    solid(knot, "A", "plain", 2611, 2)
    for i, rz in enumerate((14, -10)):
        tail = g.piece(f"headband_tail_{i}", "HEAD", (-.5, 0, -.5), (1, 5, 1), pivot=(-.5 + i, -6.6, 5.0), rotation=(30, 0, rz), motion="sway")
        solid(tail, "A", "plain", 2612 + i, 2)
    for i, (x, z) in enumerate(((-3.0, -2.6), (-1.0, -3.2), (1.0, -3.2), (3.0, -2.6), (-2.2, 0), (0, -.4), (2.2, 0), (-1.2, 2.4), (1.2, 2.4))):
        spike(g, f"spike_{i}", (x, -8.0, z), (-(z + .6) * 10, 0, x * 9), ((3, 1), (2, 1), (1, 1)), 2, 2620 + i * 3)
    lock(g, "front_spike_0", (-1.6, -8.4, -4.4), (-30, 0, 18), ((2, 2), (1, 1)), 1, 2660, ring=None)
    lock(g, "front_spike_1", (1.4, -8.4, -4.4), (-30, 0, -18), ((2, 2), (1, 1)), 1, 2661, ring=None)
    back_fan(g, "nape", [(-2.4, ((2, 4), (1, 1)), 10, 14), (0, ((3, 4), (1, 2)), 0, 12), (2.4, ((2, 4), (1, 1)), -10, 14)], 2670, z=4.4)
