"""Dairyman's Yoke Smock: a scrubbed pale smock with pin-tucked front, and a carved milking yoke across the shoulders with two hooped pails of milk hanging from its ends."""
from kit import body, flaps, roll, sleeves
from kit_male import blk
from paint import k, solid

META = {
    "name": "Dairyman's Yoke Smock",
    "gender": "male",
    "description": "A scrubbed pale dairy smock with a pin-tucked front and rolled sleeves, a carved milking yoke across the shoulders and two iron-hooped pails of fresh milk swinging from its ends.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 31700, base=3)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "S2"), f.set(5, 0, "S2")
    f.hline(1, 6, 3, "S2")                                                # the yoke seam
    for x in (2, 3, 4, 5):
        f.vline(x, 4, 9, "S4" if x % 2 else "S2")                         # pin tucks below it
    b.back.hline(1, 6, 3, "S2")
    for face in (b.right, b.left):
        face.vline(1, 1, 11, "S2")
    sleeves(g, "S", "weave", 31701, base=3, rows=(0, 5))
    roll(g, "S", 2.6, base=3)
    belt = g.piece("apron_string", "TORSO", (-4.55, 9.4, -2.55), (9, 1, 5), inflate=.05)
    solid(belt, "L", "plain", 31702, 2, edge=False)
    for face in flaps(g, "smock_hem", 4, "S", "weave", 31703, base=3, top=10.6):
        face.hline(0, 8, 3, "S2")
        for x in (1, 7):
            face.set(x, 1, "S4")                                          # a splash of whey
    # The yoke: a carved beam across the shoulders, hollowed for the neck, padded where it rests.
    yoke = g.piece("milk_yoke", "TORSO", (-11, 0, -1), (22, 1, 2), pivot=(0, .2, 3.1))
    solid(yoke, "L", "plain", 31704, 3, edge=False)
    for face in (yoke.front, yoke.back, yoke.top):
        face.set(0, 0, "L1"), face.set(face.w - 1, 0, "L1")
        for x in (6, 15):
            face.set(x, 0, "L4")                                          # carved grips
    yoke.top.hline(9, 12, 0, "L2"), yoke.top.hline(9, 12, 1, "L2")
    jacket = g.part("jacket")
    jacket.top.hline(0, 7, 0, "L2"), jacket.back.hline(1, 6, 0, "L2")       # the leather pad under the yoke
    # Cords and pails at each end, hanging clear of the arms.
    for i, x in enumerate((-10.2, 10.2)):
        cord = blk(g, f"pail_cord_{i}", (x, 1.2, 3.1), (1, 4, 1), "S", 2, "plain", 31706 + i, motion="sway",
                   edge=False)
        for y in range(4):
            cord.strip.hline(0, cord.strip.w - 1, y, "S3" if y % 2 else "S1")
        pail = g.piece(f"milk_pail_{i}", "TORSO", (-1.5, 4, -1.5), (3, 3, 3), pivot=(x, 1.2, 3.1), motion="sway")
        solid(pail, "L", "plain", 31708 + i, 3, edge=False)
        for face in pail.sides:
            face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 2, "M2")   # iron hoops
            face.set(1, 1, "L2")
        pail.top.fill("S4"), pail.top.set(1, 1, "S3"), pail.top.set(0, 0, "S3")       # brimming milk
        pail.bottom.fill("L1")
