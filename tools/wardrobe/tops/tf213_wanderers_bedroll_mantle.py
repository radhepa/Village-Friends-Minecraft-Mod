"""Wanderer's Bedroll Mantle: a short wool shoulder mantle over a plain kirtle, with a striped blanket
rolled into a horseshoe and slung from the right shoulder to the left hip, front and back."""
from kit import body, sleeves
from kit_f07 import prop
from kit_female import brooch, mantle, neck, trim
from paint import fabric

META = {
    "name": "Wanderer's Bedroll Mantle",
    "gender": "female",
    "description": "A short fringed wool mantle over a plain kirtle, with a striped blanket rolled into a horseshoe "
                   "and slung across the body from shoulder to hip.",
    "tags": ["casual", "rugged"],
}


def roll_piece(g, pid, z, seed):
    """One side of the horseshoe roll: a long tied bundle of blanket, angled shoulder to hip."""
    box = prop(g, pid, "TORSO", (-1.5, 0, -1.5), (3, 12, 3), pivot=(-3.2, -.4, z), rotation=(0, 0, -34), role="A",
               texture="weave", seed=seed, base=2)
    for face in box.sides:
        for y in range(box.h):
            face.set((y // 2) % face.w, y, "A1")                    # the rolled blanket's spiral edge
        for y in (1, 6, 10):
            face.hline(0, face.w - 1, y, "L1")                      # tie cords
    box.top.fill("A2"), box.top.set(1, 1, "A0"), box.top.set(0, 0, "A3"), box.top.set(2, 2, "A3")
    return box


def build(g):
    b = body(g, "S", "weave", 57201)
    neck(b.front, "round", "S", 2, edge="S3")
    sleeves(g, "S", "weave", 57202, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 10, "S1"), arm.strip.hline(0, 15, 11, "S3")
    j = g.part("jacket")
    fabric(j.front, "L", "leather", 57203, 2, 0, 8, 8, 1)          # a plain belt under the roll
    j.front.set(4, 8, "M3")
    for face in (j.right, j.left, j.back):
        fabric(face, "L", "leather", 57203, 2, 0, 8, face.w, 1)
    cape = mantle(g, "mantle", "P", "weave", 57204, 2, height=4, width=17, depth=6, y=-.6)
    for face in cape.sides:
        trim(face, 3, "dash", "P0")                                  # a knotted fringe along the edge
        face.hline(0, face.w - 1, 2, "P1")
    brooch(g, "mantle_pin", (1.4, .6, -3.1), metal="M", gem="A3")
    roll_piece(g, "bedroll_front", -4.4, 57205)
    roll_piece(g, "bedroll_back", 4.8, 57206)
    knot = prop(g, "bedroll_knot", "TORSO", (-1, -1, -1), (2, 2, 2), pivot=(3.7, 9.6, -4.3), role="L",
                texture="leather", seed=57207, base=2, edge=False, motion="flap_front")
    knot.front.set(0, 0, "L3"), knot.front.set(1, 1, "L1")
