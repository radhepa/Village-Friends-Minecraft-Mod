"""Cockle Gatherer's Tucked Petticoat: her wool skirt rolled up all round and tucked into a fat roll at the
hips, leaving a short tucked linen petticoat over bare knees and bare feet for the wet sands."""
from kit_female import skirt
from paint import k, solid

META = {
    "name": "Cockle Gatherer's Tucked Petticoat",
    "gender": "female",
    "description": "A wool skirt rolled up all round into a fat roll at the hips over a short tucked petticoat, bare knees and bare feet for the sands.",
    "tags": ["sea", "work", "relaxed", "skirt"],
}

SEED = 53105


def build(g):
    s = skirt(g, "S", "weave", SEED, base=3, top=10.2, length=6, side_length=5, flare=7, folds=False)
    for face in s.faces:
        for y in (2, 4):                                             # two sewn tucks round the petticoat
            face.hline(0, face.w - 1, y, "S4")
            face.hline(0, face.w - 1, y + 1, "S2")
        face.hline(0, face.w - 1, face.h - 1, "S2")
    for box in (s.right, s.left):
        for face in (box.front, box.back):
            face.hline(0, face.w - 1, face.h - 1, "S2")
    # The overskirt, rolled up and tucked in all round: a fat bunched roll riding on the hips.
    roll = g.piece("waist_skirt_roll", "TORSO", (-5, 0, -3.1), (10, 3, 6), pivot=(0, 8.7, 0), inflate=.2)
    solid(roll, "P", "weave", SEED + 1, 2, edge=False)
    for x in range(roll.strip.w):                                     # a twisted roll: lit crown, shaded belly
        for y, base in ((0, 3), (1, 2), (2, 1)):
            twist = (x + y) % 4 == 0
            roll.strip.set(x, y, k("P", base - 1 if twist else base))
    roll.bottom.fill("P0")
    # Where the skirt is pushed through the roll at the back, a bunched tail of cloth.
    tail = g.piece("waist_skirt_bunch", "TORSO", (-2, 0, 0), (4, 2, 1), pivot=(0, 10.6, 3.15), motion="flap_back")
    solid(tail, "P", "weave", SEED + 2, 2)
    for x in range(4):
        tail.back.set(x, 0, "P3" if x % 2 else "P1")
    tail.back.hline(0, 3, 1, "P1")
