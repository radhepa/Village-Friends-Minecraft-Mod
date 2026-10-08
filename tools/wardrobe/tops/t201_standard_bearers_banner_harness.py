"""Standard Bearer's Banner Harness: a tunic under a leather harness carrying a tall banner pole and swallow-tailed pennant."""
from kit import body, flaps, sleeves
from kit_m04 import diag
from paint import k, solid

META = {
    "name": "Standard Bearer's Banner Harness",
    "gender": "male",
    "description": "A bordered tunic under a leather carrying harness: breast straps meet at an iron ring, and a socket at the "
                   "small of the back holds a tall banner pole flying a swallow-tailed pennant above the left shoulder.",
    "tags": ["martial", "fancy"],
    "covers_waist": True,
}

S = 34200
BUTT = (2.5, 10.6, 3.4)     # where the pole's foot sits in its back socket
LEAN = (-4, 0, 12)          # leans back a little and out past the left side of the head
LENGTH = 25


def on_pole(g, pid, origin, size, role, base, seed, texture="plain"):
    """A cuboid in the pole's own frame (y up the pole is negative)."""
    box = g.piece(pid, "TORSO", origin, size, pivot=BUTT, rotation=LEAN)
    solid(box, role, texture, seed, base, edge=False)
    return box


def build(g):
    b = body(g, "P", "weave", S)
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "A2")
    sleeves(g, "P", "weave", S + 1, rows=(0, 10), cuff="A2")
    # Harness: two breast straps from the shoulders to a ring, an X across the back, a socket belt.
    jacket = g.part("jacket")
    f, bk = jacket.front, jacket.back
    diag(f, 0, 0, 3, 4, ["L3", "L1"])
    diag(f, 6, 0, 3, 4, ["L3", "L1"])
    f.set(3, 5, "M3"), f.set(4, 5, "M3"), f.set(3, 6, "M1"), f.set(4, 6, "M1")      # the iron ring
    f.vline(3, 7, 9, "L2"), f.vline(4, 7, 9, "L1")
    diag(bk, 0, 0, 6, 9, ["L3", "L1"])
    diag(bk, 6, 0, 0, 9, ["L3", "L1"])
    for x in (0, 1, 6, 7):
        jacket.top.vline(x, 0, 3, "L2")
    belt = g.piece("socket_belt", "TORSO", (-4.6, 9.4, -2.6), (9, 2, 5), inflate=.07)
    solid(belt, "L", "leather", S + 2, 2, edge=False)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    belt.front.set(4, 1, "M3")
    socket = g.piece("pole_socket", "TORSO", (1.4, 9.0, 2.3), (2, 3, 2))
    solid(socket, "L", "leather", S + 3, 1)
    socket.back.hline(0, 1, 0, "L3"), socket.back.set(0, 2, "M3")
    # The pole, its spear finial and the pennant.
    shaft = on_pole(g, "banner_pole", (-.5, -LENGTH, -.5), (1, LENGTH, 1), "L", 3, S + 4)
    for face in shaft.sides:
        face.vline(face.w - 1, 0, LENGTH - 1, "L2")
        for y in range(2, LENGTH, 6):
            face.set(0, y, "L4")
    tip = on_pole(g, "banner_finial", (-.5, -LENGTH - 2, -.5), (1, 2, 1), "M", 3, S + 5, "smooth")
    tip.strip.hline(0, tip.strip.w - 1, 1, "M2")
    on_pole(g, "banner_cross_bar", (-.5, -LENGTH, -.5), (7, 1, 1), "L", 2, S + 6)
    flag = on_pole(g, "pennant", (.5, -LENGTH + 1, -.5), (6, 5, 1), "A", 2, S + 7)
    for face in (flag.front, flag.back):
        face.hline(0, 5, 0, "A3"), face.hline(0, 5, 4, "A1")
        face.vline(0 if face is flag.front else 5, 0, 4, "A1")
        for x, y in ((2, 2), (3, 2), (2, 1), (3, 3), (4, 2)):
            face.set(x if face is flag.front else 5 - x, y, "S4")            # a pale charge
    for i, y in enumerate((-LENGTH + 1, -LENGTH + 4)):
        tail = on_pole(g, f"pennant_tail_{i}", (6.5, y, -.5), (2, 2, 1), "A", 2, S + 8 + i)
        for face in tail.sides:
            face.hline(0, face.w - 1, 0 if i == 0 else 1, k("A", 1 if i else 3))
    for face in flaps(g, "tunic_skirt", 3, "P", "weave", S + 10, top=10.8, hem="A2"):
        face.hline(0, 8, 1, "A3")
