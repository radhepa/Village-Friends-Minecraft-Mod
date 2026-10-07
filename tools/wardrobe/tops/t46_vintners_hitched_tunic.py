"""Vintner's Hitched Tunic: a short-sleeved tunic hitched into the belt on one side, its hem grape-stained, with a billhook."""
from kit import belt, body, neckline, sleeves
from kit_male import blk, flecks
from paint import solid

META = {
    "name": "Vintner's Hitched Tunic",
    "gender": "male",
    "description": "A short-sleeved harvest tunic hitched up into the belt on one side, its hem stained with grape juice, and a pruning billhook.",
    "tags": ["casual", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 4601)
    neckline(b.front, "laced", "P")
    sleeves(g, "P", "weave", 4602, rows=(0, 3), cuff="P1")
    belt(g, "belt", 9.4, height=1)
    hitched = g.piece("hem_hitched", "TORSO", (-2, 0, 0), (4, 2, 1), pivot=(-2.1, 10.4, -2.85), motion="flap_front")
    solid(hitched, "P", "weave", 4603, 2)
    hitched.front.hline(0, 3, 0, "P3"), hitched.front.hline(0, 3, 1, "P1")
    for name, size, pivot, motion, face_name in (
            ("hem_long", (4, 5, 1), (2.1, 10.4, -2.85), "flap_front", "front"),
            ("hem_back", (9, 4, 1), (0, 10.4, 1.85), "flap_back", "back")):
        hem = g.piece(name, "TORSO", (-size[0] / 2, 0, 0), size, pivot=pivot, motion=motion)
        solid(hem, "P", "weave", 4604 + len(name), 2)
        face = getattr(hem, face_name)
        flecks(face, "A1", 4606, .2, rows=range(size[1] - 2, size[1]))   # grape stains
        face.hline(0, size[0] - 1, size[1] - 1, "P1")
    handle = blk(g, "billhook_handle", (3.0, 9.2, -2.8), (1, 2, 1), "L", 3, "plain", 4607)
    blade = blk(g, "billhook_blade", (3.0, 11.2, -2.8), (1, 3, 1), "M", 3, "smooth", 4608)
    blade.strip.hline(0, blade.strip.w - 1, 0, "M2")
    blk(g, "billhook_tip", (2.6, 13.2, -2.8), (2, 1, 1), "M", 3, "smooth", 4609, edge=False)
