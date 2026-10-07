"""Knight's Brigandine: a riveted velvet brigandine with an embroidered badge, steel gorget, pauldrons and plate faulds."""
from kit_female import arm_rings, girdle, mail, motif, over_flaps
from paint import fabric, solid, strip_fabric

META = {
    "name": "Knight's Brigandine",
    "gender": "female",
    "description": "A riveted velvet brigandine with a lily badge, steel gorget and pauldrons, mail sleeves and plate faulds.",
    "tags": ["armor", "martial"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "velvet", 12001, 2)
    fabric(b.top, "P", "velvet", 12001, 3), fabric(b.bottom, "P", "velvet", 12001, 1)
    for face in b.sides:
        for y in (1, 4, 7, 10):
            for x in range(0 if face.w > 4 else 1, face.w, 2):
                face.set(x, y, "M3")                                  # rivet rows
    motif(b.front, 3, 3, "lily", a="A2", b="A3", c="M3")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        mail(arm.strip, "M", 2, 0, 9)
        strip_fabric(arm, "M", "smooth", 12002, 3, 10, 11)
        arm.strip.hline(0, 15, 10, "M4")
        fabric(arm.top, "M", "smooth", 12003, 3)
    gorget = g.piece("gorget", "TORSO", (-4.5, -1.2, -2.6), (9, 2, 5), inflate=.1)
    solid(gorget, "M", "smooth", 12004, 3, edge=False)
    for face in gorget.sides:
        face.hline(0, face.w - 1, 0, "M4"), face.hline(0, face.w - 1, 1, "M2")
    for box in arm_rings(g, "pauldron", -2.6, 4, 6, inflate=.06):
        solid(box, "M", "smooth", 12005, 3)
        for face in box.sides:
            face.hline(0, face.w - 1, 1, "M1"), face.hline(0, face.w - 1, 3, "M1")
            face.set(face.w // 2, 0, "A2")
        box.top.fill("M4")
    girdle(g, "sword_belt", 8.2, role="L", height=1)
    f, bk = over_flaps(g, "faulds", 4, "M", "smooth", 12006, base=3, width=10, top=9.0)
    for face in (f, bk):
        for y in range(0, 4):
            face.hline(0, face.w - 1, y, "M4" if y % 2 == 0 else "M2")
        face.set(0, 1, "M3"), face.set(face.w - 1, 1, "M3")
