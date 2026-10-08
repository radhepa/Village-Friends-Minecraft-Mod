"""Scout's Leaf-Mottled Mantle: a hooded shoulder mantle dyed in leaf-shaped blotches with a leaf-dagged edge, over
a plain wool tunic, an archer's bracer and a signal horn on a baldric."""
from kit import sleeves
from kit_female import hood_down, mantle, neck
from kit_f04 import front_prop
from paint import fabric, line, rnd, solid, strip_fabric

META = {
    "name": "Scout's Leaf-Mottled Mantle",
    "gender": "female",
    "description": "A hooded shoulder mantle dyed in leaf-shaped blotches with a leaf-dagged edge, over a plain "
                   "tunic, with a laced bracer and a signal horn on a baldric.",
    "tags": ["rugged", "simple"],
}

LEAF = [".a.", "aab", ".b."]


def mottle(face, seed, base=2):
    """Leaf-shaped dye blotches on a staggered grid: dark leaves, light leaves and a few accent ones."""
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, f"P{base}")
    row = 0
    for y in range(-1, face.h, 3):
        for x in range(-2 + (row % 2) * 2, face.w, 4):
            r = rnd(x + face.x0, y + face.y0, seed)
            a = "A2" if r < .18 else "P1" if r < .6 else "P3"
            for dy, line_ in enumerate(LEAF):
                for dx, ch in enumerate(line_):
                    if ch != "." and 0 <= x + dx < face.w and 0 <= y + dy < face.h:
                        face.set(x + dx, y + dy, a if ch == "a" else ("P0" if a == "P1" else "P1" if a == "A2" else "P2"))
        row += 1


def build(g):
    b = g.part("body")
    strip_fabric(b, "S", "weave", 54161, 2)
    fabric(b.top, "S", "weave", 54161, 3), fabric(b.bottom, "S", "weave", 54161, 1)
    neck(b.front, "round", "S", 2)
    for face in b.sides:
        face.hline(0, face.w - 1, 9, "L2")                           # a narrow cord belt
    b.front.set(3, 9, "M3")
    sleeves(g, "S", "weave", 54162, base=2, rows=(0, 11))
    left = g.part("left_arm")
    strip_fabric(left, "L", "leather", 54163, 2, 6, 10)               # the archer's bracer
    left.strip.hline(0, 15, 6, "L3")
    for y in (7, 9):
        left.front.set(1, y, "S4"), left.front.set(2, y + 1, "S4")
    # The baldric for the horn, painted on the tunic under the mantle.
    j = g.part("jacket")
    line(j.front, 7, 2, 1, 9, "L2"), line(j.back, 0, 2, 6, 9, "L2")
    m = mantle(g, "leaf_mantle", "P", "weave", 54164, 2, height=5, width=17, depth=6, y=-.8)
    for face in m.sides:
        mottle(face, 54165)
        for x in range(face.w):                                      # leaf-dagged lower edge
            face.set(x, face.h - 1, "P0" if x % 3 == 2 else face.get(x, face.h - 1))
    mottle(m.top, 54166, 3)
    m.front.vline(8, 0, 4, "P0")
    clasp = front_prop(g, "mantle_clasp", 0, (2, 1, 1), drop=-9.2, top=9.0, z=-2.85, motion="none")
    solid(clasp, "M", "smooth", 54167, 3, edge=False)
    hood = g.piece("hood", "TORSO", (-3.5, 0, 0), (7, 4, 2), pivot=(0, -.6, 3.25), rotation=(16, 0, 0))
    solid(hood, "P", "weave", 54168, 2)
    for face in (hood.back, hood.right, hood.left):
        mottle(face, 54169)
    hood.top.fill("S3"), hood.top.hline(0, 6, 1, "S2")               # the lining shows at the open face
    hood.back.vline(3, 0, 3, "P0")
    hood.back.hline(0, 6, 3, "P0")
    # Signal horn on the right hip: mouthpiece, curved body and a metal-banded bell.
    horn = front_prop(g, "horn_body", -1.6, (3, 1, 1), drop=2.2, rotation=(0, 0, -16))
    solid(horn, "S", "smooth", 54170, 3, edge=False)
    horn.front.set(0, 0, "S4"), horn.front.set(2, 0, "S2")
    bell = front_prop(g, "horn_bell", -3.4, (2, 2, 2), drop=2.4)
    solid(bell, "S", "smooth", 54171, 3, edge=False)
    for face in bell.sides:
        face.hline(0, face.w - 1, 0, "M3")
    bell.bottom.fill("K1")
    tip = front_prop(g, "horn_tip", .2, (1, 1, 1), drop=1.7)
    solid(tip, "M", "smooth", 54172, 3, edge=False)
