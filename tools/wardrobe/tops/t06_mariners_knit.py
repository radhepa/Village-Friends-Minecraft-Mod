"""Mariner's Knit: a chunky cream gansey with chest bands, a cable panel, roll neck and patched elbows."""
from paint import cap, fabric, k, solid, strip_fabric

META = {
    "name": "Mariner's Knit",
    "description": "Chunky knit sweater with banded chest, cable panel, roll neck, ribbed hem and elbow patches.",
    "tags": ["knit", "casual", "simple"],
    "covers_waist": True,
}


def cable(face, x0, y0, y1):
    """A two-column braided cable."""
    for y in range(y0, y1 + 1):
        a, b = ("S4", "S1") if y % 3 == 0 else ("S1", "S4") if y % 3 == 1 else ("S3", "S3")
        face.set(x0, y, a), face.set(x0 + 1, y, b)


def build(g):
    body = g.part("body")
    strip_fabric(body, "S", "knit", 121, 2)
    cap(body, "S", texture="knit", seed=121, base=3)
    for face in body.sides:
        for y, key in ((2, "P3"), (3, "P2"), (4, "P2"), (5, "A2")):
            for x in range(face.w):
                face.set(x, y, k(key[0], int(key[1]) - (1 if x % 2 and key[0] == "P" and y == 4 else 0)))
        fabric(face, "S", "rib", 122, 2, 0, 10, face.w, 2)
    cable(body.front, 3, 6, 9)
    body.front.vline(2, 6, 9, "S1"), body.front.vline(5, 6, 9, "S1")
    cable(body.back, 3, 6, 9)

    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "knit", 123, 2, 0, 9)
        fabric(arm.top, "S", "knit", 123, 3)
        arm.strip.hline(0, arm.strip.w - 1, 2, "P2")
        arm.strip.hline(0, arm.strip.w - 1, 3, "P2")
        fabric(arm.strip, "S", "rib", 124, 2, 0, 9, arm.strip.w, 2)
        # Primary elbow patches on the outer face.
        outer = arm.right if side == "right" else arm.left
        outer.rect(1, 5, 2, 2, "P1")
        outer.set(1, 5, "P2")
        arm.back.rect(1, 5, 2, 2, "P1")

    neck = g.piece("roll_neck", "TORSO", (-4.5, -1.3, -2.6), (9, 2, 5), inflate=.08)
    solid(neck, "S", "rib", 125, 2)
    fabric(neck.top, "S", "rib", 125, 3)
    for face in neck.sides:
        face.hline(0, face.w - 1, 0, None)
        fabric(face, "S", "rib", 126, 3, 0, 0, face.w, 1)
    hem = g.piece("ribbed_hem", "TORSO", (-4.4, 10.1, -2.5), (9, 2, 5), inflate=.05)
    solid(hem, "S", "rib", 127, 2)
