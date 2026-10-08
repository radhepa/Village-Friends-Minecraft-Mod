"""Front-Laced Wool Kirtle: a plain wool kirtle laced from neck to hip, tied at the throat, with laced-on sleeves."""
from kit import SIDES, body
from kit_female import arm_rings, lacing, neck
from kit_f10 import cord
from paint import solid, strip_fabric

META = {
    "name": "Front-Laced Wool Kirtle",
    "gender": "female",
    "description": "A plain wool kirtle laced from throat to hip and tied in a bow, its sleeves laced on with chemise puffing at the shoulders.",
    "tags": ["casual", "simple"],
}


def build(g):
    b = body(g, "P", "weave", 60000)
    neck(b.front, "round", "P", 2)
    b.front.set(3, 1, "S4"), b.front.set(4, 1, "S4")                 # the chemise at the top of the opening
    lacing(b.front, 3, 2, 10, "spiral", lace="A3", under="S3", eyelet="M3")
    b.front.set(3, 11, "P1"), b.front.set(4, 11, "P1")
    for face in (b.front, b.back):
        face.vline(1, 3, 11, "P1"), face.vline(6, 3, 11, "P1")      # shaped side-front seams
    b.back.vline(3, 1, 11, "P1"), b.back.vline(4, 1, 11, "P3")
    for face in (b.right, b.left):
        face.vline(2, 2, 11, "P1")
    # Wool sleeves laced to the bodice: the chemise puffs through the gap at each shoulder.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 60001 + (side == "left"), 2, 0, 11)
        arm.top.fill("P3")
        arm.strip.hline(0, 15, 10, "P3"), arm.strip.hline(0, 15, 11, "P1")
        outer = arm.right if side == "right" else arm.left
        outer.vline(1, 3, 9, "P1")
    for ring in arm_rings(g, "chemise_puff", -2.2, 2, 5, inflate=.1):
        solid(ring, "S", "weave", 60003, 3, edge=False)
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "S4" if x % 2 == 0 else "S3")
                face.set(x, 1, "S2" if x % 2 else "S3")
            face.set(1, 1, "A2"), face.set(3, 1, "A2")                  # the points tying the sleeve on
        ring.top.fill("S4")
    # The lace tied at the throat, its tipped ends hanging down the chest.
    knot = g.piece("lace_knot", "TORSO", (-.5, -.5, -.5), (1, 1, 1), pivot=(0, 1.6, -2.45))
    solid(knot, "A", "plain", 60004, 3, edge=False)
    cord(g, "lace_end_right", (-.4, 2.0, -2.55), 3, role="A", base=3, end="M3", rotation=(0, 0, 8))
    cord(g, "lace_end_left", (.5, 2.0, -2.55), 2, role="A", base=3, end="M3", rotation=(0, 0, -10))
