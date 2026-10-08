"""Herbalist Monk's Garden Habit: a monk's habit with sleeves bunched up, a canvas garden apron whose pocket bristles with cut herbs, sprigs stuck in his cord and a trowel at his hip."""
from kit import body, sleeves
from kit_male import blk, hood_down, sleeve_shapes
from kit_m05 import cord_end
from paint import fabric, solid

META = {
    "name": "Herbalist Monk's Garden Habit",
    "gender": "male",
    "description": "The infirmarian's garden habit: hood back, wide sleeves bunched above the elbow, a canvas apron whose pocket bristles with fresh-cut herbs, more sprigs stuck in his knotted cord and a trowel hanging at his hip.",
    "tags": ["holy", "work", "robe"],
    "locked_to": "b235_herbalist_monks_knee_tied_habit",
    "covers_waist": True,
}


def sprig(g, pid, pivot, length, rz, seed, bone="TORSO", motion="none"):
    stem = g.piece(pid, bone, (-.5, -length, -.5), (1, length, 1), pivot=pivot, rotation=(0, 0, rz), motion=motion)
    solid(stem, "S", "plain", seed, 1, edge=False)
    stem.strip.hline(0, stem.strip.w - 1, 0, "A3")                      # the flowering tip
    stem.top.fill("A4")
    if length > 2:
        stem.strip.hline(0, stem.strip.w - 1, 1, "S2")
    return stem


def build(g):
    b = body(g, "P", "weave", 35560, base=1)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.set(2, 0, "P0"), b.front.set(5, 0, "P0"), b.front.vline(3, 1, 2, "P0")
    for face in (b.front, b.back):
        face.vline(1, 2, 11, "P0"), face.vline(6, 2, 11, "P2")
    sleeves(g, "P", "weave", 35561, base=1, rows=(0, 3))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        fabric(arm.strip, "S", "weave", 35562, 2, 0, 4, arm.strip.w, 7)   # undertunic forearms
        arm.strip.hline(0, arm.strip.w - 1, 10, "S1")
    for s in sleeve_shapes(g, "bunched_sleeve", "P", 1.2, (5, 3, 5), "weave", 35563, base=1, inflate=.2):
        for face in s.sides:
            face.hline(0, face.w - 1, 0, "P2"), face.hline(0, face.w - 1, 2, "P0")
            for x in range(0, face.w, 2):
                face.set(x, 1, "P0")                                       # the bunched folds
    hood_down(g, "P", "weave", 35564, base=1, y=-1.1, z=3.1, tilt=12, lining="P0")
    # The knotted cord, herbs stuck through it.
    cord = g.piece("garden_cord", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.05)
    for face in cord.sides:
        for x in range(face.w):
            face.set(x, 0, "S3" if (x + face.x0) % 2 else "S1")
    cord.top.fill("S2"), cord.bottom.fill("S1")
    cord_end(g, "cord_tail", (-3.7, 10.4, -2.95), 5, "S", 2, 35565, knots=(1, 3))
    for i, (x, rz) in enumerate(((2.6, -16), (3.3, 6), (1.9, -30))):
        sprig(g, f"cord_sprig_{i}", (x, 10.1, -2.8), 3 - (i == 2), rz, 35566 + i)
    # Canvas garden apron with a deep pocket of cut herbs.
    apron = g.piece("garden_apron", "TORSO", (-3, 0, 0), (6, 7, 1), pivot=(0, 10.4, -3.15), motion="flap_front")
    solid(apron, "S", "weave", 35570, 2)
    af = apron.front
    af.hline(0, 5, 0, "S3"), af.hline(0, 5, 6, "S1")
    af.vline(0, 1, 6, "S1"), af.vline(5, 1, 6, "S3")
    af.rect(1, 3, 4, 3, "S1"), af.hline(1, 4, 3, "S3")                  # the deep pocket, lit at its hem
    af.rect(2, 4, 2, 2, "S2")
    for x in (0, 2, 4):
        af.set(x, 6, "L2")                                                 # earth wiped on the hem
    for i, (x, rz) in enumerate(((-1.2, -12), (-.3, 4), (.7, 18))):
        sprig(g, f"pocket_sprig_{i}", (x, 12.6, -3.35), 2 + (i == 1), rz, 35571 + i, motion="flap_front")
    # A garden trowel hung from the cord at the left hip.
    handle = blk(g, "trowel_handle", (3.4, 9.8, -3.3), (1, 2, 1), "L", 3, "plain", 35575, motion="flap_front")
    handle.top.fill("L4")
    blade = g.piece("trowel_blade", "TORSO", (-1, 2, -.5), (2, 3, 1), pivot=(3.4, 9.8, -3.3), motion="flap_front")
    solid(blade, "M", "smooth", 35576, 3, edge=False)
    blade.front.set(0, 2, "M1"), blade.front.set(1, 2, "M2"), blade.front.vline(1, 0, 1, "M4")
    blade.front.set(0, 2, "L1")                                            # earth on the tip
