"""Spiky Layered: tapered spikes fanning out from the crown, forward fringe points and a layered nape."""
from paint import hair_box, scalp, shell

META = {"name": "Spiky Layered", "gender": "male", "description": "Stepped spikes radiating from the crown over a layered nape."}

# (pivot x, pivot z, size, tilt scale)
CROWN = [(-2.6, -2.4, (2, 3, 2)), (0, -2.8, (2, 4, 2)), (2.6, -2.4, (2, 3, 2)),
         (-3.2, .4, (2, 3, 2)), (-.6, -.2, (2, 4, 2)), (1.6, .4, (2, 3, 2)), (3.4, .2, (2, 2, 2)),
         (-2.2, 2.8, (2, 3, 2)), (.6, 2.6, (2, 3, 2)), (2.8, 3.0, (2, 2, 2))]


def build(g):
    scalp(g, 101, side_rows=4, back_rows=8, sideburn=2)
    shell(g, 102, side_rows=3, back_rows=7, front=[(0, 1), (0, 2), (7, 1), (7, 2), (3, 1), (4, 1)])
    for i, (x, z, size) in enumerate(CROWN):
        w, h, d = size
        spike = g.piece(f"crown_spike_{i}", "HEAD", (-w / 2, -h, -d / 2), size, pivot=(x, -7.7, z),
                        rotation=(-z * 9, 0, x * 8))
        hair_box(spike, 110 + i, 2, sheen_row=1, top_delta=2)
    # Fringe points flicking forward over the brow line.
    for i, (x, rz) in enumerate(((-2.6, 10), (-.2, -4), (2.2, -12))):
        tip = g.piece(f"fringe_spike_{i}", "HEAD", (-1, 0, -1), (2, 2, 1), pivot=(x, -8.3, -4.25), rotation=(-28, 0, rz))
        hair_box(tip, 130 + i, 2)
    # Side spikes over the ears and layered points at the nape.
    for side, x, rz in (("right", -4.5, -22), ("left", 4.5, 22)):
        for j, z in enumerate((-1.6, 1.2)):
            lock = g.piece(f"{side}_spike_{j}", "HEAD", (-.5, -.5, -1), (1, 4, 2), pivot=(x, -7.0, z), rotation=(0, 0, rz))
            hair_box(lock, 140 + j + (0 if side == "right" else 5), 2, sheen_row=0)
    for i, (x, length, rz) in enumerate(((-3.0, 4, 10), (0, 5, 0), (3.0, 4, -10))):
        nape = g.piece(f"nape_spike_{i}", "HEAD", (-1, 0, -.5), (2, length, 1), pivot=(x, -4.5, 4.3), rotation=(22, 0, rz))
        hair_box(nape, 150 + i, 2, sheen_row=0)
