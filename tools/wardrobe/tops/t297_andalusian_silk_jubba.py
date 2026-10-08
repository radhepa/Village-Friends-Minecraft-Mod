"""Andalusian Silk Jubba: an open-fronted silk jubba over a pale qamis, bell sleeves and woven tiraz armbands."""
from kit import SIDES, body, sleeves
from kit_male import sleeve_shapes
from kit_m08 import coat_skirt
from paint import fabric, strip_fabric

META = {
    "name": "Andalusian Silk Jubba",
    "gender": "male",
    "description": "A flowing open-fronted silk jubba over a pale qamis, its bell sleeves banded high on the arm with woven tiraz bands.",
    "tags": ["fancy", "robe"],
    "covers_waist": True,
}


def tiraz(face, y):
    """A woven tiraz armband: dark edges round two rows of tall and short woven strokes."""
    face.hline(0, face.w - 1, y, "A1")
    for x in range(face.w):
        face.set(x, y + 1, "M3" if x % 4 in (0, 1) else "A2")
        face.set(x, y + 2, "M2" if x % 4 in (0, 2) else "A2")
    face.hline(0, face.w - 1, y + 3, "A1")


def build(g):
    shirt = body(g, "S", "weave", 38041, base=3)                     # the pale qamis beneath
    shirt.front.clear(3, 0), shirt.front.clear(4, 0)
    shirt.front.vline(4, 1, 2, "S1")
    jacket = g.part("jacket")
    strip_fabric(jacket, "P", "smooth", 38042, 2)
    fabric(jacket.top, "P", "smooth", 38042, 3)
    fabric(jacket.bottom, "P", "smooth", 38043, 1)
    jf = jacket.front
    for y in range(12):
        jf.clear(3, y), jf.clear(4, y)                                   # the open front shows the qamis
        jf.set(2, y, "A3" if y % 2 else "A2"), jf.set(5, y, "A3" if y % 2 else "A2")
    jf.vline(0, 3, 11, "P1"), jf.vline(7, 3, 11, "P1")                   # silk falling in soft folds
    jacket.back.hline(1, 6, 0, "A2")
    jacket.back.vline(3, 3, 11, "P1")
    sleeves(g, "P", "smooth", 38044, rows=(0, 10))
    for side in SIDES:
        tiraz(g.part(f"{side}_sleeve").strip, 1)                          # raised tiraz band on the upper arm
    for bell in sleeve_shapes(g, "bell_sleeve", "P", 4.6, (6, 4, 6), "smooth", 38045, inflate=.08):
        for face in bell.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 3, "A2")
            face.set(face.w // 2, 2, "P1")
        bell.bottom.fill("P0")
        bell.bottom.rect(2, 2, 2, 2, "S2")                               # the qamis cuff inside
    front, back, sides = coat_skirt(g, "jubba_skirt", 8, "P", "smooth", 38046, top=10.6, hem="A1")
    for y in range(8):
        for x in (3, 4, 5):
            front.set(x, y, "S3" if y < 7 else "S2")                      # the qamis hem between the fronts
        front.set(2, y, "A3" if y % 2 else "A2"), front.set(6, y, "A3" if y % 2 else "A2")
    front.vline(0, 1, 6, "P1")
    back.vline(4, 1, 6, "P1"), back.vline(1, 2, 6, "P1"), back.vline(7, 2, 6, "P1")
