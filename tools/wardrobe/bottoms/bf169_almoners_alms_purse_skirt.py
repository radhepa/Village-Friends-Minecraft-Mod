"""Almoner's Alms-Purse Skirt: an ankle-length skirt with a guard band at the hem, and a corded belt hung
with three drawstring alms purses, coins showing at their gathered mouths."""
from kit_female import OVER_FRONT, shoes, side_pouch, skirt, waist_belt
from paint import solid

META = {
    "name": "Almoner's Alms-Purse Skirt",
    "gender": "female",
    "description": "An ankle-length skirt with a guard band, and a cord belt hung with three drawstring alms purses showing coins.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def purse(box, role="A"):
    """A drawstring purse: a gathered mouth with a coin peeping out, a plump body, a dark base."""
    for face in box.sides:
        for y in range(face.h):
            face.hline(0, face.w - 1, y, f"{role}{2 if y else 3}")
        face.hline(0, face.w - 1, face.h - 1, f"{role}1")
        for x in range(face.w):
            if x % 2:
                face.set(x, 0, f"{role}1")                              # the drawstring's gathers
    box.top.fill("M3")                                                  # coins at the mouth
    box.bottom.fill(f"{role}0")


def build(g):
    s = skirt(g, "P", "weave", 55271, base=1, top=9.8, length=11, back_length=11, flare=5)
    s.band(2, "line", "A2", from_bottom=True)
    s.band(1, "line", "A1", from_bottom=True)
    s.band(0, "line", "P0", from_bottom=True)
    shoes(g, "turnshoe", "L", 2)
    cord = waist_belt(g, "waist_cord", 9.4, role="L", base=2, height=1, buckle=None, texture="plain")
    for face in cord.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "L1")                                        # a twisted cord
    for side, role in (("right", "A"), ("left", "S")):
        p = side_pouch(g, f"waist_purse_{side}", side, 9.9, size=(2, 3, 2), role="L")
        purse(p, role)
    # The front purse hangs from the cord's knot and rides the stride in front of the skirt.
    knot = g.piece("waist_cord_knot", "TORSO", (-.5, 0, -.3), (1, 1, 1), pivot=(-1.2, 9.4, OVER_FRONT - .1))
    solid(knot, "L", "plain", 55272, 2, edge=False)
    string = g.piece("waist_purse_string", "TORSO", (-.5, 1, -.2), (1, 1, 1), pivot=(-1.2, 9.4, OVER_FRONT - .1),
                     motion="flap_front")
    solid(string, "L", "plain", 55273, 1, edge=False)
    front = g.piece("waist_purse_front", "TORSO", (-1, 2, -.25), (2, 3, 1), pivot=(-1.2, 9.4, OVER_FRONT - .1),
                    motion="flap_front")
    purse(front, "A")
