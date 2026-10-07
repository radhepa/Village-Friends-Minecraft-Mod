"""Sun Priestess's Robe: a sleeveless white robe with a great embroidered sun, a rayed collar and gold armbands."""
from kit_female import arm_rings, hanging, motif, mantle
from paint import fabric, solid, strip_fabric

META = {
    "name": "Sun Priestess's Robe",
    "gender": "female",
    "description": "A sleeveless temple robe with a great embroidered sun, a gilded rayed collar, gold armbands and a sash.",
    "tags": ["holy", "robe", "fancy"],
    "locked_to": "bf028_sun_priestess_skirt",
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "S", "weave", 12801, 3)
    fabric(b.top, "S", "weave", 12801, 4), fabric(b.bottom, "S", "weave", 12801, 2)
    motif(b.front, 1, 3, "bigsun", a="A2", b="M3", m="M4")
    b.back.vline(3, 1, 11, "S2"), b.back.vline(4, 1, 11, "S4")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 0, "S3")
    for box in arm_rings(g, "armband", 1.0, 1, 5, inflate=.06):
        solid(box, "M", "smooth", 12802, 3, edge=False)
        for face in box.sides:
            face.set(face.w // 2, 0, "A2")
    for box in arm_rings(g, "bracelet", 8.6, 1, 5, inflate=.06):
        solid(box, "M", "smooth", 12803, 3, edge=False)
    collar = mantle(g, "rayed_collar", "M", "smooth", 12804, 3, height=2, width=11, depth=6, y=-1.0)
    for face in collar.sides:
        for x in range(face.w):
            face.set(x, 1, "M4" if x % 2 else "A2")
    fabric(collar.top, "M", "smooth", 12805, 3)
    for x in range(collar.top.w):
        collar.top.set(x, 0, "M4" if x % 2 else "M2")
    sash = g.piece("sash", "TORSO", (-4.6, 7.8, -2.6), (9, 2, 5), inflate=.05)
    solid(sash, "A", "plain", 12806, 2, edge=False)
    for face in sash.sides:
        face.hline(0, face.w - 1, 0, "M3")
    for i, (x, length) in enumerate(((-.6, 10), (.6, 9))):
        tail = hanging(g, f"sash_end_{i}", x, length, role="A", top=9.0)
        tail.front.set(0, length - 1, "M3")
