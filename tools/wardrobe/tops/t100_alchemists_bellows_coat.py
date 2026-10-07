"""Alchemist's Bellows Coat: a scorch-marked coat with a glowing flask at the belt and a pair of hand bellows slung on the back."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk
from paint import solid

META = {
    "name": "Alchemist's Bellows Coat",
    "gender": "male",
    "description": "A puffer's coat pocked with scorch marks, a glowing glass flask at the belt and a pair of hand bellows slung across the back.",
    "tags": ["scholarly", "work"],
    "covers_waist": True,
}

SCORCH = ((1, 5), (6, 8), (3, 10), (5, 3))


def scorch(face):
    for x, y in SCORCH:
        if face.inside(x, y):
            face.set(x, y, "K2")
            for dx, dy in ((1, 0), (0, 1)):
                if face.inside(x + dx, y + dy):
                    face.set(x + dx, y + dy, "L1")


def build(g):
    b = body(g, "P", "twill", 10001)
    neckline(b.front, "round", "P")
    scorch(b.front), scorch(b.back)
    sleeves(g, "P", "twill", 10002, rows=(0, 10), cuff="L2")
    belt(g, "belt", 9.4)
    flask = blk(g, "glowing_flask", (2.8, 10.4, -2.9), (2, 2, 2), "A", 3, "plain", 10003)
    flask.front.set(0, 0, "A4"), flask.top.fill("A4")
    blk(g, "flask_neck", (2.8, 9.6, -2.9), (1, 1, 1), "S", 4, "plain", 10004, edge=False)
    bellows = g.piece("hand_bellows", "TORSO", (-2, 0, 0), (4, 5, 1), pivot=(.6, 1.2, 2.6), rotation=(0, 0, 18))
    solid(bellows, "L", "leather", 10005, 2)
    for x in range(4):
        bellows.back.set(x, 2, "L0")                                     # pleated leather
    bellows.back.hline(0, 3, 0, "L4")
    nozzle = g.piece("bellows_nozzle", "TORSO", (-.5, 5, 0), (1, 2, 1), pivot=(.6, 1.2, 2.6), rotation=(0, 0, 18))
    solid(nozzle, "M", "smooth", 10006, 2)
    for face in flaps(g, "coat_skirt", 5, "P", "twill", 10007, top=10.8, slit=True):
        scorch(face)
