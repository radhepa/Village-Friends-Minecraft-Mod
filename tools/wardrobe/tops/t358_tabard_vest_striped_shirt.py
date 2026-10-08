"""Tabard Vest over Striped Shirt: a plain open-sided tabard vest tied at the hips over a cheerful banded-stripe shirt."""
from kit import SIDES, body
from kit_m10 import tie
from kit_male import stripes
from paint import fabric, k, solid

META = {
    "name": "Tabard Vest over Striped Shirt",
    "gender": "male",
    "description": "A plain tabard vest open at the sides and tied at the hips, its square panels hanging to the upper thigh, over a cheerful shirt banded in broad stripes down to the cuffs.",
    "tags": ["casual", "simple", "whimsical"],
    "covers_waist": True,
}

STRIPE = ["S4", "S4", "A2", "A2"]


def build(g):
    shirt = body(g, "S", "plain", 40580, base=4)
    for face in shirt.sides:
        stripes(face, STRIPE, offset=1)
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        stripes(arm.strip, STRIPE, rows=range(0, 10), offset=1)
        fabric(arm.top, "S", "plain", 40581, 4)
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")                     # plain cuff band
        arm.strip.hline(0, arm.strip.w - 1, 9, "S3")
    # The tabard panels on the overlay: open at the sides so the stripes show.
    vest = g.part("jacket")
    for face in (vest.front, vest.back):
        fabric(face, "P", "weave", 40582 + (face is vest.back), 2, 1, 0, 6, 12)
        face.vline(1, 0, 11, "P1"), face.vline(6, 0, 11, "P3" if face is vest.front else "P1")
        face.hline(1, 6, 0, "P3")
    fabric(vest.top, "P", "weave", 40584, 3, 1, 0, 6, 4)
    f = vest.front
    f.clear(3, 0), f.clear(4, 0), f.clear(3, 1), f.clear(4, 1)
    f.set(2, 0, "P1"), f.set(5, 0, "P1"), f.set(3, 2, "P1"), f.set(4, 2, "P1")
    shirt.front.set(3, 0, "S2"), shirt.front.set(4, 0, "S2")
    # Square panels below the waist, and the hip ties joining front to back.
    for name, z, motion, face_name in (("front", -2.85, "flap_front", "front"), ("back", 1.85, "flap_back", "back")):
        panel = g.piece(f"tabard_{name}", "TORSO", (-3, 0, 0), (6, 4, 1), pivot=(0, 11.2, z), motion=motion)
        solid(panel, "P", "weave", 40585 + (name == "back"), 2)
        face = getattr(panel, face_name)
        face.hline(0, 5, 0, k("P", 3))
        face.hline(0, 5, 3, "P0")
        face.vline(0, 1, 3, "P1"), face.vline(5, 1, 3, "P1")
    for i, x in enumerate((-3.4, 3.4)):
        tie(g, f"hip_tie_{i}", "TORSO", (x, 9.0, -2.45), "A", 3, 2, 40587 + i, rotation=(0, 0, 8 if i else -8))
