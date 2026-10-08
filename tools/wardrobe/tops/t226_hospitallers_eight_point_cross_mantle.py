"""Hospitaller's Eight-Point Cross Mantle: a closed black mantle with a white eight-pointed cross on the breast and a great one behind, fastened by a tasselled neck cord over a coloured tunic."""
from kit import body, neckline, sleeves
from kit_male import back_drape, shoulder_cape
from kit_m05 import cord_end, over_panels
from paint import grid

META = {
    "name": "Hospitaller's Eight-Point Cross Mantle",
    "gender": "male",
    "description": "A brother hospitaller's closed black mantle reaching the calf, a white eight-pointed cross on the breast and a great one across the back, fastened at the throat by a tasselled cord over a coloured tunic.",
    "tags": ["holy", "martial", "robe"],
    "covers_waist": True,
}

SMALL = [".aaa.",
         "a.a.a",
         "aaaaa",
         "a.a.a",
         ".aaa."]

GREAT = [".aaa.aaa.",
         "a.aaaaa.a",
         "aa.aaa.aa",
         "aaa.a.aaa",
         ".aaaaaaa.",
         "aaa.a.aaa",
         "aa.aaa.aa",
         "a.aaaaa.a",
         ".aaa.aaa."]


def build(g):
    b = body(g, "P", "weave", 35200)                                   # the tunic beneath
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 35201, rows=(0, 10), cuff="P1")
    mantle = body(g, "K", "weave", 35202, base=2, layer="jacket")
    f = mantle.front
    for x in (3, 4):
        f.clear(x, 0)
    f.set(2, 0, "K3"), f.set(5, 0, "K3")
    f.vline(1, 1, 11, "K1")                                             # deep folds either side
    f.vline(2, 8, 11, "K3")
    grid(f, 3, 2, SMALL, {"a": "S4"})                                   # the cross on the left breast
    f.set(5, 4, "S3")
    for face in (mantle.right, mantle.left):
        face.vline(1 if face is mantle.right else 2, 2, 11, "K1")
    mantle.back.vline(2, 1, 11, "K1"), mantle.back.vline(5, 1, 11, "K1")
    # The mantle's own wide half-sleeves over the tunic arms.
    for side in ("right", "left"):
        over = g.part(f"{side}_sleeve")
        for face in over.sides:
            for y in range(6):
                for x in range(face.w):
                    face.set(x, y, "K1" if (x + face.x0) % 4 == 0 else "K2")
            face.hline(0, face.w - 1, 5, "K0")
        over.top.fill("K3")
    cape = shoulder_cape(g, "mantle_shoulders", "K", "weave", 35203, length=2, width=11, depth=6)
    for face in cape.sides:
        face.hline(0, face.w - 1, 1, "K1")
    upper = back_drape(g, "mantle_back", "K", 11, "weave", 35204, width=9, y=1.4, z=3.0, tilt=3)
    grid(upper.back, 0, 1, GREAT, {"a": "S4"})                          # the great cross behind
    upper.back.hline(0, 8, 10, "K1")
    lower = back_drape(g, "mantle_hem", "K", 8, "weave", 35205, width=9, y=12.3, z=3.3, tilt=3, motion="flap_back")
    for x in (1, 4, 7):
        lower.back.vline(x, 0, 7, "K1")
    lower.back.hline(0, 8, 7, "K0")
    front, _, sides = over_panels(g, "mantle_front", 7, "K", "weave", 35206, top=11.0, width=10, sides=False)
    front.vline(4, 1, 6, "K0"), front.vline(5, 1, 6, "K3")             # where the two fronts meet
    for x in (1, 8):
        front.vline(x, 1, 6, "K1")
    front.hline(0, 9, 6, "K0")
    # Neck cord: knotted at the throat, two tasselled ends down the breast.
    for i, x in enumerate((-2.5, -1.5)):
        cord_end(g, f"neck_cord_{i}", (x, .3, -2.75), 5 - i, "S", 3, 35207 + i, knots=(1,), tassel="S1")
    knot = g.piece("neck_cord_knot", "TORSO", (-1.5, 0, -.5), (2, 1, 1), pivot=(-1.0, -.2, -2.75))
    knot.front.fill("S3"), knot.back.fill("S2"), knot.top.fill("S4"), knot.bottom.fill("S1")
    knot.left.fill("S2"), knot.right.fill("S2")
