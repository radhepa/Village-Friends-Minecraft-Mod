"""Plated Greaves: quilted chausses, steel shin plates and knee cops, armored boots."""
from paint import cap, fabric, grid, k, rivets, solid, strip_fabric

META = {
    "name": "Plated Greaves",
    "description": "Dark quilted chausses under steel greaves and poleyns, with leather sabatons.",
    "tags": ["armor", "sturdy", "martial"],
    # Plate legs only go with martial or rugged tops.
    "requires": ["martial", "rugged"],
}


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "quilt", 51 if side == "right" else 52, 1)
        fabric(leg.top, "P", "quilt", 5, 1)
        strip_fabric(leg, "L", "leather", 53, 2, 10, 11)
        leg.strip.hline(0, leg.strip.w - 1, 11, "K1")
        leg.bottom.fill("K1")
        # Steel greaves wrap the shin; the inner face stays quilted for flexibility.
        inner = pants.left if side == "right" else pants.right
        for face in pants.sides:
            if face is inner:
                continue
            fabric(face, "M", "smooth", 54, 2, 0, 6, face.w, 4)
            face.hline(0, face.w - 1, 6, "M3")
            face.hline(0, face.w - 1, 9, "M1")
        ridge = 1 if side == "right" else 2
        pants.front.vline(ridge, 6, 8, "M3")
        pants.front.set(ridge, 7, "M4")
        # Sabatons: leather boots with a steel toe cap.
        for face in pants.sides:
            fabric(face, "L", "leather", 55, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        pants.front.hline(0, 3, 10, "M2")
        pants.front.hline(0, 3, 11, "M1")
        pants.bottom.fill("K0")

        # Knee cop: a domed plate with a side wing.
        bone = "RIGHT_LEG" if side == "right" else "LEFT_LEG"
        knee = g.piece(f"{side}_poleyn", bone, (-2.5, 0, -1.0), (5, 3, 2), pivot=(0, 3.9, -1.6), rotation=(-8, 0, 0))
        solid(knee, "M", "smooth", 56, 2)
        cap(knee, "M", top_delta=2, bottom_delta=-1)
        knee.front.hline(1, 3, 0, "M3"), knee.front.set(2, 1, "M4"), knee.front.hline(0, 4, 2, "M1")
        wing_x = -3.1 if side == "right" else 2.1
        wing = g.piece(f"{side}_poleyn_wing", bone, (0, 0, -1.5), (1, 2, 3), pivot=(wing_x, 4.2, -.6))
        solid(wing, "M", "smooth", 57, 2)

    body = g.part("body")
    strip_fabric(body, "P", "quilt", 58, 1, 9, 11)
    fabric(body.bottom, "P", "quilt", 6, 1)
    belt = g.piece("waist_belt", "TORSO", (-4.6, 9.6, -2.6), (9, 2, 5), inflate=.04)
    solid(belt, "L", "leather", 59, 2)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    grid(belt.front, 3, 0, ["MMM", "MLM"], {"M": "M3", "L": "L0"})
