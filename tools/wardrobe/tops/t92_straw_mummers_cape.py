"""Straw Mummer's Cape: a festival guise of thatched straw falling from the shoulders to the hips, bound with ribbons."""
from kit import body, sleeves
from kit_male import blk, shoulder_cape

META = {
    "name": "Straw Mummer's Cape",
    "gender": "male",
    "description": "A midwinter guiser's cape of thatched straw falling in layers from shoulders to hips, bound with bright ribbons, straw at the wrists.",
    "tags": ["whimsical", "rugged"],
    "locked_to": "b92_straw_mummers_leg_bundles",
    "covers_waist": True,
}


def straw(face, offset=0, rows=None):
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            face.set(x, y, ("S2", "S3", "S4", "S3")[(x + face.x0 + offset + y // 3) % 4])
        if y % 3 == 2:
            for x in range(0, face.w, 2):
                face.set(x, y, "S1")                                     # layer edges of the thatch


def build(g):
    b = body(g, "P", "weave", 9201)
    sleeves(g, "P", "weave", 9202, rows=(0, 10))
    for side in ("right", "left"):
        straw(g.part(f"{side}_sleeve").strip, rows=range(8, 11))           # straw bound at the wrists
    cape = shoulder_cape(g, "straw_cape", "S", "plain", 9203, length=9, width=12, depth=7, y=-.9)
    for face in cape.faces:
        straw(face)
    for face in cape.sides:
        face.hline(0, face.w - 1, 2, "A2")                               # ribbon binding
    cape.front.vline(6, 3, 8, "S0")
    for i, (x, key) in enumerate(((-1.6, "A"), (1.6, "P"))):
        rib = blk(g, f"ribbon_{i}", (x, 1.6, -3.7), (1, 5, 1), key, 3, "plain", 9204 + i, motion="sway")
        rib.strip.hline(0, rib.strip.w - 1, 4, f"{key}1")
