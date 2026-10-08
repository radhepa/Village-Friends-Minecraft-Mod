"""Gleaner's Gathered-Apron Top: a plain kirtle whose linen apron is caught up by its corners into a bulging
lap-bag at the hip, heavy with gleaned ears of wheat."""
from kit import body, sleeves
from kit_female import OVER_FRONT, girdle, neck, over_panel
from kit_f01 import bundle
from paint import fabric, k, solid

META = {
    "name": "Gleaner's Gathered-Apron Top",
    "gender": "female",
    "description": "A plain kirtle with turned cuffs and a linen apron gathered up by its corners into a bulging bag of gleaned wheat ears at the hip.",
    "tags": ["work", "simple", "apron"],
    "covers_waist": True,
}

HINGE = (0, 9.0, OVER_FRONT)


def build(g):
    b = body(g, "P", "weave", 51080)
    neck(b.front, "round", "P", 2, edge="P3")
    b.front.vline(3, 1, 4, "P1")                                       # a short slit at the throat
    b.front.set(4, 2, "M3")
    for face in (b.front, b.back):
        face.vline(1, 6, 11, "P1"), face.vline(6, 6, 11, "P1")
    sleeves(g, "P", "weave", 51081, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 8, "P3"), arm.strip.hline(0, 15, 9, "P1")    # turned-back cuffs
        arm.strip.hline(0, 15, 10, "S3"), arm.strip.hline(0, 15, 11, "S2")
    # The apron band and the apron itself, its lower corners drawn up and tucked into the band.
    girdle(g, "apron_band", 8.0, role="S", base=3, height=1, buckle=None, texture="weave", wide=True)
    apron = over_panel(g, "apron", 5, "S", "weave", 51082, base=3, width=9, top=9.0)
    for x in range(0, 9, 2):
        apron.vline(x, 1, 4, "S2")                                     # pulled into gathers toward the bag
    apron.hline(0, 8, 4, "S1")
    j = g.part("jacket")
    fabric(j.front, "S", "weave", 51083, 3, 0, 8, 8, 4)
    for x in range(0, 8, 2):
        j.front.set(x, 9, "S2")
    # The lap-bag: the gathered apron bulging at her left hip, wheat ears spilling from its mouth.
    bag = g.piece("apron_bag", "TORSO", (-.6, 1.4, -2.0), (4, 4, 2), pivot=HINGE, motion="flap_front", inflate=.1)
    solid(bag, "S", "weave", 51084, 3)
    for face in bag.sides:
        for x in range(face.w):
            if x % 2:
                face.vline(x, 1, face.h - 2, "S2")
        face.hline(0, face.w - 1, 0, "S4")
    bag.top.fill("M2")
    knot = g.piece("apron_knot", "TORSO", (-1.9, .6, -1.5), (2, 2, 1), pivot=HINGE, motion="flap_front", inflate=.08)
    solid(knot, "S", "weave", 51085, 2, edge=False)
    knot.front.set(0, 0, "S4"), knot.front.set(1, 1, "S1")
    for i, (x, y, z) in enumerate(((-.2, -2.0, -1.5), (1.0, -3.0, -1.0), (2.2, -2.4, -1.7), (3.0, -1.4, -1.2))):
        ear = bundle(g, f"wheat_ear_{i}", "TORSO", HINGE, (1, 5, 1), role="M", base=2, seed=51086 + i,
                     head_rows=3, head=("M3", "M4"), motion="flap_front", origin=(x - .5, y, z - .5))
        for f in ear.sides:
            f.set(0, 3, "M1"), f.set(0, 4, "M1")                     # the bare stalk below the head
    for face in (bag.front,):
        face.set(1, 1, k("M", 3)), face.set(3, 2, k("M", 2))          # a few loose grains caught in the cloth
