"""Arcanist Longcoat: velvet longcoat with a shoulder mantle, bell cuffs, sash and knee-length skirts."""
from paint import cap, fabric, grid, k, solid, strip_fabric

META = {
    "name": "Arcanist Longcoat",
    "gender": "male",
    "description": "Clasped velvet longcoat, trimmed shoulder mantle, bell cuffs, sash and split skirts.",
    "tags": ["robe", "scholarly"],
    "covers_waist": True,
}


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "S", "weave", 81, 3)
    cap(body, "S", seed=81, base=3)
    strip_fabric(jacket, "P", "velvet", 82, 2)
    cap(jacket, "P", texture="velvet", seed=82)
    f, b = jacket.front, jacket.back
    # V opening over the tunic, edged in accent.
    for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2), (4, 3)]:
        f.clear(x, y)
    for x, y in [(1, 0), (2, 1), (2, 2), (3, 3)]:
        f.set(x, y, "A2")
    for x, y in [(6, 0), (5, 1), (5, 2), (5, 3)]:
        f.set(x, y, "A1")
    # Closure seam and paired clasps.
    f.vline(4, 4, 11, "P1")
    f.vline(3, 4, 11, "P3")
    for y in (4, 6):
        f.set(3, y, "M3"), f.set(4, y, "M2")
    # Sash.
    for face in jacket.sides:
        face.hline(0, face.w - 1, 8, "A3")
        face.hline(0, face.w - 1, 9, "A2")
        face.hline(0, face.w - 1, 10, "A1")
    b.vline(3, 0, 7, "P1"), b.vline(3, 11, 11, "P1")
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "P1")

    for side in ("right", "left"):
        arm, sleeve = g.part(f"{side}_arm"), g.part(f"{side}_sleeve")
        strip_fabric(arm, "P", "velvet", 83, 2, 0, 9)
        fabric(arm.top, "P", "velvet", 83, 3)
        strip_fabric(sleeve, "P", "velvet", 84, 2, 2, 6)
        for face in sleeve.sides:
            face.hline(0, face.w - 1, 6, "P1")
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        cuff = g.piece(f"{side}_bell_cuff", bone, (ox - .6, 5.6, -2.6), (5, 3, 5), inflate=.1)
        solid(cuff, "P", "velvet", 85, 2)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 2, "A2")
        cuff.bottom.fill("P0")

    # Shoulder mantle with a trimmed hem and a clasp at the throat.
    mantle = g.piece("mantle", "TORSO", (-8.5, -.5, -2.7), (17, 3, 5), inflate=.05)
    solid(mantle, "S", "weave", 86, 2)
    fabric(mantle.top, "S", "weave", 86, 3)
    for face in mantle.sides:
        face.hline(0, face.w - 1, 2, "A2")
    for x in range(0, 17, 4):
        mantle.front.set(x, 1, "S1"), mantle.back.set(x, 1, "S1")
    grid(mantle.front, 7, 0, ["aMa", ".M."], {"M": "M3", "a": "M1"})
    drape = g.piece("mantle_back", "TORSO", (-4.5, 2.5, 2.3), (9, 4, 1))
    solid(drape, "S", "weave", 87, 2)
    drape.back.hline(0, 8, 3, "A2")
    drape.back.vline(4, 0, 2, "S1")

    # Knee-length skirts: front and back follow the stride, side panels hang still.
    for name, z, motion, face_name in (("skirt_front", -2.9, "flap_front", "front"), ("skirt_back", 1.9, "flap_back", "back")):
        skirt = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 7, 1), pivot=(0, 11.4, z), motion=motion)
        solid(skirt, "P", "velvet", 88 if motion == "flap_front" else 89, 2)
        face = getattr(skirt, face_name)
        face.hline(0, 8, 6, "A2")
        face.hline(0, 8, 0, "P3")
        if face_name == "front":
            face.vline(4, 1, 6, "P0")
            face.vline(3, 1, 5, "P3")
        else:
            face.vline(4, 3, 6, "P0")
    for name, x in (("skirt_right", -5.0), ("skirt_left", 4.0)):
        panel = g.piece(name, "TORSO", (0, 0, -2), (1, 6, 4), pivot=(x, 11.4, 0))
        solid(panel, "P", "velvet", 90, 2)
        for face in panel.sides:
            face.hline(0, face.w - 1, 5, "A2")
