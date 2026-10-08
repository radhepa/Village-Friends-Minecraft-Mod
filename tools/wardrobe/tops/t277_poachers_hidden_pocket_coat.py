"""Poacher's Hidden-Pocket Coat: a long shabby coat hanging open, a rabbit peeking out of the deep inside pocket."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_male import blk
from paint import fabric, k, strip_fabric

META = {
    "name": "Poacher's Hidden-Pocket Coat",
    "gender": "male",
    "description": "A long shabby night coat hanging open over a drab waistcoat, its collar rolled against the night damp, the poached rabbit's ears and nose peeking out of the deep inside pocket.",
    "tags": ["rugged", "whimsical", "relaxed"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 37240, base=1)                             # the drab waistcoat
    for y in range(1, 11, 3):
        b.front.set(4, y, "L2")
    jacket = g.part("jacket")                                            # the coat, hanging open
    strip_fabric(jacket, "P", "weave", 37241, 1, 0, 11)
    fabric(jacket.top, "P", "weave", 37241, 2)
    fabric(jacket.bottom, "P", "weave", 37242, 0)
    jf = jacket.front
    for y in range(12):
        for x in (3, 4):
            jf.clear(x, y)
        jf.set(2, y, "P2"), jf.set(5, y, "P0")                          # the open front edges
    jf.clear(2, 0), jf.clear(5, 0)
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "P0")
    jacket.back.vline(4, 6, 11, "P0")                                    # the back vent
    jf.hline(0, 1, 8, "P0")                                              # a slant pocket at the right hip
    sleeves(g, "P", "weave", 37243, base=1, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P2"), arm.strip.hline(0, arm.strip.w - 1, 10, "P0")
        (arm.right if side == "right" else arm.left).set(2, 6, "S1")       # a worn-through elbow
    rolled = collar(g, "rolled_collar", "P", "weave", base=2, height=1, y=-.5)
    rolled.front.hline(3, 5, 0, "P0")

    # The deep inside pocket at the left breast, and the rabbit looking out of it.
    lip = blk(g, "inside_pocket", (1.6, 6.0, -3.0), (4, 2, 1), "P", 1, "weave", 37244, edge=False)
    lip.front.hline(0, 3, 0, "P2")
    head = blk(g, "rabbit_head", (1.7, 3.6, -2.6), (3, 3, 2), "L", 3, "plain", 37245, edge=False)
    hf = head.front
    hf.set(0, 1, "K0"), hf.set(2, 1, "K0")                               # eyes
    hf.set(1, 2, "A3"), hf.set(1, 1, "L4")                               # pink nose, pale muzzle
    hf.set(0, 2, "L4"), hf.set(2, 2, "L4")
    head.top.fill("L3")
    for i, (x, rz) in enumerate(((1.0, -12), (2.4, 10))):
        ear = blk(g, f"rabbit_ear_{i}", (x, 3.8, -2.45), (1, 3, 1), "L", 3, "plain", 37246 + i, edge=False,
                  origin=(-.5, -3, -.5), rotation=(-14, 0, rz))
        ear.front.vline(0, 0, 1, "A2")                                    # the pink inside of the ear
        ear.front.set(0, 0, "L2")
    # Long open coat skirts, front panels split at the middle.
    for face in flaps(g, "coat_skirt", 8, "P", "weave", 37248, base=1, top=10.6, slit=True):
        face.hline(0, 8, 7, k("P", 0))
        face.vline(4, 0, 7, "P0")
