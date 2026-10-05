"""Pilgrim's Tabard: an embroidered tabard over a long undertunic, a stole and a tasseled cord."""
from paint import cap, fabric, grid, k, solid, strip_fabric

META = {
    "name": "Pilgrim's Tabard",
    "description": "Sun-embroidered tabard with knee-length panels over a long undertunic, a stole and a tasseled cord.",
    "tags": ["robe", "holy"],
    "covers_waist": True,
}

SUN = [".a.a.",
       "abMba",
       ".MmM.",
       "abMba",
       ".a.a."]


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "S", "weave", 211, 3)
    cap(body, "S", texture="weave", seed=211, base=3)
    # Tabard: front and back panels on the jacket layer; the sides stay open.
    for face in (jacket.front, jacket.back):
        fabric(face, "P", "velvet", 212, 2, 1, 0, 6, 12)
        face.vline(1, 0, 11, "A2"), face.vline(6, 0, 11, "A2")
    jacket.front.hline(2, 5, 0, None)
    jacket.front.set(2, 1, "A1"), jacket.front.set(5, 1, "A1"), jacket.front.hline(3, 4, 1, "A1")
    grid(jacket.front, 2, 4, SUN, {"a": "A2", "b": "A3", "M": "M3", "m": "M4"})
    grid(jacket.back, 2, 3, SUN, {"a": "A2", "b": "A3", "M": "M3", "m": "M4"})
    fabric(jacket.top, "P", "velvet", 213, 3, 1, 0, 6, 4)
    for x in range(2, 6):
        jacket.top.set(x, 3, None)
    # Cord belt.
    for face in jacket.sides:
        face.hline(0, face.w - 1, 10, "A3")
    for face in (jacket.right, jacket.left):
        face.set(1, 10, "A1"), face.set(2, 10, "A3")

    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "weave", 214, 3, 0, 10)
        fabric(arm.top, "S", "weave", 214, 4)
        arm.strip.hline(0, arm.strip.w - 1, 9, "A2")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")

    # Stole: two accent bands falling from the shoulders.
    for name, x in (("stole_right", -3.6), ("stole_left", 1.6)):
        stole = g.piece(name, "TORSO", (0, 0, 0), (2, 9, 1), pivot=(x, -.3, -2.75))
        solid(stole, "A", "plain", 215, 2)
        stole.front.vline(0, 0, 8, "A3")
        stole.front.hline(0, 1, 8, "M3")
        stole.front.set(0, 7, "A1"), stole.front.set(1, 7, "A1")
    yoke = g.piece("stole_yoke", "TORSO", (-4.5, -.6, -2.7), (9, 1, 5))
    solid(yoke, "A", "plain", 216, 2, edge=False)
    # Tasseled cord end on the hip; it swings as the wearer walks.
    tassel = g.piece("cord_tassel", "TORSO", (-.5, 0, -.5), (1, 4, 1), pivot=(3.0, 10.6, -2.6), motion="sway")
    solid(tassel, "A", "plain", 217, 3)
    tassel.strip.hline(0, tassel.strip.w - 1, 3, "M3")
    # Knee-length tabard panels.
    for name, z, motion, face_name in (("panel_front", -2.85, "flap_front", "front"), ("panel_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-3, 0, 0), (6, 7, 1), pivot=(0, 11.4, z), motion=motion)
        solid(panel, "P", "velvet", 218, 2)
        face = getattr(panel, face_name)
        face.vline(0, 0, 6, "A2"), face.vline(5, 0, 6, "A2"), face.hline(0, 5, 6, "A2")
        face.hline(0, 5, 0, "P3")
        grid(face, 2, 2, ["MM", "MM"], {"M": "M2"})
        face.set(2, 2, "M4")
