"""Charcoal Burner's Sooty Bodice: a laced bodice and shirt blackened with soot toward the hands and hem,
a knotted neckerchief, leather cuffs and a wooden charcoal shovel slung on her back."""
from kit_f07 import prop
from kit_female import arm_rings, bodice, chemise, lacing
from paint import fabric, solid
from wardrobe import shade


def soot(face, y0, y1, step=2):
    """Soot settling toward an edge: bands of rows from y0, each band a shade darker than the last."""
    for y in range(y0, y1 + 1):
        depth = min(2, 1 + (y - y0) // step)
        for x in range(face.w):
            cur = face.get(x, y)
            if cur:
                face.set(x, y, shade(cur, -depth))


META = {
    "name": "Charcoal Burner's Sooty Bodice",
    "gender": "female",
    "description": "A laced bodice and shirt blackened with soot toward the hands and hem, a knotted neckerchief, "
                   "leather cuffs and a wooden charcoal shovel slung on her back.",
    "tags": ["work", "rugged"],
}


def build(g):
    body, arms = chemise(g, "S", 2, "weave", 57701, neckline="round", sleeve_rows=(0, 11))
    for arm in arms:
        soot(arm.strip, 6, 9)
    b = bodice(g, "P", "plain", 57702, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "ladder", lace="L3", under="P1", eyelet="M2")
    for face in b.sides:
        soot(face, 7, 9, step=1)
    for box in arm_rings(g, "cuff", 6.0, 3, 5, inflate=.06):
        solid(box, "L", "leather", 57703, 1)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 2, "K1")
    # The neckerchief: a band round the neck, knotted at the front with a point down the back.
    band = prop(g, "neckerchief", "TORSO", (-4.5, 0, -2.5), (9, 1, 5), pivot=(0, -.4, 0), role="A", texture="plain",
                seed=57704, base=2, inflate=.1, edge=False)
    for face in band.sides:
        for x in range(face.w):
            face.set(x, 0, "A2" if x % 3 else "A1")
    knot = prop(g, "neckerchief_knot", "TORSO", (-1, 0, -1), (2, 2, 1), pivot=(.6, .2, -2.45), role="A", base=2,
                seed=57705, edge=False)
    knot.front.set(0, 0, "A3"), knot.front.set(1, 1, "A1")
    for i, w in enumerate((5, 3, 1)):
        point = prop(g, f"neckerchief_point_{i}", "TORSO", (-w / 2, 0, 0), (w, 1, 1), pivot=(0, .6 + i, 2.3),
                     role="A", base=2, seed=57706 + i, edge=False)
        point.back.set(0, 0, "A1")
    # A wooden charcoal shovel, its blade standing up behind her shoulder and its shaft down to her hip.
    pv = (-1.6, 9.2, 2.4)
    shaft = prop(g, "shovel_shaft", "TORSO", (-.5, -9, 0), (1, 9, 1), pivot=pv, rotation=(-14, 0, 12), role="L",
                 texture="smooth", seed=57709, base=3)
    shaft.back.vline(0, 0, 8, "L2")
    blade = prop(g, "shovel_blade", "TORSO", (-1.5, -13, -.2), (3, 4, 1), pivot=pv, rotation=(-14, 0, 12), role="L",
                 texture="smooth", seed=57710, base=2)
    blade.back.hline(0, 2, 0, "K1"), blade.back.hline(0, 2, 1, "L1")      # the sooty scoop edge
    blade.back.set(1, 3, "L3")
    grip = prop(g, "shovel_grip", "TORSO", (-1, 0, -.5), (2, 1, 1), pivot=pv, rotation=(-14, 0, 12), role="L",
                texture="smooth", seed=57711, base=1, edge=False)
    grip.back.set(0, 0, "L2")
    strap = prop(g, "shovel_strap", "TORSO", (-3, 0, 0), (6, 1, 1), pivot=(0, 4.0, 2.25), role="L",
                 texture="leather", seed=57712, base=1, edge=False)
    strap.back.set(2, 0, "M3")
    fabric(g.part("jacket").back, "L", "leather", 57713, 1, 0, 4, 8, 1)
