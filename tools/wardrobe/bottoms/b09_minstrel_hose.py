"""Minstrel Hose: parti-colored hose under paned trunk hose, with pointed buckled shoes."""
from paint import cap, fabric, k, solid, strip_fabric

META = {
    "name": "Minstrel Hose",
    "description": "One solid and one striped leg, puffed paned trunk hose and curled pointed shoes.",
    "tags": ["whimsical", "slim", "fancy"],
    # Too fine for plate armor or a smith's apron.
    "rejects": ["armor", "work"],
}


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        if side == "right":
            strip_fabric(leg, "P", "velvet", 201, 2, 0, 10)
        else:
            for y in range(11):
                for x in range(leg.strip.w):
                    leg.strip.set(x, y, "S3" if (y // 2) % 2 == 0 else "P2")
        fabric(leg.top, "P", "velvet", 202, 2)
        if side == "right":
            leg.front.vline(1, 1, 9, "P3")
        # Pointed shoes with a buckle; the curled toe is a 3D piece.
        strip_fabric(leg, "L", "smooth", 203, 2, 11, 11)
        for face in pants.sides:
            fabric(face, "L", "smooth", 204, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 10, "L3")
        pants.front.set(1, 10, "M3"), pants.front.set(2, 10, "M3")
        leg.bottom.fill("K1"), pants.bottom.fill("K1")
        bone = "RIGHT_LEG" if side == "right" else "LEFT_LEG"
        toe = g.piece(f"{side}_shoe_toe", bone, (-1.5, 0, -2), (3, 1, 2), pivot=(0, 11.1, -2.2))
        solid(toe, "L", "smooth", 205, 2, edge=False)
        fabric(toe.top, "L", "smooth", 205, 3)
        curl = g.piece(f"{side}_shoe_curl", bone, (-.5, -1, -1), (1, 1, 1), pivot=(0, 11.5, -4.1), rotation=(-30, 0, 0))
        solid(curl, "L", "smooth", 206, 3, edge=False)

    body = g.part("body")
    strip_fabric(body, "P", "velvet", 207, 2, 9, 11)
    fabric(body.bottom, "P", "velvet", 20, 1)
    # Puffed trunk hose: alternating primary panes and cream puffs.
    trunk = g.piece("trunk_hose", "TORSO", (-4.6, 10.2, -2.6), (9, 4, 5), inflate=.08)
    for face in trunk.sides:
        for x in range(face.w):
            pane = x % 2 == 0
            for y in range(face.h):
                key = ("P2" if 0 < y < 3 else "P1") if pane else ("S3" if 0 < y < 3 else "S2")
                face.set(x, y, key)
        face.hline(0, face.w - 1, 0, "P3")
        face.hline(0, face.w - 1, 3, "P0")
    fabric(trunk.top, "P", "velvet", 208, 2)
    trunk.bottom.fill("P0")
