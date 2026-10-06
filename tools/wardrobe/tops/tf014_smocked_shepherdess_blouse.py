"""Smocked Shepherdess Blouse: a blouse with a honeycomb-smocked yoke under a short fleece-lined bolero, a horn at her back."""
from kit_female import chemise, fur, smocking, sub
from paint import fabric, solid

META = {
    "name": "Smocked Shepherdess Blouse",
    "gender": "female",
    "description": "A honeycomb-smocked linen blouse under a fleece-lined sheepskin bolero, with a herding horn on a cord.",
    "tags": ["casual", "rugged"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 11401, neckline="round", sleeve_rows=(0, 11), gather=False)
    smocking(body.front, "S", 3, 0, 1, 8, 3)
    smocking(body.back, "S", 3, 0, 0, 8, 3)
    for face in (body.front, body.back):
        for x in range(0, 8, 4):
            face.set(x + 1, 2 if face is body.front else 1, "A2")    # coloured smocking stitches
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2")
        smocking(arm.strip, "S", 3, 0, 8, 16, 2)
        arm.strip.hline(0, 15, 11, "S4")
    j = g.part("jacket")
    for face in (j.front,):
        fabric(face, "L", "leather", 11402, 2, 0, 0, 3, 8)
        fabric(face, "L", "leather", 11402, 2, 5, 0, 3, 8)
        fur(sub(face, 2, 0, 1, 8), "S", 11403, 3)
        fur(sub(face, 5, 0, 1, 8), "S", 11403, 3)
        face.set(1, 4, "M3"), face.set(6, 4, "M3")                 # horn toggles
    for face in (j.right, j.left, j.back):
        fabric(face, "L", "leather", 11404, 2, 0, 0, face.w, 8)
    for face in j.sides:
        fur(sub(face, 0, 7, face.w, 1), "S", 11405, 3)
    fabric(j.top, "L", "leather", 11406, 3)
    for x in range(8):
        j.top.set(x, 3, "S4")
    horn = g.piece("horn", "TORSO", (-.5, -.5, -1.5), (1, 1, 3), pivot=(-2.6, 6.8, 3.2), rotation=(0, 30, 0))
    solid(horn, "S", "smooth", 11407, 3)
    horn.front.set(0, 0, "L2")
    bell = g.piece("horn_mouth", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-3.6, 6.8, 2.2), rotation=(0, 30, 0))
    solid(bell, "S", "smooth", 11408, 3)
    bell.front.fill("K1")
