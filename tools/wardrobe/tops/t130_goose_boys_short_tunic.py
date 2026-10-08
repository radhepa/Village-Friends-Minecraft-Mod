"""Goose Boy's Short Tunic: a short hand-me-down tunic with pale side gores and elbow sleeves, a cord belt with a long goose feather tucked in it."""
from kit import body, sleeves
from kit_male import blk
from paint import k, solid

META = {
    "name": "Goose Boy's Short Tunic",
    "gender": "male",
    "description": "A short hand-me-down tunic with pale let-in side gores and elbow-length sleeves, a knotted cord belt with a long white goose feather tucked in it and a little crust bag at the hip.",
    "tags": ["casual", "simple", "relaxed"],
    "covers_waist": True,
}

TOP = 10.6


def build(g):
    b = body(g, "P", "weave", 31600)
    f = b.front
    for x, y in ((3, 0), (4, 0), (3, 1)):
        f.clear(x, y)
    f.set(4, 1, "P1"), f.set(2, 0, "P3"), f.set(5, 0, "P1")
    for face in (b.front, b.back):                                        # triangular let-in gores at the sides
        for y in range(5, 12):
            n = (y - 5) // 3 + 1
            for x in range(n):
                face.set(x, y, "S3" if x < n - 1 else "S2")
                face.set(7 - x, y, "S3" if x < n - 1 else "S2")
    b.front.set(5, 3, "S2"), b.front.set(6, 3, "S2"), b.front.set(5, 4, "S2"), b.front.set(6, 4, "S3")   # a patch
    sleeves(g, "P", "weave", 31601, rows=(0, 6))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 6, "S2")                       # bound sleeve ends
        arm.strip.hline(0, arm.strip.w - 1, 5, "P1")
    # Knotted cord belt with dangling ends.
    cord = g.piece("cord_belt", "TORSO", (-4.55, 9.6, -2.55), (9, 1, 5), inflate=.05)
    solid(cord, "S", "plain", 31602, 2, edge=False)
    for face in cord.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "S1")
    for i, x in enumerate((-.4, .5)):
        end = g.piece(f"cord_end_{i}", "TORSO", (x - .5, 10.0 - TOP, -1), (1, 3 - i, 1), pivot=(0, TOP, -2.9),
                      motion="flap_front")
        solid(end, "S", "plain", 31603 + i, 2, edge=False)
        end.strip.hline(0, end.strip.w - 1, 2 - i, "S4")
    # The goose feather tucked in at the left hip: a pale quill and a long vane slanting across the belly.
    quill = blk(g, "feather_quill", (3.0, 9.0, -2.9), (1, 2, 1), "S", 4, "plain", 31605, rotation=(0, 0, -34),
                edge=False)
    quill.front.set(0, 1, "S2")
    vane = g.piece("feather_vane", "TORSO", (-1, -6, -.5), (2, 6, 1), pivot=(3.0, 9.2, -2.95), rotation=(0, 0, -34))
    for face in vane.faces:
        face.fill("S4")
    for face in (vane.front, vane.back):
        face.vline(1 if face is vane.front else 0, 0, 5, "S2")            # the shaft down one edge
        face.set(0 if face is vane.front else 1, 0, "S3")
        face.set(0 if face is vane.front else 1, 3, "S3")                 # a split in the barbs
    tip = g.piece("feather_tip", "TORSO", (-1, -8, -.5), (1, 2, 1), pivot=(3.0, 9.2, -2.95), rotation=(0, 0, -34))
    solid(tip, "S", "plain", 31609, 4, edge=False)
    tip.front.set(0, 1, "S3")
    # A little crust bag on the right hip.
    bag = blk(g, "crust_bag", (-2.6, 8.0, -2.8), (2, 2, 1), "L", 2, "leather", 31606)
    bag.front.hline(0, 1, 0, "L3"), bag.front.set(1, 1, "L1")
    # A short hem, scalloped where it was cut down.
    for name, z, motion, face_name in (("tunic_hem_front", -2.85, "flap_front", "front"),
                                        ("tunic_hem_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 2, 1), pivot=(0, TOP, z), motion=motion)
        solid(panel, "P", "weave", 31607 + (z > 0), 2, edge=False)
        face = getattr(panel, face_name)
        for x in range(9):
            face.set(x, 1, k("P", 1) if x % 3 == 1 else k("P", 3))
        face.set(0, 0, "S3"), face.set(8, 0, "S3"), face.set(0, 1, "S2"), face.set(8, 1, "S2")
