"""Tippet Cotehardie: a close-fitting cotehardie buttoned from throat to hip, long white tippets and a low jeweled hip belt."""
from kit import body, sleeves
from kit_female import OVER_BACK, OVER_FRONT, buttons, neck, tippets
from paint import solid

META = {
    "name": "Tippet Cotehardie",
    "gender": "female",
    "description": "A close-fitting cotehardie buttoned from throat to hip, long white tippets at the elbows and a low jeweled belt.",
    "tags": ["fancy", "tailored", "slim"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 15201)
    neck(b.front, "boat", "P", 2, edge="P3")
    buttons(b.front, 4, 2, 11, "M3", step=1, placket=None)
    for y in range(2, 12):
        b.front.set(3, y, "P1")
    for face in (b.front, b.back):
        face.vline(1, 3, 11, "P1"), face.vline(6, 3, 11, "P1")
    sleeves(g, "P", "velvet", 15202, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        outer = arm.right if side == "right" else arm.left
        for y in range(5, 11):
            outer.set(2, y, "M3" if y % 2 else "P1")
        arm.strip.hline(0, 15, 3, "S4")                              # where the tippet bands the elbow
    tippets(g, "S", y=3.6, length=10, key_end="S2")
    # The low hip belt: front and back ride the stride with the skirt; the sides stay put.
    for name, z, motion, face in (("hip_belt_front", OVER_FRONT - .1, "flap_front", "front"), ("hip_belt_back", OVER_BACK + .1, "flap_back", "back")):
        belt = g.piece(name, "TORSO", (-5, 1.4, 0), (10, 1, 1), pivot=(0, 9.0, z), motion=motion)
        solid(belt, "M", "smooth", 15203, 3, edge=False)
        f = getattr(belt, face)
        for x in range(0, 10, 3):
            f.set(x, 0, "A2")
    for name, x in (("hip_belt_right", -5.9), ("hip_belt_left", 5.9)):
        side = g.piece(name, "TORSO", (-.5, 0, -2.9), (1, 1, 6), pivot=(x, 10.4, 0))
        solid(side, "M", "smooth", 15204, 3, edge=False)
