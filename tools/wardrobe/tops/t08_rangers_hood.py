"""Ranger's Hood: laced tunic, cowl with the hood down, bracers, belt, quiver and a dagged hem."""
from paint import cap, fabric, grid, k, line, solid, strip_fabric

META = {
    "name": "Ranger's Hood",
    "description": "Laced woodland tunic, cowl and lowered hood, leather bracers, belt and a fletched quiver.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "P", "twill", 161, 2)
    cap(body, "P", texture="twill", seed=161)
    f = body.front
    for x, y in [(3, 0), (4, 0), (3, 1), (4, 1), (4, 2)]:
        f.clear(x, y)
    for y in (1, 2, 3):
        f.set(3 if y % 2 else 4, y + 1, "L3")
    f.vline(4, 3, 4, "P1")
    # Quiver strap across the chest on the jacket layer.
    jf, jb = jacket.front, jacket.back
    line(jf, 6, 0, 1, 10, "L2")
    line(jf, 7, 0, 2, 10, "L1")
    jf.set(4, 5, "M3")
    line(jb, 1, 0, 6, 10, "L2")
    line(jb, 0, 0, 5, 10, "L1")
    jacket.top.vline(6, 0, 3, "L2")
    for face in body.sides:
        face.hline(0, face.w - 1, 11, "P1")

    for side in ("right", "left"):
        arm, sleeve = g.part(f"{side}_arm"), g.part(f"{side}_sleeve")
        strip_fabric(arm, "P", "twill", 162, 2, 0, 10)
        fabric(arm.top, "P", "twill", 162, 3)
        arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
        # Laced bracers.
        strip_fabric(sleeve, "L", "leather", 163, 2, 6, 9)
        for face in sleeve.sides:
            face.hline(0, face.w - 1, 6, "L3")
            face.hline(0, face.w - 1, 9, "L1")
        sleeve.front.set(1, 7, "S3"), sleeve.front.set(2, 8, "S3"), sleeve.front.set(2, 7, "S2"), sleeve.front.set(1, 8, "S2")

    # Cowl and the lowered hood resting on the upper back.
    cowl = g.piece("cowl", "TORSO", (-4.6, -1.0, -2.7), (9, 2, 5), inflate=.06)
    solid(cowl, "S", "weave", 164, 2)
    fabric(cowl.top, "S", "weave", 164, 3)
    for face in cowl.sides:
        face.hline(0, face.w - 1, 1, "S1")
    cowl.front.set(4, 1, "S3")
    hood = g.piece("hood_back", "TORSO", (-3.5, 0, 0), (7, 3, 2), pivot=(0, -.4, 2.1), rotation=(12, 0, 0))
    solid(hood, "S", "weave", 165, 2)
    fabric(hood.top, "S", "weave", 165, 3)
    hood.back.vline(3, 0, 2, "S1"), hood.back.vline(4, 1, 2, "S3")
    hood.back.hline(0, 6, 0, "S3")
    tip = g.piece("hood_tip", "TORSO", (-2, 0, 0), (4, 2, 1), pivot=(0, 2.4, 2.5), rotation=(8, 0, 0))
    solid(tip, "S", "weave", 166, 2)
    tip.back.set(0, 1, "S1"), tip.back.set(3, 1, "S1")

    # Quiver slung diagonally, arrow fletchings out of the top.
    quiver = g.piece("quiver", "TORSO", (-1.5, 0, -1.5), (3, 8, 3), pivot=(1.6, 4.6, 5.0), rotation=(0, 0, -30))
    solid(quiver, "L", "leather", 167, 2)
    for face in quiver.sides:
        face.hline(0, face.w - 1, 0, "L3")
        face.hline(0, face.w - 1, 6, "L1")
    quiver.back.set(1, 3, "M3")
    for i, (dx, key) in enumerate(((-1.0, "A"), (0, "S"), (.9, "A"))):
        arrow = g.piece(f"arrow_{i}", "TORSO", (dx - .5, -3.2 + abs(dx) * .4, -.5), (1, 4, 1), pivot=(1.6, 4.6, 5.0), rotation=(0, 0, -30))
        solid(arrow, key, "plain", 168 + i, 3, edge=False)
        arrow.strip.hline(0, arrow.strip.w - 1, 0, k(key, 4))
        arrow.strip.hline(0, arrow.strip.w - 1, 3, "L2")

    belt = g.piece("belt", "TORSO", (-4.6, 9.6, -2.6), (9, 2, 5), inflate=.05)
    solid(belt, "L", "leather", 171, 2)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    grid(belt.front, 3, 0, ["MMM", "M.M"], {"M": "M3"})
    belt.front.set(4, 1, "L0")
    # Short dagged tunic skirts.
    for name, z, motion, face_name in (("skirt_front", -2.8, "flap_front", "front"), ("skirt_back", 1.8, "flap_back", "back")):
        skirt = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 4, 1), pivot=(0, 11.5, z), motion=motion)
        solid(skirt, "P", "twill", 172, 2)
        face = getattr(skirt, face_name)
        for x in range(9):
            face.set(x, 3, "P1" if x % 2 else "P2")
        face.hline(0, 8, 0, "P1")
        face.vline(4, 1, 3, "P1")
