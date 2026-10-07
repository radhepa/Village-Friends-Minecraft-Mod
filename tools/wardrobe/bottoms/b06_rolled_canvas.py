"""Rolled Canvas: trousers rolled to mid-shin, glossy wading boots and a knotted rope belt."""
from paint import cap, fabric, k, rnd, solid, strip_fabric

META = {
    "name": "Rolled Canvas",
    "gender": "male",
    "description": "Canvas trousers rolled to the shin over glossy wading boots, held by a knotted rope.",
    "tags": ["rugged", "simple", "sea"],
}


def rope(face, seed):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, "S3" if (x + y) % 3 == 0 else "S2" if (x + y) % 3 == 1 else "S1")


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "twill", 131 if side == "right" else 132, 2, 0, 6)
        fabric(leg.top, "P", "twill", 13, 2)
        leg.front.set(1 if side == "right" else 2, 2, "P1"), leg.front.set(0 if side == "right" else 3, 3, "P1")
        # Glossy wading boots from mid-shin down.
        strip_fabric(leg, "L", "smooth", 133, 1, 7, 11)
        for face in pants.sides:
            fabric(face, "L", "smooth", 134, 1, 0, 7, face.w, 5)
            face.hline(0, face.w - 1, 7, "L2")
            face.hline(0, face.w - 1, 11, "K0")
        pants.front.vline(1 if side == "right" else 2, 8, 10, "L3")
        pants.front.set(1 if side == "right" else 2, 8, "L4")
        leg.bottom.fill("K0"), pants.bottom.fill("K0")
        bone = "RIGHT_LEG" if side == "right" else "LEFT_LEG"
        roll = g.piece(f"{side}_trouser_roll", bone, (-2.5, 5.6, -2.5), (5, 2, 5))
        solid(roll, "P", "twill", 135, 3)
        for face in roll.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 1, "P1")
            if face.name in ("right", "left"):
                face.set(face.w // 2, 1, "S2")

    body = g.part("body")
    strip_fabric(body, "P", "twill", 136, 2, 9, 11)
    fabric(body.bottom, "P", "twill", 14, 1)
    belt = g.piece("waist_rope", "TORSO", (-4.55, 9.9, -2.55), (9, 1, 5), inflate=.04)
    for face in belt.faces:
        rope(face, 137)
    knot = g.piece("waist_rope_knot", "TORSO", (-1, 0, -1), (2, 2, 1), pivot=(2.4, 10.2, -2.0))
    for face in knot.faces:
        rope(face, 138)
    for name, x, length in (("waist_rope_end_a", 1.9, 3), ("waist_rope_end_b", 2.9, 2)):
        end = g.piece(name, "TORSO", (0, 0, -.5), (1, length, 1), pivot=(x, 11.0, -2.75), rotation=(0, 0, 6))
        for face in end.faces:
            rope(face, 139)
        end.front.set(0, length - 1, "S1")
