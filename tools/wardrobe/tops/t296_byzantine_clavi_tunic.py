"""Byzantine Clavi Tunic: a knee-length belted tunic with two woven clavi stripes and roundel segmenta."""
from kit import belt, body, neckline, sleeves
from kit_m08 import coat_skirt, roundel

META = {
    "name": "Byzantine Clavi Tunic",
    "gender": "male",
    "description": "A knee-length tunic with two woven clavi stripes running down from the shoulders, woven roundels at shoulder and knee, and banded cuffs.",
    "tags": ["fancy", "tailored"],
    "covers_waist": True,
}

CLAVI = (1, 6)   # the two stripe columns on the body, front and back


def clavus(face, x, y0, y1):
    for y in range(y0, y1 + 1):
        face.set(x, y, "A2" if y % 3 else "A1")


def build(g):
    b = body(g, "P", "weave", 38001)
    neckline(b.front, "round", "P")
    for face in (b.front, b.back):
        for x in CLAVI:
            clavus(face, x, 0, 11)
    sleeves(g, "P", "weave", 38002, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        outer = arm.right if side == "right" else arm.left
        roundel(outer, 0, 1, "A1", "A3", "M3")                           # shoulder segmentum
        for y, key in ((7, "A1"), (8, "A2"), (9, "A2"), (10, "A1")):
            arm.strip.hline(0, arm.strip.w - 1, y, key)                   # banded cuff
        for x in range(1, arm.strip.w, 3):
            arm.strip.set(x, 8, "M3"), arm.strip.set(x + 1, 9, "M2")
    belt(g, "belt", 9.4, height=1, buckle="M")
    front, back, sides = coat_skirt(g, "tunic_skirt", 9, "P", "weave", 38003, top=10.4)
    for face in (front, back):
        for x in (1, 7):
            clavus(face, x, 0, 2)
            face.set(x, 3, "A3")                                         # leaf terminal of the clavus
        roundel(face, 0, 4, "A1", "A3", "M3"), roundel(face, 5, 4, "A1", "A3", "M3")   # knee segmenta
        face.hline(0, 8, 8, "A1")
    for box in sides:
        for f in box.sides:
            f.hline(0, f.w - 1, f.h - 1, "A1")
