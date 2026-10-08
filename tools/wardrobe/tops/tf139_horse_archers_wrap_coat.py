"""Horse Archer's Wrap Coat: a steppe riding coat wrapped across to the right with a broad trimmed edge, long coat
skirts open at the sides for the saddle, a plaque belt, a bow case at the left hip and a quiver at the right."""
from kit import sleeves
from kit_female import girdle, over_flaps
from kit_f04 import back_prop
from paint import fabric, k, line, solid, strip_fabric

META = {
    "name": "Horse Archer's Wrap Coat",
    "gender": "female",
    "description": "A riding coat wrapped across to the right with a broad trimmed edge and turned-back cuffs, a "
                   "plaque belt, and a bow case and quiver slung at the hips.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "twill", 54121, 2)
    fabric(b.top, "P", "twill", 54121, 3), fabric(b.bottom, "P", "twill", 54121, 1)
    b.front.set(3, 0, "S3"), b.front.set(4, 0, "S3")                 # the undershirt at the throat
    # The wrap: the left front crosses over to the wearer's right underarm, edged with a broad band.
    line(b.front, 5, 0, 0, 5, "A3"), line(b.front, 6, 0, 1, 5, "A2"), line(b.front, 7, 0, 2, 5, "A1")
    for x, y in ((6, 1), (7, 1), (7, 2)):
        b.front.set(x, y, "P2")
    b.right.vline(3, 5, 11, "A2"), b.right.vline(2, 5, 11, "A1")
    b.front.set(1, 4, "M3"), b.right.set(3, 7, "M3"), b.right.set(3, 10, "M3")   # toggles along the edge
    sleeves(g, "P", "twill", 54122, base=2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 9, "A3"), arm.strip.hline(0, 15, 10, "A2"), arm.strip.hline(0, 15, 11, "A1")
        arm.front.vline(1, 2, 8, "P1")
    j = g.part("jacket")
    for face in (j.right, j.left):
        face.vline(1, 0, 3, "P3")                                     # shoulder seams
    belt = girdle(g, "plaque_belt", 8.0, role="L", height=2, buckle=None)
    for face in belt.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "M3"), face.set(x, 1, "M1")                # small metal plaques
    belt.front.hline(3, 5, 0, "M4"), belt.front.hline(3, 5, 1, "M2")
    f, bk = over_flaps(g, "coat_skirt", 7, "P", "twill", 54123, width=10, top=9.0)
    f.vline(7, 0, 6, "A2"), f.vline(8, 0, 6, "A1")                    # the wrapped front edge runs on down
    for face in (f, bk):
        face.hline(0, face.w - 1, 6, "A2")
        face.vline(0, 1, 5, "P1"), face.vline(9, 1, 5, "P1")
    # Bow case at the left hip, behind the coat skirt, with the strung bow's horn tip curling out of it.
    case = back_prop(g, "bow_case", 2.8, (3, 7, 1), drop=.6, z=3.2, rotation=(0, 0, -14))
    solid(case, "L", "leather", 54124, 2)
    c = case.back
    c.vline(0, 0, 6, "A2"), c.vline(2, 0, 6, "L1")
    c.set(1, 2, "M3"), c.set(1, 4, "A3"), c.hline(0, 2, 6, "L0")
    limb = back_prop(g, "bow_limb", 2.8, (1, 3, 1), drop=-2.4, z=3.2, rotation=(0, 0, -14))
    solid(limb, "L", "smooth", 54125, 3, edge=False)
    limb.back.set(0, 0, "L1")
    ear = back_prop(g, "bow_ear", 2.8, (2, 1, 1), drop=-3.4, z=3.2, rotation=(0, 0, -14))
    solid(ear, "L", "smooth", 54126, 2, edge=False)
    ear.back.set(1, 0, "K1")
    # Quiver at the right hip, fletchings showing.
    quiver = back_prop(g, "quiver", -2.8, (2, 6, 2), drop=.8, z=3.2, rotation=(0, 0, 10))
    solid(quiver, "L", "leather", 54127, 1)
    for face in quiver.sides:
        face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 4, "A2")
    nocks = back_prop(g, "quiver_fletchings", -2.8, (2, 2, 1), drop=-1.2, z=3.7, rotation=(0, 0, 10))
    for face in nocks.faces:
        face.fill("S3")
    nocks.back.set(0, 0, "A3"), nocks.back.set(1, 1, "A2"), nocks.front.set(1, 0, k("A", 3))
