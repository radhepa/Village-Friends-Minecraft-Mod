"""Net Mender's Shuttle Bodice: a laced work bodice with a netting shuttle tucked in the lacing and a
length of mended net folded over her forearm, cork floats dangling from its edge."""
from kit_f03 import net, net_box
from kit_female import bodice, chemise, lacing
from paint import solid

META = {
    "name": "Net Mender's Shuttle Bodice",
    "gender": "female",
    "description": "A ladder-laced work bodice with a wooden netting shuttle tucked in the lacing and a fold of mended net over her forearm.",
    "tags": ["sea", "work"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 53001, neckline="round", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2")                               # a tied cuff, sleeve pushed back
        arm.strip.hline(0, 15, 10, "S4")
        arm.front.vline(2, 1, 7, "S2")
    b = bodice(g, "P", "twill", 53002, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "ladder", lace="S4", under="P0", eyelet="M3")
    for face in (b.front, b.back):
        face.hline(0, 7, 9, "P1")
    for face in (b.right, b.left):
        net(face, "P3", "P1", 4, 0, 4, 4, 5)                          # a darned side panel, netted in twine
    # The netting shuttle: a long wooden needle wound with twine, tucked down the lacing.
    shuttle = g.piece("netting_shuttle", "TORSO", (-.5, -3, -.5), (1, 5, 1), pivot=(1.6, 4.4, -2.75), rotation=(0, 0, -8))
    solid(shuttle, "L", "smooth", 53003, 3, edge=False)
    shuttle.front.set(0, 0, "L4"), shuttle.front.set(0, 4, "L2")
    for f in shuttle.sides:
        f.set(0, 1, "S4"), f.set(0, 2, "S3"), f.set(0, 3, "S4")      # twine wound on the tongue
    gauge = g.piece("mesh_gauge", "TORSO", (-.5, -2, -.5), (1, 3, 1), pivot=(2.6, 4.6, -2.7), rotation=(0, 0, 6))
    solid(gauge, "L", "smooth", 53004, 2, edge=False)
    gauge.front.set(0, 0, "L4")
    # A fold of net over the left forearm: a loop round the arm and lobes hanging outside and in front.
    left = "LEFT_ARM"
    loop = g.piece("net_loop", left, (-1.5, 4.0, -2.5), (5, 2, 5), inflate=.08)
    net_box(loop, "S3", "S2", 4, knot="S4")
    outer = g.piece("net_drape_outer", left, (3.2, 4.4, -2.6), (1, 7, 5), rotation=(0, 0, -4))
    net_box(outer, "S3", "S2", 4, knot="S4")
    front = g.piece("net_drape_front", left, (-1.4, 4.6, -3.1), (4, 5, 1))
    net_box(front, "S3", "S2", 4, knot="S4")
    for i, (z, y) in enumerate(((-1.9, 11.3), (0.6, 10.8))):
        cork = g.piece(f"net_cork_{i}", left, (3.3, y, z), (1, 1, 1), inflate=.1)
        solid(cork, "L", "smooth", 53005 + i, 3, edge=False)
        cork.front.fill("L4")
