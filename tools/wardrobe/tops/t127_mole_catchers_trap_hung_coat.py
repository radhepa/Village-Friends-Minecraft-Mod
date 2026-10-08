"""Mole Catcher's Trap-Hung Coat: a long drab wrap coat with a dark moleskin collar, deep pockets, and little wooden tube traps dangling on cords from the belt."""
from kit import belt, body, sleeves
from paint import solid

META = {
    "name": "Mole Catcher's Trap-Hung Coat",
    "gender": "male",
    "description": "A long drab wrap coat with a soft dark moleskin collar and deep pockets, a string of little iron-banded wooden tube traps dangling on cords from the belt.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}

TOP = 10.6


def hung(g, pid, x, y, size, z=-2.85, motion="flap_front", rotation=(0, 0, 0)):
    """A small piece hanging in front of the coat skirt that swings with it (origin relative to the flap pivot)."""
    w, h, d = size
    return g.piece(pid, "TORSO", (x - w / 2, y - TOP, -d), size, pivot=(0, TOP, z), motion=motion, rotation=rotation)


def build(g):
    b = body(g, "P", "twill", 31525)
    f = b.front
    for y in range(0, 12):                                                # the wrap's overlapping front edge
        x = min(6, 2 + y // 2)
        f.set(x, y, "P0"), f.set(x - 1, y, "P3")
    f.set(3, 2, "L3")                                                     # horn toggle at the chest
    for face in (b.right, b.left):
        face.vline(2, 1, 11, "P1")
    sleeves(g, "P", "twill", 31526, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in (8, 9, 10):                                              # turned-back cuffs show the lining
            arm.strip.hline(0, arm.strip.w - 1, y, "S2" if y != 8 else "S3")
        arm.strip.hline(0, arm.strip.w - 1, 7, "P1")
        for face in arm.sides:
            face.vline(1, 1, 6, "P1")
    # The moleskin collar: short dark velvet nap, lit along its roll.
    coll = g.piece("moleskin_collar", "TORSO", (-4.5, -1, -2.6), (9, 2, 5), inflate=.08)
    solid(coll, "K", "velvet", 31527, 2, edge=False)
    coll.top.fill("K3")
    for face in coll.sides:
        face.hline(0, face.w - 1, 0, "K3")
    coll.front.hline(3, 5, 1, "K1")                                       # where the wrap crosses
    belt(g, "belt", 9.4, height=1)
    # Coat skirts: long, a vent at the back, two deep patch pockets on the front.
    for name, z, motion, face_name in (("coat_front", -2.85, "flap_front", "front"), ("coat_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 6, 1), pivot=(0, TOP, z), motion=motion)
        solid(panel, "P", "twill", 31528 + (z > 0), 2)
        face = getattr(panel, face_name)
        face.hline(0, 8, 0, "P3"), face.hline(0, 8, 5, "P0")
        if face_name == "front":
            face.vline(5, 0, 5, "P0"), face.vline(4, 0, 5, "P3")          # wrap edge continues
            for x0 in (0, 6):
                face.hline(x0, x0 + 2, 1, "P3"), face.hline(x0, x0 + 2, 4, "P1")
                face.vline(x0, 1, 4, "P1"), face.vline(x0 + 2, 1, 4, "P1")
        else:
            face.vline(4, 2, 5, "P0")
    # Little wooden tube traps hanging on cords from the belt.
    for i, (x, drop) in enumerate(((-3.0, 1), (-1.0, 3), (2.9, 2))):
        cord = hung(g, f"trap_cord_{i}", x, 10.4, (1, drop, 1), z=-2.95)
        solid(cord, "S", "plain", 31530 + i, 2, edge=False)
        tube = hung(g, f"mole_trap_{i}", x, 10.4 + drop, (3, 1, 1), z=-2.95)
        solid(tube, "L", "plain", 31533 + i, 3, edge=False)
        tube.front.set(1, 0, "M3")                                        # the iron band round its middle
        tube.top.set(1, 0, "M3"), tube.bottom.set(1, 0, "M2")
        tube.right.fill("K0"), tube.left.fill("K0")                       # the hollow ends
