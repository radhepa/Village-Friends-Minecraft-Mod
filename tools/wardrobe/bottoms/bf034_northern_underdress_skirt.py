"""Northern Underdress Skirt: a long pale underdress skirt with a tablet-woven hem band and ankle-tied turnshoes."""
from kit import SIDES
from kit_female import shoes, skirt, trim

META = {
    "name": "Northern Underdress Skirt",
    "gender": "female",
    "description": "The long pale skirt of a northern underdress, a tablet-woven band at the hem and turnshoes tied at the ankle.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 13411, base=3, top=9.8, length=12)
    for face in s.faces:
        trim(face, face.h - 4, "lozenge" if face.w >= 5 else "line", "A2", "P2")
    s.hem("S2")
    shoes(g, "turnshoe", "L", 2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L1")
        pants.front.set(1, 10, "A2"), pants.front.set(2, 10, "A2")
