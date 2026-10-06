"""Drawstring Smock: a loose cream smock with a laced neck, smocked chest and sleeves pushed up."""
from kit import body, neckline, roll, sleeves
from paint import k

META = {
    "name": "Drawstring Smock",
    "gender": "male",
    "description": "Loose smock gathered at a laced neck, smocked across the chest, sleeves pushed to the elbow.",
    "tags": ["casual", "simple"],
}


def build(g):
    b = body(g, "S", "weave", 1201, base=3)
    neckline(b.front, "laced", "S", base=3)
    # Smocking: tight gathers stitched across the chest.
    for face in (b.front, b.back):
        for x in range(face.w):
            if x not in (3, 4) or face is b.back:
                face.set(x, 2, "S2" if x % 2 else "S4")
                face.set(x, 3, "S4" if x % 2 else "S2")
        for x in (1, 6):
            face.vline(x, 4, 10, "S2")
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "S2")
    b.front.set(3, 1, "A2"), b.front.set(4, 1, "A2")   # drawstring ends
    sleeves(g, "S", "weave", 1202, base=3, rows=(0, 5))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for face in arm.sides:
            face.vline(1, 1, 4, "S2")
    roll(g, "S", 2.6, base=3)
    tie = g.piece("drawstring", "TORSO", (0, 0, -.5), (1, 3, 1), pivot=(-.6, .8, -2.6), rotation=(0, 0, 12))
    for face in tie.faces:
        face.fill("A2")
    tie.front.set(0, 2, "A3")
