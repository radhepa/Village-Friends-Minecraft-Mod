"""Forager's Bramble-Torn Skirt: a calf skirt whose hem has been torn into uneven tatters by thorns, with
rips, caught burrs, wool leg wraps and soft turnshoes."""
from kit import SIDES
from kit_female import SKIRT_BACK, SKIRT_FRONT, shoes, skirt, wraps
from paint import solid

META = {
    "name": "Forager's Bramble-Torn Skirt",
    "gender": "female",
    "description": "A calf-length wool skirt torn by brambles into an uneven tattered hem, rips and caught burrs, "
                   "over wool leg wraps and soft turnshoes.",
    "tags": ["casual", "rugged", "skirt"],
}

TOP, LENGTH = 9.8, 8
# Tatters below each panel: (x from the panel's edge, width, length).
TATTERS = {"front": [(0, 2, 2), (2, 1, 1), (4, 2, 3), (7, 2, 1), (9, 1, 2)],
           "back": [(0, 1, 1), (1, 2, 3), (4, 1, 2), (6, 2, 1), (8, 2, 2)]}


def build(g):
    s = skirt(g, "P", "weave", 57421, top=TOP, length=LENGTH, side_length=7, flare=6)
    for face in s.wide_faces:
        for x, y0 in ((2, LENGTH - 3), (7, LENGTH - 2)):
            face.vline(x, y0, LENGTH - 1, "P0")                      # rips from the hem
        face.set(5, 2, "L1"), face.set(5, 3, "L0")                       # a caught burr
    for name, z, motion in (("front", SKIRT_FRONT, "flap_front"), ("back", SKIRT_BACK, "flap_back")):
        for i, (x, w, length) in enumerate(TATTERS[name]):
            t = g.piece(f"skirt_tatter_{name}_{i}", "TORSO", (x - 5, LENGTH, -.02 if name == "front" else .02),
                        (w, length, 1), pivot=(0, TOP, z), motion=motion)
            solid(t, "P", "weave", 57422 + i, 1)
            face = t.front if name == "front" else t.back
            face.hline(0, w - 1, length - 1, "P0")
    for box in (s.right, s.left):
        for face in box.sides:
            face.set(1, face.h - 1, "P0"), face.set(3, face.h - 1, "P0")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        wraps(leg.strip, 6, 9, "S", 2, step=4)
    shoes(g, "turnshoe", "L", 2)
