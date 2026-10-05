"""Minstrel's Doublet: a laced, slashed doublet with puffed shoulders, a peplum and a half-cape."""
from paint import cap, fabric, grid, k, solid, strip_fabric

META = {
    "name": "Minstrel's Doublet",
    "description": "Front-laced doublet with slashed puffed shoulders, a scalloped peplum and a jaunty half-cape.",
    "tags": ["whimsical", "fancy"],
}


def build(g):
    body = g.part("body")
    strip_fabric(body, "P", "velvet", 191, 2)
    cap(body, "P", texture="velvet", seed=191)
    f, b = body.front, body.back
    # Laced front: cream placket with accent cross-lacing.
    for y in range(1, 10):
        f.set(3, y, "S3"), f.set(4, y, "S2")
    for y in range(1, 10, 2):
        f.set(3, y, "A2"), f.set(4, y + 1, "A2")
    f.vline(2, 1, 9, "P3"), f.vline(5, 1, 9, "P1")
    f.hline(2, 5, 0, "S4")
    # Slashed panes on the chest and back.
    for face in (f, b):
        for x in (0, 7):
            for y in (2, 3, 5, 6):
                face.set(x, y, "S3" if y % 3 else "S2")
    for face in body.sides:
        face.hline(0, face.w - 1, 10, "P1")
        face.hline(0, face.w - 1, 11, "P0")

    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "velvet", 192, 2, 0, 10)
        fabric(arm.top, "P", "velvet", 192, 3)
        for face in arm.sides:
            face.vline(1, 5, 8, "P3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S4")
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        puff = g.piece(f"{side}_shoulder_puff", bone, (ox - .6, -2.4, -2.6), (5, 4, 5), inflate=.05)
        for face in puff.sides:
            for x in range(face.w):
                pane = x % 2 == 0
                for y in range(face.h):
                    face.set(x, y, ("P2" if y < 3 else "P1") if pane else ("S3" if y < 3 else "S2"))
        fabric(puff.top, "P", "velvet", 193, 3)
        puff.bottom.fill("P0")
        for face in puff.sides:
            face.hline(0, face.w - 1, 3, "A2")

    # Scalloped peplum around the waist.
    for name, z, motion, face_name in (("peplum_front", -2.75, "flap_front", "front"), ("peplum_back", 1.75, "flap_back", "back")):
        peplum = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 2, 1), pivot=(0, 11.0, z), motion=motion)
        solid(peplum, "P", "velvet", 194, 2)
        face = getattr(peplum, face_name)
        for x in range(9):
            face.set(x, 1, "A2" if x % 3 == 1 else "P1")

    # Half-cape thrown over the left shoulder, lined in accent.
    cape = g.piece("half_cape", "TORSO", (0, 0, 0), (5, 10, 1), pivot=(-.2, -.4, 2.35), rotation=(6, 0, -3))
    solid(cape, "S", "weave", 195, 2)
    cape.back.vline(0, 0, 9, "S1"), cape.back.vline(2, 2, 8, "S3")
    cape.back.hline(0, 4, 9, "A2")
    cape.front.fill("A1")
    shoulder = g.piece("half_cape_shoulder", "TORSO", (0, 0, -2.6), (5, 2, 6), pivot=(3.6, -.7, 0), rotation=(0, 0, 10))
    solid(shoulder, "S", "weave", 196, 2)
    fabric(shoulder.top, "S", "weave", 196, 3)
    for face in shoulder.sides:
        face.hline(0, face.w - 1, 1, "A2")
    clasp = g.piece("half_cape_clasp", "TORSO", (-.5, -.5, -.5), (1, 1, 1), pivot=(2.6, .5, -2.75), inflate=.1)
    solid(clasp, "M", "smooth", 197, 3, edge=False)
