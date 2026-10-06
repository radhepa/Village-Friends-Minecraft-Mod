"""Mail Skirt & Greaves: a short ring-mail skirt over quilted chausses, steel greaves, domed knee cops and sabatons."""
from kit import SIDES, leg_bone
from kit_female import mail, skirt
from paint import cap, fabric, solid, strip_fabric

META = {
    "name": "Mail Skirt & Greaves",
    "gender": "female",
    "description": "A ring-mail skirt to the knee over quilted chausses, with steel greaves, domed knee cops and sabatons.",
    "tags": ["armor", "martial", "sturdy", "skirt"],
    "requires": ["martial", "rugged", "armor"],
}


def build(g):
    s = skirt(g, "M", "smooth", 12011, top=9.6, length=6, folds=False, gather=False, flare=4)
    s.paint(lambda f: mail(f, "M", 2))
    s.hem("M1")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "quilt", 12012 + (side == "left"), 1, 0, 9)
        fabric(leg.top, "P", "quilt", 12012, 1)
        for face in pants.sides:
            if face is (pants.left if side == "right" else pants.right):
                continue
            fabric(face, "M", "smooth", 12014, 2, 0, 5, face.w, 5)
            face.hline(0, face.w - 1, 5, "M4"), face.hline(0, face.w - 1, 9, "M1")
        pants.front.vline(1 if side == "right" else 2, 6, 8, "M4")
        strip_fabric(leg, "L", "leather", 12015, 2, 10, 11)
        for face in pants.sides:
            fabric(face, "L", "leather", 12016, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K1")
        pants.front.hline(0, 3, 10, "M3"), pants.front.hline(0, 3, 11, "M2")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
        cop = g.piece(f"{side}_knee_cop", leg_bone(side), (-2, 0, -1), (4, 3, 2), pivot=(0, 3.6, -1.7))
        solid(cop, "M", "smooth", 12017, 3)
        cap(cop, "M", top_delta=1)
        cop.front.set(1, 1, "M4"), cop.front.set(2, 1, "M4"), cop.front.hline(0, 3, 2, "M1")
