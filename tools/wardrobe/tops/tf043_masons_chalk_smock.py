"""Mason's Chalk Smock: a dusty hip-length smock with a chalk-line reel and plumb bob hung from the girdle."""
from kit import body, sleeves
from kit_female import girdle, hanging, neck, over_flaps
from paint import rnd, solid

META = {
    "name": "Mason's Chalk Smock",
    "gender": "female",
    "description": "A stone-dusted hip-length smock, gathered cuffs, a chalk-line reel and a brass plumb bob on the girdle.",
    "tags": ["work", "sturdy"],
    "covers_waist": True,
}


def dust(face, seed, y0=0):
    for y in range(y0, face.h):
        for x in range(face.w):
            if rnd(x, y, seed) < .05 + y * .008:
                face.set(x, y, "S4")


def build(g):
    b = body(g, "S", "weave", 14301, base=2)
    neck(b.front, "keyhole", "S", 2)
    for face in (b.front, b.back):
        for x in range(1, 8, 2):
            face.set(x, 1, "S1")                                     # yoke gathers
        face.hline(0, 7, 2, "S3")
        dust(face, 14302 + face.x0, 4)
    sleeves(g, "S", "weave", 14303, base=2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for x in range(16):
            arm.strip.set(x, 10, "S1" if x % 2 else "S3")
        dust(arm.front, 14304, 6)
    girdle(g, "girdle", 8.0, role="L", height=1, wide=True)
    f, bk = over_flaps(g, "smock_hem", 3, "S", "weave", 14305, base=2, width=10, top=9.0)
    for face in (f, bk):
        dust(face, 14306, 0)
    reel = g.piece("chalk_reel", "TORSO", (-1, 0, -1), (2, 2, 2), pivot=(-3.0, 6.8, -3.1))
    solid(reel, "L", "smooth", 14307, 3)
    reel.front.set(0, 0, "S4"), reel.front.set(1, 1, "A2")
    hanging(g, "plumb_line", 2.8, 5, role="S", base=4, top=9.0)
    bob = g.piece("plumb_bob", "TORSO", (-.5, 5, -.4), (1, 2, 1), pivot=(2.8, 9.0, -3.25), motion="flap_front", inflate=.1)
    solid(bob, "M", "smooth", 14308, 3)
    bob.bottom.fill("M1")
