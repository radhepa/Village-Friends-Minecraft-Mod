"""Squire's Quartered Jupon: a quilted jupon in quartered colours, scalloped at the hem, with a low sword belt and scabbard."""
from kit import body, sleeves
from kit_male import blk
from paint import solid

META = {
    "name": "Squire's Quartered Jupon",
    "gender": "male",
    "description": "A padded jupon quilted in vertical channels and quartered in his lord's colours, scalloped hem, low sword belt and scabbard.",
    "tags": ["martial", "fancy"],
    "covers_waist": True,
}


def channels(face, role, x0=0):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, f"{role}1" if (x + x0) % 2 else f"{role}2")


def build(g):
    body(g, "S", "quilt", 5901, base=2)
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        for y in range(12):
            for x in range(8):
                role = "P" if (x < 4) == (y < 6) else "A"
                face.set(x, y, f"{role}1" if x % 2 else f"{role}2")
    jacket.front.hline(2, 5, 0, None)
    for face in (jacket.right, jacket.left):
        channels(face, "P")
    channels(jacket.top, "P")
    jacket.top.hline(2, 5, 2, None), jacket.top.hline(2, 5, 3, None)
    sleeves(g, "P", "quilt", 5902, rows=(0, 10), cuff="A2")
    hip = g.piece("sword_belt", "TORSO", (-4.6, 10.6, -2.6), (9, 1, 5), inflate=.08)
    solid(hip, "L", "leather", 5903, 1, edge=False)
    for face in hip.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "M3")                                         # belt plaques
    scab = blk(g, "scabbard", (4.7, 11.2, -.6), (1, 9, 1), "L", 1, "leather", 5904, rotation=(14, 0, 0))
    scab.strip.hline(0, scab.strip.w - 1, 8, "M3")
    blk(g, "sword_grip", (4.7, 9.2, -1.1), (1, 2, 1), "L", 3, "plain", 5905, rotation=(14, 0, 0))
    blk(g, "sword_guard", (4.7, 10.9, -.8), (1, 1, 3), "M", 3, "smooth", 5906, rotation=(14, 0, 0), edge=False)
    for name, z, motion, face_name, role in (("jupon_front", -2.85, "flap_front", "front", "A"),
                                              ("jupon_back", 1.85, "flap_back", "back", "P")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 11.6, z), motion=motion)
        solid(panel, role, "plain", 5907, 2)
        face = getattr(panel, face_name)
        for x in range(9):
            face.set(x, 0, "P2" if x < 4 else "A2")
            face.set(x, 1, "P1" if x < 4 else "A1")
            face.set(x, 2, ("P2" if x < 4 else "A2") if x % 2 == 0 else "S3")  # scallops
