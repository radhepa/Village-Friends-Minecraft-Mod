"""Hooded Capelet over Kirtle: a short shoulder capelet with a deep hood lying back, bound in a bright tape and tied with tasselled cords."""
from kit import SIDES, body
from kit_female import mantle, neck
from kit_f10 import cord
from paint import fabric, solid, strip_fabric

META = {
    "name": "Hooded Capelet over Kirtle",
    "gender": "female",
    "description": "A short wool capelet to the elbow with a deep hood lying back, its edges bound in a bright tape and tied at the throat with tasselled cords, over a plain kirtle.",
    "tags": ["casual", "simple"],
}


def build(g):
    b = body(g, "S", "weave", 60280, base=2)
    neck(b.front, "round", "S", 2)
    b.back.vline(3, 3, 11, "S1")
    for face in (b.front, b.back):
        face.vline(1, 5, 11, "S1"), face.vline(6, 5, 11, "S1")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "weave", 60281 + (side == "left"), 2, 0, 11)
        fabric(arm.top, "S", "weave", 60283, 3)
        arm.strip.hline(0, 15, 11, "S1")
    cape = mantle(g, "capelet", "P", "weave", 60284, 2, height=5, width=17, depth=6, y=-.6)
    for face in cape.sides:
        face.hline(0, face.w - 1, 4, "A2")                            # the bound lower edge
        for x in range(1, face.w, 4):
            face.vline(x, 1, 3, "P1")                                  # soft folds over the shoulders
    cape.front.vline(8, 0, 4, "A2")                                    # bound front edges meeting at the throat
    cape.front.vline(7, 0, 3, "P1"), cape.front.vline(9, 0, 3, "P3")
    # The hood lying back on the shoulders in two soft folds, its lining showing at the opening.
    hood = g.piece("hood_upper", "TORSO", (-4, 0, 0), (8, 3, 2), pivot=(0, -1.0, 2.75), rotation=(10, 0, 0))
    solid(hood, "P", "weave", 60285, 2)
    hood.top.fill("S3"), hood.top.hline(0, 7, 1, "A2")
    hood.back.vline(3, 0, 2, "P1"), hood.back.vline(4, 0, 2, "P3")
    tip = g.piece("hood_lower", "TORSO", (-3, 0, 0), (6, 3, 1), pivot=(0, 1.9, 3.15), rotation=(8, 0, 0))
    solid(tip, "P", "weave", 60286, 2)
    tip.back.vline(2, 0, 2, "P1"), tip.back.vline(3, 0, 1, "P3")
    tip.back.hline(1, 4, 2, "P1")
    # Tasselled cords tied at the throat.
    knot = g.piece("cord_knot", "TORSO", (-.5, -.5, -.5), (1, 1, 1), pivot=(0, .3, -3.25))
    solid(knot, "A", "plain", 60287, 3, edge=False)
    for i, (x, length, rot) in enumerate(((-.6, 4, 6), (.6, 3, -6))):
        c = cord(g, f"tassel_cord_{i}", (x, .8, -3.3), length, role="A", base=2, end="A4", rotation=(0, 0, rot))
        c.bottom.fill("A1")
