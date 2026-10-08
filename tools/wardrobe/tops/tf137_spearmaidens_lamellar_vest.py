"""Spearmaiden's Lamellar Vest: a vest of small laced plates over a wool tunic, lamellar shoulder guards, leather
bracers, and a long leaf-bladed spear slung diagonally across her back."""
from kit import sleeves
from kit_female import arm_rings, girdle
from kit_f04 import Rod, lamellae
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Spearmaiden's Lamellar Vest",
    "gender": "female",
    "description": "A vest of small laced lamellar plates over a wool tunic, with lamellar shoulder guards, leather "
                   "bracers and a leaf-bladed spear slung across her back.",
    "tags": ["armor", "martial"],
    "requires": ["sturdy"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "S", "weave", 54041, 2)
    fabric(b.top, "S", "weave", 54041, 3), fabric(b.bottom, "S", "weave", 54041, 1)
    b.front.hline(2, 5, 0, "S1")                                   # the tunic's round neck
    # The lamellar vest on the jacket layer: laced rows of plates, leather edging and shoulder straps.
    j = g.part("jacket")
    for face in j.sides:
        lamellae(face, 2, lace="L1", lace_hi="L2", y0=2, y1=10)
        face.hline(0, face.w - 1, 1, "L3")
        face.hline(0, face.w - 1, 11, "L1")
    for face in (j.front, j.back):
        for x in (0, 1, 6, 7):
            face.set(x, 0, "L2")
    for face in (j.right, j.left):
        face.hline(0, face.w - 1, 0, "L2")
    for x in (0, 1, 6, 7):
        j.top.vline(x, 0, j.top.h - 1, "L3")
    for y in range(2, 11):                                         # the side closure, laced up the left side
        j.left.set(1, y, "L3" if y % 2 else "S3")
        j.left.set(2, y, "S3" if y % 2 else "L3")
    # Tunic sleeves to the elbow, bare forearms in laced leather bracers.
    sleeves(g, "S", "weave", 54042, base=2, rows=(0, 5))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 5, "A2")
        strip_fabric(arm, "L", "leather", 54043, 2, 8, 11)
        arm.strip.hline(0, 15, 8, "L3"), arm.strip.hline(0, 15, 11, "L1")
        arm.front.set(1, 9, "S3"), arm.front.set(2, 10, "S3")
    for box in arm_rings(g, "lamellar_guard", -2.4, 4, 5, inflate=.1):
        solid(box, "M", "smooth", 54044, 2)
        for face in box.sides:
            lamellae(face, 2, lace="L1", lace_hi="L2", y0=1, y1=3)
            face.hline(0, face.w - 1, 0, "L3")
        fabric(box.top, "L", "leather", 54045, 2)
    girdle(g, "belt", 8.4, role="L", height=1)
    # The spear: butt by the right hip, rising past the left shoulder, the blade beside her head.
    rod = Rod(g, (-2.4, 10.6), (8.4, -7.4))
    rod.shaft("spear_shaft", 0, 17, "L", 2, 54046)
    heel = rod.piece("spear_heel", -.6, (1, 1, 1), inflate=.1)
    solid(heel, "M", "smooth", 54047, 2, edge=False)
    socket = rod.piece("spear_socket", 16.4, (1, 2, 1), inflate=.12)
    solid(socket, "M", "smooth", 54048, 2, edge=False)
    socket.front.set(0, 0, "M3"), socket.back.set(0, 0, "M3")
    tassel = rod.piece("spear_tassel", 15.0, (2, 1, 2), inflate=.05)
    solid(tassel, "A", "plain", 54049, 2, edge=False)
    blade = rod.piece("spear_blade", 18.2, (2, 3, 1))
    solid(blade, "M", "smooth", 54050, 3, edge=False)
    for f in (blade.front, blade.back):
        f.vline(0, 0, 2, "M4"), f.vline(1, 0, 2, "M2")             # the midrib catching the light
        f.set(0, 0, "M2"), f.set(1, 0, "M1")
    tip = rod.piece("spear_tip", 21.2, (1, 2, 1))
    solid(tip, "M", "smooth", 54051, 3, edge=False)
    tip.front.set(0, 0, "M4"), tip.back.set(0, 0, "M4")
    loop = rod.piece("spear_sling_loop", 8.0, (2, 1, 2), inflate=.05)
    solid(loop, "L", "leather", 54052, 1, edge=False)
    loop.back.set(1, 0, k("M", 3))
