"""Man-at-Arms' Long Gambeson: a thigh-length gambeson quilted in tall channels, a high padded collar and laced cuffs."""
from kit import belt, body, collar, flaps, sleeves
from kit_male import lacing

META = {
    "name": "Man-at-Arms' Long Gambeson",
    "gender": "male",
    "description": "A thigh-length soldier's gambeson quilted in tall vertical channels, with a high padded collar, laced cuffs and a plain belt.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}


def channels(face, base=2):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, f"S{base - 1}" if x % 2 else f"S{base}")


def build(g):
    b = body(g, "S", "quilt", 7101, base=2)
    for face in b.sides:
        channels(face)
    b.front.vline(4, 0, 11, "S0")
    for y in (2, 5, 8):
        b.front.set(3, y, "L2"), b.front.set(5, y, "L2")                 # laced closures
    sleeves(g, "S", "quilt", 7102, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in range(9):
            for x in range(arm.strip.w):
                arm.strip.set(x, y, "S1" if (y % 3 == 2) else "S2")         # quilted rings round the arm
        lacing(arm.front, 1, 8, 10, "L3", "L1")
    high = collar(g, "padded_collar", "S", "quilt", base=2, height=2, y=-1.2)
    for face in high.sides:
        channels(face)
        face.hline(0, face.w - 1, 0, "S3")
    belt(g, "belt", 9.4, height=1)
    for face in flaps(g, "gambeson_skirt", 5, "S", "quilt", 7103, top=10.6, slit=True):
        channels(face)
        face.vline(4, 1, 4, "S0")
        face.hline(0, 8, 4, "S1")
