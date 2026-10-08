"""Goose Girl's Hitched-Hem Skirt: a skirt caught up on one side into a bunched swag at the hip, a striped
petticoat showing beneath, and bare feet for the wet meadow."""
from kit_female import skirt
from paint import fabric, k, solid

META = {
    "name": "Goose Girl's Hitched-Hem Skirt",
    "gender": "female",
    "description": "A skirt hitched up on one side into a bunched swag at the hip over a striped petticoat, bare feet and a ribbon at one ankle.",
    "tags": ["casual", "simple", "skirt"],
}


def petticoat(face, x0, x1, y0, seed):
    """The striped petticoat under the hitched corner: cream linen banded near the hem."""
    for y in range(y0, face.h):
        for x in range(x0, x1 + 1):
            from_hem = face.h - 1 - y
            key = "A2" if from_hem in (1, 3) else "A1" if from_hem == 0 else k("S", 3 if (x + y + seed) % 7 else 2)
            face.set(x, y, key)


def build(g):
    s = skirt(g, "P", "weave", 51020, top=9.8, length=11, flare=6)
    front = s.front.front
    # The outer skirt is drawn up toward the right hip: a slanted turned edge with the petticoat below it.
    for y in range(2, front.h):
        cut = max(0, round(6 - (front.h - 1 - y) * 0.7))   # columns hitched clear on this row
        if cut <= 0:
            continue
        petticoat(front, 0, cut - 1, y, 51021)
        front.set(cut, y, "P3")                                       # the lit turned edge
        if cut + 1 < front.w:
            front.set(cut + 1, y, "P1")
    right = s.right.right
    petticoat(right, 0, right.w - 1, 3, 51022)
    right.hline(0, right.w - 1, 2, "P3")
    for face in (s.right.front, s.right.back):
        petticoat(face, 0, face.w - 1, 3, 51023)
    for face in (s.back.back, s.left.left):
        face.hline(0, face.w - 1, face.h - 2, "P3"), face.hline(0, face.w - 1, face.h - 1, "P1")
    # The swag of gathered cloth tucked up into the waistband; it rides the front panel's hinge.
    swag = g.piece("waist_swag", "TORSO", (-4.9, -.3, -1.0), (3, 3, 1), pivot=(0, 9.8, -2.95), inflate=.18,
                   motion="flap_front")
    solid(swag, "P", "weave", 51024, 2)
    for x in range(3):
        swag.front.vline(x, 0, 2, k("P", 3 if x % 2 == 0 else 1))
    swag.front.set(1, 2, "P0")
    # Bare feet: nothing below the skirt but a ribbon tied round the left ankle.
    leg = g.part("left_leg")
    leg.strip.hline(0, leg.strip.w - 1, 9, "A2")
    leg.front.set(1, 10, "A1")
