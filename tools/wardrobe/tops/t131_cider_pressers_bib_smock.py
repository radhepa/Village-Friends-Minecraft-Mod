"""Cider Presser's Bib Smock: a rolled-sleeve smock under a halter-tied canvas bib blotched with apple juice, apples in its pocket and a wooden pomace scoop at the hip."""
from kit import body, neckline, roll, sleeves
from kit_m01 import stains
from kit_male import blk
from paint import k, solid

META = {
    "name": "Cider Presser's Bib Smock",
    "gender": "male",
    "description": "A rolled-sleeve smock under a canvas bib tied round the neck, blotched with apple juice and pulp, two apples riding in its pocket and a wooden pomace scoop hooked at the hip.",
    "tags": ["work", "casual", "apron"],
    "covers_waist": True,
}

APRON_Z, APRON_TOP = -3.15, 10.4


def build(g):
    b = body(g, "P", "weave", 31625)
    neckline(b.front, "round", "P")
    for face in (b.right, b.left):
        face.vline(1, 2, 11, "P1")
    sleeves(g, "P", "weave", 31626, rows=(0, 5))
    roll(g, "P", 2.6, base=3)
    # The bib on the jacket layer: canvas from the chest down, tied round the neck by a cord.
    jacket = g.part("jacket")
    f = jacket.front
    for y in range(2, 12):
        for x in range(1, 7):
            f.set(x, y, "S3")
    f.hline(1, 6, 2, "S4")
    f.vline(1, 3, 11, "S2"), f.vline(6, 3, 11, "S2")
    stains(f, "L1", 31627, .05, rows=range(4, 12), cols=range(1, 7), cell=2, blot=.82)
    stains(f, "A1", 31628, .03, rows=range(5, 12), cols=range(2, 6), cell=2, blot=.9)
    f.set(1, 1, "L2"), f.set(6, 1, "L2"), f.set(0, 0, "L2"), f.set(7, 0, "L2")   # halter cord
    jacket.top.vline(0, 1, 3, "L2"), jacket.top.vline(7, 1, 3, "L2")
    jacket.back.hline(0, 7, 8, "S2"), jacket.back.hline(0, 7, 9, "S1")         # the waist tie behind
    for face in (jacket.right, jacket.left):
        face.hline(0, 3, 8, "S2")
    # The bib's pocket, two apples riding in it.
    pocket = blk(g, "bib_pocket", (0, 6.0, -2.55), (4, 2, 1), "S", 2, "weave", 31629)
    pocket.front.hline(0, 3, 0, "S4"), pocket.front.vline(2, 1, 1, "S1")
    stains(pocket.front, "L1", 31630, .1, cell=2, blot=.9)
    for i, x in enumerate((-.9, .8)):
        apple = blk(g, f"pocket_apple_{i}", (x, 5.2, -2.7), (1, 1, 1), "A", 2 + i, "plain", 31631 + i, edge=False,
                    inflate=.15)
        apple.top.fill("A3" if i == 0 else "A4"), apple.top.set(0, 0, "L2")
    # The apron's lower half, an over-layer that lies over any skirt.
    for name, z, motion, face_name in (("bib_apron_front", APRON_Z, "flap_front", "front"),):
        panel = g.piece(name, "TORSO", (-3, 0, 0), (6, 5, 1), pivot=(0, APRON_TOP, z), motion=motion)
        solid(panel, "S", "weave", 31633, 3, edge=False)
        face = getattr(panel, face_name)
        face.vline(0, 0, 4, "S2"), face.vline(5, 0, 4, "S2"), face.hline(0, 5, 4, "S1")
        stains(face, "L1", 31634, .06, rows=range(0, 4), cell=2, blot=.8)
        stains(face, "A1", 31635, .04, rows=range(1, 4), cell=2, blot=.88)
    for name, z, motion, face_name in (("smock_hem_front", -2.85, "flap_front", "front"),
                                        ("smock_hem_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 10.8, z), motion=motion)
        solid(panel, "P", "weave", 31636 + (z > 0), 2, edge=False)
        getattr(panel, face_name).hline(0, 8, 2, k("P", 1))
    # A wooden pomace scoop hooked on the apron string at the right hip, swinging with the hem.
    handle = g.piece("pomace_scoop_handle", "TORSO", (-3.9, 0, -1), (1, 3, 1), pivot=(0, APRON_TOP, -3.25),
                     motion="flap_front")
    solid(handle, "L", "plain", 31638, 3, edge=False)
    bowl = g.piece("pomace_scoop_bowl", "TORSO", (-4.4, 3, -2), (2, 2, 2), pivot=(0, APRON_TOP, -3.25),
                   motion="flap_front")
    solid(bowl, "L", "plain", 31639, 3, edge=False)
    bowl.top.fill("L1")
    bowl.front.set(0, 0, "L4"), bowl.front.hline(0, 1, 1, "L2")
