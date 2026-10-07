"""Buttoned Cotehardie: a fitted jacket with a long run of buttons, buttoned sleeves and a low hip belt."""
from kit import body, flaps, neckline, sleeves
from paint import grid, k, rivets, solid

META = {
    "name": "Buttoned Cotehardie",
    "gender": "male",
    "description": "A close-fitting jacket buttoned from collar to hem and down the forearms, with a jeweled hip belt.",
    "tags": ["fancy", "tailored"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 1801)
    neckline(b.front, "round", "P")
    b.front.vline(4, 1, 11, "P1"), b.front.vline(3, 1, 11, "P3")
    for y in range(1, 12):
        b.front.set(3, y, "M3" if y % 2 else "P3")
    for face in (b.right, b.left):
        face.vline(1, 0, 11, "P1")
    b.back.vline(3, 0, 11, "P1")
    sleeves(g, "P", "velvet", 1802, rows=(0, 10), cuff="A2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        outer = arm.right if side == "right" else arm.left
        for y in range(5, 10, 2):
            outer.set(2, y, "M3")
    hip = g.piece("hip_belt", "TORSO", (-4.7, 10.6, -2.7), (9, 1, 5), inflate=.06)
    solid(hip, "L", "leather", 1803, 2, edge=False)
    for face in hip.sides:
        rivets(face, 0, step=2, start=1)
    pend = g.piece("belt_pendant", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-1.6, 11.4, -2.8))
    solid(pend, "L", "leather", 1804, 2)
    pend.front.set(0, 2, "M4")
    front, back = flaps(g, "skirt", 3, "P", "velvet", 1805, top=11.0, hem="A2")
    front.vline(4, 0, 1, "M3")
