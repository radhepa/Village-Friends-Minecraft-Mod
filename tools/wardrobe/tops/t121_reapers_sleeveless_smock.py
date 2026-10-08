"""Reaper's Sleeveless Smock: a sleeveless harvest smock gathered at the yoke, a plaited straw girdle and a sickle hooked over it."""
from kit import body, flaps, neckline
from kit_m01 import gathers, twisted_box
from kit_male import blk
from paint import k

META = {
    "name": "Reaper's Sleeveless Smock",
    "gender": "male",
    "description": "A sleeveless harvest smock gathered under a stitched yoke, bare sunburnt arms with leather wristlets, a plaited straw girdle and a sickle hooked over it.",
    "tags": ["work", "casual", "relaxed"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 31001)
    neckline(b.front, "keyhole", "P")
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        gathers(face, "P", 2, range(0, 3), face.x0)                       # gathered yoke
        face.hline(0, 7, 3, "A2")                                         # stitched yoke seam
        for x in range(0, 8, 2):
            face.set(x, 3, "A3")
    for x in (3, 4):
        jacket.front.clear(x, 0), jacket.front.clear(x, 1)
    jacket.front.set(3, 2, "P1"), jacket.front.set(4, 2, "P1")
    for face in (jacket.right, jacket.left):
        gathers(face, "P", 2, range(0, 3), face.x0)
        face.hline(0, 3, 3, "A2")
    for face in (b.front, b.back):
        for x in (1, 6):
            face.vline(x, 5, 11, "P1")                                    # folds under the yoke
    for face in (b.right, b.left):                                        # bound armholes
        face.vline(0 if face is b.right else 3, 0, 3, "A1")
    b.top.vline(0, 0, 3, "A2"), b.top.vline(7, 0, 3, "A2")
    # Bare arms, only a leather wristlet on each.
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 8, "L3")
        arm.strip.hline(0, arm.strip.w - 1, 9, "L1")
        (arm.right if side == "right" else arm.left).set(1, 8, "M3")
    # Plaited straw girdle with a knot.
    girdle = g.piece("straw_girdle", "TORSO", (-4.6, 9.5, -2.6), (9, 1, 5), inflate=.06)
    twisted_box(girdle, "S", 3)
    knot = blk(g, "girdle_knot", (1.6, 9.7, -2.85), (1, 1, 1), "S", 4, "plain", 31002, edge=False)
    knot.front.set(0, 0, "S2")
    for i, (x, rz) in enumerate(((1.3, 8), (2.0, -10))):
        end = g.piece(f"girdle_end_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 10.4, -2.9),
                      rotation=(0, 0, rz), motion="sway")
        twisted_box(end, "S", 3, ox=i)
        end.strip.hline(0, end.strip.w - 1, 2, "S4")                      # frayed straw ends
    # The sickle: hooked over the girdle, wooden grip hanging at the right hip.
    grip = g.piece("sickle_grip", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-2.7, 10.5, -3.45), motion="flap_front")
    for face in grip.faces:
        face.fill("L3")
    for face in grip.sides:
        face.set(0, 1, "L2"), face.set(face.w - 1, 2, "L1")
    grip.bottom.fill("L1")
    ferrule = blk(g, "sickle_ferrule", (-2.7, 9.7, -3.45), (1, 1, 1), "M", 1, "smooth", 31003, edge=False)
    ferrule.front.fill("M2")
    for i, (x, y, size, rz) in enumerate(((-2.4, 8.2, (1, 2, 1), -14), (-1.4, 7.2, (2, 1, 1), 12),
                                          (-.1, 7.6, (1, 2, 1), -30), (.5, 9.0, (1, 1, 1), -45))):
        seg = blk(g, f"sickle_blade_{i}", (x, y, -3.25), size, "M", 3, "smooth", 31004 + i, rotation=(0, 0, rz),
                  edge=False)
        seg.front.fill("M3")
        seg.front.set(0, 0, "M4")
        seg.bottom.fill("M1")
    for face in flaps(g, "smock_hem", 5, "P", "weave", 31008, top=10.6, slit=True):
        face.hline(0, 8, 3, k("A", 2))
        for x in range(0, 9, 3):
            face.set(x, 3, "A3")
        face.hline(0, 8, 4, "P1")
