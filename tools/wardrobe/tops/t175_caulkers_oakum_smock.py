"""Caulker's Oakum Smock: a short canvas smock with pitch-blackened cuffs and hem, a twisted skein of pale oakum hung
round the neck, a caulking iron thrust through the belt and a little pitch pot swinging at the hip."""
from kit import belt, body, neckline, sleeves
from kit_m03 import rope
from kit_male import blk
from paint import solid

META = {
    "name": "Caulker's Oakum Smock",
    "gender": "male",
    "description": "A short canvas smock blackened with pitch at cuffs and hem, a twisted skein of pale oakum round the neck, "
                   "a caulking iron through the belt and a pitch pot swinging at the hip.",
    "tags": ["work", "sea", "simple"],
    "covers_waist": True,
}

POT = (2.4, 10.0, -3.0)       # the pot's bail hangs from the belt here; pot and bail share the hinge
# Pitch wiped off on the smock front: (x, y) texels in two short downward strokes.
SMEARS = [(1, 6), (1, 7), (2, 8), (2, 9), (5, 7), (6, 8), (6, 9)]


def build(g):
    b = body(g, "P", "twill", 33160)
    neckline(b.front, "round", "P")
    b.front.vline(4, 1, 4, "P1")                                         # the neck slit
    for x, y in SMEARS:
        b.front.set(x, y, "K1")
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "K2")
    sleeves(g, "P", "twill", 33161, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm").strip
        arm.hline(0, 15, 9, "K2"), arm.hline(0, 15, 10, "K1")             # cuffs dark with pitch
        for x in (1, 5, 9, 13):
            arm.set(x, 8, "K2")
    belt(g, "belt", 9.4, height=1)
    # The oakum skein: a fat twist of tarry hemp fibre round the neck, both ends hanging down the chest.
    ring = g.piece("oakum_ring", "TORSO", (-3.5, -.9, -2.5), (7, 1, 5), inflate=.14)
    for face in ring.faces:
        rope(face, "S", 3, ox=face.x0)
    for i, x in enumerate((-2.0, 2.0)):
        end = g.piece(f"oakum_end_{i}", "TORSO", (-.5, 0, -.5), (1, 6, 1), pivot=(x, .1, -2.75), inflate=.12)
        for face in end.faces:
            rope(face, "S", 3, ox=face.x0 + i)
        end.strip.hline(0, end.strip.w - 1, 5, "S4")                     # the frayed end
    # The caulking iron, thrust through the belt with its flat bit up.
    shaft = blk(g, "caulking_iron", (-2.2, 8.0, -2.8), (1, 4, 1), "M", 2, "smooth", 33162)
    shaft.strip.hline(0, shaft.strip.w - 1, 3, "M1")
    bit = blk(g, "caulking_iron_bit", (-2.2, 7.2, -2.8), (2, 1, 1), "M", 3, "smooth", 33163, edge=False)
    bit.top.fill("M4")
    # The pitch pot: a small black pot on an iron bail, swinging with the stride.
    pot = blk(g, "pitch_pot", POT, (2, 2, 2), "K", 1, "smooth", 33164, origin=(-1, 1.0, -1), motion="flap_front")
    pot.top.fill("K0"), pot.top.set(0, 0, "K3")
    for face in pot.sides:
        face.hline(0, face.w - 1, 0, "M2")
    bail = blk(g, "pitch_pot_bail", POT, (2, 1, 1), "M", 1, "smooth", 33165, origin=(-1, 0, -.5),
               motion="flap_front", edge=False)
    bail.top.fill("M2")
    # The smock's short skirt below the belt.
    for name, z, motion, face_name in (("smock_front", -2.85, "flap_front", "front"), ("smock_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 11.2, z), motion=motion)
        solid(panel, "P", "twill", 33166 + (name == "smock_back"), 2)
        face = getattr(panel, face_name)
        face.hline(0, 8, 1, "K2"), face.hline(0, 8, 2, "K1")
        for x in (2, 5, 7):
            face.set(x, 0, "K2")
