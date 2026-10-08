"""Ditcher's Mud Smock: a heavy hemp smock caked in clay from the hem up, one front corner hitched into the belt, and an iron-shod spade on the back."""
from kit import belt, body, roll, sleeves
from kit_m01 import mud
from kit_male import blk
from paint import k, solid

META = {
    "name": "Ditcher's Mud Smock",
    "gender": "male",
    "description": "A heavy hemp smock caked thick with clay from the hem up, one front corner hitched into the belt to keep it out of the ditch, and an iron-shod spade slung down the back.",
    "tags": ["work", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 31500)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "P1"), f.set(5, 0, "P1"), f.vline(4, 1, 3, "P1")      # slit neck
    for face in b.sides:
        mud(face, 31501 + face.x0, 10, role="L", base=1, splash=.04)
    for face in (b.front, b.back):
        face.vline(2, 4, 9, "P1"), face.vline(5, 5, 9, "P1")              # heavy folds
    sleeves(g, "P", "twill", 31502, rows=(0, 5))
    roll(g, "P", 2.6, base=2)
    belt(g, "belt", 9.4, height=1)
    # Long hem, front split in two: the right half hangs full, the left corner hitched up into the belt.
    for i, (name, x0, w, length, z, motion, face_name) in enumerate((
            ("smock_front_r", -4.5, 5, 6, -2.85, "flap_front", "front"),
            ("smock_front_l", .5, 4, 3, -2.9, "flap_front", "front"),
            ("smock_back", -4.5, 9, 6, 1.85, "flap_back", "back"))):
        panel = g.piece(name, "TORSO", (x0, 0, 0), (w, length, 1), pivot=(0, 10.6, z), motion=motion)
        solid(panel, "P", "twill", 31503 + i, 2)
        for face in panel.faces:
            mud(face, 31506 + face.x0, max(0, length - 3), role="L", base=1, splash=.06)
        getattr(panel, face_name).hline(0, w - 1, length - 1, "L0")
    corner = g.piece("hitched_corner", "TORSO", (-2, 0, -1), (4, 2, 1), pivot=(2.5, 9.1, -2.95))
    solid(corner, "P", "twill", 31508, 2, edge=False)
    corner.front.hline(0, 3, 0, "P3"), corner.front.hline(0, 3, 1, "L1")    # the muddy hem tucked over the belt
    corner.front.set(1, 1, "L2"), corner.front.set(3, 0, "P1")
    # Clay clods stuck to the hem, riding with the panels they cling to.
    for i, (x, y, z, motion) in enumerate(((-3.1, 4.0, -2.85, "flap_front"), (-.9, 4.6, -2.85, "flap_front"),
                                           (2.6, 4.3, 1.85, "flap_back"))):
        dz = -1 if z < 0 else 1
        clod = g.piece(f"clay_clod_{i}", "TORSO", (x - .5, y, dz if dz > 0 else -1), (1, 1, 1), pivot=(0, 10.6, z),
                       motion=motion, inflate=.1)
        solid(clod, "L", "plain", 31509 + i, 1, edge=False)
        clod.top.fill("L2")
    # The spade down the back: ash shaft with a T-grip, a narrow wooden blade shod in iron.
    blk(g, "spade_grip", (-1.6, .6, 3.5), (3, 1, 1), "L", 3, "plain", 31510, edge=False)
    shaft = blk(g, "spade_shaft", (-1.6, 1.6, 3.5), (1, 5, 1), "L", 3, "plain", 31511, edge=False)
    for face in shaft.sides:
        face.set(0, 1, "L2"), face.set(0, 4, "L2")
    blade = blk(g, "spade_blade", (-1.6, 6.6, 3.5), (3, 3, 1), "L", 2, "plain", 31512)
    blade.back.vline(1, 0, 1, "L3"), blade.back.hline(0, 2, 2, "L1")
    shoe = blk(g, "spade_iron_shoe", (-1.6, 9.6, 3.5), (3, 1, 1), "M", 2, "smooth", 31513, edge=False)
    shoe.back.set(0, 0, "M3"), shoe.back.set(2, 0, k("M", 1))
