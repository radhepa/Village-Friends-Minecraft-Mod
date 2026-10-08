"""Gate Warden's Key-Hung Brigandine: a cloth-covered brigandine studded in staggered rows and closed across the
chest with three buckled straps, mail half sleeves, and the gate keys on a great iron ring at her hip."""
from kit import sleeves
from kit_female import girdle, mail, over_flaps
from kit_f04 import front_prop
from paint import fabric, solid, strip_fabric

META = {
    "name": "Gate Warden's Key-Hung Brigandine",
    "gender": "female",
    "description": "A studded brigandine closed across the chest with three buckled straps, mail half sleeves, and "
                   "the gate keys hung on a great iron ring at her hip.",
    "tags": ["armor", "martial"],
    "requires": ["sturdy"],
    "covers_waist": True,
}


def studs(face, y0=0, y1=None):
    """Staggered rivet heads, the way the plates beneath a brigandine overlap."""
    y1 = face.h - 1 if y1 is None else y1
    for y in range(y0, y1 + 1, 2):
        for x in range(((y - y0) // 2) % 2, face.w, 2):
            face.set(x, y, "M3")


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "velvet", 54321, 2)
    fabric(b.top, "P", "velvet", 54321, 3), fabric(b.bottom, "P", "velvet", 54321, 1)
    for face in b.sides:
        studs(face, 1, 10)
        face.hline(0, face.w - 1, 11, "P1")
    b.front.vline(3, 1, 11, "P0"), b.front.vline(4, 1, 11, "P1")      # the front opening
    for y in (2, 5, 8):                                                # three straps across it
        b.front.hline(1, 6, y, "L2")
        b.front.set(4, y, "M4"), b.front.set(5, y, "L3")
    b.front.hline(2, 5, 0, "S3")                                       # arming coat at the neck
    sleeves(g, "S", "weave", 54322, base=2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        mail(arm.strip, "M", 2, 0, 5)
        arm.strip.hline(0, 15, 6, "M1")
        arm.strip.hline(0, 15, 11, "S1")
        fabric(arm.top, "M", "smooth", 54323, 3)
    girdle(g, "belt", 8.6, role="L", height=1)
    f, bk = over_flaps(g, "brigandine_skirt", 3, "P", "velvet", 54324, width=10, top=9.0)
    for face in (f, bk):
        studs(face, 0, 1)
        face.hline(0, face.w - 1, 2, "P1")
    # The key ring on a short chain at the left hip, three long keys hanging from it.
    chain = front_prop(g, "key_chain", 2.2, (1, 2, 1), drop=.4, z=-3.25)
    solid(chain, "M", "smooth", 54325, 1, edge=False)
    chain.front.set(0, 0, "M3")
    for name, x, drop, size in (("key_ring_top", 2.2, 2.4, (4, 1, 1)), ("key_ring_bottom", 2.2, 5.4, (4, 1, 1)),
                                ("key_ring_right", .7, 3.4, (1, 2, 1)), ("key_ring_left", 3.7, 3.4, (1, 2, 1))):
        part = front_prop(g, name, x, size, drop=drop, z=-3.25)
        solid(part, "M", "smooth", 54326, 2, edge=False)
        part.front.set(0, 0, "M3")
    for i, (x, length) in enumerate(((1.3, 5), (2.2, 6), (3.1, 4))):
        key = front_prop(g, f"key_{i}", x, (1, length, 1), drop=5.4, z=-3.5)
        solid(key, "M", "smooth", 54327 + i, 2, edge=False)
        key.front.set(0, 0, "M4"), key.front.set(0, length - 1, "M3")
        bit = front_prop(g, f"key_bit_{i}", x + .5, (1, 1, 1), drop=5.4 + length - 2, z=-3.5)
        solid(bit, "M", "smooth", 54330 + i, 2, edge=False)
