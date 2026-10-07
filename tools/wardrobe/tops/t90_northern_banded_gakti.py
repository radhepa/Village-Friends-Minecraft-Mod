"""Northern Banded Gakti: a wool herder's tunic with bright woven bands at shoulders and hem, a tall stand collar and a pewter belt."""
from kit import body, collar, flaps, sleeves
from kit_male import stripes
from paint import solid

META = {
    "name": "Northern Banded Gakti",
    "gender": "male",
    "description": "A reindeer herder's wool tunic with bright woven bands across the shoulders and hem, a tall banded collar and a pewter-studded belt.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}

BANDS = ["A2", "S4", "M3", "A3"]


def build(g):
    b = body(g, "P", "weave", 9001)
    for face in b.sides:
        stripes(face, BANDS, rows=range(1, 3), offset=1)
        face.hline(0, face.w - 1, 3, "A1")
    stripes(b.top, BANDS, vertical=False)
    sleeves(g, "P", "weave", 9002, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        stripes(arm.strip, BANDS, rows=range(0, 2))
        stripes(arm.strip, BANDS, rows=range(9, 11), offset=2)
    tall = collar(g, "banded_collar", "A", "plain", base=2, height=2, y=-1.2)
    for face in tall.sides:
        stripes(face, BANDS)
    hip = g.piece("pewter_belt", "TORSO", (-4.6, 9.4, -2.6), (9, 1, 5), inflate=.06)
    solid(hip, "L", "leather", 9003, 1, edge=False)
    for face in hip.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "M3")
    for face in flaps(g, "gakti_skirt", 5, "P", "weave", 9004, top=10.6):
        stripes(face, BANDS, rows=range(2, 5))
