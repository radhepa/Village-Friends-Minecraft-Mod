"""Physician's Flask-Case Gown: a long buttoned gown, a lined hood thrown back, and a urine flask in a wicker case on a strap."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk, hood_down
from kit_m05 import strap
from paint import k

META = {
    "name": "Physician's Flask-Case Gown",
    "gender": "male",
    "description": "A doctor of physic's calf-length gown closed by little cloth buttons, its lined hood thrown back, with a glass flask riding in a wicker case on a shoulder strap.",
    "tags": ["scholarly", "robe"],
    "covers_waist": True,
}


def wicker(face, rim=True):
    """Basketwork: alternating over-under texels with a lit rim."""
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, "L3" if (x + y) % 2 == 0 else "L1")
    if rim:
        face.hline(0, face.w - 1, 0, "L4")


def build(g):
    b = body(g, "P", "velvet", 35000)
    neckline(b.front, "round", "P")
    b.front.vline(3, 1, 11, "P1")
    for y in range(1, 11, 2):
        b.front.set(4, y, "A3")                                         # little cloth buttons
    for face in (b.right, b.left):
        face.vline(1 if face is b.right else 2, 2, 11, "P1")
    sleeves(g, "P", "velvet", 35001, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "A3")                   # turned-back lined cuffs
        arm.strip.hline(0, arm.strip.w - 1, 10, "A2")
        arm.strip.hline(0, arm.strip.w - 1, 8, "P1")
    hood_down(g, "A", "weave", 35002, y=-1.1, z=3.0, tilt=12, lining="S3")
    strap(g, "L2", "L1", from_side="left", low=10)
    belt(g, "girdle", 9.6, role="A", base=1, height=1, buckle=None)
    # The flask case: wicker body, the glass neck and stopper showing above it.
    case = g.piece("flask_case", "TORSO", (-1, 0, -1), (2, 4, 2), pivot=(-3.0, 9.0, -2.95), motion="flap_front")
    for face in case.sides:
        wicker(face)
    case.top.fill("L4"), case.bottom.fill("L0")
    neck = g.piece("flask_neck", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(-3.0, 9.0, -2.95), motion="flap_front")
    for face in neck.faces:
        face.fill("S4")
    neck.front.set(0, 1, "S3"), neck.left.set(0, 1, "S2"), neck.right.set(0, 1, "S2")
    stopper = g.piece("flask_stopper", "TORSO", (-.5, -3, -.5), (1, 1, 1), pivot=(-3.0, 9.0, -2.95), motion="flap_front")
    for face in stopper.faces:
        face.fill("L2")
    stopper.top.fill("L3")
    front, back = flaps(g, "gown", 9, "P", "velvet", 35003, top=10.6, hem="P1")
    front.vline(3, 0, 8, "P1"), front.vline(4, 0, 8, "P3")
    for y in range(0, 8, 2):
        front.set(4, y, "A3")                                           # buttons run on down the skirt
    back.vline(4, 1, 8, "P1"), back.vline(2, 2, 8, "P3"), back.vline(6, 2, 8, "P3")
    for name, x in (("gown_right", -4.45), ("gown_left", 4.45)):
        side = blk(g, name, (x, 10.6, 0), (1, 8, 4), "P", 2, "velvet", 35004)
        for face in side.sides:
            face.hline(0, face.w - 1, side.h - 1, k("P", 1))
