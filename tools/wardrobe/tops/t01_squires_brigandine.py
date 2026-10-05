"""Squire's Brigandine: riveted cloth armor over a quilted gambeson, layered pauldrons and tassets."""
from paint import cap, fabric, grid, k, rivets, solid, strip_fabric

META = {
    "name": "Squire's Brigandine",
    "description": "Riveted brigandine with a heraldic chevron, quilted sleeves, steel pauldrons and tassets.",
    "tags": ["armor", "martial"],
    # Armor only sits right over sturdy legwear.
    "requires": ["sturdy"],
    "covers_waist": True,
}

EMBLEM = ["abbbba",
          "bcSScb",
          "bScbSb",
          "bbccbb",
          ".abba.",
          "..aa.."]


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "S", "quilt", 3, 2)
    cap(body, "S", texture="quilt", seed=3)
    # Brigandine shell on the jacket layer: primary cloth, riveted plates.
    strip_fabric(jacket, "P", "velvet", 11, 2)
    cap(jacket, "P", seed=11)
    f, b = jacket.front, jacket.back
    for x in range(2, 6):
        f.set(x, 0, None)          # neck opening shows the gambeson
    f.set(2, 1, "P1"), f.set(5, 1, "P1"), f.hline(3, 4, 1, "P0")
    grid(f, 1, 2, EMBLEM, {"a": "A1", "b": "A2", "c": "A3", "S": "M4"})
    for y in (9, 11):
        rivets(f, y, start=0 if y == 9 else 1)
    f.hline(0, 7, 10, "P1")
    for face in (jacket.right, jacket.left):
        for y in (2, 5, 8, 11):
            rivets(face, y, start=y % 2)
    for y in (1, 4, 7, 10):
        rivets(b, y, start=(y // 3) % 2)
    b.vline(3, 0, 11, "P1"), b.vline(4, 0, 11, "P3")
    for y in range(12):
        if y % 3 == 2:
            b.hline(0, 7, y, "P1")
    jacket.top.hline(0, 7, 3, "M3")

    for side in ("right", "left"):
        arm, sleeve = g.part(f"{side}_arm"), g.part(f"{side}_sleeve")
        strip_fabric(arm, "S", "quilt", 21, 2)
        cap(arm, "S", texture="quilt", seed=21)
        # Leather vambraces laced over the quilted cuffs; hands stay bare.
        strip_fabric(sleeve, "L", "leather", 23, 2, 6, 9)
        for face in sleeve.sides:
            face.hline(0, face.w - 1, 6, "L3")
            face.hline(0, face.w - 1, 9, "L1")
        outer = sleeve.right if side == "right" else sleeve.left
        outer.set(1, 7, "M3"), outer.set(2, 7, "M3"), outer.set(1, 8, "M1"), outer.set(2, 8, "M1")
        for y in (7, 8):
            sleeve.front.set(1 + (y % 2), y, "L0")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S3")
        arm.strip.hline(0, arm.strip.w - 1, 11, None)
        arm.bottom.fill(None)

        # Two overlapping steel lames per shoulder, tilted down the outside of the arm.
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        sign = -1 if side == "right" else 1
        cx = -1.0 if side == "right" else 1.0
        upper = g.piece(f"{side}_pauldron", bone, (-3.5, -1.2, -3.0), (7, 2, 6),
                        pivot=(cx, -2.0, 0), rotation=(0, 0, 14 * sign))
        solid(upper, "M", "smooth", 31, 2)
        cap(upper, "M", top_delta=2, bottom_delta=-1)
        for face in upper.sides:
            face.hline(0, face.w - 1, 1, "A2")
            rivets(face, 0, start=1, step=3, base=4)
        lower = g.piece(f"{side}_pauldron_lame", bone, (-3.2 + .7 * sign, .4, -2.8), (6, 2, 6),
                        pivot=(cx, -2.0, 0), rotation=(0, 0, 22 * sign))
        solid(lower, "M", "smooth", 32, 2)
        cap(lower, "M", top_delta=1, bottom_delta=-2)
        for face in lower.sides:
            face.hline(0, face.w - 1, 1, "M1")
            rivets(face, 0, start=0, step=3, base=4)

    # Padded standing collar under the jaw.
    collar = g.piece("gorget", "TORSO", (-4.5, -1.0, -2.6), (9, 2, 5), inflate=.05)
    solid(collar, "S", "quilt", 41, 2)
    for face in collar.sides:
        face.hline(0, face.w - 1, 0, "S3")
        face.hline(0, face.w - 1, 1, "S1")
    collar.front.set(4, 1, "M3")
    # Sword belt riding on the hips.
    belt = g.piece("belt", "TORSO", (-4.6, 10.0, -2.6), (9, 2, 5), inflate=.06)
    solid(belt, "L", "leather", 42, 2)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    grid(belt.front, 3, 0, ["MMM", "MLM"], {"M": "M3", "L": "L0"})
    belt.left.set(2, 1, "M2")
    # Riveted tassets hanging from the belt, riding on the stride.
    for name, z, motion, depth_face in (("tasset_front", -2.85, "flap_front", "front"), ("tasset_back", 1.85, "flap_back", "back")):
        tasset = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 4, 1), pivot=(0, 11.6, z), motion=motion)
        solid(tasset, "P", "velvet", 43 if motion == "flap_front" else 44, 2)
        face = getattr(tasset, depth_face)
        face.vline(4, 0, 3, "P1")
        rivets(face, 1, start=1, step=2)
        face.hline(0, 8, 3, "L1")
        face.hline(0, 8, 0, "P3")
