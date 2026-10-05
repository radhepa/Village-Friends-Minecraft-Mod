"""Scholar's Slacks: slim pressed trousers, a narrow belt and soft leather shoes."""
from paint import fabric, grid, solid, strip_fabric

META = {
    "name": "Scholar's Slacks",
    "description": "Slim pressed trousers with a narrow belt and soft buckled shoes.",
    "tags": ["tailored", "slim", "scholarly"],
}


def build(g):
    for side in ("right", "left"):
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "P", "weave", 91 if side == "right" else 92, 1, 0, 9)
        fabric(leg.top, "P", "weave", 9, 1)
        crease = 1 if side == "right" else 2
        leg.front.vline(crease, 1, 9, "P2")
        leg.back.vline(3 - crease, 2, 8, "P2")
        leg.strip.hline(0, leg.strip.w - 1, 9, "P0")
        # Soft shoes: a pale stocking line, then leather with a little metal buckle.
        leg.strip.hline(0, leg.strip.w - 1, 10, "S3")
        strip_fabric(leg, "L", "leather", 93, 1, 11, 11)
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            fabric(face, "L", "leather", 94, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "L1")
        pants.front.hline(0, 3, 10, "L3")
        pants.front.set(1 if side == "right" else 2, 10, "M3")
        leg.bottom.fill("K1"), pants.bottom.fill("K1")

    body = g.part("body")
    strip_fabric(body, "P", "weave", 95, 1, 9, 11)
    fabric(body.bottom, "P", "weave", 10, 1)
    belt = g.piece("waist_belt", "TORSO", (-4.55, 10.0, -2.55), (9, 1, 5), inflate=.03)
    solid(belt, "L", "leather", 96, 1, edge=False)
    belt.front.set(4, 0, "M3")
