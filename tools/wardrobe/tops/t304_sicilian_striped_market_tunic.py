"""Sicilian Striped Market Tunic: a boldly striped cotton tunic with rolled sleeves, a knotted neckerchief, a rope belt and a coin purse."""
from kit import SIDES, body, collar, flaps, pouch, roll
from kit_male import blk, stripes
from paint import solid, strip_fabric

META = {
    "name": "Sicilian Striped Market Tunic",
    "gender": "male",
    "description": "A boldly striped cotton market tunic with its sleeves rolled to the elbow, a neckerchief knotted at the throat, a twisted rope belt and a coin purse.",
    "tags": ["casual", "simple"],
    "covers_waist": True,
}

STRIPE = ["P2", "S3", "S3"]


def build(g):
    b = body(g, "P", "weave", 38321)
    stripes(b.strip, STRIPE, vertical=True)
    stripes(b.top, STRIPE, vertical=True)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.vline(4, 1, 2, "P1")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 38322, 2, 0, 5)
        stripes(arm.strip, STRIPE, vertical=True, rows=range(0, 5))
        stripes(arm.top, STRIPE, vertical=True)
    roll(g, "S", 3.0, base=3)                                                # sleeves rolled to the elbow
    band = collar(g, "kerchief_band", "A", "plain", base=2, height=1, y=-.4)
    for face in band.sides:
        face.hline(0, face.w - 1, 0, "A3")
    knot = blk(g, "kerchief_knot", (0, .2, -2.8), (2, 1, 1), "A", 3, "plain", 38323, edge=False)
    knot.front.set(1, 0, "A2")
    for name, x, rz in (("kerchief_tail_right", -.7, 18), ("kerchief_tail_left", .7, -18)):
        tail = blk(g, name, (x, 1.0, -2.75), (1, 2, 1), "A", 2, "plain", 38324, rotation=(0, 0, rz), edge=False)
        tail.front.set(0, 1, "A1")
    back = g.part("jacket").back                                             # the kerchief's point on the back
    for y, (x0, x1) in enumerate(((1, 6), (2, 5), (3, 4))):
        back.hline(x0, x1, y, "A2")
        back.set(x0, y, "A1"), back.set(x1, y, "A1")
    rope = g.piece("rope_belt", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.05)
    solid(rope, "S", "plain", 38325, 2, edge=False)
    for face in rope.sides:
        for x in range(face.w):
            face.set(x, 0, "S3" if x % 2 else "S1")                        # the twist of the rope
    rope_end = blk(g, "rope_knot", (1.6, 10.2, -2.9), (1, 3, 1), "S", 2, "plain", 38326, motion="sway")
    rope_end.front.set(0, 0, "S3"), rope_end.front.set(0, 2, "S1")
    pouch(g, "coin_purse", (-2.4, 9.9, -3.0), size=(2, 2, 1), role="L", flap="M3")
    for face in flaps(g, "tunic_hem", 3, "P", "weave", 38327, top=10.4):
        stripes(face, STRIPE, vertical=True)
        face.hline(0, face.w - 1, 2, "P1")
