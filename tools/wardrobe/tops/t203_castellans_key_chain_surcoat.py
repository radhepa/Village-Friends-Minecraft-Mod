"""Castellan's Key-Chain Surcoat: a parti-coloured surcoat with a counterchanged tower over mail, and the castle keys on a chain."""
from kit import SIDES, body, sleeves
from kit_male import mail
from kit_m04 import chain, hanging, key_shape
from paint import k, solid

META = {
    "name": "Castellan's Key-Chain Surcoat",
    "gender": "male",
    "description": "A sleeveless surcoat parted down the middle in the two house colours and charged with a counterchanged "
                   "castle tower, worn over a mail shirt with quilted forearms, the castle's great keys hanging from the "
                   "belt on an iron chain.",
    "tags": ["armor", "martial", "fancy"],
    "requires": ["sturdy"],
    "covers_waist": True,
}

S = 34280

TOWER = ["t.tt.t",
         "tttttt",
         ".tttt.",
         ".tttt.",
         ".tddt.",
         ".tddt."]


def parti(face, x, back=False):
    """House colour on the wearer's right half, accent on the left (as seen on this face)."""
    right_half = (x >= 4) if back else (x < 4)
    return "P" if right_half else "A"


def build(g):
    b = body(g, "M", "smooth", S)
    for face in b.sides:
        mail(face, ox=face.x0)
    mail(b.top)
    jacket = g.part("jacket")
    for face, back in ((jacket.front, False), (jacket.back, True)):
        for y in range(12):
            for x in range(8):
                role = parti(face, x, back)
                face.set(x, y, k(role, 2 if (x + y) % 7 else 1))
        for dy, row in enumerate(TOWER):
            for dx, ch in enumerate(row):
                x = 1 + dx
                if ch == "t":
                    face.set(x, 2 + dy, k("A" if parti(face, x, back) == "P" else "P", 3))
                elif ch == "d":
                    face.set(x, 2 + dy, "K1")
        face.hline(0, 7, 0, "S3")                                          # bound edge
    jacket.front.rect(2, 0, 4, 1, None)
    for y in range(4):
        for x in range(8):
            jacket.top.set(x, y, k("P" if x < 4 else "A", 3) if y in (0, 3) else None)
    sleeves(g, "S", "quilt", S + 1, rows=(0, 10), cuff="L2")
    for side in SIDES:
        mail(g.part(f"{side}_arm").strip, rows=range(0, 6))
        g.part(f"{side}_arm").strip.hline(0, 15, 5, "M1")
    belt = g.piece("belt", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.08)
    solid(belt, "L", "leather", S + 2, 1, edge=False)
    belt.front.set(4, 0, "M3"), belt.front.set(1, 0, "M2")
    # Surcoat skirts, parted like the body, with a dagged hem.
    for name, z, motion, face_name, back in (("surcoat_front", -2.85, "flap_front", "front", False),
                                              ("surcoat_back", 1.85, "flap_back", "back", True)):
        panel = g.piece(name, "TORSO", (-4, 0, 0), (8, 6, 1), pivot=(0, 10.8, z), motion=motion)
        solid(panel, "P", "plain", S + 3, 2)
        face = getattr(panel, face_name)
        for y in range(6):
            for x in range(8):
                face.set(x, y, k(parti(face, x, back), 2 if y < 5 else (1 if x % 2 else 3)))
        face.vline(3 if not back else 4, 0, 4, k(parti(face, 3 if not back else 4, back), 1))
    # The keys: a chain from the belt to a ring hung with three great keys.
    links = hanging(g, "key_chain", -1.6, 10.6, (1, 3, 1), "M", 2, "smooth", S + 4, top=10.6, dz=-.1)
    chain(links)
    ring = hanging(g, "key_ring", -2.1, 13.6, (2, 1, 1), "M", 3, "smooth", S + 5, top=10.6, dz=-.1)
    ring.front.set(0, 0, "M4"), ring.front.set(1, 0, "M1")
    for i, (x, n) in enumerate(((-2.6, 3), (-1.6, 2), (-2.1, 4))):
        key = hanging(g, f"key_{i}", x, 14.6, (1, n, 1), "M", 2, "smooth", S + 6 + i, top=10.6, dz=-.2 - .3 * i)
        key_shape(key)
