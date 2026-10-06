"""Herald's Livery Tabard: a quartered tabard with flat winged sleeves, charged with gold bezants, and a chain of office."""
from kit import body, sleeves
from kit_male import arm_blk, check
from paint import grid, solid

META = {
    "name": "Herald's Livery Tabard",
    "gender": "male",
    "description": "A herald's quartered tabard with flat winged sleeves, charged with gold bezants, worn with a chain of office.",
    "tags": ["fancy", "tailored"],
    "locked_to": "b56_heralds_parti_hose",
    "covers_waist": True,
}

BEZANT = ["ab",
          "bb"]


def quarters(face, top_row=0):
    """Primary and accent quarters, the primary fields edged a shade darker."""
    w, h = face.w, face.h
    for y in range(h):
        for x in range(w):
            upper = (y + top_row) < 6
            left = x < w // 2
            face.set(x, y, "P2" if upper == left else "A2")
    for y in range(h):
        for x in range(w):
            if face.get(x, y) == "P2" and (x in (0, w - 1) or y in (0, h - 1)):
                face.set(x, y, "P1")


def build(g):
    b = body(g, "S", "weave", 5601, base=3)
    sleeves(g, "S", "weave", 5602, base=3, rows=(0, 10), cuff="S2")
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        quarters(face)
        grid(face, 1, 2, BEZANT, {"a": "M4", "b": "M3"}), grid(face, 5, 8, BEZANT, {"a": "M4", "b": "M3"})
    jacket.front.hline(2, 5, 0, None), jacket.front.hline(3, 4, 1, None)
    check(jacket.top, "P2", "A2", size=4)
    jacket.top.hline(2, 5, 1, None), jacket.top.hline(2, 5, 2, None)
    for i, side in enumerate(("right", "left")):
        wing = arm_blk(g, f"{side}_tabard_wing", side, -2.2, (5, 4, 5), "P", 2, "plain", 5603 + i, inflate=.1)
        for face in wing.sides:
            check(face, "P2" if side == "right" else "A2", "A2" if side == "right" else "P2", size=2)
            face.hline(0, face.w - 1, 3, "S3")
    for name, z, motion, face_name in (("tabard_front", -2.85, "flap_front", "front"),
                                        ("tabard_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4, 0, 0), (8, 5, 1), pivot=(0, 11.4, z), motion=motion)
        solid(panel, "A", "plain", 5605, 2)
        face = getattr(panel, face_name)
        quarters(face, top_row=6)
        face.hline(0, 7, 4, "S3")
    chain = g.piece("chain_of_office", "TORSO", (-4.6, -.4, -2.7), (9, 1, 5), inflate=.08)
    for face in chain.faces:
        for x in range(face.w):
            for y in range(face.h):
                face.set(x, y, "M3" if (x + y) % 2 else "M1")
